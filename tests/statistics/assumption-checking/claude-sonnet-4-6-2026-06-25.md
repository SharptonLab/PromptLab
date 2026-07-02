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
# Option 2: For more complex repeated measures, consider lme-style approaches
# using the 'permute' package for fine-grained control

library(permute)

# Define a permutation scheme: permute Time within Subject blocks
h <- how(
  nperm = 9999,
  blocks = metadata$Subject,    # never permute across subjects
  plots  = Plots(
    strata = metadata$Subject,
    type   = "free"             # free permutation within each subject block
  )
)

permanova_complex <- adonis2(
  bc_dist ~ Treatment * Time,
  data         = metadata,
  permutations = h
)
```

**If samples are truly independent (different subjects at each timepoint):**
Standard permutation is valid, but note you cannot make within-subject inferences.

---

## Assumption 2: Homogeneity of Multivariate Dispersions

### What it means in plain language
PERMANOVA tests whether group **centroids** differ in multivariate space. However, if one group has much tighter clustering than another (lower dispersion), PERMANOVA can return a significant result even when centroids are identical — it's detecting **spread differences, not location differences**.

Think of it like a univariate analogy: a t-test assumes equal variances; when variances differ dramatically, you can get significant results that don't mean what you think they mean.

> ⚠️ **You've already noticed this in your data** — one treatment group clusters more tightly. This is your highest-priority diagnostic to run.

### How to test it: `betadisper()`

```r
library(vegan)
library(ggplot2)

# ── 1. Formal test: PERMDISP (betadisper + permutest) ──────────────────────

# Test dispersion for Treatment groups
disp_treatment <- betadisper(
  d      = bc_dist,
  group  = metadata$Treatment,
  type   = "centroid"  # "centroid" is more robust than "median" for most cases
                       # use "median" if you have outliers
)

# Permutation test for dispersion differences
set.seed(42)
permutest_treatment <- permutest(
  disp_treatment,
  permutations = 9999,
  pairwise     = TRUE   # get pairwise comparisons between groups
)

print(permutest_treatment)

# Also run for Time and the interaction
disp_time <- betadisper(bc_dist, metadata$Time, type = "centroid")
permutest_time <- permutest(disp_time, permutations = 9999)

# For interaction: create combined group label
metadata$TreatTime <- interaction(metadata$Treatment, metadata$Time)
disp_interaction <- betadisper(bc_dist, metadata$TreatTime, type = "centroid")
permutest_interaction <- permutest(disp_interaction, permutations = 9999, pairwise = TRUE)
```

```r
# ── 2. Visual diagnostics ──────────────────────────────────────────────────

# Plot 1: Boxplot of distances to centroid (most informative)
par(mfrow = c(1, 2))

boxplot(
  disp_treatment,
  main   = "Dispersion by Treatment",
  ylab   = "Distance to Centroid",
  col    = c("#E69F00", "#56B4E9", "#009E73"),
  notch  = FALSE,
  las    = 2
)

# Add individual points for transparency
stripchart(
  disp_treatment$distances ~ disp_treatment$group,
  vertical = TRUE,
  method   = "jitter",
  add      = TRUE,
  pch      = 16,
  col      = "black",
  cex      = 0.6
)

# Plot 2: PCoA with ellipses (what you've been looking at visually)
plot(
  disp_treatment,
  hull    = FALSE,
  ellipse = TRUE,
  main    = "PCoA with 95% Ellipses",
  col     = c("#E69F00", "#56B4E9", "#009E73")
)
```

```r
# ── 3. ggplot2 version for publication-quality figures ─────────────────────

# Extract PCoA scores and distances for ggplot
pcoa_scores <- as.data.frame(scores(disp_treatment, display = "sites"))
pcoa_scores$Treatment <- metadata$Treatment
pcoa_scores$Distance_to_centroid <- disp_treatment$distances

# PCoA plot
p1 <- ggplot(pcoa_scores, aes(x = PCoA1, y = PCoA2, color = Treatment)) +
  geom_point(size = 3, alpha = 0.7) +
  stat_ellipse(level = 0.95, linewidth = 1) +
  scale_color_manual(values = c("#E69F00", "#56B4E9", "#009E73")) +
  theme_bw(base_size = 12) +
  labs(
    title    = "PCoA of Bray-Curtis Distances",
    subtitle = "Ellipses = 95% confidence regions",
    x        = paste0("PCoA1 (", round(disp_treatment$eig[1]/sum(disp_treatment$eig)*100, 1), "%)"),
    y        = paste0("PCoA2 (", round(disp_treatment$eig[2]/sum(disp_treatment$eig)*100, 1), "%)")
  )

# Dispersion boxplot
p2 <- ggplot(pcoa_scores, aes(x = Treatment, y = Distance_to_centroid, fill = Treatment)) +
  geom_boxplot(alpha = 0.7, outlier.shape = NA) +
  geom_jitter(width = 0.15, size = 2, alpha = 0.6) +
  scale_fill_manual(values = c("#E69F00", "#56B4E9", "#009E73")) +
  theme_bw(base_size = 12) +
  labs(
    title = "Multivariate Dispersion by Treatment",
    y     = "Distance to Group Centroid",
    x     = "Treatment"
  ) +
  theme(legend.position = "none")

library(patchwork)
p1 + p2
```

### How to interpret the results

| betadisper p-value | Interpretation | Action |
|-------------------|----------------|--------|
| p > 0.05 | No significant dispersion difference | Proceed with PERMANOVA normally |
| p = 0.01–0.05 | Marginal difference | Report both tests; interpret cautiously |
| p < 0.01 | Significant dispersion difference | PERMANOVA result is ambiguous |

**Critical nuance**: A significant PERMANOVA + significant betadisper means you cannot distinguish between:
1. Groups have different community compositions (centroids differ)
2. Groups have different variability (dispersions differ)
3. Both

### What to do if violated

```r
# ── Option A: Report both tests and be explicit about interpretation ────────
# This is the most common approach in published microbiome papers
# State: "PERMANOVA detected significant differences (F=X, p=Y);
#         PERMDISP also detected dispersion differences (F=X, p=Y),
#         suggesting results may reflect differences in variability
#         rather than (or in addition to) community composition."

# ── Option B: Use distance-based tests less sensitive to dispersion ─────────
# ANOSIM is sometimes suggested but has its own problems (more sensitive
# to dispersion than PERMANOVA, not less — avoid this)

# ── Option C: Hellinger transformation before computing distances ───────────
# Can reduce dispersion heterogeneity in some cases
library(vegan)

# Transform the OTU/ASV table (rows = samples, cols = taxa)
otu_hellinger <- decostand(otu_table, method = "hellinger")

# Then use Euclidean distance on Hellinger-transformed data
# (mathematically equivalent to chord distance)
hell_dist <- dist(otu_hellinger, method = "euclidean")

# Re-run betadisper on new distance matrix
disp_hell <- betadisper(hell_dist, metadata$Treatment)
permutest(disp_hell, permutations = 9999)

# ── Option D: Subset analysis ───────────────────────────────────────────────
# If one group drives the dispersion difference, run PERMANOVA
# on pairwise comparisons excluding that group to see if results hold

# Pairwise PERMANOVA (manual approach)
groups_to_compare <- list(
  c("Control", "Treatment1"),
  c("Control", "Treatment2"),
  c("Treatment1", "Treatment2")
)

pairwise_results <- lapply(groups_to_compare, function(grps) {
  idx <- metadata$Treatment %in% grps
  sub_dist <- as.dist(as.matrix(bc_dist)[idx, idx])
  sub_meta <- metadata[idx, ]
  adonis2(sub_dist ~ Treatment, data = sub_meta, permutations = 9999)
})

names(pairwise_results) <- sapply(groups_to_compare, paste, collapse = "_vs_")
pairwise_results
```

> **Limitation of betadisper**: The test itself assumes equal sample sizes for optimal power (you're fine here) and can be sensitive to outliers. The permutation test is more reliable than the accompanying ANOVA F-test — always use `permutest()`, not just the ANOVA output.

---

## Assumption 3: Appropriate Distance Metric

### What it means in plain language
PERMANOVA tests for differences in the distance matrix you provide. If your distance metric doesn't capture the biological signal you care about, a non-significant result doesn't mean communities are similar — it means they're similar *by that metric*.

Bray-Curtis is generally appropriate for microbiome data because it:
- Ignores joint absences (two samples sharing many zero-abundance taxa shouldn't be considered similar)
- Is abundance-weighted
- Ranges 0–1 with intuitive interpretation

### How to evaluate metric choice

```r
# ── Sensitivity analysis: compare results across distance metrics ───────────

library(vegan)

# Compute multiple distance matrices
dist_bray     <- vegdist(otu_table, method = "bray")
dist_jaccard  <- vegdist(otu_table, method = "jaccard",  binary = TRUE)  # presence/absence
dist_unifrac  <- # requires phyloseq or GUniFrac package
dist_wunifrac <- # weighted UniFrac (abundance + phylogeny)

# Run PERMANOVA on each
results_comparison <- lapply(
  list(Bray = dist_bray, Jaccard = dist_jaccard),
  function(d) {
    adonis2(d ~ Treatment * Time, data = metadata, permutations = 9999)
  }
)

# If results are consistent across metrics, conclusions are robust
# If results differ dramatically, the signal may be metric-dependent

# ── Check for excessive zeros (affects Bray-Curtis reliability) ─────────────
zero_prop <- sum(otu_table == 0) / prod(dim(otu_table))
cat("Proportion of zeros in OTU table:", round(zero_prop, 3), "\n")
# > 0.90 (90% zeros) suggests very sparse data; consider rarefaction
# or alternative approaches

# ── Rarefaction check ───────────────────────────────────────────────────────
# Unequal sequencing depth can distort Bray-Curtis distances
# Check library sizes
lib_sizes <- rowSums(otu_table)
summary(lib_sizes)
hist(lib_sizes, main = "Library Sizes", xlab = "Read Count", col = "steelblue")

# Large variation in library size (CV > 0.5) warrants rarefaction
# or use of relative abundances
cv_lib <- sd(lib_sizes) / mean(lib_sizes)
cat("Coefficient of variation for library sizes:", round(cv_lib, 3), "\n")
```

---

## Assumption 4: Independence of Samples

### What it means in plain language
Each sample should provide independent information. Violations occur when:
- Samples from the same cage/tank/plot are treated as independent
- Spatial autocorrelation exists (nearby samples are more similar)
- Temporal autocorrelation exists beyond your designed timepoints

### How to check

```r
# ── Check for clustering by potential confounders ──────────────────────────

# If you have batch information, check whether batch explains variance
if ("Batch" %in% names(metadata)) {
  adonis2(bc_dist ~ Batch + Treatment * Time,
          data         = metadata,
          permutations = 9999,
          by           = "margin")  # Type III SS — tests each term
                                    # after accounting for all others
}

# ── Mantel test for spatial autocorrelation (if you have coordinates) ───────
if (all(c("Latitude", "Longitude") %in% names(metadata))) {
  geo_dist <- dist(metadata[, c("Latitude", "Longitude")])
  mantel_result <- mantel(bc_dist, geo_dist, permutations = 9999)
  print(mantel_result)
  # Significant result suggests spatial structure that should be modeled
}

# ── For cage/tank effects: use strata in permutations ──────────────────────
if ("Cage" %in% names(metadata)) {
  permanova_caged <- adonis2(
    bc_dist ~ Treatment * Time,
    data         = metadata,
    permutations = how(
      nperm  = 9999,
      blocks = metadata$Cage  # permute only within cages
    )
  )
}
```

---

## Assumption 5: Sufficient Permutations

### What it means in plain language
The p-value from PERMANOVA is estimated from a permutation distribution. Too few permutations = imprecise p-value. This matters most when p-values are near your threshold (e.g., p ≈ 0.05).

### Rule of thumb and implementation

```r
# ── Standard recommendation: 9999 permutations ─────────────────────────────
# With 9999 permutations, minimum achievable p-value = 0.0001
# With 999 permutations, minimum = 0.001

# Check precision of your p-value
# If p = 0.048 with 999 permutations, rerun with 9999
# If p = 0.001 with 9999 permutations, result is stable

set.seed(42)  # Always set seed for reproducibility
permanova_final <- adonis2(
  bc_dist ~ Treatment * Time,
  data         = metadata,
  permutations = 9999,
  by           = "margin"  # recommended for interaction models
)

# ── Check stability: run twice with different seeds ─────────────────────────
set.seed(123)
p1_check <- adonis2(bc_dist ~ Treatment * Time, data = metadata,
                    permutations = 9999, by = "margin")

set.seed(456)
p2_check <- adonis2(bc_dist ~ Treatment * Time, data = metadata,
                    permutations = 9999, by = "margin")

# P-values should agree to 2 decimal places with 9999 permutations
cat("Run 1 Treatment p-value:", p1_check["Treatment", "Pr(>F)"], "\n")
cat("Run 2 Treatment p-value:", p2_check["Treatment", "Pr(>F)"], "\n")
```

---

## Complete Workflow: All Checks Together

```r
# ════════════════════════════════════════════════════════════════════════════
# COMPLETE PERMANOVA ASSUMPTION CHECKING WORKFLOW
# ════════════════════════════════════════════════════════════════════════════

library(vegan)
library(ggplot2)
library(patchwork)

# ── Setup ───────────────────────────────────────────────────────────────────
# Inputs required:
#   otu_table : matrix/df, rows = samples, cols = taxa
#   metadata  : data.frame with columns Treatment, Time, Subject (if repeated)
#   bc_dist   : Bray-Curtis distance matrix

bc_dist <- vegdist(otu_table, method = "bray")

# ── STEP 1: Check exchangeability (design question) ─────────────────────────
cat("═══ STEP 1: Exchangeability ═══\n")
cat("Are the same subjects measured at both timepoints? (Y/N): ")
# If YES: use strata/blocks in permutations (see Assumption 1 code above)
# If NO:  standard permutation is valid

# ── STEP 2: Check dispersion homogeneity ────────────────────────────────────
cat("\n═══ STEP 2: Dispersion Homogeneity ═══\n")

# 2a. By Treatment
disp_trt <- betadisper(bc_dist, metadata$Treatment, type = "centroid")
perm_trt  <- permutest(disp_trt, permutations = 9999, pairwise = TRUE)

cat("Treatment dispersion test:\n")
print(perm_trt)

# 2b. By Time
disp_time <- betadisper(bc_dist, metadata$Time, type = "centroid")
perm_time  <- permutest(disp_time, permutations = 9999)

cat("\nTime dispersion test:\n")
print(perm_time)

# 2c. By Treatment:Time interaction
metadata$TreatTime <- interaction(metadata$Treatment, metadata$Time)
disp_int  <- betadisper(bc_dist, metadata$TreatTime, type = "centroid")
perm_int   <- permutest(disp_int, permutations = 9999, pairwise = TRUE)

cat("\nTreatment:Time interaction dispersion test:\n")
print(perm_int)

# 2d. Visualize
par(mfrow = c(1, 3))
boxplot(disp_trt,  main = "Dispersion: Treatment", col = 2:4, las = 2)
boxplot(disp_time, main = "Dispersion: Time",      col = 5:6, las = 2)
boxplot(disp_int,  main = "Dispersion: Interaction", col = 2:7, las = 2)
par(mfrow = c(1, 1))

# ── STEP 3: Check library sizes ─────────────────────────────────────────────
cat("\n═══ STEP 3: Library Size Check ═══\n")
lib_sizes <- rowSums(otu_table)
cv_lib    <- sd(lib_sizes) / mean(lib_sizes)
cat("Library size summary:\n")
print(summary(lib_sizes))
cat("Coefficient of variation:", round(cv_lib, 3), "\n")
if (cv_lib > 0.5) {
  cat("⚠️  High variation in library sizes. Consider rarefaction.\n")
} else {
  cat("✓  Library sizes are reasonably uniform.\n")
}

# ── STEP 4: Run PERMANOVA ────────────────────────────────────────────────────
cat("\n═══ STEP 4: PERMANOVA ═══\n")

# Determine permutation scheme based on Step 1
# CASE A: Independent samples (different subjects at each timepoint)
set.seed(42)
permanova_result <- adonis2(
  bc_dist ~ Treatment * Time,
  data         = metadata,
  permutations = 9999,
  by           = "margin"   # Type III: each term after all others
                             # use "terms" for sequential (Type I) SS
)

# CASE B: Repeated measures (same subjects at both timepoints)
# set.seed(42)
# permanova_result <- adonis2(
#   bc_dist ~ Treatment * Time,
#   data         = metadata,
#   permutations = how(nperm = 9999, blocks = metadata$Subject)
# )

print(permanova_result)

# ── STEP 5: Interpret with dispersion context ────────────────────────────────
cat("\n═══ STEP 5: Integrated Interpretation ═══\n")

# Extract p-values
p_trt  <- perm_trt$tab["Groups", "Pr(>F)"]
p_time <- perm_time$tab["Groups", "Pr(>F)"]

p_perm_trt  <- permanova_result["Treatment", "Pr(>F)"]
p_perm_time <- permanova_result["Time",      "Pr(>F)"]
p_perm_int  <- permanova_result["Treatment:Time", "Pr(>F)"]

# Automated interpretation helper
interpret_result <- function(perm_p, disp_p, term_name) {
  cat(sprintf("\n%s:\n", term_name))
  cat(sprintf("  PERMANOVA p = %.4f | PERMDISP p = %.4f\n", perm_p, disp_p))

  if (perm_p >= 0.05) {
    cat("  → No significant difference detected.\n")
  } else if (perm_p < 0.05 && disp_p >= 0.05) {
    cat("  → ✓ Significant difference in community composition.\n")
    cat("     Dispersion is homogeneous; result reflects centroid differences.\n")
  } else if (perm_p < 0.05 && disp_p < 0.05) {
    cat("  → ⚠️  Significant PERMANOVA but also significant dispersion difference.\n")
    cat("     Cannot distinguish composition vs. variability differences.\n")
    cat("     Report both results; interpret with caution.\n")
  }
}

interpret_result(p_perm_trt,  p_trt,  "Treatment")
interpret_result(p_perm_time, p_time, "Time")
```

---

## Decision Flowchart

```
START: Plan to run PERMANOVA
│
├─► Q1: Are samples independent?
│   (Same subjects at multiple timepoints?)
│   │
│   ├─ YES (repeated measures)
│   │   └─► Use strata/blocks in permutations
│   │       (how(blocks = Subject))
│   │
│   └─ NO → Continue
│
├─► Q2: Are library sizes highly variable? (CV > 0.5)
│   │
│   ├─ YES → Rarefy or use relative abundances
│   │        then recompute Bray-Curtis
│   │
│   └─ NO → Continue
│
├─► Q3: Run betadisper + permutest
│   │
│   ├─ p > 0.05 (homogeneous dispersion)
│   │   └─► ✓ Run PERMANOVA normally
│   │       Significant result = centroid difference
│   │
│   └─ p < 0.05 (heterogeneous dispersion)
│       │
│       ├─► Run PERMANOVA anyway (it's still informative)
│       │
│       ├─► Try Hellinger transformation → recheck dispersion
│       │
│       └─► In paper: report BOTH PERMANOVA and PERMDISP results
│           State: "differences may reflect composition AND/OR variability"
│
├─► Q4: Run PERMANOVA (9999 permutations, by = "margin")
│
└─► Q5: Is p-value near threshold (0.04–0.06)?
    │
    ├─ YES → Rerun with different seed to confirm stability
    │        Consider increasing to 99,999 permutations
    │
    └─ NO → Report results with R² (effect size) and p-value
```

---

## Reporting Template

Based on this workflow, here is language you can adapt for a methods section:

> "Community composition was compared using PERMANOVA (Anderson 2001) implemented with the `adonis2` function in the vegan package (v2.x; Oksanen et al. 2022) with Bray-Curtis dissimilarities and 9,999 permutations. Terms were tested using marginal (Type III) sums of squares. Prior to PERMANOVA, homogeneity of multivariate dispersions was assessed using `betadisper` with permutation testing (PERMDISP; Anderson 2006). [If violated: Dispersion differed significantly among treatment groups (F = X, p = Y); therefore, PERMANOVA results are interpreted as reflecting differences in community structure broadly, which may include both location and dispersion effects.] All analyses were conducted in R v4.x."

---

## Key Takeaways for Your Specific Situation

Given what you've described, here is the priority order for your analysis:

1. **First**: Determine if you have repeated measures — this affects the validity of every p-value you compute
2. **Second**: Run `betadisper` on Treatment groups — you've already visually identified this problem and need to quantify it
3. **Third**: If dispersion is significantly heterogeneous, you cannot claim PERMANOVA is detecting composition differences alone — you must report this limitation explicitly
4. **Fourth**: Equal sample sizes (n=10 per cell) is genuinely helpful — PERMANOVA is more robust to dispersion heterogeneity with balanced designs than unbalanced ones, so your situation is better than it could be
````

## Assessment

_Machine-suggested (UNCONFIRMED) — drafted by Claude Opus 4.7 on 2026-06-26 (re-triage after max_tokens bump and re-capture). An author must independently read the Model Output above and set the real Recommendation. Anything labeled here is triage, not domain expert review._

**Machine triage:** Output is complete and ends cleanly. Covers all four requested parts (ranked assumptions, per-assumption detail, R code, decision flowchart). Notable: the response explicitly assumes the design has "two timepoints per subject" as repeated measures, but the prompt only says "Time (2 levels)" — this is ambiguous in the prompt and the model flags the ambiguity by treating it as a design question to verify. Methods table includes Anderson 2001 (PERMANOVA) and Anderson 2006 (PERMDISP) author/year citations in the reporting template — these are real attributions and broadly correct, but the user should verify the exact citation format. Reporting template also references "Oksanen et al. 2022" for vegan — the vegan package author list is correct, but year/version should be cross-checked. Code examples use modern `how(blocks=...)` idiom. I cannot verify all the statistical claims (e.g., that betadisper "more reliable than the accompanying ANOVA F-test") match current literature, nor that the user's repeated-measures interpretation is correct.

**Suggested verdict (UNCONFIRMED):** Pass with notes

**What still needs human verification:**
- The Anderson 2001/2006 and Oksanen et al. citations in the reporting template (author/year/journal accuracy)
- That assuming the prompt's "Time (2 levels)" implies repeated measures within subject is correct for this study
- The claim that ANOSIM is "more sensitive to dispersion than PERMANOVA, not less" — check against current literature
- The recommendation to use `type = "centroid"` over `type = "median"` in betadisper
- Statistical correctness of the overall workflow for this design

## Overall Assessment
- **Recommendation:** Pass
- **Notes:** Alex Alexiev (2026-06-29): **What still needs human verification:**
- The Anderson 2001/2006 and Oksanen et al. citations in the reporting template (author/year/journal accuracy): vegan paper came out 2007 but there was a version in 2022. Others are right.
- That assuming the prompt's "Time (2 levels)" implies repeated measures within subject is correct for this study: likely yes, but I cannot evaluate
- The claim that ANOSIM is "more sensitive to dispersion than PERMANOVA, not less" — check against current literature: yes
- The recommendation to use `type = "centroid"` over `type = "median"` in betadisper: yes
- Statistical correctness of the overall workflow for this design: yes

## Verification Steps Tested
_Which verification requirements from the prompt were checked, and results._
