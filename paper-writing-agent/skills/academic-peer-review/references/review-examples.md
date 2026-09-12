# Review quality reference

This file contains curated excerpts from published open peer reviews.
Read this file before generating your review in Step 4.

These examples demonstrate what HIGH-QUALITY review comments look like.
The examples below are drawn from biomedical peer reviews, but the
structural patterns they illustrate — pinpointing, evidencing,
explaining consequences, prescribing fixes, calibrating severity —
apply identically across all disciplines.

---

## What makes a review comment excellent

A good review comment has five qualities. Before writing each comment,
mentally check all five:

1. **Pinpointed**: Names the exact section, figure, paragraph, or data point.
   Not "the methods are unclear" but "the description of the cell sorting
   protocol in Methods paragraph 3 does not specify the gating strategy."

2. **Evidenced**: Cites what the manuscript actually says (or fails to say)
   as the basis for the critique. The reviewer's concern is grounded in
   the text, not in external assumptions.

3. **Consequential**: Explains WHY this matters — how it affects the
   validity, interpretability, or significance of the work.

4. **Actionable**: Tells the author specifically what to do to fix it.
   Not "improve the analysis" but "perform a sensitivity analysis excluding
   outliers beyond 3 SD to test whether the main effect holds."

5. **Proportionate**: The severity of the language matches the severity
   of the issue. A missing p-value correction is not described with the
   same urgency as a fundamentally flawed study design.

---

## Pattern 1: Precise methodological critique

Source: Published peer review, Drosophila genetics, eLife
(https://doi.org/10.7554/eLife.108910.4.sa1)

> More evidence is needed to support the claim of elevated Dpp levels
> in bam or bgcn mutant tumors. The current results with dpp-lacZ
> enhancer trap in Fig 5A,B are not convincing. First, why is the
> dpp-lacZ so much brighter in the mosaic analysis (A) than in the
> no-clone analysis (B); it is expected that the level of dpp-lacZ in
> cap cells should be invariant between ovaries and yet LacZ is very
> faint in Fig. 5B. I think that if the settings in A matched those
> in B, the apparent expression of dpp-lacZ in the tumor would be
> much lower and likely not statistically significant. Second, they
> should use RNA in situ hybridization with a sensitive technique
> like hybridization chain reactions (HCR) — an approach that has
> worked well in numerous Drosophila tissues including the ovary.

### Why this is good:
- Names the exact figures (Fig 5A, 5B) and the specific reporter
  (dpp-lacZ enhancer trap)
- Identifies the precise technical issue: imaging settings differ
  between panels, creating an artificial brightness difference
- Uses an internal control to anchor the argument: cap cell dpp-lacZ
  should be invariant across ovaries, yet it is not
- Explains the consequence: if settings were matched, the claimed
  expression difference would likely lose statistical significance
- Provides a concrete, actionable alternative method (HCR FISH) with
  supporting context (proven in this tissue type)
- Proportionate: says the current evidence is "not convincing" and
  needs stronger support — does not claim the conclusion is wrong

---

## Pattern 2: Identifying an over-interpretation

Source: Published peer review, cell biology / biophysics, eLife
(https://doi.org/10.7554/eLife.106893.1.sa2)

> While the seminal description of tissue properties based on
> interfacial tensions (Brodland 2002) is clearly key to interpreting
> these data, the actual "Differential Interfacial Tension Hypothesis"
> poses that segregation results from global differences, i.e.,
> juxtaposition of two tissues displaying different intrinsic tensions.
> On the contrary, the results of the present work support a different
> scenario, where what counts is the actual difference in tension
> ALONG the tissue boundary, in other words, that segregation is
> driven by high HETEROTYPIC interfacial tension. This is an important
> distinction that should be clarified.

### Why this is good:
- Pinpoints the exact theoretical framework being invoked (Brodland
  2002, Differential Interfacial Tension Hypothesis)
- Identifies the specific mismatch: the classical hypothesis concerns
  global tissue-level tension differences, but the data here supports
  heterotypic interface-specific tension as the driver
- Explains why it matters: these are mechanistically distinct scenarios,
  and conflating them misleads the reader about what the data actually
  demonstrate
- The fix is clear and achievable: clarify the distinction in the text
- Proportionate: acknowledges the framework is "clearly key" while
  requesting conceptual precision — does not dismiss the work

---

## Pattern 3: Constructive suggestion for strengthening a contribution

Source: Published peer review, cell biology / biophysics, eLife
(https://doi.org/10.7554/eLife.106893.1.sa2)

> One may be careful in interpreting the comparison between MCF10a
> and Beas2b cells as used in this study. The conditions may not
> necessarily be representative of the actual properties of breast
> and bronchial epithelia. How much of the epithelial organization
> is reconstituted under these experimental conditions remains to be
> established. This is particularly obvious for bronchial cells,
> which would need quite specific culture conditions to build a
> proper bronchial layer. In this study, they seemed to be on the
> verge of a mesenchymal phenotype (large gaps, huge protrusions,
> cells growing on top of each other, as mentioned in the manuscript).
> As an alternative to Beas2b, comparison of MCF10a with another
> cell line capable of more robust in vitro epithelial organization,
> but ideally with different adhesive and/or tensile properties,
> would be highly interesting, as it may narrow down the parameters
> involved in segregation of oncogenic cells.

### Why this is good:
- Does not reject the existing comparison — treats it as providing
  "preliminary clues" worth building on
- Grounds the concern in the manuscript's own data: large gaps, huge
  protrusions, cells growing on top of each other are all observations
  the authors themselves reported
- Explains why it matters: if Beas2b cells are quasi-mesenchymal under
  these conditions, the comparison may not reflect true epithelial-type
  differences
- The suggestion is constructive and specific: use a cell line with
  more robust epithelial organization but different adhesive/tensile
  properties
- Frames the alternative as "highly interesting" rather than a demand —
  the tone invites rather than commands

---

## Pattern 4: Questioning computational model assumptions

Source: Published peer review, cell biology / biophysics, eLife
(https://doi.org/10.7554/eLife.106893.1.sa1)

> It is unclear what the mechanistic origin of the shape-tension
> coupling is, which is used in the vertex model, and how important
> that coupling is for the presented results. The authors claim that
> the shape-tension coupling is due to the anisotropic distribution
> of stress fibers when cells are under external stress. It is
> unclear why the stress fibers should affect an effective line
> tension on the cell boundaries and why the stress fibers should
> be sensitive to the magnitude of the internal isotropic cell
> pressure. If all the surrounding cells have the same internal
> pressure, then the cell would not be significantly deformed due
> to that pressure, and stress fibers would not form. The authors
> should better justify the use of the shape-tension coupling in
> the model and also present simulation results without that
> coupling. I expect that most of the observed behavior is already
> captured by the differential tension, even if there is no
> shape-tension coupling.

### Why this is good:
- Targets a specific model component (shape-tension coupling) rather
  than vaguely questioning the entire model
- Traces the logical chain: the claimed physical basis (anisotropic
  stress fibers responding to isotropic pressure) contains an internal
  inconsistency — if pressure is isotropic and uniform, cells should
  not deform, so stress fibers should not form
- Clearly separates two questions: (1) is the assumption physically
  justified? and (2) does it actually matter for the results?
- Provides a concrete, testable action: re-run simulations without the
  coupling and compare
- Offers a constructive hypothesis: differential tension alone may be
  sufficient, implying the model could actually become simpler
- Proportionate: frames the issue as needing "better justification,"
  not as invalidating the work

---

## Pattern 5: Requesting statistical robustness and cross-system validation

Source: Published peer review, cell biology / biophysics, eLife
(https://doi.org/10.7554/eLife.106893.1.sa1)

> The observed difference of shape indices between the interfacial
> and bulk cells in simulations in the absence of differential line
> tension is concerning. This suggests that either there are not
> enough statistics from the simulations or that something is wrong
> with the simulations. For all presented simulation results, the
> authors should repeat multiple simulations and then present both
> averages and standard deviations. This way, it would be easier to
> determine whether the observed differences in simulations are
> statistically significant.

Source: Published peer review, Drosophila genetics, eLife
(https://doi.org/10.7554/eLife.108910.4.sa1)

> In Fig 6, the authors report results obtained with the bamBG
> allele. Do they obtain similar data with another bam allele
> (i.e., bamΔ86)?

### Why this is good:
- The first example identifies a specific red flag (unexpected
  differences in a control condition where none should exist) and
  enumerates exactly two possible interpretations (insufficient
  statistics or a simulation error)
- It prescribes the exact fix: multiple independent runs, report
  means and standard deviations — a standard expectation for
  computational work that was not met here
- The second example asks whether a key finding holds when tested
  with a different, molecularly defined reagent — a fundamental
  test of robustness that requires minimal additional effort
- Both comments address the same core question from complementary
  angles: "Is this result robust, or might it be an artifact of
  the specific conditions used?"
- Neither demands new conceptual work — they ask for straightforward
  validation of existing claims

---

## Pattern 6: Assessment summary

An assessment summary evaluates the manuscript as a whole, calibrating
the significance of the findings and the strength of the supporting
evidence. It should give the editor and authors a clear picture of where
the paper stands and what trajectory it is on.

Source: Published peer review, cell biology / biophysics, eLife
(https://doi.org/10.7554/eLife.106893.1.sa2)

> In conclusion, the study conveys an important message, but, as it
> stands, the strength of evidence is incomplete. It would greatly
> benefit from a more detailed and complete analysis of the
> experimental data, a better fit between this analysis and the
> corresponding vertex model, and a more in-depth discussion of
> biological and biophysical aspects. These revisions should be
> rather easily done, and would then make the evidence much more
> solid.

### Why this is good:
- Uses calibrated language for significance ("important message")
  and evidence strength ("incomplete" → "much more solid" after
  revision)
- Separates three specific dimensions for improvement (experimental
  analysis, model–data alignment, discussion depth) rather than a
  vague "needs more work"
- Signals feasibility: "should be rather easily done" tells the
  editor and authors that the gap is bridgeable, not fatal
- Identifies the target trajectory: the study has a clear path from
  its current state to a convincing contribution

When writing a formal eLife-style Assessment, use the journal's
calibrated vocabulary. The two key axes are:

- **Significance of findings** (in ascending order): useful, valuable,
  important, fundamental, landmark
- **Strength of evidence** (in ascending order): inadequate,
  incomplete, solid, convincing, compelling, exceptional

The assessment should also identify the audience who will benefit
from the work. For example:

> **eLife Assessment**: This study presents *important* findings on
> [topic]. The evidence is *solid / convincing / incomplete*, with
> [specific strengths], though [specific gap]. The work will be of
> interest to [target audience].

---

## Anti-patterns: What NOT to do

These are common failure modes. Avoid them.

**Vague critique (no anchor)**:
"The writing could be improved in several places."
→ Fix: Name the places. Quote the unclear sentences.

**Demanding a different study**:
"The authors should have used single-cell RNA-seq instead of bulk RNA-seq."
→ Fix: Work within the author's chosen method. If bulk RNA-seq is
   insufficient for a specific claim, say which claim and why.

**Unsupported assertion**:
"This finding contradicts the well-known Smith et al. (2019) result."
→ Fix: Only cite references you are certain exist. If uncertain, say
   "the authors should verify whether their finding is consistent with
   prior work on [topic]."

**Tone mismatch (excessive severity for minor issues)**:
"The authors' failure to include error bars on Figure 2 fundamentally
undermines the credibility of this work."
→ Fix: Missing error bars is a fixable formatting issue, not a
   credibility crisis. "Figure 2 should include error bars (SD or SEM)
   to allow readers to assess variability."

**Tone mismatch (excessive leniency for major issues)**:
"It might be nice to consider whether the control group is adequate."
→ Fix: If the control is inadequate, say so clearly. "The absence of
   a vehicle-only control in the treatment experiment (Figure 4) means
   the observed effect cannot be attributed to the drug rather than the
   solvent. This control is essential."
