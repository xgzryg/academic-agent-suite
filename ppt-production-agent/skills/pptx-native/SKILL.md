---
name: pptx-native
description: Produce editable native PowerPoint slides, charts, tables, images and speaker notes from a task-specific JSON storyboard.
---

# 原生可编辑 PPTX

用于结构清楚的学术、教学与通用演示。先读[故事板格式](../../references/storyboard-format.md)，由模型根据用户材料写好页面与实际口语稿，再运行包内脚本：

```text
python <包根>/scripts/native_deck.py <任务目录>/storyboard.json --output <任务目录>/presentation.pptx
```

支持 12 类页型、5 个可调整主题和 16:9/4:3。文本、形状、表格与原生图表保持对象可编辑；图片仍为图片。图片相对故事板定位，默认等比展示，明确选择 cover 才裁切。

脚本遇到未知类型、错误数据或缺图会失败，不得忽略后继续交付缺页结果。输出已存在时，按用户的版本和覆盖授权处理。不要为通过脚本而删掉用户要求的内容。

生成后用[演讲稿](../speech-writing/SKILL.md)导出对应口语稿与提示卡，并进入[交付核查](../delivery-qa/SKILL.md)。脚本的文本密度提示不代表视觉已通过。

复杂布局、模板或图片重建分别进入[高级引擎](../pptx-engine/SKILL.md)、[模板复用](../template-reuse/SKILL.md)或[图片重建](../image-to-slides/SKILL.md)，不强行把所有任务改成 JSON 的固定布局。
