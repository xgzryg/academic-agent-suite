#!/usr/bin/env python3
"""Check a structured journal report against the bundled Markdown risk lists."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class RiskEntry:
    category: str
    journal_name: str
    issns: tuple[str, ...]
    reason: str


def normalize_title(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold().replace("&", " and ")
    value = re.sub(r"[^\w]+", " ", value, flags=re.UNICODE)
    return " ".join(value.split())


def normalize_issn(value: str) -> str:
    return re.sub(r"[^0-9Xx]", "", value).upper()


def extract_issns(value: str) -> tuple[str, ...]:
    found = re.findall(r"\b\d{4}[- ]?\d{3}[\dXx]\b", value or "")
    return tuple(sorted({normalize_issn(item) for item in found}))


def parse_risk_list(path: Path) -> list[RiskEntry]:
    section = ""
    entries: list[RiskEntry] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("## "):
            if "On Hold" in line:
                section = "JCR On Hold"
            elif "Suppressed" in line:
                section = "JCR Suppressed"
            elif "预警" in line:
                section = "CAS warning list"
            else:
                section = ""
            continue
        if not section or not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if not cells or not cells[0].isdigit() or len(cells) < 2:
            continue
        name = cells[1]
        if section == "JCR On Hold":
            issns = extract_issns(cells[2] if len(cells) > 2 else "")
            reason = "On Hold"
        elif section == "JCR Suppressed":
            issns = ()
            reason = cells[2] if len(cells) > 2 else "Suppressed"
        else:
            issns = extract_issns(cells[2] if len(cells) > 2 else "")
            reason = cells[3] if len(cells) > 3 else "CAS warning"
        entries.append(RiskEntry(section, name, issns, reason))
    if not entries:
        raise ValueError(f"No risk entries parsed from {path}")
    return entries



def snapshot_metadata(path: Path) -> dict[str, str]:
    content = path.read_text(encoding="utf-8")
    match = re.search(r"统计截止\s*[:：]\s*(\d{4})(?:年|-)(\d{1,2})月?", content)
    if not match or not 1 <= int(match.group(2)) <= 12:
        raise ValueError("Risk list needs an explicit 统计截止: YYYY-MM or YYYY年M月 metadata line")
    return {"snapshot_file": path.name, "snapshot_through": f"{match.group(1)}-{int(match.group(2)):02d}"}

def extract_candidates(report: dict[str, Any]) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for group in report.get("groups", []):
        for journal in group.get("journals", []):
            name = str(journal.get("journal_name", "")).strip()
            if not name:
                raise ValueError("Every journal requires journal_name")
            raw_issns = journal.get("issns", [])
            if isinstance(raw_issns, str):
                raw_issns = [raw_issns]
            issns = sorted({normalize_issn(str(value)) for value in raw_issns if normalize_issn(str(value))})
            if not issns or any(not re.fullmatch(r"\d{7}[\dX]", item) for item in issns):
                raise ValueError(f"{name}: a correctly formatted ISSN/EISSN is required")
            candidates.append({"journal_name": name, "issns": issns})
    if not candidates:
        raise ValueError("No journals found in report groups")
    normalized_names = [normalize_title(item["journal_name"]) for item in candidates]
    if len(normalized_names) != len(set(normalized_names)):
        raise ValueError("Duplicate journal titles found in candidate report")
    used_issns: set[str] = set()
    for candidate in candidates:
        if used_issns.intersection(candidate["issns"]):
            raise ValueError("Duplicate journal identity found through shared ISSN/EISSN")
        used_issns.update(candidate["issns"])
    return candidates


def candidate_fingerprint(candidates: list[dict[str, Any]]) -> str:
    canonical = [
        {"journal_name": normalize_title(item["journal_name"]), "issns": sorted(item["issns"])}
        for item in candidates
    ]
    payload = json.dumps(canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def build_audit(report: dict[str, Any], entries: list[RiskEntry], risk_path: Path) -> dict[str, Any]:
    candidates = extract_candidates(report)
    metadata = snapshot_metadata(risk_path)
    risk_records = sorted([asdict(entry) for entry in entries], key=lambda row: (row["category"], row["journal_name"], row["issns"]))
    # Exact source records let the renderer detect a changed list without adding a hash.
    for record in risk_records:
        record["issns"] = list(record["issns"])
    matches: list[dict[str, Any]] = []
    counts: dict[str, int] = {}
    for entry in entries:
        counts[entry.category] = counts.get(entry.category, 0) + 1
    for candidate in candidates:
        candidate_name = normalize_title(candidate["journal_name"])
        candidate_issns = set(candidate["issns"])
        for entry in entries:
            title_match = candidate_name == normalize_title(entry.journal_name)
            issn_match = bool(candidate_issns.intersection(entry.issns))
            if title_match or issn_match:
                matched_by = []
                if title_match:
                    matched_by.append("normalized title")
                if issn_match:
                    matched_by.append("ISSN/EISSN")
                matches.append(
                    {
                        "journal_name": candidate["journal_name"],
                        "candidate_issns": candidate["issns"],
                        "risk_category": entry.category,
                        "risk_list_name": entry.journal_name,
                        "risk_list_issns": list(entry.issns),
                        "matched_by": matched_by,
                        "reason": entry.reason,
                    }
                )
    per_category_matches = {category: 0 for category in counts}
    for match in matches:
        per_category_matches[match["risk_category"]] += 1
    status = "clear" if not matches else "matches_found"
    if status == "clear":
        checked_categories = "；".join(f"{category} 命中 0 本" for category in counts)
        confirmation = (
            f"已使用指定历史快照核对全部 {len(candidates)} 本候选期刊：{checked_categories}。"
            f"此确认仅限该名单统计截止 {metadata['snapshot_through']} 的记录，不代表官方当前状态。"
        )
    else:
        confirmation = f"发现 {len(matches)} 项风险名单命中；请替换后重新核查。"
    return {
        "status": status,
        "checked_on": date.today().isoformat(),
        **metadata,
        "risk_entries": risk_records,
        "candidate_count": len(candidates),
        "candidate_fingerprint": candidate_fingerprint(candidates),
        "risk_entry_counts": counts,
        "match_counts": per_category_matches,
        "matches": matches,
        "confirmation": confirmation,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report_json", type=Path)
    parser.add_argument("--risk-list", required=True, type=Path)
    parser.add_argument("--write-audit", type=Path)
    args = parser.parse_args()
    try:
        report = json.loads(args.report_json.read_text(encoding="utf-8"))
        entries = parse_risk_list(args.risk_list)
        audit = build_audit(report, entries, args.risk_list)
        rendered = json.dumps(audit, ensure_ascii=False, indent=2)
        if args.write_audit:
            args.write_audit.parent.mkdir(parents=True, exist_ok=True)
            args.write_audit.write_text(rendered + "\n", encoding="utf-8")
        print(rendered)
        return 0 if audit["status"] == "clear" else 2
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
