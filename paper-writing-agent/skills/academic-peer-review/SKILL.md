---
name: academic-peer-review
metadata:
  original_author: 迪娜
  original_channel: 公众号「迪娜学姐」
  original_version: '4.1'
  adaptation: paper-writing-agent
description: >
  Universal academic peer review skill for evaluating research manuscripts before journal submission.
  Covers all disciplines (sciences, humanities, social sciences, engineering, medicine, etc.)
  and both Research and Review article types. The skill calibrates review standards to the
  target journal's actual publication level by learning from user-provided sample papers.
  Use this skill whenever the user asks to review, evaluate, critique, or assess an academic
  paper, manuscript, or draft — including requests like "帮我审稿", "review my paper",
  "evaluate this manuscript", "给我评审这篇论文", "peer review", or similar.
  Also trigger when users mention journal submission, pre-submission check, or manuscript
  quality assessment.
---

# Academic Peer Review Skill

Read [shared rules](../../references/shared-rules.md) before this branch. Resolve all paths from this skill directory, never the shell working directory. Use [paper-documents](../paper-documents/SKILL.md) for Word and [paper-pdf](../paper-pdf/SKILL.md) for PDF; these are bundled dependencies. Source attribution is retained in metadata, not inserted as the author of new user deliverables.

## Document roles and review mode

Use the user's explicit labels: sample papers calibrate the venue; the manuscript is the draft to review; reviewer letters are incoming comments. Arrival order never changes these roles. List filenames and actual roles when several documents could be confused; ask only about unresolved roles. A manuscript already supplied remains available throughout the workflow.

Use **venue-calibrated review** when suitable journal samples are available or the user requests that mode. Use **general manuscript review** when the user requests useful review without sample calibration; disclose that limitation and do not claim venue-specific acceptance odds. Reuse supplied information and complete independent work while calibration material is missing.

Three principles govern both modes: evidence anchoring in the manuscript; proportionate venue calibration while maintaining scientific/ethical validity at every tier; and constructive specificity about each problem, consequence and feasible correction within the author's research question.

Workflow: establish context and roles → optionally learn venue samples → read the complete manuscript → evidence-anchored review → authorized revision guidance. These are analytical stages, not repeated upload or approval rounds.

## Step 1 — Collect context

Identify the target journal, article type and available samples from supplied materials. Infer Research versus Review when clear. The journal is optional for general review; when journal fit is requested, check current official Aims & Scope within the active network boundary.

For venue calibration, prefer 2–3 recent full Research articles or 1–2 full Review articles with a similar topic or approach and preferably different author groups. This is a useful sampling default, not a demand to upload again. When examples are unavailable, disclose missing calibration and proceed with useful authorized general review.

List received documents by filename/title and actual role. Never relabel an explicitly supplied draft as a sample because it arrived early. Do not demand a second manuscript upload after calibration.

## Step 2 — Learn venue standard when applicable

Read sample papers as examples and extract the patterns below. In general-review mode, skip unsupported venue inferences. Published samples do not authorize lowering scientific or ethical requirements. Keep concise evidence-based calibration notes; give relevant rationale without hidden chain-of-thought.

### What to extract from each sample paper

Read each sample paper and extract the following characteristics:

**For Research Articles:**
- Novelty level: Is the contribution a paradigm shift, a significant advance, an
  incremental improvement, or a new application/validation?
- Methodology depth: How many experiments/analyses are reported? What is the
  typical sample size or dataset scale? How thorough are the controls?
- Statistical rigor: What statistical methods are used? Are effect sizes, confidence
  intervals, and multiple comparison corrections standard?
- Discussion depth: How extensively do the authors interpret results, acknowledge
  limitations, and connect to the broader field?
- Citation density and recency: How many references? What proportion are from the
  last 5 years?
- Figure/table count and quality: How many display items? What level of polish?
- Supplementary material: How much supplementary content is typical?

**For Review Articles:**
- Scope breadth: How broad or narrow is the topic coverage?
- Analytical depth: Is the review primarily descriptive (summarizing findings) or
  critically analytical (synthesizing, comparing, identifying contradictions)?
- Systematic methodology: Is a systematic search strategy described? PRISMA or
  similar framework?
- Use of tables/figures: Are there summary tables, conceptual frameworks, or
  visual models?
- Identification of gaps: How explicitly are research gaps and future directions
  articulated?
- Balance and objectivity: Does the review present multiple perspectives on
  contested topics?

### Build the internal rubric

Synthesize the patterns from all sample papers into a 7-dimension rubric.
For each dimension, define what "meets journal standard" looks like at this
specific venue, based on the evidence from the sample papers.

The 7 dimensions:

1. **Novelty and contribution** — What level of novelty does this journal expect?
2. **Methodological rigor** — What depth of experimental/analytical work is standard?
3. **Data sufficiency and analysis** — Are the data and statistical analyses adequate
   for claims of this scope?
4. **Logical coherence** — Do the hypotheses, methods, results, and conclusions form
   a consistent chain of reasoning?
5. **Writing quality and clarity** — Is the manuscript written at the level expected
   by this journal's readership?
6. **Relevance to journal scope** — Does the work fit what this journal publishes?
7. **Ethical and reporting standards** — Are field-specific reporting guidelines
   followed (e.g., CONSORT, PRISMA, ARRIVE, STROBE, MIAME)?

For each dimension, mentally assign the manuscript a rating:
- **Exceeds** journal standard
- **Meets** journal standard
- **Below** journal standard — specify what's missing
- **Far below** — specify what's fundamentally lacking

Use the dimensions to organize real findings. Classify severity by the concrete effect on validity, interpretation and publication readiness, not a rubric label or a comment count. When no material issue is present, say so plainly.

### Transition to manuscript review

When calibration was performed, give a short 3–5 sentence description of the learned venue patterns and their limits. Then use the identified manuscript. Ask for it only if absent.

## Step 3 — Read the manuscript

Read the complete requested manuscript before finalizing comments. Identify the central claim, design, supporting results and argument chain, maintaining a location map. For incomplete materials, state exactly what was covered and do not infer unseen results or methods.

## Step 4 — Multi-stage review

Before writing any review comments, read `references/review-examples.md`.
It contains curated examples of excellent peer review comments from open-access
journals (eLife, Nature Communications). These examples demonstrate the level
of specificity, evidence anchoring, and constructive tone your review should
achieve. Pay special attention to the five qualities of a good comment
(pinpointed, evidenced, consequential, actionable, proportionate) and the
anti-patterns to avoid.

This is the core output. It follows a structured sequence inspired by
DeepReviewer's multi-stage reasoning chain.

### Stage A: Novelty and scope check

Before diving into details, assess two threshold questions:

1. **Scope fit**: Does this manuscript fall within the target journal's stated
   Aims & Scope? If not, flag this immediately — it may warrant desk rejection
   regardless of quality.
2. **Novelty calibration**: Compared to the sample papers you analyzed, does
   this manuscript's contribution meet the novelty threshold for this journal?
   Be explicit: "The sample papers from [journal] each introduced [X-level]
   innovations. This manuscript's contribution is [comparison]."

If either check fails critically, state this upfront before proceeding.

### Stage B: Overall assessment (总评)

Write 200–300 words summarizing:
- The manuscript's main content, research question, and key findings
- Its innovation level and significance, calibrated to the target journal
- Overall research quality and writing level
- How it compares to the sample papers from this journal

This must be specific, not generic. Name the research object, dataset size,
main method, and principal finding. A reader of only this paragraph should
understand what the paper is about and whether it's likely publishable at
this venue.

### Stage C: Major comments (主要问题)

These are issues that, if not addressed, would prevent acceptance at the
target journal. Report every actual major issue; there is no minimum or target count. If none exists, say 'No major issues identified.' Never manufacture issues.

**For Research Articles, systematically check:**
- Is the research hypothesis clearly stated and well-motivated?
- Is the study design appropriate for the research question?
- Are there critical methodological gaps (missing controls, inadequate
  sample size, inappropriate statistical tests)?
- Are the data sufficient to support the claims? Are there over-interpretations?
- Are the conclusions fully supported by the results?
- Are there important alternative explanations not considered?
- Are there ethical concerns (IRB approval, informed consent, animal welfare
  protocols, data availability)?

**For Review Articles, systematically check:**
- Is the scope well-defined and justified?
- Is the search strategy systematic and reproducible?
- Is the coverage balanced, or are important perspectives missing?
- Is the synthesis critical (identifying contradictions, evaluating evidence
  quality) rather than merely descriptive?
- Are research gaps and future directions clearly articulated?
- Is the organizational structure logical and easy to follow?
- Are the conclusions supported by the evidence reviewed?

**Each major comment must follow this structure:**

```
### [Issue number] [Descriptive title]

**Location**: [Specific section, paragraph, figure, table, page, or line]

**Issue**: [Precise description of the problem, with direct reference to
the manuscript text. Quote or paraphrase the specific passage.]

**Impact**: [Why this matters — how it affects the validity, interpretability,
or contribution of the work]

**Recommendation**: [Concrete, actionable suggestion for how to fix it]

**Suggested revision** (when applicable): [Draft revised text, revised
analysis approach, or additional experiment needed]
```

### Stage D: Minor comments (次要问题)

Issues that should be fixed but would not individually prevent acceptance.
These may include:

- Language and grammar issues (with specific corrections)
- Figure/table formatting problems (with specific suggestions)
- Citation issues (missing references, incorrect formatting, outdated sources)
- Minor logical gaps or unclear phrasing
- Terminology inconsistencies

If there are no minor issues, explicitly state: "No minor issues identified."
Do not fabricate issues.

**Each minor comment must specify the location and provide a concrete fix.**
Vague minor comments like "improve the writing" are not permitted.

### Stage E: Decision recommendation (整体意见)

Based on your internal rubric assessment and the comments above, provide
a clear recommendation:

- **Accept (接收)**: All 7 rubric dimensions meet or exceed the journal standard.
  No major issues. Minor issues only.
- **Minor Revision (小修)**: The core study is sound and remaining local issues are addressable without new experiments or fundamental restructuring.
- **Major Revision (大修)**: Substantive but feasible work is needed to support interpretation or reproducibility; the core contribution remains sound. Severity, not comment count, controls the decision.
- **Reject (拒稿)**: Fundamental problems with novelty, scope fit, or
  methodological validity that cannot be fixed through revision. Or: the
  contribution level is significantly below the journal's threshold even
  with revisions.

When recommending Major Revision or Reject, explicitly state what would
need to change for the paper to become acceptable at this venue.

When recommending Reject, if appropriate, suggest a more suitable venue tier
(e.g., "This work may be better suited for a [Q2/Q3] journal in [field]
such as [example only after verifying current identity and scope]").

### Stage F: Venue-fit advisory (投稿层级建议, optional)

If relevant, add a brief assessment of where this paper would best fit:

```
## Venue-fit advisory
- [Top-tier journal, e.g., Nature/Science/Cell]: [assessment]
- [Q1 field leader]: [assessment]
- [Q2–Q3 standard]: [assessment]
- [Q4 entry-level]: [assessment]
```

This is especially useful when the paper's quality does not match the
target journal tier — either too strong or too weak.

---

## Step 5 — Revision guidance

When revision work is already authorized, continue through that scope. Otherwise, after delivering the review, invite selection of issues for further guidance:

"以上评审意见中，哪些问题你需要我提供更详细的修改指导？我可以提供具体的
改写建议、补充分析思路、或修改后的段落示例。"

When the user selects issues for detailed guidance, provide:
- Revised paragraph drafts (in the manuscript's language)
- Specific statistical analysis recommendations
- Suggested additional references (only after verifying bibliographic identity and relevance; do not fabricate references)
- Restructuring suggestions with before/after outlines

---

## Discipline-specific considerations

This skill works across all disciplines. Here are field-specific
adjustments to keep in mind.

When the manuscript involves a specific study type (clinical trial,
systematic review, observational study, animal experiment, etc.),
read `references/reporting-guidelines.md` for the relevant reporting
standard checklist (CONSORT, PRISMA, STROBE, ARRIVE, etc.).

### Natural sciences and engineering
- Emphasize reproducibility: Are methods described in sufficient detail?
- Check statistical reporting against field norms (p-values, effect sizes,
  confidence intervals, correction for multiple comparisons)
- Verify that figures have appropriate error bars, scale bars, labels
- Check data availability and code availability statements

### Biomedical and clinical sciences
- Check for appropriate ethical approvals (IRB, IACUC)
- Verify compliance with reporting guidelines (CONSORT, STROBE, PRISMA,
  ARRIVE, MIAME, STARD, etc.)
- Assess clinical significance, not just statistical significance
- Check trial registration information if applicable

### Social sciences
- Assess validity and reliability of measurement instruments
- Check for appropriate handling of confounders
- Evaluate generalizability claims against sample characteristics
- Verify ethical considerations (informed consent, anonymization)

### Humanities
- Evaluate the coherence and originality of the argument
- Assess engagement with relevant theoretical frameworks
- Check the breadth and depth of primary and secondary source engagement
- Evaluate whether the interpretive claims are well-supported

### Computer science and AI
- Check for proper baselines and ablation studies
- Assess reproducibility (code, data, hyperparameters)
- Evaluate computational cost reporting
- Check for appropriate evaluation metrics and statistical significance tests

---

## Critical rules

1. **Never fabricate references.** If you suggest the author cite additional
   work, verify the identity and relevance of any named paper. Otherwise say "the authors
   should search for recent work on [topic] to strengthen this point."

2. **Never fabricate data or results.** Do not claim the manuscript says
   something it does not say. Always re-check against the actual text before
   finalizing a comment.

3. **Calibrate to the venue, not to an ideal.** A paper for a Q3 journal
   is not held to Nature standards. Use the sample papers as your benchmark.

4. **Be constructive, not adversarial.** The goal is to help the author
   improve the paper and get it published, not to demonstrate reviewer
   superiority.

5. **Separate fact from opinion.** When a comment reflects your professional
   judgment rather than an objective flaw, label it as a suggestion rather
   than a requirement.

6. **Respect the author's research direction.** Do not suggest the authors
   conduct a fundamentally different study. Work within their chosen framework
   and help them execute it better.

---

## Output language

Match the language of your review to the user's request language. If the
user communicates in Chinese, write the review in Chinese. If in English,
write in English. The manuscript itself may be in a different language
from the conversation — that is fine.

Technical terms and journal-specific terminology should remain in their
original language (usually English) even when the review is written in
another language.
