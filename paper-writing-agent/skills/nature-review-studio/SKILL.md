---
name: nature-review-studio
description: "论文审稿与作者回复的12维证据框架、20项实列策略和真实完成状态；内置同步DOCX/Markdown渲染及任务内资料提取，不依赖旧NRS项目。"
---

# Nature Review Studio · 便携融合版

读取 [便携规则](PORTABLE.md) 和 [流程](references/workflow.md)。本包保留本机 NRS 的12维审稿框架、20项实际列出的回复策略及8项基础状态，并采用新版 Nature Reviewer 的独立性与证据规则。

| 模式 | 实际实现 |
| --- | --- |
| review | 以当前可见稿件形成可定位的审稿意见；由内置脚本渲染同步 DOCX + MD |
| respond | 逐条回应真实意见或明确模拟意见，核对完成证据；可生成内部同步工作报告；正式作者回复走 Veritas/Nature Response |
| update / learn | 仅在用户要求学习新审稿材料时提取其明确提供的 PDF/DOCX/TXT/MD，形成任务内经验草稿；不宣称重建原1287案例数据库 |

本机原 `.nrs_root` 指向的旧项目不存在，原渲染器、案例库、检索索引和蒸馏管线不在安装目录。这里用实际内置工具替换运行缺口，不读取任何本机固定路径，也不宣称拥有1287篇原始审稿文件。

审稿内容用 [review-axes](references/review-axes.md)，回复策略用 [response-axes](references/response-axes.md)，核查用 [adversarial-checklist](references/adversarial-checklist.md)。

```text
python <本分支>/scripts/render_review_docx.py --payload <任务目录>/payload.json --out <任务目录>/review.docx
python <本分支>/scripts/ingest_prf.py --input <明确提供的材料> --out <任务目录>/prf-extracted.json
```

[渲染 schema](references/render-docx.md) 描述实际字段。路径由当前加载技能根目录解析；输出明确在项目/任务目录。需要 python-docx；PDF输入另需 pypdf。脚本不安装依赖，不编内容、不训练模型、不自动创建子agent。
