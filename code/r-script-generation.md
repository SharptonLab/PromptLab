# R Script Generation Prompt

## Task Description

Generate R scripts for data analysis tasks, with emphasis on readable, well-documented code that follows best practices for reproducibility in life science research.

## When to Use

- Creating analysis scripts for common tasks (data import, visualization, statistical tests)
- Generating boilerplate code you'll customize
- Learning how to implement specific analyses in R
- Getting started with unfamiliar packages

## When NOT to Use

- For analyses you don't understand well enough to verify the output
- When you need production-ready code without testing (always test)
- For novel statistical methods where implementation correctness is uncertain
- When the task requires understanding of your specific data structure that you can't communicate clearly

## The Prompt

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
```

## Prompt Components Explained

| Component | Purpose |
|-----------|---------|
| **Research context** | Helps tailor approach to life science conventions |
| **Data description** | Critical—script quality depends on accurate data description |
| **Specific task** | Clear specification reduces ambiguity |
| **Package preferences** | Reduces dependency sprawl; ensures compatibility with your workflow |
| **Code style requirements** | Produces readable, maintainable scripts |
| **Constraints** | Keeps solutions practical and reproducible |

## Example Input

```
Context: I am a microbiome researcher working on a diet intervention study in mice. I need an R script to analyze alpha diversity changes over time.

Data description:
- Input: CSV file with columns: sample_id, mouse_id, timepoint (days 0, 7, 14, 21), treatment (control, high_fat), shannon, observed_asvs, chao1
- Sample size: ~160 samples (10 mice × 2 treatments × 4 timepoints, some missing)
- Key variables: shannon (numeric), timepoint (integer), treatment (factor), mouse_id (factor for repeated measures)

Task: Write an R script that:
1. Loads and validates the data
2. Creates a figure showing Shannon diversity over time by treatment group (mean ± SE, line plot)
3. Runs a linear mixed model testing treatment × time interaction with mouse as random effect
4. Outputs the figure and a summary of the statistical results

Requirements:
1. Packages: Use tidyverse for data manipulation, ggplot2 for plotting, lme4 for mixed models
2. Code style: Well-commented with section headers
3. Input file path: "data/alpha_diversity.csv"
4. Output: Publication-quality figure as PDF, model summary printed to console
```

## Example Output

```r
# =============================================================================
# Alpha Diversity Analysis: Diet Intervention Study
# Analyzes Shannon diversity changes over time by treatment group
# =============================================================================

# -----------------------------------------------------------------------------
# Setup: Load required packages
# -----------------------------------------------------------------------------
library(tidyverse)  # Data manipulation and ggplot2
library(lme4)       # Linear mixed effects models
library(lmerTest)   # p-values for lmer models

# -----------------------------------------------------------------------------
# Data Import and Validation
# -----------------------------------------------------------------------------

# Load data
# ASSUMPTION: CSV has headers matching expected column names
alpha_data <- read_csv("data/alpha_diversity.csv")

# Validate expected columns exist
required_cols <- c("sample_id", "mouse_id", "timepoint", "treatment", "shannon")
missing_cols <- setdiff(required_cols, names(alpha_data))
if (length(missing_cols) > 0) {
  stop("Missing required columns: ", paste(missing_cols, collapse = ", "))
}

# Convert factors and check levels
alpha_data <- alpha_data %>%
  mutate(
    treatment = factor(treatment, levels = c("control", "high_fat")),
    mouse_id = factor(mouse_id),
    timepoint = as.integer(timepoint)
  )

# Check for expected treatment levels
if (!all(c("control", "high_fat") %in% levels(alpha_data$treatment))) {
  warning("Unexpected treatment levels: ", paste(levels(alpha_data$treatment), collapse = ", "))
}

# Report missing data
n_missing <- sum(is.na(alpha_data$shannon))
if (n_missing > 0) {
  message("Note: ", n_missing, " samples have missing Shannon values")
}

# Print data summary
cat("\n=== Data Summary ===\n")
cat("Total samples:", nrow(alpha_data), "\n")
cat("Mice per group:\n")
print(alpha_data %>% distinct(mouse_id, treatment) %>% count(treatment))

# -----------------------------------------------------------------------------
# Summary Statistics for Plotting
# -----------------------------------------------------------------------------

# Calculate mean ± SE by treatment and timepoint
summary_stats <- alpha_data %>%
  group_by(treatment, timepoint) %>%
  summarise(
    mean_shannon = mean(shannon, na.rm = TRUE),
    se_shannon = sd(shannon, na.rm = TRUE) / sqrt(sum(!is.na(shannon))),
    n = sum(!is.na(shannon)),
    .groups = "drop"
  )

# -----------------------------------------------------------------------------
# Visualization: Shannon Diversity Over Time
# -----------------------------------------------------------------------------

# Create publication-quality figure
p <- ggplot(summary_stats, aes(x = timepoint, y = mean_shannon,
                                color = treatment, group = treatment)) +
  geom_line(linewidth = 1) +
  geom_point(size = 3) +
  geom_errorbar(aes(ymin = mean_shannon - se_shannon,
                    ymax = mean_shannon + se_shannon),
                width = 0.5, linewidth = 0.8) +
  scale_color_manual(values = c("control" = "#2166AC", "high_fat" = "#B2182B"),
                     labels = c("Control", "High Fat")) +
  scale_x_continuous(breaks = c(0, 7, 14, 21)) +
  labs(
    x = "Day",
    y = "Shannon Diversity Index",
    color = "Treatment"
  ) +
  theme_bw(base_size = 12) +
  theme(
    panel.grid.minor = element_blank(),
    legend.position = c(0.85, 0.85),
    legend.background = element_rect(color = "gray80")
  )

# Save figure
ggsave("figures/shannon_over_time.pdf", p, width = 6, height = 4, dpi = 300)
cat("\nFigure saved to: figures/shannon_over_time.pdf\n")

# -----------------------------------------------------------------------------
# Statistical Analysis: Linear Mixed Model
# -----------------------------------------------------------------------------

# Fit mixed model with treatment × time interaction
# Random intercept for mouse accounts for repeated measures
# ASSUMPTION: Linear relationship between diversity and time is appropriate
model <- lmer(shannon ~ treatment * timepoint + (1 | mouse_id),
              data = alpha_data)

# Model summary
cat("\n=== Mixed Model Results ===\n")
cat("Model: shannon ~ treatment * timepoint + (1 | mouse_id)\n\n")
print(summary(model))

# ANOVA-style table for fixed effects
cat("\n=== Type III ANOVA Table ===\n")
print(anova(model))

# -----------------------------------------------------------------------------
# End of Script
# -----------------------------------------------------------------------------
```

**Required packages:**
- tidyverse (includes ggplot2, dplyr, readr)
- lme4
- lmerTest

**Assumptions made:**
1. CSV file has headers matching expected column names
2. Treatment levels are exactly "control" and "high_fat"
3. Linear relationship between Shannon diversity and time is appropriate (consider adding polynomial terms if non-linear patterns expected)
4. Random intercept model is sufficient (could consider random slopes if mouse-level trajectories vary)

**Suggested validation checks:**
1. Run `plot(model)` to check residual diagnostics
2. Check for influential points with `influence(model)`
3. Verify the figure matches your mental model of the data
4. Test with a subset of known values to confirm calculations

## Test Input

Use the following scenario to test this prompt:

```
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

**Expected output should include:**
- Complete R script with sections for loading, distance calculation, ordination, plotting, statistics
- Proper use of phyloseq distance() and ordinate() functions
- ggplot2 figure with appropriate aesthetics
- PERMANOVA using adonis2() with strata argument for repeated measures
- Comments explaining each major step
- Required packages list
- Assumptions documented
- Validation checks

**Verification points:**
- Ordination method correct (PCoA on Bray-Curtis)
- PERMANOVA accounts for repeated measures (strata = subject_id)
- Figure aesthetics match request (color = treatment, shape = timepoint)
- Script runs without modification if data exists

## Failure Modes

- **Deprecated functions**: May use functions that have been superseded or removed in newer package versions
- **Package version issues**: May generate code for different package versions than you have installed
- **Logic errors**: Code may run without errors but produce incorrect results (e.g., wrong grouping, incorrect joins)
- **Inefficient code**: May produce working but slow solutions for large datasets
- **Over-engineering**: May add unnecessary complexity when simpler solutions exist
- **Missing edge cases**: May not handle missing data, unexpected factor levels, or other real-world data issues
- **Incorrect statistics**: May apply inappropriate tests or misinterpret model output

## Verification Requirements

1. **Test with known data**: Run on a small dataset where you know the expected output
2. **Check package versions**: Verify packages are installed and functions exist
3. **Validate logic**: Trace through the code to confirm operations match your intent
4. **Check intermediate results**: Print/inspect data at key steps, not just final output
5. **Verify statistical appropriateness**: Confirm the model/test is appropriate for your data structure
6. **Run residual diagnostics**: For statistical models, check assumptions are met
7. **Compare to manual calculation**: For simple operations, verify against hand calculation

## Variations

### Microbiome-specific (phyloseq)
```
Packages: Use phyloseq for microbiome data handling, vegan for diversity calculations.
Input: Describe your phyloseq object structure (OTU table, taxonomy, sample data).
```

### Visualization-focused
```
Task: Focus on creating a publication-ready figure. Include:
- Customizable theme settings
- Color-blind friendly palette options
- Multiple panel layouts if relevant
- Figure legend suitable for a journal caption
```

### Pipeline/workflow script
```
Task: Generate a script that runs a complete analysis pipeline:
- Clear input/output at each stage
- Checkpoint saves for long-running analyses
- Log file generation
- Error handling that allows partial completion
```

## Model Notes

```
Models tested: [To be completed]
Date tested: [To be completed]
Notes: [To be completed]
```

## Cross-References

- For Python equivalent, see `code/python-analysis.md`
- For debugging R errors, see `code/debugging.md`
- For understanding existing R code, see `code/code-explanation.md`
- For test requirements, see `code/testing-requirements.md`
