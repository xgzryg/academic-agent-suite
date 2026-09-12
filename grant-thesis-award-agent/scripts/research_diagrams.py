#!/usr/bin/env python3
"""Generate editable SVG and native draw.io diagrams from explicit JSON inputs.

Python 3.9+, standard library only. No network, installation or data inference.
See examples/diagrams/README.md for input formats and commands.
"""
from __future__ import annotations

import argparse
from datetime import date, timedelta
import json
from pathlib import Path
import sys
import unicodedata
import xml.etree.ElementTree as ET

COLORS = {"process": ("#E8F0FA", "#386CB0"), "input": ("#EAF4EF", "#3B8266"),
          "evaluation": ("#FFF1DD", "#B97614"), "neutral": ("#FFFFFF", "#444444")}
RELATIONS = {"flow", "dependency", "association", "hypothesis", "activation", "inhibition"}
FONT = "Arial, Microsoft YaHei, Noto Sans CJK SC, sans-serif"


def text(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field}: expected non-empty text")
    return value.strip()


def collection(value, field):
    if not isinstance(value, list) or not value:
        raise ValueError(f"{field}: expected a non-empty list")
    if not all(isinstance(item, dict) for item in value):
        raise ValueError(f"{field}: every item must be an object")
    return value


def unique(items, field):
    seen = set()
    for item in items:
        key = text(item.get("id"), f"{field}.id")
        if key in seen:
            raise ValueError(f"{field}: duplicate id {key!r}")
        seen.add(key)
        item["id"] = key


def iso(value, field):
    value = text(value, field)
    try:
        result = date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{field}: expected valid YYYY-MM-DD date") from exc
    if result.isoformat() != value:
        raise ValueError(f"{field}: expected YYYY-MM-DD date")
    return result


def wrap(value, units=27):
    """Wrap using approximate display width; preserve explicit line breaks."""
    result = []
    for paragraph in value.split("\n"):
        line, width = "", 0
        for char in paragraph:
            size = 2 if unicodedata.east_asian_width(char) in "WF" else 1
            if width + size > units and line:
                result.append(line)
                line, width = "", 0
            line += char
            width += size
        result.append(line)
    return result


def svg_string(root):
    return ET.tostring(root, encoding="unicode", xml_declaration=False)


class Canvas:
    def __init__(self, title, width, height):
        self.svg = ET.Element("svg", {"xmlns": "http://www.w3.org/2000/svg",
            "viewBox": f"0 0 {width} {height}", "width": str(width), "height": str(height),
            "role": "img", "aria-label": title})
        ET.SubElement(self.svg, "title").text = title
        ET.SubElement(self.svg, "rect", x="0", y="0", width=str(width), height=str(height), fill="white")
        defs = ET.SubElement(self.svg, "defs")
        marker = ET.SubElement(defs, "marker", id="arrow", markerWidth="8", markerHeight="8",
            refX="7", refY="4", orient="auto", markerUnits="userSpaceOnUse")
        ET.SubElement(marker, "path", d="M0,0 L8,4 L0,8 Z", fill="#444444")
        marker = ET.SubElement(defs, "marker", id="inhibit", markerWidth="10", markerHeight="12",
            refX="8", refY="6", orient="auto", markerUnits="userSpaceOnUse")
        ET.SubElement(marker, "path", d="M8,0 L8,12", stroke="#444444", **{"stroke-width": "2"})
        self.mx = ET.Element("mxfile", host="app.diagrams.net")
        diagram = ET.SubElement(self.mx, "diagram", id="research-diagram", name=title)
        model = ET.SubElement(diagram, "mxGraphModel", page="1", pageWidth=str(width), pageHeight=str(height))
        self.root = ET.SubElement(model, "root")
        ET.SubElement(self.root, "mxCell", id="0")
        ET.SubElement(self.root, "mxCell", id="1", parent="0")
        self.counter = 0
        self.nodes = {}
        self.note(title, width / 2, 30, size=22, align="center", width=width-60)

    def cell(self, value, x, y, w, h, style, key=None):
        self.counter += 1
        ident = key or f"shape-{self.counter}"
        cell = ET.SubElement(self.root, "mxCell", id=ident, value=value,
            style=style+";html=0;fontFamily=Arial;", vertex="1", parent="1")
        ET.SubElement(cell, "mxGeometry", x=str(x), y=str(y), width=str(w), height=str(h), **{"as": "geometry"})
        return ident

    def note(self, value, x, y, size=15, align="left", width=700, native=True):
        lines = value.split("\n")
        anchor = {"left": "start", "center": "middle", "right": "end"}[align]
        for i, line in enumerate(lines):
            node = ET.SubElement(self.svg, "text", x=str(x), y=str(y+i*(size+5)),
                fill="#222222", **{"font-family": FONT, "font-size": str(size), "text-anchor": anchor})
            node.text = line
        xpos = x if align == "left" else x-width/2 if align == "center" else x-width
        if native:
            self.cell(value, xpos, y-size, width, len(lines)*(size+5),
                f"text;strokeColor=none;fillColor=none;align={align};verticalAlign=top;fontSize={size};whiteSpace=wrap")

    def box(self, key, label, x, y, w, h, role="process", ellipse=False):
        fill, stroke = COLORS[role]
        if ellipse:
            ET.SubElement(self.svg, "ellipse", cx=str(x+w/2), cy=str(y+h/2), rx=str(w/2), ry=str(h/2),
                fill=fill, stroke=stroke, **{"stroke-width": "1.6"})
        else:
            ET.SubElement(self.svg, "rect", x=str(x), y=str(y), width=str(w), height=str(h), rx="5",
                fill=fill, stroke=stroke, **{"stroke-width": "1.6"})
        lines = label.split("\n")
        top = y+h/2-(len(lines)-1)*10+5
        for i, line in enumerate(lines):
            node = ET.SubElement(self.svg, "text", x=str(x+w/2), y=str(top+i*20),
                fill="#222222", **{"font-family": FONT, "font-size": "16", "text-anchor": "middle"})
            node.text = line
        ident = "node-"+key
        style = ("ellipse" if ellipse else "rounded=1")+f";whiteSpace=wrap;align=center;verticalAlign=middle;fillColor={fill};strokeColor={stroke};fontSize=16"
        self.cell(label, x, y, w, h, style, ident)
        self.nodes[key] = (x, y, w, h, ident)

    def line(self, points, relation="association", source=None, target=None, label=""):
        attrs = {"points": " ".join(f"{x},{y}" for x, y in points), "fill": "none",
                 "stroke": "#444444", "stroke-width": "1.6"}
        if relation in {"dependency", "hypothesis"}:
            attrs["stroke-dasharray"] = "6 4"
        if relation != "association":
            attrs["marker-end"] = "url(#inhibit)" if relation == "inhibition" else "url(#arrow)"
        ET.SubElement(self.svg, "polyline", attrs)
        end = "none" if relation == "association" else "ERone" if relation == "inhibition" else "block"
        self.counter += 1
        attrs = {"id": f"edge-{self.counter}", "value": label, "edge": "1", "parent": "1",
            "style": f"edgeStyle=none;rounded=0;html=0;fontFamily=Arial;fontSize=14;strokeColor=#444444;endArrow={end};endFill=1;dashed={int(relation in {'dependency', 'hypothesis'})}"}
        if source:
            attrs["source"] = self.nodes[source][4]
        if target:
            attrs["target"] = self.nodes[target][4]
        cell = ET.SubElement(self.root, "mxCell", attrs)
        geo = ET.SubElement(cell, "mxGeometry", relative="1", **{"as": "geometry"})
        ET.SubElement(geo, "mxPoint", x=str(points[0][0]), y=str(points[0][1]), **{"as": "sourcePoint"})
        ET.SubElement(geo, "mxPoint", x=str(points[-1][0]), y=str(points[-1][1]), **{"as": "targetPoint"})
        if len(points)>2:
            array = ET.SubElement(geo, "Array", **{"as": "points"})
            for x, y in points[1:-1]:
                ET.SubElement(array, "mxPoint", x=str(x), y=str(y))
        if label:
            middle = points[len(points)//2]
            self.note(label, middle[0]+7, middle[1]-7, size=13, width=190, native=False)


def flow(data):
    nodes = collection(data.get("nodes"), "nodes")
    unique(nodes, "nodes")
    edges = data.get("edges", [])
    if not isinstance(edges, list) or not all(isinstance(e, dict) for e in edges):
        raise ValueError("edges: expected list of objects")
    occupied, row_h, lookup = set(), {}, {n["id"]: n for n in nodes}
    for node in nodes:
        node["label"] = text(node.get("label"), "node.label")
        for field in ("row", "col"):
            if type(node.get(field)) is not int or node[field] < 0:
                raise ValueError(f"node {node['id']}: {field} must be a nonnegative integer")
        slot = node["row"], node["col"]
        if slot in occupied:
            raise ValueError(f"two nodes occupy row,col {slot}")
        occupied.add(slot)
        role = node.get("role", "process")
        if role not in COLORS:
            raise ValueError(f"node {node['id']}: unknown role {role}")
        node["lines"] = "\n".join(wrap(node["label"]))
        node["height"] = max(58, len(node["lines"].split("\n"))*20+24)
        row_h[node["row"]] = max(row_h.get(node["row"], 0), node["height"])
    for edge in edges:
        if edge.get("source") not in lookup or edge.get("target") not in lookup:
            raise ValueError(f"edge references unknown source/target: {edge}")
        if edge["source"] == edge["target"]:
            raise ValueError("self-loop not supported; describe the distinct iteration step explicitly")
        if edge.get("type", "flow") not in RELATIONS:
            raise ValueError(f"unknown edge type: {edge.get('type')}")
        if not isinstance(edge.get("label", ""), str):
            raise ValueError("edge.label must be text")
    positions, y = {}, 86
    for row in sorted(row_h):
        positions[row] = y
        y += row_h[row]+100
    cols = sorted({n["col"] for n in nodes})
    column = {col: index for index, col in enumerate(cols)}
    canvas = Canvas(text(data.get("title"), "title"), max(700, len(cols)*290+60), y+70)
    for node in nodes:
        canvas.box(node["id"], node["lines"], 40+column[node["col"]]*290, positions[node["row"]],
            230, node["height"], node.get("role", "process"))
    for edge in edges:
        sx, sy, sw, sh, _ = canvas.nodes[edge["source"]]
        tx, ty, tw, th, _ = canvas.nodes[edge["target"]]
        if ty > sy:
            start, end = (sx+sw/2, sy+sh), (tx+tw/2, ty)
            mid = (start[1]+end[1])/2
            points = [start, (start[0], mid), (end[0], mid), end]
        elif ty < sy:
            start, end = (sx+sw/2, sy), (tx+tw/2, ty+th)
            side = max(sx+sw, tx+tw)+25
            points = [start, (start[0], sy-25), (side, sy-25), (side, end[1]+25), (end[0], end[1]+25), end]
        else:
            points = [(sx+sw if tx>sx else sx, sy+sh/2), (tx if tx>sx else tx+tw, ty+th/2)]
        canvas.line(points, edge.get("type", "flow"), edge["source"], edge["target"], edge.get("label", ""))
    kinds = sorted({e.get("type", "flow") for e in edges})
    legend = {"flow": "实线箭头=流程", "dependency": "虚线箭头=依赖", "association": "无箭头线=关联",
              "hypothesis": "虚线箭头=假设关系", "activation": "实线箭头=激活", "inhibition": "T端线=抑制"}
    canvas.note("；".join(legend[k] for k in kinds), 40, y, size=13, width=max(620, len(cols)*290))
    return canvas


def gantt(data):
    tasks = collection(data.get("tasks"), "tasks")
    unique(tasks, "tasks")
    for task in tasks:
        task["label"] = text(task.get("label"), "task.label")
        task["a"] = iso(task.get("start"), "task.start")
        task["b"] = iso(task.get("end"), "task.end")
        if task["a"] > task["b"]:
            raise ValueError(f"task {task['id']}: start is after end")
    start, end = min(t["a"] for t in tasks), max(t["b"] for t in tasks)
    span = (end-start).days+1
    ids = {t["id"]: t for t in tasks}
    for task in tasks:
        deps = task.get("depends_on", [])
        if not isinstance(deps, list) or not all(isinstance(d, str) for d in deps):
            raise ValueError("depends_on must be a list of task IDs")
        for dep in deps:
            if dep not in ids or dep == task["id"]:
                raise ValueError(f"task {task['id']}: invalid dependency {dep}")
            if ids[dep]["b"] >= task["a"]:
                raise ValueError(f"task {task['id']}: finish-to-start dependency {dep} overlaps or ends too late")
    rows = [max(62, len(wrap(t["label"], 25))*20+18) for t in tasks]
    deps = [f"{ids[d]['label']} → {t['label']}" for t in tasks for d in t.get("depends_on", [])]
    dependency_note = "\n".join(wrap("完成后开始："+"；".join(deps), 160)) if deps else ""
    c = Canvas(text(data.get("title"), "title"), 1150, sum(rows)+210+max(0, len(dependency_note.split("\n"))-2)*17)
    left, chart_w, top = 325, 770, 108
    c.note("任务 / Task", 35, 80)
    c.note("日期轴：结束日计入；前置关系按“完成后开始”核对", left, 65, size=13, width=800)
    offsets = sorted({round((span-1)*i/4) for i in range(5)})
    for offset in offsets:
        x = left+offset/span*chart_w
        c.line([(x, top-12), (x, top+sum(rows))])
        c.note((start+timedelta(days=offset)).isoformat(), x, 88, size=12, align="center", width=115)
    y = top
    for task, h in zip(tasks, rows):
        label = "\n".join(wrap(task["label"], 25))
        c.note(label, 35, y+24, width=270)
        x = left+(task["a"]-start).days/span*chart_w
        w = ((task["b"]-task["a"]).days+1)/span*chart_w
        c.box(task["id"], "", x, y+10, w, 25)
        c.note(f"{task['start']} → {task['end']}", left, y+55, size=12, width=800)
        y += h
    if deps:
        c.note(dependency_note, 35, y+35, size=12, width=1060)
    return c


def timeline(data):
    events = collection(data.get("events"), "events")
    unique(events, "events")
    for event in events:
        event["label"] = text(event.get("label"), "event.label")
        event["date_obj"] = iso(event.get("date"), "event.date")
        if not isinstance(event.get("description", ""), str):
            raise ValueError("event.description must be text")
    events.sort(key=lambda event: event["date_obj"])
    labels = ["\n".join(wrap(e["label"]+("\n"+e["description"] if e.get("description") else ""), 61)) for e in events]
    heights = [max(65, len(label.split("\n"))*20+24) for label in labels]
    c = Canvas(text(data.get("title"), "title"), 940, sum(heights)+len(events)*35+155)
    c.note("按事件逐项排列；日期标注真实时间，纵向距离不表示时间间隔", 40, 62, size=13, width=870)
    y = 92
    centers = []
    for event, label, h in zip(events, labels, heights):
        mid = y+h/2
        centers.append(mid)
        c.note(event["date"], 135, mid+5, align="right", width=125)
        c.box("marker-"+event["id"], "", 164, mid-6, 12, 12, ellipse=True)
        c.line([(177, mid), (213, mid)])
        c.box(event["id"], label, 218, y, 660, h)
        y += h+35
    if len(centers)>1:
        c.line([(170, centers[0]+8), (170, centers[-1]-8)], "flow")
    return c


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="UTF-8 JSON source")
    parser.add_argument("--output-base", required=True, type=Path, help="Output base path; creates .svg and .drawio without overwriting")
    args = parser.parse_args()
    outputs = [Path(str(args.output_base)+suffix) for suffix in (".svg", ".drawio")]
    try:
        for output in outputs:
            if output.exists():
                raise ValueError(f"output already exists: {output}; choose another output base")
        data = json.loads(args.input.read_text(encoding="utf-8-sig"))
        if not isinstance(data, dict):
            raise ValueError("input must be a JSON object")
        kind = data.get("type")
        if kind not in {"flow", "roadmap", "gantt", "timeline"}:
            raise ValueError("type must be flow, roadmap, gantt or timeline")
        canvas = flow(data) if kind in {"flow", "roadmap"} else gantt(data) if kind == "gantt" else timeline(data)
        payloads = [svg_string(canvas.svg), svg_string(canvas.mx)]
        for payload in payloads:
            ET.fromstring(payload)
        args.output_base.parent.mkdir(parents=True, exist_ok=True)
        for output, payload in zip(outputs, payloads):
            output.write_text('<?xml version="1.0" encoding="UTF-8"?>\n'+payload+"\n", encoding="utf-8")
        print(json.dumps({"status": "created", "type": kind, "outputs": [str(p.resolve()) for p in outputs]}, ensure_ascii=False))
        return 0
    except (OSError, ValueError, TypeError, KeyError, OverflowError) as exc:
        print(f"Input/output error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
