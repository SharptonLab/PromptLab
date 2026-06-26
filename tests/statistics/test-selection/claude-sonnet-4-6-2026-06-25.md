# Test Results: statistics/test-selection.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-25.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** statistics/test-selection.md
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
# Statistical Approaches for Gut Microbiome Beta Diversity and Immunotherapy Response

---

## Preliminary Note on Sample Size

**Your n=45 is small for microbiome research, and this matters throughout every analysis below.** With 25 responders and 20 non-responders, you have limited statistical power, and results should be interpreted cautiously and treated as exploratory/hypothesis-generating rather than confirmatory. This is worth stating explicitly in any manuscript. I flag specific consequences for each method below.

---

## Approach 1: PERMANOVA (Permutational Multivariate Analysis of Variance)

### Test/Method Name
PERMANOVA, also called adonis or adonis2 in the R `vegan` package. This is the standard first-line test for your primary question.

### When Appropriate
- You have a distance or dissimilarity matrix (Bray-Curtis fits here) and want to test whether group centroids differ
- Outcome is categorical (responder/non-responder)
- You want to account for covariates in the same model
- Sample sizes are unequal between groups (as yours are)

### Key Assumptions You Must Verify
1. **Exchangeability of observations under the null hypothesis** — observations within groups must be exchangeable, which requires independence. Your design (one sample per patient, prospective cohort) satisfies this.
2. **Homogeneity of multivariate dispersions** — this is the most commonly violated assumption and the most commonly overlooked. If responders have more variable microbiome compositions than non-responders (or vice versa), PERMANOVA can return a significant result that reflects *spread differences*, not *location differences*. You must test this separately (see below).
3. **No strong confounding structure** — if confounders (age, prior treatments) are correlated with response, a naive PERMANOVA will conflate their effects with the microbiome signal.

### How to Check Assumption 2
Run **PERMDISP** (`betadisper` in vegan) before interpreting PERMANOVA results. If PERMDISP is significant, your PERMANOVA result is ambiguous — you cannot cleanly attribute it to centroid differences alone.

### Advantages
- Non-parametric permutation-based test; makes no distributional assumptions about the data
- Handles high-dimensional compositional data naturally through the distance matrix
- Can incorporate covariates (age, sex, prior treatments, tumor stage) using partial PERMANOVA, which is important for your design
- Widely used and understood in the microbiome field; reviewers will expect it
- Permutation p-values are valid even with n=45, though power will be limited

### Limitations
- **Power is genuinely limited at n=45.** A non-significant result does not mean no association exists; you may simply be underpowered.
- Significant result is ambiguous without PERMDISP — you cannot distinguish centroid shift from dispersion difference without additional testing
- Partial PERMANOVA (with covariates) uses sequential partitioning by default in some implementations; covariate order can affect results. Use marginal testing (`by = "margin"` in adonis2) to avoid this.
- Does not tell you *which* taxa drive the difference — it is a global community-level test only

### Alternatives If Assumptions Aren't Met
- If PERMDISP is significant: report both results transparently and consider ANOSIM as a complementary test, though ANOSIM has its own sensitivity to dispersion
- If observations are not independent (e.g., if patients share a clinical unit and cross-colonization is plausible): consult a statistician about permutation schemes that respect clustering

---

## Approach 2: PCoA Visualization + Multivariate Dispersion Testing (PERMDISP)

### Test/Method Name
Principal Coordinates Analysis (PCoA) for visualization, combined with PERMDISP (`betadisper`) for formal dispersion testing. This is not a standalone inferential approach but is an essential companion to PERMANOVA.

### When Appropriate
- Always, as a complement to PERMANOVA
- Particularly important when you want to understand *how* communities differ, not just *whether* they differ
- Useful for identifying outliers that could disproportionately influence results at small n

### Key Assumptions
- PCoA is a visualization tool; it has no inferential assumptions per se
- PERMDISP assumes exchangeability (same as PERMANOVA)

### Advantages
- PCoA plots allow you to visually assess whether groups separate, whether there are outliers, and whether the signal looks biologically plausible before running formal tests
- **At n=45, outlier detection is especially important** — a single patient with an unusual microbiome can substantially influence distance-based analyses
- PERMDISP formally tests whether the assumption of equal dispersion holds, which is required for clean PERMANOVA interpretation
- Helps communicate results to clinical collaborators who may not be familiar with multivariate statistics

### Limitations
- PCoA captures only a fraction of total variance in the first few axes; visual separation (or lack thereof) can be misleading
- Does not provide a p-value for group differences on its own
- PERMDISP tests a different hypothesis than PERMANOVA; a significant PERMDISP result complicates but does not invalidate your analysis

### Alternatives
- NMDS (Non-metric Multidimensional Scaling) as an alternative ordination that may better preserve rank-order distances, though it is harder to interpret quantitatively

---

## Approach 3: Differential Abundance Testing for Specific Taxa

### Test/Method Name
This is a family of methods rather than a single test. Appropriate options include:
- **DESeq2** (originally for RNA-seq, widely adapted for microbiome)
- **MaAsLin2** (Multivariate Association with Linear Models; handles covariates well)
- **ANCOM-BC2** (Analysis of Compositions of Microbiomes with Bias Correction)
- **Wilcoxon rank-sum test with FDR correction** (simpler, more transparent)

### When Appropriate
- You want to identify *which specific taxa* are associated with response, not just whether communities differ overall
- This addresses your second stated goal directly
- Should be run after (and motivated by) a significant or suggestive PERMANOVA result, though some researchers run it regardless

### Key Assumptions (Vary by Method)
1. **Compositionality** — microbiome count data are compositional (relative abundances sum to a constant). Methods that ignore this (naive t-tests on raw counts) can produce spurious results. DESeq2, ANCOM-BC2, and MaAsLin2 all handle this to varying degrees.
2. **Sparsity** — many taxa will have zero counts in many samples. Methods must handle zero inflation. Filter low-prevalence taxa (e.g., present in <10% of samples) before analysis.
3. **Multiple comparisons** — you may test hundreds of taxa simultaneously. FDR correction (Benjamini-Hochberg) is standard, but with n=45, you will have very limited power to survive FDR correction. **Expect few or no taxa to reach FDR < 0.05**, and consider reporting nominal p-values with explicit acknowledgment of the exploratory nature.
4. **Covariate adjustment** — MaAsLin2 handles covariates most naturally among these options and is a reasonable default for your design.

### Advantages
- Provides actionable biological hypotheses about specific organisms
- MaAsLin2 in particular handles your covariates (age, sex, prior treatments, tumor stage) within the same model
- Results are more interpretable to clinical collaborators than community-level tests
- Can be run at multiple taxonomic levels (genus, family, phylum) to identify signals at different resolutions

### Limitations
- **Multiple testing burden is severe.** If you test 200 genera, you expect 10 false positives at α=0.05 by chance alone. With n=45, power to detect true positives after FDR correction is very low.
- Different methods can give substantially different results on the same dataset. Running two methods (e.g., MaAsLin2 and ANCOM-BC2) and reporting only concordant findings is a reasonable strategy.
- Normalization choices (rarefaction, TSS, CLR) affect results and remain contested in the field
- **This analysis is almost certainly underpowered for confirmatory inference at n=45.** Frame findings as hypothesis-generating.

### Alternatives If Assumptions Aren't Met
- If zero inflation is extreme: consider zero-inflated models or filtering more aggressively
- If you want a non-parametric option with fewer assumptions: Wilcoxon rank-sum with FDR correction is less powerful but more transparent and harder to criticize methodologically
- **Consult a statistician** if you plan to use these results as primary evidence rather than exploratory findings

---

## Approach 4: Machine Learning-Based Classification (e.g., Random Forest)

### Test/Method Name
Random Forest classifier with cross-validation, used to assess predictive accuracy and identify important features (taxa). This is more complex and should be considered secondary to the approaches above.

### When Appropriate
- You want to assess whether microbiome composition has *predictive* value for response, not just association
- You are interested in identifying a panel of taxa that together discriminate groups
- You have reason to believe the signal is multivariate and not captured by individual taxa tests

### Key Assumptions
1. **Sample size is the critical constraint here.** With n=45, cross-validation estimates of predictive accuracy will have very wide confidence intervals. Leave-one-out cross-validation (LOOCV) is preferable to k-fold at this sample size, but results should still be interpreted with extreme caution.
2. **No data leakage** — feature selection and any preprocessing must occur *within* each cross-validation fold, not before. This is a common and consequential error in microbiome ML papers.
3. **Class imbalance** — your 25/20 split is mild and manageable, but should be accounted for in model evaluation (use balanced accuracy or AUC, not raw accuracy).

### Advantages
- Captures non-linear relationships and interactions between taxa that univariate tests miss
- Variable importance scores provide a ranked list of potentially relevant taxa
- AUC from cross-validation gives an intuitive summary of predictive performance
- Can handle high-dimensional data (many taxa relative to samples) better than logistic regression

### Limitations
- **n=45 is genuinely too small for reliable ML-based inference.** AUC estimates from LOOCV at this sample size will have 95% confidence intervals spanning roughly ±0.15–0.20, making it difficult to distinguish a useful classifier from chance.
- Variable importance scores are not equivalent to statistical significance; they do not come with p-values or confidence intervals in standard implementations
- Results are difficult to interpret mechanistically
- High risk of overfitting and inflated performance estimates if cross-validation is not implemented correctly
- Reviewers in clinical journals may be skeptical of ML approaches at this sample size

### Alternatives
- Penalized logistic regression (LASSO or elastic net on CLR-transformed taxa) is a more interpretable alternative that also handles high dimensionality
- **Strongly recommend consulting a statistician before pursuing this approach** given the sample size constraints and the technical pitfalls

---

## Summary Recommendation Table

| Approach | Primary Question Addressed | Complexity | Recommended for Your Study? |
|---|---|---|---|
| PERMANOVA + PERMDISP | Do communities differ overall? | Low–Medium | **Yes, as primary analysis** |
| PCoA visualization | How do communities differ? | Low | **Yes, always** |
| Differential abundance (MaAsLin2) | Which taxa differ? | Medium | **Yes, as secondary/exploratory** |
| Random Forest | Can microbiome predict response? | High | **Optional; frame as exploratory** |

---

## Cross-Cutting Recommendations

**On reporting:** Pre-register your analysis plan if possible, or clearly distinguish confirmatory from exploratory analyses in your manuscript. With n=45, almost everything is exploratory.

**On covariates:** Age, prior treatments, and tumor stage are plausible confounders that could drive microbiome differences independently of treatment response. Include them in PERMANOVA (partial) and MaAsLin2 models. Do not ignore them.

**On multiple distance metrics:** Bray-Curtis is appropriate and standard, but consider also running analyses with unweighted UniFrac (if phylogenetic data are available) to assess whether rare taxa or phylogenetic structure tell a different story.

**On consulting a statistician:** I would recommend this specifically if (1) you plan to use differential abundance results as primary evidence in a clinical claim, (2) you pursue the machine learning approach, or (3) PERMDISP is significant and you are unsure how to interpret the PERMANOVA result. The sample size limitations here make careful statistical guidance particularly valuable.
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
