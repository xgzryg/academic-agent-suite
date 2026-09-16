# 完整路由表

根据语义选择一个或多个分支。用户指名的任务决定范围；先读对应真实SKILL.md，不以此表代替执行说明。需要Office/PDF/宿主工具时再读取相应支撑分支。

| 任务 | 包内入口 | 决策要点 |
| --- | --- | --- |
| 选题与语料主题分析 | [paper-topic-discovery](../skills/paper-topic-discovery/SKILL.md) | 候选问题与主题图谱；用户选择后细化 |
| 检索、精读、Review证据与思维导图 | [paper-literature-reading](../skills/paper-literature-reading/SKILL.md) | Research逐图表，Review逐章节；联网条件化 |
| 研究设计和图表规划 | [paper-study-design](../skills/paper-study-design/SKILL.md) | 检验假设；拟议与已执行分开 |
| 前言框架、综述与正文 | [paper-introduction](../skills/paper-introduction/SKILL.md) | 复用选定框架和引用；范文隔离 |
| 方法章节 | [paper-methods](../skills/paper-methods/SKILL.md) | 新章节大纲确认；不补实验细节 |
| 结果与图注 | [paper-results-legends](../skills/paper-results-legends/SKILL.md) | 图/分图映射；新章节大纲确认 |
| 讨论 | [paper-discussion](../skills/paper-discussion/SKILL.md) | 本研究与外部结论分开；不超证据 |
| 标题、摘要、结论与关键词 | [paper-title-abstract-conclusion](../skills/paper-title-abstract-conclusion/SKILL.md) | 按所需组件执行；数字与主稿一致 |
| Highlights | [generate-paper-highlights](../skills/generate-paper-highlights/SKILL.md) | 实际计数；期刊/用户规则优先 |
| 图形摘要 | [paper-graphical-abstract](../skills/paper-graphical-abstract/SKILL.md) | 文字方案确认；画幅比例正确 |
| 中译英 | [translate-academic-manuscript-zh-to-en](../skills/translate-academic-manuscript-zh-to-en/SKILL.md) | 小块三步；术语统一；完整重组 |
| 全文精细润色 | [polish-academic-manuscript](../skills/polish-academic-manuscript/SKILL.md) | 保持结构、科学含义和作者声音 |
| 精简与缩写 | [paper-compression](../skills/paper-compression/SKILL.md) | 实质取舍先决定；程序计数 |
| 重复表达改写 | [rewrite-academic-overlap](../skills/rewrite-academic-overlap/SKILL.md) | 限定片段；不承诺检测结果 |
| 同行预审与期刊校准 | [academic-peer-review](../skills/academic-peer-review/SKILL.md) | 文档角色由用户指定；不凑意见 |
| 选刊和HTML报告 | [recommend-sci-journals-report](../skills/recommend-sci-journals-report/SKILL.md) | 现行指标查证；历史快照有截止日期 |
| 投稿信息总表、投稿系统填报资料、投稿参照文档、作者信息总表 | [paper-submission-reference](../skills/paper-submission-reference/SKILL.md) | 先抽取后追问；Excel 为唯一主表；关键项未确认只能生成草稿 |
| 投稿附信 | [write-journal-cover-letter](../skills/write-journal-cover-letter/SKILL.md) | 声明、作者与预印本按实际情况 |
| 审稿状态、接收后校样/制作进度询问 | [editorial-correspondence](../skills/editorial-correspondence/SKILL.md) | 按实际阶段拟邮件；不要求返修决定或整篇稿件；未知事实留待补 |
| 返修与逐条回复 | [paper-reviewer-response](../skills/paper-reviewer-response/SKILL.md) | 原意见/作者回答/修订证据分隔 |
| Proof校对 | [proofread-journal-manuscripts](../skills/proofread-journal-manuscripts/SKILL.md) | 默认逐节确认；已授权可全文连续 |
| Word创建编辑与修订 | [paper-documents](../skills/paper-documents/SKILL.md) | 包内原创工具；复杂对象保留；渲染条件明确 |
| PDF提取与页面核验 | [paper-pdf](../skills/paper-pdf/SKILL.md) | 抽取伪影不计作者错误；视觉检查实际页面 |
| 表格、定量图、PPT及交互解释、精读HTML | [paper-research-artifacts](../skills/paper-research-artifacts/SKILL.md) | 数据驱动；精读网页支持主题、移动目录和长页导航；按产物核验；不自动部署 |
| 工作区、恢复、代码修复与宿主工具 | [paper-workspace-operations](../skills/paper-workspace-operations/SKILL.md) | 最小科研代码修复；工具发现、权限、任务/版本/GUI/定时条件路由 |

## 串联与局部任务

- 新论文：选题/文献→按已选问题设计→真实结果与图注→分章节写作→所需摘要/标题/Highlights；仅执行当前已授权阶段。
- 中文全文：翻译→必要时另行润色→所需Word/PDF交付；不把翻译自动变成补写。
- 已有英文稿：按请求选择润色、精简、改写或Proof；这些分支不互相替代。
- 投稿：通用投稿信息总表可先从当前稿件抽取并补齐→选刊→已选期刊适配→Cover Letter/Highlights/图形摘要；未知作者声明不能自动填肯定句，投稿信息总表中的未确认值也不能作为确定声明。
- 返修：当前主稿+真实评语+已完成改动→逐条回复→必要的引用/统计证据核对→同步授权范围内文稿。
- 编辑询问信：实际稿件阶段与已知事实→审稿状态或接收后进度模式→可复制主题与正文。写信不自动触发返修、Proof检查或发送。
- 精读网页：按请求完成文献精读及证据定位→科研产物分支的阅读HTML预设→检查全文覆盖、图表、来源锚点及阅读交互。
- 研究工具：只有当前任务需要表格、图、PPT、站点、定时/GUI时进入对应支撑分支。

分支执行要点见[分支执行说明](source-skill-adaptations.md)；共享底线见[shared-rules.md](shared-rules.md)。

## 内置专家与扩展能力

重复能力按[integration-v1.1.md](integration-v1.1.md)选择，不依次全跑。

| 包内入口 | 用途 |
| --- | --- |
| [academic-literature-search](../skills/academic-literature-search/SKILL.md) | 学术检索、引用身份核验与多数据库补充；记录已查/未查来源 |
| [aequitas](../skills/aequitas/SKILL.md) | 按可见材料开展多视角审稿，定位实质问题、证据与最小修正 |
| [calder-code-reviewer](../skills/calder-code-reviewer/SKILL.md) | 审核论文代码的复现、数据划分、泄漏、公平性和结果一致性 |
| [code-review-academic](../skills/code-review-academic/SKILL.md) | 学术代码审计；内置6组只读学术代码审计参考规范 |
| [journal-if-lookup](../skills/journal-if-lookup/SKILL.md) | 按期刊名、缩写或ISSN查询用户显式提供的数据，或联网核验现行指标；记录年份与来源 |
| [literature-workflow-orchestrator](../skills/literature-workflow-orchestrator/SKILL.md) | 组织检索、筛选、精读、证据整理和综述阶段的衔接 |
| [litorchestrator](../skills/litorchestrator/SKILL.md) | 文献任务总调度，按问题选用包内检索、阅读、下载及引用功能 |
| [nature-polishing](../skills/nature-polishing/SKILL.md) | 按语言、论文类型及章节选择Nature风格润色资源，保护研究事实 |
| [nature-reader](../skills/nature-reader/SKILL.md) | 论文全文、图表、补充材料与公式精读，标明实际阅读范围 |
| [nature-response](../skills/nature-response/SKILL.md) | Nature风格逐条回应、修订策略及正文/回复一致性检查 |
| [nature-review-studio](../skills/nature-review-studio/SKILL.md) | 应用现有聚合审稿规则；生成同步Word/Markdown报告，提取任务内材料 |
| [nature-reviewer](../skills/nature-reviewer/SKILL.md) | 区分重大/次要意见、证据位置与真实阻塞；支持分开审稿再综合 |
| [nature-shared](../skills/nature-shared/SKILL.md) | 供Nature分支共享术语、结构、统计、图表和数据可用性写作资源 |
| [nature-statistics](../skills/nature-statistics/SKILL.md) | 核查统计方法与结果报告的完整性、准确性和证据边界 |
| [nature-writing](../skills/nature-writing/SKILL.md) | 按论文类型、章节和语言路由Nature写作框架及主文/补充材料组织 |
| [paper-novelty-assessment](../skills/paper-novelty-assessment/SKILL.md) | PubMed宽窄查询、种子近邻和逐篇比较，判断创新主张的证据支持 |
| [paper-review-revision-loop](../skills/paper-review-revision-loop/SKILL.md) | 显式开启真实审稿/返修子agent往返，保存版本、问题状态和最终再审 |
| [peer-review](../skills/peer-review/SKILL.md) | 补充科研设计、方法、统计、图表和论证的批判性评价 |
| [pubmed-database](../skills/pubmed-database/SKILL.md) | 实际执行PubMed检索、完整摘要获取和Similar Articles近邻查询 |
| [rebuttal-writing](../skills/rebuttal-writing/SKILL.md) | 解析审稿意见、组织逐条回应，区分已完成修改与待办分析 |
| [ref-downloader](../skills/ref-downloader/SKILL.md) | 解析与核验参考文献，按实际访问条件下载可取得全文并报告缺项 |
| [reproducibility-checklist](../skills/reproducibility-checklist/SKILL.md) | 依据实际材料检查数据、代码、环境、方法和可复现性报告 |
| [veritas-agent](../skills/veritas-agent/SKILL.md) | 核对当前稿、图表、统计、引用和审稿意见，整合返修稿与逐条回应 |
| [wordpolish-academic](../skills/wordpolish-academic/SKILL.md) | 调用两个内置学术文风子技能，压缩模板表达并保留作者声音和事实 |
