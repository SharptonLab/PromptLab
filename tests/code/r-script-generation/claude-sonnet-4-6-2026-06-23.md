# Test Results: code/r-script-generation.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-23.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** code/r-script-generation.md
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
Context: I am a {RESEARCHER_ROLE} working on {RESEARCH_CONTEXT}. I need an R script to {GENERAL_GOAL}.

Data description:
- Input: {DESCRIBE_INPUT_DATA: format, columns, data types, source}
- Sample size: {APPROXIMATE_N}
- Key variables: {LIST_KEY_VARIABLES_AND_TYPES}

Task: Write an R script that accomplishes the following:
{SPECIFIC_TASK_DESCRIPTION}

Requirements:
1. **Packages**: Use {PREFERRED_PACKAGES: e.g., "tidyverse for data manipulation," "phyloseq for microbiome analysis"}. If you suggest other packages, explain why.

2. **Code style**:
   - Include comments explaining each major step
   - Use descriptive variable names
   - Group related operations into labeled sections

3. **Input/Output**:
   - Input file path: {INPUT_PATH_OR_PLACEHOLDER}
   - Output: {DESCRIBE_DESIRED_OUTPUT: file, plot, statistics}

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
1. Packages: phyloseq, vegan, ggplot2
2. Code style: Well-commented with section headers
3. Input file path: "data/probiotic_study.rds"
4. Output: Publication-quality figure, statistical summary to console
```

## Model Output
```
# Microbiome Ordination Analysis: Probiotic Intervention Study
# Author: [Your Name]
# Date: [Date]
# Description: PCoA ordination and PERMANOVA analysis of probiotic intervention
#              microbiome data with repeated measures design

# ============================================================
# SECTION 1: SETUP - Load packages and define parameters
# ============================================================

# Load required packages
# NOTE: Install with:
#   install.packages(c("tidyverse", "ggplot2"))
#   BiocManager::install("phyloseq")
#   install.packages("vegan")

suppressPackageStartupMessages({
  library(phyloseq)   # Microbiome data structures and basic operations
  library(vegan)      # Ecological statistics including PERMANOVA (adonis2)
  library(ggplot2)    # Publication-quality plotting
  library(dplyr)      # Data manipulation
  library(tidyr)      # Data tidying
})

# --- User-defined parameters (edit these as needed) ---
INPUT_PATH       <- "data/probiotic_study.rds"
OUTPUT_PLOT_PATH <- "results/pcoa_ordination.pdf"
OUTPUT_STATS_PATH <- "results/permanova_results.txt"

# Plotting aesthetics
TREATMENT_COLORS <- c("probiotic" = "#2166AC",   # Blue
                       "placebo"   = "#D6604D")   # Red/orange
TIMEPOINT_SHAPES <- c("baseline" = 21,            # Circle
                       "week4"    = 22,            # Square
                       "week8"    = 24)            # Triangle

# PERMANOVA parameters
N_PERMUTATIONS <- 999   # Increase to 9999 for final publication

# ============================================================
# SECTION 2: DATA LOADING AND VALIDATION
# ============================================================

cat("=== Loading Data ===\n")

# --- Load phyloseq object ---
# ASSUMPTION: File is a valid phyloseq RDS object with otu_table,
#             tax_table, and sample_data components
if (!file.exists(INPUT_PATH)) {
  stop(
    "Input file not found: ", INPUT_PATH,
    "\nCheck your working directory with getwd() and verify the file path."
  )
}

ps <- readRDS(INPUT_PATH)

# --- Validate phyloseq object structure ---
cat("Validating phyloseq object structure...\n")

# Check that required components are present
required_components <- c("otu_table", "tax_table", "sam_data")
component_present <- c(
  !is.null(otu_table(ps)),
  !is.null(tax_table(ps)),
  !is.null(sample_data(ps))
)
names(component_present) <- required_components

if (!all(component_present)) {
  missing <- names(component_present)[!component_present]
  stop("Phyloseq object is missing required components: ",
       paste(missing, collapse = ", "))
}

# Check that required metadata columns exist
# ASSUMPTION: Sample data contains these exact column names
required_cols <- c("sample_id", "subject_id", "timepoint", "treatment",
                   "age", "sex")
actual_cols   <- colnames(sample_data(ps))
missing_cols  <- setdiff(required_cols, actual_cols)

if (length(missing_cols) > 0) {
  stop(
    "Missing required metadata columns: ",
    paste(missing_cols, collapse = ", "),
    "\nAvailable columns: ", paste(actual_cols, collapse = ", ")
  )
}

# ============================================================
# SECTION 3: QUALITY CONTROL
# ============================================================

cat("\n=== Quality Control ===\n")

# --- Basic counts ---
n_samples <- nsamples(ps)
n_taxa    <- ntaxa(ps)
cat(sprintf("Samples: %d (expected: 180)\n", n_samples))
cat(sprintf("Taxa:    %d\n", n_taxa))

# Warn if sample count is unexpected
if (n_samples != 180) {
  warning(sprintf(
    "Expected 180 samples but found %d. Verify data completeness.",
    n_samples
  ))
}

# --- Sequencing depth summary ---
sample_sums_vec <- sample_sums(ps)
cat("\nSequencing depth summary (reads per sample):\n")
print(summary(sample_sums_vec))

# Flag samples with very low read counts (potential QC failures)
# ASSUMPTION: Samples with < 1000 reads may be unreliable
LOW_READ_THRESHOLD <- 1000
low_read_samples <- names(sample_sums_vec[sample_sums_vec < LOW_READ_THRESHOLD])

if (length(low_read_samples) > 0) {
  warning(sprintf(
    "%d sample(s) have fewer than %d reads: %s\n",
    length(low_read_samples),
    LOW_READ_THRESHOLD,
    paste(low_read_samples, collapse = ", ")
  ))
} else {
  cat(sprintf("All samples exceed %d read threshold. ✓\n", LOW_READ_THRESHOLD))
}

# --- Check factor levels in metadata ---
sample_df <- as(sample_data(ps), "data.frame")

# Convert grouping variables to factors with explicit level ordering
# ASSUMPTION: These are the complete set of levels for each variable
sample_df$timepoint <- factor(sample_df$timepoint,
                               levels = c("baseline", "week4", "week8"))
sample_df$treatment <- factor(sample_df$treatment,
                               levels = c("probiotic", "placebo"))

# Check for unexpected factor levels (e.g., typos in metadata)
unexpected_timepoints <- setdiff(levels(sample_df$timepoint),
                                  c("baseline", "week4", "week8"))
unexpected_treatments <- setdiff(levels(sample_df$treatment),
                                  c("probiotic", "placebo"))

if (length(unexpected_timepoints) > 0) {
  warning("Unexpected timepoint levels: ",
          paste(unexpected_timepoints, collapse = ", "))
}
if (length(unexpected_treatments) > 0) {
  warning("Unexpected treatment levels: ",
          paste(unexpected_treatments, collapse = ", "))
}

# --- Sample balance check ---
cat("\nSample counts by treatment × timepoint:\n")
balance_table <- table(treatment  = sample_df$treatment,
                        timepoint  = sample_df$timepoint)
print(balance_table)

# Check for missing combinations
if (any(balance_table == 0)) {
  warning("Some treatment × timepoint combinations have zero samples!")
}

# Update sample_data with corrected factor levels
sample_data(ps) <- sample_data(sample_df)

# ============================================================
# SECTION 4: NORMALIZATION
# ============================================================

cat("\n=== Normalization ===\n")

# Rarefy to even depth to remove sequencing depth artifacts
# ALTERNATIVE: Use relative abundance transformation (divide by sample sum)
#              or DESeq2 variance-stabilizing transformation for more power
# NOTE: Rarefaction discards data; consider alternatives for small datasets

min_depth <- min(sample_sums(ps))
cat(sprintf("Rarefying to minimum depth: %d reads\n", min_depth))

# Set seed for reproducibility of random rarefaction
set.seed(42)
ps_rare <- rarefy_even_depth(
  ps,
  sample.size = min_depth,
  rngseed     = FALSE,   # Seed already set above
  replace     = FALSE,
  trimOTUs    = TRUE,    # Remove OTUs that drop to zero after rarefaction
  verbose     = FALSE
)

cat(sprintf(
  "After rarefaction: %d samples, %d taxa\n",
  nsamples(ps_rare), ntaxa(ps_rare)
))

# ============================================================
# SECTION 5: BRAY-CURTIS DISTANCE AND PCoA ORDINATION
# ============================================================

cat("\n=== Ordination ===\n")

# --- Calculate Bray-Curtis dissimilarity ---
# ASSUMPTION: Using Bray-Curtis as it is standard for microbiome abundance data
# ALTERNATIVE: UniFrac distances (weighted/unweighted) if phylogenetic tree
#              is available in the phyloseq object
cat("Calculating Bray-Curtis dissimilarity matrix...\n")
bc_dist <- phyloseq::distance(ps_rare, method = "bray")

# --- Perform PCoA (Principal Coordinates Analysis) ---
# ALTERNATIVE: NMDS (ordinate(ps_rare, "NMDS", "bray")) is rank-based and
#              more robust to non-linearity but harder to interpret axes
cat("Running PCoA ordination...\n")
pcoa_ord <- ordinate(ps_rare, method = "PCoA", distance = bc_dist)

# --- Extract variance explained by each axis ---
eigenvalues    <- pcoa_ord$values$Eigenvalues
# Guard against negative eigenvalues (can occur with some distance matrices)
eigenvalues_pos <- pmax(eigenvalues, 0)
variance_explained <- eigenvalues_pos / sum(eigenvalues_pos) * 100

axis1_var <- round(variance_explained[1], 1)
axis2_var <- round(variance_explained[2], 1)

cat(sprintf("PCoA Axis 1: %.1f%% variance explained\n", axis1_var))
cat(sprintf("PCoA Axis 2: %.1f%% variance explained\n", axis2_var))

# ============================================================
# SECTION 6: PREPARE DATA FOR PLOTTING
# ============================================================

cat("\n=== Preparing Plot Data ===\n")

# Extract PCoA scores and merge with metadata
pcoa_scores <- as.data.frame(pcoa_ord$vectors[, 1:2])
colnames(pcoa_scores) <- c("Axis1", "Axis2")
pcoa_scores$sample_id <- rownames(pcoa_scores)

# Retrieve updated metadata
plot_metadata <- as(sample_data(ps_rare), "data.frame") %>%
  select(sample_id, subject_id, timepoint, treatment, age, sex)

# Join ordination scores with metadata
# ASSUMPTION: sample_id in metadata matches rownames of OTU table
plot_data <- pcoa_scores %>%
  left_join(plot_metadata, by = "sample_id")

# Check for any samples that failed to join
n_missing_meta <- sum(is.na(plot_data$treatment))
if (n_missing_meta > 0) {
  warning(sprintf(
    "%d samples have missing metadata after join. Check sample_id consistency.",
    n_missing_meta
  ))
}

# ============================================================
# SECTION 7: CALCULATE GROUP CENTROIDS (for visual clarity)
# ============================================================

# Compute centroids per treatment × timepoint group
# These will be used to draw connecting lines showing temporal trajectories
group_centroids <- plot_data %>%
  group_by(treatment, timepoint) %>%
  summarise(
    centroid_x = mean(Axis1),
    centroid_y = mean(Axis2),
    .groups    = "drop"
  ) %>%
  # Order timepoints for correct line drawing
  arrange(treatment, timepoint)

# ============================================================
# SECTION 8: CREATE ORDINATION PLOT
# ============================================================

cat("\n=== Creating Ordination Plot ===\n")

# --- Build axis labels with variance explained ---
x_label <- sprintf("PCoA Axis 1 [%.1f%%]", axis1_var)
y_label <- sprintf("PCoA Axis 2 [%.1f%%]", axis2_var)

# --- Main PCoA plot ---
pcoa_plot <- ggplot(plot_data,
                    aes(x = Axis1, y = Axis2,
                        fill  = treatment,
                        shape = timepoint)) +

  # --- Individual sample points ---
  geom_point(
    size   = 3,
    alpha  = 0.75,
    stroke = 0.4,
    color  = "grey20"   # Outline color for filled shapes
  ) +

  # --- Centroid markers (larger, fully opaque) ---
  geom_point(
    data   = group_centroids,
    aes(x = centroid_x, y = centroid_y,
        fill  = treatment,
        shape = timepoint),
    size   = 6,
    stroke = 1.2,
    color  = "black"
  ) +

  # --- Lines connecting centroids across timepoints (temporal trajectory) ---
  geom_path(
    data     = group_centroids,
    aes(x     = centroid_x,
        y     = centroid_y,
        color = treatment,
        group = treatment),
    linewidth = 0.8,
    linetype  = "dashed",
    arrow     = arrow(length = unit(0.2, "cm"),
                      type   = "closed",
                      ends   = "last")
  ) +

  # --- Scales ---
  scale_fill_manual(
    values = TREATMENT_COLORS,
    name   = "Treatment"
  ) +
  scale_color_manual(
    values = TREATMENT_COLORS,
    guide  = "none"   # Suppress duplicate color legend
  ) +
  scale_shape_manual(
    values = TIMEPOINT_SHAPES,
    name   = "Timepoint"
  ) +

  # --- Labels ---
  labs(
    title    = "Gut Microbiome Community Composition",
    subtitle = "Bray-Curtis PCoA — Probiotic Intervention Study",
    x        = x_label,
    y        = y_label,
    caption  = sprintf(
      "n = %d samples; %d subjects; rarefied to %d reads/sample",
      nrow(plot_data), n_distinct(plot_data$subject_id), min_depth
    )
  ) +

  # --- Theme ---
  theme_bw(base_size = 12) +
  theme(
    plot.title      = element_text(face = "bold", size = 14),
    plot.subtitle   = element_text(color = "grey40", size = 11),
    plot.caption    = element_text(color = "grey50", size = 9),
    legend.position = "right",
    legend.box      = "vertical",
    legend.title    = element_text(face = "bold"),
    panel.grid.minor = element_blank(),
    aspect.ratio    = 1   # Square plot for ordination
  ) +

  # --- Force filled shapes (21-25 use fill, not color) ---
  guides(
    fill  = guide_legend(override.aes = list(shape = 21, size = 4)),
    shape = guide_legend(override.aes = list(fill  = "grey50", size = 4))
  )

# ============================================================
# SECTION 9: SAVE PLOT
# ============================================================

# Create output directory if it doesn't exist
output_dir <- dirname(OUTPUT_PLOT_PATH)
if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
  cat(sprintf("Created output directory: %s\n", output_dir))
}

ggsave(
  filename = OUTPUT_PLOT_PATH,
  plot     = pcoa_plot,
  device   = "pdf",
  width    = 8,
  height   = 7,
  units    = "in",
  dpi      = 300   # Relevant if rasterized elements are present
)
cat(sprintf("Plot saved to: %s\n", OUTPUT_PLOT_PATH))

# Also display in RStudio viewer
print(pcoa_plot)

# ============================================================
# SECTION 10: PERMANOVA ANALYSIS
# ============================================================

cat("\n=== PERMANOVA Analysis ===\n")

# --- Prepare inputs for vegan::adonis2 ---
# Extract OTU matrix (samples as rows) from rarefied phyloseq object
# ASSUMPTION: adonis2 requires samples as rows
otu_matrix <- as(otu_table(ps_rare), "matrix")
if (taxa_are_rows(ps_rare)) {
  otu_matrix <- t(otu_matrix)   # Transpose so samples are rows
}

# Retrieve metadata aligned to OTU
```

## Assessment

_Machine-suggested (UNCONFIRMED) — drafted by Claude Opus 4.7 on 2026-06-24 to speed T4 review. An author must independently read the Model Output above and set the real Recommendation. Anything labeled here is triage, not domain expert review._

**Machine triage:** Long, heavily-commented R script (410 lines) with numbered sections. Loads phyloseq with BiocManager guidance, performs QC, calculates Bray-Curtis on rarefied data, makes PCoA plot, and reaches PERMANOVA prep. Clearly **truncated** at 'Retrieve metadata aligned to OTU' with no closing — missing the adonis2 call, strata argument, and outputs. Code style is publication-grade.

**Suggested verdict (UNCONFIRMED):** Needs revision

**What still needs human verification:**
- Truncation: regenerate with higher token cap. The script lacks the actual adonis2 PERMANOVA call, which is the statistical heart of the analysis.
- Rarefaction-before-Bray-Curtis is one common choice; some prefer no rarefaction with proportions or CSS normalization. Confirm this matches the user's pipeline.
- Whether the missing PERMANOVA section would use `strata = subject_id` (as the prompt requires for repeated measures) — the truncation prevents verification.

## Overall Assessment
- **Recommendation:** PENDING AUTHOR REVIEW
- **Notes:**

## Verification Steps Tested
_Which verification requirements from the prompt were checked, and results._
