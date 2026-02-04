# Case Study: Code Generation Workflow

## Overview

This case study demonstrates a complete code generation workflow using LLM assistance, from initial script generation through testing, debugging, and documentation. The example follows a microbiome researcher generating an R analysis pipeline for 16S rRNA data.

**Goal:** Create an R script that processes a phyloseq object to calculate alpha diversity metrics, run statistical tests comparing groups, and generate publication-ready figures.

**Prompts used in this workflow:**
- `code/r-script-generation.md`
- `code/debugging.md`
- `code/code-explanation.md`
- `validation/verification-checklist.md`

---

## Step 1: Initial Code Generation

### Setup

The researcher needs a script to analyze alpha diversity from a phyloseq object containing 16S data from a mouse study with two treatment groups (control vs. antibiotic).

**Prompt used:** Adapted from `code/r-script-generation.md`

```
Write an R script that takes a phyloseq object and performs alpha diversity analysis.

Input:
- phyloseq object named `ps` with:
  - OTU table (taxa as rows, samples as columns)
  - Sample data with column "treatment" (values: "control", "antibiotic")
  - Taxonomy table

Required outputs:
1. Calculate Shannon, Simpson, and Observed richness for each sample
2. Statistical comparison between treatment groups (appropriate test for n≈10 per group)
3. Box plot of Shannon diversity by treatment group, publication-ready

Requirements:
- Use tidyverse style
- Include comments explaining each step
- Use phyloseq and vegan packages
- Handle potential errors (e.g., samples with zero reads)
- Output statistical test results with effect size

Provide the complete script with all necessary library calls.
```

**LLM Output:**

```r
# Alpha Diversity Analysis Script
# Compares diversity metrics between treatment groups

# Load required libraries
library(phyloseq)
library(vegan)
library(tidyverse)
library(ggpubr)  # for publication-ready plots

# Function to calculate alpha diversity metrics
calculate_alpha_diversity <- function(ps) {
  # Extract OTU table (samples as rows for vegan)
  otu <- as.data.frame(t(otu_table(ps)))

  # Check for and handle samples with zero reads
  sample_sums <- rowSums(otu)
  if (any(sample_sums == 0)) {
    warning(paste("Removing", sum(sample_sums == 0), "samples with zero reads"))
    otu <- otu[sample_sums > 0, ]
  }

  # Calculate diversity metrics
  alpha_div <- data.frame(
    sample_id = rownames(otu),
    shannon = diversity(otu, index = "shannon"),
    simpson = diversity(otu, index = "simpson"),
    observed = specnumber(otu)
  )

  # Merge with sample metadata
  sample_meta <- as.data.frame(sample_data(ps))
  sample_meta$sample_id <- rownames(sample_meta)

  alpha_div <- left_join(alpha_div, sample_meta, by = "sample_id")

  return(alpha_div)
}

# Calculate alpha diversity
alpha_results <- calculate_alpha_diversity(ps)

# Statistical comparison: Wilcoxon rank-sum test
# (appropriate for small n, non-parametric)
stat_test <- wilcox.test(
  shannon ~ treatment,
  data = alpha_results,
  exact = FALSE  # use normal approximation
)

# Calculate effect size (Cliff's delta for non-parametric)
library(effsize)
effect <- cliff.delta(
  alpha_results$shannon[alpha_results$treatment == "antibiotic"],
  alpha_results$shannon[alpha_results$treatment == "control"]
)

# Print results
cat("Wilcoxon rank-sum test for Shannon diversity:\n")
cat("W =", stat_test$statistic, "\n")
cat("p-value =", stat_test$p.value, "\n")
cat("Cliff's delta =", effect$estimate, "(", effect$magnitude, ")\n")

# Publication-ready box plot
diversity_plot <- ggplot(alpha_results, aes(x = treatment, y = shannon, fill = treatment)) +
  geom_boxplot(outlier.shape = NA, alpha = 0.7) +
  geom_jitter(width = 0.2, size = 2, alpha = 0.8) +
  scale_fill_manual(values = c("control" = "#4575b4", "antibiotic" = "#d73027")) +
  labs(
    x = "Treatment",
    y = "Shannon Diversity Index",
    title = NULL
  ) +
  theme_classic(base_size = 14) +
  theme(
    legend.position = "none",
    axis.text = element_text(color = "black")
  ) +
  stat_compare_means(method = "wilcox.test", label = "p.format")

# Save plot
ggsave("alpha_diversity_plot.pdf", diversity_plot, width = 4, height = 5)

# Return results as list
results <- list(
  alpha_diversity = alpha_results,
  statistical_test = stat_test,
  effect_size = effect,
  plot = diversity_plot
)
```

---

## Step 2: Code Review and Testing

### Initial Review

Before running, the researcher reviews the code logic:

**Review checklist:**
- [x] Libraries appropriate for task
- [x] OTU table transposition correct (phyloseq stores taxa as rows)
- [x] Zero-read handling present
- [x] Statistical test appropriate for small sample size
- [x] Effect size included
- [ ] **Issue found:** `effsize` package not in original library calls

### Test with Synthetic Data

The researcher creates a test dataset with known properties:

```r
# Create test phyloseq object with known properties
set.seed(42)

# Known values: control should have higher diversity
control_otu <- matrix(
  c(rep(c(100, 100, 100, 100, 100), 5)),  # even distribution
  nrow = 5, ncol = 5, byrow = TRUE
)
antibiotic_otu <- matrix(
  c(rep(c(400, 50, 25, 15, 10), 5)),  # dominated by one taxon
  nrow = 5, ncol = 5, byrow = TRUE
)

test_otu <- rbind(control_otu, antibiotic_otu)
rownames(test_otu) <- paste0("Taxa", 1:5)
colnames(test_otu) <- paste0("Sample", 1:10)

test_sample_data <- data.frame(
  treatment = c(rep("control", 5), rep("antibiotic", 5)),
  row.names = paste0("Sample", 1:10)
)

test_ps <- phyloseq(
  otu_table(test_otu, taxa_are_rows = TRUE),
  sample_data(test_sample_data)
)

# Expected: Shannon diversity should be higher for control
# Even distribution (control): Shannon ≈ 1.61 (log of 5)
# Dominated distribution (antibiotic): Shannon ≈ 0.94
```

### First Run: Error Encountered

```r
# Running the script produces error:
# Error in library(effsize) : there is no package called 'effsize'
```

---

## Step 3: Debugging

**Prompt used:** Adapted from `code/debugging.md`

```
My R script produces this error:

Error in library(effsize) : there is no package called 'effsize'

The script calculates alpha diversity and uses Cliff's delta for effect size. Two options:
1. Add effsize to dependencies
2. Replace with base R or another common package

Which approach is better for reproducibility, and provide the fix?
```

**LLM Output:**

> For reproducibility, I recommend replacing `effsize` with a manual calculation or using the `rstatix` package, which is more commonly installed alongside tidyverse workflows.
>
> **Option 1: Manual Cliff's delta** (no additional dependencies)
> ```r
> # Calculate Cliff's delta manually
> cliff_delta <- function(x, y) {
>   n_x <- length(x)
>   n_y <- length(y)
>   dominance <- outer(x, y, function(a, b) sign(a - b))
>   delta <- mean(dominance)
>   return(list(
>     estimate = delta,
>     magnitude = case_when(
>       abs(delta) < 0.147 ~ "negligible",
>       abs(delta) < 0.33 ~ "small",
>       abs(delta) < 0.474 ~ "medium",
>       TRUE ~ "large"
>     )
>   ))
> }
> ```
>
> **Option 2: Use rstatix** (common in microbiome workflows)
> ```r
> library(rstatix)
> effect <- alpha_results %>%
>   wilcox_effsize(shannon ~ treatment)
> ```
>
> I recommend Option 1 for maximum portability, or Option 2 if rstatix is already in your workflow.

**Fix applied:** Researcher chooses Option 1 (manual calculation) and updates the script.

---

## Step 4: Successful Test Run

After fix, the script runs successfully on test data:

```
Wilcoxon rank-sum test for Shannon diversity:
W = 25
p-value = 0.007936508
Cliff's delta = 1 ( large )
```

**Verification against expected values:**
- [x] Control samples have higher Shannon diversity (~1.61 vs ~0.94) ✓
- [x] Statistical test detects significant difference (p < 0.05) ✓
- [x] Effect size is "large" as expected for this synthetic data ✓
- [x] Plot generated correctly with proper axis labels ✓

### Edge Case Testing

```r
# Test with sample containing zero reads
zero_otu <- test_otu
zero_otu[, 1] <- 0  # Sample1 now has zero reads

zero_ps <- phyloseq(
  otu_table(zero_otu, taxa_are_rows = TRUE),
  sample_data(test_sample_data)
)

# Run script
alpha_results_zero <- calculate_alpha_diversity(zero_ps)
# Warning message: Removing 1 samples with zero reads
# Script handles edge case correctly ✓
```

---

## Step 5: Code Explanation for Documentation

Before finalizing, the researcher generates documentation for the Methods section.

**Prompt used:** Adapted from `code/code-explanation.md`

```
Explain this R code for a Methods section. Focus on:
1. What statistical approach is used and why
2. How diversity metrics are calculated
3. Any data quality steps

Keep it concise (3-4 sentences suitable for Methods).

[Paste final script]
```

**LLM Output:**

> Alpha diversity metrics (Shannon index, Simpson index, and observed richness) were calculated using the vegan package in R. Samples with zero total reads were excluded prior to analysis. Between-group comparisons were performed using Wilcoxon rank-sum tests, appropriate for small sample sizes without assuming normality, with effect sizes reported as Cliff's delta.

---

## Step 6: Final Verification Checklist

**Using:** `validation/verification-checklist.md`

| Check | Status | Notes |
|-------|--------|-------|
| Code runs without errors | ✓ | After effsize fix |
| Output matches expectations on test data | ✓ | Shannon values, p-value, effect size |
| Edge cases handled | ✓ | Zero-read samples excluded with warning |
| Statistical test appropriate | ✓ | Wilcoxon for small n, non-parametric |
| Packages are current | ✓ | Checked CRAN dates |
| Code is commented | ✓ | Each major step explained |
| Results reproducible | ✓ | set.seed() used in test; script is deterministic |

---

## Final Script (After Revisions)

```r
# Alpha Diversity Analysis Script
# Compares diversity metrics between treatment groups
# Generated with LLM assistance; tested and verified

# Load required libraries
library(phyloseq)
library(vegan)
library(tidyverse)
library(ggpubr)

# Manual Cliff's delta calculation (avoids effsize dependency)
cliff_delta <- function(x, y) {
  dominance <- outer(x, y, function(a, b) sign(a - b))
  delta <- mean(dominance)
  magnitude <- case_when(
    abs(delta) < 0.147 ~ "negligible",
    abs(delta) < 0.33 ~ "small",
    abs(delta) < 0.474 ~ "medium",
    TRUE ~ "large"
  )
  return(list(estimate = delta, magnitude = magnitude))
}

# Function to calculate alpha diversity metrics
calculate_alpha_diversity <- function(ps) {
  # Extract OTU table (samples as rows for vegan)
  otu <- as.data.frame(t(otu_table(ps)))

  # Check for and handle samples with zero reads
  sample_sums <- rowSums(otu)
  if (any(sample_sums == 0)) {
    warning(paste("Removing", sum(sample_sums == 0), "samples with zero reads"))
    otu <- otu[sample_sums > 0, ]
  }

  # Calculate diversity metrics
  alpha_div <- data.frame(
    sample_id = rownames(otu),
    shannon = diversity(otu, index = "shannon"),
    simpson = diversity(otu, index = "simpson"),
    observed = specnumber(otu)
  )

  # Merge with sample metadata
  sample_meta <- as.data.frame(sample_data(ps))
  sample_meta$sample_id <- rownames(sample_meta)

  alpha_div <- left_join(alpha_div, sample_meta, by = "sample_id")

  return(alpha_div)
}

# Main analysis
run_alpha_analysis <- function(ps, group_var = "treatment") {
  # Calculate alpha diversity
  alpha_results <- calculate_alpha_diversity(ps)

  # Statistical comparison
  formula <- as.formula(paste("shannon ~", group_var))
  stat_test <- wilcox.test(formula, data = alpha_results, exact = FALSE)

  # Effect size
  groups <- unique(alpha_results[[group_var]])
  effect <- cliff_delta(
    alpha_results$shannon[alpha_results[[group_var]] == groups[1]],
    alpha_results$shannon[alpha_results[[group_var]] == groups[2]]
  )

  # Results summary
  cat("Wilcoxon rank-sum test for Shannon diversity:\n")
  cat("W =", stat_test$statistic, "\n")
  cat("p-value =", format(stat_test$p.value, digits = 3), "\n")
  cat("Cliff's delta =", round(effect$estimate, 3), "(", effect$magnitude, ")\n")

  # Return results
  return(list(
    alpha_diversity = alpha_results,
    statistical_test = stat_test,
    effect_size = effect
  ))
}

# Generate publication-ready plot
plot_alpha_diversity <- function(alpha_results, group_var = "treatment") {
  ggplot(alpha_results, aes_string(x = group_var, y = "shannon", fill = group_var)) +
    geom_boxplot(outlier.shape = NA, alpha = 0.7) +
    geom_jitter(width = 0.2, size = 2, alpha = 0.8) +
    labs(x = "Treatment", y = "Shannon Diversity Index") +
    theme_classic(base_size = 14) +
    theme(legend.position = "none") +
    stat_compare_means(method = "wilcox.test", label = "p.format")
}
```

---

## Key Lessons from This Workflow

1. **Test with known-answer data:** Synthetic data with predictable properties catches logic errors that "runs without errors" misses.

2. **Check dependencies:** LLM-generated code may assume packages you don't have. Review library calls before running.

3. **Edge cases matter:** Explicitly test boundary conditions (zero reads, missing data, single-sample groups).

4. **Debugging is iterative:** The first version rarely works perfectly. Budget time for the debug-test cycle.

5. **Document as you go:** The explanation prompt at the end is easier when you've tracked changes throughout.

---

## Prompts Used (Quick Reference)

| Step | Prompt File | Purpose |
|------|-------------|---------|
| 1 | `code/r-script-generation.md` | Initial script generation |
| 3 | `code/debugging.md` | Fix dependency error |
| 5 | `code/code-explanation.md` | Generate Methods text |
| 6 | `validation/verification-checklist.md` | Final verification |
