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

## Example Output

For a representative model response to the Test Input, see:

`tests/code/r-script-generation/claude-sonnet-4-6-2026-06-25.md`

That cell was captured on 2026-06-25 and human-verified by both project reviewers as passing. Other panel models' responses (Claude Opus 4.7, GPT-5.5, Gemini 2.5 Pro, Nemotron 3 Super 120B, Step-3.7 Flash) are alongside it in the same directory.

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
Tested across the panel; verdicts set by human review.

- Claude Opus 4 (claude-opus-4-5-20251101) (2026-02-04): Pass
- claude-opus-4.7 (2026-06-25): Pass
- claude-sonnet-4.6 (2026-06-25): Pass
- gemini-2.5-pro (2026-06-25): Pass
- gpt-5.5 (2026-06-25): Pass
- nemotron-3-super-120b (2026-06-25): Pass
- step-3.7-flash (2026-06-25): Pass

Full per-model raw outputs and reviewer notes: tests/code/r-script-generation/
```

## Cross-References

- For Python equivalent, see `code/python-analysis.md`
- For debugging R errors, see `code/debugging.md`
- For understanding existing R code, see `code/code-explanation.md`
- For test requirements, see `code/testing-requirements.md`
