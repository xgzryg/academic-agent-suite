---
name: literature-workflow-orchestrator
description: 文献证据流程：问题和检索式、PubMed与条件多源检索、去重筛选、全文取得、精读、引用和交付；为审稿返修提供可追溯的文献支持。
---

# 文献证据工作流

先沿用主任务简报；用公开的通用术语检索，不把整篇未发表稿件或私人资料发送至外部服务。检索预算、日期范围和选用来源必须记录。研究有效性依赖范围时先明确范围；常规快速核查可声明合理的检索上限并执行。

| 当前需要 | 包内入口 | 执行要求 |
| --- | --- | --- |
| PubMed、MeSH、近似文献 | [pubmed-database](../pubmed-database/SKILL.md) | 保存检索式、总命中数、取回范围、摘要、标识和失败状态 |
| 多源检索、引用及去重 | [academic-literature-search](../academic-literature-search/SKILL.md) | 先核宿主可用工具；无 MCP 可走包内 PubMed 脚本；其他源按任务调用官方服务 |
| 创新性或审稿查新 | [paper-novelty-assessment](../paper-novelty-assessment/SKILL.md) | 逐主张比较相近文献，独立记录已知内容与增量 |
| 用户要求全文下载 | [ref-downloader](../ref-downloader/SKILL.md) | 批次范围已获授权才下载；优先开放获取，登录及浏览器配置按真实环境处理 |
| 全文双语精读 | [nature-reader](../nature-reader/SKILL.md) | 源锚定、图表公式、术语一致；摘要核查不自动扩为全文翻译 |
| 摘要综合或综述提纲 | [paper-literature-reading](../paper-literature-reading/SKILL.md) | 基于实际读到内容综合，不能把题目当研究结论 |
| 期刊指标 | [journal-if-lookup](../journal-if-lookup/SKILL.md) | 仅任务需要时查询；内置为历史2025来源，不能称当前指标或文章质量 |
| Word/PDF与表格图示交付 | [paper-documents](../paper-documents/SKILL.md)、[paper-pdf](../paper-pdf/SKILL.md)、[paper-research-artifacts](../paper-research-artifacts/SKILL.md) | 仅交付用户要的格式并真实核查 |
| 返修补引与回复 | [paper-reviewer-response](../paper-reviewer-response/SKILL.md) | 可引用事实与计划工作分开，真实修改后给位置 |

阶段按依赖运行：构造宽窄查询 → 检索取回 → 标识去重且保留来源 → 按问题相关性阅读 → 必要时取得全文 → 证据比较 → 写作或报告。不要以 IF、语言、免费全文或任意近三年过滤来默默缩小查新范围。近期文献和早期先行研究均可能影响创新性；预印本与正式版本分开标注且核对版本。

若系统综述是明确目标，另行定义纳排标准、数据库覆盖、检索日期与筛选过程；快速查新不能冒称系统综述。网络不可用时交付策略和待核实项；不能把失败记成零命中。

原工作流列出的基因、临床试验、期刊/PPT生态等推荐项不构成本包自动调用依赖；已需要的检索、阅读、写作和文件功能均映射为上表包内入口。原说明留存来源档案用于追溯。
