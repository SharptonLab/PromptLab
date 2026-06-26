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

This is a well-conceived experiment addressing an important question, but there are several issues ranging from potentially fatal flaws to minor refinements. I'll be direct about severity. I also have questions at the end that would change some of my assessments.

---

## 1. Strengths

**Genuinely well-constructed elements:**

- **Blinded clinical scoring** is appropriate and important, since EAE scoring is subjective and the observer knowing treatment group would introduce bias
- **Factorial design logic** (EAE × diet) is correct—you need all four combinations to distinguish diet effects from disease effects and detect interactions
- **Multiple outcome measures** that span the proposed mechanism (microbiome → immune → clinical) allow you to test the causal chain, not just the endpoints
- **Repeated microbiome sampling** (days 0, 7, 14, 21) is good; a single timepoint would miss the dynamics of how the microbiome changes relative to disease onset
- **Female C57BL/6 with MOG-EAE** is the field-standard model, which aids comparability with existing literature
- **Identifying cage effects as a confounder** shows methodological awareness—many researchers miss this

---

## 2. Missing Controls

### Essential Missing Controls

**A. Fiber-type control / dietary composition control**

This is the most important missing control. High-fiber diets differ from standard diets in multiple ways simultaneously: fiber content, caloric density, macronutrient ratios, micronutrient content, and palatability. If you observe an effect, you cannot attribute it to fiber specifically.

*What you need:* Either (a) a diet matched in all respects except fiber content, obtained from the same manufacturer, or (b) a purified diet with a specific fiber source (e.g., inulin, pectin, cellulose) added at a defined dose. Using cellulose as a "non-fermentable fiber" control versus fermentable fiber (e.g., inulin) would also let you test whether fermentation specifically—and thus microbiome activity—is the mechanism.

**B. Antibiotic depletion or germ-free control**

Your hypothesis is that fiber works *through* the microbiome. Without a condition that removes the microbiome, you cannot establish that the microbiome is the mediating mechanism rather than a correlate. If fiber reduces EAE severity in germ-free mice or antibiotic-treated mice, the effect is microbiome-independent.

*What you need:* Ideally, an antibiotic-cocktail group (EAE + high-fiber + antibiotics) to test whether the microbiome is required for the fiber effect. This is a mechanistic control, not just a nice-to-have if your claim is about the microbiome-immune axis specifically.

*Caveat:* Antibiotics themselves affect immune function, so this control has its own interpretive complications. Germ-free mice are the cleaner test but require specialized facilities.

**C. Baseline microbiome characterization**

You have a day 0 timepoint, which is good, but it's unclear when day 0 is relative to diet initiation and EAE induction. See the timeline concern in Section 6.

### Nice-to-Have Controls

- **Fiber dose-response groups**: Testing one dose tells you whether fiber has an effect but not the dose-response relationship, which matters for translation and for confirming specificity
- **Male mice**: EAE has sex-dependent features; female-only results limit generalizability (discussed further in external validity)

---

## 3. Potential Confounds

These are factors that could produce your expected result without the fiber → microbiome → immune mechanism you hypothesize.

**A. Caloric intake and body weight differences**

High-fiber diets are often less calorically dense and may be less palatable. If mice on the high-fiber diet eat less, they may be calorically restricted. Caloric restriction independently suppresses inflammation and can reduce EAE severity. This is a major alternative explanation.

*You listed food consumption as a confounder you've considered—but have you planned to measure it?* You need daily or weekly food weight measurements and body weights throughout the experiment. Without this data, a significant result is uninterpretable.

**B. Cage microbiome effects (partially identified)**

You noted cage effects, but two cages per group is insufficient to separate cage effects from treatment effects (see Statistical Concerns). Mice in the same cage share a microbiome through coprophagy (eating each other's feces), which means cage-mates are not independent observations for microbiome outcomes. This is not just a statistical nuisance—it means your microbiome data has a fundamentally different unit of analysis (cage) than your clinical data (individual mouse).

**C. Stress from dietary change**

If mice are switched to the high-fiber diet at weaning (as implied by your randomization note), this is less of a concern. But if the diet change occurs at or near EAE induction, the stress of dietary change could itself affect immune function and EAE severity independently of fiber content.

**D. Differential EAE induction efficacy**

MOG-EAE induction involves an adjuvant (CFA) and pertussis toxin. If the person performing inductions is not blinded to group, or if inductions are performed in batches that correlate with groups, systematic differences in disease induction could confound results. Is the person performing EAE induction blinded?

**E. Microbiome drift over time**

Even within the same diet group, microbiomes change over the course of an experiment due to aging, disease progression, and facility-level environmental changes. Your day 21 microbiome may differ from day 0 for reasons unrelated to diet.

---

## 4. Threats to Validity

### Internal Validity

**Threat 1: Cage confounding is likely to be severe**

With 2 cages per group and approximately 6 mice per cage (12 mice / 2 cages), your effective sample size for microbiome outcomes may be n=2 per group, not n=12. PERMANOVA on microbiome data will show significant differences between groups partly because cage-mates cluster together, and you have no way to separate cage effects from diet effects with only 2 cages per group.

*This is potentially a fatal flaw for the microbiome analysis specifically.*

**Threat 2: Pseudoreplication in microbiome analysis**

Related to the above: if you analyze individual mice as independent units for microbiome composition when they share a cage, you are pseudoreplicating. This inflates your effective sample size and your statistical power, making it easier to find significant differences that may not be real.

**Threat 3: Timeline ambiguity**

When does the diet start relative to EAE induction? The microbiome takes time to shift in response to dietary change—typically 1-2 weeks for substantial changes in composition. If the diet starts at the same time as EAE induction, the microbiome may not have shifted meaningfully by the time disease onset occurs (typically day 10-14 post-induction). This would mean you're testing whether fiber affects an already-established disease trajectory rather than whether fiber-induced microbiome changes prevent disease development.

**Threat 4: Day 21 immune analysis is a single snapshot**

EAE has distinct phases (induction, peak, recovery). Day 21 may be peak disease in some mice and recovery in others, depending on individual variation. Comparing T cell populations at a fixed timepoint when mice are at different disease stages conflates disease stage effects with treatment effects.

*Better approach:* Analyze immune parameters at a defined disease stage (e.g., at peak score) rather than a fixed timepoint, or add an additional timepoint.

**Threat 5: Partial blinding**

You mention blinding for clinical scoring, which is good. But are the people performing flow cytometry, 16S sequencing analysis, and statistical analysis blinded? Unblinded analysis of flow cytometry data (gating decisions) and microbiome data (choice of diversity metrics, filtering thresholds) can introduce bias.

### External Validity

**Threat 1: Female-only design**

EAE severity, immune responses, and microbiome composition differ between sexes. Results in female mice may not generalize to males, and certainly not directly to human MS, which affects both sexes. This is a known limitation of the field, but worth stating explicitly in your eventual paper.

**Threat 2: Single mouse strain and EAE model**

C57BL/6 MOG-EAE produces a chronic progressive disease. Other EAE models (SJL/J with PLP, relapsing-remitting) have different immunological profiles. Findings may be model-specific.

**Threat 3: Facility-specific microbiome**

Mouse gut microbiomes vary dramatically between facilities, even within the same strain. Your results may not replicate in another institution's mice. This is a general problem in microbiome research, not specific to your design, but it means your findings should be interpreted as "in mice with this facility's baseline microbiome."

**Threat 4: Translation to human MS**

EAE models human MS imperfectly. The fiber doses achievable in mice (as a proportion of diet) differ from human dietary interventions. This doesn't invalidate the experiment but should frame your claims appropriately.

---

## 5. Statistical Concerns

### Sample Size

**The n=10 justification is insufficient as stated.**

A power calculation based on "previous EAE studies showing adequate power at n=10" for clinical scores does not necessarily apply here because:

1. Your primary question may be about microbiome changes, for which EAE clinical score power calculations are irrelevant
2. If cage is the unit of analysis for microbiome data, your effective n is 2 per group—almost certainly underpowered
3. You have multiple primary outcomes (clinical score, microbiome, T cells), which requires correction for multiple comparisons or pre-specification of a single primary outcome

*What I'd want to see:* A formal power calculation for each primary outcome, with the unit of analysis correctly specified. For microbiome PERMANOVA with cage as the unit, you would need substantially more cages.

### Design-Analysis Mismatch

**Issue 1: Repeated measures ANOVA for EAE scores**

EAE clinical scores are ordinal (0-5 scale), not continuous. Repeated measures ANOVA assumes continuous, normally distributed outcomes. The appropriate analysis is either a non-parametric repeated measures test or a mixed-effects ordinal regression model. This is a common error in EAE papers but it's still an error.

Additionally, EAE scores often have many zeros early in the experiment and are right-skewed. Standard ANOVA will perform poorly.

**Issue 2: PERMANOVA and cage effects**

PERMANOVA can account for cage as a blocking factor, but only if you have enough cages to estimate the cage effect. With 2 cages per group, you cannot reliably partition variance between cage and treatment.

**Issue 3: Correlation of microbiome with immune parameters**

Correlating microbiome composition (a high-dimensional dataset with hundreds of OTUs/ASVs) with immune parameters requires careful multiple testing correction. Simple Pearson/Spearman correlations across all taxa will produce many false positives. Methods like MaAsLin2 or sparse CCA are more appropriate.

**Issue 4: Multiple comparisons across groups**

With four groups, pairwise comparisons generate six tests. Your analysis plan should specify which comparisons are primary (presumably EAE+standard vs. EAE+high-fiber) and which are secondary, and how you'll control the family-wise error rate.

### Missing from Analysis Plan

- How will you handle mice that don't develop EAE (non-responders)? This is common and affects your group sizes
- How will you handle missing data from mice that die or are removed?
- What alpha level and what correction method for multiple comparisons?

---

## 6. Practical Issues

**A. EAE non-responders**

Typically 10-30% of mice fail to develop EAE even with standard induction protocols. With n=12 per EAE group, you may end up with 8-10 mice with disease. Will non-responders be excluded? Included? This decision should be pre-specified, as post-hoc exclusion is a form of bias.

**B. Diet timeline is unspecified**

When does the high-fiber diet start? Options include:
- At weaning (before the experiment begins)
- At the start of the experiment (before EAE induction)
- At EAE induction

Each tests a different question. Starting at weaning tests whether a lifetime high-fiber diet prevents EAE. Starting 2 weeks before induction tests whether fiber-induced microbiome changes affect susceptibility. Starting at induction tests whether fiber affects disease progression. You need to decide which question you're asking and design the timeline accordingly.

**C. Coprophagy and cage microbiome homogenization**

Mice eat each other's feces, which rapidly homogenizes the microbiome within a cage. This means individual mice within a cage are not independent for microbiome purposes. This is unavoidable in standard housing but must be accounted for analytically.

**D. Fiber diet palatability and food intake**

High-fiber diets are often less palatable. If mice eat less, they lose weight, which affects EAE severity and immune function independently. You must measure food intake and body weight. Consider pair-feeding the control group if intake differs substantially.

**E. Batch effects in 16S sequencing**

If fecal samples from different timepoints are sequenced in different batches, batch effects can create artifactual differences. All samples should ideally be sequenced together, or batch should be included as a covariate.

**F. Sample storage**

Fecal samples for 16S must be frozen immediately at -80°C. Delays or freeze-thaw cycles alter microbiome composition. Your sample collection protocol needs to be standardized.

**G. Flow cytometry panel not specified**

"T cell populations" is vague. Which populations? Th1, Th17, Treg, CD8? The choice matters for your hypothesis (fiber → SCFAs → Treg induction is a common proposed mechanism). Your panel should be designed around the mechanistic hypothesis.

---

## 7. Prioritized Recommendations

### Tier 1: Essential Fixes (Address Before Starting)

| Priority | Issue | Recommendation |
|----------|-------|----------------|
| 1 | Dietary control | Use a matched control diet from the same manufacturer, differing only in fiber content and type |
| 2 | Cage replication | Increase to 4-6 cages per group (3-4 mice per cage) rather than 2 cages of 6 |
| 3 | Specify and measure food intake | Weigh food daily or every other day; measure body weight weekly |
| 4 | Define timeline explicitly | Specify when diet starts relative to EAE induction; start diet at least 2 weeks before induction |
| 5 | Pre-specify primary outcome | Designate one primary outcome for power calculation and primary analysis |
| 6 | Specify flow cytometry panel | Define which T cell populations based on your mechanistic hypothesis |
| 7 | Blinding scope | Extend blinding to flow cytometry analysis and microbiome data analysis |

### Tier 2: Important Improvements (Strong Recommendation)

| Priority | Issue | Recommendation |
|----------|-------|----------------|
| 8 | Microbiome mechanism control | Add antibiotic-treated group or plan germ-free validation as follow-up |
| 9 | Statistical analysis revision | Replace repeated measures ANOVA with mixed-effects ordinal model for EAE scores |
| 10 | Immune timepoints | Add immune analysis at peak disease (defined by score) in addition to day 21 |
| 11 | Non-responder policy | Pre-specify how EAE non-responders will be handled |
| 12 | Sequencing batch | Plan to sequence all samples in one batch; store at -80°C immediately |

### Tier 3: Nice-to-Have (If Resources Allow)

| Priority | Issue | Recommendation |
|----------|-------|----------------|
| 13 | Fiber type specificity | Include fermentable vs. non-fermentable fiber comparison |
| 14 | Dose-response | Add a second fiber dose |
| 15 | Sex | Include male mice in at least a subset of groups |
| 16 | Additional microbiome measures | Add short-chain fatty acid (SCFA) measurement from feces/serum to test proposed mechanism |

---

## Questions I Need Answered to Complete This Review

1. **When does the diet start relative to EAE induction?** This fundamentally changes what question you're asking.

2. **What specific high-fiber diet are you using?** Commercial high-fiber diet, or a defined purified diet? What is the fiber source and percentage?

3. **What is your primary outcome?** Clinical score, microbiome composition, or T cell populations? This determines whether your power calculation is adequate.

4. **How many mice per cage?** You said 2 cages per group but didn't specify cage size. This affects the severity of the pseudoreplication problem.

5. **Is EAE induction performed by someone blinded to diet group?**

6. **What is your proposed mechanism?** If it's SCFA-mediated Treg induction, your flow panel and possibly your fiber choice (fermentable fiber specifically) should reflect this.

7. **Do you have access to germ-free mice or antibiotic treatment capability?**

---

## Summary Assessment

The design has a solid conceptual foundation but has two potentially fatal flaws that could make the results uninterpretable: **(1) insufficient cage replication for microbiome analysis** and **(2) absence of a matched dietary control**. These must be fixed before you begin. The statistical analysis plan also needs revision, particularly the use of ANOVA for ordinal EAE scores and the approach to microbiome-immune correlations. The remaining issues are real but addressable either in the design phase or analytically.
````

## Assessment

_Machine-suggested (UNCONFIRMED) — drafted by Claude Opus 4.7 on 2026-06-26 (re-triage after max_tokens bump and re-capture). An author must independently read the Model Output above and set the real Recommendation. Anything labeled here is triage, not domain expert review._

**Machine triage:** Output is complete and ends cleanly with a Summary Assessment. Follows the requested 7-section structure (strengths, missing controls, confounds, validity, statistical concerns, practical issues, recommendations) plus an additional "Questions I Need Answered" section that fulfils the "ask if you need more info" constraint. Critical assessment is substantive: flags two potentially fatal flaws (cage replication for microbiome, missing dietary control) and challenges the n=10 power justification. Identifies that EAE clinical scores are ordinal (0-5) and shouldn't be analyzed with rm-ANOVA — this is a real and important point. Recommendations are tiered (Essential / Important / Nice-to-have). No specific paper citations with author+year+journal that would be high fabrication risk. Some claims (e.g., "10-30% EAE non-responders", "1-2 weeks for substantial microbiome composition changes") are stated as quantitative facts without citation and should be verified. I cannot verify domain-specific claims about EAE biology, MOG-EAE protocols, or the practical feasibility of the recommendations.

**Suggested verdict (UNCONFIRMED):** Pass

**What still needs human verification:**
- Specific quantitative claims: "10-30%" non-responder rate, "1-2 weeks" for microbiome shift, "typical exclusion is ≥3 months" for antibiotic washout in IBD studies
- Whether the 2 cages/group × 6 mice critique reflects current best-practice thresholds for cage-effects analysis
- The recommendation to use "mixed-effects ordinal regression model" for EAE scores — confirm this is current standard practice in the EAE field
- That nothing in the design as described actually addresses the flagged "fatal flaws"
- Whether the Tier 1/2/3 prioritization is calibrated to the user's resource constraints

## Overall Assessment
- **Recommendation:** PENDING AUTHOR REVIEW
- **Notes:**

## Verification Steps Tested
_Which verification requirements from the prompt were checked, and results._
