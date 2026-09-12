# 配置、报告和轮次记录

主 agent 调用包内 `scripts/review_loop_state.py`，解析实际工具/文件结果后记录状态。这个脚本不委派、不审稿、不宣称用 JSON 能证明研究正确；它检测实际会发生的版本错配、漏掉前轮未解决问题、返修者自审和最后改稿未经再审就通过。

所有命令中的脚本路径都相对包根解析成绝对路径。下面的占位路径替换为真实任务路径，不能照字面执行。

## 配置

```json
{
  "manuscript": "manuscript.md",
  "visible_files": ["supplement.md"],
  "max_rounds": 3,
  "goal": "主张与观察性证据一致，重大问题修正且数值引用保持准确",
  "novelty": false,
  "network_allowed": false,
  "human_checkpoint": false,
  "constraints": "仅修改工作副本文字，不重算统计，不修改样本量和效应值"
}
```

输入相对路径按 config.json 所在目录解析。初始稿会复制到任务目录 `versions/v000.<ext>`，原件不变。`visible_files` 为明确允许审稿的附件；作者内部说明由调度者按角色需要传递，不自动全发。

```text
python <package>/scripts/review_loop_state.py --run-dir <task>/review-revision init --config <task>/config.json
```

## 审稿报告 review.json

```json
{
  "version": "v000",
  "manuscript": "versions/v000.md",
  "agent_id": "由实际工具返回的审稿执行标识",
  "goal_met": false,
  "can_revise": true,
  "reason": "结论用了因果动词，但方法为观察性设计，可以按已有数据收窄表述。",
  "novelty_status": "not_requested",
  "issues": [
    {"id": "R-001", "severity": "major", "status": "open", "in_scope": true,
     "evidence": "Conclusion 第1段 uses prevents；Methods 第1段 observational cohort"}
  ]
}
```

以上只是合成格式例子，不是真实审稿结果。实际 `reason`、证据及问题必须来自当前稿件；`agent_id` 由主 agent 以真实工具结果填入。问题状态为 open / partial / resolved / not_applicable / accepted_rebuttal。再审必须包含前轮所有未解决问题及本次处理状态，避免通过遗漏问题获得通过。

`novelty_status` 为 complete / partial / offline / failed / not_requested；complete 指完成约定范围的证据评估，不表示查尽所有文献。当 novelty=true，仍是 partial/offline/failed 时不能 goal_met=true。

```text
python <package>/scripts/review_loop_state.py --run-dir <task>/review-revision review --report <task>/review-revision/round-00/review.json
```

## 返修记录 revision.json

```json
{
  "from_version": "v000",
  "agent_id": "由实际工具返回的返修执行标识",
  "manuscript": "versions/v001.md",
  "responses": "round-01/responses.md",
  "summary": "将因果动词改为关联表述；原数值保持。"
}
```

先实际创建新稿与逐条回应，再记录。新稿路径必须位于当前任务 versions 目录且不同于旧稿。若附件确在授权范围内有改动，提供 `updated_visible_files` 完整当前附件列表并保留旧附件；列表相对路径按任务目录解析。主 agent 回读实际变更，不能仅靠列出附件来凑一次无改动返修。

```text
python <package>/scripts/review_loop_state.py --run-dir <task>/review-revision revision --report <task>/review-revision/round-01/revision.json
```

只有 human_checkpoint=true 且实际已获得本轮批准时，才加 `--approved`。默认连续模式不需要该参数。记录返修后状态是 awaiting_review；只有再审记录成功，completed_rounds 才增加。不能手改 state.json 把 pending 稿写成通过。

## 停止与恢复

```text
python <package>/scripts/review_loop_state.py --run-dir <task>/review-revision status
python <package>/scripts/review_loop_state.py --run-dir <task>/review-revision stop --status needs_input --reason "缺少真实伦理批件编号，其他可做修改已经完成"
python <package>/scripts/review_loop_state.py --run-dir <task>/review-revision resume --reason "作者提供了批件信息并授权继续"
```

续作先检查当前文件和 agent/进程结果，复用已有阶段；不能因上下文中断重新从第0轮开始。`resume` 仅用于条件已改变的 blocked/needs_input/user_stopped，不重置轮数。已经达到轮数上限后，只有用户另行授权追加轮次时才执行 `extend --max-rounds <新的总上限> --reason <用户授权说明>`；历史记录会保留旧上限，已完成轮数不归零。不能自行无限延长。

任何工作副本在受审后都不要原路径继续改写。新增改动写到下一个明确版本并再次审查；状态机记录不能替代这项文件操作规则。Word 的版本差异仍需内容/修订检查，不能以 ZIP 字节有变化证明实质修正。
