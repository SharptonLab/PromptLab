# Test Results: fundamentals/cross-model-validation.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-25.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** fundamentals/cross-model-validation.md
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
````

## Model Output
````
## Critical Evaluation

### Factual Errors

**The core recommendation is wrong.** The t-test is generally *not* the standard approach for alpha diversity in microbiome studies, for a specific reason the response ignores entirely: alpha diversity metrics are frequently non-normally distributed. Shannon diversity and especially observed species counts often show skewness, particularly with uneven sample sizes or low-depth sequencing. The t-test assumes normality, and this assumption is routinely violated in microbiome data.

**The claim that "most microbiome studies" use t-tests is unverifiable and likely false.** The actual field standard leans toward non-parametric alternatives.

---

### Logical Gaps

**The response skips the decision tree entirely.** A defensible recommendation requires:
1. Testing normality first (Shapiro-Wilk, Q-Q plots)
2. Checking variance homogeneity (Levene's test)
3. *Then* selecting a test

Jumping directly to t-test without these steps is methodologically backwards.

**Continuous scale ≠ t-test appropriate.** The reasoning that "alpha diversity metrics are continuous variables, making the t-test appropriate" is a non-sequitur. Continuous variables can still violate normality. This is a fundamental statistical error.

---

### Missing Considerations

**Non-parametric alternatives not mentioned:**
- Wilcoxon rank-sum test (Mann-Whitney U) is arguably the more defensible default given typical microbiome data distributions
- Permutation tests are common in the field

**Confounders completely ignored:**
- Sequencing depth dramatically affects alpha diversity metrics; rarefaction or depth-corrected models are often necessary
- Covariates (age, BMI, medication use, diet) frequently need adjustment, requiring linear models rather than simple two-group tests

**Multiple metrics problem not addressed:**
- Researchers typically calculate several alpha diversity metrics simultaneously (Shannon, Simpson, Faith's PD, observed features), creating multiple comparisons issues requiring correction

**Effect size absent:**
- P-values alone are insufficient; Cohen's d or rank-biserial correlation should accompany any test

**Sample size considerations ignored:**
- With small n, t-test performance degrades further; bootstrap approaches may be preferable

---

### Overconfidence Problems

| Claim | Problem |
|-------|---------|
| "This is the standard approach" | Contradicted by major microbiome analysis frameworks (QIIME2, phyloseq tutorials recommend Wilcoxon/Kruskal-Wallis) |
| "Will give you a p-value indicating whether groups differ" | Implies the p-value is straightforwardly interpretable without addressing multiple testing or effect size |
| Presents single workflow with no caveats | Real analysis requires conditional decisions |

---

### What a Better Response Looks Like

A responsible answer would:
1. Recommend checking distributional assumptions first
2. Suggest Wilcoxon rank-sum as a reasonable default with justification
3. Address sequencing depth normalization
4. Mention covariate adjustment via linear models (e.g., `lm()` with diversity as outcome)
5. Flag the multiple metrics problem
6. Acknowledge that "standard approach" varies by subfield and dataset characteristics

---

### Bottom Line

The response gives a confident, simple answer to a question that requires conditional reasoning. The specific test recommended (t-test) is defensible only after assumption checking that the response never mentions, and the field generally favors non-parametric approaches precisely because those assumptions often fail. A student following this advice uncritically could produce statistically invalid results.
````

## Assessment

_Machine-suggested (UNCONFIRMED) — drafted by Claude Opus 4.7 on 2026-06-26 to speed T4 review. An author must independently read the Model Output above and set the real Recommendation. Anything labeled here is triage, not domain expert review._

**Machine triage:** Output covers all 5 requested critique dimensions and closes with a "Better Response Looks Like" framework + Bottom Line. Complete, no truncation. Correctly identifies the t-test-as-standard claim as wrong and Wilcoxon as more appropriate default. **Strong cross-model agreement** with Opus, Gemini, GPT, Nemotron, Step on substantive critique. No quantitative citations were fabricated.

**Suggested verdict (UNCONFIRMED):** Pass

**What still needs human verification:**
- The framing "A student following this advice uncritically could produce statistically invalid results" — confirm this is acceptable tone for the use case
- Spot-check the field-practice claims (e.g., that the field "generally favors non-parametric approaches")

## Overall Assessment
- **Recommendation:** Pass
- **Notes:** Alex Alexiev (2026-06-30): **What still needs human verification:**
- The framing "A student following this advice uncritically could produce statistically invalid results" — confirm this is acceptable tone for the use case: yes
- Spot-check the field-practice claims (e.g., that the field "generally favors non-parametric approaches"): yes

## Verification Steps Tested
_Which verification requirements from the prompt were checked, and results._
