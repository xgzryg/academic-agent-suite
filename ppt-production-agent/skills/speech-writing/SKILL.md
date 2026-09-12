---
name: speech-writing
description: Write and revise Chinese, English or bilingual slide-aligned oral scripts, speaker notes, cue cards, openings, transitions and closings. Extract actual notes from current PPTX and export Markdown, offline presenter HTML and optional Word without inventing missing speech content.
---

# 演讲稿与逐页备注

主 agent 沿用已确认的任务、当前稿和授权。该分支负责语言和讲述；`../../scripts/speaker_pack.py` 只负责提取、核对、估时与格式化，不是语言模型写作器。

## 使用方式

先读 `../../references/speech-format.md`。用户只要求某页修改、开场或全文稿时直接完成该范围；无需重建全部 PPT。没有幻灯片时可先根据用户提供的材料写独立演讲稿，但不能宣称已与不存在的 PPT 同步。

1. 识别受众、使用语言、讲述目的、时长是否含互动/问答和作者口吻。复用上下文，只有决定内容的事实确实缺失时才问；一般偏好采用明确说明的默认。
2. 读取当前 PPTX 的顺序、标题、实际备注和相关素材，或当前 JSON 故事板。旧故事板与人工修改后的 PPT 冲突时，先协调当前内容，不用旧 JSON 覆盖。
3. 编写三层文字：屏幕短文案、逐页提示卡、完整口语稿。保留数字、单位、基因/方法/药物名、引用、结论强度和作者身份。讲稿解释图表和上下页关系，不能只照读 bullets。
4. 每页以稳定 `id` 对应正文 `notes`。口语稿使用完整可说出的句子；`cues` 记录强调、指图、停顿或转场提醒，不把没有根据的演示效果写成已实现。
5. 根据内容重要性与实际资料安排篇幅；需要压缩时先去重复和非必需例子，把技术细节移到备用页，保留关键证据与结尾。不靠单纯加快语速凑时长。
6. 做过修改就同步对应故事板、实际 PPT notes 与交付的 Markdown/HTML/Word。需要核对的事实或未提供备注逐项说明，不编造补齐。

双语稿按用户选择分段对照或分别输出；中英文表达支持同一科学结论，不以译文“流畅”之名强化原文。中文指引听众、停顿和必要的转场可自然保留，不机械删除所有“接下来/我们先看”。

## 工具调用

从包根调用：

```text
python scripts/speaker_pack.py storyboard.json --out-dir <output-directory> --pptx current.pptx --docx
python scripts/speaker_pack.py current.pptx --out-dir <output-directory>
python scripts/speaker_pack.py storyboard.json --pptx current.pptx --check-only
```

省略 `--docx` 时输出 Markdown、单文件 HTML 和简短报告。输入 PPTX 时按当前页序取真实备注；没有 `ppa-title:<id>` 标记的普通 PPTX 用 PowerPoint slide_id 作为 ID。该导入不自动恢复单独的提示卡或参考文献清单。

`--zh-cpm`、`--en-wpm` 和 `--pause-seconds` 可以调整估时。若当前目标已存在，默认拒绝替换；沿已有修改授权核对后可用 `--overwrite`，否则选新输出目录。

## 交付与边界

- 默认给实际请求的稿件；需要文件时提供完整路径。缺原稿/备注要报告缺项。
- HTML 支持分页、提示卡、全文、跳页及本地练习计时；它不自动控制 PowerPoint、不合成语音、不在关闭后继续运行。
- 文字估时不是实测试讲；无法知道的演示/互动时间由任务简报另行安排。
- 不编个人经历、患者故事、名人/研究者引语、机构署名和联系方式；用户提供引用时核对其原意与归属。

