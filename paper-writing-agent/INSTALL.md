# 安装与使用

这是 v1.1.3 版本的论文写作综合 agent，以 Codex skill 形式提供，调用名为 `$paper-writing-agent`。ZIP 顶层只有 `paper-writing-agent/`，其内部包含所有功能分支和期刊指标数据，不需要把每个子技能另行散装。完整操作与可复制示例见包内[用户说明书](docs/user-guide.html)。

## 手动安装

1. 解压 ZIP，将整个 `paper-writing-agent` 文件夹放入目标宿主使用的 skills 目录。
2. 保持 `SKILL.md` 位于 `paper-writing-agent` 第一层，并保留内部所有相对路径。
3. 如果目标已有同名目录，先判断现有版本与需要的处理，不直接覆盖；本包不自动删除或替换已有安装。
4. 按宿主当前方式刷新技能发现或开启新任务，输入 `$paper-writing-agent` 并给出真实材料与目标。

本包不修改主 agent 选择目录；安装完成后可用 slug 直接调用。是否在 UI 立即出现取决于宿主当前技能发现机制，不能把复制文件等同当前运行对话已经热加载。

## 可选安装命令

使用现有 Python，从任意工作目录调用解压包里的脚本；`--destination` 指向目标 **skills 父目录**。

```text
python <解压目录>/paper-writing-agent/scripts/install.py --destination <目标skills目录> --dry-run
python <解压目录>/paper-writing-agent/scripts/install.py --destination <目标skills目录>
```

安装工具仅复制一个完整文件夹。它拒绝覆盖同名目标，不安装运行库，不更改全局规则、权限、其他 skill、定时任务或盘符映射。

## 使用示例

本包内置 49 个直接功能分支和 2 个嵌套支持技能，覆盖审稿、返修、文献检索、投稿信息总表、编辑询问信及 Nature 风格写作润色。主入口根据任务选择分支，无需分别安装其他 agent 或 skill。具体见[融合路由](references/integration-v1.1.md)。

- `请使用 $paper-writing-agent，精读这篇研究论文，逐图逐表解释，附原文页码。`
- `请使用 $paper-writing-agent，把这份已完成的论文精读结果做成一个可离线打开的 HTML 阅读页，保留全部图表与来源定位，支持明暗主题、手机目录和长页导航。`
- `请使用 $paper-writing-agent，根据我提供的稿号、投稿日期和系统状态，拟一封简洁礼貌的英文邮件询问稿件进度；未知字段留占位符。`
- `请使用 $paper-writing-agent，扫描当前手稿和标题页，预填跨期刊首次投稿信息总表；缺失声明先分组询问，交付 Excel 主表和由它生成的中英双语 Word 参照文档。`
- `请使用 $paper-writing-agent，我的论文已经接收但尚未收到校样，请根据接收通知拟一封英文邮件询问制作进度和下一步需要完成的事项。`
- `请使用 $paper-writing-agent，根据这批真实结果写 Methods，先给大纲，缺参数明确列出。`
- `请使用 $paper-writing-agent，翻译这篇中文稿，保持引文、数值、章节和术语，输出 Word。`
- `请使用 $paper-writing-agent，只改方括号内被标记内容，其他文字保持原样。`
- `请使用 $paper-writing-agent，逐条回复审稿意见，区分已完成修订和仍待补充的分析。`
- `请使用 $paper-writing-agent，自动连续检查这份全文 Proof 并生成报告。`
- `请使用 $paper-writing-agent，开启审稿—返修循环，最多3轮；审稿只看正文和补充材料，保留原统计结果，目标是解决实质问题并完成最终再审。`
- `请使用 $paper-writing-agent，开启最多2轮审稿—返修循环，加入PubMed近似文献与创新性评估；必要的新分析先列出，不自行重算。`
- `请使用 $paper-writing-agent，按Nature Communications的论证风格润色Discussion，保留我的数据、引文与作者声音。`

循环的“一轮”是一次返修及其再审；先有基线审稿，最多 N 轮会有最多 N+1 次审稿。需宿主真实子 agent 能力；没有该能力时会明确说明，不会用角色模拟冒充双代理。普通审稿不会自行开启循环。

未指定 Proof 模式时按逐节确认进行；明确写“自动连续全文”即可采用连续模式。已确认的方法大纲、摘要图方案和作者答案不必重复发送。

编辑询问信提供可复制的主题与正文；收到审稿意见后的逐条回复、已收到校样后的内容检查仍由各自分支处理。阅读 HTML 预设使用包内模板与 Python 标准库生成，可在普通浏览器本地打开；网页呈现不改变原精读或翻译范围。

## 包含与不包含

包内提供运行所需的 agent/skill 文件、脚本、模板与共享规则。Python 解释器、公共运行库、Word/LibreOffice、联网与宿主连接器分别见[运行依赖](references/dependencies.md)。主入口不调用安装目录之外的其他本地 agent/skill；本包不包含模型或数据库账号。

期刊指标查询已随包附带 `2025IF.xlsx` 原始表和由其构建的 `journals_index.json`，解压后位于 `skills/journal-if-lookup/data/`，不需要额外下载。直接运行查询脚本时会默认使用这个内置索引；使用自己有权使用的数据时仍可用 `--data-file` 覆盖。内置数据是带年份的离线快照，不自动代表当前指标；报告时仍要注明年份，必要时核验现行来源。

第三方组件随附的署名和许可继续适用，见[组件说明](references/provenance.md)。
