# PPTX 工程调用说明

所有命令从综合包根目录运行，示例中的 `work` 是用户项目内的任务目录；替换为本次明确目录。宿主选择已具备依赖的 Python，不写死本机路径。`engines/easyslides/engine.py --help` 提供实际支持的命令。

## 原生 SVG 精细设计

把实际 SVG 放入 `work/svg_output/`，按阅读顺序命名，例如 `01_title.svg`、`02_result.svg`；逐页备注放入 `work/notes/` 同名 Markdown。

```shell
python engines/easyslides/engine.py svg work --output work/exports/deck.pptx
```

这会生成原生 DrawingML 文本、形状和路径，不添加默认动画/音频。位图保持图片。SVG应自含文本、形状和实际图片引用，不写指向原开发机图标库的 `data-icon`。避免 foreignObject、脚本、未支持滤镜等；出现不支持元素时修复实际SVG，不转成整页截图声称可编辑。

## 模板提取和复用

```shell
python engines/easyslides/engine.py template-assets work/template.pptx --output work/template_assets
python engines/easyslides/engine.py template-inspect work/template.pptx --output work/slide_library.json
python engines/easyslides/engine.py template-plan work/slide_library.json --slides 1,3,3,5 --output work/fill_plan.json
python engines/easyslides/engine.py template-fill work/fill_plan.json --output work/filled.pptx
```

先按真实任务编辑 fill_plan 的页面用途、文本、表格/图表数据，再填充。可选页、复用、重排，不修改模板源文件。替换文本保留各段原段落属性和首run样式；旧的局部强调不能自动对应到全新文字。表格和图表必须从当前模板提取实际ID，图表类型和系列结构以原模板及实际编辑支持为界。notes/transition计划字段不由fill执行；需要时走下文备注分支。

资产提取同时保留源特定文字/图片作为任务证据。若要制作通用模板，agent继续划分固定装饰与内容槽位、移除源研究/身份占位内容，使用第二个无关主题验证槽位复用；不能仅凭导出JSON就称通用模板完成。

## 保留混合文字格式的局部编辑

```shell
python engines/easyslides/engine.py patch-runs work/current.pptx work/run_edits.json --output work/edited.pptx
```

`run_edits.json`：

```json
{"edits":[{"slide":1,"shape_id":2,"run_index":0,"expected_text":"原文字","text":"新文字"}]}
```

slide按当前展示顺序从1计数；run_index在指定文本框内从0计数。先读取当前PPTX确认ID/内容。只改指定run的文字，其格式和其他部件保持；文字变长后仍要检查行数、溢出和视觉效果。表格文字用模板填充或专门表格编辑；本命令不冒充任意SmartArt/OLE内部编辑器。

## 添加或更新演讲备注

```shell
python engines/easyslides/engine.py notes-init work/current.pptx --output work/notes_work --name talk_notes
```

命令打印创建的项目路径。依其 `analysis/slide_index.json` 在 `notes/` 内填写对应逐页Markdown。读取并按已授权操作设置 `analysis/enhancement_plan.json`：`status` 为 `confirmed`，仅开启用户要使用的模块；notes默认启用，audio/timings/transitions默认关闭。`confirmed`只是本次已授权任务的执行状态，不能伪造用户额外批准。

```shell
python engines/easyslides/engine.py notes-apply work/notes_work/talk_notes --output work/deck_with_notes.pptx
```

实际目录可能包含日期后缀，以init打印路径为准。备注应基于当前可见页，输出后核对页序和备注覆盖。只有用户明确要求配音时才开启已有音频嵌入；自动生成声音还需要可用服务/库，不自动联网安装。

## 实际渲染、PDF及文字几何检查

Windows且安装Microsoft PowerPoint：

```powershell
powershell -NoProfile -File scripts/render_pptx.ps1 -InputPptx work/exports/deck.pptx -OutputDir work/rendered -Format both
```

生成逐页PNG、PDF和render-report.json。只关闭本任务打开的文件，不退出用户其他PPT窗口。使用新任务目录，授权更新既有导出才加 `-Overwrite`。其他平台可在已有LibreOffice环境中导出PDF并渲染逐页图；没有渲染器时如实说明，不能用SVG预览替代最终PPTX检查。

```shell
python engines/easyslides/engine.py text-check work/exports/deck.pptx --output work/text-layout.json
```

几何检查可发现部分越界/碰撞/字体问题，渲染图负责实际可读性。检查器的启发式结果须结合页面判断，不凑问题、不循环制造修复。不支持的媒体/转场和未验证路线在交付时明确标注。

包内 `assets/examples/svg-demo/` 提供两页自含SVG和同名备注的可编辑示例。若Windows报告脚本执行策略阻止当前已审读脚本，可使用 `powershell -NoProfile -ExecutionPolicy Bypass -File ...` 为本次子进程运行，不修改机器级策略。对同一PowerPoint实例串行导出；遇到应用忙或文件打开失败时保留原错误并检查文件与应用状态，不能直接宣布文件有效或反复重试。
