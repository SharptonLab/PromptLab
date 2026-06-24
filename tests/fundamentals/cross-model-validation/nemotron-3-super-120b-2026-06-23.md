# Test Results: fundamentals/cross-model-validation.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-23.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** fundamentals/cross-model-validation.md
- **Model:** nemotron-3-super-120b
- **Model ID (pinned):** Nemotron-3-Super-120B-A12B-NVFP4
- **Endpoint:** https://copilot-dev.cqls.oregonstate.edu/llm/nemotron3-super-120b-nvfp4/v1
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


**1. Factual accuracy**  
- **“Alpha diversity metrics … are continuous variables”** – Observed species richness is a *count* (integer) variable; Shannon diversity is bounded between 0 and log(S) and often behaves like a proportion after a logit transform. Treating them as unrestricted continuous normals is not strictly correct.  
- **“Simply calculate the alpha diversity for each sample, then perform an independent samples t‑test”** – The default `t.test()` in R assumes *equal variances* and *normality* of the residuals. No check of these assumptions is mentioned, yet microbiome data frequently violate them (skewed richness, heteroscedasticity across groups).  
- **“This is the standard approach used in most microbiome studies”** – While t‑tests appear in some papers, many recent microbiome studies explicitly recommend or use non‑parametric tests (Wilcoxon rank‑sum, permutation tests) or linear/mixed‑effects models because the normality assumption is often untenable. The claim overstates the prevalence of the t‑test approach.  

**2. Logical validity**  
- The argument jumps from “continuous variable → t‑test” without establishing that the *necessary* conditions (normality, homoscedasticity, independence) hold. This is a logical gap: continuity alone does not justify a parametric test.  
- The recommendation to “use t.test() in R” ignores the option to set `var.equal = FALSE` (Welch’s test) when variances differ, which is a common scenario in microbiome data.  
- No mention of effect‑size reporting or confidence intervals; a p‑value alone does not convey the magnitude of difference, yet the implication is that a significant p‑value suffices for interpretation.  

**3. Completeness**  
- **Assumption checking:** No advice to inspect histograms, Q‑Q plots, or run Shapiro‑Wilk/Levene tests before deciding on a test.  
- **Alternative tests:** No discussion of Wilcoxon rank‑sum (Mann‑Whitney), permutation‑based t‑test, or bootstrap confidence intervals, which are robust to non‑normality.  
- **Model‑based approaches:** No mention of using linear models (`lm`) or generalized linear models (e.g., Gaussian with logit‑transformed Shannon, Poisson/negative‑binomial for richness) that can incorporate covariates (age, BMI, sequencing depth, batch).  
- **Random effects / nesting:** No note about mixed‑effects models (`lme4::glmer`) when samples are clustered (e.g., multiple time points per subject, litter effects).  
- **Multiple testing:** If several alpha‑diversity indices are examined, no correction (Bonferroni, FDR) is suggested.  
- **Data preprocessing:** No comment on rarefaction vs. modeling sequencing depth as an offset or covariate, which can influence diversity estimates.  
- **Visualization:** No recommendation to plot group distributions (box/violin plots, jittered points) to inspect overlap and outliers before testing.  

**4. Alternative perspectives**  
- **Non‑parametric tests:** Wilcoxon rank‑sum (or Kruskal‑Wallis for >2 groups) is often more appropriate for richness and can be used for Shannon when normality fails.  
- **Permutation tests:** A permutation‑based t‑test (e.g., `coin::independence_test` or `permute::permTS`) provides an exact p‑value under the exchangeability null, distributional‑free.  
- **Bootstrap confidence intervals:** Bootstrapping the difference in means (or medians) yields a CI that does not rely on normality.  
- **Generalized linear models:** Model richness with a Poisson or negative‑binomial GLM (including an offset for library size) and Shannon with a Gaussian GLM after a logit or log transformation.  
- **Linear mixed‑effects models:** Account for repeated measures, litter, or plate effects (`lmer`/`glmer`).  
- **Bayesian approaches:** Provide full posterior distributions for the group difference (e.g., via `brms` or `rstanarm`).  
- **Effect‑size focus:** Report Cohen’s d, Hedges’ g, or Cliff’s delta alongside p‑values to convey practical significance.  
- **Visualization & diagnostics:** Use violin plots, jittered points, and overlay model‑based estimated means with confidence intervals.  

**5. Confidence calibration**  
- The statement “This is the standard approach used in most microbiome studies” is **overconfident**; empirical surveys of the literature show a substantial minority (often >30 %) using non‑parametric or model‑based methods, especially when sample sizes are modest or data are skewed.  
- The claim that the t‑test “will give you a p‑value indicating whether the groups differ significantly” ignores that the p‑value’s validity hinges on unverified assumptions; presenting it as a guaranteed measure of significance is misleading.  
- No qualification is given about small sample sizes (common in pilot microbiome work) where the t‑test can be severely anti‑conservative or overly conservative.  
- The advice to “simply calculate … then perform” suggests a routine, plug‑and‑play procedure, which understates the need for exploratory diagnostics and thoughtful model selection.  

**Bottom line:** While a t‑test *can* be appropriate for alpha‑diversity comparison when its assumptions are met, the response presents it as a universal, default solution without the necessary checks, alternatives, or nuance that microbiome analysts should consider. A more balanced recommendation would first examine distributional properties, consider robust or model‑based alternatives, report effect sizes and confidence intervals, and adjust for any relevant covariates or multiple testing.
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
