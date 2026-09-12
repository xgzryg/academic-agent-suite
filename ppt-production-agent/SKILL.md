---
name: ppt-production-agent
description: Plan, create, edit and validate editable PowerPoint presentations for research, defenses, teaching, cases, business and public communication. Route to bundled slide, template, evidence and speech tools; synchronize slide notes, scripts and rehearsal materials with the current deck.
---

# PPT 制作与演讲综合助手

根据当前任务制作可继续编辑、能用于实际讲述的演示材料。支持中文、英文与双语；默认中文沟通，成品语言遵循用户要求。

## 开始工作

1. 先读一次[共享规则](references/shared-rules.md)。复用用户已给出的材料、受众、时长、模板、当前稿和编辑范围，不重新询问已确认事项。
2. 按下表选择完成任务所需的最少分支，**实际读取包内 SKILL 并执行**。普通局部任务不强制重走完整制作流程。
3. 新建整套演示从[策划与故事板](skills/presentation-planning/SKILL.md)进入。已有 PPTX 先读当前文件，进入[编辑](skills/presentation-editing/SKILL.md)；只要演讲稿时进入[演讲](skills/speech-writing/SKILL.md)。
4. 复合任务按“内容与证据→故事板→页面与口语稿→生成与同步→核查与交付”衔接。用户明确要求自动完成且输入充分时连续执行；明确的确认点仍须遵守，缺失事实只暂停依赖部分。
5. 交付前进入[导出与核查](skills/delivery-qa/SKILL.md)，检查最终实际版本。任务完成后停止，不自动发布、发给他人或创建后台服务。

## 按任务选择包内分支

| 用户需要 | 应读取 |
| --- | --- |
| 从材料规划一套 PPT、安排页数与时长 | [策划与故事板](skills/presentation-planning/SKILL.md) |
| 文献汇报、组会、会议、毕业答辩、开题、项目答辩 | [学术演示](skills/academic-presentations/SKILL.md) |
| 讲课、培训、科普、练习与讲师提示 | [教学演示](skills/teaching-presentations/SKILL.md) |
| 病例讨论、医学教学、病程与诊断依据 | [病例演示](skills/case-presentations/SKILL.md) |
| 工作汇报、商业项目、产品、技术介绍或路演 | [商务演示](skills/business-presentations/SKILL.md) |
| 配色、版式、字体、视觉主线与可读性 | [页面设计](skills/slide-design/SKILL.md) |
| 用清楚的结构快速生成原生可编辑 PPTX | [原生 PPTX](skills/pptx-native/SKILL.md) |
| SVG 精细排版、对象级可编辑导出 | [高级 PPTX 引擎](skills/pptx-engine/SKILL.md) |
| 提取、蒸馏、复用或填充已有模板 | [模板复用](skills/template-reuse/SKILL.md) |
| 修改已有 PPTX、调整对象或统一主题 | [演示编辑](skills/presentation-editing/SKILL.md) |
| 从图片/截图重建可编辑页 | [图片重建](skills/image-to-slides/SKILL.md) |
| 文献查阅、引用身份、原始资料提取 | [文献与材料](skills/literature-research/SKILL.md) |
| 原文图表、数据图、表格与证据对应 | [图表与证据](skills/figures-and-evidence/SKILL.md) |
| 逐页演讲稿、备注、提示卡、HTML 讲稿与估时 | [演讲稿](skills/speech-writing/SKILL.md) |
| 答辩备答、互动排练、问答和修改建议 | [问答与排练](skills/qa-rehearsal/SKILL.md) |
| PNG/PDF 导出、逐页视觉检查、完整交付 | [导出与核查](skills/delivery-qa/SKILL.md) |

## 统一原则

- 默认制作可编辑文本、形状、表格及可用的原生图表；位图保留为图片，不把整页截图称为完全可编辑 PPT。
- 屏幕文案、演讲口语稿、备注与备答各有用途，保持同一页标识、证据和当前顺序。用户修改过 PPT 后先读取当前稿，不能从旧故事板重建覆盖。
- 保护用户事实、数字、单位、引用、图表含义和人工固定项。范文、样本模板、模拟数据、计划工作不能成为当前任务的事实。
- 不固定页数、模型、平台或商业服务。时长与语速是可调整估计，实际排练优先。来源中不适用的强制署名、去水印或默认全页栅格化不进入工作流。
- 内部依赖从本包相对路径定位；不要寻找构建者全局 skills 目录。实际工具、模型、Office 和公共库条件见[运行依赖](references/dependencies.md)。

版本与组件见[安装说明](INSTALL.md)及[组件说明](references/components.md)。普通制作不自动启动循环；需要真实子 agent 或后台任务时，按当前宿主实际能力和用户授权处理。
