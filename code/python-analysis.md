# Python Analysis Script Generation Prompt

## Task Description

Generate Python scripts for data analysis, bioinformatics, and scientific computing tasks, with emphasis on readable code, proper documentation, and reproducibility.

## When to Use

- Creating analysis scripts using pandas, numpy, scipy, scikit-learn, or biopython
- Generating data processing pipelines
- Implementing bioinformatics workflows
- Learning how to use specific Python libraries for analysis

## When NOT to Use

- For analyses you don't understand well enough to verify
- When you need production code without testing
- For performance-critical applications without profiling
- When the task requires deep domain knowledge you can't communicate

## The Prompt

```
Context: I am a {RESEARCHER_ROLE} working on {RESEARCH_CONTEXT}. I need a Python script to {GENERAL_GOAL}.

Data description:
- Input: {DESCRIBE_INPUT: file format, structure, columns/fields}
- Sample size: {APPROXIMATE_SIZE}
- Key variables: {LIST_KEY_VARIABLES}

Environment:
- Python version: {VERSION: e.g., "3.10+"}
- Key packages available: {PACKAGES: e.g., "pandas, numpy, scipy, scikit-learn, matplotlib"}
- Environment manager: {CONDA/VENV/NONE}

Task: Write a Python script that:
{SPECIFIC_TASK_DESCRIPTION}

Requirements:
1. **Structure**:
   - Use functions with docstrings for reusable operations
   - Include a `main()` function with `if __name__ == "__main__":` guard
   - Group imports at the top (standard library, third-party, local)

2. **Documentation**:
   - Module-level docstring describing the script's purpose
   - Type hints for function arguments and returns
   - Comments for non-obvious logic

3. **Error handling**:
   - Validate inputs exist and have expected format
   - Provide informative error messages
   - Handle common failure modes gracefully

4. **Output**:
   - {DESCRIBE_DESIRED_OUTPUT}

Constraints:
- Use only packages from standard library, PyPI, or conda-forge
- Prefer pandas/numpy idioms over loops where appropriate
- Flag assumptions about data structure with comments
- Note any operations that may be slow on large data

Output format: Complete Python script. After the script, provide:
- Requirements list (for requirements.txt or environment.yml)
- Assumptions made
- Validation checks to run
```

## Prompt Components Explained

| Component | Purpose |
|-----------|---------|
| **Research context** | Tailors approach to scientific computing conventions |
| **Data description** | Essential for generating appropriate code |
| **Environment** | Ensures compatibility with your setup |
| **Structure requirements** | Produces maintainable, reusable code |
| **Documentation requirements** | Supports reproducibility and understanding |
| **Constraints** | Keeps solutions practical |

## Example Output

For a representative model response to the Test Input, see:

`tests/code/python-analysis/claude-sonnet-4-6-2026-06-25.md`

That cell was captured on 2026-06-25 and human-verified by both project reviewers as passing. Other panel models' responses (Claude Opus 4.7, GPT-5.5, Gemini 2.5 Pro, Nemotron 3 Super 120B, Step-3.7 Flash) are alongside it in the same directory.

## Test Input

Use the following scenario to test this prompt:

```
Context: I am a microbiome researcher working on a longitudinal infant gut microbiome study. I need a Python script to calculate and plot diversity trajectories.

Data description:
- Input: CSV file with columns: sample_id, subject_id, age_days, shannon, observed_features, delivery_mode (vaginal/cesarean), feeding_mode (breastfed/formula)
- Sample size: ~800 samples from 100 infants, sampled every 2 weeks for first year
- Key variables: shannon (numeric), age_days (integer), subject_id (string), delivery_mode (categorical)

Environment:
- Python version: 3.10+
- Key packages: pandas, numpy, scipy, matplotlib, seaborn
- Environment: conda

Task: Write a Python script that:
1. Loads the data and validates expected columns
2. Calculates mean Shannon diversity at each age (binned by month: 0-30, 31-60, etc.)
3. Compares diversity trajectories between delivery modes using a linear mixed model
4. Creates a figure showing diversity over time by delivery mode (mean ± 95% CI)
5. Outputs: summary statistics table, model results, publication-quality figure

Requirements:
1. **Structure**:
   - Use functions with docstrings for reusable operations
   - Include a `main()` function with `if __name__ == "__main__":` guard
   - Group imports at the top (standard library, third-party, local)

2. **Documentation**:
   - Module-level docstring describing the script's purpose
   - Type hints for function arguments and returns
   - Comments for non-obvious logic

3. **Error handling**:
   - Validate inputs exist and have expected format
   - Provide informative error messages
   - Handle common failure modes gracefully

4. **Output**:
   - Summary statistics table (CSV), linear mixed model results (text/CSV), publication-quality figure showing diversity trajectories by delivery mode with mean ± 95% CI

Constraints:
- Use only packages from standard library, PyPI, or conda-forge
- Prefer pandas/numpy idioms over loops where appropriate
- Flag assumptions about data structure with comments
- Note any operations that may be slow on large data

Output format: Complete Python script. After the script, provide:
- Requirements list (for requirements.txt or environment.yml)
- Assumptions made
- Validation checks to run
```

**Expected output should include:**
- Complete Python script with:
  - Proper imports and docstrings
  - Data loading with validation
  - Age binning logic (0-30 days = month 1, etc.)
  - Linear mixed model using statsmodels
  - Seaborn or matplotlib figure with error bands
  - Type hints and comments
- Requirements list
- Assumptions documented (e.g., age binning approach)
- Validation checks suggested

**Verification points:**
- Script has proper structure (main function, if __name__ guard)
- Statistical model appropriate for longitudinal data with random effects
- Figure shows trajectory with confidence intervals
- Error handling for missing data

## Failure Modes

- **API changes**: May use deprecated pandas/numpy syntax
- **Memory issues**: May not handle very large files efficiently (consider chunked reading)
- **Logic errors**: Groupby/aggregation operations may not match your intent
- **Type errors**: May assume data types that don't match your actual data
- **Path issues**: May not handle Windows/Unix path differences correctly
- **Edge cases**: May fail on empty files, missing columns, or unexpected values
- **Performance**: Suggested operations may be slow on large datasets

## Verification Requirements

1. **Test on small sample**: Verify output on a file small enough to check manually
2. **Check intermediate steps**: Print DataFrame shapes and samples at each stage
3. **Validate logic**: Trace through groupby operations to confirm they match intent
4. **Test edge cases**: Run on files with missing data, single rows, duplicates
5. **Verify numeric results**: Spot-check calculations against manual computation
6. **Check file I/O**: Confirm output files are created and readable

## Variations

### Bioinformatics pipeline (Snakemake/Nextflow integration)
```
Task: Generate a script designed to be called from a workflow manager.
Requirements: Accept input/output as command-line arguments, return non-zero exit codes on failure, produce log output suitable for workflow manager capture.
```

### Jupyter notebook format
```
Task: Generate code as Jupyter notebook cells with markdown explanations.
Format: Provide as a sequence of cells (markdown and code) that can be copied into a notebook or converted using jupytext.
```

### Parallelized processing
```
Additional requirement: The data is too large for single-threaded processing.
Use multiprocessing or dask for parallel execution. Include progress reporting.
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

Full per-model raw outputs and reviewer notes: tests/code/python-analysis/
```

## Cross-References

- For R equivalent, see `code/r-script-generation.md`
- For debugging Python errors, see `code/debugging.md`
- For understanding existing code, see `code/code-explanation.md`
- For test requirements, see `code/testing-requirements.md`
