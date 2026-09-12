# Reporting guidelines quick reference

This is a non-exhaustive historical teaching summary, not the complete current official standard. Match the actual study design and verify the applicable official version before treating an item as required. Reporting completeness and methodological necessity are different.

When reviewing a manuscript, check whether the study type matches any of
the reporting guidelines below. If it does, verify that the key requirements
are met. This is NOT an exhaustive list — it covers the most commonly
applicable guidelines across disciplines.

Read this file only when needed: if the manuscript involves a clinical trial,
systematic review, observational study, animal experiment, or other study
type listed below, consult the relevant section.

---

## Clinical trials — CONSORT

Applies to: Randomized controlled trials (RCTs)
Checklist: https://www.consort-statement.org/checklist

Key items to check:
- Trial registration number and registry name
- Clear description of randomization method (sequence generation,
  allocation concealment)
- Blinding: who was blinded (participants, care providers, outcome assessors)
- Primary and secondary outcomes pre-specified
- Sample size calculation with assumptions stated
- Flow diagram (enrollment, allocation, follow-up, analysis)
- Intention-to-treat analysis or per-protocol with justification
- Adverse events reported

---

## Systematic reviews and meta-analyses — PRISMA

Applies to: Systematic reviews, scoping reviews, meta-analyses
Checklist: https://www.prisma-statement.org/checklist

Key items to check:
- Report protocol/registration and deviations when applicable; do not assume every review type is eligible for PROSPERO.
- Explicit eligibility criteria (PICOS: population, intervention,
  comparator, outcomes, study design)
- Report searched sources, dates and full strategies reproducibly. Judge database coverage against the review question; a universal two-database minimum is not assumed.
- Study selection process described (screening, eligibility, inclusion)
- PRISMA flow diagram with numbers at each stage
- Risk of bias assessment for included studies
- Data synthesis method described (narrative, quantitative, or both)
- If meta-analysis: heterogeneity assessment (I², Q test),
  sensitivity analyses, publication bias assessment

---

## Observational studies — STROBE

Applies to: Cohort, case-control, and cross-sectional studies
Checklist: https://www.strobe-statement.org/checklists

Key items to check:
- Study design identified in title or abstract
- Setting (locations, dates, periods of recruitment/follow-up)
- Participants: eligibility criteria, sources, methods of selection
- Variables: outcomes, exposures, confounders clearly defined
- Statistical methods including handling of confounders
- Descriptive data: characteristics of participants, missing data
- Main results with confidence intervals and measures of precision

---

## Animal studies — ARRIVE 2.0

Applies to: All in vivo animal experiments
Checklist: https://arriveguidelines.org/arrive-guidelines

Key items to check:
- Study design: experimental groups, controls, experimental unit
- Sample size: calculation method, rationale for number of animals
- Randomization: method of allocating animals to groups
- Blinding: whether investigators were blinded during allocation,
  conduct, and assessment
- Outcome measures: primary and secondary, clearly defined
- Statistical methods: including method for assessing assumptions
- Ethical statement: approval body, protocol number, compliance
  with regulations
- Species, strain, sex, age/weight, housing, husbandry conditions

---

## Diagnostic accuracy studies — STARD

Applies to: Studies evaluating diagnostic tests or biomarkers
Checklist: https://www.equator-network.org/reporting-guidelines/stard

Key items to check:
- Reference standard clearly defined and justified
- Participant selection: consecutive or random series
- Blinding between index test and reference standard
- Indeterminate results reported and handled
- 2×2 table or sensitivity/specificity with confidence intervals
- Flow diagram showing participant flow

---

## Qualitative research — SRQR / COREQ

Applies to: Qualitative studies (interviews, focus groups, ethnography)
SRQR checklist: https://www.equator-network.org/reporting-guidelines/srqr
COREQ checklist: https://www.equator-network.org/reporting-guidelines/coreq

Key items to check:
- Research paradigm and theoretical framework stated
- Researcher characteristics and reflexivity
- Sampling strategy and participant selection rationale
- Data collection methods described in detail
- Data analysis approach (thematic, grounded theory, etc.)
- Strategies to enhance trustworthiness (member checking,
  triangulation, audit trail)
- Ethics approval and informed consent

---

## Computational and AI/ML studies

No single universal guideline, but check for:
- Dataset description: source, size, preprocessing, train/val/test split
- Baseline comparisons: appropriate and recent baselines included
- Ablation studies for key components
- Evaluation metrics: standard for the task, with significance tests
  or confidence intervals
- Reproducibility: code availability, random seed reporting,
  hyperparameter specification
- Computational cost reporting (training time, hardware)
- For clinical AI, select the guideline for the actual design (prediction, diagnostic accuracy, trial protocol or completed trial) and verify its current AI extension; the standards are not interchangeable.

---

## Microarray / high-throughput genomics — MIAME

Applies to: MIAME specifically addresses microarrays. For sequencing studies, check the appropriate sequencing reporting/data-submission standard and repository requirements.
Standard: https://www.fged.org/projects/miame

Key items to check:
- Raw data deposited in public repository (GEO, ArrayExpress)
- Accession number provided
- Experimental design: sample descriptions, conditions
- Normalization and data processing methods
- Multiple testing correction for differential expression

---

## Case reports — CARE

Applies to: Clinical case reports
Checklist: https://www.care-statement.org/checklist

Key items to check:
- Patient information: demographics, relevant history
- Clinical findings, timeline, diagnostic assessment
- Therapeutic intervention and follow-up
- Informed consent for publication
- Discussion of rationale for conclusions

---

## How to use this in your review

When you identify the study type, mentally walk through the relevant
checklist above. You do NOT need to check every single item — focus on
the items that are:

1. **Missing entirely** — judge severity by the actual impact on reproducibility or validity
2. **Present but inadequate** — provide a specific improvement and classify severity by actual impact
3. **Not applicable** — skip silently; do not comment on items that
   genuinely do not apply

Do NOT demand compliance with a guideline that does not match the study
type (e.g., do not ask for CONSORT compliance from an observational study).

When flagging a reporting gap, name the guideline and item:
"Per ARRIVE 2.0 item 2, the sample size calculation (or rationale for
the number of animals used) should be reported."
