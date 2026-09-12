# PubMed 独立执行器

执行器位于包根目录 `scripts/pubmed_evidence.py`。脚本只用 Python 标准库；从任意当前目录运行均可。实际命令中的 `<PACKAGE>` 是当前安装文件夹的绝对路径，`<TASK>` 是本次用户指定或项目内任务目录。

```text
python "<PACKAGE>/scripts/pubmed_evidence.py" --output "<TASK>/literature/search-wide.json" search --query "(topic[tiab] OR synonym[tiab]) AND method[tiab]" --limit 20
python "<PACKAGE>/scripts/pubmed_evidence.py" --output "<TASK>/literature/records.json" fetch --pmids "PMID1,PMID2"
python "<PACKAGE>/scripts/pubmed_evidence.py" --output "<TASK>/literature/related-seed.json" related --seeds "PMID1,PMID2" --limit 10
```

示例中 PMID1/PMID2 必须替换成实际检索或用户提供、随后核对身份的数字 PMID。`--limit` 是每个查询或每个种子的取回上限，1–100；`search --start` 支持当前检索窗口，PubMed 的大结果集限制需遵循 NCBI 当前规则，不能声称穷尽全库。`fetch` 每批最多100个标识，自动顺序分批。不要在循环双方并发执行多份脚本来绕过整体限速，优先由一个文献执行方取回结果供双方阅读。

脚本不要求 API key。用户已经配置 `NCBI_API_KEY` 时会自动在请求体使用；可选联系邮箱仅读取为此用途显式配置的 `NCBI_EMAIL`，不从通用邮箱变量取值。不要查看、打印、复制这些值，不生成 `.env`，不把凭据写进文献结果。所有请求固定至少间隔0.4秒，429或暂时服务失败有限重试，最长单次网络超时30秒。

输出为 JSON，包含查询及检索时间、搜索总数、query translation、实际返回 PMID、结果截断标记、完整摘要及结构化段落、内嵌XML文本、DOI/PMCID、发表类型和更正/撤稿关联字段。`read_level=record_and_abstract_only` 说明未取全文。缺失摘要并非全文不存在；取回缺失或脚本未处理的书籍记录也不等于论文不存在。

- `ok`：本次请求取回成功，不代表检索范围穷尽。
- `no_hits`：本次无语法错误的具体检索式返回零命中。
- `no_links`：已核对种子的近邻接口未返回近邻。
- `partial`：部分取回失败或结果窗口不完整；退出码1，仍保存成功部分。
- `error`：请求、解析、查询或记录取回失败；退出码1，总命中未知时使用null。禁止按零文献解释。

近邻结果按种子分组，保留 `seed_pmid`、相关PMID及NCBI相似分。相似分仅用于挑选待阅读文献，不能计算“创新性分数”、作为通过目标或替代逐篇比较。

输出文件必须在安装包外的任务目录，既有路径会被拒绝。结果只保存真实公共查询与文献内容，不保存用户稿件全文。创新性任务先读取 [查新流程](../../paper-novelty-assessment/SKILL.md)。

官方核查入口：[E-utilities说明](https://www.ncbi.nlm.nih.gov/books/NBK25499/)、[PubMed帮助](https://pubmed.ncbi.nlm.nih.gov/help/)、[使用建议与API key](https://www.ncbi.nlm.nih.gov/books/NBK25497/)、[NCBI免责声明与版权提示](https://www.ncbi.nlm.nih.gov/About/disclaimer.html)。摘要及全文可能受各自版权约束，公开访问不自动代表获准大规模再分发。实际取回只代表对应运行日期的数据库状态。
