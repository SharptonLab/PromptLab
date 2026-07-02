# Assumption Checking Prompt

## Task Description

Generate a workflow for checking the assumptions of a statistical test, including what to check, how to check it, and what to do if assumptions are violated.

## When to Use

- Before running a statistical analysis to verify assumptions are met
- When interpreting results and wondering if assumption violations affect conclusions
- When learning what assumptions a test requires
- When reviewers question whether your analysis assumptions were verified

## When NOT to Use

- As the sole guide for complex analyses (consult a statistician)
- When you don't have the data to actually perform the checks
- When assumption checking would be post-hoc rationalization for choosing tests

## The Prompt

```
Context: I plan to use {STATISTICAL_TEST_OR_MODEL} to analyze my data. I need to verify the assumptions are met.

Analysis details:
- Test/model: {SPECIFIC_TEST: e.g., "two-way ANOVA," "logistic regression," "Wilcoxon rank-sum"}
- Outcome variable: {type and name}
- Predictor(s): {type and names}
- Sample size: {n or n per group}
- Software: {what you're using}

Data characteristics I've noticed:
- {ANY_OBSERVATIONS: e.g., "outcome looks skewed," "several outliers visible," "one group has higher variance"}

Task: Provide a complete assumption-checking workflow:

1. **List all assumptions** for this test, in order of importance (which violations are most problematic)

2. **For each assumption**:
   - What it means in plain language
   - How to test it (formal tests and/or visual diagnostics)
   - How to interpret the results
   - What to do if violated (robust alternatives, transformations, or when it's okay to proceed)

3. **Code examples** for the assumption checks in {SOFTWARE}

4. **Decision summary**: A flowchart or decision tree for how to proceed based on results

Constraints:
- Be practical—focus on violations that meaningfully affect inference
- Note when minor violations are unlikely to matter
- Acknowledge that some assumption tests have their own limitations
```

## Prompt Components Explained

| Component | Purpose |
|-----------|---------|
| **Specific test** | Determines which assumptions apply |
| **Data characteristics** | Flags likely issues to focus on |
| **Software** | Provides runnable code |
| **Decision focus** | Makes output actionable |

## Example Output

For a representative model response to the Test Input, see:

`tests/statistics/assumption-checking/claude-sonnet-4-6-2026-06-25.md`

That cell was captured on 2026-06-25 and human-verified by both project reviewers as passing. Other panel models' responses (Claude Opus 4.7, GPT-5.5, Gemini 2.5 Pro, Nemotron 3 Super 120B, Step-3.7 Flash) are alongside it in the same directory.

## Test Input

Use the following scenario to test this prompt:

```
Context: I plan to use PERMANOVA to analyze my data. I need to verify the assumptions are met.

Analysis details:
- Test/model: PERMANOVA (adonis2 in vegan package)
- Outcome variable: Bray-Curtis distance matrix of microbiome community composition
- Predictors: Treatment group (3 levels), Time (2 levels), Treatment × Time interaction
- Sample size: 60 samples (10 per group-time combination)
- Software: R with vegan package

Data characteristics I've noticed:
- Groups have different spread on PCoA plots (dispersion looks unequal)
- One treatment group clusters more tightly than others
- Sample sizes are equal across groups

Task: Provide a complete assumption-checking workflow:

1. **List all assumptions** for this test, in order of importance (which violations are most problematic)

2. **For each assumption**:
   - What it means in plain language
   - How to test it (formal tests and/or visual diagnostics)
   - How to interpret the results
   - What to do if violated (robust alternatives, transformations, or when it's okay to proceed)

3. **Code examples** for the assumption checks in R with vegan

4. **Decision summary**: A flowchart or decision tree for how to proceed based on results

Constraints:
- Be practical—focus on violations that meaningfully affect inference
- Note when minor violations are unlikely to matter
- Acknowledge that some assumption tests have their own limitations
```

**Expected output should include:**
- Key assumptions: multivariate homogeneity of dispersions (most critical for PERMANOVA), adequate sample size
- betadisper() explained as the dispersion homogeneity test
- Discussion of PERMANOVA sensitivity to dispersion differences
- Code examples for betadisper and permutest
- Guidance on interpretation if dispersion differs significantly
- Alternatives if assumptions violated (consider dispersion as outcome)

**Verification points:**
- Correctly identifies dispersion homogeneity as key assumption
- Provides betadisper code in R
- Explains that significant PERMANOVA with unequal dispersion could mean location OR dispersion difference
- Practical guidance given observed unequal spread

## Failure Modes

- **Wrong assumptions listed**: May list assumptions for a different test
- **Over-emphasis on normality**: May overstate importance of normality for large samples
- **Test limitations not noted**: Formal assumption tests have their own assumptions and limitations
- **Cookbook approach**: May not emphasize that judgment is required
- **Missing field conventions**: Some fields have specific preferences for handling violations

## Verification Requirements

1. **Verify assumptions are correct for your test**: Cross-reference with textbooks
2. **Actually run the checks**: Don't just take the code—run it on your data
3. **Use judgment**: Understand that some violations matter more than others
4. **Document what you did**: Report assumption checks in your methods

## Variations

### Pre-analysis focus
```
Additional context: I haven't run the model yet and want to check assumptions before proceeding.
Task: Provide checks I can run on the raw data before fitting the model.
```

### Specific violation follow-up
```
I've found that {SPECIFIC_ASSUMPTION} is violated. What are my options and what do you recommend?
```

### Reporting template
```
Additional request: Provide template text for reporting assumption checks in a methods section.
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

Full per-model raw outputs and reviewer notes: tests/statistics/assumption-checking/
```

## Cross-References

- For selecting appropriate tests, see `statistics/test-selection.md`
- For experimental design review, see `statistics/design-review.md`
- For implementing analysis in R, see `code/r-script-generation.md`
