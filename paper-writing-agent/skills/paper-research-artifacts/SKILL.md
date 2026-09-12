---
name: paper-research-artifacts
description: Produce research evidence workbooks, manuscript tables, data-based figures, editable presentation outlines and local interactive explanations as requested, with appropriate scientific and visual verification.
---

# 科研表格、图表、PPT 与交互解释

遵守[共享规则](../../references/shared-rules.md)。这是任务驱动的支撑分支；文字任务不会自动产生所有文件。所需公共运行库和宿主服务见[依赖说明](../../references/dependencies.md)。

## 表格和证据矩阵

输入为实际研究材料/数据表和所需字段。文献矩阵包含身份、设计、样本、方法、主要结果、局限、可支持/不能支持的论点、页码及待核对项；返修矩阵按 R1-Q1 等编号跟踪原意见、实际改动、证据位置、状态和待办。

CSV/XLSX 数据先核字段、单位、缺失和重复；保留原始数据，不默认删除异常值或把缺失值填零。复杂清洗可采用 Raw_Copy、Data_Dictionary、Cleaning_Log、Clean_Data、Summary、Charts、Exceptions 七表结构，按实际需求取用，不对纯文献表强制七张表。每项转换记录规则及影响；应计算的数值保留可追溯公式/代码，不把输入本身误作必须公式化。

用现有 openpyxl 构建可编辑 XLSX，设置清晰表头、列宽、冻结窗格和筛选。公式由实际公式引擎重算才可声称计算已验证；openpyxl 不计算公式。抽查关键数据、公式引用范围和图表源。无法重算时说明，保留公式及独立核算依据。

## 定量图与表

先明确每图科学问题、实际数据、单位、分组、误差/置信区间、分析单位、统计标记与解释上限；采用与图种匹配的 R/ggplot2 或 Python/Matplotlib。提供生成代码和用户要求的 SVG/PDF/PNG 等文件。检查真实数字、轴/对数尺度、颜色、样本量、误差类型、负值及离群值处理。不能根据文字描述臆造实验曲线或显微图。

图形摘要使用[摘要图分支](../paper-graphical-abstract/SKILL.md)，机制推断与证实关系分开。用户的既有样式、字体、期刊尺寸优先。绘图软件/库不足时可先形成可执行绘图规范和真实数据表，但明确图尚未生成。

## PPTX 学术汇报

读取受众、时长、主结论与真实论文证据。按问题→设计→证据→解释→局限组织，避免搬入整段论文；每页承担清楚功能，图和来源可定位。优先保留可编辑文字、表格和图形，通过现有 python-pptx 或宿主幻灯片工具制作，不把全部页面压成图片假称可编辑。

按用户模板布局，结合投影阅读检查字号、留白、图注和每页信息量。用现有 Office/LibreOffice 导出页面 PDF，再经[PDF 分支](../paper-pdf/SKILL.md)实际查看全部页面。没有渲染器则明确未通过版面核验，不以页数或 XML 可读代表演示可用。

## 本地 HTML、思维导图和交互演示

优先生成自包含 HTML/SVG/JavaScript，引用用户允许的数据；明确参数、假设、公式和适用范围。适合样本量/效应量关系、模型阈值、文献筛选或敏感性解释。科研/教学演示不凭此宣称具备临床诊断用途。实际打开并改变关键参数检查结果和错误状态；如果没有浏览器工具，只能声明代码/数值检查，不能宣称交互已验证。

Review 思维导图可直接交付 Markdown 层级源码；有 markmap 时再渲染，无需联网加载第三方脚本才能阅读基本内容。构建站点与发布的权限分开，转[工作区与宿主分支](../paper-workspace-operations/SKILL.md)处理已请求部署。

### 论文阅读网页

需要精读可视化或全文阅读的浏览器预览时，读取[论文阅读 HTML 说明](references/paper-reader.md)，用包内模板和标准库脚本渲染已完成的阅读内容。预设支持系统/浅色/深色主题、移动目录、章节锚点、页面进度、长表与图片适配及打印；基本阅读无需 CDN。

页面仅改变呈现，保留原阅读范围、全部所需图表与来源 ID。全文中英对照保留既有原文和译文、原 Markdown 与 source map；不重新翻译或改成摘要。模板不生成科学内容，公式须由上游提供可读形式。输出写用户任务目录，并实际检查所需的交互和版面。

公共库是本分支的条件运行依赖；执行规则已随包提供，不需要原构建资料或其他机器上的 agent/skill。
