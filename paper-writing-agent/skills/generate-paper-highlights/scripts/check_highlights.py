#!/usr/bin/env python3
"""Validate the number and character length of paper Highlights."""

from __future__ import annotations

import argparse
import json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "highlights",
        nargs="+",
        help="Highlight statements, each passed as one quoted argument.",
    )
    limits = parser.add_mutually_exclusive_group(required=True)
    limits.add_argument("--limit", type=int, help="Maximum Unicode code points, including spaces and punctuation.")
    limits.add_argument("--word-limit", type=int, help="Maximum whitespace-delimited words per item.")
    limits.add_argument("--no-limit", action="store_true", help="Check count/nonempty items without a length cap.")
    parser.add_argument(
        "--min-items",
        type=int,
        default=3,
        help="Minimum number of Highlights (default: 3).",
    )
    parser.add_argument(
        "--max-items",
        type=int,
        default=5,
        help="Maximum number of Highlights (default: 5).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.limit is not None and args.limit < 1:
        raise SystemExit("--limit must be a positive integer")
    if args.word_limit is not None and args.word_limit < 1:
        raise SystemExit("--word-limit must be a positive integer")
    if args.min_items < 1 or args.max_items < args.min_items:
        raise SystemExit("item-count bounds are invalid")

    items = []
    all_within_limit = True
    for index, statement in enumerate(args.highlights, start=1):
        length = len(statement)
        words = len(statement.split())
        within_limit = bool(statement.strip()) and (
            (args.limit is None or length <= args.limit)
            and (args.word_limit is None or words <= args.word_limit)
        )
        all_within_limit = all_within_limit and within_limit
        items.append(
            {
                "index": index,
                "characters": length,
                "words": words,
                "word_limit": args.word_limit,
                "nonempty": bool(statement.strip()),
                "limit": args.limit,
                "within_limit": within_limit,
                "text": statement,
            }
        )

    count = len(args.highlights)
    count_valid = args.min_items <= count <= args.max_items
    report = {
        "valid": count_valid and all_within_limit,
        "count": count,
        "count_valid": count_valid,
        "required_count": [args.min_items, args.max_items],
        "items": items,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
