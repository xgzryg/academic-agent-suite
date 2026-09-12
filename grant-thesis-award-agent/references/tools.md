# 包内工具用法

以下命令里的 `<包目录>`、`<任务目录>`、`<输入文件>` 均由实际位置替换，路径有空格时保留引号。`python`代表用户实际可用的Python 3.10+命令。所有输出使用任务目录；同名输出默认拒绝覆盖。安装文件夹不作为结果目录。

## PubMed

```text
python "<包目录>/scripts/pubmed_evidence.py" --output "<任务目录>/records.json" search --query "senescence AND liver" --limit 10
python "<包目录>/scripts/pubmed_evidence.py" --output "<任务目录>/fetched.json" fetch --pmids 31452104
python "<包目录>/scripts/pubmed_evidence.py" --output "<任务目录>/related.json" related --seeds 31452104 --limit 5
```

输出含真实检索式/日期/范围、完整可取得摘要、PMID、种子关联、失败及缺失情况。相似度排序是检索排序，不是创新性分数。返回partial/error时仍保存状态记录，不能称为无文献。

## 引用结构审计

```text
python "<包目录>/scripts/citation_audit.py" --input "<任务目录>/citations.json" --output "<任务目录>/citation-audit.json"
```

输入示例：
```json
{"citations":["R1"],"references":[{"id":"R1","title":"用户实际提供的题名","authors":["实际作者"],"year":2024,"doi":"","verification":{}}]}
```

待核元数据空缺保留。实际核验后可在verification记录source、checked_at、note；工具只转述用户提供的核验记录，不自行断言真实。它不解析所有Word/BibTeX引用格式，先从实际文档整理此结构，再回核正文位置。

## Word

```text
python "<包目录>/scripts/document_io.py" extract "<输入文件.docx>" --output "<任务目录>/word-content.json"
python "<包目录>/scripts/document_io.py" from-json "<任务目录>/report.json" --output "<任务目录>/report.docx"
python "<包目录>/scripts/document_io.py" replace "<输入文件.docx>" --edits "<任务目录>/edits.json" --output "<任务目录>/revised.docx" --track --author "Editor"
python "<包目录>/scripts/document_io.py" render "<任务目录>/revised.docx" --output-dir "<任务目录>/word-pages"
```

from-json输入：
```json
{"title":"研究材料审读","blocks":[{"type":"heading","text":"当前依据","level":1},{"type":"paragraph","text":"正文内容"},{"type":"table","rows":[["事项","状态"],["伦理信息","待作者提供"]]}]}
```
edits.json输入：
```json
{"replacements":[{"old":"唯一存在的原文","new":"授权修改后的文字"}]}
```

精确替换必须在唯一单个文本run内命中；跨run、已有修订和复杂对象可能不适用，不能据此重建整篇纯文本覆盖。render需要已有LibreOffice，支持显式--renderer；Word导出可使用宿主实际工具。XML抽取包含删除和插入文字，不代表已接受全部修订。

## PDF

```text
python "<包目录>/scripts/pdf_io.py" extract "<输入文件.pdf>" --output "<任务目录>/pdf-content.json"
python "<包目录>/scripts/pdf_io.py" render "<输入文件.pdf>" --output-dir "<任务目录>/pdf-pages" --pages 1,3-5 --scale 1.5
```

渲染成功后仍需实际看图。低字数标记不识别所有字体乱码，图片化页面不等于读懂。该脚本不含OCR。

## 基础PPTX

```text
python "<包目录>/scripts/presentation_builder.py" --input "<任务目录>/slides.json" --output "<任务目录>/presentation.pptx"
```

```json
{"title":"研究汇报","slides":[{"title":"研究问题与依据","bullets":["现有证据支持什么","本项目拟解决什么"],"notes":"这一页的讲述内容。","image":"可选的相对图片路径.png"}]}
```

不插图时删除image字段。图片路径相对JSON文件；基础版每页最多6条简短要点，过密时拆页。输出可编辑文字、图片对象和讲稿备注，不自动复刻专有模板。生成成功不代表已通过页面视觉检查。

## 科研图形

```text
python "<包目录>/scripts/research_diagrams.py" --input "<包目录>/examples/diagrams/roadmap.json" --output-base "<任务目录>/research-roadmap"
```

具体图种、字段和例子见 [科研可视化分支](../skills/research-visuals/SKILL.md)。核心图形不需要API，可编辑SVG与draw.io文件由实际节点和边生成。复杂插画与真实统计图另按任务选择可用工具。
