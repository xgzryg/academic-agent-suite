---
name: literature-research
description: Read supplied documents and retrieve verifiable literature identities or supporting evidence needed for a presentation, with explicit coverage and source locations.
---

# 文献与材料读取

先读当前任务的真实材料，不默认把 PPT 制作扩成全文翻译或另写综述。需要完整精读时按用户要求覆盖全文及图表，明确可读取范围。

- PDF 可调用 `scripts/pdf_io.py extract`，记录页码；短文本、扫描页或复杂图表应渲染查看，文本提取不能代替视觉阅读。
- Word 可调用 `scripts/document_io.py extract`；图片、表格和复杂对象回到实际文件核对，不能只取段落就宣称全部材料已读。
- 文献身份核对题名、作者、期刊、年份、DOI/PMID；正文主张与其具体证据对应，范文只提供组织思路。
- 需要新增文献且符合联网范围时，选择宿主实际可用的数据库或浏览工具。PubMed 支持可用的包内 `scripts/pubmed_evidence.py`，其他数据库不能假称已查询。
- 检索日期、检索式、取回与阅读范围如实记录；失败、部分返回和零命中分开。公共检索词使用必要主题概念，不外传未发表全文、病例和敏感原始数据。
- 文献相似度用于发现候选，不是创新性评分。期刊历史指标不当现行事实，未核验的数值不填入成品。

先运行相应脚本 `--help` 读取实际参数，再显式指定任务内输出路径。无网时可整理已有证据和检索式，但不能编造参考文献。

需要展示原图表时进入[图表与证据](../figures-and-evidence/SKILL.md)，需要学术主线时进入[学术演示](../academic-presentations/SKILL.md)。
