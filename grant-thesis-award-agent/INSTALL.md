# 安装与首次调用

本包名称：grant-thesis-award-agent，版本1.0.0。它是供支持本地SKILL.md的AI宿主使用的一套技能，不是双击启动的独立桌面软件。

1. 将ZIP解压到一个普通目录，确认只有一个顶层grant-thesis-award-agent文件夹，里面直接可见SKILL.md。
2. 找到你当前AI宿主实际使用的skills父目录。将整个文件夹复制进去；不要把22个子技能拆成全局目录。每个宿主的发现路径可能不同，以其当前配置为准。
3. 也可在终端使用已有Python：

```text
python "<解压目录>/grant-thesis-award-agent/scripts/install.py" --destination "<宿主实际skills父目录>" --dry-run
python "<解压目录>/grant-thesis-award-agent/scripts/install.py" --destination "<宿主实际skills父目录>"
```

--destination传父目录，脚本会建立唯一的grant-thesis-award-agent子文件夹；若已存在会停止并保留旧安装。安装不修改主角色目录、全局AGENTS.md、系统服务或环境，不自动安装依赖。

4. 按宿主实际支持方式刷新或重新打开会话，然后输入：

```text
请使用 $grant-thesis-award-agent。我的任务是……，当前材料在……，本次输出保存到……。请按任务调用需要的内置分支，完成授权范围内的工作并列明待补项。
```

5. 若宿主不支持$调用但能读取文件，可让它读取安装目录SKILL.md，按入口流程执行。如果技能没有显示，核查实际配置路径与目录层级，不要反复复制到猜测的目录。

完整功能与自动化示例见 [使用说明.html](使用说明.html)，工具运行条件见 [依赖说明](references/dependencies.md)。需要升级时先保留已有安装及人工修改，再按用户批准的替换方案处理；本安装器不提供强制覆盖。
