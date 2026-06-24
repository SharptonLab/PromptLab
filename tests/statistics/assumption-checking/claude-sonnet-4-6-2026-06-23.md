# Test Results: statistics/assumption-checking.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-23.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** statistics/assumption-checking.md
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
Context: I plan to use {STATISTICAL_TEST_OR_MODEL} to analyze my data. I need to verify the assumptions are met.

Analysis details:
- Test/model: {SPECIFIC_TEST: e.g., "two-way ANOVA," "logistic regression," "Wilcoxon rank-sum"}
- Outcome variable: {type and name}
- Predictor(s): {type and names}
- Sample size: {n or n per group}
- Software: {what you're using}

Data characteristics I've noticed:
- {ANY_OBSERVATIONS: e.g., "outcome looks skewed," "several outliers visible," "one group has higher variance"}

Task: Provide a complete assumption-checking workflow:

1. **List all assumptions** for this test, in order of importance (which violations are most problematic)

2. **For each assumption**:
   - What it means in plain language
   - How to test it (formal tests and/or visual diagnostics)
   - How to interpret the results
   - What to do if violated (robust alternatives, transformations, or when it's okay to proceed)

3. **Code examples** for the assumption checks in {SOFTWARE}

4. **Decision summary**: A flowchart or decision tree for how to proceed based on results

Constraints:
- Be practical—focus on violations that meaningfully affect inference
- Note when minor violations are unlikely to matter
- Acknowledge that some assumption tests have their own limitations

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

## Model Output
```
# PERMANOVA Assumption-Checking Workflow
## Bray-Curtis Microbiome Data | adonis2 | R/vegan

---

## Preliminary Note on PERMANOVA's Nature

PERMANOVA is often described as "assumption-free" because it uses permutations rather than distributional assumptions. **This is misleading.** It has real assumptions, and the dispersion issue you've already noticed is the most critical one. This guide prioritizes accordingly.

---

## 1. Complete Assumption List (Ordered by Consequence of Violation)

| Priority | Assumption | Violation Consequence |
|----------|-----------|----------------------|
| 🔴 **Critical** | Homogeneity of multivariate dispersions | Significant result may reflect spread differences, not location differences — **false positive for group effect** |
| 🔴 **Critical** | Exchangeability of samples under H₀ | Invalid permutation p-values |
| 🟡 **Important** | Independence of observations | Inflated Type I error |
| 🟡 **Important** | Appropriate distance metric | Misrepresents biological relationships |
| 🟢 **Minor** | Sufficient permutations | Imprecise p-values (easily fixed) |
| 🟢 **Minor** | No extreme leverage samples | Unstable results |

---

## 2. Each Assumption in Detail

---

### 🔴 ASSUMPTION 1: Homogeneity of Multivariate Dispersions
*(Your flagged concern — address this first)*

**Plain language:**
Each group should have similar *spread* around its centroid in multivariate space. PERMANOVA tests whether group *centroids* differ, but if one group is tightly clustered and another is widely scattered, a significant result could mean either "groups are in different locations" OR "groups have different spread" — you can't tell which.

**Why your situation is concerning:**
You've already noticed one treatment group clusters more tightly on PCoA. This is exactly the scenario where PERMANOVA can produce false positives.

**Formal test: `betadisper` + `permutest`**

```r
library(vegan)
library(ggplot2)
library(dplyr)

# Assume your data is structured as:
# - otu_table: samples × taxa matrix (rows = samples)
# - metadata: data frame with columns Treatment, Time, SampleID

# ── Step 1: Compute Bray-Curtis distance matrix ──────────────────────────────
bc_dist <- vegdist(otu_table, method = "bray")

# ── Step 2: Test dispersion for Treatment ────────────────────────────────────
disp_treatment <- betadisper(bc_dist, metadata$Treatment)
permutest(disp_treatment, permutations = 999)

# ── Step 3: Test dispersion for Time ─────────────────────────────────────────
disp_time <- betadisper(bc_dist, metadata$Time)
permutest(disp_time, permutations = 999)

# ── Step 4: Test dispersion for Treatment:Time interaction ───────────────────
# Create combined group variable for interaction
metadata$TreatTime <- interaction(metadata$Treatment, metadata$Time)
disp_interaction <- betadisper(bc_dist, metadata$TreatTime)
permutest(disp_interaction, permutations = 999)

# ── Step 5: Post-hoc pairwise dispersion comparisons ─────────────────────────
# If overall betadisper is significant, identify which groups differ
permutest(disp_treatment, permutations = 999, pairwise = TRUE)
```

**Visual diagnostics:**

```r
# ── Boxplot of distances to centroid ─────────────────────────────────────────
# This is often more interpretable than the PCoA plot

# Extract distances to centroid
disp_df <- data.frame(
  Distance = disp_treatment$distances,
  Treatment = metadata$Treatment,
  Time = metadata$Time
)

ggplot(disp_df, aes(x = Treatment, y = Distance, fill = Treatment)) +
  geom_boxplot(alpha = 0.7, outlier.shape = 21) +
  geom_jitter(width = 0.15, alpha = 0.5, size = 2) +
  facet_wrap(~Time) +
  labs(
    title = "Multivariate Dispersion by Group",
    subtitle = "Distance of each sample to its group centroid",
    y = "Distance to Centroid (Bray-Curtis)",
    x = "Treatment"
  ) +
  theme_bw(base_size = 13) +
  theme(legend.position = "none")

# ── PCoA plot with dispersion ellipses ───────────────────────────────────────
# Standard deviation ellipses reveal unequal spread visually

pcoa_result <- cmdscale(bc_dist, k = 2, eig = TRUE)
pcoa_df <- data.frame(
  PC1 = pcoa_result$points[, 1],
  PC2 = pcoa_result$points[, 2],
  Treatment = metadata$Treatment,
  Time = metadata$Time
)

# Variance explained
var_explained <- round(pcoa_result$eig / sum(pcoa_result$eig[pcoa_result$eig > 0]) * 100, 1)

ggplot(pcoa_df, aes(x = PC1, y = PC2, color = Treatment, shape = Time)) +
  geom_point(size = 3, alpha = 0.8) +
  stat_ellipse(aes(group = Treatment), type = "t", level = 0.95, linewidth = 0.8) +
  labs(
    title = "PCoA of Bray-Curtis Distances",
    subtitle = "Ellipses = 95% confidence (t-distribution) — unequal ellipse sizes = unequal dispersion",
    x = paste0("PC1 (", var_explained[1], "% variance)"),
    y = paste0("PC2 (", var_explained[2], "% variance)")
  ) +
  theme_bw(base_size = 13) +
  scale_color_brewer(palette = "Set1")
```

**Interpreting results:**

| betadisper p-value | Interpretation | Action |
|-------------------|----------------|--------|
| p > 0.05 | Dispersions are homogeneous | Proceed with PERMANOVA normally |
| p < 0.05, small effect | Mild heterogeneity | Report it; PERMANOVA is somewhat robust with equal n |
| p < 0.05, large effect | Serious heterogeneity | Do NOT interpret PERMANOVA alone — see remedies below |

**Quantify the dispersion difference:**

```r
# Get mean distance to centroid per group — report these numbers
tapply(disp_treatment$distances, metadata$Treatment, mean)
tapply(disp_treatment$distances, metadata$Treatment, sd)

# Effect size: ratio of largest to smallest mean dispersion
# Ratio > 2 is generally considered practically meaningful
disp_means <- tapply(disp_treatment$distances, metadata$Treatment, mean)
max(disp_means) / min(disp_means)
```

**What to do if violated:**

```r
# ── Option A: Report both PERMANOVA and betadisper results together ───────────
# This is the minimum — let readers know what's driving significance

# ── Option B: PERMDISP2 — test dispersion as the primary question ─────────────
# If your biological question IS about variability (e.g., dysbiosis = more variable)
# then betadisper IS your analysis, not a nuisance check

# ── Option C: Permutation test on medians (more robust to dispersion) ─────────
# adonis2 uses centroids; some argue median-based approaches are better
# No standard R implementation, but worth noting in limitations

# ── Option D: Analyze subgroups separately ────────────────────────────────────
# If interaction is not significant, analyze Treatment and Time separately
# within strata where dispersion is homogeneous

# ── Option E: Transform the distance matrix ───────────────────────────────────
# Square-root transformation of Bray-Curtis can reduce dispersion differences
bc_sqrt <- sqrt(bc_dist)  # Apply before adonis2
disp_sqrt <- betadisper(bc_sqrt, metadata$Treatment)
permutest(disp_sqrt, permutations = 999)
# Check if transformation improved homogeneity

# ── Option F: Use Aitchison distance (CLR-transformed) ───────────────────────
# Often more homogeneous dispersion than Bray-Curtis
# Requires compositions package or manual CLR transform
library(compositions)
clr_data <- as.matrix(clr(otu_table + 0.5))  # +0.5 pseudocount for zeros
aitchison_dist <- dist(clr_data, method = "euclidean")
disp_aitchison <- betadisper(aitchison_dist, metadata$Treatment)
permutest(disp_aitchison, permutations = 999)
```

---

### 🔴 ASSUMPTION 2: Exchangeability of Samples Under H₀

**Plain language:**
For permutation p-values to be valid, samples must be interchangeable between groups if the null hypothesis (no group difference) were true. This is violated when samples are **not independent** — e.g., repeated measures, nested designs, or spatial/temporal autocorrelation.

**Your design has a potential issue:**
With Treatment × Time, if the same subjects are measured at both time points (repeated measures), samples within a subject are NOT exchangeable. This is a critical design question to resolve.

```r
# ── Determine your design ─────────────────────────────────────────────────────

# SCENARIO A: Independent samples (different subjects at each time point)
# → Standard adonis2 is valid
# → Permute freely within your design

# SCENARIO B: Repeated measures (same subjects at Time 1 and Time 2)
# → Standard adonis2 is INVALID — p-values will be wrong
# → Must use restricted permutations

# ── Restricted permutations for repeated measures ────────────────────────────
library(permute)

# Assuming metadata has a Subject column identifying repeated individuals
# Permute only WITHIN subjects (swap time points within each subject)

h_subjects <- how(
  blocks = metadata$Subject,      # Never permute across subjects
  plots  = Plots(strata = metadata$Subject, type = "free"),
  within = Within(type = "free")  # Permute time within subject
)

# Verify permutation scheme makes sense
check(metadata, control = h_subjects)

# Run adonis2 with restricted permutations
set.seed(42)
perm_result <- adonis2(
  bc_dist ~ Treatment * Time,
  data        = metadata,
  permutations = h_subjects,
  method      = "bray",  # ignored since we pass distance matrix
  by          = "terms"
)
print(perm_result)

# ── For nested designs (e.g., samples nested within patients within sites) ────
h_nested <- how(
  within = Within(type = "free"),
  plots  = Plots(strata = metadata$Site, type = "free"),
  nperm  = 999
)
```

---

### 🟡 ASSUMPTION 3: Independence of Observations

**Plain language:**
Samples should not be correlated with each other beyond what's explained by your predictors. Common violations in microbiome studies: samples from the same patient, same cage/tank, same batch, same collection day.

```r
# ── Check for batch effects visually ─────────────────────────────────────────
# Color PCoA by potential confounders

# Example: check if extraction batch clusters
if ("Batch" %in% colnames(metadata)) {
  pcoa_df$Batch <- metadata$Batch
  
  ggplot(pcoa_df, aes(x = PC1, y = PC2, color = Batch)) +
    geom_point(size = 3) +
    labs(title = "PCoA colored by Batch — check for batch clustering") +
    theme_bw()
  
  # If batch clusters, include it as a covariate in adonis2
  adonis2(bc_dist ~ Batch + Treatment * Time, 
          data = metadata, 
          by = "terms",
          permutations = 999)
}

# ── Check for cage/tank effects (common in animal studies) ───────────────────
# If animals are housed in cages, cage is the true experimental unit
# Use cage as strata in permutations

if ("Cage" %in% colnames(metadata)) {
  h_cage <- how(
    plots = Plots(strata = metadata$Cage, type = "free"),
    nperm = 999
  )
  adonis2(bc_dist ~ Treatment * Time,
          data = metadata,
          permutations = h_cage)
}
```

---

### 🟡 ASSUMPTION 4: Appropriate Distance Metric

**Plain language:**
Bray-Curtis is a reasonable default for microbiome data, but it's worth confirming it matches your biological question and data properties.

```r
# ── Compare multiple distance metrics ────────────────────────────────────────
# Run PERMANOVA with alternatives and compare R² values

distances <- list(
  BrayCurtis  = vegdist(otu_table, method = "bray"),
  Jaccard     = vegdist(otu_table, method = "jaccard", binary = TRUE),
  Aitchison   = dist(as.matrix(clr(otu_table + 0.5)), method = "euclidean"),
  UniFrac_w   = NULL,  # Requires phyloseq: UniFrac(physeq, weighted = TRUE)
  UniFrac_uw  = NULL   # Requires phyloseq: UniFrac(physeq, weighted = FALSE)
)

# Compare R² across metrics (higher = metric captures more group structure)
results_comparison <- lapply(names(distances)[1:3], function(metric) {
  res <- adonis2(distances[[metric]] ~ Treatment * Time,
                 data = metadata, by = "terms", permutations = 999)
  data.frame(
    Metric = metric,
    R2_Treatment = res["Treatment", "R2"],
    R2_Time      = res["Time", "R2"],
    R2_Interaction = res["Treatment:Time", "R2"]
  )
})
do.call(rbind, results_comparison)

# ── Check for zero-inflation issues with Bray-Curtis ─────────────────────────
# Bray-Curtis can behave oddly with very sparse data
sparsity <- sum(otu_table == 0) / prod(dim(otu_table))
cat("Data sparsity:", round(sparsity * 100, 1), "%\n")
# If > 90% zeros, consider Jaccard or presence/absence transformations
```

---

### 🟢 ASSUMPTION 5: Sufficient Permutations

```r
# ── Standard: 999 permutations is usually sufficient ─────────────────────────
# For p-values near your alpha threshold, use more

# Rule of thumb:
# p > 0.10  → 999 permutations fine
# p ~ 0.05  → use 4999 or 9999
# p ~ 0.01  → use 9999

set.seed(42)
result_999 <- adonis2(bc_dist ~ Treatment * Time, 
                      data = metadata, by = "terms", permutations = 999)

set.seed(42)
result_9999 <- adonis2(bc_dist ~ Treatment * Time, 
                       data = metadata, by = "terms", permutations = 9999)

# Compare p-values — should be similar if 999 was sufficient
cbind(
  p_999  = result_999[, "Pr(>F)"],
  p_9999 = result_9999[, "Pr(>F)"]
)
```

---

### 🟢 ASSUMPTION 6: No Extreme Leverage Samples

```r
# ── Identify outlier samples ──────────────────────────────────────────────────
# Samples far from all others can disproportionately influence results

# Method 1: Distance to group centroid (
```

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
