---
name: research-visuals
description: Create editable technical roadmaps, process diagrams, Gantt charts and timelines from real structured content; provide Markdown mindmaps and evidence-grounded graphical abstract or mechanism plans, using host image tools only when needed and available.
---

# 科研图形与计划可视化

将真实研究内容转为准确、可编辑、可核查的图。先遵守[共享规则](../../references/shared-rules.md)和[当前目标要求](../../references/current-requirements.md)，复用当前数据、已确认方法、参考图及人工固定成品。

## 输入和选型

- 路线/流程：研究目标、节点、并行/依赖/汇聚关系及必要证据；图形逻辑不能从例图照搬。
- 甘特/时间线：实际日期、任务、里程碑和依赖；没有日期先整理待定计划，不编造日历。
- 思维导图：实际文档或已确认内容层级。
- 摘要/机制：核心信息、实体、关系与出处、目标规格；区分既定结果、相关性、假设和计划。
- 统计图：实际数据或已确认分析结果、单位/效应尺度与统计方法；不使用生成式图像伪造数据点。

局部修改直接读取当前图和源文件，不重复广泛选型。用户启用其他个人样式角色时，科学含义、可访问性和明确规格优先，在兼容范围内沿用其样式。

## 执行

1. 从当前材料整理节点/任务与科学关系，保持研究计划、实际结果和应用业绩的时态。文本与参考风格冲突时按内容逻辑构图；实质关系不清才询问，复用已有确认，不每张图重新审批。
2. 对路线、流程、甘特或时间线创建项目 JSON，使用包内[图形脚本](../../scripts/research_diagrams.py)。输入格式与完整命令见[示例说明](../../examples/diagrams/README.md)；四种 type 为 `roadmap`、`flow`、`gantt`、`timeline`。采用显式用户项目输出路径，任何同名 `.svg` 或 `.drawio` 均拒绝覆盖。
3. 对思维导图交付类似[层级示例](../../examples/diagrams/mindmap.md)的 Markdown 源，必要时按宿主已有工具导出图。脚本不生成 `.xmind`，不宣称专有样式完整兼容。
4. 对摘要或机制图按[视觉与证据说明](references/visual-method.md)先形成可执行设计、标签与关系。需要插画且宿主有真实图像工具时按宿主规则生成；没有该能力时完成文字方案和可编辑关系图，明确插画尚未制作。图像生成不作为代码图依赖。
5. 实际渲染图形并查看标题、节点、边、箭头、标签、中文字体、留白和目标尺寸；普通源代码/XML 解析不能替代看图。路线节点与边不得漏掉，筛选图核对人数和分母，甘特核日期和依赖，图例核其真实编码含义。修复本次具体问题后完成交付。
6. 图注/文档衔接交[文档分支](../academic-documents/SKILL.md)，外部机制证据交[证据分支](../evidence-research/SKILL.md)。统计数据图仅在宿主有适用 R/Python 库时按真实结果实现必要脚本；本包标准库图形脚本不做统计分析或任意绘图库自动安装。

## 输出与能力边界

需要区分研究架构图与详细路线图，或做现有图修改时，按需读 [架构与路线衔接](../../references/grant-deepening.md) 第5部分。架构图说明问题和模块，详细路线表达输入、步骤、验证与反馈；视觉改写保持模块与关系不变。

默认可编辑 JSON 源、SVG 和原生 draw.io 文件；需要且能执行时追加预览。输出格式遵守用户实际要求。脚本支持显式行列布局、有效 ID/边引用、日期及完成后开始依赖检查；不自动判断科学真伪或解决任意密集网络布线。复杂图需要调整行列或原生对象后重新查看。SVG 文字保留为 text，编辑效果取决于字体与编辑器。

不得用关系箭头把关联升级为因果；预期结果、推测机制必须标明；不能把示例人数、日期和技术方案纳入真实项目。未能渲染或尚未在目标编辑器打开时，准确说明实际验证层级，不能把文件已保存当成最终视觉验收。
