# Test Results: statistics/test-selection.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-23.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** statistics/test-selection.md
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
# Statistical Approaches for Gut Microbiome Beta Diversity and Immunotherapy Response

## Preliminary Notes on Your Data

**Your sample size (n=45) is small for microbiome research.** This affects statistical power, the reliability of distance-based permutation tests, and especially any taxon-level analyses. Results should be treated as exploratory/hypothesis-generating rather than confirmatory. Be transparent about this limitation in any publication.

**Your analysis has two distinct questions** that require different methods:
- **Question 1:** Do microbial *communities* differ between responders and non-responders? (beta diversity level)
- **Question 2:** Which specific *taxa* are associated with response? (taxon level)

These are addressed separately below.

---

## Question 1: Community-Level Beta Diversity Analysis

---

### Option 1: PERMANOVA (Permutational Multivariate Analysis of Variance)

**Also known as:** adonis2 in the R `vegan` package; McArdo's PERMANOVA

**1. Test/Method Name**
PERMANOVA tests whether the centroids (and dispersion) of groups in multivariate distance space differ more than expected by chance, using permutation rather than distributional assumptions.

**2. When Appropriate**
- You have a distance/dissimilarity matrix (Bray-Curtis fits here)
- You want to test group differences in overall community composition
- You have a categorical grouping variable (responder/non-responder)
- You want to include covariates (age, sex, prior treatment, stage)

**3. Key Assumptions**
- ⚠️ **Exchangeability under the null:** Observations must be exchangeable between groups if H₀ is true; violated if groups differ in variance (dispersion), not just location
- **Independence of samples:** Met here (one sample per patient)
- **Sufficient permutations:** With n=45, you can generate ~10,000 permutations; adequate but not generous
- **Balanced or near-balanced groups:** Your 25/20 split is acceptable

**4. Advantages**
- Works directly on any distance matrix — no distributional assumptions about the data
- Handles covariates (partial PERMANOVA): you can control for age, sex, stage, prior treatment
- Widely used and accepted in microbiome literature
- Interpretable R² effect size (proportion of variance explained)

**5. Limitations**
- ⚠️ **Sensitive to heterogeneous dispersion:** If responders have more variable microbiomes than non-responders (or vice versa), PERMANOVA may detect dispersion differences, not location differences — this is a real concern in microbiome data
- With n=45, power to detect modest effects is limited; small R² values may be non-significant even if real
- Covariates are handled sequentially (order matters in adonis2 unless using `by="margin"`)
- Does not tell you *which* taxa drive the difference

**6. Alternatives if Assumptions Aren't Met**
- If dispersion is heterogeneous: report PERMDISP2 results alongside PERMANOVA and interpret cautiously; consider ANOSIM (though it has its own limitations)
- If you want robustness checks: run with multiple distance metrics (unweighted UniFrac, weighted UniFrac if phylogenetic data available)

**⚠️ Critical Step:** Always run **PERMDISP2** (`betadisper` in vegan) alongside PERMANOVA to test whether groups differ in *dispersion*. Report both results. If PERMDISP2 is significant, your PERMANOVA result is ambiguous.

---

### Option 2: PERMDISP2 (Permutational Analysis of Multivariate Dispersions)

**1. Test/Method Name**
Tests whether groups differ in *within-group variability* (dispersion around group centroid) in distance space.

**2. When Appropriate**
- Run as a **companion to PERMANOVA**, not a replacement
- Specifically tests the assumption that PERMANOVA requires (homogeneous dispersion)
- Also scientifically interesting: do responders have more "diverse" community structures?

**3. Key Assumptions**
- Same exchangeability assumption as PERMANOVA
- Requires a distance matrix

**4. Advantages**
- Directly tests the homogeneity assumption for PERMANOVA
- Scientifically meaningful on its own: heterogeneous dispersion in non-responders could indicate ecological instability
- Simple to implement alongside PERMANOVA

**5. Limitations**
- Does not test for differences in community composition (centroid location)
- With n=45, power to detect dispersion differences is modest

**6. Recommendation**
Run this as a required diagnostic step, not optional.

---

### Option 3: ANOSIM (Analysis of Similarities)

**1. Test/Method Name**
Rank-based test comparing within-group to between-group dissimilarities.

**2. When Appropriate**
- Alternative or complement to PERMANOVA
- When you want a rank-based approach less sensitive to outliers

**3. Key Assumptions**
- Independence of samples
- Exchangeability under H₀

**4. Advantages**
- Rank-based: robust to outliers in the distance matrix
- Simple R statistic (ranges -1 to 1; >0.25 often considered meaningful)
- Less sensitive to dispersion differences than PERMANOVA

**5. Limitations**
- ⚠️ Less powerful than PERMANOVA in most simulation studies
- Cannot easily incorporate covariates/confounders — a significant problem given your confounders
- R statistic is not a clean effect size
- Generally considered inferior to PERMANOVA for most applications

**6. Recommendation**
Use as a sensitivity check only. **Do not use as your primary test** given the need to control for confounders.

---

### Recommended Workflow for Question 1

```
1. Compute Bray-Curtis distance matrix
2. Run PERMDISP2 → report result
3. Run PERMANOVA with covariates (partial PERMANOVA)
   - Include: age, sex, prior treatment, tumor stage as covariates
   - Use by="margin" for Type III-style testing
4. Visualize with PCoA/NMDS ordination, color by response
5. Report R², p-value, and number of permutations
6. Sensitivity: repeat with alternative distance metric
```

---

## Question 2: Taxon-Level Differential Abundance Analysis

This is a **separate and more complex problem.** You are now testing potentially hundreds of taxa simultaneously with n=45, which creates serious multiple testing and power concerns.

---

### Option A: DESeq2 (Negative Binomial Model)

**1. Test/Method Name**
Originally developed for RNA-seq; widely adapted for microbiome count data. Models raw counts with a negative binomial distribution, with variance shrinkage estimation.

**2. When Appropriate**
- Raw count data (OTU/ASV table before rarefaction)
- You want to test each taxon for differential abundance between groups
- Sample sizes are small (shrinkage estimation helps)

**3. Key Assumptions**
- Count data (integers), not rarefied proportions
- Negative binomial distribution for counts
- ⚠️ Assumes most taxa are *not* differentially abundant (used for normalization) — may be violated in microbiome data with large compositional shifts
- Independence of samples

**4. Advantages**
- Shrinkage of variance estimates helps with small n
- Handles overdispersion (common in microbiome counts)
- Produces fold-change estimates with confidence intervals
- Well-documented, widely used

**5. Limitations**
- ⚠️ Normalization assumption (most taxa unchanged) may not hold
- Has been shown to have elevated false positive rates in some microbiome simulation studies
- Does not account for compositionality (taxa are not independent — they sum to a constant)
- With n=45 and hundreds of taxa, power per taxon is very low after multiple testing correction

**6. Alternatives**
- ANCOM-BC2, MaAsLin2 (see below)

---

### Option B: ANCOM-BC2 (Analysis of Compositions of Microbiomes with Bias Correction, version 2)

**1. Test/Method Name**
Compositionally-aware differential abundance method that explicitly accounts for the fact that microbiome data are compositional (relative, not absolute).

**2. When Appropriate**
- Microbiome relative abundance or count data
- You want to account for compositionality
- You have covariates to include
- Current (2023+) best-practice recommendation for many microbiome studies

**3. Key Assumptions**
- At least some taxa are truly not differentially abundant (needed for bias correction)
- Samples are independent
- Covariates are correctly specified

**4. Advantages**
- Explicitly handles compositional nature of microbiome data
- Controls FDR with better calibration than DESeq2 in simulation studies
- Handles covariates (age, sex, stage, prior treatment)
- Provides effect size estimates
- ANCOM-BC2 has improved sensitivity/specificity over original ANCOM

**5. Limitations**
- More complex to implement and interpret than DESeq2
- Still relatively new; less accumulated literature on performance across all scenarios
- With n=45, power remains limited regardless of method

**6. Recommendation**
This is currently among the better-supported methods for microbiome differential abundance. Consider as primary method.

---

### Option C: MaAsLin2 (Multivariable Association with Linear Models)

**1. Test/Method Name**
Multivariate linear model framework for microbiome associations, with multiple normalization and transformation options.

**2. When Appropriate**
- You have multiple covariates to control simultaneously
- You want a flexible, well-documented framework
- You want to test associations at multiple taxonomic levels

**3. Key Assumptions**
- Depends on chosen transformation (log, arcsin-sqrt, etc.)
- Independence of samples
- Linear relationship between transformed abundance and predictors

**4. Advantages**
- Explicitly designed for multivariable microbiome analysis
- Handles confounders directly in the model
- Flexible: works at species, genus, pathway levels
- Well-documented with clear output

**5. Limitations**
- Transformation choices affect results; no single "correct" choice
- Linear models on compositional data have theoretical limitations
- With n=45, many taxa will be underpowered

**6. Recommendation**
Excellent for multivariable analysis. Consider running alongside ANCOM-BC2 as a sensitivity check.

---

### Multiple Testing: A Critical Warning

> ⚠️ **With n=45 and potentially hundreds of taxa, taxon-level analysis is severely underpowered after FDR correction.** You should expect many false negatives (missed associations) and some false positives. Any taxon-level findings should be explicitly labeled as **hypothesis-generating** and require validation in an independent cohort.

**Minimum requirements:**
- Apply FDR correction (Benjamini-Hochberg) — do not use uncorrected p-values
- Report effect sizes, not just p-values
- Consider restricting analysis to taxa present in >20-30% of samples to reduce burden
- Pre-register your analysis plan if possible

---

## Summary Recommendation Table

| Question | Primary Method | Companion/Sensitivity | Key Output |
|---|---|---|---|
| Community-level difference | PERMANOVA (partial, with covariates) | PERMDISP2, ANOSIM | R², p-value |
| Dispersion difference | PERMDISP2 | — | F-statistic, p-value |
| Taxon-level associations | ANCOM-BC2 | MaAsLin2 | Log fold-change, FDR q-value |
| Visualization | PCoA/NMDS ordination | — | Plot colored by response |

---

## When to Consult a Biostatistician

**You should consult a statistician or bioinformatician with microbiome expertise if:**

- [ ] You are unsure how to handle the compositional nature of microbiome data
- [ ] You want to combine beta diversity results with taxon-level findings in a single model
- [ ] You are considering rarefaction vs. alternative normalization strategies (this is an active methodological debate)
- [ ] You want to perform any machine learning or predictive modeling (e.g., random forest for biomarker discovery) — n=45 makes this especially risky without careful cross-validation
- [ ] You plan to submit to a high-impact journal where methods will be scrutinized
- [ ] You want to perform phylogenetic analyses (UniFrac distances, phylogenetic regression)

**Given your sample size and the clinical stakes of immunotherapy research, consultation is strongly recommended.**

---

## Honest Assessment of Your Study's Limitations

| Limitation | Impact | Mitigation |
|---|---|---|
| n=45 | Low power for taxon-level analysis; PERMANOVA may miss modest community differences | Frame as exploratory; seek replication cohort |
| Binary outcome | Loss of information vs. continuous response metrics | Consider also analyzing with continuous outcomes (e.g., % tumor reduction) if available |
| Unbalanced groups (25/20) | Minor; acceptable for PERMANOVA | Report group sizes clearly |
| Multiple confounders with small n | Covariate adjustment reduces effective sample size | Prioritize most important confounders; avoid over-adjustment |
| Single time point | Cannot assess microbiome dynamics | Acknowledge as limitation |
```

## Overall Assessment
- **Recommendation:** Pass
- **Notes:**
## Verification Steps Tested
_Which verification requirements from the prompt were checked, and results._
