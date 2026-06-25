# Test Results: statistics/test-selection.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-23.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** statistics/test-selection.md
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

## Model Output
```


**Suggested statistical approaches (ordered from simpler → more complex)**  

| # | Test / Method | When appropriate | Key assumptions | Advantages | Limitations | Alternatives if assumptions fail |
|---|---------------|------------------|-----------------|------------|-------------|-----------------------------------|
| **1** | **PERMANOVA (e.g., `adonis2` in vegan / `permutational multivariate analysis of variance`)** | • You have a distance/dissimilarity matrix (Bray‑Curtis) and want to test whether the centroids of two (or more) groups differ.<br>• Works with a binary outcome (responder vs. non‑responder) and can include covariates (age, sex, prior treatment, stage) as *strata* or *conditional* terms. | • Exchangeability under the null (permutations are valid).<br>• **Homogeneity of multivariate dispersion** (similar spread/variance) across groups – checked with PERMDISP (`betadisper`).<br>• Independent observations (one sample per patient). | • Directly tests the hypothesis “beta‑diversity differs between responders and non‑responders”.<br>• Handles any distance metric; no need to reduce dimensionality first.<br>• Can incorporate multiple confounders in a single model. | • Sensitive to differences in dispersion; a significant PERMANOVA may reflect heterogeneity rather than location shift.<br>• With *n* = 45 (25/20) power is modest; very small effect sizes may be missed.<br>• Permutation scheme must respect any blocking or stratification (e.g., site). | • If dispersion differs, report PERMDISP results and consider a **distance‑based test that is robust to dispersion**, such as **Mantel test** (correlating the distance matrix with a binary trait vector) or **MRPP** (Multi‑Response Permutation Procedure).<br>• Use **stratified permutations** (e.g., within sex or tumor stage) if those variables are strong confounders. |
| **2** | **Distance‑based Redundancy Analysis (dbRDA) / Constrained Ordination (CAP)** | • You want to visualise how much of the variation in Bray‑Curtis distances is explained by response status (and covariates) while also obtaining axes for downstream modelling.<br>• Useful when you plan to follow up with logistic regression on the constrained axes. | • Same as PERMANOVA (exchangeability, homogeneity of dispersion).<br>• Linear relationships between the response (binary) and the fitted canonical axes (dbRDA works with any distance metric via PCoA). | • Provides a low‑dimensional plot that shows separation of responders vs. non‑responders.<br>• Gives an R² (proportion of variance explained) that is easy to communicate.<br>• Axes can be extracted and used as predictors in regression models (see #3). | • Interpretation of axes can be less intuitive than raw taxa.<br>• Still relies on the dispersion assumption; if violated, the constrained axes may be biased.<br>• With limited sample size, over‑fitting is a risk if many covariates are entered. | • If dispersion is heterogeneous, consider **non‑metric multidimensional scaling (NMDS)** followed by **envfit** to test correlation of response with the ordination (permution‑based).<br>• Use **regularised dbRDA** (e.g., ridge penalty) when many covariates relative to *n*. |
| **3** | **Logistic regression on Principal Coordinates (PCoA) axes** (e.g., first 2–5 axes from Bray‑Curtis PCoA) | • You prefer a familiar regression framework for a binary outcome and want to adjust for confounders easily.<br>• Works when the first few PCoA axes capture a substantial proportion of the beta‑diversity variation (check scree plot). | • Independent observations.<br>• Linear log‑odds relationship between each PCoA axis and the outcome (no strong non‑linear effects).<br>• No perfect multicollinearity among predictors.<br>• Adequate events‑per‑variable (EPV) – roughly ≥10 events per predictor; with 25 responders, limit to ≤2–3 predictors unless you use penalisation. | • Directly yields odds ratios, confidence intervals, and p‑values for each axis.<br>• Easy to add covariates (age, sex, stage, prior treatment) and test interactions.<br>• Familiar to clinicians; results can be reported in a standard table. | • Reduces information to a few axes; if the true signal is spread across many higher‑order axes, power drops.<br>• Assumes linearity; may miss threshold or interaction effects.<br>• Small *n* may lead to unstable estimates; need to check EPV or use penalised logistic regression (Firth, LASSO). | • If EPV is low, use **Firth’s penalised logistic regression** (reduces bias) or **LASSO/elastic‑net** logistic regression with cross‑validation.<br>• Alternatively, treat the PCoA scores as predictors in a **random forest** or **support vector machine** for classification (see #4). |
| **4** | **Differential abundance testing of individual taxa (e.g., DESeq2, ANCOM‑BC, or LEfSe)** | • After establishing an overall beta‑diversity association, you want to pinpoint which specific microbes drive the difference.<br>• Works on raw count tables (OTU/ASV) and can adjust for confounders via model formulas. | • DESeq2: negative‑binomial distribution of counts, size‑factor normalization, independence of samples.<br>• ANCOM‑BC: bias‑corrected log‑linear model, assumes approximately normal errors after transformation.<br>• LEfSe: non‑parametric Kruskal‑Wallis + LDA; assumes independence and that features are roughly normally distributed after log‑transform (less strict). | • Provides effect sizes (log‑fold change) and taxa‑level significance, facilitating biological interpretation.<br>• Can incorporate covariates directly (e.g., `~ response + age + sex + stage`).<br>• Multiple‑testing correction (Benjamini‑Hochberg) controls false discovery rate. | • With *n* = 45, power to detect modest taxon‑level differences is limited; many taxa will be sparse (many zeros).<br>• Methods differ in assumptions; results can be method‑dependent.<br>• Compositional nature of microbiome data can induce spurious correlations if not properly addressed. | • If counts are extremely sparse, consider **presence/absence‑based tests** (e.g., Fisher’s exact test per taxon) or **Bayesian approaches** (e.g., `brms` with zero‑inflated negative binomial).<br>• Use **phylogenetic‑aware methods** (e.g., `PhyloFactor`, `TreeWAS`) to borrow information across related taxa.<br>• When unsure, consult a statistician/microbiome analyst to choose and validate the method. |

---

### How to proceed with your data (practical workflow)

1. **Explore the distance matrix**  
   * Compute Bray‑Curtis distances, run `betadisper` to check homogeneity of dispersion across responders vs. non‑responders.  
   * If dispersions are similar, proceed with PERMANOVA; if not, note the limitation and consider Mantel/MRPP as a robustness check.

2. **Overall association test**  
   * Run PERMANOVA (`adonis2(dist ~ response + age + sex + prior_treatment + stage, permutations = 9999)`).  
   * Report pseudo‑F, R², and p‑value.  
   * Complement with dbRDA to visualise constrained ordination and obtain the proportion of variance explained.

3. **Dimension reduction for regression (optional)**  
   * Perform PCoA on the Bray‑Curtis matrix; examine scree plot.  
   * Retain axes that together explain ~50‑70 % of variation (often 2–4 axes).  
   * Fit a logistic regression (or penalised version if EPV is low) with those axes plus covariates.  
   * Report odds ratios per SD change in each axis.

4. **Taxa‑level follow‑up**  
   * Normalise count data (e.g., DESeq2’s size factors) and fit `~ response + age + sex + stage`.  
   * Extract taxa with adjusted p‑value < 0.1 (or a stricter threshold) and log₂‑fold‑change > |1|.  
   * Validate key taxa with an independent method (e.g., ANCOM‑BC) or by visualising relative abundances (boxplots, ROC curves).

5. **Reporting & caveats**  
   * Explicitly state that the PERMANOVA result assumes similar dispersion; provide PERMDISP statistics.  
   * Note the modest sample size and resulting limited power; avoid over‑interpreting non‑significant taxa.  
   * If any assumption is seriously violated (e.g., strong heterogeneity of dispersion, severe sparsity), flag the need for a statistician to consider alternative models (e.g., mixed‑effects distance‑based models, Bayesian hierarchical models, or machine‑learning classifiers with proper cross‑validation).

---

### When to consult a statistician

* **Dispersion heterogeneity** – if PERMDISP shows significant differences, a statistician can help choose a robust test or adjust the permutation scheme.  
* **Low events‑per‑variable** – for logistic regression with many covariates, a statistician can advise on penalisation (Firth, LASSO) or exact methods.  
* **Multiple testing & compositionality** – microbiome‑specific corrections (e.g., ANCOM‑BC, ALDEx2) and interpretation of log‑ratios benefit from expert input.  
* **Complex modelling** – if you wish to model longitudinal changes, incorporate random effects (site, batch), or use machine‑learning classifiers, a statistician/data scientist can ensure proper validation and avoid over‑fitting.

--- 

**Bottom line:** With 45 melanoma patients, a PERMANOVA (checking dispersion) is the most straightforward way to test whether overall gut‑microbiome beta‑diversity differs between responders and non‑responders. Complementary dbRDA/PCoA‑based logistic regression offers effect‑size estimates and covariate adjustment, while differential abundance pipelines (DESeq2/ANCOM‑BC/LEfSe) let you identify candidate taxa. Always verify the underlying assumptions, report limitations, and seek statistical guidance when those assumptions are not met or when the model becomes more complex.
```

## Assessment

_Machine-suggested (UNCONFIRMED) — drafted by Claude Opus 4.7 on 2026-06-24 to speed T4 review. An author must independently read the Model Output above and set the real Recommendation. Anything labeled here is triage, not domain expert review._

**Machine triage:** Most exhaustive of the six (50 lines but 9.6K chars). Large table comparing 4 methods (PERMANOVA, dbRDA/CAP, PCoA-axis logistic regression, differential abundance) with assumptions, advantages, limitations, and alternatives if assumptions fail. Recommends Firth's penalized logistic regression for low events-per-variable — a sophisticated and correct suggestion. Mentions PhyloFactor/TreeWAS as phylogenetic-aware alternatives.

**Suggested verdict (UNCONFIRMED):** Pass

**What still needs human verification:**
- Verify PhyloFactor and TreeWAS exist as named — both are real (PhyloFactor by Washburne et al., TreeWAS in microbiome ecology) but the user should confirm relevance to their question.
- EPV (events-per-variable) framing: with 25 responders and ≤2-3 predictors recommended, this is a defensible constraint per Vittinghoff/Peduzzi guidance.
- Cross-model: see Sonnet cell.

## Overall Assessment
- **Recommendation:** PENDING AUTHOR REVIEW
- **Notes:**

## Verification Steps Tested
_Which verification requirements from the prompt were checked, and results._
