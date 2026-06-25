# Test Results: code/python-analysis.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-23.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** code/python-analysis.md
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

Requirements as specified in the prompt template.
```

## Model Output
```


**Python script**

```python
#!/usr/bin/env python
"""
microbiome_diversity_trajectories.py

Calculate and plot longitudinal Shannon diversity trajectories from an infant gut
microbiome study.

The script:
1. Loads a CSV file and validates expected columns.
2. Bins infant age into monthly intervals (0‑30, 31‑60, … days).
3. Computes mean Shannon diversity ± 95 % confidence interval per age bin and
   delivery mode.
4. Fits a linear mixed‑effects model (random intercept for subject) to test
   whether delivery mode influences the diversity trajectory.
5. Saves:
   - a summary statistics CSV (mean, SEM, CI per bin & delivery mode),
   - a CSV with the mixed‑model fixed‑effects table,
   - a publication‑quality figure (PNG) showing diversity over time by delivery
     mode with shaded 95 % CI bands.

Usage
-----
    python microbiome_diversity_trajectories.py --input data.csv \
        --output-dir results/

Parameters
----------
--input : str
    Path to the input CSV file.
--output-dir : str
    Directory where output files will be written (created if missing).
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats


# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def load_and_validate(filepath: Path) -> pd.DataFrame:
    """
    Load CSV and check for required columns.

    Parameters
    ----------
    filepath : pathlib.Path
        Path to the input CSV.

    Returns
    -------
    pd.DataFrame
        Loaded data with missing key variables removed.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If expected columns are missing.
    """
    if not filepath.is_file():
        raise FileNotFoundError(f"Input file not found: {filepath}")

    df = pd.read_csv(filepath)

    expected_cols = {
        "sample_id",
        "subject_id",
        "age_days",
        "shannon",
        "observed_features",
        "delivery_mode",
        "feeding_mode",
    }
    missing = expected_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing expected columns: {missing}")

    # Drop rows where key variables are missing – they cannot be used in analysis
    key_vars = ["subject_id", "age_days", "shannon", "delivery_mode"]
    initial_len = len(df)
    df = df.dropna(subset=key_vars)
    if len(df) < initial_len:
        print(
            f"Warning: Dropped {initial_len - len(df)} rows with missing key variables."
        )

    # Ensure correct dtypes
    df["age_days"] = df["age_days"].astype(int)
    df["delivery_mode"] = df["delivery_mode"].astype(str).str.lower()
    df["feeding_mode"] = df["feeding_mode"].astype(str).str.lower()

    return df


def bin_age(df: pd.DataFrame, bin_width: int = 30) -> pd.DataFrame:
    """
    Create an age bin column based on ``bin_width`` days.

    Parameters
    ----------
    df : pd.DataFrame
        Input data containing ``age_days``.
    bin_width : int, default 30
        Width of each age bin in days.

    Returns
    -------
    pd.DataFrame
        Copy of ``df`` with an additional ``age_bin`` column (interval label).
    """
    max_age = df["age_days"].max()
    # Create bins from 0 to the next multiple of bin_width beyond max_age
    bin_edges = list(range(0, ((max_age // bin_width) + 2) * bin_width + 1, bin_width))
    # Use pd.cut with right=False to get intervals like [0,30), [30,60), …
    df = df.copy()
    df["age_bin"] = pd.cut(
        df["age_days"],
        bins=bin_edges,
        right=False,
        labels=[f"{i}-{i+bin_width-1}" for i in bin_edges[:-1]],
    )
    return df


def compute_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate mean Shannon diversity, standard error, and 95 % CI per age bin
    and delivery mode.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing ``age_bin``, ``delivery_mode``, and ``shannon``.

    Returns
    -------
    pd.DataFrame
        Summary table with columns:
        ['age_bin', 'delivery_mode', 'n', 'mean_shannon', 'sem', 'ci_low', 'ci_high']
    """
    grouped = (
        df.groupby(["age_bin", "delivery_mode"], observed=False)["shannon"]
        .agg(["count", "mean", "std"])
        .reset_index()
    )
    grouped.rename(
        columns={"count": "n", "mean": "mean_shannon", "std": "std_shannon"},
        inplace=True,
    )
    grouped["sem"] = grouped["std_shannon"] / np.sqrt(grouped["n"])
    grouped["ci_low"] = grouped["mean_shannon"] - 1.96 * grouped["sem"]
    grouped["ci_high"] = grouped["mean_shannon"] + 1.96 * grouped["sem"]
    # Keep only needed columns
    summary = grouped[
        ["age_bin", "delivery_mode", "n", "mean_shannon", "sem", "ci_low", "ci_high"]
    ]
    return summary


def fit_mixed_model(df: pd.DataFrame) -> Tuple[sm.regression.linear_model.RegressionResultsWrapper, pd.DataFrame]:
    """
    Fit a linear mixed‑effects model with random intercept for subject.

    Model: shannon ~ age_days * delivery_mode + (1|subject_id)

    Parameters
    ----------
    df : pd.DataFrame
        Input data with columns ``shannon``, ``age_days``, ``delivery_mode``,
        ``subject_id``.

    Returns
    -------
    model_result : statsmodels regression results object
        Fitted MixedLM model.
    fixed_effects_df : pd.DataFrame
        Table of fixed‑effect estimates, std err, z, p‑value, and confidence
        intervals.
    """
    # Ensure categorical treatment
    df = df.copy()
    df["delivery_mode"] = pd.Categorical(
        df["delivery_mode"], categories=["cesarean", "vaginal"]
    )

    # Formula for MixedLM
    formula = "shannon ~ age_days * delivery_mode"
    try:
        model = smf.mixedlm(formula, df, groups=df["subject_id"]).fit(reml=False)
    except Exception as exc:
        raise RuntimeError(f"MixedLM fitting failed: {exc}") from exc

    # Extract fixed effects into a tidy DataFrame
    fe = model.fe_params
    se = model.bse_fe
    z = model.tvalues  # statsmodels uses t-values for fixed effects
    p = model.pvalues_fe
    ci_low = fe - 1.96 * se
    ci_high = fe + 1.96 * se

    fixed_effects_df = pd.DataFrame(
        {
            "parameter": fe.index,
            "estimate": fe.values,
            "std_err": se.values,
            "z_value": z.values,
            "p_value": p.values,
            "ci_low": ci_low.values,
            "ci_high": ci_high.values,
        }
    )
    return model, fixed_effects_df


def plot_trajectories(
    summary_df: pd.DataFrame,
    raw_df: pd.DataFrame,
    output_path: Path,
    dpi: int = 300,
) -> None:
    """
    Create a line plot of mean Shannon diversity ± 95 % CI by delivery mode.

    Parameters
    ----------
    summary_df : pd.DataFrame
        Output of :func:`compute_summary`.
    raw_df : pd.DataFrame
        Original data (used for optional jittered points; not plotted here).
    output_path : pathlib.Path
        File path where the figure will be saved (PNG).
    dpi : int, default 300
        Resolution of the saved figure.
    """
    # Set seaborn style for publication quality
    sns.set_style("whitegrid")
    sns.set_context("talk", font_scale=1.2)

    plt.figure(figsize=(8, 5))
    # Use seaborn lineplot with error bars representing CI
    sns.lineplot(
        data=summary_df,
        x="age_bin",
        y="mean_shannon",
        hue="delivery_mode",
        err_style="band",
        ci=None,  # we will draw our own CI bands
        linewidth=2.5,
    )

    # Manually add shaded 95 % CI bands
    for mode in summary_df["delivery_mode"].unique():
        mode_data = summary_df[summary_df["delivery_mode"] == mode]
        plt.fill_between(
            mode_data["age_bin"],
            mode_data["ci_low"],
            mode_data["ci_high"],
            alpha=0.2,
        )

    plt.xlabel("Age (days)")
    plt.ylabel("Shannon diversity")
    plt.title("Shannon diversity trajectories by delivery mode")
    plt.legend(title="Delivery mode")
    plt.tight_layout()
    plt.savefig(output_path, dpi=dpi)
    plt.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calculate and plot longitudinal Shannon diversity trajectories."
    )
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Path to input CSV file with microbiome diversity data.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="results",
        help="Directory to write output files (will be created if missing).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # 1. Load & validate
    # ------------------------------------------------------------------
    try:
        df_raw = load_and_validate(Path(args.input))
    except Exception as e:
        sys.exit(f"Error loading data: {e}")

    # ------------------------------------------------------------------
    # 2. Bin age
    # ------------------------------------------------------------------
    df_binned = bin_age(df_raw, bin_width=30)

    # ------------------------------------------------------------------
    # 3. Summary statistics
    # ------------------------------------------------------------------
    summary = compute_summary(df_binned)
    summary_path = out_dir / "diversity_summary.csv"
    summary.to_csv(summary_path, index=False)
    print(f"Summary statistics saved to: {summary_path}")

    # ------------------------------------------------------------------
    # 4. Mixed‑effects model
    # ------------------------------------------------------------------
    try:
        model, fe_table = fit_mixed_model(df_binned)
    except Exception as e:
        sys.exit(f"Error fitting mixed model: {e}")

    fe_path = out_dir / "mixed_model_fixed_effects.csv"
    fe_table.to_csv(fe_path, index=False)
    print(f"Mixed‑model fixed effects saved to: {fe_path}")

    # Also save a textual summary for quick inspection
    model_summary_path = out_dir / "mixed_model_summary.txt"
    with open(model_summary_path, "w") as f:
        f.write(str(model.summary()))
    print(f"Full model summary saved to: {model_summary_path}")

    # ------------------------------------------------------------------
    # 5. Plot
    # ------------------------------------------------------------------
    fig_path = out_dir / "diversity_trajectories.png"
    plot_trajectories(summary, df_binned, fig_path)
    print(f"Figure saved to: {fig_path}")

    print("All steps completed successfully.")


if __name__ == "__main__":
    main()
```

---

### Requirements list (`requirements.txt` or `environment.yml`)

```
pandas>=2.0
numpy>=1.24
scipy>=1.10
matplotlib>=3.7
seaborn>=0.13
statsmodels>=0.14
```

*If you use `conda`, you can create the environment with:*

```bash
conda create -n microbiome_div python=3.10 pandas numpy scipy matplotlib seaborn statsmodels
conda activate microbiome_div
```

---

### Assumptions made

1. **Data structure** – Each row corresponds to a single stool sample; `subject_id` uniquely identifies an infant, and `age_days` is an integer count of days since birth.
2. **Age binning** – Bins are defined as left‑closed, right‑open intervals of 30 days (e.g., `[0,30)`, `[30,60)`, …). The last bin may be partially filled if the maximum age does not fall exactly on a bin edge.
3. **Missing data** – Rows missing any of the key variables (`subject_id`, `age_days`, `shannon`, `delivery_mode`) are dropped; a warning is printed.
4. **Delivery mode coding** – Treated as a categorical variable with levels `"cesarean"` (reference) and `"vaginal"`.
5. **Linear mixed model** – Random intercept for each subject (`(1|subject_id)`) captures within‑infant correlation; fixed effects include age, delivery mode, and their interaction. Residuals are assumed approximately normal and homoscedastic.
6. **Confidence intervals** – 95 % CI computed as `mean ± 1.96 * SEM` (SEM = SD / √n). This approximation is reasonable for moderate‑to‑large `n` per bin.
7. **Figure format** – Output figure is saved as a high‑resolution PNG (300 dpi) suitable for publication.

---

### Validation checks to run

1. **File existence** – After running the script, verify that the following files exist in the output directory:
   - `diversity_summary.csv`
   - `mixed_model_fixed_effects.csv`
   - `mixed_model_summary.txt`
   - `diversity_trajectories.png`
2. **Summary table shape** – The summary CSV should have one row per `(age_bin, delivery_mode)` combination.
```

## Overall Assessment
- **Recommendation:** Pass
- **Notes:**
## Verification Steps Tested
_Which verification requirements from the prompt were checked, and results._
