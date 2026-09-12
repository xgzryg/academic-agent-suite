# Report data schema

Create a UTF-8 JSON object with these fields:

```json
{
  "paper_title": "稿件的准确英文标题",
  "research_date": "YYYY-MM-DD",
  "expected_journal_count": 15,
  "profile": [
    {"label": "文章类型/研究设计", "text": "根据稿件整理的中文概述"}
  ],
  "selection_notes": ["JCR 分区体系、年份及年发文量统计口径说明"],
  "groups": [
    {
      "id": "q1-journals",
      "title": "Q1 期刊（5 本）",
      "journals": [
        {
          "rank": 1,
          "journal_name": "期刊官方英文名称",
          "journal_url": "https://official.example/",
          "issns": ["1234-5678", "8765-4321"],
          "fit": "中文说明稿件与期刊的匹配点及主要投稿风险",
          "jif": "5.4 (2025)",
          "quartile": "JCR 2025: Q1, Immunology",
          "field_ranking": "Immunology 9/183 (JCR 2025)",
          "articles_per_year": "210（2025；数据库统计/近似值）",
          "oa_apc": "Hybrid；订阅发表无强制 APC；可选 OA 的 APC 为 USD 4,000（访问日期 YYYY-MM-DD）",
          "first_decision": "中位数 7 天（出版社口径）",
          "first_peer_review_comments": "官网未公开",
          "evidence_status": "除明确标注的缺失项外均已核实",
          "sources": {
            "fit": [{"label": "官方期刊范围", "url": "https://official.example/scope"}],
            "jif": [{"label": "官方期刊指标", "url": "https://official.example/metrics"}],
            "quartile": [{"label": "JCR 官方数据", "url": "https://jcr.clarivate.com/"}],
            "field_ranking": [{"label": "JCR 官方排名", "url": "https://official.example/ranking"}],
            "articles_per_year": [{"label": "发文量统计查询", "url": "https://api.openalex.org/..."}],
            "oa_apc": [{"label": "官方 OA/APC 说明", "url": "https://official.example/apc"}],
            "first_decision": [{"label": "官方审稿时效", "url": "https://official.example/timeline"}],
            "first_peer_review_comments": []
          }
        }
      ]
    }
  ],
  "submission_order": ["1. 期刊官方英文名称——中文说明推荐顺序的理由"],
  "uncertainties": ["期刊官方英文名称——需要再次确认的具体事项"],
  "source_scope": ["中文说明来源范围、指标版本、统计周期和访问日期"]
}
```

Requirements:

- Use three groups by default; honor explicit user-selected grouping and total counts. Set expected_journal_count to the actual intended total.
- Use exact official journal titles and at least one ISSN/EISSN per journal.
- Keep `field_ranking` and `oa_apc` separate from `quartile` and other fields.
- Use plain text in values. Put links only in `journal_url` and `sources`.
- Use direct HTTP(S) source URLs. The renderer escapes all text and rejects unsafe links.
- Represent unavailable facts with explicit Chinese text such as `官方精确排名无法公开获取` or `官网未公开 APC 金额`.
- Write all translatable user-facing content in Simplified Chinese. Preserve only exact journal/manuscript titles, official JCR category names, established acronyms, identifiers, currencies, and other terms that must remain in English.
- Do not add a `risk_check` field manually. Pass the independent audit JSON and the actual dated risk-list file to the renderer; it recomputes the audit and rejects stale results.
