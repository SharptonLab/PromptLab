# Test Results: code/r-script-generation.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-25.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** code/r-script-generation.md
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
Context: I am a microbiome researcher working on a probiotic intervention study. I need an R script to perform ordination analysis and visualize community composition.

Data description:
- Input: phyloseq object saved as RDS file, containing OTU table, taxonomy, and sample data
- Sample data columns: sample_id, subject_id, timepoint (baseline, week4, week8), treatment (probiotic, placebo), age, sex
- Sample size: 180 samples (30 subjects × 2 treatments × 3 timepoints)
- Key variables: timepoint (factor), treatment (factor), subject_id (for repeated measures)

Task: Write an R script that:
1. Loads the phyloseq object and performs basic QC (sample counts, taxa counts)
2. Calculates Bray-Curtis distance matrix
3. Performs PCoA ordination
4. Creates a figure with PCoA colored by treatment, shaped by timepoint
5. Runs PERMANOVA testing treatment × timepoint interaction (accounting for repeated measures via subject blocking)
6. Outputs: ordination plot as PDF, PERMANOVA results summary

Requirements:
1. **Packages**: Use phyloseq, vegan, ggplot2. If you suggest other packages, explain why.

2. **Code style**:
   - Include comments explaining each major step
   - Use descriptive variable names
   - Group related operations into labeled sections

3. **Input/Output**:
   - Input file path: "data/probiotic_study.rds"
   - Output: Publication-quality ordination figure as PDF, statistical summary (PERMANOVA results) printed to console

4. **Error handling**: Include basic checks for common issues (missing data, unexpected formats)

Constraints:
- Use only packages available on CRAN or Bioconductor
- Prefer base R or tidyverse solutions when possible for maintainability
- Flag any assumptions about data structure as comments
- If there are multiple valid approaches, briefly note alternatives

Output format: Complete R script with section headers and comments. After the script, provide:
- List of required packages
- Any assumptions made about the data
- Suggested validation checks to run
````

## Model Output
````
# Microbiome Ordination Analysis Script

```r
# =============================================================================
# Probiotic Intervention Study: Ordination Analysis
# Purpose: PCoA of Bray-Curtis distances with PERMANOVA testing
# Author: [Your Name]
# Date: [Date]
# =============================================================================

# =============================================================================
# SECTION 1: Package Loading
# =============================================================================

# Core packages for microbiome analysis and visualization
library(phyloseq)   # Microbiome data structures and basic operations
library(vegan)      # Ecological statistics (PERMANOVA, distance matrices)
library(ggplot2)    # Publication-quality visualization

# Additional packages (all on CRAN) - see notes at end of script for rationale
library(dplyr)      # Data manipulation; cleaner than base R for data frames
library(tibble)     # Modern data frames; rownames_to_column() is essential here
library(scales)     # Color scale helpers for ggplot2

# =============================================================================
# SECTION 2: Configuration and File Paths
# =============================================================================

# --- Input/Output paths ---
INPUT_RDS   <- "data/probiotic_study.rds"
OUTPUT_PDF  <- "output/ordination_pcoa_bray.pdf"
OUTPUT_STATS <- "output/permanova_results.txt"  # Optional: also save to file

# --- Plot dimensions (inches) ---
PLOT_WIDTH  <- 8
PLOT_HEIGHT <- 6

# --- PERMANOVA settings ---
PERMANOVA_PERMUTATIONS <- 9999  # Increase for final analysis; 999 for quick checks
RANDOM_SEED <- 42               # For reproducibility of permutation tests

# =============================================================================
# SECTION 3: Helper Functions
# =============================================================================

# --- Function: Validate phyloseq object structure ---
# Checks that required components and metadata columns are present
validate_phyloseq <- function(ps) {
  
  # Check that object is a phyloseq instance
  if (!inherits(ps, "phyloseq")) {
    stop("ERROR: Loaded object is not a phyloseq instance. ",
         "Check that the RDS file contains a phyloseq object.")
  }
  
  # Check for required phyloseq components
  required_components <- c("otu_table", "sam_data", "tax_table")
  for (comp in required_components) {
    # ASSUMPTION: OTU table, sample data, and taxonomy are all present
    if (is.null(ps@.Data[[which(slotNames(ps) == comp)]])) {
      warning("WARNING: phyloseq object may be missing component: ", comp)
    }
  }
  
  # Check for required metadata columns
  # ASSUMPTION: Column names match exactly as specified in the data description
  required_cols <- c("sample_id", "subject_id", "timepoint", "treatment",
                     "age", "sex")
  sample_df <- as.data.frame(sample_data(ps))
  missing_cols <- setdiff(required_cols, colnames(sample_df))
  
  if (length(missing_cols) > 0) {
    stop("ERROR: Missing required metadata columns: ",
         paste(missing_cols, collapse = ", "),
         "\nAvailable columns: ", paste(colnames(sample_df), collapse = ", "))
  }
  
  message("✓ Phyloseq object structure validated successfully.")
  invisible(ps)
}

# --- Function: Check and set factor levels for key variables ---
# Ensures timepoint and treatment are factors with meaningful level ordering
prepare_metadata_factors <- function(ps) {
  
  sample_df <- as.data.frame(sample_data(ps))
  
  # ASSUMPTION: These are the expected levels; adjust if your data differs
  expected_timepoints  <- c("baseline", "week4", "week8")
  expected_treatments  <- c("placebo", "probiotic")  # placebo as reference
  
  # Validate timepoint levels
  observed_timepoints <- unique(sample_df$timepoint)
  unexpected_tp <- setdiff(observed_timepoints, expected_timepoints)
  if (length(unexpected_tp) > 0) {
    warning("WARNING: Unexpected timepoint values found: ",
            paste(unexpected_tp, collapse = ", "),
            "\nExpected: ", paste(expected_timepoints, collapse = ", "))
  }
  
  # Set ordered factor levels (baseline → week4 → week8)
  sample_df$timepoint <- factor(sample_df$timepoint,
                                levels = expected_timepoints)
  
  # Set treatment factor with placebo as reference level
  sample_df$treatment <- factor(sample_df$treatment,
                                levels = expected_treatments)
  
  # Write modified metadata back to phyloseq object
  sample_data(ps) <- sample_df
  
  message("✓ Metadata factors prepared: timepoint and treatment levels set.")
  return(ps)
}

# --- Function: Print a formatted section divider to console ---
print_section <- function(title) {
  cat("\n", strrep("=", 60), "\n", sep = "")
  cat(" ", title, "\n", sep = "")
  cat(strrep("=", 60), "\n\n", sep = "")
}

# =============================================================================
# SECTION 4: Load and Validate Data
# =============================================================================

print_section("LOADING DATA")

# Check that input file exists before attempting to load
if (!file.exists(INPUT_RDS)) {
  stop("ERROR: Input file not found at path: ", INPUT_RDS,
       "\nPlease check the file path and working directory: ", getwd())
}

# Load phyloseq object
ps_raw <- readRDS(INPUT_RDS)
message("✓ Phyloseq object loaded from: ", INPUT_RDS)

# Validate structure and prepare factors
ps_raw <- validate_phyloseq(ps_raw)
ps      <- prepare_metadata_factors(ps_raw)

# =============================================================================
# SECTION 5: Quality Control Summary
# =============================================================================

print_section("QUALITY CONTROL SUMMARY")

# Extract key counts
n_samples   <- nsamples(ps)
n_taxa      <- ntaxa(ps)
sample_df   <- as.data.frame(sample_data(ps))

# --- Sample count summary ---
cat("Total samples:  ", n_samples, "\n")
cat("Total taxa:     ", n_taxa, "\n\n")

# ASSUMPTION: 180 samples expected (30 subjects × 2 treatments × 3 timepoints)
if (n_samples != 180) {
  warning("WARNING: Expected 180 samples but found ", n_samples,
          ". Verify sample completeness.")
}

# --- Sequencing depth summary ---
sample_sums_vec <- sample_sums(ps)
cat("Sequencing depth (read counts per sample):\n")
cat("  Min:    ", min(sample_sums_vec), "\n")
cat("  Median: ", median(sample_sums_vec), "\n")
cat("  Max:    ", max(sample_sums_vec), "\n")
cat("  Mean:   ", round(mean(sample_sums_vec), 0), "\n\n")

# Flag samples with very low read counts (potential QC failures)
# ASSUMPTION: Samples with < 1000 reads are considered low-quality
LOW_READ_THRESHOLD <- 1000
low_read_samples <- names(sample_sums_vec[sample_sums_vec < LOW_READ_THRESHOLD])
if (length(low_read_samples) > 0) {
  warning("WARNING: ", length(low_read_samples),
          " sample(s) have fewer than ", LOW_READ_THRESHOLD, " reads:\n  ",
          paste(low_read_samples, collapse = ", "))
} else {
  message("✓ All samples exceed minimum read count threshold (", 
          LOW_READ_THRESHOLD, " reads).")
}

# --- Sample balance across experimental groups ---
cat("Sample distribution by treatment × timepoint:\n")
print(table(sample_df$treatment, sample_df$timepoint))
cat("\n")

# Check for missing combinations (unbalanced design)
group_counts <- table(sample_df$treatment, sample_df$timepoint)
if (any(group_counts == 0)) {
  warning("WARNING: Some treatment × timepoint combinations have zero samples. ",
          "Check for missing data.")
}

# --- Check for missing metadata values ---
key_vars <- c("subject_id", "timepoint", "treatment")
for (var in key_vars) {
  n_missing <- sum(is.na(sample_df[[var]]))
  if (n_missing > 0) {
    warning("WARNING: ", n_missing, " missing values in column '", var, "'")
  }
}
message("✓ Metadata completeness check passed for key variables.")

# =============================================================================
# SECTION 6: Data Preprocessing
# =============================================================================

print_section("DATA PREPROCESSING")

# --- Relative abundance transformation ---
# Bray-Curtis on relative abundances is standard for microbiome data.
# ALTERNATIVE: rarefaction (phyloseq::rarefy_even_depth()) is common but
# discards data; relative abundance is preferred for ordination.
# ALTERNATIVE: CLR transformation (compositions package) for Aitchison distance
# is increasingly recommended but requires different distance metric.

ps_rel <- transform_sample_counts(ps, function(x) x / sum(x))
message("✓ Counts transformed to relative abundances.")

# Verify transformation (each sample should sum to 1)
rel_sums <- sample_sums(ps_rel)
if (!all(abs(rel_sums - 1) < 1e-10)) {
  warning("WARNING: Relative abundance transformation may have failed. ",
          "Sample sums do not all equal 1.")
} else {
  message("✓ Relative abundance transformation verified (all samples sum to 1).")
}

# =============================================================================
# SECTION 7: Bray-Curtis Distance Matrix
# =============================================================================

print_section("BRAY-CURTIS DISTANCE CALCULATION")

# Calculate Bray-Curtis dissimilarity matrix using phyloseq's wrapper
# This calls vegan::vegdist() internally on the OTU table
# ASSUMPTION: OTU table is oriented with taxa as rows (phyloseq default)
bray_dist <- phyloseq::distance(ps_rel, method = "bray")

# Validate distance matrix dimensions
n_dist <- attr(bray_dist, "Size")
if (n_dist != n_samples) {
  stop("ERROR: Distance matrix size (", n_dist, ") does not match ",
       "number of samples (", n_samples, ").")
}

cat("Bray-Curtis distance matrix computed: ", n_dist, "×", n_dist, "\n")
cat("Distance range: [", round(min(bray_dist), 4), ", ",
    round(max(bray_dist), 4), "]\n\n", sep = "")

# =============================================================================
# SECTION 8: PCoA Ordination
# =============================================================================

print_section("PCoA ORDINATION")

# Perform Principal Coordinates Analysis using phyloseq's ordinate()
# This calls ape::pcoa() internally
# ALTERNATIVE: NMDS (method = "NMDS") is non-metric and often preferred for
# highly non-linear data, but PCoA is more interpretable with % variance explained
pcoa_result <- ordinate(ps_rel, method = "PCoA", distance = bray_dist)

# Extract eigenvalues to calculate variance explained
eigenvalues    <- pcoa_result$values$Eigenvalues
# Use only positive eigenvalues for variance calculation
# (negative eigenvalues arise from non-Euclidean distances and are artifacts)
pos_eigenvalues <- eigenvalues[eigenvalues > 0]
variance_explained <- pos_eigenvalues / sum(pos_eigenvalues) * 100

# Report variance explained by first three axes
cat("Variance explained by PCoA axes:\n")
for (i in 1:min(3, length(variance_explained))) {
  cat(sprintf("  PCo%d: %.2f%%\n", i, variance_explained[i]))
}
cat(sprintf("  PCo1 + PCo2 combined: %.2f%%\n\n",
            sum(variance_explained[1:2])))

# Axis labels with variance explained (for plot)
pcoa_axis1_label <- sprintf("PCo1 (%.1f%% variance)", variance_explained[1])
pcoa_axis2_label <- sprintf("PCo2 (%.1f%% variance)", variance_explained[2])

# =============================================================================
# SECTION 9: Prepare Data for Plotting
# =============================================================================

print_section("PREPARING PLOT DATA")

# Extract PCoA scores (sample coordinates) and merge with metadata
# ASSUMPTION: Row names of PCoA scores match phyloseq sample names
pcoa_scores <- as.data.frame(pcoa_result$vectors)

# Verify row name alignment before merging
if (!all(rownames(pcoa_scores) %in% rownames(sample_df))) {
  stop("ERROR: PCoA score row names do not match sample metadata row names. ",
       "Check sample name consistency.")
}

# Combine PCoA coordinates with sample metadata
plot_data <- pcoa_scores %>%
  tibble::rownames_to_column("sample_rowname") %>%
  dplyr::select(sample_rowname, Axis.1, Axis.2) %>%   # Keep first two axes
  dplyr::left_join(
    sample_df %>% tibble::rownames_to_column("sample_rowname"),
    by = "sample_rowname"
  )

# Verify no rows were lost in the join
if (nrow(plot_data) != n_samples) {
  stop("ERROR: Row count mismatch after joining PCoA scores with metadata. ",
       "Expected ", n_samples, " rows, got ", nrow(plot_data), ".")
}

message("✓ PCoA scores merged with metadata: ", nrow(plot_data), " samples.")

# =============================================================================
# SECTION 10: Create Ordination Plot
# =============================================================================

print_section("CREATING ORDINATION PLOT")

# --- Define visual aesthetics ---
# Color palette: colorblind-friendly (Wong 2011 palette)
treatment_colors <- c(
  "placebo"   = "#0072B2",   # Blue
  "probiotic" = "#D55E00"    # Vermillion
)

# Shape palette: distinct shapes for three timepoints
timepoint_shapes <- c(
  "baseline" = 16,   # Filled circle
  "week4"    = 17,   # Filled triangle
  "week8"    = 15    # Filled square
)

# --- Calculate group centroids for centroid overlay ---
# Centroids help visualize group-level trends in the ordination
centroids <- plot_data %>%
  dplyr::group_by(treatment, timepoint) %>%
  dplyr::summarise(
    centroid_x = mean(Axis.1),
    centroid_y = mean(Axis.2),
    .groups = "drop"
  )

# --- Build the ggplot ---
ordination_plot <- ggplot(plot_data,
                          aes(x = Axis.1, y = Axis.2,
                              color = treatment,
                              shape = timepoint)) +
  
  # Individual sample points
  geom_point(size = 2.5, alpha = 0.7, stroke = 0.3) +
  
  # Centroid points (larger, with black border for visibility)
  geom_point(data = centroids,
             aes(x = centroid_x, y = centroid_y,
                 color = treatment, shape = timepoint),
             size = 5, stroke = 1.2,
             show.legend = FALSE) +
  
  # Lines connecting centroids across timepoints within each treatment
  # This visualizes the trajectory of community change over time
  geom_path(data = centroids,
            aes(x = centroid_x, y = centroid_y,
                group = treatment, color = treatment),
            linewidth = 0.8, linetype = "dashed",
            arrow = arrow(length = unit(0.2, "cm"),
                          type = "closed", ends = "last"),
            show.legend = FALSE) +
  
  # Reference lines at origin
  geom_hline(yintercept = 0, linetype = "dotted",
             color = "grey60", linewidth = 0.4) +
  geom_vline(xintercept = 0, linetype = "dotted",
             color = "grey60", linewidth = 0.4) +
  
  # Apply custom color and shape scales
  scale_color_manual(
    values = treatment_colors,
    name   = "Treatment",
    labels = c("placebo" = "Placebo", "probiotic" = "Probiotic")
  ) +
  scale_shape_manual(
    values = timepoint_shapes,
    name   = "Timepoint",
    labels = c("baseline" = "Baseline", "week4" = "Week 4", "week8" = "Week 8")
  ) +
  
  # Axis labels with variance explained
  labs(
    title    = "Gut Microbiome Community Composition",
    subtitle = "PCoA of Bray-Curtis Dissimilarity",
    x        = pcoa_axis1_label,
    y        = pcoa_axis2_label,
    caption  = paste0("Large symbols = group centroids; dashed arrows = ",
                      "temporal trajectory\nn = ", n_samples, " samples, ",
                      n_taxa, " taxa")
  ) +
  
  # Publication-quality theme
  theme_bw(base_size = 12) +
  theme(
    # Title formatting
    plot.title      = element_text(face = "bold", size = 13, hjust = 0),
    plot.subtitle   = element_text(size = 10, color = "grey40", hjust = 0),
    plot.caption    = element_text(size = 8, color = "grey50", hjust = 0),
    
    # Legend formatting
    legend.position  = "right",
    legend.title     = element_text(face = "bold", size = 10),
    legend.text      = element_text(size = 9),
    legend.key.size  = unit(0.8, "lines"),
    legend.box       = "vertical",
    
    # Panel formatting
    panel.grid.minor = element_blank(),
    panel.grid.major = element_line(color = "grey92", linewidth = 0.3),
    
    # Axis formatting
    axis.title = element_text(size = 10),
    axis.text  = element_text(size = 9)
  ) +
  
  # Ensure equal scaling on both axes (important for distance-based ordination)
  coord_equal()

# Preview plot dimensions
message("✓ Ordination plot created.")

# =============================================================================
# SECTION 11: Save Ordination Plot
# =============================================================================

print_section("SAVING PLOT")

# Create output directory if it doesn't exist
output_dir <- dirname(OUTPUT_PDF)
if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
  message("✓ Created output directory: ", output_dir)
}

# Save as PDF (vector format for publication; scales without quality loss)
ggsave(
  filename = OUTPUT_PDF,
  plot     = ordination_plot,
  width    = PLOT_WIDTH,
  height   = PLOT_HEIGHT,
  units    = "in",
  device   = "pdf",
  useDingbats = FALSE   # Ensures compatibility with Adobe Illustrator
)

message("✓ Ordination plot saved to: ", OUTPUT_PDF)

# Also save as PNG for quick review (300 DPI for publication quality)
OUTPUT_PNG <- sub("\\.pdf$", ".png", OUTPUT_PDF)
ggsave(
  filename = OUTPUT_PNG,
  plot     = ordination_plot,
  width    = PLOT_WIDTH,
  height   = PLOT_HEIGHT,
  units    = "in",
  dpi      = 300
)
message("✓ PNG preview saved to: ", OUTPUT_PNG)

# =============================================================================
# SECTION 12: PERMANOVA Analysis
# =============================================================================

print_section("PERMANOVA ANALYSIS")

# --- Prepare inputs for vegan::adonis2() ---

# Convert distance object to matrix (required by adonis2)
bray_matrix <- as.matrix(bray_dist)

# Ensure metadata row order matches distance matrix row order
# This is critical: misalignment causes silent errors in PERMANOVA
metadata_ordered <- sample_df[rownames(bray_matrix), ]

# Verify alignment
if (!identical(rownames(bray_matrix), rownames(metadata_ordered))) {
  stop("ERROR: Distance matrix row names do not align with metadata row names. ",
       "Cannot proceed with PERMANOVA.")
}
message("✓ Distance matrix and metadata alignment verified.")

# --- Set random seed for reproducibility ---
set.seed(RANDOM_SEED)

# --- PERMANOVA Model 1: Treatment × Timepoint interaction ---
# 
# Formula explanation:
#   bray_matrix ~ treatment * timepoint
#   The * expands to: treatment + timepoint + treatment:timepoint
#
# Blocking by subject_id accounts for repeated measures structure:
#   - Permutations are restricted within subjects
#   - This prevents pseudoreplication from treating repeated samples as independent
#   - ALTERNATIVE: Use strata = metadata_ordered$subject_id in older vegan versions
#
# by = "margin" tests each term after accounting for all others (Type III SS)
# ALTERNATIVE: by = "terms" uses sequential (Type I) SS; order-dependent

cat("Running PERMANOVA: treatment × timepoint (blocked by subject)...\n")
cat("Permutations:", PERMANOVA_PERMUTATIONS, "\n\n")

permanova_interaction <- vegan::adonis2(
  formula      = bray_matrix ~ treatment * timepoint,
  data         = metadata_ordered,
  permutations = PERMANOVA_PERMUTATIONS,
  method       = "bray",          # Redundant here (using pre-computed matrix) but explicit
  by           = "margin",        # Marginal (Type III) tests
  strata       = metadata_ordered$subject_id  # Block permutations within subjects
)

# --- PERMANOVA Model 2: Main effects only (for comparison) ---
# Useful if interaction is non-significant
permanova_main <- vegan::adonis2(
  formula      = bray_matrix ~ treatment + timepoint,
  data         = metadata_ordered,
  permutations = PERMANOVA_PERMUTATIONS,
  by           = "margin",
  strata       = metadata_ordered$subject_id
)

# =============================================================================
# SECTION 13: Homogeneity of Dispersion Test
# =============================================================================

# PERMANOVA assumes homogeneous within-group dispersion (similar to ANOVA homoscedasticity)
# betadisper() tests this assumption; significant result means PERMANOVA results
# should be interpreted cautiously (differences may reflect dispersion, not location)

cat("Testing homogeneity of dispersion (PERMANOVA assumption check)...\n\n")

# Test dispersion by treatment group
betadisp_treatment <- vegan::betadisper(bray_dist,
                                        group = metadata_ordered$treatment)
betadisp_treatment_test <- vegan::permutest(betadisp_treatment,
                                            permutations = PERMANOVA_PERMUTATIONS)

# Test dispersion by timepoint
betadisp_timepoint <- vegan::betadisper(bray_dist,
                                        group = metadata_ordered$timepoint)
betadisp_timepoint_test <- vegan::permutest(betadisp_timepoint,
                                            permutations = PERMANOVA_PERMUTATIONS)

# =============================================================================
# SECTION 14: Print Statistical Results
# =============================================================================

print_section("STATISTICAL RESULTS SUMMARY")

# --- PERMANOVA: Interaction model ---
cat("─── PERMANOVA: Treatment × Timepoint Interaction Model ───\n")
cat("Formula: Bray-Curtis ~ treatment * timepoint\n")
cat("Blocking: subject_id (accounts for repeated measures)\n")
cat("Permutations:", PERMANOVA_PERMUTATIONS, "| Seed:", RANDOM_SEED, "\n\n")
print(permanova_interaction)

cat("\n")

# --- PERMANOVA: Main effects model ---
cat("─── PERMANOVA: Main Effects Model ───\n")
cat("Formula: Bray-Curtis ~ treatment + timepoint\n\n")
print(permanova_main)

cat("\n")

# --- Betadisper results ---
cat("─── Homogeneity of Dispersion Tests ───\n\n")

cat("By Treatment:\n")
print(betadisp_treatment_test)

cat("\nBy Timepoint:\n")
print(betadisp_timepoint_test)

# --- Interpretation guidance ---
cat("\n─── Interpretation Notes ───\n")
cat("• R²: Proportion of variance explained by each term\n")
cat("• Pr(>F): p-value from permutation test\n")
cat("• Strata blocking restricts permutations within subjects\n")
cat("  (conservative; appropriate for repeated measures designs)\n")
cat("• If betadisper p < 0.05: PERMANOVA differences may partly\n")
cat("  reflect dispersion differences, not just centroid shifts\n")
cat("• Consider pairwise tests (pairwiseAdonis package) for\n")
cat("  post-hoc comparisons if overall test is significant\n\n")

# =============================================================================
# SECTION 15: Save Statistical Results to File
# =============================================================================

# Capture all output and write to text file for record-keeping
sink(OUTPUT_STATS)

cat("PERMANOVA RESULTS - Probiotic Intervention Study\n")
cat("Generated:", format(Sys.time(), "%Y-%m-%d %H:%M:%S"), "\n")
cat("Input file:", INPUT_RDS, "\n")
cat("Permutations:", PERMANOVA_PERMUTATIONS, "| Seed:", RANDOM_SEED, "\n")
cat(strrep("=", 60), "\n\n")

cat("PERMANOVA: Treatment × Timepoint Interaction\n")
print(permanova_interaction)

cat("\nPERMANOVA: Main Effects\n")
print(permanova_main)

cat("\nBetadisper - Treatment:\n")
print(betadisp_treatment_test)

cat("\nBetadisper - Timepoint:\n")
print(betadisp_timepoint_test)

sink()  # Close the sink

message("✓ Statistical results saved to: ", OUTPUT_STATS)

# =============================================================================
# SECTION 16: Session Information
# =============================================================================

print_section("SESSION INFORMATION")
sessionInfo()

# =============================================================================
# END OF SCRIPT
# =============================================================================
```

---

## Required Packages

| Package | Source | Version Tested | Purpose |
|---|---|---|---|
| `phyloseq` | Bioconductor | ≥ 1.42 | Microbiome data structures, distance calculation, ordination |
| `vegan` | CRAN | ≥ 2.6 | PERMANOVA (`adonis2`), betadisper |
| `ggplot2` | CRAN | ≥ 3.4 | Visualization |
| `dplyr` | CRAN | ≥ 1.1 | Data manipulation |
| `tibble` | CRAN | ≥ 3.2 | `rownames_to_column()` for safe joins |
| `scales` | CRAN | ≥ 1.2 | Color scale utilities |

**Why `dplyr`/`tibble` over base R?** The join between PCoA scores and metadata is error-prone with `merge()` because row order is not guaranteed. `dplyr::left_join()` with explicit key columns is safer and more readable.

---

## Assumptions Made

1. **OTU table orientation**: Taxa as rows, samples as columns (phyloseq default). If transposed, `phyloseq::distance()` will still work correctly, but verify with `taxa_are_rows(ps)`.

2. **Column names match exactly**: `sample_id`, `subject_id`, `timepoint`, `treatment`, `age`, `sex`. The validation function will error clearly if they don't.

3. **Timepoint values**: Exactly `"baseline"`, `"week4"`, `"week8"` (case-sensitive). The script warns if unexpected values appear.

4. **Balanced design**: 30 subjects × 2 treatments × 3 timepoints = 180 samples. The script warns if this doesn't hold but continues.

5. **`adonis2` strata behavior**: Blocking by `subject_id` restricts permutations within subjects. This is conservative and appropriate for repeated measures, but note that `strata` in `adonis2` does not model the random effect — it only constrains permutations.

6. **No rarefaction applied**: Relative abundance transformation is used instead. If your samples have extreme depth variation (>10× range), consider rarefaction or DESeq2-style normalization.

---

## Suggested Validation Checks

### Before Running
```r
# Check working directory
getwd()

# Verify file exists and is readable
file.exists("data/probiotic_study.rds")

# Quick peek at the object
ps_test <- readRDS("data/probiotic_study.rds")
class(ps_test)          # Should be "phyloseq"
taxa_are_rows(ps_test)  # Should be TRUE
head(sample_data(ps_test))
```

### After Running
```r
# 1. Verify distance matrix is symmetric
all(bray_matrix == t(bray_matrix))  # Should be TRUE

# 2. Check PCoA scores are not all zero
summary(pcoa_result$vectors[, 1:2])

# 3. Confirm plot renders correctly before saving
print(ordination_plot)

# 4. Sanity check: R² values in PERMANOVA should sum to < 1
sum(permanova_interaction$R2, na.rm = TRUE)  # Should be < 1

# 5. Check subject_id appears correct number of times (3 per subject)
table(table(sample_df$subject_id))  # Should show all 3s
```

### Potential Issues to Investigate
- **If PERMANOVA p-values are all 1.0**: The `strata` argument may be too restrictive given your sample size. Try without blocking first to confirm the test is running.
- **If betadisper is significant**: Report it alongside PERMANOVA and consider visualizing dispersion with `plot(betadisp_treatment)`.
- **If PCo1 + PCo2 < 20%**: Consider reporting PCo3 as well, or switching to NMDS which optimizes 2D representation directly.
````

## Assessment

_Machine-suggested (UNCONFIRMED) — drafted by Claude Opus 4.7 on 2026-06-26 (re-triage after max_tokens bump and re-capture). An author must independently read the Model Output above and set the real Recommendation. Anything labeled here is triage, not domain expert review._

**Machine triage:** Output is complete and ends cleanly (script + required packages table + assumptions + validation checks). Follows requested format closely with labelled sections. Adds extra CRAN packages (`dplyr`, `tibble`, `scales`) beyond the spec'd `phyloseq`/`vegan`/`ggplot2` but justifies them inline as the prompt allows. Uses `adonis2` with `strata = subject_id` for repeated-measures blocking (older API; vegan now prefers `permutations = how(blocks = ...)`) — both still work but the newer pattern is preferred; this may cause confusion in current vegan versions. Includes a `betadisper` dispersion check, which is good practice. Code is verbose (centroid overlays, low-read warnings, alignment assertions) but compiles to a coherent pipeline. I cannot verify the slot-introspection used in `validate_phyloseq` (`ps@.Data[[which(slotNames(ps) == comp)]]`) works correctly across phyloseq versions, nor that PERMANOVA blocking + dispersion test are the appropriate statistical approach for this design.

**Suggested verdict (UNCONFIRMED):** Pass with notes

**What still needs human verification:**
- That `strata = metadata_ordered$subject_id` in `adonis2()` still behaves as expected in the user's vegan version (current API prefers `how(blocks=...)`)
- The phyloseq slot introspection (`ps@.Data[[which(slotNames(ps) == comp)]]`) for component checking — fragile across S4 class versions
- Whether the added dplyr/tibble/scales dependencies are acceptable to the user
- Statistical correctness of PERMANOVA + main-effects + dispersion sub-tests for this design

**Local code check:** Syntax PASS across 3 block(s) · 6/6 imports available.

## Overall Assessment
- **Recommendation:** Pass
- **Notes:** Alex Alexiev (2026-06-29): **What still needs human verification:**
- That `strata = metadata_ordered$subject_id` in `adonis2()` still behaves as expected in the user's vegan version (current API prefers `how(blocks=...)`): should still work
- The phyloseq slot introspection (`ps@.Data[[which(slotNames(ps) == comp)]]`) for component checking — fragile across S4 class versions: NA, haven't used before personally, but looking over how it's written, it should work fine
- Whether the added dplyr/tibble/scales dependencies are acceptable to the user: yes
- Statistical correctness of PERMANOVA + main-effects + dispersion sub-tests for this design: yes

## Verification Steps Tested
_Which verification requirements from the prompt were checked, and results._
