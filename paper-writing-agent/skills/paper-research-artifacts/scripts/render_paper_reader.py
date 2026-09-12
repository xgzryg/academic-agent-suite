#!/usr/bin/env python3
"""Render prepared paper-reading HTML fragments with an offline reading layout.

Python 3.10+, standard library only. No literature retrieval or text generation.
"""

import argparse
import base64
import html
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import quote, unquote, urlsplit, urlunsplit


TEMPLATE = Path(__file__).resolve().parents[1] / "assets" / "paper-reader.html"
IMAGE_TYPES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
               ".svg": "image/svg+xml", ".gif": "image/gif", ".webp": "image/webp"}


def text_field(data, name, required=False, default=""):
    value = data.get(name, default)
    if not isinstance(value, str) or (required and not value.strip()):
        raise ValueError(f"{name} must be {'a nonempty' if required else 'a'} string")
    return value


class Fragment(HTMLParser):
    """Keep prepared content, embed local images, and make wide tables scrollable."""

    def __init__(self, input_dir, output_dir, known_ids):
        super().__init__(convert_charrefs=False)
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.known_ids = known_ids
        self.parts = []
        self.fragment_links = []
        self.image_count = 0

    def image_source(self, value):
        if value.startswith("data:image/"):
            return value
        parsed = urlsplit(value)
        if parsed.scheme or parsed.netloc:
            raise ValueError("Images must be local relative paths or data:image URLs; download authorized images before rendering")
        path = self.input_dir / unquote(parsed.path)
        if not path.is_file():
            raise ValueError(f"Image file does not exist: {path}")
        media_type = IMAGE_TYPES.get(path.suffix.lower())
        if not media_type:
            raise ValueError(f"Unsupported image format: {path.suffix}; use PNG/JPEG/SVG/GIF/WebP")
        return f"data:{media_type};base64," + base64.b64encode(path.read_bytes()).decode("ascii")

    def source_link(self, value):
        parsed = urlsplit(value)
        if parsed.scheme or parsed.netloc or not parsed.path:
            return value
        path = self.input_dir / unquote(parsed.path)
        if not path.exists():
            raise ValueError(f"Local source link does not exist: {path}")
        try:
            relative = Path(os.path.relpath(path, self.output_dir)).as_posix()
        except ValueError:  # Windows source and output on different existing drives.
            return path.resolve().as_uri() + ("#" + parsed.fragment if parsed.fragment else "")
        return urlunsplit(("", "", quote(relative, safe="/"), parsed.query, parsed.fragment))

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "link", "iframe", "object", "embed", "video", "audio", "source", "base"}:
            raise ValueError(f"<{tag}> is not part of the reading-fragment interface; supply prepared text, tables, images, inline SVG or MathML")
        attrs = dict(attrs)
        anchor = attrs.get("id")
        if anchor is not None:
            if not anchor or re.search(r"\s", anchor) or anchor.startswith("pwa-") or anchor in self.known_ids:
                raise ValueError(f"Empty, duplicate, reserved or whitespace-containing source ID: {anchor!r}")
            self.known_ids.add(anchor)
        if tag == "img":
            if "srcset" in attrs:
                raise ValueError("Use one local image src rather than srcset so the output stays self-contained")
            if not attrs.get("src"):
                raise ValueError("Every image requires src")
            if not attrs.get("alt"):
                raise ValueError("Every paper image requires an evidence-based alt description")
            attrs["src"] = self.image_source(attrs["src"])
            attrs.setdefault("loading", "lazy")
            attrs.setdefault("decoding", "async")
            self.image_count += 1
        if "href" in attrs and tag == "a":
            value = attrs["href"] or ""
            if value.startswith("#") and len(value) > 1:
                self.fragment_links.append(unquote(value[1:]))
            attrs["href"] = self.source_link(value)
        # Remote CSS/SVG resources would contradict the offline fragment interface.
        for key, value in attrs.items():
            if key.lower().startswith("on") or (key == "style" and value and re.search(r"url\s*\(", value, re.I)):
                raise ValueError("Reading fragments do not accept event handlers or CSS resource URLs")
            if tag != "a" and key in {"href", "xlink:href"} and value and not value.startswith(("#", "data:")):
                raise ValueError("Inline graphics must not depend on external resources")
        if tag == "table":
            self.parts.append('<div class="table-scroll" role="region" aria-label="可横向滚动的数据表" tabindex="0">')
        if tag in {"img", "a"}:
            attributes = "".join(" " + key if value is None else f' {key}="{html.escape(value, quote=True)}"' for key, value in attrs.items())
            self.parts.append(f"<{tag}{attributes}>")
        else:
            # Preserve SVG/MathML attribute case (for example viewBox) and markup.
            self.parts.append(self.get_starttag_text())

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag == "a":
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        self.parts.append(f"</{tag}>")
        if tag == "table":
            self.parts.append("</div>")

    def handle_data(self, data):
        self.parts.append(data)

    def handle_entityref(self, name):
        self.parts.append(f"&{name};")

    def handle_charref(self, name):
        self.parts.append(f"&#{name};")

    def handle_comment(self, data):
        self.parts.append(f"<!--{data}-->")


def render(data, input_dir, output_dir):
    if not isinstance(data, dict):
        raise ValueError("Input JSON must be an object")
    title = text_field(data, "title", required=True)
    coverage = text_field(data, "coverage", required=True)
    sections = data.get("sections")
    if not isinstance(sections, list) or not sections:
        raise ValueError("sections must be a nonempty array")
    metadata = data.get("metadata", [])
    if not isinstance(metadata, list) or any(not isinstance(item, str) for item in metadata):
        raise ValueError("metadata must be an array of strings")
    known_ids = {"pwa-top", "pwa-content"}
    for section in sections:
        if not isinstance(section, dict):
            raise ValueError("Each section must be an object")
        anchor = text_field(section, "id", required=True)
        if re.search(r"\s", anchor) or anchor.startswith("pwa-") or anchor in known_ids:
            raise ValueError(f"Duplicate, reserved or whitespace-containing section ID: {anchor!r}")
        known_ids.add(anchor)
    toc, content, links = [], [], []
    image_count = 0
    for index, section in enumerate(sections, 1):
        anchor = html.escape(section["id"], quote=True)
        heading = html.escape(text_field(section, "title", required=True))
        fragment = Fragment(input_dir, output_dir, known_ids)
        fragment.feed(text_field(section, "html", required=True))
        fragment.close()
        links.extend(fragment.fragment_links)
        image_count += fragment.image_count
        toc.append(f'<li><a href="#{quote(section["id"], safe="")}" data-section="{anchor}"><span class="toc-number">{index:02}</span><span>{heading}</span></a></li>')
        content.append(f'<section class="reader-section" id="{anchor}"><div class="section-heading"><span class="section-number">{index:02}</span><h2>{heading}</h2></div>{"".join(fragment.parts)}</section>')
    missing = sorted(set(links) - known_ids)
    if missing:
        raise ValueError("Internal source links have no matching ID: " + ", ".join(missing))
    subtitle = text_field(data, "subtitle")
    values = {"LANG": html.escape(text_field(data, "lang", default="zh-CN"), quote=True),
              "TITLE": html.escape(title), "EYEBROW": html.escape(text_field(data, "label", default="PAPER READER / 学术阅读")),
              "SUBTITLE": f'<p class="subtitle">{html.escape(subtitle)}</p>' if subtitle else "",
              "METADATA": "".join(f"<span>{html.escape(item)}</span>" for item in metadata),
              "COVERAGE": html.escape(coverage), "TOC": "\n".join(toc), "SECTIONS": "\n".join(content)}
    template = TEMPLATE.read_text(encoding="utf-8")
    result = re.sub(r"@@([A-Z]+)@@", lambda match: values[match.group(1)], template)
    return result, {"sections": len(sections), "images_embedded": image_count, "source_ids": len(known_ids) - 2}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="UTF-8 JSON with title, coverage and prepared sections")
    parser.add_argument("--output", type=Path, required=True, help="HTML in the user's task/output directory")
    args = parser.parse_args()
    try:
        source = args.input.resolve()
        destination = args.output.resolve()
        skill_dir = Path(__file__).resolve().parents[1]
        if destination == source or destination.is_relative_to(skill_dir):
            raise ValueError("Choose a task output path; do not overwrite the input or write into the installed skill")
        data = json.loads(source.read_text(encoding="utf-8-sig"))
        result, info = render(data, source.parent, destination.parent)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(result, encoding="utf-8")
        print(json.dumps({"output": str(destination), **info}, ensure_ascii=False))
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
