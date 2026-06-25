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
```
Run identical prompt through 2-3 different models. Compare outputs.

### Adversarial Critique (Model B Critiques Model A)
```
Here is a response from another AI system to the following question:

**Question:** {ORIGINAL_QUESTION}

**Response to critique:**
{MODEL_A_OUTPUT}

Your task is to critically evaluate this response:

1. **Factual accuracy:** Identify any claims that may be incorrect, outdated, or unverifiable
2. **Logical validity:** Are there gaps in reasoning or unsupported conclusions?
3. **Completeness:** What important considerations are missing?
4. **Alternative perspectives:** What other approaches or interpretations weren't considered?
5. **Confidence calibration:** Where is the response more confident than warranted?

Be specific and direct. Identify concrete problems rather than vague concerns.
```

### Synthesis Across Models
```
I asked multiple AI systems the same question and received these responses:

**Response 1:**
{MODEL_A_OUTPUT}

**Response 2:**
{MODEL_B_OUTPUT}

**Response 3 (optional):**
{MODEL_C_OUTPUT}

Synthesize these responses:
1. Where do they agree? (Higher confidence)
2. Where do they disagree? (Requires verification)
3. What does each response include that others miss?
4. What's the most defensible answer given the combination?

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

This response contains several significant problems that could lead to incorrect statistical conclusions in a real study.

---

### 1. Factual Accuracy

**The claim that t-tests are "standard" is misleading to false.**

Alpha diversity metrics are frequently non-normally distributed. Shannon diversity and especially observed species richness (a count-based metric) often show skewed distributions, particularly in studies with uneven sequencing depth or sparse communities. The t-test assumes normality, and this assumption is routinely violated in microbiome data.

**The claim that continuous scale justifies a t-test is a non-sequitur.** Continuity is a necessary but not sufficient condition for a t-test. The response treats it as sufficient, which is a logical error.

---

### 2. Logical Validity

**The reasoning chain is broken in a specific way:** The response goes directly from "continuous variable" → "use t-test" without addressing:

- Whether the normality assumption holds
- Whether sample sizes are sufficient for the Central Limit Theorem to rescue the t-test
- Whether variances are equal between groups (homoscedasticity)

This is not a minor omission — it's the core of the decision logic.

**The response also conflates "commonly done" with "correct."** Microbiome literature has well-documented reproducibility and statistical rigor problems. Citing common practice in this field as justification is particularly weak.

---

### 3. Completeness — Specific Missing Elements

**Non-parametric alternatives are entirely absent:**
- The **Wilcoxon rank-sum test** (Mann-Whitney U) is arguably the more defensible default for two-group alpha diversity comparisons precisely because it doesn't assume normality
- This is the recommendation in multiple microbiome analysis guidelines (e.g., the approaches recommended alongside QIIME2 and phyloseq workflows)

**Normality testing is not mentioned:**
- Shapiro-Wilk test on residuals/values
- Visual inspection via Q-Q plots
- These are standard pre-analysis steps

**Confounding variables are ignored:**
- Age, sex, BMI, antibiotic use, and diet are common confounders in microbiome studies
- A simple two-sample t-test cannot account for these
- Linear models (e.g., `lm()` in R with covariates) or ANCOVA are often more appropriate

**Multiple testing is not addressed:**
- Studies rarely compare just one alpha diversity metric
- Comparing Shannon, Faith's PD, observed features, and Chao1 simultaneously requires correction (Bonferroni, BH/FDR)
- The response implies a single test gives a clean answer

**Sequencing depth/rarefaction is unmentioned:**
- Observed species richness is directly confounded by sequencing depth
- Whether and how to rarefy, or whether to use depth as a covariate, is a substantive analytical decision that affects which test is even appropriate

---

### 4. Alternative Perspectives Not Considered

| Approach | When Appropriate | Not Mentioned? |
|---|---|---|
| Wilcoxon rank-sum | Non-normal distributions (common default) | ✗ Absent |
| Linear model with covariates | Confounders present | ✗ Absent |
| Permutation test | Small n, unknown distribution | ✗ Absent |
| Mixed effects model | Repeated measures / longitudinal | ✗ Absent |
| Kruskal-Wallis | Extension to >2 groups | ✗ Absent |

The response presents exactly one option as if no alternatives exist.

---

### 5. Confidence Calibration

The response is **systematically overconfident** in three specific ways:

**"You should use a t-test"** — stated without qualification. Should be: "A t-test *may* be appropriate *if* normality assumptions are met, but non-parametric alternatives are often preferred."

**"This is the standard approach used in most microbiome studies"** — this is stated as if it settles the question. Even if true descriptively, it doesn't mean it's *correct*. The microbiome field has been actively criticized for statistical practices, and "most studies do it" is not methodological justification.

**The R code example (`t.test()`)** implies a single correct implementation. Presenting one line of code without diagnostic steps creates false confidence that the analysis is complete.

---

### Summary Verdict

This response would be **actively harmful** to a researcher who followed it without prior statistical training. It:

- Omits the most important assumption check (normality)
- Ignores the most commonly recommended alternative (Wilcoxon)
- Ignores confounders entirely
- Ignores multiple testing
- Ignores sequencing depth as a confounder of the most commonly used metric it recommends

A researcher following this advice could submit a paper with inappropriate statistical methods and face rejection or post-publication criticism. The correct response should present a **decision framework**, not a single answer.
```

## Assessment

_Machine-suggested (UNCONFIRMED) — drafted by Claude Opus 4.7 on 2026-06-24 (refresh) to speed T4 review. An author must independently read the Model Output above and set the real Recommendation. Anything labeled here is triage, not domain expert review. This draft was regenerated after a harness bug (truncated test inputs on this prompt) was fixed and the model was re-run with the full prompt._

**Machine triage:** Follows the 5-section critique structure. Correctly identifies the response under review as overconfident and incomplete. Includes a structured table of unmentioned alternatives (Wilcoxon, linear-model-with-covariates, permutation, mixed-effects, Kruskal-Wallis) marked as Absent. Closes with the strongest verdict on the panel: "actively harmful" — defensible given the critique but more emphatic than the other 5 models. Argues that "most studies do it" is not methodological justification (a meta-critique of the original response's reasoning) — a useful framing. Cross-model comparison: substantive critique points unanimous across all 6 models; this output is more rhetorical than opus-4.7's tighter version. No fabricated citations; no refusals.

**Suggested verdict (UNCONFIRMED):** Pass with notes

**What still needs human verification:**
- That the "actively harmful" framing is the right tonal calibration for a teaching example — the other panel models use softer language.
- That the alternatives table (Wilcoxon, linear model with covariates, permutation test, mixed-effects model, Kruskal-Wallis) is comprehensive enough for the audience.
- The implicit claim that "most studies do it" is itself an unsupported overgeneralization — the critique attacks that pattern but does not explicitly source the counter-claim.

## Overall Assessment
- **Recommendation:** PENDING AUTHOR REVIEW
- **Notes:**

## Verification Steps Tested
_Which verification requirements from the prompt were checked, and results._
