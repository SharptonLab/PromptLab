# Test Results: test-selection.md

## Test Metadata
- **Prompt:** statistics/test-selection.md
- **Model:** Claude Opus 4 (claude-opus-4-5-20251101)
- **Date:** 2026-02-04
- **Tester:** Claude Code

## Test Input Used

Standard test input from prompt file:

```
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

### Statistical Approaches for Microbiome-Immunotherapy Response Association

Your research question has two components: (1) testing whether overall community composition differs between responders and non-responders, and (2) identifying specific taxa associated with response. These require different approaches.

---

## Part 1: Community-Level Testing (Beta Diversity)

### Option 1: PERMANOVA (Permutational Multivariate Analysis of Variance)

**Test name:** PERMANOVA, implemented as `adonis2()` in R's vegan package

**When appropriate:**
- Testing whether group centroids differ in multivariate space
- When you have a distance matrix (like your Bray-Curtis matrix)
- For ecological community data where traditional parametric assumptions don't hold
- When you want to include covariates in the model

**Key assumptions:**
1. **Homogeneity of dispersions**: Groups should have similar spread (multivariate variance)
2. **Independence of observations**: Your one-sample-per-patient design satisfies this
3. **Exchangeability under the null hypothesis**: Observations are exchangeable when groups are equivalent

**Advantages:**
- Non-parametric; no assumptions about underlying distribution
- Handles the distance matrix directly
- Can include covariates (age, sex, stage, prior treatment)
- Well-established in microbiome research; reviewers will recognize it
- Robust to many types of data

**Limitations:**
- **Sensitive to dispersion differences**: A significant result could mean groups differ in location, dispersion, or both. With your observed data, always check this.
- **Small sample size**: With n=45 (25 vs 20), power may be limited for detecting moderate effects
- **Multiple covariates consume degrees of freedom**: Adding all four confounders reduces power further
- **Permutation-based p-values**: With small n and many covariates, permutation space may be limited

**Implementation:**
```r
library(vegan)

# Basic model
adonis2(distance_matrix ~ response, data = metadata, permutations = 9999)

# With covariates (order matters for sequential tests)
adonis2(distance_matrix ~ age + sex + stage + prior_treatment + response,
        data = metadata, permutations = 9999, by = "margin")
```

**Important:** Always run `betadisper()` to check dispersion homogeneity before interpreting PERMANOVA.

---

### Option 2: ANOSIM (Analysis of Similarities)

**Test name:** ANOSIM, available via `anosim()` in vegan

**When appropriate:**
- Simple two-group comparison without covariates
- When you want a measure of effect size (R statistic)
- As a complement to PERMANOVA

**Key assumptions:**
- Similar to PERMANOVA but cannot accommodate covariates
- Assumes groups have similar dispersion

**Advantages:**
- Simple, intuitive R statistic (ranges from -1 to 1)
- Well-established in ecological literature

**Limitations:**
- **Cannot adjust for confounders**: This is a significant limitation given your potential confounders
- Less powerful than PERMANOVA in many scenarios
- More sensitive to dispersion heterogeneity than PERMANOVA
- Not recommended as sole analysis for clinical data with confounders

**Recommendation:** Use PERMANOVA as primary analysis; ANOSIM could supplement if you want to report the R statistic for effect size interpretation.

---

### Option 3: Distance-Based Redundancy Analysis (db-RDA)

**Test name:** db-RDA via `dbrda()` or `capscale()` in vegan

**When appropriate:**
- When you want to partition variance explained by response vs. confounders
- When you're interested in visualizing the constrained ordination
- For exploratory analysis of which variables structure the community

**Key assumptions:**
- Similar to PERMANOVA
- Assumes linear relationships between predictors and ordination axes

**Advantages:**
- Provides variance partitioning (how much variation explained by response vs. confounders)
- Produces ordination plot showing constrained axes
- Can formally test individual terms

**Limitations:**
- More complex to interpret
- With small n and many predictors, may overfit
- Variance partitioning with confounded predictors requires careful interpretation

---

## Part 2: Taxon-Level Analysis (Differential Abundance)

### Option 4: Differential Abundance Testing

**Test name:** Multiple methods available; recommended: DESeq2, ANCOM-BC, or MaAsLin2

**When appropriate:**
- Identifying which specific taxa differ between groups
- When you want to adjust for confounders at the taxon level

**Key assumptions (vary by method):**
- DESeq2: Negative binomial distribution of counts; appropriate normalization
- ANCOM-BC: Compositional nature of data is accounted for
- MaAsLin2: Various distributional assumptions depending on settings

**Advantages:**
- Directly identifies which taxa are associated with response
- MaAsLin2 specifically designed for microbiome data with covariates
- ANCOM-BC handles compositional nature explicitly

**Limitations:**
- **Multiple testing burden**: With hundreds of taxa, multiple comparison correction (FDR) is essential
- **Small sample size is problematic**: With n=45, you have limited power to detect individual taxa, and many results may be false positives even after correction
- **Compositionality issues**: Relative abundance data is compositional; methods handle this differently
- **Effect sizes may be inflated**: Small samples produce unreliable effect size estimates

**Recommendation:** Use MaAsLin2 or ANCOM-BC as primary. Filter to taxa present in at least 10-20% of samples before testing. Report FDR-adjusted p-values and be conservative in interpretation.

```r
# MaAsLin2 example
library(Maaslin2)
Maaslin2(
  input_data = taxa_table,
  input_metadata = metadata,
  output = "maaslin2_output",
  fixed_effects = c("response", "age", "sex", "stage", "prior_treatment"),
  reference = c("response,non_responder")
)
```

---

## Summary and Recommendations

| Analysis Goal | Recommended Method | Alternative | Key Concern |
|--------------|-------------------|-------------|-------------|
| Community-level difference | PERMANOVA (adonis2) | db-RDA | Check dispersion homogeneity |
| Effect size (community) | ANOSIM R statistic | PERMANOVA R-squared | Limited interpretability |
| Individual taxa | MaAsLin2 or ANCOM-BC | DESeq2 | Multiple testing, small n |

### Sample Size Concerns

Your sample size (n=45) is workable but limited:
- For PERMANOVA: Adequate for detecting moderate-to-large effects; may miss subtle differences
- For differential abundance: Underpowered for detecting all but the strongest associations; interpret taxon-level results as hypothesis-generating, not confirmatory
- Power decreases when adding multiple covariates

### Recommendations for Your Analysis

1. **Primary analysis:** PERMANOVA with covariates, testing response effect
2. **Check assumptions:** Run betadisper() before PERMANOVA
3. **Visualize:** PCoA plots colored by response, with confidence ellipses
4. **Secondary analysis:** MaAsLin2 or ANCOM-BC for individual taxa, with FDR correction
5. **Be conservative:** Given small n, frame taxon-level results as exploratory

### Consult a Statistician If:

- PERMANOVA is significant but betadisper is also significant (dispersion differs)
- You want to run formal power analysis
- Results differ substantially between PERMANOVA and taxon-level analyses
- You plan to build a predictive model (classifier) from these data—different considerations apply
- You want to combine multiple outcomes (clinical response + microbiome + other biomarkers)

### Questions to Consider

1. **How were responders vs. non-responders defined?** RECIST criteria have categories (CR, PR, SD, PD)—did you dichotomize? Consider whether response should be ordinal.
2. **Are confounders balanced between groups?** Check for confounding before including in models.
3. **Is this discovery or validation?** With n=45, results should be framed as discovery requiring validation in an independent cohort.
4. **Will you report effect sizes?** Beyond p-values, report R-squared (variance explained) and individual effect sizes where possible.

---

## Caution for Clinical Interpretation

This is a clinical study with potential treatment implications. Statistical significance does not equal clinical utility. If you identify microbiome signatures associated with response, validation in an independent cohort is essential before any clinical application. The small sample size means effect estimates are likely unstable, and there is meaningful risk of false positive associations, especially at the taxon level.

## Overall Assessment

- **Recommendation:** Pass
- **Notes:**
  - Output correctly identified PERMANOVA as appropriate for distance matrix comparison
  - Small sample size limitations appropriately acknowledged throughout
  - Multiple approaches provided with clear trade-offs
  - Appropriate caution about clinical study implications included
  - Confound adjustment options discussed for both community and taxon-level analyses
  - Multiple testing concerns raised for taxon-level analysis
  - The output would be valuable for a researcher in this situation

## Verification Steps Tested

| Verification Requirement | Result |
|-------------------------|--------|
| PERMANOVA correctly identified as appropriate for distance matrix comparison | Confirmed |
| Limitations of small n acknowledged | Confirmed (multiple mentions) |
| Multiple approaches provided, not just one "answer" | Confirmed (4 approaches) |
| Appropriate caution about clinical implications | Confirmed (dedicated section) |
| betadisper mentioned for dispersion checking | Confirmed |
| Multiple testing correction mentioned for taxon analysis | Confirmed |
| Confound adjustment options discussed | Confirmed (both PERMANOVA and MaAsLin2) |
