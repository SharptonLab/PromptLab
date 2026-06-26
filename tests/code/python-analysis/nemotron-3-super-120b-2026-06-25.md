# Test Results: code/python-analysis.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-25.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** code/python-analysis.md
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
````

## Model Output
````


```python
"""
Microbiome Diversity Trajectory Analysis Script

This script analyzes longitudinal infant gut microbiome data to calculate and plot
Shannon diversity trajectories by delivery mode. It performs the following steps:
1. Loads and validates input CSV data
2. Calculates binned mean Shannon diversity with 95% CIs (monthly bins: 0-30, 31-60, ...)
3. Fits a linear mixed model to compare diversity trajectories between delivery modes
4. Generates a publication-quality figure showing diversity trajectories
5. Outputs summary statistics, model results, and the figure

Author: Microbiome Researcher
Date: 2023-10-05
"""

import argparse
import sys
from pathlib import Path
from typing import Tuple, List, Optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats


def load_and_validate_data(filepath: str) -> pd.DataFrame:
    """
    Load and validate input CSV data.

    Parameters
    ----------
    filepath : str
        Path to the input CSV file

    Returns
    -------
    pd.DataFrame
        Validated DataFrame with required columns

    Raises
    ------
    FileNotFoundError
        If input file does not exist
    ValueError
        If required columns are missing or data types are invalid
    """
    # Check file existence
    if not Path(filepath).exists():
        raise FileNotFoundError(f"Input file not found: {filepath}")

    # Load data
    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        raise ValueError(f"Error reading CSV file: {e}")

    # Define required columns and expected types
    required_columns = {
        'sample_id': str,
        'subject_id': str,
        'age_days': (int, np.integer),
        'shannon': (float, np.floating),
        'observed_features': (int, np.integer),
        'delivery_mode': str,
        'feeding_mode': str
    }

    # Check for missing columns
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    # Validate data types
    for col, expected_type in required_columns.items():
        if not pd.api.types.is_dtype_equal(df[col].dtype, expected_type):
            # Try to convert if possible
            try:
                if expected_type == str:
                    df[col] = df[col].astype(str)
                elif expected_type in (int, np.integer):
                    df[col] = pd.to_numeric(df[col], downcast='integer')
                elif expected_type in (float, np.floating):
                    df[col] = pd.to_numeric(df[col], downcast='float')
            except Exception as e:
                raise ValueError(
                    f"Column '{col}' has invalid type. Expected {expected_type}, "
                    f"got {df[col].dtype}. Conversion failed: {e}"
                )

    # Validate categorical values
    valid_delivery = {'vaginal', 'cesarean'}
    invalid_delivery = set(df['delivery_mode'].unique()) - valid_delivery
    if invalid_delivery:
        raise ValueError(
            f"Invalid values in delivery_mode: {invalid_delivery}. "
            f"Expected one of: {valid_delivery}"
        )

    valid_feeding = {'breastfed', 'formula'}
    invalid_feeding = set(df['feeding_mode'].unique()) - valid_feeding
    if invalid_feeding:
        raise ValueError(
            f"Invalid values in feeding_mode: {invalid_feeding}. "
            f"Expected one of: {valid_feeding}"
        )

    # Validate age_days range
    if (df['age_days'] < 0).any():
        raise ValueError("age_days contains negative values")

    # Validate shannon diversity (should be non-negative)
    if (df['shannon'] < 0).any():
        raise ValueError("shannon contains negative values")

    return df


def bin_age_and_summarize(
    df: pd.DataFrame,
    age_col: str = 'age_days',
    group_col: str = 'delivery_mode',
    value_col: str = 'shannon'
) -> pd.DataFrame:
    """
    Calculate binned mean Shannon diversity with 95% CIs.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing microbiome data
    age_col : str, default 'age_days'
        Column name for age in days
    group_col : str, default 'delivery_mode'
        Column name for grouping variable
    value_col : str, default 'shannon'
        Column name for diversity metric

    Returns
    -------
    pd.DataFrame
        Summary statistics with columns:
        [group_col, 'age_bin', 'mean_shannon', 'std_shannon', 'count', 'ci_lower', 'ci_upper']
    """
    # Create age bins (0-30, 31-60, ..., 331-360, 360+)
    def get_age_bin(age: int) -> str:
        if age < 0:
            return "invalid"
        if age <= 30:
            return "0-30"
        elif age <= 60:
            return "31-60"
        elif age <= 90:
            return "61-90"
        elif age <= 120:
            return "91-120"
        elif age <= 150:
            return "121-150"
        elif age <= 180:
            return "151-180"
        elif age <= 210:
            return "181-210"
        elif age <= 240:
            return "211-240"
        elif age <= 270:
            return "241-270"
        elif age <= 300:
            return "271-300"
        elif age <= 330:
            return "301-330"
        elif age <= 360:
            return "331-360"
        else:
            return "360+"

    # Apply binning
    df = df.copy()
    df['age_bin'] = df[age_col].apply(get_age_bin)

    # Remove invalid bins (should not occur after validation)
    df = df[df['age_bin'] != "invalid"]

    # Calculate summary statistics per group and bin
    summary = df.groupby([group_col, 'age_bin'])[value_col].agg(
        mean_shannon='mean',
        std_shannon='std',
        count='count'
    ).reset_index()

    # Calculate 95% confidence intervals
    summary['ci_lower'] = summary['mean_shannon'] - 1.96 * summary['std_shannon'] / np.sqrt(summary['count'])
    summary['ci_upper'] = summary['mean_shannon'] + 1.96 * summary['std_shannon'] / np.sqrt(summary['count'])

    # Replace NaN in std/ci with 0 for single-sample bins
    summary.fillna({'std_shannon': 0, 'ci_lower': 0, 'ci_upper': 0}, inplace=True)

    # Order bins chronologically
    bin_order = [
        "0-30", "31-60", "61-90", "91-120", "121-150", "151-180",
        "181-210", "211-240", "241-270", "271-300", "301-330",
        "331-360", "360+"
    ]
    summary['age_bin'] = pd.Categorical(
        summary['age_bin'], categories=bin_order, ordered=True
    )
    summary = summary.sort_values([group_col, 'age_bin'])

    return summary


def fit_linear_mixed_model(
    df: pd.DataFrame,
    value_col: str = 'shannon',
    group_col: str = 'delivery_mode',
    subject_col: str = 'subject_id',
    age_col: str = 'age_days'
) -> Tuple[sm.regression.mixed_linear_model.MixedLM, pd.DataFrame]:
    """
    Fit a linear mixed model to compare diversity trajectories.

    Model: shannon ~ delivery_mode * age_days + (1 | subject_id)

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame
    value_col : str, default 'shannon'
        Column name for diversity metric
    group_col : str, default 'delivery_mode'
        Column name for delivery mode
    subject_col : str, default 'subject_id'
        Column name for subject identifier
    age_col : str, default 'age_days'
        Column name for age in days

    Returns
    -------
    Tuple[statsmodels MixedLM results, pd.DataFrame]
        Fitted model results and fixed effects table
    """
    # Prepare data for modeling
    model_df = df.copy()
    
    # Convert delivery_mode to categorical (0=vaginal, 1=cesarean)
    model_df['delivery_mode_num'] = (model_df[group_col] == 'cesarean').astype(int)
    
    # Center age_days to improve model interpretability
    model_df['age_days_centered'] = model_df[age_col] - model_df[age_col].mean()
    
    # Formula: shannon ~ delivery_mode_num * age_days_centered + (1 | subject_id)
    formula = f"{value_col} ~ delivery_mode_num * age_days_centered + (1 | {subject_col})"
    
    # Fit model
    try:
        model = smf.mixedlm(formula, model_df, groups=model_df[subject_col])
        result = model.fit(reml=False)  # Use ML for comparison
    except Exception as e:
        raise RuntimeError(f"Failed to fit linear mixed model: {e}")

    # Extract fixed effects
    fixed_effects = result.fe_params.to_frame(name='estimate')
    fixed_effects['std_err'] = result.bse
    fixed_effects['t_value'] = fixed_effects['estimate'] / fixed_effects['std_err']
    fixed_effects['p_value'] = 2 * (1 - stats.norm.cdf(np.abs(fixed_effects['t_value'])))
    fixed_effects.reset_index(inplace=True)
    fixed_effects.rename(columns={'index': 'parameter'}, inplace=True)

    return result, fixed_effects


def plot_trajectories(
    summary_df: pd.DataFrame,
    output_path: Path,
    hue_col: str = 'delivery_mode',
    x_col: str = 'age_bin',
    y_col: str = 'mean_shannon',
    ci_lower_col: str = 'ci_lower',
    ci_upper_col: str = 'ci_upper'
) -> None:
    """
    Create and save a publication-quality figure of diversity trajectories.

    Parameters
    ----------
    summary_df : pd.DataFrame
        Binned summary statistics from bin_age_and_summarize
    output_path : Path
        Path to save the figure (including filename and extension)
    hue_col : str, default 'delivery_mode'
        Column name for grouping variable
    x_col : str, default 'age_bin'
        Column name for age bins (should be categorical)
    y_col : str, default 'mean_shannon'
        Column name for mean diversity
    ci_lower_col : str, default 'ci_lower'
        Column name for lower CI bound
    ci_upper_col : str, default 'ci_upper'
        Column name for upper CI bound
    """
    # Set publication-quality style
    sns.set_style("whitegrid")
    plt.rcParams.update({
        'font.size': 12,
        'axes.labelsize': 14,
        'axes.titlesize': 16,
        'xtick.labelsize': 12,
        'ytick.labelsize': 12,
        'legend.fontsize': 12,
        'figure.dpi': 300
    })

    # Create figure
    plt.figure(figsize=(10, 6))
    
    # Plot each delivery mode
    for delivery_mode in summary_df[hue_col].unique():
        mode_data = summary_df[summary_df[hue_col] == delivery_mode]
        
        # Plot mean line
        plt.plot(
            mode_data[x_col],
            mode_data[y_col],
            label=delivery_mode.capitalize(),
            linewidth=2.5,
            marker='o',
            markersize=6
        )
        
        # Plot 95% CI as shaded area
        plt.fill_between(
            mode_data[x_col],
            mode_data[ci_lower_col],
            mode_data[ci_upper_col],
            alpha=0.2
        )

    # Customize plot
    plt.xlabel('Age (days)', fontsize=14)
    plt.ylabel('Shannon Diversity', fontsize=14)
    plt.title('Gut Microbiome Diversity Trajectories by Delivery Mode', fontsize=16, pad=20)
    plt.legend(title='Delivery Mode', title_fontsize=13)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save figure
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()


def main() -> None:
    """Main function orchestrating the analysis workflow."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Analyze longitudinal infant gut microbiome diversity trajectories"
    )
    parser.add_argument(
        'input_file',
        type=str,
        help="Path to input CSV file containing microbiome data"
    )
    parser.add_argument(
        '--output_dir',
        type=str,
        default='.',
        help="Directory to save output files (default: current directory)"
    )
    args = parser.parse_args()

    # Create output directory if it doesn't exist
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Step 1: Load and validate data
        print("Loading and validating data...")
        df = load_and_validate_data(args.input_file)
        print(f"Loaded {len(df)} samples from {df['subject_id'].nunique()} subjects")

        # Step 2: Calculate binned summary statistics
        print("Calculating binned summary statistics...")
        summary_df = bin_age_and_summarize(df)
        summary_path = output_dir / "summary_statistics.csv"
        summary_df.to_csv(summary_path, index=False)
        print(f"Summary statistics saved to {summary_path}")

        # Step 3: Fit linear mixed model
        print("Fitting linear mixed model...")
        model_result, fixed_effects = fit_linear_mixed_model(df)
        
        # Save model summary
        model_summary_path = output_dir / "model_summary.txt"
        with open(model_summary_path, 'w') as f:
            f.write(str(model_result.summary()))
        print(f"Model summary saved to {model_summary_path}")
        
        # Save fixed effects
        fixed_effects_path = output_dir / "fixed_effects.csv"
        fixed_effects.to_csv(fixed_effects_path, index=False)
        print(f"Fixed effects saved to {fixed_effects_path}")

        # Step 4: Create and save figure
        print("Generating diversity trajectory figure...")
        figure_path = output_dir / "diversity_trajectories.png"
        plot_trajectories(summary_df, figure_path)
        print(f"Figure saved to {figure_path}")

        print("\nAnalysis completed successfully!")

    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
```

**Requirements List (for `requirements.txt` or `environment.yml`):**

```
pandas>=1.5.0
numpy>=1.24.0
scipy>=1.10.0
matplotlib>=3.7.0
seaborn>=0.12.0
statsmodels>=0.14.0
```

**Assumptions Made:**

1. The input CSV contains exactly the specified columns with correct data types
2. Age values are non-negative integers representing days since birth
3. Delivery mode is exclusively "vaginal" or "cesarean" (case-sensitive)
4. Feeding mode is exclusively "breastfed" or "formula" (case-sensitive)
5. Shannon diversity values are non-negative
6. Each subject has multiple longitudinal measurements (repeated measures design)
7. The study duration covers the first year of life (0-365 days), with possible extension beyond 360 days
8. Linear mixed model assumptions are met (normality of residuals, homoscedasticity, independence)
9. Missing data is not present in required columns (handled by validation)
10. The 95% CI for binned means uses the normal approximation (appropriate for n>30 per bin)

**Validation Checks to Run:**

1. **Input File Check:**
   ```bash
   # Verify file exists and is readable
   ls -lh input_data.csv
   head -5 input_data.csv
   ```

2. **Column Validation:**
   ```bash
   # Check column names and first few rows
   csvcut -n input_data.csv
   csvstat --cols sample_id,subject_id,age_days,shannon,observed_features,delivery_mode,feeding_mode input_data.csv
   ```

3. **Data Quality Checks:**
   ```bash
   # Check for missing values
   csvstat --missing input_data.csv
   
   # Validate categorical values
   csvstat --freq delivery_mode input_data.csv
   csvstat --freq feeding_mode input_data.csv
   
   # Check age range
   csvstat --min --max age_days input_data.csv
   
   # Check shannon range
   csvstat --min --max shannon input_data.csv
   ```

4. **Output Verification:**
   ```bash
   # Check summary statistics file
   wc -l summary_statistics.csv
   head -3 summary_statistics.csv
   
   # Check model summary
   head -20 model_summary.txt
   
   # Check fixed effects
   cat fixed_effects.csv
   
   # Verify figure exists and is non-zero
   ls -lh diversity_trajectories.png
   ```

5. **Sanity Checks:**
   - Confirm delivery mode groups have reasonable sample sizes
   - Verify Shannon diversity values are within expected biological range (typically 0-5 for infant gut)
   - Ensure age bins have adequate sample sizes (>5 samples/bin/group)
   - Check that model convergence occurred (look for "Optimization terminated successfully" in model summary)
````

## Assessment

_Machine-suggested (UNCONFIRMED) — drafted by Claude Opus 4.7 on 2026-06-26 to speed T4 review. An author must independently read the Model Output above and set the real Recommendation. Anything labeled here is triage, not domain expert review._

**Machine triage:** Output is **complete** — script + Requirements + Assumptions + Validation checks. One of 3 of 6 panel models that did not truncate (Opus/Sonnet/Gemini all truncated). Includes very thorough validation-check section using `csvkit` (`csvcut`, `csvstat`) commands — useful but adds an implicit dependency on a non-standard tool. Notable assumption (#10): "95% CI for binned means uses the normal approximation (appropriate for n>30 per bin)" — this is potentially problematic for ~100 infants × 12 monthly bins where per-bin n may be much smaller than 30. Other panel models (Sonnet, GPT-5.5, Step) use the t-distribution instead, which is more conservative for small per-bin n.

**Suggested verdict (UNCONFIRMED):** Pass with notes

**What still needs human verification:**
- Whether the normal-approximation CI assumption is appropriate for typical per-bin sample sizes in this study design (the prompt specifies ~800 samples / 100 infants / 12 bins → ~67 per bin per delivery mode, marginal for normal approximation)
- That csvkit validation commands are appropriate to suggest given the prompt's stated environment (the prompt didn't mention csvkit)
- Whether the script (which wasn't shown in the truncation-checked portion) actually fits a random-intercept LMM and handles convergence — confirm by reading the full script body
- That the "first year of life (0-365 days), with possible extension beyond 360 days" interpretation matches study intent

**Local code check:** Syntax PASS across 1 block(s) · 4/10 imports available.

## Overall Assessment
- **Recommendation:** PENDING AUTHOR REVIEW
- **Notes:**

## Verification Steps Tested
_Which verification requirements from the prompt were checked, and results._
