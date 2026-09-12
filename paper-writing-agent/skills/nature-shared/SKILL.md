---
name: nature-shared
description: Internal shared-reference support package for installed Nature Skills, including nature-writing, nature-polishing, nature-response, nature-reader, and ../paper-research-artifacts/SKILL.md. Do not invoke it as a standalone user workflow. Load only the specific core or journal-format file requested by another Nature skill.
---

# Nature Shared References

## Integrated-package execution rules

This is a vendored, adapted branch of `paper-writing-agent`. Read
[the package shared rules](../../references/shared-rules.md) first. User scope,
scientific fidelity, current verified journal requirements and already supplied
answers take precedence over generic examples or historical local defaults.
Task-related files stay in the user's project/output directory. Do not modify
the installed skill while processing a manuscript.

Explicit `../` references resolve from the file containing them. Shorthand
`references/`, `static/`, `templates/` and `scripts/` paths in prose are relative
to this skill's own folder; manifest paths are relative to its manifest.
Load a sibling skill by its actual bundled `../<slug>/SKILL.md`; mentioning a
skill name is not a tool call, automatic role change or permission to delegate.
Use actual host tools and supplied author facts. Never follow historical
installation commands, copy credentials or invoke an external service merely
because an example mentions it.

The generic writing sequence is guidance. A clear local edit proceeds within
its scope. Reuse an approved outline/terms/analysis choice; ask only when a
missing fact changes the scientific premise or an explicitly required approval
remains outstanding. The package Methods/Results outline-confirmation rule
still applies to new full sections. Do not manufacture claims or limitations.
If the requested output is Chinese, keep it Chinese; the `zh-to-en` fragment
applies only when English translation/drafting is requested. For a Chinese
academic style edit use [wordpolish-academic](../wordpolish-academic/SKILL.md).


Use this package only as a dependency of another installed Nature skill.

- Load the exact referenced file; do not preload the whole package.
- Treat `core/` and `journal-formats/` as shared definitions, not standalone workflows.
- Use `journal-formats/nature.md` only for the flagship journal Nature and
  `core/research-compliance.md` only when its specialist applicability gate is
  triggered.
- Use `journal-formats/nature-machine-intelligence.md` for exact NMI article
  types, limits, initial-submission files, data/code duties and production
  requirements; do not import flagship Nature or Nature Communications limits.
- Use `core/main-text-discipline.md` for result placement, main-text compression,
  revision accretion, caption/SI allocation, and claim-repetition checks.
- Use `core/nature-results-discussion.md` for corpus-derived Nature-style
  Results claim escalation, evidence-bound local interpretation, and Discussion
  synthesis; do not present it as official journal policy.
- Use `core/discussion-argument-language.md` for journal-general Discussion
  function sequencing, reverse-funnel control, evidence-calibrated modality,
  claim-specific limitations, and uncertainty-driven future work.
- Use `core/nature-introduction.md` for corpus-derived Nature-style problem
  funnels, exact knowledge gaps, literature tension, question-first novelty,
  and Introduction–Results alignment; do not present it as official journal
  policy.
- Use `core/nature-abstract.md` for corpus-derived Nature-style
  discovery-centred abstract compression, claim hierarchy, selective numeric
  support, and field-level payoff; do not present it as official journal policy.
- Return to the requesting skill for task logic, output format, and final QA.
