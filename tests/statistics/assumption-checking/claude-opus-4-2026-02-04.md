# Test Results: assumption-checking.md

## Test Metadata
- **Prompt:** statistics/assumption-checking.md
- **Model:** Claude Opus 4 (claude-opus-4-5-20251101)
- **Date:** 2026-02-04
- **Tester:** Claude Code

## Test Input Used

Standard test input from prompt file:

```
Context: I plan to use PERMANOVA to analyze my data. I need to verify the assumptions are met.

Analysis details:
- Test/model: PERMANOVA (adonis2 in vegan package)
- Outcome variable: Bray-Curtis distance matrix of microbiome community composition
- Predictors: Treatment group (3 levels), Time (2 levels), Treatment × Time interaction
- Sample size: 60 samples (10 per group-time combination)
- Software: R with vegan package

Data characteristics I've noticed:
- Groups have different spread on PCoA plots (dispersion looks unequal)
- One treatment group clusters more tightly than others
- Sample sizes are equal across groups
```

## Filled Prompt

```
Context: I plan to use PERMANOVA to analyze my data. I need to verify the assumptions are met.

Analysis details:
- Test/model: PERMANOVA (adonis2 in vegan package)
- Outcome variable: Bray-Curtis distance matrix of microbiome community composition
- Predictors: Treatment group (3 levels), Time (2 levels), Treatment × Time interaction
- Sample size: 60 samples (10 per group-time combination)
- Software: R with vegan package

Data characteristics I've noticed:
- Groups have different spread on PCoA plots (dispersion looks unequal)
- One treatment group clusters more tightly than others
- Sample sizes are equal across groups

Task: Provide a complete assumption-checking workflow:

1. **List all assumptions** for this test, in order of importance (which violations are most problematic)

2. **For each assumption**:
   - What it means in plain language
   - How to test it (formal tests and/or visual diagnostics)
   - How to interpret the results
   - What to do if violated (robust alternatives, transformations, or when it's okay to proceed)

3. **Code examples** for the assumption checks in R with vegan package

4. **Decision summary**: A flowchart or decision tree for how to proceed based on results

Constraints:
- Be practical—focus on violations that meaningfully affect inference
- Note when minor violations are unlikely to matter
- Acknowledge that some assumption tests have their own limitations
```

## Model Output

# PERMANOVA Assumption-Checking Workflow

## Overview

PERMANOVA (Permutational Multivariate Analysis of Variance) is a non-parametric test that compares group centroids using a distance matrix. It is more robust than parametric alternatives but still has assumptions that affect interpretation. Based on what you've noticed (unequal dispersion visible on PCoA), the dispersion assumption deserves particular attention.

---

## Assumptions Ranked by Importance

1. **Homogeneity of multivariate dispersions** — Most critical for your data
2. **Independence of observations** — Fundamental design issue
3. **Appropriate distance metric** — Affects what biological signal you test
4. **Sufficient sample size / exchangeability** — Affects permutation validity

---

## 1. Homogeneity of Multivariate Dispersions

### What It Means

Groups should have similar spread (variance) around their centroids. If one group is tightly clustered and another is diffuse, PERMANOVA can yield a significant result even if centroids are identical—it's detecting the difference in spread, not location.

**Your observation that "one treatment group clusters more tightly than others" suggests this assumption may be violated.**

### How to Test

**Primary method: betadisper() + permutest()**

`betadisper()` calculates each sample's distance to its group centroid. You then test whether these distances differ across groups using permutation (analogous to Levene's test for univariate data).

### How to Interpret

- **Non-significant permutest (p > 0.05):** Dispersion is similar enough; PERMANOVA can be interpreted as testing location differences
- **Significant permutest (p < 0.05):** Groups differ in dispersion; PERMANOVA significance could reflect location, dispersion, or both

### What to Do If Violated

1. **Report both tests:** Always report betadisper results alongside PERMANOVA
2. **Consider dispersion as a meaningful outcome:** In microbiome studies, dispersion differences often have biological meaning (community stability, dysbiosis)
3. **Use adjusted interpretation:** If PERMANOVA is significant and dispersion differs, state: "Groups differ in community structure, potentially reflecting differences in location, dispersion, or both"
4. **Alternative analyses:**
   - Analyze dispersion directly as an outcome
   - Use ANOSIM (but note: also affected by dispersion)
   - Pairwise PERMANOVA on groups with similar dispersion

### Code

```r
library(vegan)

# Load your distance matrix (already computed as Bray-Curtis)
# bray_dist <- vegdist(community_matrix, method = "bray")

# Create grouping variable for the 6 treatment-time combinations
# Or test just treatment (3 levels) or time (2 levels) separately
metadata$treatment_time <- interaction(metadata$treatment, metadata$time)

# Test dispersion homogeneity across treatment groups
disp_treatment <- betadisper(bray_dist, metadata$treatment)

# Permutation test for dispersion differences
permutest(disp_treatment, permutations = 9999)

# Visualize dispersion
plot(disp_treatment, main = "Dispersion by Treatment Group")

# Boxplot of distances to centroid
boxplot(disp_treatment, main = "Distance to Centroid by Treatment")

# If you want pairwise comparisons of dispersion
TukeyHSD(disp_treatment)

# Also check dispersion by time
disp_time <- betadisper(bray_dist, metadata$time)
permutest(disp_time, permutations = 9999)

# And by treatment × time if relevant
disp_interaction <- betadisper(bray_dist, metadata$treatment_time)
permutest(disp_interaction, permutations = 9999)
```

### Practical Notes

- With equal sample sizes (as you have), PERMANOVA is somewhat more robust to dispersion heterogeneity
- Visual inspection (PCoA with confidence ellipses) can be more informative than p-values alone
- If dispersion differences are modest and you're more interested in location, cautious interpretation is often acceptable

---

## 2. Independence of Observations

### What It Means

Each sample should be independent of other samples. Dependence structures (repeated measures from same subject, samples from same cage, spatial/temporal autocorrelation) violate independence.

### How to Test

This is primarily a design consideration, not a statistical test:

- **Do you have repeated samples from the same subjects?** (If measuring same subjects at Time 1 and Time 2, they're not independent)
- **Are samples clustered?** (Same cage, same batch, same plate)
- **Is there spatial or temporal structure?** (Samples collected in sequence)

### How to Interpret

Your design has 60 samples with Treatment (3) × Time (2) = 6 groups of 10. Key question: Are the Time 1 and Time 2 samples from the same subjects or different subjects?

- **Same subjects at both timepoints:** Observations are not independent; standard PERMANOVA may be inappropriate
- **Different subjects at each timepoint:** Observations are independent; proceed with standard PERMANOVA

### What to Do If Violated

If you have repeated measures (same subjects at Time 1 and Time 2):

1. **Restricted permutations:** Permute within subjects, not across the whole dataset
2. **Use strata argument in adonis2:** `strata = metadata$subject_id`
3. **Alternative: Analyze separately by time** then compare patterns
4. **Consider specialized methods:** PERMANOVA for repeated measures is an active research area; consult a statistician

### Code

```r
# If samples are independent (different subjects per timepoint)
adonis2(bray_dist ~ treatment * time, data = metadata, permutations = 9999)

# If samples are NOT independent (repeated measures on same subjects)
# Use strata to restrict permutations within subjects

# Create permutation structure
perm_structure <- how(nperm = 9999,
                       blocks = metadata$subject_id)  # Permute within subject

adonis2(bray_dist ~ treatment * time,
        data = metadata,
        permutations = perm_structure)

# Or, for simple stratified permutation (less flexible but simpler)
adonis2(bray_dist ~ treatment * time,
        data = metadata,
        permutations = 9999,
        strata = metadata$subject_id)
```

---

## 3. Appropriate Distance Metric

### What It Means

The distance metric should capture the biological variation you care about. Bray-Curtis is a good default for compositional data, but different metrics emphasize different aspects.

### How to Test

Not a formal test—requires biological judgment:

- **Bray-Curtis:** Emphasizes abundant taxa; ignores shared absences
- **Jaccard:** Presence/absence only; emphasizes rare taxa
- **UniFrac (weighted/unweighted):** Incorporates phylogeny; requires tree
- **Aitchison distance:** Handles compositionality explicitly; robust to zeros

### How to Interpret

For microbiome data:
- Bray-Curtis is standard and appropriate for most questions
- If you care about rare taxa, consider Jaccard
- If phylogenetic relationships matter, use UniFrac (requires phylogenetic tree)

### What to Do If Uncertain

Run sensitivity analysis: Repeat PERMANOVA with 2-3 different distance metrics. If conclusions are consistent, results are robust. If they differ, report all and discuss what each emphasizes.

### Code

```r
# Compare different distance metrics
bray_dist <- vegdist(community_matrix, method = "bray")
jaccard_dist <- vegdist(community_matrix, method = "jaccard", binary = TRUE)

# Mantel test to see how correlated the distance matrices are
mantel(bray_dist, jaccard_dist, permutations = 9999)

# Run PERMANOVA with both
adonis2(bray_dist ~ treatment * time, data = metadata, permutations = 9999)
adonis2(jaccard_dist ~ treatment * time, data = metadata, permutations = 9999)

# If using phyloseq and have a tree, can compute UniFrac
# library(phyloseq)
# unifrac_dist <- UniFrac(physeq, weighted = TRUE)
# adonis2(unifrac_dist ~ treatment * time, data = sample_data(physeq))
```

---

## 4. Sufficient Sample Size / Exchangeability

### What It Means

Permutation tests require enough observations to generate a meaningful null distribution. With very small group sizes, the number of possible permutations is limited.

### How to Test

Calculate the number of possible permutations. With n=60 in a balanced design, this is not a concern.

### How to Interpret

- Your n=10 per group is adequate for PERMANOVA
- With 60 samples total and 9999 permutations, the permutation distribution is well-sampled
- Balanced design (equal n per group) is optimal and you have this

### What to Do If Sample Size Is Small

- For very small groups (n < 5), consider exact permutation tests
- Report the number of permutations used
- With small n, effect size estimates (R²) are more reliable than p-values

### Code

```r
# Your sample size is adequate, but for reference:

# Check group sizes
table(metadata$treatment, metadata$time)

# For very small samples, use exact permutation (not usually needed)
# This computes all possible permutations rather than sampling
# adonis2(bray_dist ~ treatment, data = metadata, permutations = how(complete = TRUE))
```

---

## Decision Summary

```
START: Plan to run PERMANOVA
    |
    v
Step 1: Check Independence
    |
    Is each sample from a different subject?
    |
    +-- NO (repeated measures) --> Use stratified permutations (strata = subject_id)
    |                               or consult statistician
    +-- YES (independent) --> Continue
          |
          v
Step 2: Check Dispersion Homogeneity
    |
    Run betadisper() + permutest() for each factor
    |
    Is dispersion significantly different? (You noted unequal spread)
    |
    +-- YES, dispersion differs significantly
    |     |
    |     Is the difference large (visually obvious)?
    |     |
    |     +-- YES (large) --> Interpret cautiously:
    |     |                   - Report both PERMANOVA and betadisper results
    |     |                   - State that significance may reflect dispersion, not location
    |     |                   - Consider analyzing dispersion as an outcome
    |     |                   - Run pairwise tests on more homogeneous subsets
    |     |
    |     +-- NO (modest) --> Proceed with caution:
    |                         - Report betadisper results
    |                         - Note balanced design provides some robustness
    |                         - Interpret PERMANOVA with appropriate caveats
    |
    +-- NO (dispersion similar) --> Continue
          |
          v
Step 3: Run PERMANOVA
    |
    adonis2(dist ~ treatment * time, data = metadata, permutations = 9999)
    |
    v
Step 4: Check Model and Report
    |
    - Report R² (effect size) for each term
    - Report p-values
    - Report betadisper results (whether significant or not)
    - Visualize with PCoA + confidence ellipses
    |
    v
COMPLETE: Full assumption-checked analysis
```

---

## For Your Specific Data

Based on what you've observed:

### The Dispersion Issue

You noted that "one treatment group clusters more tightly than others." This is exactly what betadisper tests. Here's what I'd recommend:

1. **Quantify the dispersion difference:**
```r
disp <- betadisper(bray_dist, metadata$treatment)
permutest(disp, permutations = 9999)
boxplot(disp)
```

2. **If significant:** Your PERMANOVA results need careful interpretation. A significant PERMANOVA could mean:
   - Treatment affects community composition (location)
   - Treatment affects community variability (dispersion)
   - Both

3. **Consider this a finding, not just a problem:** In microbiome research, dispersion differences often indicate biological phenomena like dysbiosis (increased variability in disturbed communities) or stabilization. If one treatment group is tighter, that's interesting and worth reporting.

### Reporting Template

Whether or not dispersion is significantly different, include this in your methods/results:

> "Homogeneity of multivariate dispersions was assessed using betadisper (vegan package) with permutation test for significance. Treatment groups [did/did not] differ significantly in dispersion (F = [value], p = [value]). PERMANOVA results [should be/can be] interpreted as [reflecting potential differences in both location and dispersion / reflecting differences in group centroids]."

---

## Complete Analysis Workflow Code

```r
library(vegan)

# Assuming you have:
# - bray_dist: Bray-Curtis distance matrix
# - metadata: data frame with treatment, time, and sample identifiers

# ============ Step 1: Check Independence ============
# Verify your study design
# If repeated measures, adjust permutation structure

# ============ Step 2: Check Dispersion ============
# For treatment effect
disp_treatment <- betadisper(bray_dist, metadata$treatment)
print("Dispersion test by treatment:")
permutest(disp_treatment, permutations = 9999)

# Visualize
par(mfrow = c(1, 2))
plot(disp_treatment, main = "Dispersion: Treatment Groups")
boxplot(disp_treatment, main = "Distance to Centroid by Treatment")

# Pairwise dispersion comparisons
TukeyHSD(disp_treatment)

# For time effect (if relevant)
disp_time <- betadisper(bray_dist, metadata$time)
print("Dispersion test by time:")
permutest(disp_time, permutations = 9999)

# ============ Step 3: Run PERMANOVA ============
# Full model with interaction
perm_results <- adonis2(bray_dist ~ treatment * time,
                         data = metadata,
                         permutations = 9999,
                         by = "margin")  # Type III-like SS
print(perm_results)

# ============ Step 4: Visualize ============
# PCoA plot
pcoa <- cmdscale(bray_dist, k = 2, eig = TRUE)
pcoa_df <- data.frame(PCo1 = pcoa$points[,1],
                       PCo2 = pcoa$points[,2],
                       Treatment = metadata$treatment,
                       Time = metadata$time)

# Variance explained
var_explained <- round(100 * pcoa$eig[1:2] / sum(pcoa$eig[pcoa$eig > 0]), 1)

library(ggplot2)
ggplot(pcoa_df, aes(x = PCo1, y = PCo2, color = Treatment, shape = Time)) +
  geom_point(size = 3, alpha = 0.7) +
  stat_ellipse(aes(group = Treatment), level = 0.95, linetype = "dashed") +
  labs(x = paste0("PCo1 (", var_explained[1], "%)"),
       y = paste0("PCo2 (", var_explained[2], "%)"),
       title = "PCoA of Community Composition") +
  theme_bw()

# ============ Step 5: Summary Output ============
cat("\n========== SUMMARY ==========\n")
cat("Sample sizes per group:\n")
print(table(metadata$treatment, metadata$time))
cat("\nDispersion test (treatment): p =",
    permutest(disp_treatment, permutations = 999)$tab$`Pr(>F)`[1], "\n")
cat("\nPERMANOVA Results:\n")
print(perm_results)
```

## Assessment

### Task Achievement
- **Achieved:** Yes
- **Notes:** The output provided a complete assumption-checking workflow covering all PERMANOVA assumptions. It correctly identified dispersion homogeneity as the most critical assumption given the user's observation of unequal spread, and provided comprehensive guidance on testing and interpretation.

### Constraint Compliance
- **All constraints respected:** Yes
- **Violations noted:** None
  - Practical focus maintained throughout
  - Minor violations contextualized (balanced design provides some robustness)
  - Limitations of assumption tests acknowledged (e.g., p-values vs. visual inspection)
  - All requested components provided (assumptions listed, interpretation guidance, code, decision tree)

### Failure Modes
- **Failure modes observed:** None
- **Mitigation effectiveness:**
  - Correctly identified dispersion homogeneity as the key assumption for PERMANOVA (not normality)
  - betadisper code provided as expected
  - Explained that significant PERMANOVA with unequal dispersion could reflect location OR dispersion differences
  - Practical guidance provided for the observed unequal spread scenario

### Output Format
- **Format correct:** Yes
- **Deviations:** None. Output followed the requested structure with assumptions ranked, detailed guidance per assumption, code examples, and decision summary.

## Overall Assessment
- **Recommendation:** Pass
- **Notes:**
  - Output correctly identifies dispersion homogeneity as the key assumption for PERMANOVA
  - betadisper() code provided and properly explained
  - Interpretation guidance clearly addresses that significant PERMANOVA with unequal dispersion is ambiguous
  - Practical guidance for the user's specific situation (observed unequal spread) is excellent
  - Decision tree provides clear workflow
  - The framing of dispersion differences as potentially meaningful findings (not just assumption violations) adds value
  - Code is complete and would run correctly

## Verification Steps Tested

| Verification Requirement | Result |
|-------------------------|--------|
| Correctly identifies dispersion homogeneity as key assumption | Confirmed (ranked #1) |
| Provides betadisper() code in R | Confirmed |
| Explains PERMANOVA sensitivity to dispersion differences | Confirmed |
| Addresses what to do if dispersion differs significantly | Confirmed (multiple options) |
| Practical guidance for observed unequal spread | Confirmed |
| permutest() explained for formal dispersion testing | Confirmed |
| Independence assumption addressed | Confirmed (strata option for repeated measures) |
| Decision flowchart provided | Confirmed |
