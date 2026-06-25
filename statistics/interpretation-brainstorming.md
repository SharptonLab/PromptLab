# Results Interpretation Brainstorming Prompt

## Task Description

Generate alternative interpretations, potential confounds, and questions to consider when interpreting experimental results, helping you think through your data more thoroughly.

## When to Use

- After getting results to explore possible interpretations beyond your initial hypothesis
- When results are unexpected and you need to consider alternatives
- Before writing Discussion to anticipate reviewer questions
- To identify limitations and caveats to acknowledge

## When NOT to Use

- As a substitute for domain expertise in evaluating interpretations
- To confirm your preferred interpretation (actively counter this tendency)
- When you need statistical re-analysis (this is for interpretation, not analysis)
- To generate speculative mechanisms you can't support

## The Prompt

```
Context: I have completed an experiment and am interpreting the results. I want to think through possible interpretations thoroughly, including alternatives to my initial hypothesis.

Research question: {YOUR_RESEARCH_QUESTION}

Experimental design (brief): {KEY_DESIGN_FEATURES}

Results summary:
{DESCRIBE_YOUR_KEY_FINDINGS}
- Main finding: {PRIMARY_RESULT}
- Effect size: {MAGNITUDE_IF_AVAILABLE}
- Statistical outcome: {p-values, confidence intervals, etc.}
- Secondary findings: {OTHER_NOTABLE_RESULTS}
- Unexpected findings: {ANYTHING_SURPRISING}

My initial interpretation: {WHAT_YOU_THINK_IT_MEANS}

Task: Help me think through these results critically:

1. **Support for initial interpretation**: What evidence supports my interpretation? How strong is it?

2. **Alternative interpretations**: What other explanations could produce these results? For each alternative:
   - What would it predict?
   - How could I distinguish it from my interpretation?

3. **Potential confounds**: What factors might have influenced the results that aren't captured in my interpretation?

4. **Limitations to acknowledge**: What caveats should I include when presenting these findings?

5. **Questions for follow-up**: What additional experiments or analyses would strengthen the interpretation?

6. **What the results don't show**: What conclusions would be overreach?

Constraints:
- Be genuinely critical—I want to anticipate reviewer objections
- Don't just agree with my interpretation; actively generate alternatives
- Distinguish between plausible alternatives and unlikely ones
- Focus on scientific interpretation, not just statistical significance
```

## Prompt Components Explained

| Component | Purpose |
|-----------|---------|
| **Research question** | Provides context for what interpretations are relevant |
| **Design summary** | Helps identify design-based limitations |
| **Results with specifics** | Effect sizes and statistics matter for interpretation |
| **Your initial interpretation** | Gives something to critique and build on |
| **Critical stance requested** | Counters sycophancy |

## Example Input

```
Context: I have completed an experiment and am interpreting the results. I want to think through possible interpretations thoroughly.

Research question: Does probiotic treatment protect against antibiotic-induced gut dysbiosis in mice?

Experimental design (brief):
- 4 groups (n=10 each): Control, Antibiotic, Antibiotic+Probiotic, Probiotic-only
- 7 days treatment, fecal samples at Day 0 and Day 7
- Measured Shannon diversity and community composition (16S)

Results summary:
- Main finding: Antibiotic+Probiotic group had significantly higher Shannon diversity at Day 7 than Antibiotic-only group (p=0.003, Cohen's d=1.2)
- Effect size: Mean Shannon 3.8 vs 2.2 (Antibiotic+Probiotic vs Antibiotic)
- Control group: Shannon 4.1; Probiotic-only: Shannon 4.0
- The probiotic Lactobacillus was detected at high abundance in both groups receiving it
- Beta diversity: Antibiotic+Probiotic group clustered between Control and Antibiotic groups
- Unexpected: Antibiotic+Probiotic group had slightly lower diversity than Control (not significant, p=0.09)

My initial interpretation: The probiotic protects the native gut community from antibiotic-induced diversity loss, suggesting a protective mechanism that could be developed therapeutically.
```

## Example Output

### 1. Support for Initial Interpretation

**Evidence supporting your interpretation:**
- Large effect size (d=1.2) is substantial and suggests a real biological effect
- The Antibiotic+Probiotic group maintained diversity closer to controls than to Antibiotic-alone
- Probiotic-only group shows no harm (similar to Control)
- Result is consistent with the "colonization resistance" or "niche protection" literature

**Strength of evidence:**
- Moderate-to-strong for "probiotic is associated with maintained diversity"
- Weaker for "probiotic protects native community"—you'd need compositional analysis to confirm the *native* taxa are preserved, not just that *some* bacteria are present

**Key question**: Does the preserved diversity reflect protection of native taxa, or just the presence of the probiotic itself (plus whatever survives with it)?

---

### 2. Alternative Interpretations

#### Alternative A: "Additive diversity" (not protection)
**Explanation**: The probiotic colonizes successfully and simply adds to whatever survives antibiotic treatment. You're not measuring protected diversity—you're measuring surviving diversity + probiotic.

**What it predicts**:
- Shannon diversity increase would be driven primarily by Lactobacillus presence
- Native taxa would be depleted similarly in both antibiotic groups

**How to distinguish**:
- Calculate diversity after excluding Lactobacillus from both groups
- Compare relative abundance of native taxa between Antibiotic and Antibiotic+Probiotic groups

#### Alternative B: "Niche competition" (probiotic reduces antibiotic damage indirectly)
**Explanation**: The probiotic competes with antibiotic-sensitive taxa, altering the community before antibiotic exposure in ways that happen to reduce overall disruption (not necessarily beneficial long-term).

**What it predicts**:
- Probiotic-only group would show subtle community shifts even without antibiotics
- The "protection" might not persist after probiotic withdrawal

**How to distinguish**:
- Detailed analysis of Probiotic-only vs. Control community composition
- Follow-up timepoints after probiotic/antibiotic cessation

#### Alternative C: "Antibiotic sequestration"
**Explanation**: The probiotic or its metabolites could bind or inactivate some antibiotic in the gut, reducing effective antibiotic exposure in that group.

**What it predicts**:
- Lower effective antibiotic concentration in gut contents of Antibiotic+Probiotic group
- Systemic antibiotic levels might be similar (if sequestration is local)

**How to distinguish**:
- Measure antibiotic concentration in feces or gut contents
- Check if this probiotic is known to produce β-lactamases or binding agents

#### Alternative D: "Measurement artifact"
**Explanation**: Shannon diversity is influenced by both richness and evenness. The probiotic could affect evenness without changing richness, or vice versa.

**What it predicts**:
- Differences in richness metrics (Observed ASVs) might tell a different story

**How to distinguish**:
- Report multiple diversity metrics (Observed ASVs, Chao1, Faith's PD)
- This isn't really an alternative interpretation but a measurement consideration

---

### 3. Potential Confounds

| Confound | Concern | Evidence in your data? |
|----------|---------|------------------------|
| **Lactobacillus detection** | High abundance of probiotic in treated groups means it's directly contributing to diversity metrics | Yes—you noted high abundance |
| **Cage effects** | If probiotic groups share cages distinct from antibiotic-only cages, could be cage, not treatment | Depends on your cage layout—check this |
| **Gavage effects** | Daily gavage stress could affect gut physiology differently between groups | Depends on whether all groups got equivalent handling |
| **Baseline differences** | Were groups equivalent at Day 0? | You have Day 0 data—analyze for baseline differences |
| **Water consumption** | Ampicillin in water may reduce consumption; probiotic group also gets gavage fluid | Worth checking if you tracked consumption |

---

### 4. Limitations to Acknowledge

**For your Discussion/paper:**

1. "We cannot distinguish whether the probiotic protects native community members or simply contributes its own diversity to the measured community."

2. "Shannon diversity is a single metric that conflates richness and evenness; future work should examine specific taxa of interest."

3. "We used a single antibiotic and single probiotic strain; generalizability to other antibiotics or probiotics is unknown."

4. "The study endpoint was Day 7; durability of any protective effect after treatment cessation was not assessed."

5. "Only male mice of one strain were used; sex and genetic background effects are possible."

---

### 5. Questions for Follow-up

**To strengthen your interpretation:**
1. Recalculate Shannon diversity *excluding* Lactobacillus reads from all samples—does the protective effect persist?
2. Identify which native taxa are preserved in the Antibiotic+Probiotic group—are they ecologically important?
3. Add timepoints: Day 14, 21 after treatment cessation—does protection persist?
4. Functional analysis: Are protective functions (e.g., short-chain fatty acid production) maintained?

**To test alternative mechanisms:**
5. Measure antibiotic levels in feces to rule out sequestration
6. In vitro: Does this Lactobacillus produce β-lactamases or ampicillin-binding compounds?
7. Does protection extend to a different class of antibiotics (ruling out ampicillin-specific effects)?

---

### 6. What the Results Don't Show

**Overreach to avoid:**

- ❌ "The probiotic prevents antibiotic-induced dysbiosis" — You showed diversity maintenance, not full prevention
- ❌ "This probiotic protects the native gut community" — You haven't demonstrated native taxa are protected vs. probiotic just being detected
- ❌ "This has therapeutic potential for humans" — Mouse study, single antibiotic, no health outcomes measured
- ❌ "The mechanism is colonization resistance" — You haven't tested mechanisms
- ❌ "This probiotic is safe and beneficial" — Safety wasn't the study question; "beneficial" requires defining benefit

**Appropriate claims:**
- ✓ "Probiotic co-administration is associated with maintenance of higher fecal Shannon diversity during antibiotic treatment"
- ✓ "This raises the hypothesis that probiotics may modulate antibiotic-microbiome interactions"
- ✓ "Further work is needed to determine whether this reflects protection of native taxa or simply probiotic contribution"

---

### Summary

Your initial interpretation has support but is likely an over-interpretation of what the data actually show. The most important issue is distinguishing "probiotic protects native community" from "probiotic adds to diversity metrics." This is addressable with your existing data by re-analyzing without Lactobacillus reads.

## Test Input

Use the following results to test this prompt:

```
Context: I have completed an experiment and am interpreting the results. I want to think through possible interpretations thoroughly.

Research question: Does fecal microbiota transplantation from lean donors improve metabolic outcomes in obese mice?

Experimental design (brief):
- 3 groups (n=10 each): Control (PBS), FMT from lean donors, FMT from obese donors
- High-fat diet-induced obese mice, 8 weeks treatment
- Measured: body weight, fasting glucose, microbiome composition

Results summary:
- Main finding: FMT-lean group had significantly lower fasting glucose than Control (p=0.01) and FMT-obese (p=0.03)
- Effect size: Mean glucose 145 vs 180 mg/dL (FMT-lean vs Control)
- Body weight: No significant differences between any groups
- Microbiome: FMT-lean group showed higher diversity and different community composition
- The donor-derived taxa were detectable in recipients
- Unexpected: FMT-obese group showed slightly (non-significant) lower glucose than Control

My initial interpretation: Lean-donor microbiota transfers metabolically beneficial effects to obese recipients, potentially through specific bacterial taxa that improve glucose regulation.
```

**Expected output should include:**
- Support for initial interpretation with caveats
- Alternative interpretations:
  - Donor-specific effects (not lean vs obese, but individual donor variation)
  - Procedural effects (FMT procedure itself, regardless of donor)
  - Microbiome-independent factors in donor material
- Confound consideration: Why did weight not change if metabolism improved?
- Limitations: Single donor per group? Mechanism unproven
- Follow-up questions: Would a second lean donor replicate effect? Specific taxa correlations?
- Overreach warnings: Can't claim causation from specific taxa without manipulation

**Verification points:**
- Genuinely critical, not just validating initial interpretation
- Alternative explanations plausible and specific
- Weight/glucose disconnect noted as requiring explanation
- Appropriate scope of claims identified

## Failure Modes

- **Sycophancy**: May validate your interpretation when it should challenge it
- **Missing domain-specific alternatives**: May not know field-specific alternative explanations
- **Over-generating alternatives**: May produce implausible alternatives that waste your time
- **Confirmation bias toward novelty**: May overemphasize exciting interpretations
- **Ignoring effect sizes**: May focus on significance when magnitude matters
- **Fabricating mechanisms**: May suggest mechanistic explanations without evidence

## Verification Requirements

1. **Discuss with colleagues**: Share alternatives with people who know your system
2. **Check against literature**: Are the alternative interpretations discussed in published work?
3. **Evaluate plausibility**: Rank alternatives by how plausible they are given your domain knowledge
4. **Test with data**: Can you address any alternatives with data you have or could easily collect?

## Variations

### Unexpected results focus
```
Additional context: My results were opposite to what I predicted. Please focus on interpretations that could explain this unexpected direction.
```

### Null result interpretation
```
My main finding was null (no significant difference). Help me interpret what a null result means in this context—is it evidence of no effect, or could I have missed a real effect?
```

### Reviewer anticipation
```
Additional focus: What objections would you raise as a reviewer of this paper? Help me anticipate and address likely critiques.
```

## Model Notes

```
Tested across the panel; verdicts set by human review.

- Claude Opus 4 (claude-opus-4-5-20251101) (2026-02-04): Pass
- claude-opus-4.7 (2026-06-23): Pass
- claude-sonnet-4.6 (2026-06-23): Pass
- gemini-2.5-pro (2026-06-23): Pass
- gpt-5.5 (2026-06-23): Pass
- nemotron-3-super-120b (2026-06-23): Pass
- step-3.7-flash (2026-06-23): Pass

Full per-model raw outputs and reviewer notes: tests/statistics/interpretation-brainstorming/
```

## Cross-References

- For experimental design review before data collection, see `statistics/design-review.md`
- For statistical test selection, see `statistics/test-selection.md`
- For adversarial critique of interpretations, see `validation/adversarial-critique.md`
- For writing results descriptions, see `writing/results-description.md`
