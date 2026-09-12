---
name: journal-if-lookup
description: Look up journal names, abbreviations, ISSNs and available metrics in the bundled 2025 local index or an explicitly supplied replacement. Build an index from an authorized spreadsheet, distinguish unavailable data from no matches, and route current journal information to official online verification when needed.
---

# Journal IF Lookup

按期刊全名、缩写、ISSN 或名称片段，查询包内随附的 2025 年本地期刊索引，或查询用户显式指定的替代数据。保留准确匹配、候选消歧和相近名称提示。内置数据用于离线初筛；需要当前指标时按年份和正式来源核验。

## 使用流程

1. 默认使用包内 `data/journals_index.json`；用户提供替代索引时显式传入 `--data-file`。不要在其他项目、旧安装目录或个人数据目录静默寻找文件。
2. 只有 XLSX 时，按下面的导入命令生成项目内的新索引，再用 `--data-file` 查询。包内原始表 `data/2025IF.xlsx` 可作为已随包提供的导入来源，但不应覆盖既有索引。
3. 用户要求当前指标时，使用宿主实际提供的联网工具，在可访问的期刊官方网站或正式数据库核验。记录页面和查询日期；需要机构访问而当前不可用时如实说明。脚本本身不会联网。
4. 区分期刊身份、数据发布年、JIF 指标年和当前年份。读取记录中的 `jcr_year`、`jif_year` 与 `jif_source_column`；年份不明时标明缺失，不根据文件名或当前日期猜测。
5. 匹配含糊时列出真实候选，由用户选定或用已知 ISSN 消歧。不要把相近名称当成确定期刊，也不要将指标值赋给猜测名称。

缺少数据为“尚未执行本地查询”，不等于“期刊不存在”或“检索零命中”。JIF 不代表单篇论文的质量或创新性。中科院分区、实时引用、投稿指南及审稿周期不从缺失字段推断，应另查对应正式来源。

## 从自己的 XLSX 导入

只导入用户有权使用的文件，原表保留，输出写入明确指定的项目路径。需要 Python 3.10+ 与已有的 `openpyxl`；不要未经授权安装环境。

```bash
python "<package>/skills/journal-if-lookup/build_index.py" --data-file "<project>/journals.xlsx" --output "<project>/journals_index.json"
```

默认读取 `Journals` 工作表；其他名称用 `--sheet "Metrics"`。表头必须有 `Journal name`，空名称行被跳过。其他字段可缺失，缺失指标保持为空。

支持的主要表头：`Rank`、`Journal name`、`Abbreviated journal`、`Publisher`、`ISSN`、`eISSN`、`Categories`、`Editions`、`JCR year`、`JIF` 或 `2024 JIF` 等年份列、`5-year JIF`、`JIF quartile`、`JIF percentile`、`JIF rank`、`JCI`、`JCI quartile`、`Article influence score`、`AIS quartile`、`Total citations`。其他支持字段见 `build_index.py` 的记录映射。

只有一个 `JIF` 或 `YYYY JIF` 表头时自动选择；存在多个年度列时必须显式选择：

```bash
python "<package>/skills/journal-if-lookup/build_index.py" --data-file "<project>/journals.xlsx" --output "<project>/journals_2024_index.json" --sheet "Journals" --jif-column "2024 JIF" --source-label "My journal metrics export"
```

`YYYY JIF` 的年份原样写入 `jif_year`，不从 `JCR year` 推断指标年。使用一般 `JIF` 列时 `jif_year` 为空，报告时说明年份未指定。索引只整理表中已有值，不认证数据真实性，也不自动核验现行指标。输出已存在时拒绝覆盖，应选择新路径。

## 查询命令

直接查询（使用包内 2025 索引）：

```bash
python "<package>/skills/journal-if-lookup/query.py" "Nature"
```

替换为用户自己的索引：

```bash
python "<package>/skills/journal-if-lookup/query.py" "Nature" --data-file "<project>/journals_index.json"
python "<package>/skills/journal-if-lookup/query.py" "1471-0072" --data-file "<project>/journals_index.json" --json
python "<package>/skills/journal-if-lookup/query.py" "journal abbreviation" --data-file "<project>/journals_index.json" --top 5 --json
```

Python API：将本分支目录加入当前解释器的模块搜索路径后，使用 `from query import lookup`，调用 `lookup("Nature", top=5)` 使用包内索引；需要替代索引时传入 `data_file="<project>/journals_index.json"`。不会读取旧安装位置或其他目录中的隐式数据。

## 状态与输出

| 状态 | 含义 | 下一步 |
| --- | --- | --- |
| `ok` | 在提供的索引中找到匹配记录 | 核对身份及年份，报告已有字段 |
| `ambiguous` | 存在多个可能候选 | 展示 `candidates`，用全名或 ISSN 消歧 |
| `not_found` | 已查询提供的索引，但没有可靠匹配 | 提供 `closest`（如有），核对拼写或联网查证；不推广为全球不存在 |
| `data_unavailable` | 内置索引缺失，或用户指定的替代文件缺失 | 检查安装是否完整，或指定有权使用的数据；也可由宿主进行官方联网核验 |
| `data_error` | 索引无法读取、JSON 损坏或不是所需结构 | 检查文件或从原表重新构建，不当作零命中 |
| `error` | 查询参数无效 | 修正参数后重试 |

CLI 在成功完成本地查询（包括含糊或无匹配）时返回 0；缺数据返回 3；输入/索引错误返回 2。`--json` 返回完整结构，便于其他工作流区分这些情况。

精确结果的 `journal` 包括已知名称、缩写、出版商、ISSN、学科、JIF、5 年 JIF、分区、排名、JCI、AIS 和引用数等字段；未提供的数值为空。内部匹配键不会显示。支持 ISSN、规范化全名、缩写、首字母缩写及相近名称检索，候选分只用于身份匹配，不能用作期刊质量评分。

## 文件与运行范围

- `query.py`：标准库查询 API 和命令行。
- `build_index.py`：读取显式 XLSX，生成显式 JSON 输出。
- `__init__.py`：查询 API 导出。
- `data/README.md`：内置快照、原始表和替代数据用法说明。

工具和技能可随安装文件夹迁移。内置索引随安装目录迁移；用户自己的数据和索引仍保存在其项目里，查询时用 `--data-file` 指定，不必覆盖包内数据。
