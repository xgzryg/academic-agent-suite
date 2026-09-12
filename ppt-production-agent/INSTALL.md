# 安装与首次使用

适用于 **PPT 制作与演讲综合助手 v1.0.0**，调用名称 `$ppt-production-agent`。

## 1. 确认宿主与目录

本包运行在能读取本地 skill 文档、执行文件工具及必要脚本的 AI 宿主中。完整自动制作还需要支持材料阅读和图像查看。只支持文本聊天、不能访问本地文件或执行脚本的环境，可以使用提示词和流程，但不能把建议描述成实际已生成的 PPTX。

先在宿主设置或已有技能目录中确认它实际读取的 **skills 父目录**。不把其他电脑的路径照搬到自己的环境。安装不会自动把本 agent 加入自定义的编号菜单，也不会修改全局 AGENTS.md、注册表、服务或其他 agent。

## 2. 解压并安装整个文件夹

压缩包解压后应得到一个 `ppt-production-agent` 文件夹，内部直接包含 `SKILL.md`、`skills/`、`scripts/`、`engines/`、`references/`、`assets/` 等。不要只复制 `SKILL.md`，也不要把 16 个子分支拆散安装。

手动方式：把整个文件夹复制到宿主的 skills 父目录，结果应为：

```text
<实际 skills 父目录>/
└── ppt-production-agent/
    ├── SKILL.md
    ├── agents/openai.yaml
    ├── skills/
    ├── scripts/
    ├── engines/
    ├── references/
    └── docs/用户使用说明书.html
```

也可在解压后的包根目录使用自带安装脚本。请将示例路径替换为你实际确认的目录；`--destination` 必须是父目录，脚本会自动附加 `ppt-production-agent`。

```shell
python scripts/install.py --destination "/path/to/your/skills" --dry-run
python scripts/install.py --destination "/path/to/your/skills"
```

Windows PowerShell 的等价示例：

```powershell
$SkillsParent = 'D:\YourTools\skills'
python .\scripts\install.py --destination $SkillsParent --dry-run
python .\scripts\install.py --destination $SkillsParent
```

`--dry-run` 只显示将复制到哪里，不写文件。脚本会拒绝覆盖同名已有安装；它也不安装 Python 库、不下载软件、不复制凭据、不改其他技能。升级时先按自己的版本管理方式保留旧安装，确认新的目标位置后再操作。

## 3. 检查运行依赖

先让宿主发现已有 Python 和库；已有可用环境可以直接使用。基础 PPTX 生成使用 `python-pptx` 和 `Pillow`，Word 讲稿使用 `python-docx`，PDF 提取/渲染使用 `pypdf`/`pypdfium2`，模板图表工作簿修改使用 `openpyxl`。详见 [依赖说明](references/dependencies.md)。

没有可用 Python 环境、并且你准备手动创建环境时，可在自己的工具目录中执行：

```shell
python -m venv .venv
# Windows 使用 .venv\Scripts\python；macOS/Linux 使用 .venv/bin/python
.venv/Scripts/python -m pip install python-pptx Pillow python-docx pypdf pypdfium2 openpyxl
```

上述示例是用户主动执行的依赖安装，会联网下载公共库。它不由 `install.py` 自动执行。模型服务、PowerPoint/LibreOffice、字体和网络访问按自己的环境提供。

## 4. 让宿主读取并调用

按宿主实际能力刷新技能或重启对话后，用完整 slug 调用：

```text
$ppt-production-agent
先检查可用的 PPTX 生成、文档读取和页面渲染能力，再根据我提供的材料制作演示。
```

如果宿主没有自动发现本包，可让它直接读取 `<包根>/SKILL.md`，再按主入口读取包内相对分支。无需额外安装开发机上的其他 agent。路径方式只适用于本来就支持本地文件读取的宿主；不要在不能读取文件的聊天环境中假定已经激活。

## 5. 做一份实际演示

```text
$ppt-production-agent
输入：我提供的材料文件夹和模板 PPTX。
场景：中文项目进展汇报，听众为项目组，主报告 12 分钟，问答 3 分钟。
要求：保留真实数据和单位，以当前稿为准；允许调整结构和版式。
请自动完成故事板、可编辑 PPTX、逐页备注、HTML 演讲稿和备答。
能渲染时检查最终实际 PPTX；不能完成的导出或核验准确列明。
成果保存到我指定的项目输出目录；保留原始材料。
```

命令行用户可以先运行包内合成示例。以下命令中的 `work` 指项目目录，并不是安装目录；使用绝对路径可以避免混淆。

```shell
python scripts/native_deck.py assets/examples/native-demo.json --output /path/to/project/work/demo.pptx
python scripts/speaker_pack.py assets/examples/native-demo.json --pptx /path/to/project/work/demo.pptx --out-dir /path/to/project/work/speech --docx
```

示例数据只演示软件功能，不代表真实科研或业务结果。PPTX 生成成功以后仍需查看实际渲染；讲稿同步检查也不等于完成了科学核查。

## 常见情况

- **发现不到 agent**：核对是否多套了一层目录、宿主是否读取该 skills 父目录，再使用完整 slug 或明确的 `SKILL.md` 路径。
- **提示目标已存在**：脚本正在保护已有安装或输出。确认当前版本和授权后选择新位置，或仅对允许更新的成果使用相应 `--overwrite`；安装脚本没有覆盖参数。
- **缺少库或 Office**：先查已有环境。可以先完成现有能力支持的文件，准确说明尚未渲染或导出；不要把“缺少渲染器”当成页面已经检查通过。
- **字体不同**：选用本机实际具备、适合目标系统的字体，再渲染确认换行。包不会自动安装或内嵌字体。
- **希望卸载**：确认本包安装目录后，按宿主常规方式移除该文件夹即可；项目成果保存在你自己的项目目录，与技能安装分开。
