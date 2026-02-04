# Experimental Design Review Prompt

## Task Description

Get critical feedback on an experimental design before data collection, identifying potential issues with controls, confounds, power, and analysis plan.

## When to Use

- Before starting an experiment to catch design flaws
- When planning a grant or protocol and want structured feedback
- Reviewing a trainee's proposed experiment
- Checking if your design will support the conclusions you want to draw

## When NOT to Use

- After data collection (too late to fix design issues)
- As a substitute for statistical consultation on complex designs
- When you need definitive power calculations (use proper power analysis software)
- For regulatory or clinical trial design (requires specialized expertise)

## The Prompt

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
```

## Prompt Components Explained

| Component | Purpose |
|-----------|---------|
| **Research question** | Helps evaluate if design can answer the question |
| **Complete design description** | Required for thorough review |
| **Confounders considered** | Shows what you've already thought about |
| **Planned analysis** | Identifies mismatches between design and analysis |
| **Critical stance requested** | Overcomes LLM tendency toward sycophancy |

## Example Input

```
Context: I am planning an experiment to test whether a specific probiotic (Lactobacillus strain X) prevents antibiotic-induced gut dysbiosis. I want critical feedback before I begin.

Research question: Does oral administration of Lactobacillus X before and during antibiotic treatment prevent loss of gut microbial diversity?

Experimental design:
- Study system: C57BL/6J mice, 8 weeks old, male
- Treatment groups:
  1. Control (no antibiotic, no probiotic)
  2. Antibiotic only (ampicillin 1g/L in water, 7 days)
  3. Antibiotic + probiotic (ampicillin + daily oral gavage of Lactobacillus X)
- Sample size: 10 mice per group, based on previous studies in our lab
- Controls: Group 1 is untreated control; Group 2 is antibiotic-only control
- Randomization: Mice randomly assigned to groups at study start
- Blinding: Technician collecting samples doesn't know group assignments
- Outcome measures: Shannon diversity at Day 7, relative abundance of Lactobacillus
- Timepoints: Fecal samples at Day 0 (baseline) and Day 7

Potential confounders I've considered:
- Cage effects (housing 5/cage, 2 cages per group)
- Individual baseline variation

Planned analysis: One-way ANOVA comparing Shannon diversity at Day 7 across the three groups, with Tukey post-hoc tests.
```

## Example Output

## Experimental Design Review

### 1. Strengths

- Clear, testable hypothesis
- Includes appropriate baseline measurement (Day 0)
- Randomization and partial blinding (sample collection) are good
- Antibiotic-only group provides essential comparison
- Practical sample size for a pilot/initial study

### 2. Missing Controls

**Essential:**
- **Probiotic-only group (no antibiotic)**: Without this, you cannot determine whether observed effects in Group 3 are due to probiotic protection or simply probiotic presence adding to diversity. If Lactobacillus X just colonizes and persists, it could increase Shannon diversity without actually protecting the resident community.

**Strongly recommended:**
- **Vehicle control for gavage**: Group 2 (antibiotic only) should receive daily gavage with vehicle (saline, buffer, or culture medium without bacteria). Daily gavage itself is a stressor that could affect microbiome. Without this, you're comparing antibiotic + gavage stress vs. antibiotic alone.

**Consider:**
- **Heat-killed probiotic control**: Distinguishes live organism effects from any effect of bacterial components.

### 3. Potential Confounds

| Confound | Concern | Mitigation |
|----------|---------|------------|
| **Gavage stress** | Daily handling/gavage affects Group 3 differently than Group 2 | Add vehicle-gavage control to Group 2 |
| **Cage effects** | 2 cages per group means cage and treatment are nearly confounded | With only 2 cages per group, you effectively have n=2 independent units. Consider more cages with fewer mice each. |
| **Lactobacillus detection** | If you measure Lactobacillus abundance as outcome, the probiotic group will obviously have higher levels—this doesn't prove protection | Focus on diversity and other taxa, not Lactobacillus abundance |
| **Water consumption** | Ampicillin-treated mice may drink differently (taste aversion); probiotic group also has gavage | Monitor and report water consumption |
| **Coprophagy** | Mice eat feces; within-cage microbial exchange | Inherent to mouse studies; affects generalizability |

### 4. Threats to Validity

**Internal validity issues:**

1. **The cage problem is serious.** With 10 mice in 2 cages per group, your actual independent replication is n=2 cages, not n=10 mice. If the two "antibiotic only" cages differ from the two "antibiotic + probiotic" cages for any reason (cage location, slight environmental differences, social hierarchy), you may attribute cage differences to treatment.

   *Recommendation*: Either (a) use more cages with fewer mice (e.g., pairs or trios), or (b) acknowledge this limits power and interpret cautiously, or (c) analyze with cage as a random effect but recognize you have very few cages.

2. **Confounded comparison**: Without probiotic-only and vehicle controls, you have multiple explanations for any observed difference.

3. **Single timepoint for main outcome**: If diversity is measured only at Day 7, you don't know the trajectory. Does protection occur immediately? Does it develop over time? Consider Day 3 or Day 5 samples.

**External validity issues:**

- Only male mice (sex differences in microbiome and immune response are documented)
- Single mouse strain
- Single antibiotic (ampicillin); generalization to other antibiotics uncertain
- Single probiotic dose/timing

### 5. Statistical Concerns

**Sample size:**
- 10 per group is reasonable for detecting large effects in microbiome studies
- However, effective n for cage-clustered data may be closer to 2 per group
- Without pilot data on effect size and variance, formal power is unknown

**Design-analysis mismatch:**
- One-way ANOVA ignores baseline (Day 0) measurements
- Better: ANCOVA with Day 0 as covariate, or analyze change from baseline
- With cage clustering, should consider mixed model with cage as random effect

**Analysis complications:**
- With 3 groups and post-hoc tests, you're making multiple comparisons
- Shannon diversity can be insensitive to community changes (see beta diversity as complementary)

### 6. Practical Issues

- **Probiotic viability**: How will you confirm the Lactobacillus is alive and at expected CFU when gavaged? Consider plating each dose.
- **Gavage stress**: Daily gavage for 7 days can be stressful; monitor animal welfare (weight, behavior).
- **Antibiotic palatability**: Some mice reduce water intake with ampicillin; track water consumption.
- **Sample handling**: 16S is sensitive to extraction method and storage; have a validated protocol.
- **Baseline comparison**: What if groups differ at Day 0 by chance? Randomization helps, but check and adjust if needed.

### 7. Recommendations (Prioritized)

**Must fix before proceeding:**
1. Add a probiotic-only group (Group 4: Lactobacillus X without antibiotic)
2. Add vehicle gavage to antibiotic-only group (or all non-gavage groups)
3. Either increase cage number or explicitly address cage confounding in analysis and interpretation

**Strongly recommended:**
4. Add an intermediate timepoint (Day 3 or Day 5)
5. Change analysis to ANCOVA or mixed model with baseline and cage effects
6. Measure beta diversity in addition to alpha diversity

**If resources allow:**
7. Include female mice or acknowledge sex as limitation
8. Include heat-killed probiotic control
9. Add functional outcome (e.g., colonization resistance challenge, metabolite levels)

---

### Summary Assessment

This design has a solid foundation but has a **critical flaw** in the missing controls and a **serious limitation** in the cage structure. The missing probiotic-only group means you cannot distinguish "probiotic protects against antibiotic damage" from "probiotic presence inflates diversity metrics." The cage structure means you have very low power to detect treatment effects with statistical confidence.

I recommend revising the design before proceeding. A statistician consultation would help with the cage/power issue specifically.

## Test Input

Use the following experimental design to test this prompt:

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

**Expected output should include:**
- Identification of unbalanced design (different n in disease vs control groups)
- Concern about cage confounding with only 2 cages per group
- Question about whether randomization at weaning is early enough
- Missing controls: What about fiber effect timing? Pre-treatment vs during disease?
- Power concerns for detecting diet × disease interactions
- EAE model specific concerns (variability, female-only appropriate here)
- Practical concerns: Is diet change prior to EAE induction or after?

**Verification points:**
- Critical issues identified (cage effects, unbalanced design)
- Prioritized recommendations provided
- Design-specific concerns raised (EAE model characteristics)
- Statistical analysis matched to design structure

## Failure Modes

- **Missing field-specific concerns**: May not know domain-specific issues (e.g., coprophagy in mouse studies)
- **Overconfidence in critique**: May raise concerns that aren't actually problems
- **Underconfidence**: May miss serious issues due to lack of domain knowledge
- **Generic feedback**: May provide standard advice that doesn't address your specific design
- **Not asking for needed information**: May critique based on incomplete understanding

## Verification Requirements

1. **Get expert input**: Share this review with your advisor, statistician, or experienced colleague
2. **Check field conventions**: Verify concerns are relevant to your field's standards
3. **Evaluate feasibility**: Assess whether recommended changes are practical
4. **Prioritize carefully**: Distinguish essential fixes from ideal-world improvements

## Variations

### Power-focused review
```
Additional focus: I'm particularly concerned about whether my sample size is adequate. Please provide a more detailed power assessment and suggest how to estimate required n.
```

### Revised design feedback
```
I've revised my design based on previous feedback. Here's the new design: {REVISED_DESIGN}
Please compare to the original and confirm whether the main concerns have been addressed.
```

### Pilot study scope
```
Additional context: This is a pilot study with limited resources. Please distinguish between "essential for even a pilot" and "important for a full study."
```

## Model Notes

```
Models tested: [To be completed]
Date tested: [To be completed]
Notes: [To be completed]
```

## Cross-References

- For statistical test selection, see `statistics/test-selection.md`
- For assumption checking once you have data, see `statistics/assumption-checking.md`
- For interpreting results, see `statistics/interpretation-brainstorming.md`
- For adversarial critique of completed work, see `validation/adversarial-critique.md`
