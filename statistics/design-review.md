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

## Example Output

For a representative model response to the Test Input, see:

`tests/statistics/design-review/claude-sonnet-4-6-2026-06-25.md`

That cell was captured on 2026-06-25 and human-verified by both project reviewers as passing. Other panel models' responses (Claude Opus 4.7, GPT-5.5, Gemini 2.5 Pro, Nemotron 3 Super 120B, Step-3.7 Flash) are alongside it in the same directory.

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
Tested across the panel; verdicts set by human review.

- Claude Opus 4 (claude-opus-4-5-20251101) (2026-02-04): Pass
- claude-opus-4.7 (2026-06-25): Pass
- claude-sonnet-4.6 (2026-06-25): Pass
- gemini-2.5-pro (2026-06-25): Needs revision
- gpt-5.5 (2026-06-25): Pass
- nemotron-3-super-120b (2026-06-25): Pass
- step-3.7-flash (2026-06-25): Pass

Full per-model raw outputs and reviewer notes: tests/statistics/design-review/
```

## Cross-References

- For statistical test selection, see `statistics/test-selection.md`
- For assumption checking once you have data, see `statistics/assumption-checking.md`
- For interpreting results, see `statistics/interpretation-brainstorming.md`
- For adversarial critique of completed work, see `validation/adversarial-critique.md`
