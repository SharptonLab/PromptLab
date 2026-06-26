# Test Results: statistics/assumption-checking.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-25.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** statistics/assumption-checking.md
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

3. **Code examples** for the assumption checks in R with vegan

4. **Decision summary**: A flowchart or decision tree for how to proceed based on results

Constraints:
- Be practical—focus on violations that meaningfully affect inference
- Note when minor violations are unlikely to matter
- Acknowledge that some assumption tests have their own limitations
````

## Model Output
````
# PERMANOVA Assumption-Checking Workflow

## Conceptual Foundation First

PERMANOVA is often described as "assumption-free" because it uses permutations rather than parametric distributions. This is **partially true but misleading**. The test is robust to non-normality, but it has real assumptions that, when violated, can produce false positives or uninterpretable results. Understanding *why* each assumption matters will help you make better judgment calls.

---

## Assumptions Ranked by Severity of Violation

| Rank | Assumption | Violation Consequence | Your Situation |
|------|-----------|----------------------|----------------|
| 1 | **Exchangeability** | Invalid p-values (fundamental) | Need to verify |
| 2 | **Homogeneity of dispersions** | False positives for group differences | ⚠️ Flagged concern |
| 3 | **Appropriate distance metric** | Testing wrong biological question | Need to verify |
| 4 | **Independence of samples** | Inflated Type I error | Need to verify |
| 5 | **Sufficient permutations** | Imprecise p-values | Easy to fix |

---

## Assumption 1: Exchangeability (Most Critical)

### What it means in plain language
The permutation test works by randomly shuffling group labels and asking: "How often would we see a result this extreme by chance?" This is only valid if, under the null hypothesis, observations are interchangeable across groups. In practice, this means **your experimental design must be respected during permutation**.

The most common violation: **repeated measures or nested data** where you permute as if samples are independent when they are not (e.g., multiple timepoints from the same subject).

> ⚠️ **Your design has two timepoints per subject — this is the most critical issue in your analysis.** If the same subjects are measured at both timepoints, naive PERMANOVA will be anti-conservative.

### How to test it
This is primarily a **design question**, not a statistical test. Ask yourself:
- Are any samples from the same individual/plot/tank/cage?
- Are samples nested within a higher-level unit?
- Is there a blocking structure?

### What to do if violated

**If you have repeated measures (same subjects at both timepoints):**

```r
# Option 1: Use strata argument to restrict permutations within subjects
# This permutes time labels only within each subject

library(vegan)

# Assuming your metadata has columns: SampleID, Subject, Treatment, Time
# and 'bc_dist' is your Bray-Curtis distance matrix

# Create a grouping factor for strata (one level per subject)
# This tells adonis2 to only permute within subjects
permanova_repeated <- adonis2(
  bc_dist ~ Treatment * Time,
  data = metadata,
  permutations = how(
    nperm = 9999,
    blocks = metadata$Subject  # restricts permutations within subjects
  )
)

print(permanova_repeated)
```

```r
# Option 2: Separate analyses per timepoint if interaction isn't the focus
# Timepoint 1 only
meta_t1 <- metadata[metadata$Time == "T1", ]
dist_t1 <- as.dist(as.matrix(bc_dist)[meta_t1$SampleID, meta_t1$SampleID])

permanova_t1 <- adonis2(dist_t1 ~ Treatment, data = meta_t1, permutations = 9999)

# Timepoint 2 only  
meta_t2 <- metadata[metadata$Time == "T2", ]
dist_t2 <- as.dist(as.matrix(bc_dist)[meta_t2$SampleID, meta_t2$SampleID])

permanova_t2 <- adonis2(dist_t2 ~ Treatment, data = meta_t2, permutations = 9999)
```

```r
# Option 3: Mixed-effects analog using lme-style approach
# The 'permute' package gives fine-grained control

library(permute)

# Define a permutation scheme: free permutation within blocks (subjects)
h <- how(
  nperm    = 9999,
  blocks   = metadata$Subject,   # never permute across subjects
  plots    = Plots(strata = metadata$Subject, type = "free")
)

# Check that your scheme makes sense
# Should show permutations restricted within subjects
check(metadata, control = h)

permanova_mixed <- adonis2(
  bc_dist ~ Treatment * Time,
  data         = metadata,
  permutations = h
)
```

### Interpreting the strata approach
When you use `blocks`, permutations are restricted so that Time labels are shuffled only within each subject. This correctly accounts for the within-subject correlation. The effective number of permutations may be lower — check this with `check()`.

---

## Assumption 2: Homogeneity of Multivariate Dispersions

### What it means in plain language
PERMANOVA tests whether group **centroids** differ in multivariate space. But if one group is tightly clustered and another is spread out (as you've observed), a significant PERMANOVA result could mean either:
- The groups genuinely differ in composition (centroid difference) ✓
- The groups differ only in *variability*, not location ✗

This is the multivariate analog of Levene's test for homogeneity of variance. The key function is `betadisper()`.

> ⚠️ **You've already noticed this problem** — one treatment group clusters more tightly. This needs formal testing.

### How to test it

```r
# ============================================================
# BETADISPER: Test homogeneity of multivariate dispersions
# ============================================================

library(vegan)

# Test dispersion by Treatment group
disp_treatment <- betadisper(bc_dist, metadata$Treatment)

# Formal test: permutation-based (preferred over parametric ANOVA)
set.seed(123)
disp_test_treatment <- permutest(disp_treatment, permutations = 9999)
print(disp_test_treatment)

# Also run parametric ANOVA for comparison
disp_anova_treatment <- anova(disp_treatment)
print(disp_anova_treatment)

# Tukey HSD to identify which groups differ in dispersion
disp_tukey_treatment <- TukeyHSD(disp_treatment)
print(disp_tukey_treatment)
```

```r
# Test dispersion by Time
disp_time <- betadisper(bc_dist, metadata$Time)
set.seed(123)
permutest(disp_time, permutations = 9999)

# Test dispersion by Treatment:Time combination
metadata$TreatTime <- interaction(metadata$Treatment, metadata$Time)
disp_interaction <- betadisper(bc_dist, metadata$TreatTime)
set.seed(123)
permutest(disp_interaction, permutations = 9999)
```

```r
# ============================================================
# VISUALIZATION: This is often more informative than the test
# ============================================================

par(mfrow = c(1, 2))

# Plot 1: PCoA with dispersion ellipses
plot(disp_treatment,
     hull    = FALSE,      # convex hulls can be misleading
     ellipse = TRUE,       # standard deviation ellipses
     main    = "Dispersion by Treatment",
     col     = c("#E41A1C", "#377EB8", "#4DAF4A"),
     label   = TRUE)

# Plot 2: Boxplot of distances to centroid
# This directly shows which groups have higher spread
boxplot(disp_treatment,
        main   = "Distance to Group Centroid",
        ylab   = "Distance to centroid",
        col    = c("#E41A1C", "#377EB8", "#4DAF4A"),
        notch  = FALSE)

par(mfrow = c(1, 1))
```

```r
# ============================================================
# GGPLOT VERSION: More publication-ready
# ============================================================

library(ggplot2)
library(dplyr)

# Extract distances to centroid
distances_df <- data.frame(
  Distance  = disp_treatment$distances,
  Treatment = metadata$Treatment,
  Time      = metadata$Time
)

# Boxplot with individual points
ggplot(distances_df, aes(x = Treatment, y = Distance, fill = Treatment)) +
  geom_boxplot(alpha = 0.7, outlier.shape = NA) +
  geom_jitter(width = 0.15, size = 2, alpha = 0.6) +
  facet_wrap(~Time) +
  labs(
    title    = "Multivariate Dispersion by Group",
    subtitle = "Distance to group centroid (Bray-Curtis)",
    y        = "Distance to centroid",
    x        = "Treatment"
  ) +
  theme_bw() +
  theme(legend.position = "none")
```

### Interpreting betadisper results

| betadisper p-value | Interpretation | Action |
|-------------------|----------------|--------|
| p > 0.05 | Dispersions are homogeneous | Proceed with PERMANOVA normally |
| p < 0.05, small effect | Mild heterogeneity | Report both tests, note caveat |
| p < 0.05, large effect | Serious heterogeneity | PERMANOVA result is ambiguous |

### What to do if violated

```r
# ============================================================
# OPTION 1: Report PERMANOVA + betadisper together
# Standard practice — let readers interpret both
# ============================================================

# Run both and report side by side
results_permanova  <- adonis2(bc_dist ~ Treatment * Time, data = metadata, permutations = 9999)
results_betadisper <- permutest(disp_treatment, permutations = 9999)

# If PERMANOVA is significant BUT betadisper is also significant:
# "Groups differ in composition (PERMANOVA p = X), but also in 
#  dispersion (betadisper p = Y), so the PERMANOVA result may 
#  partly reflect differences in variability rather than location."
```

```r
# ============================================================
# OPTION 2: Transformation to stabilize dispersion
# Hellinger transformation often reduces dispersion differences
# ============================================================

library(vegan)

# Hellinger-transform the OTU/ASV table first
otu_hellinger <- decostand(otu_table, method = "hellinger")

# Then compute Euclidean distance on transformed data
# (equivalent to Hellinger distance)
hell_dist <- dist(otu_hellinger, method = "euclidean")

# Re-check dispersion
disp_hell <- betadisper(hell_dist, metadata$Treatment)
permutest(disp_hell, permutations = 9999)
```

```r
# ============================================================
# OPTION 3: ANOSIM as a complementary test
# More sensitive to location differences, less to dispersion
# (though it has its own limitations)
# ============================================================

anosim_result <- anosim(bc_dist, metadata$Treatment, permutations = 9999)
summary(anosim_result)
# R statistic: 1 = complete separation, 0 = no separation, negative = more within than between
# Compare with PERMANOVA — if both significant, more confident in location difference
```

```r
# ============================================================
# OPTION 4: Multivariate Levene's test approach
# Test dispersion differences directly as your primary question
# ============================================================

# If your biological question IS about variability (e.g., does 
# treatment reduce community variability?), betadisper IS your test
summary(disp_treatment)
# Groups with smaller mean distance to centroid = more homogeneous communities
```

---

## Assumption 3: Appropriate Distance Metric

### What it means in plain language
PERMANOVA doesn't care what distance matrix you use, but your choice determines what biological question you're answering. Bray-Curtis is appropriate for most microbiome work, but it's worth confirming it matches your question.

### How to evaluate it

```r
# ============================================================
# COMPARE DISTANCE METRICS: Do conclusions change?
# ============================================================

# Bray-Curtis (abundance-weighted, ignores joint absences)
bc_dist <- vegdist(otu_table, method = "bray")

# Jaccard (presence/absence only)
jac_dist <- vegdist(otu_table, method = "jaccard", binary = TRUE)

# Weighted UniFrac (if phylogenetic tree available)
# library(phyloseq)
# wunifrac_dist <- UniFrac(physeq, weighted = TRUE)

# Unweighted UniFrac
# uwunifrac_dist <- UniFrac(physeq, weighted = FALSE)

# Run PERMANOVA with each
perm_bc  <- adonis2(bc_dist  ~ Treatment * Time, data = metadata, permutations = 9999)
perm_jac <- adonis2(jac_dist ~ Treatment * Time, data = metadata, permutations = 9999)

# Compare R² values and p-values
cat("Bray-Curtis R²:", perm_bc$R2[1:3], "\n")
cat("Jaccard R²:    ", perm_jac$R2[1:3], "\n")
```

```r
# ============================================================
# MANTEL TEST: Are distance matrices correlated?
# Checks if different metrics tell the same story
# ============================================================

mantel_result <- mantel(bc_dist, jac_dist, method = "pearson", permutations = 9999)
print(mantel_result)
# r > 0.9: metrics are telling the same story
# r < 0.7: metrics diverge — investigate why (rare taxa driving differences?)
```

### Decision guide for distance metrics

```
Is phylogenetic relatedness important?
├── YES → Use UniFrac (weighted if abundance matters, unweighted if presence/absence)
└── NO  → 
    Is your question about rare vs. dominant taxa?
    ├── Dominant taxa matter more → Bray-Curtis (default for microbiome)
    ├── All taxa equally → Jaccard (presence/absence)
    └── Unsure → Run both and compare
```

---

## Assumption 4: Independence of Observations

### What it means in plain language
Samples should not be correlated with each other beyond what's explained by your predictors. Common violations:
- Multiple samples from the same subject (covered in Assumption 1)
- Spatial autocorrelation (samples near each other are more similar)
- Temporal autocorrelation (samples close in time are more similar)
- Batch effects (samples processed together are more similar)

### How to test it

```r
# ============================================================
# CHECK FOR BATCH EFFECTS
# ============================================================

# If you have batch information:
adonis2(bc_dist ~ Batch + Treatment * Time, data = metadata, permutations = 9999)
# If Batch is significant, it's a confound

# Visual check: does PCoA cluster by batch?
pcoa_result <- cmdscale(bc_dist, k = 2, eig = TRUE)
pcoa_df <- data.frame(
  PC1   = pcoa_result$points[, 1],
  PC2   = pcoa_result$points[, 2],
  Batch = metadata$Batch,
  Treatment = metadata$Treatment
)

ggplot(pcoa_df, aes(x = PC1, y = PC2, color = Treatment, shape = Batch)) +
  geom_point(size = 3) +
  theme_bw() +
  labs(title = "PCoA: Check for batch clustering")
```

```r
# ============================================================
# CHECK FOR SPATIAL/TEMPORAL AUTOCORRELATION
# ============================================================

# Mantel test against geographic/temporal distance
# (if you have spatial coordinates or collection dates)

# Create a geographic distance matrix
geo_dist <- dist(metadata[, c("Longitude", "Latitude")])

# Test correlation between community similarity and geographic distance
mantel_geo <- mantel(bc_dist, geo_dist, method = "pearson", permutations = 9999)
print(mantel_geo)
# Significant positive r: nearby samples are more similar (spatial autocorrelation)
```

---

## Assumption 5: Sufficient Permutations

### What it means in plain language
The p-value precision is limited by the number of permutations. With 999 permutations, the minimum possible p-value is 0.001. With 9999, it's 0.0001. For borderline results,
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
