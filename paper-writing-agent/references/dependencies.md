# 运行依赖与独立性

本包的 **agent/skill 指令、分支、辅助脚本、模板与共享资源** 均在同一文件夹中。运行不读取安装目录之外的其他 skill 目录。核心文本任务只需要能阅读文件的模型宿主，不需要先装 Office 或全部 Python 库。

| 能力 | 实际依赖 | 缺失时如何处理 |
| --- | --- | --- |
| 主入口、写作、翻译、评审、返修等文本分支 | 模型宿主及读取 Markdown 的能力 | 本包不包含模型权重或账户；由当前宿主执行 |
| Highlights/选刊脚本、精简计数、安装 | Python 3.10+，标准库 | 可先手工解压、进行文本工作；不能声称脚本已运行 |
| 精读 HTML 阅读页 | Python 3.10+ 标准库、包内模板和本地浏览器 | 主题、目录及阅读功能无需 CDN；没有浏览器时标明交互与版面未实测 |
| Word 内容提取 | Python 标准库 | 可用宿主文档阅读能力，说明读取范围 |
| Word 报告创建、Proof 报告 | python-docx | 先交请求允许的文字草稿；若必须 Word 则说明缺库 |
| Word 精确修改/修订 | lxml；完整对象编辑还需相应 OOXML/Office 能力 | 简单帮助程序只支持唯一文本 run 内替换；跨 run/复杂对象需保留原包进行针对编辑 |
| PDF 文本提取 | pypdf | 可用已有 PDF 阅读工具；扫描件需要 OCR/视觉 |
| PDF 页面渲染 | pypdfium2、Pillow | 有宿主 PDF 页面查看可替代；没有则明确视觉未核验 |
| PDF 表格/OCR（任务需要时） | 可用 pdfplumber/OCR 服务或软件 | 回到原始表格/可读页面；不编缺失单元格 |
| Word/PPT 页面排版渲染 | 现有 Word/PowerPoint 或 LibreOffice | 交付时注明版面未验；必须版面验收的任务保留此缺项 |
| XLSX、PPTX | openpyxl、python-pptx 或当前宿主相应工具 | 可先交 CSV/结构稿，仅在符合用户交付要求时使用；不把替代格式称原格式 |
| 投稿信息总表与 Word 参照文档 | openpyxl、python-docx；可选 Word/LibreOffice 用于版面渲染 | 依赖缺失时保留已抽取事实和缺项清单，明确不能生成要求的 XLSX/DOCX；不自动安装，不把临时 JSON 当第二资料源 |
| 定量图/PDF生成 | 按实际方案使用 Matplotlib/R/ggplot2/ReportLab | 不能仅凭 skill 文本生成真实统计结果；已有数据/库决定可运行方案 |
| 最新文献/选刊与数据库 | 实际联网搜索/浏览器/机构数据库权限 | 使用本地证据并标截止日期；不伪造当前 JIF、APC、风险状态 |
| AI 图像生成与图像编辑 | 当前宿主实际图像工具和相应权限 | 可交文字方案或可编辑 SVG 示意；不虚称 AI 生图已执行 |
| GUI、Sites、插件/MCP、定时、Goal、远程、任务管理 | 当前宿主暴露的工具、账户和用户授权 | 给准备好的手工步骤/简报，不模拟已创建服务 |
| 双子 agent 审稿—返修循环 | 当前宿主真实委派工具；Python 3.10+ 用于可选轮次记录 | 无委派工具时说明限制，不能假装已创建审稿/返修实例；只有用户接受后改用顺序单 agent |
| PubMed search/fetch/related | Python 3.10+ 标准库和 NCBI 网络访问 | 无 API key 可低速使用；缺网报告未执行/失败，不能当零命中。可用 NCBI_API_KEY / NCBI_EMAIL，但不随包分发或记录值 |
| 审稿/回复同步报告 | python-docx；任务内审稿材料的 PDF 提取需要 pypdf | 使用包内报告渲染与材料提取工具；只依据任务实际提供或读取的材料 |
| Nature 一致性与回复检查 | Python 标准库 | 检查是线索，回到上下文判断，不能机械改数字或把检测器当统计检验 |
| 期刊指标查询 | Python 标准库即可使用包内 `skills/journal-if-lookup/data/journals_index.json`；从用户表格构建新索引还需 openpyxl | 安装包附带带年份的本地索引和原始 `2025IF.xlsx`；无须额外数据即可离线查询。它不是实时指标，报告时注明年份并按需要核验现行来源；`--data-file` 可覆盖内置索引 |
| 条件批量全文下载 | Python 3.11+（tomllib）、Playwright及可用浏览器；PDF DOI辅助识别可用PyMuPDF | 先查现有环境，不自动装库/下载浏览器或复制个人登录凭据；输出与浏览器profile显式放任务目录；登录操作由用户掌握 |

`requirements.txt` 只列脚本及常用输出的公共 Python 库，**安装工具不执行 pip/npm、不改环境**。目标环境有官方运行时发现工具时优先使用它；否则使用用户明确提供或现有可用解释器。实际版本记录在任务验证中，不以单一环境的版本约束所有使用者。

若用户要求零联网、连解释器与依赖库也离线打包，需要另行指定目标系统/架构并制作运行时分发包；当前交付的独立性范围是一个可移植 agent/skill 目录。

优先使用当前环境的可用字体，不固定个人字体路径。缓存、临时文件和渲染输出写入当前任务目录；安装包本身保持工具与知识文件，不堆入每篇论文的结果。

NCBI E-utilities 的接口与访问要求见[官方接口文档](https://www.ncbi.nlm.nih.gov/books/NBK25499/)及[使用说明](https://www.ncbi.nlm.nih.gov/books/NBK25497/)。PubMed摘要可能有独立版权，参见[NCBI免责声明与版权说明](https://www.ncbi.nlm.nih.gov/About/disclaimer.html)。近邻分值用于发现候选文章，不是创新性评价分。
