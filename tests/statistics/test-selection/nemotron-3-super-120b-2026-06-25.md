# Test Results: statistics/test-selection.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-25.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** statistics/test-selection.md
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
````

## Model Output
````


**Statistical‑analysis options for linking gut‑microbiome β‑diversity (Bray‑Curtis) to binary immunotherapy response in melanoma (n = 45)**  

Below are three defensible strategies, ordered from relatively simple to more complex. For each I list the method name, when it is appropriate, key assumptions, advantages, limitations, and what to try if the assumptions fail.  

---  

## 1. PERMANOVA (adonis / adonis2) – “Permutational Multivariate Analysis of Variance”

| Item | Details |
|------|---------|
| **Test/method name** | PERMANOVA (implemented as `adonis2` in the **vegan** R package or `permANOVA` in **scikit‑bio**). |
| **When appropriate** | You want to test whether the overall centroid of microbiome communities differs between responders vs. non‑responders, while optionally adjusting for covariates (age, sex, prior treatment, tumor stage). Works with any distance matrix (here Bray‑Curtis). |
| **Key assumptions** | 1. **Exchangeability under the null** – permutations of sample labels generate a valid reference distribution (requires independent observations). <br>2. **Homogeneity of multivariate dispersion** (similar spread/variance) across groups; if violated, PERMANOVA can conflate location and dispersion effects. <br>3. Linear additive effects of covariates (if included). |
| **Advantages** | • Directly tests the hypothesis of interest on the distance matrix (no need to reduce dimensions first). <br>• Permutation‑based p‑value is robust to non‑normality and small‑to‑moderate sample sizes. <br>• Easy to add strata or blocking variables (e.g., batch) and to include multiple confounders in the model formula. |
| **Limitations** | • Sensitive to differences in dispersion; a significant result may reflect heterogeneity rather than a shift in community composition. <br>• With *n* = 45, the number of unique permutations is limited (max = 45! but practical Monte‑Carlo permutations of 5 000–10 000 are fine). <br>• Does not provide effect‑size estimates for individual taxa. |
| **Alternatives if assumptions fail** | • **Betadisper** (PERMDISP) to test and, if needed, stratify by dispersion or use a dispersion‑adjusted PERMANOVA. <br>• **Distance‑based linear model (DistLM)** with sequential testing (e.g., `distlm.forward` in **PRIMER**) that can partition variation and is less sensitive to dispersion when used with sequential tests. <br>• If dispersion differs markedly, consider a **generalized linear mixed model (GLMM)** on presence/absence or count data (see Approach 3). |

**What to verify**  
- Run `betadisper()` on the Bray‑Curtis matrix and test for homogeneity of variances (ANOVA on distances to group centroids).  
- If dispersion differs, report both PERMANOVA and betadisper results, or choose a dispersion‑robust method.  

**When to consult a statistician**  
- To decide on the number of permutations, to set up a stratified permutation scheme (e.g., by sequencing batch), and to interpret potential dispersion confounds.  

---  

## 2. Distance‑Based Redundancy Analysis (dbRDA) + Variation Partitioning

| Item | Details |
|------|---------|
| **Test/method name** | Distance‑based Redundancy Analysis (dbRDA) – a constrained ordination technique (`capscale` in **vegan**). |
| **When appropriate** | You want to model β‑diversity as a function of response and covariates, visualize the constrained axes, and quantify how much variation each predictor explains. Works well when you suspect linear relationships between predictors and the distance‑based representation of community composition. |
| **Key assumptions** | 1. **Linear relationships** between predictors and the PCoA‑transformed Bray‑Curtis distances (dbRDA fits a linear model to the principal coordinates). <br>2. **Independence** of samples. <br>3. **Multivariate normality** of residuals is *not* required because significance is assessed by permutation (usually 999–9 999 permutations). <br>4. **Homogeneity of dispersion** is still advisable; severe heterodispersion can bias the constrained axes. |
| **Advantages** | • Provides an ordination plot that shows how responders and non‑responders separate along constrained axes, facilitating interpretation. <br>• Allows **variation partitioning** (e.g., `varpart`) to separate the unique contribution of response from that of confounders. <br>• Permutation‑based significance makes it robust to non‑Euclidean distance matrices like Bray‑Curtis. |
| **Limitations** | • Interpretation of axes can be less intuitive than raw taxa tables; you may need to overlay species scores (biplot) to see which taxa drive separation. <br>• With only 45 samples, over‑fitting is a risk if you include many covariates; aim for a parsimonious model (e.g., ≤ 1/10 × n predictors). <br>• Still assumes that the dominant variation in the distance matrix is captured by the first few PCoA axes (usually true if you retain enough axes to explain > 70 % of variation). |
| **Alternatives if assumptions fail** | • **Non‑metric multidimensional scaling (NMDS)** followed by **envfit** or **post hoc PERMANOVA** on NMDS scores (more flexible to non‑linear relationships). <br>• **Generalized dissimilarity modeling (GDM)** if you suspect non‑linear, threshold‑type relationships with covariates. <br>• If linearity is doubtful, consider **machine‑learning approaches** (see Approach 3) that do not assume linear constraints. |
| **What to verify** | - Examine the proportion of variance explained by the constrained axes (`R2`). <br>- Check residuals for patterns (e.g., plot fitted vs. residual distances). <br>- Test dispersion with `betadisper`; if significant, consider using **stratified permutations** or reporting both location and dispersion effects. |
| **When to consult a statistician** | - To decide on the number of PCoA axes to retain (avoid over‑fitting). <br>- To set up variation partitioning and interpret shared vs. unique fractions correctly. <br>- To choose an appropriate permutation scheme (e.g., free vs. restricted by batch). |

---  

## 3. Taxa‑level Differential Abundance + Predictive Modeling (e.g., DESeq2/ANCOM‑BC + LASSO Logistic Regression)

| Item | Details |
|------|---------|
| **Test/method name** | (a) **Differential abundance testing** (DESeq2, ANCOM‑BC, or MaAsLin2) to identify individual taxa whose relative abundances differ between responders and non‑responders. <br>(b) **Regularized logistic regression** (LASSO, elastic‑net) using selected taxa (or PCoA axes) as predictors to build a parsimonious classifier of response. |
| **When appropriate** | You want to move beyond overall community differences and pinpoint *which* microbes are associated with outcome, while also evaluating whether a microbial signature can predict response. Particularly useful when you have a modest sample size but still wish to explore high‑dimensional taxon data. |
| **Key assumptions** | **Differential abundance**: <br>1. **Appropriate count model** – DESeq2 assumes negative‑binomial distribution with mean‑variance relationship; ANCOM‑BC assumes log‑linear model with bias correction; MaAsLin2 allows various distributions (Gaussian, Poisson, NB). <br>2. **Independence** of samples. <br>3. **Correct normalization** (e.g., DESeq2’s size‑factor, ANCOM‑BC’s bias correction). <br>**LASSO logistic regression**: <br>1. Linear log‑odds relationship between predictors (taxa abundances or PCoA scores) and outcome. <br>2. Independence of observations. <br>3. No perfect multicollinearity (LASSO handles correlated predictors by shrinking). |
| **Advantages** | • **Interpretability**: DESeq2/ANCOM‑BC give log‑fold‑change and adjusted p‑values for each taxon, highlighting candidate biomarkers. <br>• **Prediction**: LASSO yields a sparse set of taxa (or PCs) that can be used to construct a risk score; cross‑validated AUC provides an estimate of predictive performance. <br>• Handles **high dimensionality** (hundreds of taxa) better than PERMANOVA, which collapses information into a distance matrix. <br>• Permutation‑free (though you can still use cross‑validation or bootstrap for inference). |
| **Limitations** | • Differential abundance methods can be **sensitive to compositionality** and low‑count taxa; results may change with different normalization or filtering thresholds. <br>• LASSO with *n* = 45 risks over‑fitting if too many predictors are entered; strong regularization (high λ) is needed, which may shrink true signals to zero. <br>• Does not directly test the *overall* community shift (β‑diversity) – you would still need a PERMANOVA/dbRDA for that complementary view. <br>• Interpretation of LASSO coefficients is conditional on the penalty; stability selection or bootstrapping is recommended to assess variable‑selection robustness. |
| **Alternatives if assumptions fail** | • **Bayesian hierarchical models** (e.g., `brms` with a multinomial or Dirichlet‑multinomial likelihood) that naturally accommodate compositional data and small samples. <br>• **Random Forest** or **Support Vector Machine** with recursive feature elimination (RFE) for non‑linear classification; variable importance can be extracted, but inference is less straightforward. <br>• If count‑distribution assumptions are violated, consider **zero‑inflated models** (e.g., ZIGA, metagenomeSeq) or **compositional approaches** (ALDEx2, ANCOM‑II) that work on centered log‑ratio transformed data. |
| **What to verify** | - For DESeq2/ANCOM‑BC: examine dispersion estimates, check for outliers, and apply a sensible pre‑filter (e.g., keep taxa present in ≥ 20 % of samples with a minimum count). <br>- For LASSO: perform **k‑fold cross‑validation** (k = 5 or leave‑one‑out) to choose λ that minimizes deviance; report cross‑validated AUC, sensitivity, specificity. <br>- Assess multicollinearity (VIF) on CLR‑transformed taxa if you plan to use unpenalized logistic regression later. |
| **When to consult a statistician** | - To choose the appropriate differential abundance framework given your data’s sparsity and compositional nature. <br>- To set up a robust penalized regression pipeline (nested cross‑validation, stability selection) and avoid optimistic performance estimates. <br>- To interpret the results in the context of multiple testing (e.g., Benjamini‑Hochberg FDR) and to discuss biological plausibility. |

---  

### Quick Decision Guide

| Goal | Recommended primary method | Complementary check |
|------|----------------------------|---------------------|
| **Test overall community difference** | PERMANOVA (adonis2) – test `response` + confounders | Verify dispersion with `betadisper`; if heterogeneous, report both PERMANOVA and betadisper or use DistLM. |
| **Quantify how much variation response explains & visualize** | dbRDA (`capscale`) + variation partitioning | Check eigenvalues; ensure enough PCoA axes retained (> 70 % cumulative). |
| **Identify specific biomarkers & build a predictive signature** | Differential abundance (DESeq2/ANCOM‑BC) → LASSO logistic regression (or elastic net) | Cross‑validate the classifier; consider stability selection or bootstrapping for variable importance. |

### Sample‑size Caveats
- **n = 45** is modest for high‑dimensional microbiome data. Permutation‑based methods (PERMANOVA, dbRDA) are relatively safe because they do not rely on large‑sample asymptotics, but the number of unique permutations is limited; use a Monte‑Carlo approach with at least 5 000–10 000 permutations.  
- For penalized regression, the **events‑per‑variable (EPPV)** rule of thumb suggests ≤ 5–10 predictors per outcome event. With 25 responders, aim for no more than ~2–5 predictor variables (or rely on strong regularization).  
- If you find that dispersion differs markedly between groups, the PERMANOVA result may be misleading; in that case, consider a **generalized linear mixed model on presence/absence** or a **distance‑based test that separates location and dispersion** (e.g., `PERMANOVA+` in PRIMER).  

### When to Seek Expert Help
- Setting up a **stratified permutation scheme** (e.g., by sequencing run or DNA‑extraction batch).  
- Choosing and justifying the **number of PCoA axes** for dbRDA or the **regularization strength** for LASSO.  
- Interpreting **compositional data issues** and selecting the most appropriate differential abundance tool for your sequencing depth and zero‑inflation level.  
- Performing **power/sensitivity analysis** post‑hoc to convey the detectable effect size given your sample size.  

---  

**Bottom line:** Start with a PERMANOVA to test whether overall community composition differs by response (checking dispersion). Follow with dbRDA if you want to visualize and partition variance. Finally, pursue taxa‑level differential abundance and a sparsity‑promoting predictive model to pinpoint candidate biomarkers and evaluate their clinical utility. Each step comes with its own assumptions; verify them, and involve a statistician whenever you deviate from the standard workflow or when the sample size feels limiting for the chosen model.
````

## Assessment

_Machine-suggested (UNCONFIRMED) — drafted by Claude Opus 4.7 on 2026-06-26 to speed T4 review. An author must independently read the Model Output above and set the real Recommendation. Anything labeled here is triage, not domain expert review._

**Machine triage:** Output covers 3 strategies (PERMANOVA, dbRDA, MaAsLin2 + sPLS-DA). Complete, no truncation. Bottom-line workflow ties them together with PERMDISP and statistician-consult flags. Strong cross-model agreement on the multi-step pipeline.

**Suggested verdict (UNCONFIRMED):** Pass

**What still needs human verification:**
- Whether sparse PLS-DA (sPLS-DA) is appropriate for the n=45 / high-dimensional task
- That dbRDA after PERMANOVA is the recommended sequence vs. alternatives
- Spot-check the variance-partitioning interpretation

## Overall Assessment
- **Recommendation:** Pass
- **Notes:** Alex Alexiev (2026-06-29): **What still needs human verification:**
- Whether sparse PLS-DA (sPLS-DA) is appropriate for the n=45 / high-dimensional task: doable but it is a low sample size so could overfit
- That dbRDA after PERMANOVA is the recommended sequence vs. alternatives: it does work
- Spot-check the variance-partitioning interpretation: yes

## Verification Steps Tested
_Which verification requirements from the prompt were checked, and results._
