# Test Results: fundamentals/cross-model-validation.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-23.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** fundamentals/cross-model-validation.md
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
{YOUR_ORIGINAL_PROMPT}

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
## Critical Evaluation of the Alpha Diversity Statistical Advice

### Major Factual Errors

**The t-test recommendation is often inappropriate for alpha diversity data.** The response assumes normality without justification. Alpha diversity metrics, particularly observed species richness, are frequently non-normally distributed, especially with small sample sizes typical in microbiome studies (n=10-50 per group). The t-test's robustness to non-normality does not eliminate this concern—it should be verified, not assumed.

**"Standard approach" claim is false.** The actual field standard, reflected in major microbiome analysis pipelines (QIIME2, phyloseq tutorials) and methods papers, recommends non-parametric tests—specifically the **Wilcoxon rank-sum test (Mann-Whitney U)**—as the default for two-group alpha diversity comparisons. The response inverts the actual consensus.

---

### Logical Gaps

**"Continuous variable → t-test" is a non-sequitur.** Continuous measurement is a necessary but insufficient condition for a t-test. The reasoning skips the required assumptions:
- Independence of observations
- Approximate normality (or sufficient n for CLT)
- Homogeneity of variance

None of these are addressed.

**No mention of effect size.** Reporting only a p-value is insufficient. Cohen's d or rank-biserial correlation should accompany any significance test.

---

### Critical Omissions

1. **Normality testing guidance is absent.** At minimum, Shapiro-Wilk testing or Q-Q plot inspection should be recommended before choosing between parametric and non-parametric approaches.

2. **Multiple testing correction ignored.** Researchers typically compare several alpha diversity metrics simultaneously (Shannon, Faith's PD, Chao1, observed features). Running multiple t-tests without correction (Benjamini-Hochberg, Bonferroni) inflates Type I error—a serious and common mistake.

3. **Covariates completely ignored.** In IBD vs. healthy comparisons specifically, confounders like age, sex, BMI, antibiotic use, and sequencing depth are well-documented to affect alpha diversity. A simple two-sample test is often inadequate; linear models or ANCOVA controlling for covariates are frequently more appropriate.

4. **Sequencing depth (rarefaction) not mentioned.** Alpha diversity is sensitive to library size. Whether and how to rarefy, or whether to use depth-corrected metrics, is a substantive methodological decision that precedes any statistical test.

5. **Sample size considerations absent.** With n<10 per group (common in pilot microbiome studies), neither the t-test nor asymptotic non-parametric tests are reliable. Permutation tests become preferable.

---

### Overconfidence Problems

- **"This is the standard approach"** — Demonstrably incorrect; presents minority practice as consensus
- **"Will give you a p-value indicating whether the groups differ significantly"** — Conflates statistical significance with biological significance; no caveats about interpretation
- The response offers no uncertainty, no "it depends," and no recommendation to consult the data's distributional properties first

---

### What a Better Response Looks Like

1. Default to **Wilcoxon rank-sum test** unless normality is confirmed
2. Check normality explicitly before deciding
3. Apply **multiple testing correction** across metrics
4. Consider **linear models** when covariates matter
5. Address **rarefaction/depth normalization** first
6. Report **effect sizes** alongside p-values
7. Acknowledge that the "right" test depends on sample size, distribution, and study design

The response is confidently wrong on the most important point and omits the considerations that most commonly cause errors in practice.
```

## Assessment
_To be completed by a human reviewer. Do not mark Pass without reading the output._

### Task Achievement
- **Achieved:** [Yes / No / Partial]
- **Notes:**

### Constraint Compliance
- **All constraints respected:** [Yes / No]
- **Violations noted:**

### Failure Modes
- **Failure modes observed:** [None / list]
- **Mitigation effectiveness:**

### Output Format
- **Format correct:** [Yes / No]
- **Deviations:**

## Overall Assessment
- **Recommendation:** PENDING AUTHOR REVIEW
- **Notes:**

## Verification Steps Tested
_Which verification requirements from the prompt were checked, and results._
