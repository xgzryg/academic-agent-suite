---
name: paper-pdf
description: Extract academic PDFs with page locations, render pages for visual evidence, and inspect figures, formulas, tables and scanning failures without mistaking extraction artifacts for manuscript errors.
---

# 科研 PDF 读取与页面核验

遵守[共享规则](../../references/shared-rules.md)。使用包内[pdf_io.py](../../scripts/pdf_io.py)，无其他本机 skill 依赖。原 PDF 只读，所有文本和页面图片写到任务目录。

1. 读取文件总页数、逐页文本与字符数，用真实 PDF 页码定位。低文本页、双栏顺序、上下标、连字、断词、图例、公式和表格可能需要视觉回查，不能把抽取结果当真实排版。
2. 按任务范围渲染：精读的所有相关图表；Proof 的覆盖页面及每个疑似排版错误位置；其他任务只核会影响判断的页面。用当前宿主实际图像查看工具阅读图片。生成 PNG 不代表已经看图。
3. 图片/扫描页无可靠文本时，用现有 OCR 能力或人工视觉转录。OCR 结果与页面核对后才能作为已验证原文；没有 OCR 不凭空补段。不为一页解析失败重新下载或改写原件。
4. 表格优先用已有 pdfplumber 或原始表格文件，并核跨页表头、合并单元格、单位、脚注。图像不能代替原始实验数据，不从模糊图猜精确数值。公式、上下标、希腊字母按页面解释。
5. 原文未读、原文缺失和提取失败分别标记。校样问题需给“页面原貌→具体问题→建议”依据；仅抽取字符错而页面正确时，记录解析问题并不计为作者错误。

```text
python <包根>/scripts/pdf_io.py extract paper.pdf --output paper-pages.json
python <包根>/scripts/pdf_io.py render paper.pdf --output-dir pages --pages 1,3-5 --scale 1.5
```

`--pages` 为一基页码，省略则全页。脚本只向新路径写入，不覆盖已有图片。若必须产出 PDF，可用现有 Word/LibreOffice 导出或基于原始数据的 ReportLab 生成，随后重新读取和渲染核查；不把生成截图称可编辑矢量稿。

PDF 合并、拆页、旋转或标注只在用户请求时使用现有 pypdf/Office 能力生成副本，并核页码/方向/书签和相关内容；不擅自移除保护或覆盖原件。

交付说明实际读取/视觉核验范围，给定位和缺项。所需 pypdf、pypdfium2、Pillow 为普通运行库，见[依赖说明](../../references/dependencies.md)。

本分支工具为本包原创；执行规则与脚本已随包提供，不需要原构建资料。
