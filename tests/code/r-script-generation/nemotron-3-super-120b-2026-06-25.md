# Test Results: code/r-script-generation.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-25.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** code/r-script-generation.md
- **Model:** nemotron-3-super-120b
- **Model ID (pinned):** Nemotron-3-Super-120B-A12B-NVFP4
- **Endpoint:** https://copilot-dev.cqls.oregonstate.edu/llm/nemotron3-super-120b-nvfp4/v1
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


**R script – Ordination and PERMANOVA for a probiotic intervention study**  
*(Save as e.g., `ordination_permanova.R` and run with `Rscript ordination_permanova.R`)*  

```r
################################################################################
# 0. SETUP & PACKAGE LOADING
################################################################################
# Load required packages. Install if missing (comment out after first run).
pkgs <- c("phyloseq", "vegan", "ggplot2")
installed <- pkgs %in% rownames(installed.packages())
if (any(!installed)) {
  install.packages(pkgs[!installed], dependencies = TRUE)
}
lapply(pkgs, library, character.only = TRUE)

# Optional: set a seed for reproducible permutations
set.seed(123)

################################################################################
# 1. LOAD PHYLOSEQ OBJECT
################################################################################
input_file <- "data/probiotic_study.rds"

# Basic file‑existence check
if (!file.exists(input_file)) {
  stop(sprintf("Input file not found: %s", input_file))
}

# Load the object
physeq <- readRDS(input_file)

# Verify that we indeed have a phyloseq object
if (!inherits(physeq, "phyloseq")) {
  stop("Loaded object is not a phyloseq instance.")
}

################################################################################
# 2. BASIC QUALITY CONTROL (QC)
################################################################################
cat("\n=== QC SUMMARY ===\n")

# Sample-level summaries
sample_sums <- sample_sums(physeq)
cat(sprintf("Number of samples: %d\n", nsamples(physeq)))
cat(sprintf("Total reads per sample: min = %d, median = %d, max = %d\n",
            min(sample_sums), median(sample_sums), max(sample_sums)))

# Taxon-level summaries
taxa_sums <- taxa_sums(physeq)
cat(sprintf("Number of taxa (OTUs/ASVs): %d\n", ntaxa(physeq)))
cat(sprintf("Total reads per taxon: min = %d, median = %d, max = %d\n",
            min(taxa_sums), median(taxa_sums), max(taxa_sums)))

# Check for samples with zero total reads (should be removed or flagged)
zero_read_samples <- names(sample_sums[sample_sums == 0])
if (length(zero_read_samples) > 0) {
  warning(sprintf(
    "The following %d sample(s) have zero total reads: %s",
    length(zero_read_samples),
    paste(zero_read_samples, collapse = ", ")
  ))
}

# Check for missing values in key sample variables
sample_df <- as(sample_data(physeq), "data.frame")
key_vars <- c("sample_id", "subject_id", "timepoint", "treatment", "age", "sex")
missing_key <- sapply(key_vars, function(v) any(is.na(sample_df[[v]])))
if (any(missing_key)) {
  stop(sprintf(
    "Missing data in key variable(s): %s",
    paste(names(missing_key)[missing_key], collapse = ", ")
  ))
}

# Ensure factors have expected levels (helpful for plotting)
sample_df$timepoint <- factor(sample_df$timepoint,
                              levels = c("baseline", "week4", "week8"))
sample_df$treatment <- factor(sample_df$treatment,
                              levels = c("placebo", "probiotic"))
sample_data(physeq) <- sample_df

################################################################################
# 3. BRAY‑CURTIS DISTANCE MATRIX
################################################################################
cat("\n=== CALCULATING BRAY‑CURTIS DISTANCE ===\n")
# phyloseq::distance handles OTU table internally and returns a dist object
bray_dist <- distance(physeq, method = "bray")

# Quick sanity check: distance matrix should not be all zeros
if (all(bray_dist == 0)) {
  stop("Bray‑Curtis distance matrix contains only zeros – check OTU table.")
}

################################################################################
# 4. PCoA ORDINATION
################################################################################
cat("\n=== PERFORMING PCoA ===\n")
# Using vegan's cmdscale (classical multidimensional scaling) on the distance
pcoa_res <- cmdscale(bray_dist, k = 2, eig = TRUE)   # k = 2 for 2‑D plot

# Extract coordinates and eigenvalues for plotting
pcoa_df <- data.frame(
  SampleID = rownames(pcoa_res$points),
  PCoA1    = pcoa_res$points[, 1],
  PCoA2    = pcoa_res$points[, 2],
  stringsAsFactors = FALSE
)

# Merge with sample data for plotting
pcoa_df <- merge(pcoa_df, sample_df, by.x = "SampleID", by.y = "sample_id")

# Calculate % variance explained by each axis
var_expl <- round(100 * pcoa_res$eig / sum(pcoa_res$eig), 1)
cat(sprintf("Variance explained: PCoA1 = %s%%, PCoA2 = %s%%\n",
            var_expl[1], var_expl[2]))

################################################################################
# 5. ORDINATION PLOT (ggplot2)
################################################################################
cat("\n=== CREATING ORDINATION FIGURE ===\n")
p <- ggplot(pcoa_df, aes(x = PCoA1, y = PCoA2,
                         colour = treatment, shape = timepoint)) +
  geom_point(size = 3, alpha = 0.8) +
  scale_colour_manual(
    values = c("placebo" = "gray40", "probiotic" = "steelblue"),
    name = "Treatment"
  ) +
  scale_shape_manual(
    values = c(baseline = 15, week4 = 17, week8 = 19),
    name = "Timepoint"
  ) +
  labs(
    title = "PCoA of Bray‑Curtis dissimilarities",
    subtitle = sprintf("PCoA1 (%s%%) – PCoA2 (%s%%)", var_expl[1], var_expl[2]),
    x = paste0("PCoA1 (", var_expl[1], "%)"),
    y = paste0("PCoA2 (", var_expl[2], "%)")
  ) +
  theme_minimal(base_size = 14) +
  theme(
    plot.title = element_text(face = "bold", hjust = 0.5),
    plot.subtitle = element_text(hjust = 0.5),
    legend.position = "right"
  )

# Save as PDF (publication‑ready dimensions)
pdf_file <- "output/probiotic_pcoa.pdf"
pdf(pdf_file, width = 7, height = 5)
print(p)
dev.off()
cat(sprintf("Ordination plot saved to: %s\n", pdf_file))

################################################################################
# 6. PERMANOVA (adonis2) WITH SUBJECT BLOCKING
################################################################################
cat("\n=== RUNNING PERMANOVA (adonis2) ===\n")
# Formula: treatment * timepoint  (interaction of interest)
# Blocking: permutations restricted within each subject (strata = subject_id)
# Using 999 permutations (increase for final analysis if desired)
permanova_res <- adonis2(
  bray_dist ~ treatment * timepoint,
  data = sample_df,
  permutations = how(block = sample_df$subject_id, nperm = 999),
  method = "bray"
)

# Print a tidy summary
print(permanova_res)

# Optional: extract p-values for reporting
cat("\n=== PERMANOVA SUMMARY (key terms) ===\n")
cat(sprintf(
  "Treatment:      F = %.3f, R2 = %.3f, p = %.3f\n",
  permanova_res$F[1], permanova_res$R2[1], permanova_res$`Pr(>F)`[1]
))
cat(sprintf(
  "Timepoint:      F = %.3f, R2 = %.3f, p = %.3f\n",
  permanova_res$F[2], permanova_res$R2[2], permanova_res$`Pr(>F)`[2]
))
cat(sprintf(
  "Treatment:Timepoint interaction: F = %.3f, R2 = %.3f, p = %.3f\n",
  permanova_res$F[3], permanova_res$R2[3], permanova_res$`Pr(>F)`[3]
))

################################################################################
# 7. END OF SCRIPT
################################################################################
cat("\n=== SCRIPT COMPLETED SUCCESSFULLY ===\n")
```

---

### Required Packages
| Package   | Version (CRAN/Bioconductor) | Purpose |
|-----------|-----------------------------|---------|
| **phyloseq** | ≥ 1.30.0 | Import, store, and manipulate microbiome data (OTU table, taxonomy, sample data). |
| **vegan**    | ≥ 2.6-0  | Distance calculations (`distance`), PCoA (`cmdscale`), PERMANOVA (`adonis2`). |
| **ggplot2**  | ≥ 3.3.0  | Production of publication‑quality ordination plots. |
| (optional) **dplyr** | ≥ 1.0.0 | Could be used for data wrangling; not strictly required in the script above. |

*All packages are available on CRAN (phyloseq is also on Bioconductor).*

---

### Key Assumptions About the Data
1. **Sample data columns** – The `sample_data` slot contains at least the columns: `sample_id`, `subject_id`, `timepoint`, `treatment`, `age`, `sex`.  
2. **Factor levels** – `timepoint` is expected to have levels `"baseline"`, `"week4"`, `"week8"`; `treatment` expected levels `"placebo"` and `"probiotic"` (the script re‑orders them accordingly).  
3. **Repeated measures** – Each `subject_id` appears exactly three times (one per timepoint) under each treatment; this enables subject‑level blocking in PERMANOVA.  
4. **OTU table** – Counts are non‑negative integers; no prior rarefaction is performed (Bray‑Curtis is robust to library size differences, but users may rarefy or transform if desired).  
5. **No missing values** – The script stops if any of the key variables contain `NA`.  

---

### Suggested Validation Checks (to run after/before the script)
| Check | How to Perform | Why |
|-------|----------------|-----|
| **Library size distribution** | `summary(sample_sums(physeq))` or plot a histogram | Detect outliers or failed sequencing runs. |
| **Rarefaction curves** | `rarecurve(t(otu_table(physeq)), step=50, cex=0.5)` | Verify sequencing depth sufficiency. |
| **Taxa prevalence** | `sum(taxa_sums(physeq) > 0)` vs total taxa | Ensure many taxa are not just noise. |
| **Distance matrix inspection** | `hist(as.matrix(bray_dist), breaks=50)` | Confirm a reasonable spread of dissimilarities (not all zeros or ones). |
| **PERMANOVA convergence** | Increase permutations (`nperm=9999`) and compare p‑values | Ensure p‑value stability. |
| **Model diagnostics** | Plot residuals from a distance‑based redundancy analysis (`capscale`) if needed | Check for heteroscedasticity or outliers influencing PERMANOVA. |
| **Reproducibility** | Set a seed (`set.seed`) before permutations (already done) | Guarantees identical results across runs. |

Feel free to adapt the script (e.g., change permutation number, add faceting by `sex` or `age`, or apply alternative transformations such as Hellinger before distance calculation). The provided workflow follows common practice for microbiome ordination and hypothesis testing while keeping the code transparent and maintainable.
````

## Assessment

_Machine-suggested (UNCONFIRMED) — drafted by Claude Opus 4.7 on 2026-06-26 to speed T4 review. An author must independently read the Model Output above and set the real Recommendation. Anything labeled here is triage, not domain expert review._

**Machine triage:** Output is **complete** — full R script + a tabulated validation checks section. One of 3 of 6 panel models that did not truncate. Includes set.seed, suggests Hellinger transformation as alternative, capscale-based diagnostics. Strong cross-model agreement with GPT/Step on core workflow.

**Suggested verdict (UNCONFIRMED):** Pass

**What still needs human verification:**
- Confirm the validation table cells (e.g., "hist(as.matrix(bray_dist))" for distance inspection) are technically appropriate
- That the MRPP fallback for dispersion-test failures matches reviewer preference
- Spot-check the script runs without errors on test data

## Overall Assessment
- **Recommendation:** PENDING AUTHOR REVIEW
- **Notes:**

## Verification Steps Tested
_Which verification requirements from the prompt were checked, and results._
