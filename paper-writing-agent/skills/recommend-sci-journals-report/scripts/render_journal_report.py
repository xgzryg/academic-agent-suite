#!/usr/bin/env python3
"""Render a verified journal-selection JSON file as a styled self-contained HTML report."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from check_journal_risk import build_audit, candidate_fingerprint, extract_candidates, parse_risk_list


FIELDS = [
    ("fit", "推荐理由"),
    ("jif", "影响因子（年份）"),
    ("quartile", "JCR 分区（体系/学科/年份）"),
    ("field_ranking", "学科排名（年份）"),
    ("articles_per_year", "年发文量（周期/统计口径）"),
    ("oa_apc", "开放获取与版面费（OA/APC）"),
    ("first_decision", "首次决定"),
    ("first_peer_review_comments", "首轮外审意见"),
    ("evidence_status", "证据状态/待确认项"),
]

COMMON_TRANSLATIONS = {
    "Not found publicly": "官网未公开",
    "Official exact rank not publicly accessible": "官方精确排名无法公开获取",
    "APC amount not found publicly": "官网未公开 APC 金额",
    "Official source": "官方来源",
    "Verified": "已核实",
    "Calculated/approximate": "计算/近似",
    "Conflicting": "来源冲突",
    "Not found": "未查到",
}

GROUP_LABELS = {
    "q1-journals": "Q1 期刊",
    "q2-journals": "Q2 期刊",
    "broad-journals": "综合性期刊",
}


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True).replace("\n", "<br>")


def localize(value: Any) -> str:
    text = str(value)
    for source, target in COMMON_TRANSLATIONS.items():
        text = text.replace(source, target)
    return text


def safe_url(value: str) -> str:
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"Unsafe or invalid source URL: {value}")
    return html.escape(value, quote=True)


def slug(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip()).strip("-")
    return value or "section"


def list_html(items: list[Any], empty: str = "暂无") -> str:
    if not items:
        return f"<p>{esc(empty)}</p>"
    return "<ul>" + "".join(f"<li>{esc(localize(item))}</li>" for item in items) + "</ul>"


def source_links(journal: dict[str, Any], key: str) -> str:
    sources = journal.get("sources", {}).get(key, [])
    if not sources:
        return ""
    links = []
    for source in sources:
        label = esc(localize(source.get("label", "来源")))
        url = safe_url(str(source.get("url", "")))
        links.append(f'<a href="{url}" target="_blank" rel="noopener noreferrer">{label}</a>')
    return '<div class="sources">' + " · ".join(links) + "</div>"


def validate(report: dict[str, Any], audit: dict[str, Any], risk_path: Path) -> tuple[list[dict[str, Any]], int]:
    for key in ("paper_title", "research_date", "groups"):
        if not report.get(key):
            raise ValueError(f"Missing required report field: {key}")
    fresh = build_audit(report, parse_risk_list(risk_path), risk_path)
    for key in fresh:
        if audit.get(key) != fresh[key]:
            raise ValueError(f"Risk audit is stale or mismatched at {key}; rerun the checker for this candidate list and actual risk file")
    if audit.get("status") != "clear" or audit.get("matches"):
        raise ValueError("Risk audit is not clear; replace matched journals and rerun the checker")
    candidates = extract_candidates(report)
    expected = int(report.get("expected_journal_count", 15))
    if len(candidates) != expected:
        raise ValueError(f"Expected {expected} journals, found {len(candidates)}")
    if audit.get("candidate_count") != len(candidates):
        raise ValueError("Risk audit candidate count does not match the report")
    if audit.get("candidate_fingerprint") != candidate_fingerprint(candidates):
        raise ValueError("Risk audit fingerprint does not match the final journal list")
    for group in report["groups"]:
        if not group.get("title") or not isinstance(group.get("journals"), list):
            raise ValueError("Every group requires title and journals")
        for journal in group["journals"]:
            for key in ("rank", "journal_name", "journal_url", "issns"):
                if not journal.get(key):
                    raise ValueError(f"Journal missing required field {key}: {journal.get('journal_name', 'unknown')}")
            safe_url(str(journal["journal_url"]))
            for key, _ in FIELDS:
                if key not in journal or str(journal[key]).strip() == "":
                    raise ValueError(f"{journal['journal_name']}: missing {key}")
    return candidates, expected


def render_table(group: dict[str, Any]) -> str:
    headers = ["序号", "期刊名称"] + [label for _, label in FIELDS]
    rows = []
    for journal in group["journals"]:
        homepage = safe_url(str(journal["journal_url"]))
        issns = ", ".join(esc(value) for value in journal["issns"])
        cells = [
            f"<td>{esc(journal['rank'])}</td>",
            (
                f'<td><a class="journal" href="{homepage}" target="_blank" rel="noopener noreferrer">'
                f"{esc(journal['journal_name'])}</a><div class=\"issn\">ISSN/EISSN: {issns}</div></td>"
            ),
        ]
        for key, _ in FIELDS:
            cells.append(f"<td>{esc(localize(journal[key]))}{source_links(journal, key)}</td>")
        rows.append("<tr>" + "".join(cells) + "</tr>")
    return (
        '<div class="table-wrap"><table><thead><tr>'
        + "".join(f"<th>{esc(header)}</th>" for header in headers)
        + "</tr></thead><tbody>"
        + "".join(rows)
        + "</tbody></table></div>"
    )


def render(report: dict[str, Any], audit: dict[str, Any], risk_path: Path) -> str:
    _, expected = validate(report, audit, risk_path)
    profile = report.get("profile", [])
    profile_html = "<ul>" + "".join(
        f"<li><strong>{esc(localize(item.get('label', '项目')))}</strong>：{esc(localize(item.get('text', '')))}</li>" for item in profile
    ) + "</ul>"
    group_sections = []
    nav_links = ['<a href="#profile">论文画像</a>']
    for index, group in enumerate(report["groups"], 1):
        section_id = slug(str(group.get("id") or f"group-{index}"))
        group_label = GROUP_LABELS.get(section_id)
        display_title = f"{group_label}（{len(group['journals'])} 本）" if group_label else localize(group["title"])
        nav_links.append(f'<a href="#{section_id}">{esc(display_title)}</a>')
        group_sections.append(f'<section><h2 id="{section_id}">{esc(display_title)}</h2>{render_table(group)}</section>')
    nav_links.extend(
        [
            '<a href="#submission-order">投稿顺序</a>',
            '<a href="#risk-check">风险核查</a>',
        ]
    )
    match_counts = audit.get("match_counts", {})
    risk_counts = "；".join(f"{esc(key)} 命中 {esc(value)} 本" for key, value in match_counts.items())
    risk_section = f"""
      <section class="risk-clear">
        <h2 id="risk-check">风险期刊核查</h2>
        <p class="status"><span aria-hidden="true">✓</span> 全部 {expected} 本候选期刊通过指定快照核查</p>
        <p>{esc(audit.get('confirmation', ''))}</p>
        <p><strong>逐表结果</strong>：{risk_counts}</p>
        <p><strong>快照文件</strong>：{esc(audit.get('snapshot_file', ''))}；<strong>统计截止</strong>：{esc(audit.get('snapshot_through', ''))}；<strong>核查日期</strong>：{esc(audit.get('checked_on', ''))}</p>
        <p class="fingerprint"><strong>候选清单指纹</strong>：<code>{esc(audit.get('candidate_fingerprint', ''))}</code></p>
        <blockquote>此结果仅确认最终候选清单未命中指定快照，不等同于期刊在所有时间、所有数据库或所有风险维度上“绝对无风险”。</blockquote>
      </section>
    """
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="选刊推荐、OA/APC 与风险核查报告">
  <title>选刊推荐报告｜{esc(report['paper_title'])}</title>
  <style>
    :root {{ color-scheme: light; --ink:#17212b; --muted:#5d6975; --paper:#fff; --canvas:#f2f5f3; --line:#dce4df; --brand:#0e6958; --brand-dark:#084a3e; --brand-soft:#e7f3ef; --accent:#b56d1c; --shadow:0 16px 40px rgba(20,48,41,.09); }}
    * {{ box-sizing:border-box; }} html {{ scroll-behavior:smooth; }}
    body {{ margin:0; color:var(--ink); background:radial-gradient(circle at 8% 0%,rgba(14,105,88,.09),transparent 28rem),var(--canvas); font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif; font-size:16px; line-height:1.72; }}
    a {{ color:var(--brand); text-decoration-thickness:1px; text-underline-offset:3px; }} a:hover {{ color:var(--brand-dark); }}
    .page {{ width:min(1600px,calc(100% - 32px)); margin:28px auto 56px; }}
    .hero {{ padding:44px clamp(24px,5vw,72px) 38px; color:#fff; background:linear-gradient(128deg,#073d34 0%,#0e6958 62%,#197d68 100%); border-radius:22px 22px 0 0; box-shadow:var(--shadow); }}
    .eyebrow {{ margin:0 0 12px; color:#bfe4d9; font-size:13px; font-weight:750; letter-spacing:.14em; text-transform:uppercase; }}
    .hero h1 {{ margin:0; font-size:clamp(30px,5vw,54px); line-height:1.14; letter-spacing:-.035em; }} .hero p {{ max-width:1050px; margin:18px 0 0; color:#e7f4f0; font-size:clamp(15px,2vw,19px); }}
    .meta {{ display:flex; flex-wrap:wrap; gap:10px; margin-top:22px; }} .meta span {{ padding:5px 11px; border:1px solid rgba(255,255,255,.24); border-radius:999px; background:rgba(255,255,255,.08); font-size:13px; }}
    .nav {{ position:sticky; top:0; z-index:10; display:flex; gap:8px; overflow-x:auto; padding:12px clamp(16px,4vw,54px); background:rgba(255,255,255,.95); border-bottom:1px solid var(--line); box-shadow:0 6px 16px rgba(31,56,49,.06); backdrop-filter:blur(12px); scrollbar-width:thin; }}
    .nav a {{ flex:0 0 auto; padding:7px 11px; color:var(--brand-dark); border-radius:8px; font-size:13px; font-weight:700; text-decoration:none; }} .nav a:hover {{ background:var(--brand-soft); }}
    main {{ padding:38px clamp(18px,4vw,56px) 58px; background:var(--paper); border-radius:0 0 22px 22px; box-shadow:var(--shadow); }}
    h2 {{ scroll-margin-top:76px; margin:54px 0 20px; padding-bottom:10px; color:var(--brand-dark); border-bottom:2px solid var(--brand-soft); font-size:clamp(23px,3vw,31px); line-height:1.3; font-weight:800; letter-spacing:-.02em; }} h2:first-of-type {{ margin-top:14px; }}
    p {{ margin:12px 0; }} ul,ol {{ padding-left:1.45em; }} li {{ margin:7px 0; }} strong {{ color:#102f29; font-weight:800; }}
    code {{ padding:2px 5px; color:#084a3e; background:#e7f3ef; border-radius:4px; font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; font-size:.86em; overflow-wrap:anywhere; }}
    blockquote {{ margin:20px 0; padding:14px 18px; color:#40504a; background:var(--brand-soft); border-left:4px solid var(--brand); border-radius:0 10px 10px 0; }}
    .table-wrap {{ margin:22px 0 32px; overflow-x:auto; border:1px solid var(--line); border-radius:12px; box-shadow:0 4px 14px rgba(25,54,46,.05); }}
    table {{ width:100%; min-width:1600px; border-collapse:collapse; font-size:13px; line-height:1.48; }} th,td {{ padding:12px 13px; text-align:left; vertical-align:top; border-right:1px solid var(--line); border-bottom:1px solid var(--line); }} th:last-child,td:last-child {{ border-right:0; }} tr:last-child td {{ border-bottom:0; }}
    thead th {{ position:sticky; top:0; z-index:1; color:#fff; background:var(--brand-dark); font-size:12px; line-height:1.35; }} tbody tr:nth-child(even) {{ background:#f8faf9; }} tbody tr:hover {{ background:#eff7f4; }}
    td:first-child {{ width:52px; color:var(--accent); font-weight:800; text-align:center; }} td:nth-child(2) {{ min-width:210px; }} .journal {{ color:var(--brand-dark); font-weight:800; }} .issn {{ margin-top:5px; color:var(--muted); font-size:11px; }} .sources {{ margin-top:7px; font-size:11px; line-height:1.45; }}
    .risk-clear {{ padding:1px 20px 20px; background:#f4faf7; border:1px solid #b9dccf; border-radius:14px; }} .risk-clear .status {{ color:var(--brand-dark); font-size:18px; font-weight:800; }} .fingerprint {{ color:var(--muted); font-size:12px; }}
    .footer {{ padding:22px; color:var(--muted); text-align:center; font-size:13px; }} .print-button {{ position:fixed; right:22px; bottom:22px; z-index:20; padding:10px 15px; color:#fff; background:var(--brand); border:0; border-radius:999px; box-shadow:0 8px 22px rgba(8,74,62,.25); cursor:pointer; font:inherit; font-size:14px; font-weight:700; }} .print-button:hover {{ background:var(--brand-dark); }}
    @media (max-width:720px) {{ .page {{ width:100%; margin:0; }} .hero,main {{ border-radius:0; }} .hero {{ padding-top:34px; }} main {{ padding-top:24px; }} h2 {{ margin-top:42px; }} .print-button {{ right:14px; bottom:14px; }} }}
    @media print {{ @page {{ size:A4 landscape; margin:12mm; }} body {{ background:#fff; font-size:10pt; }} .page {{ width:100%; margin:0; }} .hero {{ padding:18px 24px; border-radius:0; box-shadow:none; print-color-adjust:exact; -webkit-print-color-adjust:exact; }} .hero h1 {{ font-size:25pt; }} .hero p {{ font-size:10pt; }} .nav,.print-button {{ display:none; }} main {{ padding:12px 0; border-radius:0; box-shadow:none; }} h2 {{ break-after:avoid; margin-top:22px; font-size:17pt; }} .table-wrap {{ overflow:visible; box-shadow:none; }} table {{ min-width:0; font-size:6pt; }} th,td {{ padding:4px; }} thead {{ display:table-header-group; }} tr {{ break-inside:avoid; }} thead th {{ position:static; print-color-adjust:exact; -webkit-print-color-adjust:exact; }} a {{ color:inherit; text-decoration:none; }} .footer {{ display:none; }} }}
  </style>
</head>
<body>
  <div class="page">
    <header class="hero"><p class="eyebrow">SCI 论文投稿决策支持</p><h1>选刊推荐报告</h1><p><em>{esc(report['paper_title'])}</em></p><div class="meta"><span>{expected} 本候选期刊</span><span>学科排名 · OA/APC · 风险核查</span><span>研究日期：{esc(report['research_date'])}</span></div></header>
    <nav class="nav" aria-label="报告章节导航">{''.join(nav_links)}</nav>
    <main>
      <section><h2 id="profile">一、论文画像与选刊口径</h2>{profile_html}<h3>选刊与数据口径</h3>{list_html(report.get('selection_notes', []))}</section>
      {''.join(group_sections)}
      <section><h2 id="submission-order">建议投稿顺序</h2>{list_html(report.get('submission_order', []))}</section>
      {risk_section}
      <section><h2 id="uncertainties">不确定性与投稿前确认</h2>{list_html(report.get('uncertainties', []), '暂无未解决事项')}</section>
      <section><h2 id="sources">来源范围与访问日期</h2>{list_html(report.get('source_scope', []))}</section>
    </main>
    <footer class="footer">本报告用于辅助投稿决策，不预测或保证录用。</footer>
  </div>
  <button class="print-button" type="button" onclick="window.print()">打印 / 保存 PDF</button>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report_json", type=Path)
    parser.add_argument("--risk-audit", required=True, type=Path)
    parser.add_argument("--risk-list", required=True, type=Path, help="Actual dated risk list to recompute before rendering")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        report = json.loads(args.report_json.read_text(encoding="utf-8"))
        audit = json.loads(args.risk_audit.read_text(encoding="utf-8"))
        rendered = render(report, audit, args.risk_list)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        verify = args.output.read_text(encoding="utf-8")
        for sentinel in ("<!doctype html>", "#073d34", "#0e6958", "选刊推荐报告", "学科排名（年份）", "开放获取与版面费（OA/APC）", "风险期刊核查", "</html>"):
            if sentinel not in verify:
                raise ValueError(f"Rendered HTML failed sentinel check: {sentinel}")
        print(args.output.resolve())
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
