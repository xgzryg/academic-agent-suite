# 回复策略与完成状态

原材料标题写21项，实际表格只有20项；本包按实际20项保留，不补造第21项。

| Strategy | When appropriate |
|---|---|
| `acknowledge_and_correct` | Reviewer spotted a real error in the manuscript |
| `clarify_existing_content` | Reviewer misread or under-read the manuscript |
| `add_textual_explanation` | The point belongs in the manuscript, not as a new analysis |
| `add_reference` | A prior reference supports the omitted context |
| `add_method_detail` | Methods section needs more detail |
| `add_statistical_analysis` | A reviewer-requested analysis can be run on existing data |
| `add_robustness_analysis` | Sensitivity, alternative model, resampling, etc. |
| `add_control` | A control experiment can address the concern |
| `add_experiment` | A reviewer-required wet-lab or clinical experiment is feasible |
| `add_validation_dataset` | Independent cohort / dataset needed |
| `moderate_claim` | The claim is too strong for the evidence — hedging |
| `change_terminology` | Replace an over-strong word or phrase |
| `restructure_figure` | Re-arrange panels / labeling |
| `move_content_to_supplement` | Promote or demote content for readability |
| `provide_data_or_code` | Make anonymized data or code publicly available |
| `explain_infeasibility` | Request is genuinely not feasible in this revision cycle |
| `respectfully_disagree` | Reviewer is wrong, with evidence |
| `request_editor_adjudication` | Reviewer conflict / scope issue belongs with editor |
| `defer_to_future_work` | The issue is real but out of scope; mark for future study |
| `withdraw_claim` | The claim is not supportable even after analysis |



基础8状态：DONE、DRAFTED、TODO_TEXT、TODO_ANALYSIS、TODO_EXPERIMENT、TODO_AUTHOR_CONFIRM、NOT_FEASIBLE、PROPOSED_DISAGREEMENT。为与Nature Response同步，支持 VERIFIED_DONE 和 REPORTED_DONE_UNVERIFIED 两个精确标签。DONE/VERIFIED_DONE 只用于已核对实际产物，必须附 verification.path 与 verification.excerpt；渲染器检查该摘录实际存在。作者口述完成但无产物用 REPORTED_DONE_UNVERIFIED。草稿不是实验，计划不是结果。

正式回应仍覆盖直接回答、理由/证据、实际改动、修订位置、作者待办五项逻辑。子问题不能漏；不同意要依据，不能靠防御修辞；不能为满足审稿而虚构实验、删除不利结果或不当提升因果/创新性结论。全部未来行动保持未来态。

对照 [详细行动映射](../../nature-response/references/action-mapping.md) 与 [返修困难情况](../../nature-response/references/difficult-cases.md)。
