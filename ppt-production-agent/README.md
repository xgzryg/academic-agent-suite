# PPT 制作与演讲综合助手

**PPT Production & Speaking Agent · v1.0.0**

一个覆盖演示策划、可编辑 PPTX 制作、模板复用、已有稿修改、逐页演讲稿和答辩排练的综合助手。根据任务主动读取包内技能，支持学术汇报、毕业与开题答辩、教学培训、病例讨论、商务及公众演示。

An integrated agent for presentation planning, editable PowerPoint production, template reuse, deck editing, slide-aligned speech writing, and rehearsal. It routes tasks to bundled skills and supports academic, teaching, clinical case, business, and public-facing presentations.

## 开始使用

1. 解压安装包，保留完整的 `ppt-production-agent` 文件夹。
2. 按 [安装说明](INSTALL.md) 放入宿主实际使用的 skills 目录，或让支持本地文件的宿主读取本包 `SKILL.md`。
3. 在对话中调用 `$ppt-production-agent`，提供材料、受众、时长、输出目录和当前模板。

```text
$ppt-production-agent
根据附件论文制作 15 分钟中文组会汇报，另留 5 分钟问答。
听众有生物医学基础；突出研究问题、关键图表、证据与局限。
请自动完成可编辑 PPTX、逐页备注、HTML/Word 演讲稿和备答。
输出到我指定的项目目录；原始文件保留。缺少关键事实时指出具体缺项。
```

完整说明见 [离线 HTML 用户手册](docs/用户使用说明书.html)，包含每项功能、调用示例、自动制作和修改方法。HTML 可以直接在浏览器打开，无需联网。

## 能做什么

| 内容与场景 | 制作与设计 | 讲述与交付 |
| --- | --- | --- |
| 策划与故事板 | 页面视觉设计 | 逐页演讲稿、提示卡与备注 |
| 文献/组会/会议/毕业/开题/项目答辩 | 原生文本、形状、表格与图表 | 中英文与双语表达、计划估时 |
| 教学培训、继续教育与科普 | SVG 精细排版与对象级导出 | 问答、备用页与互动排练 |
| 病例讨论与临床教学 | 模板提取、复用与填充 | 明确开启的有界审查—修改循环 |
| 工作/产品/技术/商业演示 | 当前 PPTX 局部编辑、图片辅助重建 | PDF/PNG 导出与实际页面核查 |
| 文献资料提取、PubMed 与证据对应 | 统一版式、可读性和图表呈现 | Markdown、离线 HTML、可选 Word 讲稿 |

## 包的形式与能力边界

这是安装到 AI 宿主的 agent/skill 文件夹，包含主入口、16 个功能分支、选定 PPTX 引擎和辅助脚本。运行时使用包内相对路径，不依赖开发机原有 agent 文件夹。它不是独立桌面应用，也不包含大模型、Python、Office、字体或外部数据库服务。

原生文字、形状、表格和原生图表可继续编辑；照片与插入位图仍是图片。SVG 图表转换后通常是形状，不自动带有 PowerPoint 数据工作表。复杂 SmartArt、OLE、动画和媒体需要按实际输入与工具判断，不承诺任意文件一键无损转换。

模型负责依据真实材料组织和撰写内容，脚本负责生成、提取、同步和导出。没有备注的 PPTX 不会被工具自动补成完整演讲稿；缺失的事实、数据和引用也不会自动补造。

## 文档与示例

- [安装与首次调用](INSTALL.md)
- [用户使用说明书](docs/用户使用说明书.html)
- [运行依赖](references/dependencies.md)
- [故事板与原生页型](references/storyboard-format.md)
- [高级引擎、模板与编辑命令](references/engine-usage.md)
- [讲稿格式与估时](references/speech-format.md)
- [组件说明](references/components.md)
- [中性合成示例故事板](assets/examples/native-demo.json)
- [四页中性学术模板](assets/templates/neutral-academic.pptx)
- [按需审查—修改循环](references/review-iteration.md)

普通任务自动完成必要检查，不自动开启多轮子 agent、后台定时任务、上传或发送。需要有界循环时，明确最大轮数、完成目标和修改范围；是否能使用真实独立子 agent 取决于宿主。
