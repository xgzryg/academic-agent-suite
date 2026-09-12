# 演讲稿、提示卡与计时格式

主入口故事板的 `slides` 为当前顺序。每页：

- `id`：稳定且唯一的字符串/整数，重排后不重新编号。
- `title`：当前幻灯片标题。
- `notes`：实际口语正文字符串；缺省/空白意味着没有提供，导出工具不补写。
- `cues`：简短提示字符串列表；可包括强调、指图、停顿或转场提醒。
- `sources`：来源字符串列表，来自真实材料定位，不生成虚假文献。
- `duration_seconds`：可选非负数，代表当前已提供计划的每页秒数；省略时才用文字估算。

屏幕文案由页面自身布局字段承载，不能把 `notes` 全段搬到屏幕。其他字段按主故事板规范使用。本文件只定义讲稿相关部分，不创建第二份故事板标准。

## 提取、核对与输出

`scripts/speaker_pack.py` 可读取 JSON 或 PPTX：

```text
python scripts/speaker_pack.py current.json --out-dir output --pptx current.pptx --docx
python scripts/speaker_pack.py current.pptx --out-dir output
python scripts/speaker_pack.py current.json --pptx current.pptx --check-only
```

PPTX 提取沿当前页序；原生生成器的标题框名 `ppa-title:<id>` 用于稳定映射。普通外部 PPTX 使用 `slide.slide_id`；真正标题占位框优先，缺标题则使用首个非空文本框，完全无文字则留空。源备注不存在时保留缺项，不创建假稿；独立提示卡/来源列表不能从普通备注里自动还原。

JSON 加 `--pptx` 将核对当前页数、逐页 ID、标题和正文备注；实质不一致时以非零状态失败，不导出错版讲稿。只统一首尾空白和换行，不删除或改写实际文本。检查不证明全部页内数字/图像相同，仍需主 agent 做内容核对。PPTX 用户改稿后，应先以当前成品更新对应工作稿，再重新同步。

输出：
- `speaker_notes.md`：当前顺序的逐页稿、提示卡、来源和时间。
- `speaker_notes.html`：离线分页讲稿、提示卡/全文切换、跳页、本页/全场练习计时，支持打印全文。
- `speaker_pack_report.json`：缺备注页、当前 ID、同步状态和估时参数。
- `speaker_notes.docx`：仅用 `--docx` 时生成，需 python-docx。

默认检查所有将写出的同名文件并拒绝覆盖。根据本次明确修改授权可传 `--overwrite`；工具不修改输入 PPTX 或 JSON。

## 估算的含义

默认中文 230 字/分钟、英文 130 词/分钟、有正文页面另加 5 秒停顿，可用 `--zh-cpm`、`--en-wpm`、`--pause-seconds` 修改。中文基本/扩展 A 汉字按字符计，英文按单词计，数字串粗略按一词计；混合文字分开累计。符号、化学式、方程、演示、互动、问答及真实讲述习惯可能让时间差异很大，所以这是计划辅助，不是语音测量。

如果页面提供 `duration_seconds`，累计时间使用该计划，并另外报告文字估计；计划不足以讲完当前文字时给提醒。缺正文且无计划时估计为零，并明确缺备注，不能用零假装该页无须讲述。

用户确认总时段是否包含问答后，再由主 agent 预留相应时间。完整逐字稿与简版路线要实际修改内容；工具不会自动压缩文字或生成问答。

## HTML 边界

HTML 没有外部脚本、字体或网络请求。正文按文本呈现，不执行用户稿中的 HTML/脚本片段。练习计时在打开的浏览器页面内运行，停止/重置由用户控制；关闭页面不后台运行，不记录录音，不自动操控 PowerPoint。页面中的“演讲模式”指便于阅读的分页稿与提示卡，不等于双屏 PowerPoint Presenter View。

