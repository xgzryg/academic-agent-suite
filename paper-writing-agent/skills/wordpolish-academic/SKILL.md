---
name: wordpolish-academic
description: Preserve scientific facts, author voice and academic register while editing Chinese or English manuscript prose, removing repetitive templates, repairing vague attribution, or providing structure-preserving translation. Routes only to bundled academic editing resources, with bounded passes and no AI-detection promises.
---

# 学术文风与保真编辑

先读[主包共同规则](../../references/shared-rules.md)。本分支融合本机 wordpolish 的学术调度、de-ai-writing 的保真修补，以及 humanizer-zh-academic 的中文学术表达经验；不启动营销、社媒、发布或学位论文工程流水线。

## 按任务读取

| 当前任务 | 实际读取资源 |
| --- | --- |
| 中文论文自然表达、重复模板与学术语域 | [中文学术编辑](skills/humanizer-zh-academic/SKILL.md) |
| 只改指定范围、保留作者声音、清除模板性表述 | [保真表达修补](skills/de-ai-writing/SKILL.md) |
| 保结构翻译 | [翻译规则](skills/de-ai-writing/references/translation-guardrails.md)；中译英论文术语可再读[论文翻译分支](../translate-academic-manuscript-zh-to-en/SKILL.md) |
| 英文学术或指定 Nature 风格润色 | [nature-polishing](../nature-polishing/SKILL.md) |
| 科学审稿或返修事实核查 | 返回综合主入口按审稿/返修路由处理，文风编辑不冒充科学审稿 |

默认选一个分支，读取后执行。只有存在具体未解决且职责不同的问题才追加一次互补编辑；同一分支不自循环，不用“更像人”作为无限加链的理由。新增用户修改另按新指令处理。这里的 skill 调用是读取真实文件，不是输出伪调用标签，也不表示已经启动子agent。

## 输入、范围和作者性

复用当前指定稿和已经说明的语言、用途、范围、期刊与保留项。能从材料判断的普通偏好不再次询问。关键语言目标不明或编辑会改变科学含义时，先处理不依赖该决定的部分，再询问必要信息。用户要求只改括号、指定段落或仅标出问题时严格遵守。

数字、单位、P值、区间、方向、样本量、条件、引用、专名及作者原本的立场和必要局限都受保护。具体作者声音来自提供的样本；不把样本事实搬进稿件，不发明亲历、访谈、意外发现、动机或心路历程。不要为避免“基于”“首先”等词破坏真正的方法步骤或逻辑关系。

## 完成标准

改写必须有具体可解释的阅读改善。先修真实问题，再一次检查变更涉及的含义和保护项；发现偏差就恢复/纠正受影响内容。无需为每轮制造量表、固定词频配额、检测噪声或长度比例。不声称测过某检测器，不保证AIGC率、降重率或可直接投稿。修改稿与科学创新性/原创贡献是不同判断。

默认直接交付目标正文，按需要附简短改动说明和实际缺口；用户要仅正文时按其要求，不把内部路由标签塞进论文。来源与适配见[来源说明](references/provenance.md)。
