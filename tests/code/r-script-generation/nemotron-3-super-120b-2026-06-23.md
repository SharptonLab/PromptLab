# Test Results: code/r-script-generation.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-23.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** code/r-script-generation.md
- **Model:** nemotron-3-super-120b
- **Model ID (pinned):** Nemotron-3-Super-120B-A12B-NVFP4
- **Endpoint:** https://copilot-dev.cqls.oregonstate.edu/llm/nemotron3-super-120b-nvfp4/v1
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


**R Script**

```r
## ==========================================================================
##  Microbiome Ordination & PERMANOVA for Probiotic Intervention Study
##  Author:  [Your Name]
##  Date:    [Today's Date]
##  Description:
##    1. Load a phyloseq object (RDS) containing OTU table, taxonomy, sample data.
##    2. Perform basic QC (sample/taxa counts, filtering low‑abundance samples).
##    3. Compute Bray‑Curtis dissimilarity matrix.
##    4. Run PCoA (principal coordinates analysis) on the distance matrix.
##    5. Plot PCoA1 vs PCoA2 coloured by treatment, shaped by timepoint.
##    6. Test treatment × timepoint interaction with PERMANOVA (adonis2),
##       using subject_id as a blocking/strata factor to account for repeated measures.
##    7. Save the ordination plot as PDF and print PERMANOVA summary to console.
## ==========================================================================

## -------------------------- 0. Setup ---------------------------------------
# Clear workspace (optional)
rm(list = ls())

# Load required packages ----------------------------------------------------
# Install if not present (comment out after first run)
if (!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager")
pkgs <- c("phyloseq", "vegan", "ggplot2", "dplyr")
for (p in pkgs) {
  if (!requireNamespace(p, quietly = TRUE)) {
    if (p %in% BiocManager::available())
      BiocManager::install(p)
    else
      install.packages(p)
  }
  library(p, character.only = TRUE)
}

# Set seed for reproducibility (PERMANOVA uses permutations)
set.seed(123)

## -------------------------- 1. Load Data -----------------------------------
input_file <- "data/probiotic_study.rds"

# Basic file existence check
if (!file.exists(input_file)) {
  stop(sprintf("Input file not found: %s", input_file))
}

# Load phyloseq object
ps <- readRDS(input_file)

# Quick sanity check: is it a phyloseq object?
if (!inherits(ps, "phyloseq")) {
  stop("Loaded object is not of class 'phyloseq'.")
}

## -------------------------- 2. Basic QC ------------------------------------
cat("\n=== Basic QC ===\n")
# Sample sums (total reads per sample)
sample_sums_vec <- sample_sums(ps)
cat(sprintf("Number of samples: %d\n", nsamples(ps)))
cat(sprintf("Reads per sample: min = %d, median = %d, max = %d\n",
            min(sample_sums_vec), median(sample_sums_vec), max(sample_sums_vec)))

# Taxa sums (total counts per taxon)
taxa_sums_vec <- taxa_sums(ps)
cat(sprintf("Number of taxa: %d\n", ntaxa(ps)))
cat(sprintf("Taxon counts: min = %d, median = %d, max = %d\n",
            min(taxa_sums_vec), median(taxa_sums_vec), max(taxa_sums_vec)))

# Optional: filter out samples with extremely low library size
# (e.g., < 1000 reads). Adjust threshold as needed.
low_read_thresh <- 1000
keep_samples <- sample_sums_vec >= low_read_thresh
if (any(!keep_samples)) {
  cat(sprintf("Removing %d sample(s) with < %d reads.\n",
              sum(!keep_samples), low_read_thresh))
  ps <- prune_samples(keep_samples, ps)
}

# Optional: remove taxa that are never observed (zero across all samples)
ps <- prune_taxa(taxa_sums(ps) > 0, ps)

cat(sprintf("After QC: %d samples, %d taxa remain.\n\n",
            nsamples(ps), ntaxa(ps)))

## -------------------------- 3. Distance Matrix -----------------------------
cat("=== Computing Bray-Curtis distance ===\n")
# Use vegan's vegdist on the OTU table (counts)
otu_mat <- otu_table(ps)
if (!is.numeric(otu_mat)) {
  stop("OTU table must be numeric.")
}
bray_dist <- vegdist(otu_mat, method = "bray")
cat(sprintf("Distance matrix dimensions: %d x %d\n",
            attr(bray_dist, "Size"), attr(bray_dist, "Size")))

## -------------------------- 4. PCoA Ordination ----------------------------
cat("=== Performing PCoA ===\n"
pcoa_res <- cmdscale(bray_dist, k = 2, eig = TRUE)   # k = 2 for 2D plot
# Extract coordinates and eigenvalues
pcoa_points <- as.data.frame(pcoa_res$points)
colnames(pcoa_points) <- c("PCoA1", "PCoA2")
# Calculate % variance explained
eig <- pcoa_res$eig
var_explained <- 100 * eig / sum(eig)
pcoa_var <- round(var_explained[1:2], 1)

# Attach sample metadata for plotting
sample_df <- as.data.frame(sample_data(ps))
# Ensure sample IDs match row names of pcoa_points
if (!all(row.names(sample_df) == row.names(pcoa_points))) {
  # Reorder to match
  sample_df <- sample_df[row.names(pcoa_points), , drop = FALSE]
}
pcoa_df <- cbind(pcoa_points, sample_df)

## -------------------------- 5. Plot PCoA -----------------------------------
cat("=== Creating ordination plot ===\n"
p <- ggplot(pcoa_df, aes(x = PCoA1, y = PCoA2,
                         colour = treatment, shape = timepoint)) +
  geom_point(size = 3, alpha = 0.8) +
  labs(
    title = "PCoA of Bray-Curtis Dissimilarities",
    subtitle = sprintf("PCoA1: %s%% variance, PCoA2: %s%% variance",
                       pcoa_var[1], pcoa_var[2]),
    x = paste0("PCoA1 (", pcoa_var[1], "%)"),
    y = paste0("PCoA2 (", pcoa_var[2], "%)"),
    colour = "Treatment",
    shape = "Timepoint"
  ) +
  theme_minimal(base_size = 14) +
  theme(
    plot.title = element_text(face = "bold"),
    legend.position = "right"
  )

# Save plot
pdf_file <- "output/probiotic_pcoa.pdf"
dir.create(dirname(pdf_file), showWarnings = FALSE, recursive = TRUE)
ggsave(filename = pdf_file, plot = p, width = 7, height = 5, units = "in")
cat(sprintf("Ordination plot saved to: %s\n", pdf_file))

## -------------------------- 6. PERMANOVA ----------------------------------
cat("=== Running PERMANOVA (adonis2) ===\n"
# Build formula: distance ~ treatment * timepoint + Subject(ID) as strata
# Using strata argument to restrict permutations within subjects (blocking)
adonis_formula <- as.formula(bray_dist ~ treatment * timepoint)

# Check for missing values in covariates
covars <- sample_df[, c("treatment", "timepoint", "subject_id")]
if (any(is.na(covars))) {
  stop("Missing values detected in treatment, timepoint, or subject_id.")
}

# Run adonis2 with 999 permutations, stratified by subject_id
set.seed(123)  # ensure reproducibility
adonis_res <- adonis2(
  adonis_formula,
  data = sample_df,
  permutations = how(blocks = sample_df$subject_id, nperm = 999),
  method = "bray"
)

# Print results
print(adonis_res)

## -------------------------- 7. Session Info -------------------------------
cat("\n=== Session Info ===\n")
sessionInfo()

```

---

### Required Packages
| Package   | Source        | Reason for Use |
|-----------|---------------|----------------|
| **phyloseq** | Bioconductor | Core class for microbiome data (OTU table, taxonomy, sample data). |
| **vegan**    | CRAN          | Provides `vegdist` for Bray‑Curtis, `cmdscale`/`capscale` for PCoA, and `adonis2` for PERMANOVA with custom permutation schemes. |
| **ggplot2**  | CRAN          | Publication‑quality graphics; easy to colour by treatment and shape by timepoint. |
| **dplyr**    | CRAN          | Convenient data manipulation (filtering, summarising) – optional but improves readability. |
| **BiocManager** | CRAN      | Helper to install Bioconductor packages if needed. |

*(All packages are available on CRAN or Bioconductor.)*

---

### Assumptions About the Data
1. The RDS file contains a valid `phyloseq` object with:
   - OTU table (samples × taxa) of integer counts.
   - Sample data (`sample_data`) that includes columns: `sample_id`, `subject_id`, `timepoint` (factor with levels *baseline*, *week4*, *week8*), `treatment` (factor: *probiotic*, *placebo*), `age`, `sex`.
2. Sample IDs in the OTU table match the row names of the sample data.
3. No missing values in the key variables used for modelling (`treatment`, `timepoint`, `subject_id`). The script stops with an error if any are found.
4. Library sizes are sufficient; samples with < 1000 reads are removed (threshold can be adjusted).
5. The study design is balanced enough for PERMANOVA; however, the script uses a stratified permutation scheme (`subject_id` as blocks) to account for repeated measures, which is appropriate even with modest imbalance.
6. Bray‑Curtis dissimilarity is appropriate for count‑based community data (common in microbiome analyses).

---

### Suggested Validation Checks
1. **QC Plots** – After loading, examine library size distribution (e.g., histogram of `sample_sums`) to confirm the low‑read filter is sensible.
2. **Distance Matrix Inspection** – Check a few distances (`as.matrix(bray_dist)[1:5, 1:5]`) to ensure they are within [0,1] and not all zeros.
3. **PCoA Eigenvalues** – Verify that the first two axes explain a reasonable proportion of variance (> 10 % each is typical); if not, consider higher dimensions or alternative distances.
4. **PERMANOVA Diagnostics** – 
   - Examine the permutation distribution (`adonis_res$perm`) for any extreme p‑values.
   - Check that the number of unique permutations is adequate (should be close to 999 when possible).
   - Optionally run `betadisper` (homogeneity of variances) to assess whether significant PERMANOVA results could be driven by dispersion differences.
5. **Plot Review** – Open the generated PDF to confirm that points are not overlapping excessively; consider adding `geom_jitter` or adjusting point size/alpha if needed.
6. **Reproducibility** – Run the script in a fresh R session (or using `renv`/`packrat`) to ensure all package versions are captured and the script runs without errors. 

Feel free to adjust thresholds, colour palettes, or the number of permutations according to your project's standards. Happy analyzing!
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
