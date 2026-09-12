# 基金、毕业论文与奖项申报助手

An academic agent for grant development, thesis writing, research award applications, evidence research, scientific diagrams, and review-driven revision. Routes tasks to 22 bundled skills and includes portable helpers for PubMed, Word/PDF, editable diagrams, and basic presentations.

一个覆盖基金论证与用户稿修改、学位论文、科技奖申报、文献证据和科研可视化的综合助手。按任务主动调用22个包内技能；可在用户明确开启后，使用宿主真实子agent完成有上限的审稿—返修循环。

- 基金：选题、立项、研究方案、基础可行性、创新与年度计划、标题摘要、润色预审。
- 毕业论文：选题开题、绪论综述、方法结果讨论、双语前后置章节、润色格式、答辩。
- 科技奖：证据与附件盘点、申报字段写作、创新贡献与应用效益、申报前核查。
- 支撑工具：文献核验、路线/流程/甘特/时间线、Word/PDF、基础PPTX、预审与修改。

从 [安装说明](INSTALL.md) 或 [离线HTML手册](使用说明.html) 开始。入口为 [SKILL.md](SKILL.md)，详细功能索引为 [feature-catalog.json](references/feature-catalog.json)。

内部技能与脚本随包提供，公共运行库、网络服务、Office渲染及真实子agent由宿主提供，详见 [依赖说明](references/dependencies.md)。年度、机构和学校规则以当次正式材料为准，适用规则快照见 [current-requirements.md](references/current-requirements.md)。

自动化在当前会话和授权范围内工作：缺少真实数据、资格信息或证明时明确留出待补项。不能保证资助、毕业、获奖或查重结果，也不会自动提交申请。
