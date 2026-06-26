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
# Core packages:
#   - phyloseq: microbiome data handling (Bioconductor)
#   - vegan: ecological statistics including PERMANOVA (CRAN)
#   - ggplot2: publication-quality plotting (CRAN, via tidyverse)
# Additional packages:
#   - dplyr: data manipulation, cleaner than base R for metadata handling (CRAN)
#   - ggrepel: non-overlapping labels if sample labels are needed (CRAN)
#   - patchwork: combining multiple plots into one figure (CRAN)
#   - scales: axis formatting and color palette helpers (CRAN)

required_packages <- c("phyloseq", "vegan", "ggplot2", "dplyr",
                        "ggrepel", "patchwork", "scales")

# Check and alert for any missing packages before attempting to load
missing_packages <- required_packages[
  !sapply(required_packages, requireNamespace, quietly = TRUE)
]

if (length(missing_packages) > 0) {
  stop(
    "The following required packages are not installed:\n",
    paste(" -", missing_packages, collapse = "\n"), "\n\n",
    "Install CRAN packages with: install.packages(c(",
    paste0('"', missing_packages, '"', collapse = ", "), "))\n",
    "Install Bioconductor packages with:\n",
    "  BiocManager::install('phyloseq')"
  )
}

suppressPackageStartupMessages({
  library(phyloseq)
  library(vegan)
  library(ggplot2)
  library(dplyr)
  library(ggrepel)
  library(patchwork)
  library(scales)
})

cat("All packages loaded successfully.\n")

# =============================================================================
# SECTION 2: Configuration and File Paths
# =============================================================================
# Centralizing paths and parameters here makes the script easier to adapt

# --- Input/Output paths ---
INPUT_RDS_PATH  <- "data/probiotic_study.rds"
OUTPUT_PDF_PATH <- "results/ordination_pcoa.pdf"
OUTPUT_STATS_PATH <- "results/permanova_results.txt"  # optional text file output

# --- Analysis parameters ---
# ASSUMPTION: Rarefaction depth will be determined from data (see QC section).
# Set to NULL to use the minimum sample depth; override with a specific integer
# if you have a biologically motivated cutoff.
RAREFY_DEPTH <- NULL  # e.g., set to 10000 to force a specific depth

# --- Plot parameters ---
PDF_WIDTH  <- 10   # inches
PDF_HEIGHT <- 8    # inches
POINT_SIZE <- 3
POINT_ALPHA <- 0.85

# --- Expected metadata columns (used in validation checks) ---
# ASSUMPTION: These column names match exactly what is in the phyloseq sample_data
EXPECTED_COLS <- c("sample_id", "subject_id", "timepoint", "treatment",
                   "age", "sex")

# --- Factor level ordering for plots ---
# ASSUMPTION: These are the only levels present; adjust if your data differs
TIMEPOINT_LEVELS  <- c("baseline", "week4", "week8")
TREATMENT_LEVELS  <- c("placebo", "probiotic")  # placebo first as reference

# =============================================================================
# SECTION 3: Load Data and Basic Validation
# =============================================================================

cat("\n--- Loading phyloseq object ---\n")

# Check that the input file exists before attempting to load
if (!file.exists(INPUT_RDS_PATH)) {
  stop(
    "Input file not found: ", INPUT_RDS_PATH, "\n",
    "Check that your working directory is set correctly with getwd(), ",
    "and that the file path is accurate."
  )
}

ps_raw <- readRDS(INPUT_RDS_PATH)

# Validate that the loaded object is actually a phyloseq object
if (!inherits(ps_raw, "phyloseq")) {
  stop(
    "The loaded RDS file does not contain a phyloseq object.\n",
    "Object class found: ", class(ps_raw)
  )
}

cat("Phyloseq object loaded successfully.\n")

# =============================================================================
# SECTION 4: Quality Control and Descriptive Summary
# =============================================================================

cat("\n--- Quality Control Summary ---\n")

# --- Basic counts ---
n_samples <- nsamples(ps_raw)
n_taxa    <- ntaxa(ps_raw)
cat(sprintf("  Samples : %d (expected: 180)\n", n_samples))
cat(sprintf("  Taxa    : %d\n", n_taxa))

# Warn if sample count is unexpected
if (n_samples != 180) {
  warning(
    sprintf(
      "Expected 180 samples but found %d. ",
      n_samples
    ),
    "Verify that no samples were lost during upstream processing."
  )
}

# --- Metadata validation ---
sample_metadata <- as(sample_data(ps_raw), "data.frame")

missing_cols <- setdiff(EXPECTED_COLS, colnames(sample_metadata))
if (length(missing_cols) > 0) {
  stop(
    "The following expected metadata columns are missing:\n",
    paste(" -", missing_cols, collapse = "\n"), "\n",
    "Available columns: ", paste(colnames(sample_metadata), collapse = ", ")
  )
}

cat("  All expected metadata columns present.\n")

# --- Check for missing values in key variables ---
key_vars <- c("subject_id", "timepoint", "treatment")
for (var in key_vars) {
  n_missing <- sum(is.na(sample_metadata[[var]]))
  if (n_missing > 0) {
    warning(sprintf("Column '%s' has %d missing value(s). ", var, n_missing),
            "These samples may be dropped during analysis.")
  }
}

# --- Enforce factor levels ---
# ASSUMPTION: All timepoint and treatment values match the defined levels exactly
sample_metadata$timepoint <- factor(sample_metadata$timepoint,
                                    levels = TIMEPOINT_LEVELS)
sample_metadata$treatment <- factor(sample_metadata$treatment,
                                    levels = TREATMENT_LEVELS)

# Check for unexpected factor levels (e.g., typos in metadata)
unexpected_timepoints <- levels(droplevels(
  factor(sample_metadata$timepoint[
    !sample_metadata$timepoint %in% TIMEPOINT_LEVELS
  ])
))
if (length(unexpected_timepoints) > 0) {
  warning("Unexpected timepoint values found: ",
          paste(unexpected_timepoints, collapse = ", "))
}

# Write validated metadata back to the phyloseq object
sample_data(ps_raw) <- sample_data(sample_metadata)

# --- Sample depth summary ---
sample_depths <- sample_sums(ps_raw)
cat(sprintf(
  "  Read depth: min = %s, median = %s, max = %s\n",
  format(min(sample_depths),    big.mark = ","),
  format(median(sample_depths), big.mark = ","),
  format(max(sample_depths),    big.mark = ",")
))

# Flag samples with very low read counts (potential QC failures)
# ASSUMPTION: Samples with fewer than 1000 reads are considered low-quality
LOW_DEPTH_THRESHOLD <- 1000
low_depth_samples <- names(sample_depths[sample_depths < LOW_DEPTH_THRESHOLD])
if (length(low_depth_samples) > 0) {
  warning(
    length(low_depth_samples), " sample(s) have fewer than ",
    LOW_DEPTH_THRESHOLD, " reads:\n",
    paste(" -", low_depth_samples, collapse = "\n"), "\n",
    "Consider removing these before rarefaction."
  )
}

# --- Experimental design check ---
design_table <- table(
  sample_metadata$treatment,
  sample_metadata$timepoint
)
cat("\n  Sample counts by treatment × timepoint:\n")
print(design_table)

# =============================================================================
# SECTION 5: Data Preprocessing — Rarefaction
# =============================================================================
# RATIONALE: Bray-Curtis distances are sensitive to differences in sequencing
# depth. Rarefaction normalizes library sizes before calculating distances.
#
# ALTERNATIVE: Some researchers prefer not to rarefy and instead use
# variance-stabilizing transformations (e.g., DESeq2's VST) or relative
# abundance. If you prefer that approach, replace this section with:
#   ps_norm <- transform_sample_counts(ps_raw, function(x) x / sum(x))
# and skip the rarefaction step.

cat("\n--- Rarefaction ---\n")

# Determine rarefaction depth
if (is.null(RAREFY_DEPTH)) {
  rarefy_depth <- min(sample_sums(ps_raw))
  cat(sprintf(
    "  RAREFY_DEPTH not specified; using minimum sample depth: %s reads\n",
    format(rarefy_depth, big.mark = ",")
  ))
} else {
  rarefy_depth <- RAREFY_DEPTH
  cat(sprintf("  Using specified rarefaction depth: %s reads\n",
              format(rarefy_depth, big.mark = ",")))
  
  # Check that all samples meet the specified depth
  samples_below_depth <- sum(sample_sums(ps_raw) < rarefy_depth)
  if (samples_below_depth > 0) {
    warning(
      samples_below_depth, " sample(s) have fewer reads than the specified ",
      "rarefaction depth (", format(rarefy_depth, big.mark = ","), ") ",
      "and will be dropped."
    )
  }
}

# Rarefy to even depth
# set.seed ensures reproducibility of the random subsampling
set.seed(42)
ps_rarefied <- rarefy_even_depth(
  ps_raw,
  sample.size = rarefy_depth,
  rngseed     = FALSE,  # we set seed manually above
  replace     = FALSE,  # sample without replacement (standard practice)
  trimOTUs    = TRUE,   # remove OTUs that become zero after rarefaction
  verbose     = FALSE
)

cat(sprintf(
  "  After rarefaction: %d samples, %d taxa\n",
  nsamples(ps_rarefied),
  ntaxa(ps_rarefied)
))

# Warn if samples were dropped during rarefaction
if (nsamples(ps_rarefied) < n_samples) {
  cat(sprintf(
    "  WARNING: %d sample(s) were dropped during rarefaction.\n",
    n_samples - nsamples(ps_rarefied)
  ))
}

# =============================================================================
# SECTION 6: Bray-Curtis Distance Matrix
# =============================================================================

cat("\n--- Calculating Bray-Curtis distances ---\n")

# phyloseq's distance() wraps vegan's vegdist() for phyloseq objects
# ALTERNATIVE: Use UniFrac distances if a phylogenetic tree is available:
#   bray_dist <- UniFrac(ps_rarefied, weighted = TRUE)
bray_dist <- distance(ps_rarefied, method = "bray")

# Basic sanity check on the distance matrix
dist_matrix <- as.matrix(bray_dist)
if (any(is.na(dist_matrix))) {
  stop("NA values found in the Bray-Curtis distance matrix. ",
       "Check for samples with all-zero counts after rarefaction.")
}

cat(sprintf(
  "  Distance matrix: %d × %d\n",
  nrow(dist_matrix), ncol(dist_matrix)
))
cat(sprintf(
  "  Distance range: %.4f – %.4f\n",
  min(dist_matrix[dist_matrix > 0]),
  max(dist_matrix)
))

# =============================================================================
# SECTION 7: PCoA Ordination
# =============================================================================

cat("\n--- Running PCoA ordination ---\n")

# phyloseq's ordinate() wraps vegan's cmdscale() for PCoA
pcoa_result <- ordinate(ps_rarefied, method = "PCoA", distance = bray_dist)

# Extract variance explained by each axis
eigenvalues    <- pcoa_result$values$Eigenvalues
# Use only positive eigenvalues for variance calculation
# (negative eigenvalues arise from non-Euclidean distances and are artifacts)
positive_eigen <- eigenvalues[eigenvalues > 0]
variance_explained <- positive_eigen / sum(positive_eigen) * 100

pct_axis1 <- round(variance_explained[1], 1)
pct_axis2 <- round(variance_explained[2], 1)

cat(sprintf("  Axis 1 explains: %.1f%% of variance\n", pct_axis1))
cat(sprintf("  Axis 2 explains: %.1f%% of variance\n", pct_axis2))
cat(sprintf("  Axes 1+2 combined: %.1f%%\n", pct_axis1 + pct_axis2))

# =============================================================================
# SECTION 8: Prepare Plotting Data
# =============================================================================

cat("\n--- Preparing plot data ---\n")

# Extract PCoA coordinates and merge with sample metadata
# ASSUMPTION: Row names of the PCoA scores match phyloseq sample names
pcoa_coords <- as.data.frame(pcoa_result$vectors[, 1:2])
colnames(pcoa_coords) <- c("Axis1", "Axis2")
pcoa_coords$sample_id <- rownames(pcoa_coords)

# Pull metadata from the rarefied phyloseq object (may differ from ps_raw
# if samples were dropped during rarefaction)
plot_metadata <- as(sample_data(ps_rarefied), "data.frame") %>%
  select(sample_id, subject_id, timepoint, treatment, age, sex)

# Join coordinates with metadata
plot_data <- pcoa_coords %>%
  left_join(plot_metadata, by = "sample_id")

# Verify the join worked correctly
if (any(is.na(plot_data$treatment))) {
  warning("Some samples could not be matched to metadata after join. ",
          "Check that sample_id values are consistent.")
}

cat(sprintf("  Plot data prepared: %d points\n", nrow(plot_data)))

# =============================================================================
# SECTION 9: Calculate Group Centroids (for visual clarity)
# =============================================================================
# Adding centroids and connecting lines helps visualize treatment trajectories
# across timepoints — particularly useful for repeated-measures designs

centroids <- plot_data %>%
  group_by(treatment, timepoint) %>%
  summarise(
    Axis1 = mean(Axis1),
    Axis2 = mean(Axis2),
    .groups = "drop"
  )

# =============================================================================
# SECTION 10: Build the Ordination Plot
# =============================================================================

cat("\n--- Building ordination plot ---\n")

# --- Color and shape palettes ---
# Color-blind-friendly palette for treatment groups
treatment_colors <- c(
  "placebo"   = "#4393C3",  # blue
  "probiotic" = "#D6604D"   # red-orange
)

# Shape palette for timepoints (filled shapes for better visibility)
timepoint_shapes <- c(
  "baseline" = 21,  # circle
  "week4"    = 22,  # square
  "week8"    = 24   # triangle
)

# --- Axis labels with variance explained ---
x_label <- sprintf("PCoA Axis 1 (%.1f%%)", pct_axis1)
y_label <- sprintf("PCoA Axis 2 (%.1f%%)", pct_axis2)

# --- Main scatter plot ---
p_main <- ggplot(plot_data, aes(x = Axis1, y = Axis2)) +
  
  # Draw individual sample points
  # Using fill aesthetic with shape 21-25 allows separate color for border
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
