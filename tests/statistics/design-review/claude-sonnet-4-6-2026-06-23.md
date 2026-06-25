# Test Results: statistics/design-review.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-23.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** statistics/design-review.md
- **Model:** claude-sonnet-4.6
- **Model ID (pinned):** claude-sonnet-4-6
- **Endpoint:** native
- **Date:** 2026-06-23
- **Tester:** cross-model-harness
- **Assembly strategy:** concat
- **Temperature:** 0.0

## Test Input Used
Standard test input from prompt file (`## Test Input`).

## Filled Prompt
```
Context: I am planning an experiment and want critical feedback on the design before I begin. I want you to identify potential problems, not just validate my plan.

Research question: {WHAT_YOU_WANT_TO_LEARN}

Experimental design:
- Study system: {ORGANISM, CELL_LINE, POPULATION, etc.}
- Treatment groups: {LIST_ALL_GROUPS_WITH_DESCRIPTIONS}
- Sample size: {N_PER_GROUP_AND_JUSTIFICATION}
- Controls: {POSITIVE/NEGATIVE_CONTROLS}
- Randomization: {HOW_SUBJECTS_ASSIGNED_TO_GROUPS}
- Blinding: {WHO_IS_BLINDED_TO_WHAT}
- Outcome measures: {PRIMARY_AND_SECONDARY_ENDPOINTS}
- Timepoints: {WHEN_DATA_COLLECTED}

Potential confounders I've considered: {LIST_ANY}

Planned analysis: {BRIEF_STATISTICAL_PLAN}

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

## Model Output
```
# Critical Review: High-Fiber Diet × EAE Mouse Experiment

## Overall Assessment

This is a reasonable starting design with a clear question, but it has several significant problems that could undermine your ability to draw conclusions. Some issues are fixable before you start; others represent fundamental tradeoffs you should consciously accept or address. I'll be direct about which problems are serious.

---

## 1. Strengths

- **Four-group factorial structure** is appropriate — you need the no-EAE fiber group to distinguish diet effects from disease effects
- **Multiple outcome levels** (behavior, microbiome, immune cells) allows mechanistic inference rather than just correlation
- **Blinded clinical scoring** is good practice and correctly identified
- **Longitudinal microbiome sampling** at multiple timepoints is well-designed for capturing dynamics
- **Acknowledging cage effects** shows awareness of a real problem (though the solution is inadequate — see below)

---

## 2. Missing Controls

### Essential

**Vehicle/fiber carrier control**
High-fiber diets differ from standard diets in multiple ways simultaneously: fiber content, caloric density, macronutrient ratios, palatability, and sometimes micronutrient composition. If you see an effect, you cannot attribute it specifically to fiber without knowing what changed. You need either:
- A matched control diet identical except for fiber content (most diet manufacturers can provide this), or
- At minimum, documentation that caloric intake and body weight are equivalent across groups

**Antibiotic-treated group (strongly recommended)**
If your hypothesis is that fiber works *through* the microbiome, you need a group that tests this mechanistically. Mice given antibiotics to deplete the microbiome, then fiber, should lose the fiber effect if the microbiome is the mediator. Without this, you can show fiber changes both the microbiome and inflammation simultaneously, but cannot establish the microbiome as the causal link — a major interpretive gap.

**Germ-free or gnotobiotic validation (longer-term consideration)**
This is a higher bar, but the field increasingly expects mechanistic evidence. Flag this as a future experiment if not feasible now.

### Nice-to-Have

**Positive control for EAE induction**
If you have variable EAE induction efficiency (common), a historical or concurrent positive control with a known immunosuppressant (e.g., fingolimod) helps confirm your model is working as expected in this cohort.

---

## 3. Potential Confounds

These are factors that could produce your expected result *without* fiber specifically modifying microbiome-immune interactions:

**Caloric intake and body weight**
High-fiber diets are often less calorie-dense and can reduce food intake. Caloric restriction alone alters immune function and can reduce EAE severity independently of microbiome changes. If fiber-fed mice eat less and weigh less, you cannot separate fiber effects from caloric effects.
> *Fix: Weigh mice weekly; measure food consumption per cage; consider pair-feeding if weights diverge*

**Diet-induced changes in intestinal transit time**
Fiber accelerates gut transit, which changes the physical environment for microbes independently of fermentation effects. This is a mechanistic nuance, not necessarily a fatal flaw, but affects how you interpret microbiome data.

**Coprophagy**
Mice eat each other's feces. This means microbiome "contamination" between cagemates is constant and intentional from the mouse's perspective. With only 2 cages per group, your cage is effectively your experimental unit for microbiome outcomes — but you're treating individual mice as the unit. This is a serious analytical problem (see Section 5).

**Stress from diet transition**
If mice are switched to high-fiber diet at weaning (8 weeks old — clarification needed on timing), the transition itself is a stressor. When exactly does the diet change occur relative to EAE induction?

**Vendor/batch effects on baseline microbiome**
C57BL/6 mice from different vendors or shipments have dramatically different baseline microbiomes. If your EAE and control mice come from different shipments or are housed at different times, this alone can explain microbiome differences.
> *Fix: Use a single shipment; co-house acclimatization period before group assignment*

**Sex hormones and EAE**
You're using female mice, which is appropriate for EAE (females develop more severe disease). However, estrous cycle stage affects both immune function and microbiome composition. With n=12 per group, random variation in cycle stage adds noise. This is probably acceptable but worth acknowledging.

---

## 4. Threats to Validity

### Internal Validity

**Cage confounding — this is your most serious problem**

You have 2 cages per group. Mice within a cage share microbiomes, bedding, water, and social environment. For microbiome outcomes especially, the cage is the true experimental unit, not the individual mouse. With 2 cages per group, you have an effective n=2 for microbiome comparisons, regardless of how many mice are in each cage.

This means:
- Your PERMANOVA will be anti-conservative (inflated false positive rate) if you treat mice as independent
- A single cage-level event (one sick mouse, one cage malfunction, contamination) can destroy half your data for that group
- You cannot statistically separate cage effects from treatment effects

> **Essential fix**: Increase to 4–5 cages per group with 3 mice per cage, rather than 2 cages with 6 mice. This keeps total animal numbers similar but gives you actual replication at the correct unit of analysis.

**Randomization timing problem**
You state mice are assigned to groups "at weaning." Standard weaning is 3 weeks; you describe mice as 8 weeks old. Clarify: Are mice assigned at 3 weeks and then aged to 8 weeks before EAE induction? If so, what diet are they on during that 5-week period? If the high-fiber diet starts at weaning, mice have very different microbiome histories by the time EAE is induced — which may be intentional but should be explicit.

**EAE induction variability**
MOG-EAE induction is notoriously variable. Typical induction rates are 70–90%, meaning some mice won't develop disease. Your analysis plan needs to specify in advance: Do you analyze all mice (intent-to-treat) or only mice that develop EAE? Each choice has implications. Excluding non-inducers introduces selection bias; including them dilutes your signal.
> *Fix: Pre-specify your inclusion criteria; consider whether to analyze by disease severity at onset*

**Day 21 endpoint may miss important dynamics**
EAE typically peaks around days 14–18 and can remit. If fiber delays rather than prevents disease, a day 21 endpoint might show groups converging after different peak severities. Your daily clinical scoring captures this, but your immune analysis at a single timepoint (day 21) may not reflect peak disease biology.
> *Consider: Adding an immune timepoint at peak disease (day 14–16) or using a separate cohort for terminal analysis at peak*

### External Validity

**EAE ≠ Multiple Sclerosis**
EAE is a model of acute CNS inflammation induced by a single antigen. MS is a chronic, heterogeneous disease with complex genetics and environmental history. Be explicit in your framing that findings are about EAE, not MS, and that translation requires additional evidence.

**Single fiber type**
"High-fiber diet" is not a single intervention. Different fibers (inulin, pectin, cellulose, resistant starch) have dramatically different fermentation profiles and microbial effects. Your findings will be specific to whatever fiber source your diet contains. Name it explicitly and acknowledge this limits generalizability.

**Female C57BL/6 only**
Results may not generalize to males or other strains. This is a standard limitation but worth stating.

**Specific pathogen-free (SPF) housing**
Your mice live in a microbiologically simplified environment compared to wild mice or humans. Fiber effects on microbiome may be larger or smaller in more complex microbial communities.

---

## 5. Statistical Concerns

### Sample Size Justification — Inadequate as Stated

"Based on previous EAE studies showing adequate power at n=10" is not a power calculation. To evaluate whether n=12 is sufficient, you need:
- The effect size you expect (e.g., difference in clinical score, or difference in microbiome beta-diversity)
- The variability in your outcome (SD from previous experiments)
- Your acceptable Type I error rate (α, typically 0.05)
- Your desired power (typically 0.80)

EAE clinical scores are highly variable (SD often 30–50% of the mean). For microbiome outcomes, effect sizes are rarely established a priori. I'd recommend:
1. Running a formal power calculation for your primary outcome (clinical score)
2. Acknowledging that microbiome analysis is exploratory/hypothesis-generating
3. Considering that with cage as the unit of analysis, your effective n for microbiome is much smaller than you think

### Repeated Measures ANOVA for Clinical Scores — Problematic

EAE clinical scores are:
- **Ordinal** (0, 1, 2, 3, 4, 5), not continuous — ANOVA assumes continuous data
- **Non-normally distributed** — scores cluster at 0 before disease onset and at peak values
- **Bounded** — cannot go below 0 or above 5
- **Correlated within mouse** — which repeated measures handles, but the ordinal issue remains

> *Better approaches*: Mixed-effects models with appropriate link functions for ordinal data; area under the curve (AUC) analysis of disease course; survival analysis for time to onset; maximum score analysis. Consult a statistician before finalizing.

### PERMANOVA for Microbiome — Appropriate but Incomplete

PERMANOVA is the right choice for beta-diversity, but:
- It assumes exchangeability of samples under the null hypothesis, which is violated if cage effects exist
- You should include cage as a blocking factor or covariate
- Report which distance metric you'll use (UniFrac, Bray-Curtis, etc.) and justify it
- Alpha diversity (within-sample diversity) should also be reported — different metrics (Shannon, Chao1) answer different questions
- Differential abundance testing (which taxa change?) requires separate analysis with appropriate multiple testing correction

### Correlation Analysis — Exploratory, Not Confirmatory

Correlating microbiome changes with immune parameters is hypothesis-generating. With the number of taxa you'll identify, you'll have a massive multiple testing problem. Be explicit that these correlations are exploratory and require independent validation. Do not present them as confirmatory findings.

### Design-Analysis Mismatch

Your design is a 2×2 factorial (EAE yes/no × diet). Your analysis plan doesn't mention testing the interaction term, which is actually your primary question: Does fiber have a *different* effect in EAE mice than healthy mice? A factorial ANOVA or mixed model should test:
- Main effect of EAE
- Main effect of diet
- **EAE × Diet interaction** ← this is your hypothesis

---

## 6. Practical Issues

**Fiber diet palatability and consumption**
High-fiber diets are sometimes less palatable. If EAE mice (which lose weight during disease) eat less of the high-fiber diet, you have a confound and a welfare concern simultaneously. Measure food intake per cage from the start.

**Fecal sample collection**
Specify your collection protocol: individual mouse samples or pooled per cage? Individual is better scientifically but requires training mice to defecate on cue or using metabolic cages. Pooled samples eliminate individual variation data. Clarify this before you start.

**16S rRNA gene sequencing decisions**
Which variable region (V3-V4? V4?)? Which sequencing platform? What sequencing depth per sample? These choices affect which taxa you can detect and how results compare to published literature. Standardize with your sequencing facility before beginning.

**EAE scoring inter-rater reliability**
Even with blinding, EAE scoring has subjectivity. If multiple people score at different times, establish inter-rater reliability before the experiment. Score drift over a 21-day experiment is a real problem.

**Sample attrition**
EAE mice can die or reach humane endpoints before day 21. With n=12, losing 2–3 mice per group is plausible and will affect your power. Plan for this in your sample size calculation and specify your humane endpoint criteria in advance.

**Microbiome sample storage**
Fecal samples must be frozen immediately at -80°C or in appropriate stabilization buffer. Delays between collection and freezing alter microbiome composition. Standardize collection time of day (microbiome has diurnal variation) and handling protocol.

---

## 7. Prioritized Recommendations

### Essential — Fix Before Starting

| Priority | Issue | Recommended Fix |
|----------|-------|-----------------|
| 🔴 1 | Cage confounding | Increase to 4–5 cages/group, 3 mice/cage |
| 🔴 2 | Diet not controlled | Use matched control diet; measure food intake and body weight weekly |
| 🔴 3 | No mechanistic control | Add antibiotic-treated group to test microbiome mediation |
| 🔴 4 | Statistical approach for clinical scores | Replace repeated measures ANOVA with appropriate ordinal/mixed model; consult statistician |
| 🔴 5 | Power calculation | Conduct formal power analysis for primary outcome |
| 🔴 6 | Randomization timing | Clarify and document exactly when diet starts relative to EAE induction |

### Important — Address If Possible

| Priority | Issue | Recommended Fix |
|----------|-------|-----------------|
| 🟡 7 | EAE induction variability | Pre-specify inclusion criteria for non-inducers |
| 🟡 8 | Single immune timepoint | Add peak-disease timepoint or use separate cohort |
| 🟡 9 | Interaction term missing | Explicitly test EAE × Diet interaction in analysis plan |
| 🟡 10 | 16S protocol unspecified | Standardize region, platform, depth before starting |
| 🟡 11 | Fecal collection protocol | Specify individual vs. pooled; standardize time of day |

### Nice-to-Have — Consider for Future Experiments

| Priority | Issue | Recommended Fix |
|----------|-------|-----------------|
| 🟢 12 | Mechanistic validation | Germ-free or gnotobiotic transfer experiment |
| 🟢 13 | Positive disease control | Add fingolimod group to validate model sensitivity |
| 🟢 14 | Fiber specificity | Test multiple fiber types in follow-up |
| 🟢 15 | Sex generalizability | Replicate in males |

---

## Questions I Need You to Answer

Before I can fully evaluate some aspects, please clarify:

1. **What specific fiber** is in the high-fiber diet, and what is the matched control diet?
2. **When exactly does the diet start** — at weaning (3 weeks) or at 8 weeks just before EAE induction?
3. **What is your primary outcome** — clinical score, microbiome composition, or T cell populations? This determines your power calculation.
4. **What previous effect size** did your lab observe in prior EAE experiments that justifies n=10?
5. **How are fecal samples collected** — individual or pooled per cage?
6. **Do you have access to a statistician** for consultation on the analysis plan?

---

## Summary Judgment

Your design has the right conceptual structure but two problems could make your results uninterpretable even if the experiment runs perfectly: **(1) cage confounding in the microbiome analysis** and **(2) inability to distinguish fiber effects from other dietary changes**. These are fixable before you start and should be treated as blockers. The statistical approach for clinical scores also needs revision. The remaining issues are real but manageable. I'd recommend addressing the red-priority items before ordering animals.
```

## Overall Assessment
- **Recommendation:** Pass
- **Notes:**
## Verification Steps Tested
_Which verification requirements from the prompt were checked, and results._
