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

## Example Output

For a representative model response to the Test Input, see:

`tests/statistics/interpretation-brainstorming/claude-sonnet-4-6-2026-06-25.md`

That cell was captured on 2026-06-25 and human-verified by both project reviewers as passing. Other panel models' responses (Claude Opus 4.7, GPT-5.5, Gemini 2.5 Pro, Nemotron 3 Super 120B, Step-3.7 Flash) are alongside it in the same directory.

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
- claude-opus-4.7 (2026-06-25): Pass
- claude-sonnet-4.6 (2026-06-25): Pass
- gemini-2.5-pro (2026-06-25): Pass
- gpt-5.5 (2026-06-25): Pass
- nemotron-3-super-120b (2026-06-25): Needs revision
- step-3.7-flash (2026-06-25): Pass

Full per-model raw outputs and reviewer notes: tests/statistics/interpretation-brainstorming/
```

## Cross-References

- For experimental design review before data collection, see `statistics/design-review.md`
- For statistical test selection, see `statistics/test-selection.md`
- For adversarial critique of interpretations, see `validation/adversarial-critique.md`
- For writing results descriptions, see `writing/results-description.md`
