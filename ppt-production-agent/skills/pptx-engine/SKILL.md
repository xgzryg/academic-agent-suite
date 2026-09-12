---
name: pptx-engine
description: Produce editable PPTX using the bundled native JSON engine or detailed SVG-to-DrawingML backend, then inspect the actual PowerPoint output.
---

# 可编辑 PPTX 工程

接收主agent确认的实际材料、故事板、输出目录和视觉方向。保持主角色，按任务选择包内引擎。

- 常规汇报使用主agent的原生JSON生成器；需要精细矢量排版时读 `../../references/engine-usage.md` 使用 SVG → DrawingML。
- 原始PPTX模板走 `../template-reuse/SKILL.md`，已有成品局部修改走 `../presentation-editing/SKILL.md`，截图重建走 `../image-to-slides/SKILL.md`。只加演讲稿/notes不能触发整套重做。
- 使用真实数据/图表/图片和当前用户已定的故事顺序；不得为填充版式编造结论、数值或引用。
- 选用的每个输出元素说明编辑范围：原生文字/形状/表格/图表可编辑，插入图片仍是图片；SVG图表转换后通常是形状，不自动等于带数据工作表的PowerPoint图表。
- 源SVG使用一致画布、自含路径和真实图片，显式字体、合理文本框。先精炼/换版/拆页处理超载，再考虑小范围字号调整。没有用户授权不改变人工固定源稿。
- 默认无对象动画、无自动播放、无配音；这些是用户要求时的额外模块。
- 生成后用 `../../scripts/render_pptx.ps1` 或实际可用平台渲染器查看最终PPTX所有页，核对页数、备注、原生图表数据、图片比例和可读性。不能把XML通过或SVG效果图当成PowerPoint效果已通过。
- 输出PPTX、用户需要的PDF/PNG及当前任务源码。临时、源码和检查文件保存到项目指定目录，不写到安装目录，不调用原开发机技能路径。

依赖：Python、python-pptx和Pillow；图表工作簿修改另需openpyxl；真实PowerPoint渲染需要PowerPoint/LibreOffice等外部软件。仅内置技能不意味着内置Office或模型运行时。
