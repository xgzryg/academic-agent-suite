#!/usr/bin/env python3
"""Count explicitly selected UTF-8 plain text without modifying inputs.

english-words: whitespace-separated tokens containing a letter or digit;
hyphenated words and contractions remain one token. This is an explicit
working convention, not a claim to reproduce every journal or Word counter.
nonspace-characters: all Unicode non-whitespace characters, including punctuation.
"""
import argparse
import json
from pathlib import Path


def count_text(text, mode):
    if mode == "english-words":
        return sum(any(char.isalnum() for char in token) for token in text.split())
    return sum(not char.isspace() for char in text)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument(
        "--mode",
        choices=("english-words", "nonspace-characters"),
        default="english-words",
    )
    args = parser.parse_args()
    records = []
    for path in args.files:
        if not path.is_file():
            parser.error("Input file does not exist: " + str(path))
        text = path.read_text(encoding="utf-8-sig")
        records.append({"file": str(path.resolve()), "count": count_text(text, args.mode)})
    result = {"mode": args.mode, "scope": "entire content of each supplied plain-text file", "files": records}
    if len(records) == 2:
        original, revised = (record["count"] for record in records)
        result["reduction"] = original - revised
        result["reduction_percent"] = round(100 * (original - revised) / original, 2) if original else None
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

