# Test Results: cross-model-validation.md

## Test Metadata
- **Prompt:** fundamentals/cross-model-validation.md
- **Model:** Claude Opus 4 (claude-opus-4-5-20251101)
- **Date:** 2026-02-04
- **Tester:** Claude Code (automated testing)

## Test Input Used
Standard test input from prompt file (adversarial critique of t-test recommendation for alpha diversity)

## Filled Prompt
```
Here is a response from another AI system to the following question:

**Question:** What statistical test should I use to compare alpha diversity between two groups in my microbiome study?

**Response to critique:**
"For comparing alpha diversity between two groups, you should use a t-test. Alpha diversity metrics like Shannon diversity and observed species richness are continuous variables, making the t-test appropriate. Simply calculate the alpha diversity for each sample, then perform an independent samples t-test to compare the means between your two groups.

For example, if comparing gut microbiome diversity between healthy controls and IBD patients, calculate Shannon diversity for each sample, then use t.test() in R to compare. This is the standard approach used in most microbiome studies and will give you a p-value indicating whether the groups differ significantly."

Your task is to critically evaluate this response:

1. **Factual accuracy:** Identify any claims that may be incorrect, outdated, or unverifiable
2. **Logical validity:** Are there gaps in reasoning or unsupported conclusions?
3. **Completeness:** What important considerations are missing?
4. **Alternative perspectives:** What other approaches or interpretations weren't considered?
5. **Confidence calibration:** Where is the response more confident than warranted?

Be specific and direct. Identify concrete problems rather than vague concerns.
```

## Model Output
```
**Critical Evaluation:**

**1. Factual accuracy issues:**

- **"T-test is appropriate for continuous variables" is misleading**: While technically true that t-tests are for continuous data, this ignores the critical assumption of normality. Alpha diversity metrics, particularly Shannon diversity and observed richness, are often not normally distributed in microbiome studies—they frequently show skewness, especially in disease vs. control comparisons where one group may have compressed diversity ranges.

- **"Standard approach used in most microbiome studies" is questionable**: This claim is unverifiable and potentially incorrect. Many microbiome studies use non-parametric alternatives (Wilcoxon rank-sum/Mann-Whitney U test) precisely because of normality concerns. Reviewing recent microbiome methods literature would likely show mixed practice, not a clear "standard."

- **Observed species richness is particularly problematic for t-tests**: Richness is bounded below (cannot be negative) and often shows strong right skew or zero-inflation in low-biomass samples.

**2. Logical validity issues:**

- **Missing assumption verification step**: The response jumps directly from "continuous variable" to "use t-test" without any mention of checking whether t-test assumptions are met. This is a significant logical gap.

- **Conflates "can use" with "should use"**: The response presents the t-test as the definitive answer rather than one option that requires assumption checking.

**3. Completeness gaps:**

- **No mention of normality assumption checking**: Should recommend Shapiro-Wilk test or Q-Q plots before deciding on parametric vs. non-parametric approach.

- **No mention of non-parametric alternatives**: Wilcoxon rank-sum test (Mann-Whitney U) is the standard non-parametric alternative when normality is violated and is widely used in microbiome research.

- **No mention of rarefaction**: Alpha diversity should typically be calculated on rarefied data to account for unequal sequencing depth. Failing to rarefy can introduce systematic bias.

- **No discussion of multiple alpha diversity metrics**: Studies typically calculate multiple metrics (Shannon, Simpson, observed ASVs, Faith's PD). No guidance on whether to test each separately and how to handle multiple comparisons.

- **No mention of sample size considerations**: With small sample sizes (common in microbiome studies), the Central Limit Theorem may not rescue non-normal data, and non-parametric tests are more appropriate.

- **No discussion of effect size**: P-values alone don't indicate biological importance. Should mention calculating and reporting effect sizes (e.g., Cohen's d or rank-biserial correlation).

**4. Alternative perspectives not considered:**

- **Wilcoxon rank-sum test**: Non-parametric alternative that makes no distributional assumptions beyond continuous data. Often more appropriate for microbiome alpha diversity.

- **Permutation tests**: Another non-parametric option that can be more powerful than rank-based tests for some data structures.

- **Linear models with covariates**: If confounders (age, sex, BMI) need adjustment, a linear model with diversity as outcome is more appropriate than a simple t-test.

- **Kruskal-Wallis**: If more than two groups are involved, this extends the non-parametric approach.

- **Bootstrap confidence intervals**: For robust estimation of group differences without distributional assumptions.

**5. Confidence calibration issues:**

- **"The t-test is appropriate" stated without qualification**: Should be "A t-test *may* be appropriate *if normality assumptions are met*"

- **"Standard approach" claim is overconfident**: Presents one approach as consensus when field practice is heterogeneous.

- **"Simply calculate...then perform" oversimplifies**: Makes the analysis sound trivial when multiple decisions (rarefaction, normality checking, multiple testing) should be considered.

- **No acknowledgment of ongoing methodological debate**: There is active discussion in the microbiome field about best practices for comparing diversity, and the response presents a settled answer where none exists.

---

**Summary:**

The response provides technically functional advice (t-tests can be used on continuous data) but fails as methodological guidance by:
1. Ignoring the normality assumption and how to check it
2. Not mentioning the standard non-parametric alternative (Wilcoxon)
3. Omitting critical preprocessing steps (rarefaction)
4. Presenting one option as "the" standard approach
5. Oversimplifying what should be a considered decision

A researcher following this advice uncritically might use inappropriate tests on non-normal data and fail to account for sequencing depth differences—both of which could lead to incorrect conclusions.
```

## Assessment

### Task Achievement
- **Achieved:** Yes
- **Notes:** The model provided a thorough adversarial critique identifying specific problems with the original response across all five requested dimensions.

### Constraint Compliance
- **All constraints respected:** Yes
- **Violations noted:** None. Critique was specific and direct as requested, identifying concrete problems rather than vague concerns.

### Failure Modes
- **Failure modes observed:** None
- **Mitigation effectiveness:** The instruction to be "specific and direct" and "identify concrete problems" successfully elicited substantive critique rather than mild feedback.

### Output Format
- **Format correct:** Yes
- **Deviations:** None. All five critique dimensions addressed with clear structure.

## Overall Assessment
- **Recommendation:** Pass
- **Notes:** Excellent demonstration of cross-model adversarial critique. The critique correctly identified all expected issues: t-test normality assumptions, the Wilcoxon rank-sum alternative, rarefaction considerations, and the overconfident "standard approach" claim. The critique also identified additional valid concerns not in the expected output (effect sizes, covariates, bootstrap methods), showing the model went beyond minimum requirements. The summary effectively synthesized why the original response would be problematic for an actual researcher.

## Verification Steps Tested
- [x] T-test normality assumptions identified - **Yes, first factual accuracy point**
- [x] "Standard approach" claim questioned - **Yes, noted as unverifiable**
- [x] Non-parametric alternatives mentioned - **Yes, Wilcoxon prominently featured**
- [x] Rarefaction mentioned - **Yes, in completeness section**
- [x] Multiple testing considerations raised - **Yes**
- [x] Alternative approaches listed - **Yes, 5 alternatives including linear models**
- [x] Confidence calibration issues identified - **Yes, multiple specific examples**
