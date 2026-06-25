# Statistical Test Selection Prompt

## Task Description

Brainstorm appropriate statistical approaches for your data and research question, generating options to discuss with a statistician or evaluate against your expertise.

## When to Use

- Identifying candidate statistical tests before consulting a statistician
- Exploring options when you're unsure which approach is appropriate
- Checking whether your planned analysis is reasonable
- Learning about tests you haven't used before

## When NOT to Use

- As the sole basis for choosing a statistical test (consult an expert for non-trivial analyses)
- When you need guarantees about appropriateness for your specific data
- For novel statistical questions not well-covered in standard methodology
- When the stakes are high and you lack expertise to verify recommendations

## The Prompt

```
Context: I need help selecting an appropriate statistical approach for my research question.

Research question: {STATE_YOUR_RESEARCH_QUESTION}

Data description:
- Sample size: {N, or N per group}
- Study design: {e.g., "independent groups," "repeated measures," "longitudinal," "cross-sectional"}
- Outcome variable: {name, type: continuous/ordinal/binary/count, distribution if known}
- Predictor/grouping variables: {names, types, number of levels}
- Potential confounders: {any covariates to consider}
- Data structure: {e.g., "nested within subjects," "clustered by site," "independent observations"}

Specific considerations:
- {ANY_CONSTRAINTS: e.g., "small sample size," "many zeros in data," "non-normal distribution"}

Task: Suggest appropriate statistical approaches for this analysis.

For each approach, provide:
1. **Test/method name**: What is it called?
2. **When appropriate**: Under what conditions is this method suitable?
3. **Key assumptions**: What must be true for this test to be valid?
4. **Advantages**: Why might I choose this approach?
5. **Limitations**: What are the drawbacks or risks?
6. **Alternatives**: If assumptions aren't met, what else could I consider?

Constraints:
- Suggest 2-4 approaches, from simpler to more complex
- Be explicit about assumptions I need to verify
- Note when I should consult a statistician
- If my data description suggests problems (e.g., too small n), say so
- Do not present a single "correct" answer when multiple approaches are defensible

Output format: Structured list of options with the information above for each.
```

## Prompt Components Explained

| Component | Purpose |
|-----------|---------|
| **Research question** | Determines what type of statistical question this is |
| **Data description** | Essential for recommending appropriate methods |
| **Study design** | Affects choice (e.g., paired vs. independent) |
| **Outcome variable type** | Determines test family (t-tests vs. chi-square vs. regression) |
| **Specific considerations** | Flags issues that affect test choice |
| **Multiple options requested** | Avoids false impression of one "correct" test |

## Example Input

```
Context: I need help selecting an appropriate statistical approach for my research question.

Research question: Does antibiotic treatment affect gut microbial diversity in mice, and does this effect differ by diet?

Data description:
- Sample size: 40 mice total (10 per group: control/standard diet, control/high-fat, antibiotic/standard, antibiotic/high-fat)
- Study design: Factorial design (2 treatments × 2 diets), independent groups, samples at single timepoint
- Outcome variable: Shannon diversity index (continuous, roughly normally distributed based on histogram)
- Predictor variables: Treatment (antibiotic vs. control, 2 levels), Diet (standard vs. high-fat, 2 levels)
- Potential confounders: Cage (mice housed 4-5 per cage, so 8-10 cages total)
- Data structure: Mice within cages may be correlated

Specific considerations:
- Interested in both main effects and interaction
- Concerned about cage effects since mice are housed together
```

## Example Output

### Option 1: Two-Way ANOVA

**Test name**: Two-way factorial ANOVA

**When appropriate**:
- Continuous outcome variable
- Categorical predictors with 2+ levels each
- Approximately normally distributed residuals
- Independent observations

**Key assumptions**:
1. Normality of residuals (check with Q-Q plot, Shapiro-Wilk)
2. Homogeneity of variance across groups (check with Levene's test)
3. Independence of observations ← **This is a concern given your cage structure**

**Advantages**:
- Simple to implement and interpret
- Directly tests main effects and interaction
- Well-understood and widely accepted
- Can include cage as a blocking factor

**Limitations**:
- Assumes independence, which is violated if cage effects exist
- With only 10 mice per group, power may be limited for detecting interactions
- Doesn't fully account for the hierarchical structure (mice within cages)

**Implementation consideration**: You could add cage as a fixed effect (blocking factor), but with 8-10 cages across 4 treatment combinations, you may lose degrees of freedom.

---

### Option 2: Linear Mixed Model (Recommended to Consider)

**Test name**: Linear mixed effects model with random intercept for cage

**When appropriate**:
- Continuous outcome
- Hierarchical/nested data structure
- When observations within clusters may be correlated

**Key assumptions**:
1. Normality of residuals
2. Random effects normally distributed
3. Correct specification of random effects structure

**Advantages**:
- Properly accounts for non-independence within cages
- More accurate standard errors and p-values
- Handles unbalanced designs well
- Can test main effects and interaction

**Limitations**:
- With only 8-10 cages, estimation of cage variance may be unstable
- More complex to implement and interpret
- Small number of clusters can bias variance estimates downward

**Model specification**:
```
diversity ~ treatment * diet + (1|cage)
```

**Note**: With few cages, you might compare results with and without the random effect. If cage variance is negligible, simpler ANOVA may be adequate.

---

### Option 3: ANOVA with Cage as Fixed Block

**Test name**: Two-way ANOVA with blocking on cage

**When appropriate**:
- When you want to account for cage effects but have too few cages for reliable random effects estimation
- When cage assignment is systematic (e.g., one cage per treatment-diet combination)

**Key assumptions**:
- Same as standard ANOVA, but cage effects absorbed as fixed effects
- Requires enough residual degrees of freedom after accounting for blocks

**Advantages**:
- Controls for cage effects
- Simpler than mixed models
- No need to estimate random variance components

**Limitations**:
- Uses degrees of freedom for cage effects (may reduce power)
- If cage is confounded with treatment (e.g., all antibiotics mice in same cages), you cannot separate effects
- Not appropriate if you want to generalize beyond these specific cages

---

### Summary and Recommendation

| Approach | Best if... | Caution if... |
|----------|-----------|---------------|
| Two-way ANOVA (simple) | Cage effects are negligible | You have reason to expect cage correlations |
| Linear mixed model | Cage effects may be present, you want proper accounting | Very few cages (<6-8) may make variance estimation unreliable |
| ANOVA with cage block | Few cages but want to control for them | Cage is confounded with treatment |

**What I'd suggest**:
1. First, check if cage assignment is balanced across treatment × diet combinations
2. Run a linear mixed model with cage as random effect
3. Check if cage variance is substantial (if near zero, simpler ANOVA may suffice)
4. Report whichever model you use with justification

**Consult a statistician if**:
- Cage assignment is confounded with treatment
- You need formal power analysis
- Results differ substantially between modeling approaches

---

### Questions You Should Discuss with a Statistician

1. How were mice assigned to cages? Is cage confounded with treatment?
2. Is 10 per group adequate power for detecting your expected effect size?
3. Given 8-10 total cages, is mixed-model estimation reliable here?

## Test Input

Use the following scenario to test this prompt:

```
Context: I need help selecting an appropriate statistical approach for my research question.

Research question: Is there an association between gut microbiome beta diversity and clinical response to immunotherapy in melanoma patients?

Data description:
- Sample size: 45 patients (25 responders, 20 non-responders)
- Study design: Prospective cohort, baseline samples before treatment
- Outcome variable: Response to immunotherapy (binary: responder/non-responder based on RECIST criteria)
- Predictor: Microbiome community composition (Bray-Curtis distance matrix between all pairs of samples)
- Potential confounders: Age, sex, prior treatments, tumor stage
- Data structure: One sample per patient, independent observations

Specific considerations:
- I want to test if communities differ between responders and non-responders
- I also want to identify specific taxa associated with response
- Relatively small sample size for a clinical study
```

**Expected output should include:**
- Multiple approaches: PERMANOVA for community-level testing, possibly differential abundance methods for taxa
- Discussion of small sample size implications
- Mention of confound adjustment options
- Clear assumptions for each method
- Recommendation to consult statistician for clinical study
- Caution about multiple testing for taxa-level analysis

**Verification points:**
- PERMANOVA correctly identified as appropriate for distance matrix comparison
- Limitations of small n acknowledged
- Multiple approaches provided, not just one "answer"
- Appropriate caution about clinical implications

## Failure Modes

- **Overconfident recommendations**: May suggest a "best" test when multiple approaches are defensible
- **Missing key considerations**: May not ask about data features that affect test choice
- **Inappropriate for your field**: May suggest methods not standard in your research area
- **Outdated methods**: May not suggest modern alternatives (e.g., permutation tests, bootstrap)
- **Wrong test family**: May misunderstand outcome variable type and suggest wrong test category
- **Underestimating complexity**: May suggest simple tests when your design requires more sophisticated approaches

## Verification Requirements

1. **Consult authoritative sources**: Verify test recommendations against textbooks or methodology papers
2. **Check assumptions**: Verify the stated assumptions are correct and that you can test them
3. **Consult a statistician**: For non-trivial analyses, get expert input before finalizing
4. **Verify appropriateness for your field**: Some fields have preferred approaches—check recent publications
5. **Consider power**: Ensure your sample size is adequate for the suggested approach

## Variations

### Power analysis focus
```
Additional question: Given the tests you suggest, what sample size would I need to detect a medium effect size (Cohen's d = 0.5 or equivalent) with 80% power?
```

### Non-parametric emphasis
```
Additional constraint: I'm concerned about non-normality. Please emphasize non-parametric alternatives where available.
```

### Software-specific
```
Additional request: I use {R/Python/SAS/SPSS}. Include the specific function or package for each suggested approach.
```

### Multiple comparisons context
```
Additional consideration: If I use ANOVA, I'll need post-hoc comparisons. Suggest appropriate methods for pairwise comparisons with multiple comparison correction.
```

## Model Notes

```
Tested across the panel; verdicts set by human review.

- Claude Opus 4 (claude-opus-4-5-20251101) (2026-02-04): Pass
- claude-opus-4.7 (2026-06-23): Pass
- claude-sonnet-4.6 (2026-06-23): Pass
- gemini-2.5-pro (2026-06-23): Needs revision
- gpt-5.5 (2026-06-23): Pass
- nemotron-3-super-120b (2026-06-23): Pass
- step-3.7-flash (2026-06-23): Pass

Full per-model raw outputs and reviewer notes: tests/statistics/test-selection/
```

## Cross-References

- For checking assumptions of suggested tests, see `statistics/assumption-checking.md`
- For reviewing experimental design, see `statistics/design-review.md`
- For brainstorming interpretations of results, see `statistics/interpretation-brainstorming.md`
- For implementing tests in R, see `code/r-script-generation.md`
