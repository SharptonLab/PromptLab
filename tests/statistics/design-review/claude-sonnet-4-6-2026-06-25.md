# Test Results: statistics/design-review.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-25.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** statistics/design-review.md
- **Model:** claude-sonnet-4.6
- **Model ID (pinned):** claude-sonnet-4-6
- **Endpoint:** native
- **Date:** 2026-06-25
- **Tester:** cross-model-harness
- **Assembly strategy:** test-only
- **Temperature:** 0.0

## Test Input Used
Standard test input from prompt file (`## Test Input`).

## Filled Prompt
````
Context: I am planning an experiment to test whether a high-fiber diet alters gut microbiome-immune interactions in a mouse model of autoimmune disease. I want critical feedback before I begin.

Research question: Does dietary fiber supplementation modify gut microbiome composition and reduce autoimmune inflammation in the EAE mouse model?

Experimental design:
- Study system: C57BL/6 mice, 8 weeks old, female, EAE model (MOG-induced)
- Treatment groups:
  1. EAE + standard diet (n=12)
  2. EAE + high-fiber diet (n=12)
  3. No EAE + standard diet (n=6)
  4. No EAE + high-fiber diet (n=6)
- Sample size: Based on previous EAE studies in our lab showing adequate power at n=10
- Controls: Groups 3-4 are healthy controls
- Randomization: Mice assigned to groups at weaning
- Blinding: Clinical scoring will be performed by blinded observer
- Outcome measures: Clinical EAE score (daily), microbiome composition (16S), T cell populations (flow cytometry)
- Timepoints: Fecal samples at days 0, 7, 14, 21; immune analysis at day 21

Potential confounders I've considered:
- Cage effects (2 cages per group)
- Litter effects
- Food consumption differences

Planned analysis: Compare clinical scores with repeated measures ANOVA; compare microbiome with PERMANOVA; correlate microbiome changes with immune parameters.

Task: Review this experimental design critically. Please identify:

1. **Strengths**: What aspects of the design are well-constructed?

2. **Missing controls**: Are there controls that should be added?

3. **Potential confounds**: What factors could produce the expected result without the hypothesized mechanism?

4. **Threats to validity**:
   - Internal validity: Could something other than the treatment explain results?
   - External validity: How generalizable are potential findings?

5. **Statistical concerns**:
   - Is the sample size likely adequate?
   - Does the design match the planned analysis?
   - Are there design features that complicate analysis?

6. **Practical issues**: What could go wrong during execution?

7. **Recommendations**: Prioritized list of suggested improvements

Constraints:
- Be critical—I want to find problems now, not after data collection
- Distinguish between essential fixes and nice-to-haves
- If you need more information to evaluate an aspect, ask
- Don't assume expertise I may not have; explain concerns clearly
````

## Model Output
````
# Critical Review of EAE Fiber Diet Experimental Design

## Preliminary Note

This is a well-thought-out design with several genuine strengths, but there are some significant issues that could undermine your conclusions if not addressed before you begin. I'll be direct about severity throughout.

---

## 1. Strengths

**Genuinely well-constructed elements:**

- **Blinded clinical scoring** is essential for EAE studies, where scoring is subjective and observer bias is a known problem. This is correctly included.

- **Four-group factorial structure** (disease × diet) is the right conceptual framework. It allows you to ask whether fiber has different effects in diseased versus healthy animals, which is more informative than a two-group comparison.

- **Multiple outcome levels** (behavior, microbiome, immune cells) allow you to test the proposed mechanism rather than just the endpoint. If fiber reduces EAE severity but doesn't change the microbiome, that tells you something important.

- **Longitudinal microbiome sampling** (days 0, 7, 14, 21) is better than a single endpoint. Microbiome changes often precede or follow immune changes, and the trajectory matters.

- **Acknowledging cage effects** as a confounder shows methodological awareness that many researchers miss.

- **Using female C57BL/6 mice** is appropriate—this is the standard for MOG-EAE and maximizes comparability with existing literature.

---

## 2. Missing Controls

### Essential Missing Controls

**A. Fiber-type control / fiber composition documentation**

This is arguably the most important missing element. "High-fiber diet" is not a single thing. Dietary fiber encompasses:
- Soluble fermentable fibers (inulin, pectin) — rapidly fermented by gut bacteria, produce short-chain fatty acids (SCFAs), strongly immunomodulatory
- Insoluble fibers (cellulose) — largely non-fermentable, mechanical effects only
- Mixed fibers with different fermentation kinetics

*Why this matters:* If you use a commercially prepared high-fiber diet, you need to document exactly what fiber sources it contains and at what concentrations. Two "high-fiber" diets can have opposite immunological effects. Without this, your result is not reproducible and not interpretable mechanistically.

*What to do:* Specify the fiber source explicitly. Consider whether you need a third dietary group (e.g., soluble vs. insoluble fiber) depending on your mechanistic hypothesis.

**B. Pair-fed or calorie-matched control**

High-fiber diets alter caloric density, palatability, and often total food intake. If mice on the high-fiber diet eat less (or more), you may be studying the effects of caloric restriction or excess rather than fiber per se.

*Why this matters:* Caloric restriction alone is immunomodulatory and can reduce EAE severity. This is a direct alternative explanation for any positive result.

*What to do:* At minimum, measure food intake gravimetrically daily. Ideally, use a diet matched for calories, protein, fat, and micronutrients, differing only in fiber content. Many researchers use a custom diet with added fiber (e.g., adding inulin to standard chow) rather than a commercially formulated "high-fiber" diet, precisely to control this.

**C. Antibiotic-treated group (optional but valuable)**

If your hypothesis is that fiber works *through* the microbiome, a group where the microbiome is depleted (via antibiotics) and then fiber is given would let you test whether the microbiome is necessary for the effect. Without this, you can show correlation between microbiome changes and outcomes, but not that the microbiome change is causally required.

*Severity:* This is a nice-to-have for a first experiment, but essential if you want to publish a mechanistic claim.

**D. SCFA measurement**

If fermentable fiber is your intervention, short-chain fatty acids (butyrate, propionate, acetate) are the primary proposed mediators. Not measuring them is a significant mechanistic gap. Fecal or serum SCFA measurement by GC-MS or LC-MS is feasible and would substantially strengthen causal inference.

---

## 3. Potential Confounds

These are factors that could produce your expected result (fiber reduces EAE, fiber changes microbiome) through mechanisms other than the one you're proposing.

**A. Caloric intake / body weight** *(severity: high)*
Already mentioned above. Mice on high-fiber diets often weigh less. Lower body weight correlates with reduced EAE severity independently of immune mechanisms. You must track body weight daily alongside clinical scores.

**B. Coprophagy** *(severity: high, often overlooked)*
Mice eat their own and cagemates' feces. This means:
- Microbiome "treatment" is partially determined by what feces are available in the cage
- Mice in the same cage will converge in microbiome composition regardless of diet
- This is actually a reason cage effects are severe in microbiome studies (see Section 5)

*What to do:* You cannot eliminate coprophagy in standard housing. You must account for it statistically by treating cage as the unit of analysis, not individual mouse.

**C. Stress from dietary transition** *(severity: moderate)*
If mice are switched to the high-fiber diet at weaning (as implied by your randomization note), this is less of a concern. But if the diet change happens at EAE induction, the stress of dietary change could itself affect immune responses. Clarify your timeline.

**D. Micronutrient differences between diets** *(severity: moderate)*
Commercial high-fiber diets often differ in vitamins (especially vitamin D, which is immunomodulatory) and minerals. Vitamin D deficiency or excess can substantially alter EAE severity. Verify that your diets are matched for micronutrients, or obtain full nutritional composition from the manufacturer.

**E. Gut transit time and drug absorption** *(severity: moderate for EAE specifically)*
EAE is induced with MOG peptide emulsified in Complete Freund's Adjuvant (CFA), plus pertussis toxin. High-fiber diets alter gut transit time, which could affect absorption of pertussis toxin or alter the systemic immune response to CFA. This is a subtle but real concern specific to your model.

**F. Cage microenvironment** *(severity: moderate)*
Bedding, cage position (rack height affects light/temperature), and cage change frequency all affect microbiome composition. These need to be standardized and documented.

---

## 4. Threats to Validity

### Internal Validity

**Threat 1: Cage confounding is likely your biggest internal validity problem**

You have 2 cages per group. With 12 mice per group, that's approximately 6 mice per cage. In microbiome research, mice within a cage share a microbiome environment through coprophagy and environmental exposure. This means your true *n* for microbiome outcomes is closer to 2 (cages) per group, not 12.

This is not a minor statistical nuance—it is a fundamental unit-of-analysis problem. If you analyze microbiome data treating each mouse as independent, your p-values will be dramatically anti-conservative (falsely significant). This has caused numerous retractions in the microbiome field.

*Minimum fix:* Increase to 4-6 cages per group (3-4 mice per cage). This is essential, not optional.

**Threat 2: EAE variability**

EAE is notoriously variable. Even within a single experiment, some mice develop severe disease, some mild, and some fail to develop disease at all ("non-responders"). Non-responders are typically excluded from analysis, but this exclusion is itself a source of bias—if fiber affects disease incidence (not just severity), excluding non-responders will mask this effect.

*What to do:* Pre-specify your exclusion criteria before unblinding. Report incidence (proportion developing disease) as a separate outcome from severity in those that do develop disease.

**Threat 3: Day 21 immune analysis captures only one timepoint**

EAE has distinct phases: induction, peak disease, and remission/chronic phase. Day 21 post-immunization is typically around peak disease in C57BL/6 MOG-EAE, but this varies. If fiber shifts the timing of disease rather than its severity, a single immune timepoint could be misleading.

*Recommendation:* Consider adding an immune analysis timepoint at day 14 (pre-peak) or at a defined disease stage rather than a fixed day.

**Threat 4: Randomization timing**

You state mice are assigned to groups at weaning. EAE is induced at 8 weeks. This means mice are on their respective diets for approximately 4-5 weeks before immunization, which is actually good—it allows the microbiome to stabilize on the new diet. However, you should confirm that your day 0 microbiome sample is taken *after* dietary stabilization but *before* EAE induction, so you have a true baseline for each animal on its assigned diet.

### External Validity

**Limitation 1: Female mice only**

This is standard for EAE and appropriate for internal consistency, but autoimmune diseases often show sex differences in both disease course and microbiome composition. Your findings will not be generalizable to males without additional experiments. This is worth acknowledging explicitly in your eventual write-up.

**Limitation 2: Single mouse strain**

C57BL/6 mice have a specific genetic background that influences both EAE susceptibility and microbiome composition. Results may not replicate in other strains.

**Limitation 3: EAE-to-MS translation**

EAE is a model of MS, but it is an imperfect one. MOG-EAE in C57BL/6 mice models a specific aspect of MS pathology (CD4+ T cell-mediated demyelination). The microbiome-immune interactions you observe may not translate to human MS, where disease is more heterogeneous and the microbiome is far more diverse.

**Limitation 4: Specific pathogen-free (SPF) housing**

I assume your mice are SPF. SPF mice have a dramatically different and less diverse microbiome than conventionally housed mice or humans. Fiber effects on microbiome composition may be substantially different in a more complex microbial community. This is a fundamental limitation of all mouse microbiome work.

---

## 5. Statistical Concerns

### Sample Size

**The stated justification is insufficient.**

"Previous EAE studies in our lab showing adequate power at n=10" tells us nothing about power for your specific outcomes. Power depends on:
- The effect size you expect
- The variability of the outcome
- The specific statistical test

For **clinical EAE scores**: n=12 per group may be adequate if your lab has established effect sizes for dietary interventions. However, EAE scores are ordinal (0-5 scale), not continuous, which affects the appropriate test (see below).

For **microbiome outcomes**: As discussed above, your effective n for microbiome analysis is the number of cages, not mice. With 2 cages per group, you are severely underpowered for microbiome comparisons. PERMANOVA with n=2 per group is essentially meaningless.

For **flow cytometry**: Power depends heavily on which T cell populations you're measuring and expected effect sizes. This needs a formal power calculation.

**Recommendation:** Conduct formal power calculations for each primary outcome. For microbiome outcomes specifically, increase cage number before worrying about mouse number.

### Analysis-Design Mismatch

**Issue 1: EAE scores are ordinal, not continuous**

EAE clinical scores (0, 1, 2, 3, 4, 5) are ordered categories, not continuous measurements. Repeated measures ANOVA assumes continuous, normally distributed data. Applying it to ordinal scores is technically incorrect and can produce misleading results.

*Better approach:* Mixed-effects ordinal regression, or at minimum a non-parametric alternative (Friedman test for repeated measures). Many EAE papers use ANOVA anyway and reviewers often accept it, but you should be aware of this limitation and consider whether your scores will be sufficiently variable to approximate continuous data.

**Issue 2: Cage as unit of analysis for microbiome**

Your PERMANOVA should include cage as a factor or should be run at the cage level (averaging within cages) rather than treating individual mice as independent. Failure to do this will produce false positives.

**Issue 3: Multiple comparisons**

You have four groups, three outcome domains, multiple timepoints, and planned correlations. The number of statistical tests you will run is large. You need a pre-specified analysis plan that addresses multiple comparisons—either through correction (Bonferroni, FDR) or by clearly distinguishing primary from exploratory analyses.

**Issue 4: Correlation analysis**

Correlating microbiome changes with immune parameters is exploratory and hypothesis-generating, not confirmatory. With the sample sizes involved and the high dimensionality of microbiome data (potentially hundreds of OTUs/ASVs), spurious correlations are nearly guaranteed without appropriate correction. Plan to use FDR correction and treat these correlations as preliminary.

**Issue 5: Repeated measures structure**

Your microbiome data has a repeated measures structure (same mouse at days 0, 7, 14, 21) nested within cages. PERMANOVA as typically implemented does not handle this nested structure well. You may need to use a mixed-effects distance-based approach or analyze each timepoint separately with appropriate correction.

---

## 6. Practical Issues

**A. EAE induction variability between batches**

If you cannot immunize all mice on the same day (which is logistically difficult with 36 mice), mice immunized on different days will have disease courses offset in time. This creates a confound if you're comparing absolute day numbers. *Solution:* Score relative to disease onset, not absolute day post-immunization, or immunize all mice within a 48-hour window.

**B. Fecal sample collection**

Collecting fecal samples from individual mice at multiple timepoints requires either individual housing (which itself dramatically alters microbiome and stress hormones) or careful individual identification during collection. Group-housed mice produce feces collectively, making individual attribution difficult.

*This is a significant practical problem.* Options:
- Briefly individually house mice for 1-2 hours for sample collection (stressful but time-limited)
- Use metabolic cages for collection periods
- Accept that fecal samples represent cage-level microbiome rather than individual-level

This decision affects your entire analysis plan and should be made before you begin.

**C. Antibiotic contamination of water**

Some facilities add antibiotics to water for routine health maintenance. Verify that your facility does not do this, as it would confound your microbiome results entirely.

**D. Diet storage and freshness**

High-fiber diets, especially those containing fermentable fibers, can degrade or develop mold. Establish a diet storage and replacement protocol. Stale or contaminated diet is a common source of unexplained variability.

**E. Blinding scope**

You mention blinding for clinical scoring, which is good. But are the people performing flow cytometry and microbiome analysis also blinded to group assignment? If not, there is potential for bias in sample processing, gating decisions, and data analysis. Extend blinding to all outcome measurements.

**F. Humane endpoints and mortality**

EAE can cause severe disease requiring euthanasia. Mice that die or are euthanized before day 21 will be missing from your immune analysis. Pre-specify how you will handle this in your analysis (intent-to-treat vs. per-protocol) and whether early death is itself an outcome.

---

## 7. Prioritized Recommendations

### Tier 1: Essential — Fix Before Starting

| Priority | Issue | Action |
|----------|-------|--------|
| 1 | Cage number | Increase to minimum 4 cages per group (3 mice/cage). Your current design is underpowered for microbiome analysis and has a unit-of-analysis problem. |
| 2 | Diet characterization | Obtain full nutritional composition of both diets. Verify caloric density, macronutrient ratios, micronutrients (especially vitamin D), and fiber type/source. |
| 3 | Food intake monitoring | Weigh food daily per cage. Without this, you cannot rule out caloric restriction as the mechanism. |
| 4 | Fecal sampling protocol | Decide now whether samples are individual or cage-level, and design your collection protocol accordingly. This affects your entire analysis plan. |
| 5 | Blinding extension | Blind all personnel performing assays (flow cytometry, microbiome processing) to group assignment, not just clinical scorers. |
| 6 | Pre-specify exclusion criteria | Define non-responder criteria and analysis approach before unblinding. |

### Tier 2: Important — Strong Recommendation

| Priority | Issue | Action |
|----------|-------|--------|
| 7 | SCFA measurement | Add fecal or serum SCFA measurement. This is the most plausible mechanistic link and is relatively low-cost. |
| 8 | Formal power calculation | Run power calculations for each primary outcome with realistic effect sizes and variability estimates. |
| 9 | Statistical analysis plan | Pre-register or at minimum write down your complete analysis plan before data collection,
````

## Assessment
_To be completed by a human reviewer. Do not mark Pass without reading the output._

### Task Achievement
- **Achieved:** [Yes / No / Partial]
- **Notes:**

### Constraint Compliance
- **All constraints respected:** [Yes / No]
- **Violations noted:**

### Failure Modes
- **Failure modes observed:** [None / list]
- **Mitigation effectiveness:**

### Output Format
- **Format correct:** [Yes / No]
- **Deviations:**

## Overall Assessment
- **Recommendation:** PENDING AUTHOR REVIEW
- **Notes:**

## Verification Steps Tested
_Which verification requirements from the prompt were checked, and results._
