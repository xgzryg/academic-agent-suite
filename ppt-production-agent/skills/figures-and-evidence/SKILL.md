---
name: figures-and-evidence
description: Map presentation claims to supplied figures, tables and real data; preserve scientific meaning when extracting, cropping, redrawing or summarizing visuals.
---

# 图表与证据

先区分原文图、用户数据、模板示例图和拟制作示意图。为采用的图表记录源文件、页码、图/表号、面板、需要说明的结论，以及裁切或重绘方式。

1. 对照原始图与相邻正文，确认物种/人群、实验问题、分组和指标与该页主张一致；不能只因图片好看就采用。
2. 优先保存原清晰图，等比放置；必须裁切时保留解释所需坐标、单位、图例和比例尺，并在来源表记录。普通裁切不会增加原图分辨率。
3. 提供真实数据时可以使用原生 PowerPoint 图表/表格或已有绘图库制作数值图；保持数值、分组、缺失值、不确定性和统计含义。只给截图时不反推精确数据。
4. 多面板过密时按科学关系拆页，清楚标注同一原图的不同面板；只显示选定图表时说明汇报范围，不冒称完整覆盖。
5. 示意图用来解释机制或流程，标注假设与证据状态。真实实验、病理和临床影像不以生成图替换。
6. 页面、讲稿与来源表同步，讲解只使用实际图中可支持的结果。图文冲突先指出，在授权范围内修正。

PDF 提取和页面渲染使用包内 `scripts/pdf_io.py`，具体可用参数见 `--help`。版式走[设计](../slide-design/SKILL.md)，工程走[原生 PPTX](../pptx-native/SKILL.md)或[高级引擎](../pptx-engine/SKILL.md)，最终检查真实页面。
