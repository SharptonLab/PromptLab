# Test Results: design-review.md

## Test Metadata
- **Prompt:** statistics/design-review.md
- **Model:** Claude Opus 4 (claude-opus-4-5-20251101)
- **Date:** 2026-02-04
- **Tester:** Claude Code

## Test Input Used

Standard test input from prompt file:

```
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
```

## Filled Prompt

````
Context: I am planning an experiment to test whether a high-fiber diet alters gut microbiome-immune interactions in a mouse model of autoimmune disease. I want critical feedback before I begin. I want you to identify potential problems, not just validate my plan.

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

# Experimental Design Review: EAE Mouse Model with Dietary Fiber Intervention

## 1. Strengths

Your design has several solid features:

- **Appropriate model system**: EAE in C57BL/6 mice is a well-established MS model. Female mice are appropriate—EAE is typically more robust in females, matching human MS epidemiology.

- **Full 2×2 factorial design**: Including all four combinations (EAE±, fiber±) allows you to test main effects and interactions—essential for your question.

- **Longitudinal sampling**: Multiple fecal timepoints (days 0, 7, 14, 21) allow you to track microbiome dynamics, not just endpoint differences.

- **Blinded clinical scoring**: Critical for EAE studies where scoring can be subjective.

- **Multiple outcome levels**: Combining clinical scores, microbiome, and immune cell populations provides a more complete picture.

- **Baseline measurement**: Day 0 fecal sample provides pre-treatment reference.

## 2. Missing Controls

### Essential

**Sham immunization control**: Groups 3-4 receive no EAE induction, but do they receive the vehicle/adjuvant without MOG peptide? The immunization procedure itself (CFA, pertussis toxin) causes substantial inflammation and could affect the microbiome independently of EAE.

*Recommendation*: Either (a) administer sham immunization (CFA + vehicle without MOG) to non-EAE groups, or (b) acknowledge that your non-EAE groups are truly naive and cannot distinguish EAE-specific effects from immunization effects.

### Strongly Recommended

**Pair-feeding or food consumption monitoring with adjustment**: If high-fiber mice eat more or less than standard diet mice (fiber is filling; also affects palatability), caloric intake differences could confound results.

*Recommendation*: At minimum, track daily food consumption. Ideally, pair-feed or report calories consumed.

### Consider

**Time-matched controls**: EAE progresses over time. Your non-EAE groups may not experience the same time-dependent stress as EAE groups. This is inherent to the model but worth noting.

## 3. Potential Confounds

| Confound | Concern | How It Could Produce Your Result |
|----------|---------|----------------------------------|
| **Food consumption** | High-fiber diet may reduce caloric intake | Caloric restriction itself has anti-inflammatory effects and modifies the microbiome |
| **Cage effects** | 2 cages per group = 8 cages total | With only 2 cages per group, cage effects could be mistaken for treatment effects (see Statistical Concerns) |
| **Diet timing** | Randomization at weaning, but when does diet change begin? | If diet begins well before EAE induction, you're studying prophylactic effects. If concurrent, you're studying therapeutic effects. These are different questions. |
| **Litter effects** | You mentioned this as considered | If littermates are not distributed across groups, genetic/maternal effects could confound. How are litters assigned to groups? |
| **Fiber type** | Different fibers have different effects | "High-fiber diet" could mean inulin, cellulose, resistant starch, etc.—mechanisms differ |
| **EAE severity variability** | EAE has high inter-mouse variability | High variability may mask moderate treatment effects, especially with n=12 |

### Critical Question: When Does the Dietary Intervention Begin?

Your design says "assigned to groups at weaning," but you're studying 8-week-old mice. Does this mean:
- (A) Fiber diet starts at weaning (~3 weeks) and continues through EAE? (prophylactic)
- (B) Fiber diet starts at 8 weeks, concurrent with EAE induction? (therapeutic)
- (C) Fiber diet starts at 8 weeks, before EAE induction? (pre-treatment window?)

**This substantially affects interpretation.** Prophylactic and therapeutic mechanisms can differ, and the microbiome at disease onset will be very different in A vs. B.

## 4. Threats to Validity

### Internal Validity

**The cage effect problem is serious.**

With only 2 cages per group and 6 or 12 mice per group:
- EAE + standard: 2 cages × 6 mice
- EAE + fiber: 2 cages × 6 mice
- No-EAE + standard: 2 cages × 3 mice
- No-EAE + fiber: 2 cages × 3 mice

Your true independent replication is n=2 per group, not n=12 or n=6. Any cage-level factor (cage position, water bottle, social dynamics, coprophagy homogenization) could produce differences attributed to treatment.

**Unbalanced design in healthy controls**

You have n=12 for EAE groups but n=6 for non-EAE groups. While this reflects the clinical focus, it creates:
- Less power to detect fiber effects in healthy mice
- Unequal precision for the 2×2 interaction

**Blinding limitations**

Clinical scoring is blinded, which is excellent. But what about:
- Diet preparation and cage maintenance (who knows which cages get which diet?)
- Sample processing (does technician know group when extracting DNA, staining for flow?)
- Analysis (are you blinded when analyzing data?)

### External Validity

- **Single strain, single sex**: Results may not generalize to other strains or males
- **Single fiber type**: Generalization to other fibers is uncertain
- **MOG35-55 EAE**: This specific model may not reflect all aspects of MS
- **Laboratory microbiome**: Your facility's baseline microbiome differs from other facilities

## 5. Statistical Concerns

### Sample Size

**For clinical EAE scores:**
Your power calculation for n=10 may be appropriate, and you have n=12. However:
- EAE has high variability (mice with score 0-1 and mice with score 4 in the same group)
- With 2 cages per group, effective n may be much smaller if cage effects exist
- Power for detecting the *interaction* (does fiber effect differ with EAE status?) requires larger n than for main effects

**Recommendation**: If your pilot data suggest the effect of fiber is modest, n=12 may be underpowered, especially for detecting diet × EAE interactions.

### Design-Analysis Mismatch

**Your planned analysis may not match your design:**

| Analysis | Concern |
|----------|---------|
| Repeated measures ANOVA for clinical scores | Appropriate, but should include diet × time interaction. Should also consider accounting for cage. |
| PERMANOVA for microbiome | Works for comparing groups at single timepoint. For longitudinal microbiome (4 timepoints), consider: Which timepoint matters? Or use constrained ordination with time? |
| Correlate microbiome with immune | Correlation is exploratory but requires defining: Which microbiome features? At which timepoint? How do you handle multiple comparisons? |

**The cage problem affects analysis:**
With only 2 cages per group, adding cage as a random effect gives you very few independent units. Your effective sample size for diet comparisons may be n=2, not n=12.

**Unbalanced design complicates 2×2 analysis:**
Type III sums of squares or equivalent should be used. With n=12 vs. n=6, the interaction effect will be estimated with different precision in different cells.

### Recommendations for Analysis

1. For EAE scores: Mixed model with mouse as random effect, cage as random effect (though only 2 per group), diet and time as fixed effects
2. For microbiome: Analyze day 21 as primary endpoint; use earlier timepoints for exploratory trajectory analysis
3. For correlations: Pre-specify which taxa/features you'll correlate; apply FDR correction; consider day 21 only

## 6. Practical Issues

| Issue | Risk | Mitigation |
|-------|------|------------|
| **EAE induction failure** | Some mice may not develop EAE | Plan for potential exclusions; define a priori criteria for "EAE non-responders" |
| **Mortality** | Severe EAE can be lethal; affects n | Monitor carefully; define humane endpoints; plan for attrition in power calculation |
| **Diet palatability** | Mice may reject or under-eat high-fiber diet | Track food consumption daily; have backup if severe aversion |
| **Cage fighting** | Females usually okay, but stressed/sick mice can be aggressive | Monitor and separate if needed |
| **Fecal sample quality** | Need enough for 16S; consistency across mice | Standardize collection protocol; collect at same time of day |
| **Flow cytometry timing** | All 36 mice at day 21 is a lot of flow | Can you process all samples in one session? Consider batching with batch as covariate |
| **Freezer failure** | Losing samples would be devastating | Backup freezer; split samples if possible |

### Timeline Question

Day 0 = EAE induction day? Or day 0 = diet switch day?

Clarify your timeline:
- Day of dietary intervention start
- Day of EAE induction (if different)
- Day of disease onset (typically day 10-12 in EAE)
- Day 21 endpoint (post-induction? Post-diet start?)

## 7. Recommendations (Prioritized)

### Must Fix Before Proceeding

1. **Address the cage problem**
   - **Best option**: Increase number of cages to at least 4-6 per group with 2-3 mice each
   - **Minimum option**: Acknowledge cage as a confound; analyze with cage as random effect but interpret cautiously; discuss limitation

2. **Clarify dietary intervention timing**
   - When exactly does the fiber diet begin relative to EAE induction?
   - This determines whether you're studying prophylaxis vs. treatment

3. **Decide on sham immunization**
   - Either add sham-immunized controls or explicitly state that non-EAE groups cannot distinguish EAE effects from adjuvant effects

### Strongly Recommended

4. **Balance sample sizes or justify imbalance**
   - Either increase non-EAE groups to n=12, or explicitly state why healthy controls need less power
   - Consider: For your research question, do you even need healthy controls? If the question is "does fiber affect EAE," the critical comparison is groups 1 vs. 2

5. **Extend blinding**
   - Blind sample processing and analysis, not just clinical scoring

6. **Track and report food consumption**
   - Daily food intake should be measured and reported, if not controlled

7. **Specify your fiber source**
   - "High-fiber diet" is not sufficient detail. What type of fiber? What percentage?

### Before Analysis

8. **Pre-register analysis plan**
   - Define primary endpoint, primary comparison, and statistical tests before unblinding
   - Define criteria for excluding non-responder mice

9. **Plan for multiple comparisons**
   - With microbiome data generating hundreds of features, pre-specify how you'll handle multiplicity

### If Resources Allow

10. **Add intermediate disease timepoint**
    - Day 14-15 immune analysis (at peak disease) in addition to day 21 (recovery phase)

11. **Include male mice**
    - Or explicitly limit conclusions to females

12. **Consider a second fiber type**
    - Or frame conclusions as specific to your fiber, not "dietary fiber" broadly

---

## Summary Assessment

This design addresses an interesting and timely question with clinical relevance. The core structure (2×2 factorial, longitudinal sampling, multiple outcomes) is sound.

**Critical flaw:** The cage structure (only 2 cages per group) severely limits your ability to distinguish treatment effects from cage effects. This is the most important issue to address.

**Significant issues:**
- Timing of dietary intervention needs clarification
- Unbalanced healthy controls reduce power for diet × disease interaction
- Sham immunization question affects interpretation

**Before proceeding:** I would recommend discussing the cage issue with a statistician. With only 2 cages per group, your effective sample size for detecting diet effects is arguably n=2, regardless of how many mice are in each cage. Either reorganize cages or plan your analysis and interpretation around this limitation.

---

## Questions I'd Need Answered

1. When exactly does the fiber diet start relative to weaning and EAE induction?
2. What is the specific fiber type and dose in the high-fiber diet?
3. How are litters distributed across groups?
4. Will non-EAE groups receive sham immunization?
5. Is there any way to increase the number of cages per group?
6. What is your plan for EAE non-responders (mice that don't develop disease)?

## Overall Assessment

- **Recommendation:** Pass
- **Notes:**
  - Critical issues correctly identified:
    - Cage confounding as severe limitation (effective n=2)
    - Unbalanced design (n=12 vs n=6 for EAE vs non-EAE groups)
    - Missing sham immunization control
    - Unclear timing of dietary intervention
  - Prioritized recommendations provided in clear tiers
  - Design-specific concerns raised (EAE model variability, sham immunization)
  - Statistical analysis appropriately matched to design structure
  - Power concerns for interaction effects noted
  - Practical issues (mortality, food palatability, flow cytometry logistics) addressed
  - The output would be valuable for a researcher planning this experiment
  - Questions at end demonstrate appropriate recognition of information gaps

## Verification Steps Tested

| Verification Requirement | Result |
|-------------------------|--------|
| Unbalanced design identified (different n in disease vs control groups) | Confirmed |
| Cage confounding concern raised (only 2 cages per group) | Confirmed (identified as critical flaw) |
| Question about timing of randomization/intervention | Confirmed (dietary timing ambiguity highlighted) |
| Missing controls identified | Confirmed (sham immunization, pair-feeding) |
| Power concerns for diet × disease interactions | Confirmed |
| EAE model specific concerns raised | Confirmed (variability, non-responders, sham immunization) |
| Practical concerns noted | Confirmed (mortality, palatability, flow timing) |
| Prioritized recommendations provided | Confirmed (3 tiers: must fix, strongly recommended, if resources allow) |
