---
name: presentation-support
description: 为基金汇报、学位答辩和科技奖答辩组织演示叙事，生成含可编辑标题正文、可选图片和逐页备注的基础PPTX，并交付逐页讲稿。专有模板和页面视觉核查按实际工具能力处理。
---

# 汇报材料与基础 PPTX

遵守 [共享规则](../../references/shared-rules.md)。确认受众、时长、汇报目的、已确定研究材料和实际模板；用户仅要一页时直接完成该页。

1. 先按实际问题组织故事：为什么值得做/已完成什么；核心证据；方法与可信度；意义与边界；下一步或答辩请求。计划与结果分开标明。
2. 每页确定一句主要信息、支持证据和讲述顺序。图表引用真实结果，避免把未核数字或生成式图画当数据图。
3. 文字、数据图和讲稿同步。学位答辩衔接 [thesis-defense](../thesis-defense/SKILL.md)，路线和时间图衔接 [research-visuals](../research-visuals/SKILL.md)。
4. 基础版可用 [presentation_builder.py](../../scripts/presentation_builder.py) 从JSON创建PPTX。输入title与slides，每页title、bullets、notes，可选image。文字可编辑，图片以图片对象插入；不声称图片内部元素均可编辑。
5. 用户给了专有模板时先审查实际母版和占位符，再用可用工具沿用；基础脚本不是任意模板复刻器。保留模板原件。
6. 回读标题、正文、备注与图片数量。实际渲染后检查溢出、字号与图像比例；未提供渲染器时如实说明只做结构和内容检查。

交付PPTX、可继续编辑的输入JSON和讲稿；避免自动增加与任务无关的大量页面。具体CLI见 [工具指南](../../references/tools.md)。
