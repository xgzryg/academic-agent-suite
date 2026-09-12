---
name: paper-documents
description: Read, create and carefully edit Word manuscript artifacts using the bundled document helper; preserve scientific text, document objects and revisions, and inspect rendered pages when a renderer is available.
---

# 论文 Word 文档

先遵守[共享规则](../../references/shared-rules.md)。此为本包原创支撑技能，不调用其他安装目录中的 documents/docx skill。

## 读取与对象保护

读取当前文件与允许编辑范围。使用包根[document_io.py](../../scripts/document_io.py)的 `extract` 提取正文、表格、页眉页脚、脚注/尾注、批注和修订信息。输出只用于内容定位；XML 段落不是最终排版页码。查看脚本报告的公式、图像、域、超链接和修订对象数量，决定是否可以使用普通文本编辑。

复杂主稿不能仅用 `paragraph.text = ...` 或从抽取文本新建文档来替换原件，这会丢失公式、交叉引用、引用管理器域或修订。保留原 OOXML 包及其关系，只修改授权文本节点；用用户稿件的实际格式和模板，不强加新样式。

## 创建和编辑

- 新报告可用 `from-json`，输入 `title`、`author`（仅真实提供时）、`blocks`，块类型为 paragraph/heading/table。输出文件必须为新文件。图像、参考文献域、目录等复杂对象由 agent 按真实需求通过可用 OOXML/Office 工具构造，再回读与渲染；不假称简易生成器保留了它们。
- 单一文本 run 内的精确替换可用 `replace`：每项 `{old,new}` 必须在稿件中唯一匹配。工具在一次工作副本中完成全部匹配才写出；跨 run 文本会说明不适用，不能静默漏改。
- 用户要求修订时加入 `--track --author <真实指定姓名或助手标签>`。该帮助程序支持新插入/删除修订，不自动接受或抹掉既有作者修订。需要批注时用 OOXML 的评论主体、锚点和关系或宿主文档接口实现，并验证双向对应；不把旁边的对照表叫 Word 原生修订。
- 原稿存在修订时先明确需要观察的状态；不可擅自接受全部修订。干净稿与对照稿只按请求提供。

## 命令

从本技能目录定位包根，将以下路径转换为绝对路径；输出在用户任务目录。

```text
python <包根>/scripts/document_io.py extract manuscript.docx --output manuscript-extracted.json
python <包根>/scripts/document_io.py from-json report.json --output report.docx
python <包根>/scripts/document_io.py replace manuscript.docx --edits edits.json --output edited.docx
python <包根>/scripts/document_io.py replace manuscript.docx --edits edits.json --track --author Editor --output tracked.docx
python <包根>/scripts/document_io.py render manuscript.docx --output-dir render --renderer <已有的soffice可执行文件>
```

`replace` 的 edits.json 是 `{ "replacements": [{ "old": "原文", "new": "新文" }] }`。仅针对能保留格式的唯一 run 内替换；其他编辑由 agent 在保留真实对象的工作副本中执行。

## 必要验证与缺失能力

回读新稿，核对数值、引用、完整章节、表格、公式、图片和修改范围。对版式交付，用已有 Word 导出或 `render` 调用 LibreOffice 生成 PDF，再转[PDF 技能](../paper-pdf/SKILL.md)渲染 PNG 并实际查看每页。关注中文字体、跨页表格、图注、上下标、重叠和截断。Word/LibreOffice 的呈现可不同，投稿模板以期刊要求和用户最终软件为准。

没有渲染器时继续交付内容已核稿，明确“版面尚未渲染核验”；若任务要求必须版面验收，列出缺少的渲染器而不冒充完成。不得未经请求修改系统字体、执行策略或安装软件。依赖见[依赖说明](../../references/dependencies.md)。

本分支的文档工具为独立实现；运行规则与脚本已随包提供，不需要原构建资料或本机第三方文档技能。
