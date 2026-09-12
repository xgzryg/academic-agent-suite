---
name: rebuttal-writing
description: "逐点回复结构、评论解析、语气与长度校准、返修信模板；融合后不以编辑语气猜测录用或申诉结果。"
---

# Rebuttal Writing · 融合分支

先读取 [便携规则](PORTABLE.md)。来源为 awesome-rosetta-skills contributors 的 MIT 标注技能。完整 [原始示例](references/original-examples.md) 仅用于学习语气/结构和来源追踪，示例数值、固定日期、已补实验、自动申诉评分与安装命令不得执行或当作事实。

采用流程：保留真实评论全文和编号；拆分子问但不改变含义；逐条给直接回应、证据、实际修改、位置与尚缺项；批注不等于完成；校准语气和篇幅；输出所需格式并同步核查。

- 评论解析、数量统计和占位骨架使用 [parse_reviews.py](scripts/parse_reviews.py)。启发式解析后必须对原文核对 reviewer 边界和子问完整性。分审稿人输出，不跨审稿人引用。
- 接受、澄清、证据支持的不同意、已补实验与局部更正的措辞，用 [Nature Response语气库](../nature-response/references/tone-and-stance.md)；无法实施、冲突意见、补引用与申诉分流用 [困难情况](../nature-response/references/difficult-cases.md)。每句完成态由真实产物支持。
- 篇幅按问题复杂度：错字1—2句；澄清2—4句；方法修改1—2段；方法分歧或新增真实证据2—3段；核心概念争议必要时3—5段。这些是参考，不为凑段数扩写。
- Word使用 [Veritas模板](../veritas-agent/references/attachments/reviewer_response_blank_template.docx)，LaTeX使用 [内置模板](../nature-response/references/latex-templates.md)，返修Cover Letter用 [对应结构](../nature-response/references/response-structure.md)。编译引擎和额外库为条件依赖，不自动安装。
- 真实编辑决定以决定信为准；按截止日安排，不用统一3周/3月代替真实要求。不能凭某审稿人正面评价决定申诉，申诉须用户明确任务与真实事实支持，不代发送。
