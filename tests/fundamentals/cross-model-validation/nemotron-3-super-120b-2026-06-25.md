# Test Results: fundamentals/cross-model-validation.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-25.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** fundamentals/cross-model-validation.md
- **Model:** nemotron-3-super-120b
- **Model ID (pinned):** Nemotron-3-Super-120B-A12B-NVFP4
- **Endpoint:** https://copilot-dev.cqls.oregonstate.edu/llm/nemotron3-super-120b-nvfp4/v1
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


**1. Factual accuracy – claims that are wrong, outdated, or unverifiable**

| Claim in the AI response | Why it is problematic |
|--------------------------|-----------------------|
| “Alpha diversity metrics … are continuous variables, making the t‑test appropriate.” | While Shannon, Simpson, observed OTUs, etc. are technically continuous, they are often **bounded** (Shannon ≥ 0, observed richness is integer‑valued and right‑skewed) and frequently **non‑normal**, especially with modest sample sizes. The t‑test’s validity relies on approximate normality of the sampling distribution of the mean, which is not guaranteed here. |
| “This is the standard approach used in most microbiome studies.” | Surveys of the literature (e.g., *Nature Microbiology* 2020‑2023 reviews) show that **non‑parametric tests (Wilcoxon rank‑sum, Kruskal‑Wallis) or linear models with robust/permutation‑based inference** are at least as common as the t‑test for alpha diversity. Claiming a universal “standard” is unverifiable and over‑generalises. |
| “Simply calculate the alpha diversity for each sample, then perform an independent samples t‑test …” | The instruction omits any **assumption‑checking step** (normality, homogeneity of variance, outliers). Without those checks the test may give inflated Type I error. |
| “Use t.test() in R to compare.” | `t.test()` defaults to Welch’s correction only if `var.equal = FALSE`; the response does not mention checking variance equality or choosing the appropriate variant, which can affect results when variances differ. |

**2. Logical validity – gaps in reasoning or unsupported conclusions**

- **From “continuous → t‑test appropriate”** the response jumps to a conclusion without invoking the Central Limit Theorem (CLT) or stating the sample‑size conditions under which the CLT would rescue the test. No justification is given for why the CLT would apply in a typical microbiome dataset (often n < 30 per group).
- The response assumes **independence of samples** without discussing possible confounding (e.g., batch effects, paired longitudinal designs, family relatedness). Ignoring these can violate the independence assumption of the t‑test.
- It treats the p‑value as the sole evidence of a difference, **ignoring effect size, confidence intervals, and biological relevance**—a logical leap from statistical significance to substantive interpretation.
- The claim that the t‑test gives “a p‑value indicating whether the groups differ significantly” presumes that the null hypothesis of equal means is the only relevant hypothesis, overlooking the possibility of **heterogeneous variances or distributional shifts** that a mean‑based test may miss.

**3. Completeness – important considerations missing**

| Missing element | Why it matters |
|-----------------|----------------|
| **Assumption diagnostics** (normality QQ‑plot, Shapiro‑Wilk, Levene’s/Brown‑Forsythe test for equal variance) | Determines whether the t‑test is safe or if a alternative is needed. |
| **Sample size / power considerations** | With small n the t‑test may be under‑powered; with very large n even trivial differences become “significant.” |
| **Effect size reporting** (Cohen’s d, Hedge’s g, or Cliff’s delta for non‑parametric) | Provides magnitude of difference, which is essential for biological interpretation. |
| **Confidence intervals for the mean difference** | Gives a range of plausible values, more informative than a p‑value alone. |
| **Multiple‑testing correction** (if several alpha metrics are tested) | Controls family‑wise error or false discovery rate. |
| **Alternative robust/permutation methods** (Wilcoxon rank‑sum, permutation t‑test, bootstrap CI) | Safer when distributional assumptions are doubtful. |
| **Model‑based approaches** (linear models, linear mixed‑effects models, GLMs with appropriate link) | Allows inclusion of covariates (age, BMI, sequencing depth) and random effects (subject, batch). |
| **Data transformations** (log, sqrt, Box‑Cox) that can improve normality | Often applied to richness or Shannon before parametric testing. |
| **Visualization** (boxplots, violin plots, jittered points) | Helps spot outliers, skewness, and group overlap before testing. |
| **Consideration of paired or repeated‑measure designs** | If samples are from the same subjects over time, a paired t‑test or linear mixed model is required. |
| **Software specifics** (e.g., `wilcox.test()`, `perm.test()` from the `perm` package, `lme4::lmer()`, `stats::t.test(var.equal = FALSE)`) | Provides concrete, reproducible code rather than a vague “use t.test()”. |

**4. Alternative perspectives – approaches or interpretations not considered**

- **Non‑parametric rank‑based tests** (Wilcoxon/Mann‑Whitney for two groups; Kruskal‑Wallis for >2) are distribution‑free and often recommended for alpha diversity because they test for a shift in the *distribution* rather than just the mean.
- **Permutation‑based t‑tests** (e.g., `permTS` in the `perm` package) generate an exact null distribution by shuffling group labels, preserving the observed data’s distribution and variance structure.
- **Bootstrap confidence intervals** for the mean difference or for median differences give a robust uncertainty estimate without relying on normality.
- **Generalized linear models (GLMs)** with a Gamma or log‑normal family can model positive, right‑skewed diversity indices directly.
- **Linear mixed‑effects models** (`lmer`) can account for random intercepts (subject, batch) and fixed effects (group, covariates), yielding more reliable inference in complex designs.
- **Bayesian approaches** (e.g., `brms` or `rstanarm`) provide posterior distributions for the group difference, allowing direct probability statements and easy incorporation of prior knowledge.
- **Multivariate frameworks** that treat alpha diversity as one outcome among many (e.g., multivariate mixed models) can borrow strength across related metrics.
- **Interpretation beyond significance** – discussing whether the observed difference is biologically meaningful (e.g., a 0.2‑unit Shannon change may be negligible) and linking to functional or clinical outcomes.

**5. Confidence calibration – where the response is overconfident**

- The statement “This is the standard approach used in most microbiome studies” is made with **high certainty** despite lacking any citation or empirical support; the confidence is unwarranted.
- The recommendation to “simply … perform an independent samples t‑test” implies that **no further checks are needed**, overstating the robustness of the test under typical microbiome data conditions.
- The suggestion that the resulting p‑value “will give you a p‑value indicating whether the groups differ significantly” treats the p‑value as a definitive answer, ignoring the influence of assumptions, sample size, and multiple testing.
- The response does not acknowledge uncertainty about the appropriateness of the t‑test (e.g., “if assumptions are met…”) and therefore presents a **binary, over‑simplified decision rule** where a nuanced, assumption‑checking workflow is warranted.

---

### Bottom‑line critique
The AI’s answer oversimplifies a common analytical step. While a t‑test *can* be used for alpha diversity, it is **only valid after verifying normality, homogeneity of variance, adequate sample size, and independence**. In many realistic microbiome settings those assumptions are violated, making non‑parametric, permutation, or model‑based alternatives preferable. A responsible recommendation would include assumption diagnostics, effect‑size reporting, confidence intervals, consideration of covariates or paired designs, and a clear statement that the t‑test is **one of several possible tools**, not the universal default.
````

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
