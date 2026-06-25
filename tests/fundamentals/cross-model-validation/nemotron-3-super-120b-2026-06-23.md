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


### Adversarial Critique of Model A's Response  
*(Applied to the microbiome alpha diversity question)*  

#### 1. **Factual Accuracy**  
- **Incorrect claim**: "Alpha diversity metrics like Shannon diversity [...] are continuous variables, making the t-test appropriate."  
  - *Problem*: While Shannon diversity is technically continuous, it often violates t-test assumptions (normality, homoscedasticity) in microbiome data. Shannon indices frequently exhibit right-skew, zero-inflation, or bounded ranges (e.g., 0–5 for Shannon in low-diversity samples), making parametric tests unreliable without transformation or validation. Observed species richness is a *count* variable (non-negative integers), violating continuity assumptions entirely.  
- **Outdated/unverifiable claim**: "This is the standard approach used in most microbiome studies."  
  - *Problem*: Recent methodological papers (e.g., McMurdie & Holmes, 2014; Weiss et al., 2017) explicitly caution against t-tests/ANOVA for alpha diversity due to compositionality effects and non-normality. Permutation-based tests (e.g., Wilcoxon rank-sum) or linear models with appropriate error distributions (e.g., gamma, log-normal) are now recommended as defaults in tools like `phyloseq` or `microbiome`.  

#### 2. **Logical Validity**  
- **Gap in reasoning**: Model A assumes alpha diversity metrics are "continuous variables" → therefore t-test is appropriate, but skips critical validation steps.  
  - *Problem*: No mention of checking assumptions (e.g., Shapiro-Wilk for normality, Levene’s test for equal variance). Blindly applying a t-test risks inflated Type I/II errors if assumptions fail. For example, if Shannon diversity is log-normally distributed (common), a t-test on raw values lacks power; a log-transform *first* would be needed—but Model A omits this nuance.  
- **Unsupported conclusion**: "Simply calculate the alpha diversity for each sample, then perform an independent samples t-test."  
  - *Problem*: Ignores preprocessing dependencies. Alpha diversity values depend on rarefaction depth (if used) or sequencing depth normalization. Comparing raw counts without addressing depth bias (e.g., via CSS or TSS normalization) confounds biological signal with technical artifacts.  

#### 3. **Completeness**  
- **Missing considerations**:  
  - **Data distribution checks**: No advice to visualize (QQ-plots, histograms) or test assumptions before choosing a test.  
  - **Alternative tests**: Omits robust non-parametric options (Wilcoxon rank-sum/Mann-Whitney U) or modern alternatives (e.g., PERMANOVA for beta diversity *if* misapplied to alpha—though irrelevant here, it shows lack of scope awareness).  
  - **Multiple testing correction**: If comparing >2 alpha diversity metrics (e.g., Shannon, Simpson, observed species), Model A ignores family-wise error rate inflation.  
  - **Effect size**: Focuses solely on p-value; neglects reporting Cohen’s *d* or Cliff’s delta for practical significance.  
  - **Software specifics**: No guidance on R implementation (e.g., `wilcox.test()` vs. `t.test(var.equal = FALSE)` for Welch’s correction).  

#### 4. **Alternative Perspectives**  
- **Overlooked approaches**:  
  - **Transformations + parametric tests**: Log-transform Shannon diversity (to address skew) *then* use t-test—but only after verifying normality post-transform.  
  - **Generalized linear models (GLMs)**: Model alpha diversity as gamma-distributed (for positive continuous data) or Poisson (for richness) with group as predictor—more flexible for non-normal data.  
  - **Resampling methods**: Bootstrap confidence intervals for group differences (e.g., via `boot` package) to avoid distributional assumptions entirely.  
  - **Bayesian approaches**: Estimate posterior probability of group difference (e.g., using `brms`), incorporating uncertainty in diversity estimation.  
- **Misinterpretation risk**: Model A implies alpha diversity tests alone suffice, but microbiome studies often require *beta diversity* (e.g., UniFrac) for community-level shifts—alpha diversity may miss critical ecological changes.  

#### 5. **Confidence Calibration**  
- **Overconfident claims**:  
  - "Alpha diversity metrics [...] are continuous variables, making the t-test appropriate."  
    - *Issue*: Expresses certainty about test suitability without acknowledging context-dependence (e.g., "appropriate *only if* assumptions hold"). In practice, microbiome alpha diversity often fails normality tests (Weiss et al., 2017), making this claim dangerously overconfident.  
  - "This is the standard approach used in most microbiome studies."  
    - *Issue: Overstates consensus. While t-tests appeared in early 2010s papers, current best practices (per `microbiome` tutorial, 2023) prioritize non-parametric or model-based methods. Citing "most studies" ignores methodological evolution and risks propagating outdated advice.  
- **Understated uncertainty**: No mention of how sequencing depth, rarefaction, or compositionality affects alpha diversity validity—factors that could invalidate *any* test if unaddressed.  

### Key Takeaway for Model A  
The response correctly identifies alpha diversity as a univariate comparison problem but fails to operationalize statistical rigor. It treats test selection as a mechanical step ("calculate → t-test") rather than an assumption-dependent process. A defensible answer would: (1) mandate assumption checks, (2) prioritize robustness (e.g., Welch’s t-test *or* Wilcoxon by default), and (3) contextualize limitations (e.g., "If data are normal/homoscedastic, t-test is valid; otherwise, use Wilcoxon"). Confidence should scale with evidence—not default to parametric tests.  

---  
*Critique grounded in: Weiss et al. (2017) mSystems; McMurdie & Holmes (2014) PLOS ONE; `phyloseq`/`microbiome` vignettes (2023).*
```

## Assessment

_Machine-suggested (UNCONFIRMED) — drafted by Claude Opus 4.7 on 2026-06-24 (refresh) to speed T4 review. An author must independently read the Model Output above and set the real Recommendation. Anything labeled here is triage, not domain expert review. This draft was regenerated after a harness bug (truncated test inputs on this prompt) was fixed and the model was re-run with the full prompt._

**Machine triage:** Follows the 5-section critique structure. Substantive points agree with the rest of the panel (t-test assumes normality, Wilcoxon is the more defensible default, sequencing depth / rarefaction is missing, etc.). **Flag**: this is the only output on this prompt that supplies specific author+year+journal citations to back its critique — "Weiss et al. (2017) mSystems," "McMurdie & Holmes (2014) PLOS ONE," and "phyloseq/microbiome vignettes (2023)." Both papers are well-known in the microbiome literature: Weiss et al. 2017 mSystems on normalization is real; McMurdie & Holmes 2014 is real but was published in PLOS Computational Biology ("Waste Not, Want Not"), not PLOS ONE — that journal name is likely wrong. The citation fabrication risk is exactly what this prompt is supposed to teach against, so this is a meaningful failure mode worth recording. Recommends gamma-distributed GLMs for alpha diversity and log-transformation for Shannon — both reasonable but worth a domain check.

**Suggested verdict (UNCONFIRMED):** Needs revision

**What still needs human verification:**
- That "McMurdie & Holmes (2014) PLOS ONE" is correctly cited — the well-known paper appears in PLOS Computational Biology, not PLOS ONE. If wrong, that is a partial-fabrication failure mode worth flagging in the prompt's failure modes.
- That "Weiss et al. (2017) mSystems" is correctly cited and actually says what nemotron claims about non-parametric alternatives for alpha diversity.
- That the gamma-distributed GLM recommendation is sound — gamma assumes positive continuous data but Shannon is bounded above by log(S).

## Overall Assessment
- **Recommendation:** PENDING AUTHOR REVIEW
- **Notes:**

## Verification Steps Tested
_Which verification requirements from the prompt were checked, and results._
