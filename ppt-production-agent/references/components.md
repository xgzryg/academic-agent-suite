# 版本与内置组件

版本：1.0.0。调用入口：`$ppt-production-agent`。安装后为一个同名独立目录。

| 组件 | 包内位置 | 用途 |
| --- | --- | --- |
| 主入口与 16 个专业分支 | SKILL.md、skills/ | 按场景读取适用指引并完成任务 |
| 原生 PPTX 生成器 | scripts/native_deck.py | 12 种页型、5 类原生图表、5 种主题、16:9/4:3、实际备注 |
| SVG 与模板工程核心 | engines/easyslides/ | SVG→DrawingML、模板分析和填充、原对象文字编辑、素材提取 |
| 演讲包工具 | scripts/speaker_pack.py | 当前页序/ID/标题/备注核对，MD/JSON/HTML 和可选 DOCX |
| 文档与证据工具 | scripts/pdf_io.py、document_io.py、pubmed_evidence.py | PDF/Word 材料提取与公共 PubMed 记录查阅 |
| PowerPoint 导出 | scripts/render_pptx.ps1 | Windows 已有 PowerPoint 条件下导出当前 PPTX 的 PNG/PDF |
| 安装工具 | scripts/install.py | 复制整个包至显式指定的技能父目录，保留已有同名安装 |
| 中性模板与合成例子 | assets/templates/、assets/examples/ | 作为实际可编辑起点与工具用法示例 |

场景规则已在包内整合。运行时不会回到构建机器寻找其他 agent 或 skill。外部公共库、宿主模型、网络服务、Office 与字体是[运行条件](dependencies.md)，不随 ZIP 提供。

SVG 核心含 EasySlides 选定模块及本包适配，保留其 [MIT 许可证](../engines/easyslides/LICENSE)与[适配说明](../engines/easyslides/ADAPTATIONS.md)。其余新编排、工具和示例由本项目编写。示例数据明确为合成资料，不能替代用户的研究、病例或业务证据。

“高级引擎”不代表任意 SVG、SmartArt、动画、公式或媒体均可无损转换。按实际对象与真实渲染报告完成范围。生成脚本不会自行写作；内容理解、演讲稿撰写、审查判断和可选子 agent 调度由宿主执行本包工作流完成。
