# Test Results: python-analysis.md

## Test Metadata
- **Prompt:** code/python-analysis.md
- **Model:** Claude Opus 4 (claude-opus-4-5-20251101)
- **Date:** 2026-02-04
- **Tester:** Claude Code

## Test Input Used

Standard test input from prompt file:

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
4. Creates a figure showing diversity over time by delivery mode (mean +/- 95% CI)
5. Outputs: summary statistics table, model results, publication-quality figure

Requirements as specified in the prompt template.
```

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
4. Creates a figure showing diversity over time by delivery mode (mean +/- 95% CI)
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
   - Summary statistics CSV
   - Model results printed to console
   - Publication-quality figure as PDF

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

```python
#!/usr/bin/env python3
"""
Infant Gut Microbiome Diversity Trajectory Analysis

Analyzes longitudinal Shannon diversity data from infant gut microbiome samples,
comparing trajectories between delivery modes (vaginal vs. cesarean). Implements
a linear mixed effects model to account for repeated measures within subjects.

Usage:
    python diversity_trajectory.py input.csv output_prefix

Outputs:
    - {prefix}_summary_stats.csv: Mean diversity by age bin and delivery mode
    - {prefix}_diversity_trajectory.pdf: Publication-quality figure
    - Model results printed to console

Author: [Your name]
Date: [Date]
"""

import argparse
import logging
import sys
import warnings
from pathlib import Path
from typing import Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Suppress convergence warnings for display (still logged)
warnings.filterwarnings('ignore', category=sm.tools.sm_exceptions.ConvergenceWarning)


# =============================================================================
# Data Loading and Validation
# =============================================================================

def load_and_validate_data(filepath: Path) -> pd.DataFrame:
    """
    Load diversity data from CSV and validate expected structure.

    Parameters
    ----------
    filepath : Path
        Path to input CSV file

    Returns
    -------
    pd.DataFrame
        Validated dataframe with expected columns

    Raises
    ------
    FileNotFoundError
        If input file doesn't exist
    ValueError
        If required columns are missing or data validation fails
    """
    if not filepath.exists():
        raise FileNotFoundError(f"Input file not found: {filepath}")

    logger.info(f"Loading data from {filepath}")
    df = pd.read_csv(filepath)

    # ASSUMPTION: These column names exactly match the input file
    required_columns = [
        'sample_id', 'subject_id', 'age_days', 'shannon',
        'observed_features', 'delivery_mode', 'feeding_mode'
    ]

    missing = set(required_columns) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Validate data types and values
    if not pd.api.types.is_numeric_dtype(df['shannon']):
        raise ValueError("'shannon' column must be numeric")

    if not pd.api.types.is_numeric_dtype(df['age_days']):
        raise ValueError("'age_days' column must be numeric")

    # Check delivery_mode values
    valid_delivery = {'vaginal', 'cesarean'}
    actual_delivery = set(df['delivery_mode'].dropna().unique())
    if not actual_delivery.issubset(valid_delivery):
        unexpected = actual_delivery - valid_delivery
        logger.warning(f"Unexpected delivery_mode values: {unexpected}")

    # Report missing data
    n_missing_shannon = df['shannon'].isna().sum()
    if n_missing_shannon > 0:
        logger.warning(f"{n_missing_shannon} samples have missing Shannon values")

    logger.info(f"Loaded {len(df):,} samples from {df['subject_id'].nunique():,} subjects")

    return df


# =============================================================================
# Age Binning
# =============================================================================

def assign_age_bins(df: pd.DataFrame, bin_size_days: int = 30) -> pd.DataFrame:
    """
    Assign samples to age bins (months) based on age in days.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe with 'age_days' column
    bin_size_days : int
        Size of each bin in days (default: 30 for ~monthly bins)

    Returns
    -------
    pd.DataFrame
        Dataframe with added 'age_bin' and 'age_month' columns
    """
    df = df.copy()

    # ASSUMPTION: age_days starts at 0 (birth)
    # Bin labels: 0-30 = month 1, 31-60 = month 2, etc.
    df['age_bin'] = pd.cut(
        df['age_days'],
        bins=range(0, int(df['age_days'].max()) + bin_size_days + 1, bin_size_days),
        labels=False,
        right=True
    )

    # Convert to 1-indexed months for readability
    df['age_month'] = df['age_bin'] + 1

    logger.info(f"Assigned samples to {df['age_month'].nunique()} age bins")

    return df


# =============================================================================
# Summary Statistics
# =============================================================================

def calculate_summary_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate summary statistics for Shannon diversity by age and delivery mode.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with 'age_month', 'delivery_mode', and 'shannon' columns

    Returns
    -------
    pd.DataFrame
        Summary statistics including mean, std, sem, n, and 95% CI bounds
    """
    summary = df.groupby(['age_month', 'delivery_mode']).agg(
        mean_shannon=('shannon', 'mean'),
        std_shannon=('shannon', 'std'),
        n_samples=('shannon', 'count')
    ).reset_index()

    # Calculate standard error and 95% CI
    summary['sem_shannon'] = summary['std_shannon'] / np.sqrt(summary['n_samples'])

    # 95% CI using t-distribution
    from scipy import stats
    summary['ci_95_lower'] = summary.apply(
        lambda row: row['mean_shannon'] - stats.t.ppf(0.975, row['n_samples'] - 1) * row['sem_shannon']
        if row['n_samples'] > 1 else np.nan,
        axis=1
    )
    summary['ci_95_upper'] = summary.apply(
        lambda row: row['mean_shannon'] + stats.t.ppf(0.975, row['n_samples'] - 1) * row['sem_shannon']
        if row['n_samples'] > 1 else np.nan,
        axis=1
    )

    logger.info("Calculated summary statistics")

    return summary


# =============================================================================
# Linear Mixed Effects Model
# =============================================================================

def fit_mixed_model(df: pd.DataFrame) -> Tuple[sm.regression.mixed_linear_model.MixedLMResultsWrapper, str]:
    """
    Fit a linear mixed effects model to compare diversity trajectories.

    Model: shannon ~ age_month * delivery_mode + (1 | subject_id)

    Tests whether delivery mode affects:
    1. Overall diversity level (main effect)
    2. Rate of diversity change over time (interaction)

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with columns: shannon, age_month, delivery_mode, subject_id

    Returns
    -------
    Tuple[MixedLMResultsWrapper, str]
        Fitted model object and formatted results string
    """
    # Prepare data: remove missing values
    model_df = df[['shannon', 'age_month', 'delivery_mode', 'subject_id']].dropna()

    # ASSUMPTION: vaginal is reference category (alphabetically first after sorting)
    # Explicitly set reference for clarity
    model_df['delivery_mode'] = pd.Categorical(
        model_df['delivery_mode'],
        categories=['vaginal', 'cesarean']
    )

    logger.info(f"Fitting mixed model with {len(model_df):,} observations")

    # Fit model with random intercept for subject
    # Formula: diversity ~ age + delivery_mode + age:delivery_mode + (1|subject)
    model = smf.mixedlm(
        formula="shannon ~ age_month * C(delivery_mode, Treatment('vaginal'))",
        data=model_df,
        groups=model_df['subject_id']
    )

    # NOTE: This may be slow with many subjects (>500)
    result = model.fit(reml=True)

    # Format results for display
    results_text = format_model_results(result)

    return result, results_text


def format_model_results(result) -> str:
    """Format mixed model results for console output."""
    lines = [
        "\n" + "=" * 70,
        "LINEAR MIXED EFFECTS MODEL RESULTS",
        "=" * 70,
        f"\nModel: shannon ~ age_month * delivery_mode",
        f"Random effects: (1 | subject_id)",
        f"Reference category: vaginal delivery",
        f"\nNumber of observations: {int(result.nobs):,}",
        f"Number of groups (subjects): {result.n_groups:,}",
        "\n" + "-" * 70,
        "FIXED EFFECTS",
        "-" * 70,
    ]

    # Extract coefficients and p-values
    params = result.params
    pvalues = result.pvalues
    conf_int = result.conf_int()

    for name in params.index:
        coef = params[name]
        pval = pvalues[name]
        ci_low, ci_high = conf_int.loc[name]
        sig = '***' if pval < 0.001 else '**' if pval < 0.01 else '*' if pval < 0.05 else ''

        # Clean up coefficient name for display
        display_name = name.replace("C(delivery_mode, Treatment('vaginal'))[T.cesarean]", "cesarean")
        display_name = display_name.replace("age_month:", "age_month x ")

        lines.append(f"  {display_name:40} {coef:8.4f} [{ci_low:7.4f}, {ci_high:7.4f}] p={pval:.4f} {sig}")

    lines.extend([
        "\n" + "-" * 70,
        "RANDOM EFFECTS",
        "-" * 70,
        f"  Subject variance: {result.cov_re.iloc[0, 0]:.4f}",
        f"  Residual variance: {result.scale:.4f}",
        "\n" + "-" * 70,
        "INTERPRETATION",
        "-" * 70,
    ])

    # Add interpretation
    cesarean_effect = params.get("C(delivery_mode, Treatment('vaginal'))[T.cesarean]", 0)
    interaction = params.get("age_month:C(delivery_mode, Treatment('vaginal'))[T.cesarean]", 0)

    if cesarean_effect < 0:
        lines.append(f"  Cesarean delivery associated with {abs(cesarean_effect):.3f} lower Shannon diversity at baseline")
    else:
        lines.append(f"  Cesarean delivery associated with {cesarean_effect:.3f} higher Shannon diversity at baseline")

    if interaction < 0:
        lines.append(f"  Cesarean infants show {abs(interaction):.4f} slower monthly increase in diversity")
    else:
        lines.append(f"  Cesarean infants show {interaction:.4f} faster monthly increase in diversity")

    lines.append("=" * 70)

    return "\n".join(lines)


# =============================================================================
# Visualization
# =============================================================================

def create_trajectory_figure(
    summary: pd.DataFrame,
    output_path: Path,
    figsize: Tuple[float, float] = (8, 6)
) -> None:
    """
    Create publication-quality figure showing diversity trajectories.

    Parameters
    ----------
    summary : pd.DataFrame
        Summary statistics from calculate_summary_stats()
    output_path : Path
        Path to save figure (PDF)
    figsize : Tuple[float, float]
        Figure dimensions in inches
    """
    # Set publication-quality defaults
    plt.rcParams.update({
        'font.size': 11,
        'axes.labelsize': 12,
        'axes.titlesize': 13,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.dpi': 300
    })

    fig, ax = plt.subplots(figsize=figsize)

    # Color palette - colorblind friendly
    colors = {'vaginal': '#0072B2', 'cesarean': '#D55E00'}
    labels = {'vaginal': 'Vaginal', 'cesarean': 'Cesarean'}

    for delivery_mode in ['vaginal', 'cesarean']:
        data = summary[summary['delivery_mode'] == delivery_mode].sort_values('age_month')

        if len(data) == 0:
            logger.warning(f"No data for delivery_mode: {delivery_mode}")
            continue

        # Plot mean line
        ax.plot(
            data['age_month'],
            data['mean_shannon'],
            color=colors[delivery_mode],
            linewidth=2,
            label=labels[delivery_mode],
            marker='o',
            markersize=5
        )

        # Plot 95% CI as shaded region
        ax.fill_between(
            data['age_month'],
            data['ci_95_lower'],
            data['ci_95_upper'],
            color=colors[delivery_mode],
            alpha=0.2
        )

    # Formatting
    ax.set_xlabel('Age (months)')
    ax.set_ylabel('Shannon Diversity Index')
    ax.set_title('Gut Microbiome Diversity Development\nby Delivery Mode')

    # Set x-axis to show integer months
    max_month = int(summary['age_month'].max())
    ax.set_xticks(range(1, max_month + 1, 2))  # Every 2 months for readability
    ax.set_xlim(0.5, max_month + 0.5)

    # Y-axis: start at 0 unless data goes lower
    y_min = min(0, summary['ci_95_lower'].min() - 0.2)
    y_max = summary['ci_95_upper'].max() + 0.3
    ax.set_ylim(y_min, y_max)

    # Legend
    ax.legend(title='Delivery Mode', loc='lower right', framealpha=0.9)

    # Clean up appearance
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Add subtle grid
    ax.grid(True, alpha=0.3, linestyle='--')

    plt.tight_layout()
    plt.savefig(output_path, format='pdf', bbox_inches='tight', dpi=300)
    plt.close()

    logger.info(f"Saved figure to {output_path}")


# =============================================================================
# Main Execution
# =============================================================================

def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Analyze infant gut microbiome diversity trajectories',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        'input_file',
        type=Path,
        help='Input CSV file with diversity data'
    )
    parser.add_argument(
        'output_prefix',
        type=str,
        help='Prefix for output files'
    )
    parser.add_argument(
        '--bin-size',
        type=int,
        default=30,
        help='Age bin size in days (default: 30)'
    )

    args = parser.parse_args()

    try:
        # Load and prepare data
        df = load_and_validate_data(args.input_file)
        df = assign_age_bins(df, bin_size_days=args.bin_size)

        # Calculate summary statistics
        summary = calculate_summary_stats(df)

        # Save summary statistics
        summary_path = Path(f"{args.output_prefix}_summary_stats.csv")
        summary.to_csv(summary_path, index=False)
        logger.info(f"Saved summary statistics to {summary_path}")

        # Print summary table
        print("\n=== Summary Statistics (first 10 rows) ===")
        print(summary.head(10).to_string(index=False))

        # Fit mixed model
        model_result, model_text = fit_mixed_model(df)
        print(model_text)

        # Create figure
        figure_path = Path(f"{args.output_prefix}_diversity_trajectory.pdf")
        create_trajectory_figure(summary, figure_path)

        print(f"\n=== Analysis Complete ===")
        print(f"Summary statistics: {summary_path}")
        print(f"Figure: {figure_path}")

    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

---

**Requirements (requirements.txt):**
```
pandas>=1.5.0
numpy>=1.21.0
scipy>=1.9.0
matplotlib>=3.5.0
seaborn>=0.12.0
statsmodels>=0.13.0
```

**Or for conda (environment.yml):**
```yaml
name: diversity_analysis
channels:
  - conda-forge
dependencies:
  - python>=3.10
  - pandas>=1.5
  - numpy>=1.21
  - scipy>=1.9
  - matplotlib>=3.5
  - seaborn>=0.12
  - statsmodels>=0.13
```

---

**Assumptions made:**

1. **Age binning**: Days 1-30 = month 1, days 31-60 = month 2, etc. Adjust `--bin-size` if different binning is needed.

2. **Column names**: Exact match to specified names (sample_id, subject_id, age_days, shannon, delivery_mode, feeding_mode, observed_features).

3. **Delivery mode values**: Expected to be exactly "vaginal" or "cesarean" (case-sensitive).

4. **Reference category**: Vaginal delivery is used as the reference (baseline) for the mixed model. Cesarean effects are relative to vaginal.

5. **Random effects structure**: Random intercept only. If individual trajectories vary substantially, a random slope model (random intercept + slope for age) may be more appropriate but requires more data per subject.

6. **Missing data handling**: Samples with missing Shannon values are excluded from analysis. Missing values are not imputed.

7. **Independence of observations within bin**: The summary statistics treat samples within an age bin as independent for CI calculation. The mixed model properly accounts for within-subject correlation.

---

**Validation checks:**

1. **Test with small dataset**: Create a test file with 5-10 subjects and verify:
   - Summary statistics match manual calculation
   - Figure displays correctly
   - Model runs without errors

2. **Check data loading**:
   ```python
   df = pd.read_csv("your_file.csv")
   print(df.dtypes)
   print(df['delivery_mode'].value_counts())
   print(df.groupby('subject_id').size().describe())
   ```

3. **Verify age binning**:
   ```python
   print(df[['age_days', 'age_month']].drop_duplicates().sort_values('age_days'))
   ```

4. **Check model assumptions**:
   - Plot residuals: `plt.hist(model_result.resid)`
   - Check for normality: `scipy.stats.normaltest(model_result.resid)`
   - Inspect random effects: `model_result.random_effects`

5. **Verify figure accuracy**:
   - Spot-check a few data points against the summary CSV
   - Ensure CI bands look reasonable (not impossibly narrow or wide)

6. **Cross-validate with R**: If possible, run the same model in R with lme4:
   ```r
   library(lme4)
   model <- lmer(shannon ~ age_month * delivery_mode + (1|subject_id), data=df)
   summary(model)
   ```

## Overall Assessment

- **Recommendation:** Pass
- **Notes:** The script demonstrates proper handling of longitudinal microbiome data. The mixed model specification (random intercept for subject) is appropriate for the described data structure. The visualization uses colorblind-friendly colors and includes proper uncertainty representation. One potential enhancement would be to add a random slope term if individual trajectories are suspected to vary, but the current approach is a reasonable default.

## Verification Steps Tested

1. **Script has proper structure:** Verified
   - Main function with `if __name__ == "__main__":` guard
   - Functions with docstrings
   - Grouped imports (standard, third-party)
   - Type hints throughout

2. **Statistical model appropriate for longitudinal data:** Verified
   - Uses linear mixed effects model with random intercept for subject
   - Correctly accounts for repeated measures within subjects
   - Formula includes age x delivery_mode interaction to test trajectory differences

3. **Figure shows trajectory with confidence intervals:** Verified
   - Mean line with markers for each delivery mode
   - 95% CI as shaded region using proper t-distribution calculation
   - Colorblind-friendly palette

4. **Error handling for missing data:** Verified
   - Checks for missing Shannon values and logs warning
   - Drops NA values before model fitting
   - Validates required columns exist
