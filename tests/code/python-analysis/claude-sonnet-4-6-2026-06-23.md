# Test Results: code/python-analysis.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-23.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** code/python-analysis.md
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
```python
"""
Longitudinal Infant Gut Microbiome Diversity Analysis
======================================================
Calculates and plots Shannon diversity trajectories across the first year of life,
stratified by delivery mode (vaginal vs. cesarean). Includes monthly binned summary
statistics, a linear mixed-effects model comparing trajectories, and a
publication-quality figure with 95% confidence intervals.

Usage:
    python microbiome_diversity_analysis.py --input data.csv --output_dir results/

Author: [Your Name]
Date: [Date]
"""

# ---------------------------------------------------------------------------
# Standard library
# ---------------------------------------------------------------------------
import argparse
import logging
import sys
import warnings
from pathlib import Path

# ---------------------------------------------------------------------------
# Third-party
# ---------------------------------------------------------------------------
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

# statsmodels is a conda-forge / PyPI package; imported with a clear error
# message if missing so the user knows exactly what to install.
try:
    import statsmodels.formula.api as smf
    from statsmodels.tools.sm_exceptions import ConvergenceWarning
except ImportError as exc:
    sys.exit(
        "statsmodels is required for the mixed-effects model.\n"
        "Install it with:  conda install -c conda-forge statsmodels\n"
        f"Original error: {exc}"
    )

# ---------------------------------------------------------------------------
# Module-level constants
# ---------------------------------------------------------------------------
REQUIRED_COLUMNS: list[str] = [
    "sample_id",
    "subject_id",
    "age_days",
    "shannon",
    "observed_features",
    "delivery_mode",
    "feeding_mode",
]

# Bin edges in days (0–365, one bin per ~30-day month)
# ASSUMPTION: "first year" means days 0–365 inclusive.
BIN_EDGES: list[int] = list(range(0, 396, 30))  # 0, 30, 60, …, 390
BIN_LABELS: list[int] = list(range(1, len(BIN_EDGES)))  # 1-indexed month bins

DELIVERY_PALETTE: dict[str, str] = {
    "vaginal": "#2196F3",    # blue
    "cesarean": "#F44336",   # red
}

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


# ===========================================================================
# 1. Data loading and validation
# ===========================================================================

def load_and_validate(filepath: str | Path) -> pd.DataFrame:
    """
    Load the microbiome CSV and validate its structure.

    Parameters
    ----------
    filepath : str or Path
        Path to the input CSV file.

    Returns
    -------
    pd.DataFrame
        Cleaned and type-coerced DataFrame ready for analysis.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If required columns are missing or data types are unexpected.
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Input file not found: {filepath}")
    if filepath.suffix.lower() != ".csv":
        raise ValueError(f"Expected a .csv file, got: {filepath.suffix}")

    log.info("Loading data from %s", filepath)
    df = pd.read_csv(filepath)

    # ---- Column presence check ----
    missing_cols = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing_cols:
        raise ValueError(
            f"Input CSV is missing required columns: {sorted(missing_cols)}\n"
            f"Found columns: {sorted(df.columns.tolist())}"
        )

    # ---- Type coercion ----
    df["age_days"] = pd.to_numeric(df["age_days"], errors="coerce")
    df["shannon"] = pd.to_numeric(df["shannon"], errors="coerce")
    df["observed_features"] = pd.to_numeric(df["observed_features"], errors="coerce")

    # ---- Range checks ----
    n_before = len(df)
    df = df.dropna(subset=["age_days", "shannon", "subject_id"])
    n_dropped = n_before - len(df)
    if n_dropped > 0:
        log.warning(
            "Dropped %d rows with missing age_days, shannon, or subject_id.", n_dropped
        )

    negative_shannon = (df["shannon"] < 0).sum()
    if negative_shannon > 0:
        log.warning(
            "%d rows have negative Shannon diversity — check your data.", negative_shannon
        )

    out_of_range = (df["age_days"] < 0) | (df["age_days"] > 365)
    if out_of_range.sum() > 0:
        log.warning(
            "%d samples have age_days outside [0, 365] and will be excluded from "
            "monthly bins but retained for the mixed model.",
            out_of_range.sum(),
        )

    # ---- Categorical standardisation ----
    # ASSUMPTION: delivery_mode values are exactly "vaginal" or "cesarean"
    #             (case-insensitive). Unexpected values are flagged.
    df["delivery_mode"] = df["delivery_mode"].str.strip().str.lower()
    unexpected_delivery = df.loc[
        ~df["delivery_mode"].isin(["vaginal", "cesarean"]), "delivery_mode"
    ].unique()
    if len(unexpected_delivery) > 0:
        raise ValueError(
            f"Unexpected delivery_mode values: {unexpected_delivery}. "
            "Expected 'vaginal' or 'cesarean'."
        )

    df["feeding_mode"] = df["feeding_mode"].str.strip().str.lower()

    log.info(
        "Loaded %d samples from %d subjects.",
        len(df),
        df["subject_id"].nunique(),
    )
    return df


# ===========================================================================
# 2. Monthly binning and summary statistics
# ===========================================================================

def assign_month_bins(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a 'month_bin' column representing 30-day intervals (1 = days 0–30, etc.).

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with an 'age_days' column.

    Returns
    -------
    pd.DataFrame
        Copy of df with 'month_bin' (integer) and 'month_label' (string) columns.
    """
    df = df.copy()
    df["month_bin"] = pd.cut(
        df["age_days"],
        bins=BIN_EDGES,
        labels=BIN_LABELS,
        right=True,          # (0,30], (30,60], …
        include_lowest=True, # include day 0
    ).astype("Int64")        # nullable integer to preserve NaN for out-of-range

    # Human-readable label: "Month 1 (0–30d)", etc.
    bin_starts = BIN_EDGES[:-1]
    bin_ends = BIN_EDGES[1:]
    label_map = {
        i + 1: f"Month {i + 1}\n({bin_starts[i]}–{bin_ends[i]}d)"
        for i in range(len(BIN_LABELS))
    }
    df["month_label"] = df["month_bin"].map(label_map)
    return df


def compute_summary_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute mean Shannon diversity ± 95 % CI per month bin × delivery mode.

    The 95 % CI is calculated as:  mean ± t_{α/2, n-1} × (SD / √n)

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with columns: month_bin, delivery_mode, shannon.

    Returns
    -------
    pd.DataFrame
        Summary table with columns:
        month_bin, delivery_mode, n, mean, sd, se, ci95_lower, ci95_upper,
        median, q25, q75.
    """
    # NOTE: This groupby + agg is O(n) and fast even for large datasets.
    grouped = df.dropna(subset=["month_bin"]).groupby(
        ["month_bin", "delivery_mode"], observed=True
    )["shannon"]

    summary = grouped.agg(
        n="count",
        mean="mean",
        sd="std",
        median="median",
        q25=lambda x: x.quantile(0.25),
        q75=lambda x: x.quantile(0.75),
    ).reset_index()

    summary["se"] = summary["sd"] / np.sqrt(summary["n"])

    # t-based 95 % CI (more appropriate than z for small per-bin sample sizes)
    t_crit = summary["n"].apply(
        lambda n: stats.t.ppf(0.975, df=max(n - 1, 1))
    )
    summary["ci95_lower"] = summary["mean"] - t_crit * summary["se"]
    summary["ci95_upper"] = summary["mean"] + t_crit * summary["se"]

    # Midpoint of each bin in days (for plotting on a continuous axis)
    bin_midpoints = {
        label: (BIN_EDGES[label - 1] + BIN_EDGES[label]) / 2
        for label in BIN_LABELS
    }
    summary["age_days_mid"] = summary["month_bin"].map(bin_midpoints)

    return summary.sort_values(["delivery_mode", "month_bin"]).reset_index(drop=True)


# ===========================================================================
# 3. Linear mixed-effects model
# ===========================================================================

def run_mixed_model(df: pd.DataFrame) -> dict:
    """
    Fit a linear mixed-effects model to compare Shannon diversity trajectories
    between delivery modes.

    Model specification
    -------------------
    Fixed effects:
        age_days            — linear time trend (continuous)
        delivery_mode       — group difference at baseline
        age_days:delivery_mode — interaction (different slopes per group)

    Random effects:
        Random intercept + random slope for age_days per subject_id.
        This accounts for repeated measures within infants.

    ASSUMPTION: The relationship between age_days and Shannon diversity is
    approximately linear within the first year. If non-linear, consider adding
    a quadratic term (np.power(age_days, 2)).

    Parameters
    ----------
    df : pd.DataFrame
        Full (unbinned) DataFrame with columns:
        shannon, age_days, delivery_mode, subject_id.

    Returns
    -------
    dict with keys:
        'model'   : fitted MixedLM result object
        'summary' : statsmodels Summary object
        'aic'     : float
        'bic'     : float
        'fixed_effects_table' : pd.DataFrame of fixed-effect estimates
    """
    log.info("Fitting linear mixed-effects model …")

    # Encode delivery_mode as 0/1 for interpretability
    # ASSUMPTION: "vaginal" is the reference category.
    df = df.copy()
    df["delivery_cesarean"] = (df["delivery_mode"] == "cesarean").astype(int)

    formula = "shannon ~ age_days * delivery_cesarean"

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", ConvergenceWarning)
        try:
            model = smf.mixedlm(
                formula=formula,
                data=df,
                groups=df["subject_id"],
                # Random slope for time — NOTE: may be slow on large datasets;
                # remove 're_formula' to fit random-intercept-only model if needed.
                re_formula="~age_days",
            )
            result = model.fit(method="lbfgs", maxiter=1000)
        except Exception as exc:
            log.warning(
                "Random-slope model failed (%s). Falling back to random-intercept model.",
                exc,
            )
            model = smf.mixedlm(formula=formula, data=df, groups=df["subject_id"])
            result = model.fit(method="lbfgs", maxiter=1000)

    if not result.converged:
        log.warning(
            "Mixed model did not fully converge. Interpret results with caution."
        )

    # Build a tidy fixed-effects table
    fe_table = pd.DataFrame(
        {
            "estimate": result.fe_params,
            "std_err": result.bse_fe,
            "z_stat": result.tvalues,
            "p_value": result.pvalues,
            "ci_lower": result.conf_int().iloc[:, 0],
            "ci_upper": result.conf_int().iloc[:, 1],
        }
    ).rename_axis("term").reset_index()

    log.info("Model AIC: %.2f  BIC: %.2f", result.aic, result.bic)

    return {
        "model": result,
        "summary": result.summary(),
        "aic": result.aic,
        "bic": result.bic,
        "fixed_effects_table": fe_table,
    }


# ===========================================================================
# 4. Publication-quality figure
# ===========================================================================

def plot_diversity_trajectories(
    summary: pd.DataFrame,
    model_results: dict,
    output_path: str | Path,
) -> plt.Figure:
    """
    Create a publication-quality figure of Shannon diversity over time,
    stratified by delivery mode, with 95 % CI ribbons and individual
    trajectory context.

    Parameters
    ----------
    summary : pd.DataFrame
        Output of compute_summary_statistics().
    model_results : dict
        Output of run_mixed_model().
    output_path : str or Path
        File path for the saved figure (extension determines format).

    Returns
    -------
    matplotlib.figure.Figure
    """
    sns.set_theme(style="whitegrid", context="paper", font_scale=1.3)
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )

    fig, ax = plt.subplots(figsize=(9, 5.5))

    for mode, grp in summary.groupby("delivery_mode"):
        color = DELIVERY_PALETTE.get(mode, "gray")
        label = mode.capitalize()

        # Mean line
        ax.plot(
            grp["age_days_mid"],
            grp["mean"],
            color=color,
            linewidth=2.2,
            marker="o",
            markersize=5,
            label=label,
            zorder=3,
        )

        # 95 % CI ribbon
        ax.fill_between(
            grp["age_days_mid"],
            grp["ci95_lower"],
            grp["ci95_upper"],
            color=color,
            alpha=0.18,
            zorder=2,
        )

        # Error bars (optional visual redundancy for clarity in print)
        ax.errorbar(
            grp["age_days_mid"],
            grp["mean"],
            yerr=[
                grp["mean"] - grp["ci95_lower"],
                grp["ci95_upper"] - grp["mean"],
            ],
            fmt="none",
            color=color,
            capsize=3,
            linewidth=1,
            alpha=0.6,
            zorder=2,
        )

    # ---- Axis formatting ----
    ax.set_xlabel("Age (days)", fontsize=13)
    ax.set_ylabel("Shannon Diversity Index", fontsize=13)
    ax.set_title(
        "Gut Microbiome Alpha-Diversity Trajectories\nby Delivery Mode (Mean ± 95% CI)",
        fontsize=14,
        pad=12,
    )

    # Tick at each bin midpoint, labelled in months
    midpoints = sorted(summary
```

## Assessment

_Machine-suggested (UNCONFIRMED) — drafted by Claude Opus 4.7 on 2026-06-24 to speed T4 review. An author must independently read the Model Output above and set the real Recommendation. Anything labeled here is triage, not domain expert review._

**Machine triage:** Long, well-structured script (450 lines): docstring, type hints, REQUIRED_COLUMNS constant, conda-forge ImportError messaging, t-based 95% CI (more appropriate than 1.96*SEM at small n), random-intercept + random-slope LMM with fallback to intercept-only on convergence failure, seaborn publication theme. Code is **truncated** mid-tick-formatting (`midpoints = sorted(summary` — no closing). Structure looks excellent before truncation. The math (t-based CI, mixed-model formula `shannon ~ age_days * delivery_cesarean` with random intercept+slope by subject) appears sound.

**Suggested verdict (UNCONFIRMED):** Needs revision

**What still needs human verification:**
- Truncation: regenerate with higher token cap. The script is incomplete past the figure formatting.
- Whether the t-based CI (`stats.t.ppf(0.975, df=max(n-1,1))`) per bin matches the user's reporting convention (vs the simpler 1.96*SEM the other models used).
- Random slope on age_days is more flexible than random intercept only; confirm this is the intended model. Sonnet adds a graceful fallback to intercept-only if convergence fails — confirm this fallback policy is acceptable.
- Whether actually running the script on the user's data produces sensible output (the harness can't check that).

## Overall Assessment
- **Recommendation:** PENDING AUTHOR REVIEW
- **Notes:**

## Verification Steps Tested
_Which verification requirements from the prompt were checked, and results._
