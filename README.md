# Academic Agent Suite｜学术综合 Agent 套件

面向科研写作、基金与学位材料、学术演示的一组可独立安装 Agent。仓库收录 3 个完整 Agent 包及对应的离线 HTML 用户手册。

## 包含的 Agent

### 1. 论文写作综合助手（`paper-writing-agent`）

覆盖选题、文献检索与精读、研究设计、论文各章节写作、翻译润色、创新性评估、投稿准备、同行评审与返修回复。支持在用户明确开启后，由不同子 agent 执行有轮次上限的审稿—返修流程。

- 当前版本：1.1.3
- 入口文件：[`paper-writing-agent/SKILL.md`](paper-writing-agent/SKILL.md)
- 安装说明：[`paper-writing-agent/INSTALL.md`](paper-writing-agent/INSTALL.md)
- 用户手册：[`manuals/论文写作综合Agent_用户使用说明书.html`](manuals/论文写作综合Agent_用户使用说明书.html)

### 2. 基金、毕业论文与奖项申报助手（`grant-thesis-award-agent`）

支持基金选题与立项论证、研究方案和技术路线，学位论文规划、章节写作与答辩，以及科技奖创新贡献、应用效益、证据材料和申报前核查。能够根据当前任务自动选择所需功能分支。

- 当前版本：1.0.0
- 入口文件：[`grant-thesis-award-agent/SKILL.md`](grant-thesis-award-agent/SKILL.md)
- 安装说明：[`grant-thesis-award-agent/INSTALL.md`](grant-thesis-award-agent/INSTALL.md)
- 用户手册：[`manuals/基金毕业论文奖项申报Agent_用户使用说明书.html`](manuals/基金毕业论文奖项申报Agent_用户使用说明书.html)

### 3. PPT 制作与演讲综合助手（`ppt-production-agent`）

适用于组会、开题与毕业答辩、教学培训、病例讨论和商务演示。可完成内容策划、故事板、可编辑 PPTX、模板复用、图表与文献核对、逐页演讲稿、问答准备和最终视觉核查。

- 当前版本：1.0.0
- 入口文件：[`ppt-production-agent/SKILL.md`](ppt-production-agent/SKILL.md)
- 安装说明：[`ppt-production-agent/INSTALL.md`](ppt-production-agent/INSTALL.md)
- 用户手册：[`manuals/PPT制作与演讲综合Agent_用户使用说明书.html`](manuals/PPT制作与演讲综合Agent_用户使用说明书.html)

## 安装

选择所需 Agent，将对应的整个目录复制到宿主支持的 skills 目录中。不要只复制 `SKILL.md`，各 Agent 的内部技能、脚本、参考资料和资源文件均通过相对路径调用。具体要求见各目录中的 `INSTALL.md`。

安装后可使用对应 slug 调用：

```text
$paper-writing-agent
$grant-thesis-award-agent
$ppt-production-agent
```

## 仓库结构

```text
academic-agent-suite/
├── paper-writing-agent/
├── grant-thesis-award-agent/
├── ppt-production-agent/
└── manuals/
```

## 使用说明

- 三个 Agent 可独立安装，不要求同时启用。
- 模型、联网、文档处理、Office/PDF 工具及子 agent 能力取决于实际运行宿主。
- Agent 不会把缺失数据、文献、实验结果或申报证明自动视为真实事实。
- 第三方组件及其许可信息保留在各 Agent 包内；再分发时请同时保留相应 NOTICE、许可证与来源说明。

