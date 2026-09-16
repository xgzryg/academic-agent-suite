---
name: polish-academic-manuscript
description: Polish a complete English academic or SCI manuscript supplied as Markdown (.md) or Word (.docx), processing it sequentially in small chunks and recombining all polished sections into one final document. Use when a user asks to 润色论文、SCI论文润色、学术英语润色、全文润色, or to edit, proofread, refine, or journal-align a research/review manuscript while preserving meaning, structure, data, citations, and author voice. Supports any discipline and optional target field, journal, article type, and English variant.
metadata:
  author: 迪娜学姐
  微信公众号: 迪娜学姐
---

# Polish Academic Manuscript

Read [shared rules](../../references/shared-rules.md) before this branch. Resolve all paths from this skill directory, never the shell working directory. Use [paper-documents](../paper-documents/SKILL.md) for Word and [paper-pdf](../paper-pdf/SKILL.md) for PDF; these are bundled dependencies. Source attribution is retained in metadata, not inserted as the author of new user deliverables.

When Methods or Supplementary Methods are within scope, read [Methods directness and cross-section redundancy](../../references/methods-directness-and-redundancy.md) before editing those chunks. Preserve load-bearing method facts, keep interpretation in its necessary Discussion location, and remove only redundant explanation after checking the relevant cross-section context.

Polish the entire manuscript from beginning to end while preserving scientific meaning and document structure. Work chunk by chunk, maintain a manuscript-wide style sheet, and deliver one recombined document in the input format.

Apply the shared rules' figure-order and Discussion convention to all steps
below and the editorial standard. Within authorized Discussion editing, replace
own-study main/SI figure/table callouts with self-contained prose, including
their links or cross-reference fields; preserve literature citations, necessary
numbers and scientific meaning. Do not insert figures, tables or legends into
Discussion. This is an explicit exception to generic cross-reference preservation,
not permission to renumber displays, move/delete existing display objects or
restructure outside scope. Check Results first-introduction order and thematic
continuity; report any repair requiring broader authorization. Read-only and
translation-only tasks report the issue outside the unchanged source/faithful
translation. Local edits remain local.

## Apply the editorial standard

Read [references/editorial-standard.md](references/editorial-standard.md) before editing. Apply it to every chunk and to the final manuscript-wide quality check.

Do not promise acceptance or imply that language editing can guarantee publication.

## Establish the job

1. Locate the submitted `.md` or `.docx` manuscript and preserve the source unchanged.
2. For `.docx`, also invoke the bundled [paper-documents skill](../paper-documents/SKILL.md) and follow its complete instructions for extraction, editing, formatting preservation, rendering, and verification.
3. Infer the field, target journal, article type, English variant, and output location from the request and manuscript. Ask only when a missing value would materially change the edit:
   - Treat the target journal as optional. If absent, use broadly accepted international academic English.
   - Infer the discipline from the title, abstract, keywords, terminology, and methods.
   - Infer the article type from the section structure; default to research article when still unclear.
   - Preserve the manuscript's dominant US or UK spelling; if inconsistent, choose the target journal's variant when known, otherwise use the dominant variant.
4. Do not require a separate confirmation turn before beginning. If a target journal is named but its current style is not locally available, either use official current author guidelines when journal-specific alignment is important or explicitly apply general scholarly conventions. Do not guess journal requirements.
5. Create a task-local working directory. Keep at least:
   - a source snapshot or extracted working copy;
   - a section/chunk manifest with stable IDs and source order;
   - a live style sheet for terminology, abbreviations, spelling, capitalization, tense, symbols, units, and citation conventions;
   - one polished fragment per chunk;
   - a final QA record.

If the task is interrupted, resume from the first unfinished chunk after verifying the manifest and the last completed fragment. Do not restart or repolish completed chunks unless QA reveals a consistency problem.

## Map before editing

Read the whole manuscript once for orientation before changing prose. Build a section map that includes front matter, all heading levels, body sections, captions, tables, equations or code blocks, declarations, and references.

Record the central research question, contribution, study design, principal findings, and conclusion in the private working notes. Use this only to preserve coherence; never add claims not present in the manuscript.

Use this default order, while respecting the manuscript's actual structure:

1. Title, abstract, and keywords
2. Introduction
3. Materials and methods / methodology
4. Results
5. Discussion
6. Conclusion
7. Supplementary prose, figure captions, table text, acknowledgments, declarations, and other end matter
8. References, checked for internal consistency but not substantively rewritten

Never rearrange major sections unless the user explicitly requests structural editing.

## Build sequential chunks

Process exactly one chunk at a time and commit its polished fragment before moving to the next.

Apply both limits to every prose chunk:

- Include no more than 2–3 source paragraphs.
- Include no more than 1,000 English words.

Use the stricter limit. Prefer natural paragraph and subsection boundaries. Keep the title, abstract, and keywords together only when their combined length is at most 1,000 words; otherwise split the abstract at paragraph boundaries after the title.

Handle exceptions without omitting text:

- Put a single source paragraph longer than 1,000 words in its own chunk and edit it in sequential sentence groups of at most 1,000 words, then rejoin the paragraph.
- Keep a short heading with its first paragraph when practical.
- Treat each table, caption group, displayed equation context, or list as an atomic unit when splitting it would damage meaning. If an atomic unit exceeds the limit, process its cells/items sequentially while preserving its structure.
- Do not split a citation token, equation, cross-reference, tracked field, or Markdown code block.

Maintain stable chunk IDs and record source boundaries so every source element appears exactly once in the final assembly.

## Polish each chunk

For every chunk:

1. Read the immediately preceding polished chunk and the next source chunk for local continuity.
2. Preserve the claims, degree of certainty, logical relationships, numbers, units, equations, sample sizes, statistical notation, literature citations and authorial intent. Preserve cross-references except own-study display callouts in authorized Discussion edits, as specified above.
3. Correct grammar, syntax, spelling, punctuation, articles, agreement, modifiers, parallelism, and sentence boundaries.
4. Improve clarity, logical flow, precision, concision, formality, and readability. Retain accurate original wording wherever it is already effective.
5. Resolve unnecessary repetition and awkward transitions within the chunk without deleting substantive content.
6. Apply discipline-appropriate terminology conservatively. Do not replace an established technical term merely for variety.
7. Keep terminology, abbreviations, capitalization, tense, voice, symbols, hyphenation, and spelling consistent with the live style sheet. Update the style sheet only after resolving a genuine inconsistency.
8. Preserve all formatting and structural markers required for lossless reassembly.
9. Save only the refined manuscript fragment in the polished-fragment file. Keep reasoning and diagnostics out of the manuscript.

Do not stop for approval after each chunk unless the user explicitly requests staged review. Progress updates may report sections completed, but must not replace the final combined deliverable.

## Respect evidence boundaries

- Never fabricate citations, references, data, methods, results, definitions, or journal rules.
- Never silently change a scientific fact, numerical value, statistical result, equation, citation key, figure/table number, or conclusion strength.
- Preserve hedging and causal versus correlational language unless the source clearly supports a correction.
- Do not perform substantive fact-checking merely because the task is language polishing. If a possible scientific inconsistency is visible, preserve the source claim and report the concern separately and concisely after delivery; do not insert editorial commentary into the polished manuscript.
- Preserve existing citations exactly unless correcting an obvious formatting inconsistency with a known required style.
- Do not add `[citation needed]` or new references unless the user explicitly authorizes citation editing.
- Leave bibliography wording and metadata unchanged except for safe, requested style normalization. Never infer missing bibliographic fields.

## Reassemble the manuscript

After all chunks are polished:

1. Recombine fragments strictly by the manifest's source order.
2. Preserve heading hierarchy, paragraph order, lists, tables, equations, captions, footnotes/endnotes, hyperlinks, citation fields, cross-references, page elements, and reference order, except the authorized Discussion display-callout edits specified above. Do not restore removed display links or fields during reassembly; literature citation fields remain protected.
3. Use the original file format:
   - For Markdown, produce `<source-stem>_polished.md` with valid Markdown and preserved non-prose blocks.
   - For Word, produce a clean `<source-stem>_polished.docx`, preserve usable styling and document objects, and follow the bundled [paper-documents skill](../paper-documents/SKILL.md)'s render-and-verify workflow. Add tracked changes or comments only when the user explicitly requests them.
4. Never overwrite the source unless the user explicitly requests it.

## Run final QA

Compare the assembled document with the source, then verify:

- every mapped source element appears once and in order;
- no paragraph or sentence was accidentally dropped, duplicated, or truncated;
- all numbers, units, symbols, equations, citation tokens, figure/table identifiers, and cross-references match the source unless an explicitly authorized change was made;
- terminology, abbreviations, spelling variant, capitalization, tense, and formatting are manuscript-wide consistent;
- the abstract agrees with the reported methods, results, and conclusion;
- headings and transitions are coherent without unauthorized restructuring;
- Markdown parses cleanly, or every page of the Word document renders without clipping, overlap, missing glyphs, or broken objects.

If a QA check fails, repair the assembled document and rerun the relevant checks before delivery.

## Deliver

Return the path or link to the single polished manuscript. The manuscript itself must contain only refined manuscript content, not explanations, change logs, editing notes, or invented metadata.

In the handoff message, state the output format and that the source was preserved. Mention separate scientific or citation concerns only when material; keep them outside the document. Do not paste the entire manuscript into chat when a file has been created unless the user asks.
