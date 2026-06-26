# Test Results: code/python-analysis.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-25.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** code/python-analysis.md
- **Model:** claude-sonnet-4.6
- **Model ID (pinned):** claude-sonnet-4-6
- **Endpoint:** native
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
Infant Gut Microbiome Diversity Trajectory Analysis
====================================================
Calculates and visualises Shannon diversity trajectories over the first year
of life, stratified by delivery mode (vaginal vs. cesarean).

Workflow
--------
1. Load and validate the input CSV.
2. Bin samples into calendar months (0-30 days, 31-60 days, …).
3. Compute per-bin summary statistics (mean, SD, 95 % CI).
4. Fit a linear mixed-effects model:
       shannon ~ age_days * delivery_mode + (1 + age_days | subject_id)
   using statsmodels MixedLM.
5. Export summary statistics (CSV), model results (CSV + plain-text),
   and a publication-quality figure (PNG + PDF).

Usage
-----
    python diversity_trajectories.py --input data.csv --outdir results/

Dependencies
------------
    pandas, numpy, scipy, matplotlib, seaborn, statsmodels
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
from statsmodels.formula.api import mixedlm
from statsmodels.tools.sm_exceptions import ConvergenceWarning

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

# Bin edges in days (0-30, 31-60, …, 331-365)
# ASSUMPTION: "first year" means days 0-365 inclusive.
BIN_EDGES: list[int] = list(range(0, 366, 30)) + [366]  # 13 bins
BIN_LABELS: list[str] = [f"{BIN_EDGES[i]+1 if i > 0 else 0}-{BIN_EDGES[i+1]}" for i in range(len(BIN_EDGES) - 1)]

# Colour palette – colour-blind-friendly (Wong 2011)
PALETTE: dict[str, str] = {
    "vaginal": "#0072B2",   # blue
    "cesarean": "#D55E00",  # vermillion
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# 1. Data loading & validation
# ---------------------------------------------------------------------------

def load_and_validate(filepath: str | Path) -> pd.DataFrame:
    """Load the microbiome CSV and validate its structure.

    Parameters
    ----------
    filepath:
        Path to the input CSV file.

    Returns
    -------
    pd.DataFrame
        Cleaned dataframe ready for downstream analysis.

    Raises
    ------
    FileNotFoundError
        If *filepath* does not exist.
    ValueError
        If required columns are missing or key columns contain unexpected values.
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Input file not found: {filepath}")
    if filepath.stat().st_size == 0:
        raise ValueError(f"Input file is empty: {filepath}")

    log.info("Loading data from %s", filepath)
    df = pd.read_csv(filepath)

    # ---- Column presence check ----
    missing_cols = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing_cols:
        raise ValueError(
            f"Missing required columns: {missing_cols}\n"
            f"Found columns: {list(df.columns)}"
        )

    # ---- Type coercion ----
    df["age_days"] = pd.to_numeric(df["age_days"], errors="coerce")
    df["shannon"] = pd.to_numeric(df["shannon"], errors="coerce")
    df["observed_features"] = pd.to_numeric(df["observed_features"], errors="coerce")

    # ---- Range checks ----
    n_before = len(df)
    df = df.dropna(subset=["age_days", "shannon"])
    n_dropped = n_before - len(df)
    if n_dropped > 0:
        log.warning("Dropped %d rows with NaN in age_days or shannon.", n_dropped)

    invalid_age = df[(df["age_days"] < 0) | (df["age_days"] > 365)]
    if not invalid_age.empty:
        log.warning(
            "%d samples have age_days outside [0, 365] and will be excluded.",
            len(invalid_age),
        )
        df = df[df["age_days"].between(0, 365)]

    if df["shannon"].lt(0).any():
        raise ValueError("Shannon diversity contains negative values – check input data.")

    # ---- Categorical checks ----
    # ASSUMPTION: delivery_mode is exactly 'vaginal' or 'cesarean' (case-insensitive).
    df["delivery_mode"] = df["delivery_mode"].str.strip().str.lower()
    unexpected_dm = set(df["delivery_mode"].unique()) - {"vaginal", "cesarean"}
    if unexpected_dm:
        raise ValueError(
            f"Unexpected delivery_mode values: {unexpected_dm}. "
            "Expected 'vaginal' or 'cesarean'."
        )

    df["feeding_mode"] = df["feeding_mode"].str.strip().str.lower()

    # ---- Duplicate sample check ----
    dupes = df.duplicated(subset=["sample_id"])
    if dupes.any():
        log.warning(
            "%d duplicate sample_ids detected; keeping first occurrence.",
            dupes.sum(),
        )
        df = df[~dupes]

    log.info(
        "Loaded %d samples from %d subjects (%d vaginal, %d cesarean).",
        len(df),
        df["subject_id"].nunique(),
        (df["delivery_mode"] == "vaginal").sum(),
        (df["delivery_mode"] == "cesarean").sum(),
    )
    return df.reset_index(drop=True)


# ---------------------------------------------------------------------------
# 2. Monthly binning & summary statistics
# ---------------------------------------------------------------------------

def assign_month_bins(df: pd.DataFrame) -> pd.DataFrame:
    """Add a *month_bin* column that groups samples into 30-day windows.

    Parameters
    ----------
    df:
        Validated dataframe containing *age_days*.

    Returns
    -------
    pd.DataFrame
        Input dataframe with two new columns:
        - ``month_bin``  : string label, e.g. ``"0-30"``
        - ``month_mid``  : midpoint of the bin in days (for plotting)
    """
    # pd.cut is vectorised – no Python loop needed.
    df = df.copy()
    df["month_bin"] = pd.cut(
        df["age_days"],
        bins=BIN_EDGES,
        labels=BIN_LABELS,
        right=True,
        include_lowest=True,  # ensures day 0 is captured in the first bin
    )
    # Map label → midpoint for continuous x-axis plotting
    midpoints = {
        label: (BIN_EDGES[i] + BIN_EDGES[i + 1]) / 2
        for i, label in enumerate(BIN_LABELS)
    }
    df["month_mid"] = df["month_bin"].map(midpoints)
    return df


def compute_summary_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Compute per-bin, per-delivery-mode summary statistics for Shannon diversity.

    Statistics computed
    -------------------
    n, mean, sd, se, ci95_lower, ci95_upper (95 % CI via t-distribution)

    Parameters
    ----------
    df:
        Dataframe with *month_bin*, *month_mid*, *delivery_mode*, *shannon*.

    Returns
    -------
    pd.DataFrame
        One row per (month_bin × delivery_mode) combination.
    """
    def _agg(x: pd.Series) -> pd.Series:
        n = x.count()
        mean = x.mean()
        sd = x.std(ddof=1)
        se = sd / np.sqrt(n) if n > 1 else np.nan
        # Two-sided 95 % CI using t-distribution (appropriate for small n per bin)
        t_crit = stats.t.ppf(0.975, df=n - 1) if n > 1 else np.nan
        return pd.Series(
            {
                "n": n,
                "mean": mean,
                "sd": sd,
                "se": se,
                "ci95_lower": mean - t_crit * se,
                "ci95_upper": mean + t_crit * se,
            }
        )

    # NOTE: groupby + apply can be slow for very large dataframes; here ~800 rows
    # is fine. For >100 k rows consider using agg with named aggregations instead.
    summary = (
        df.groupby(["month_bin", "month_mid", "delivery_mode"], observed=True)["shannon"]
        .apply(_agg)
        .reset_index()
    )
    # Ensure month_mid is numeric (it may become object after groupby)
    summary["month_mid"] = pd.to_numeric(summary["month_mid"])
    summary = summary.sort_values(["delivery_mode", "month_mid"]).reset_index(drop=True)
    return summary


# ---------------------------------------------------------------------------
# 3. Linear mixed-effects model
# ---------------------------------------------------------------------------

def fit_mixed_model(df: pd.DataFrame) -> tuple[object, pd.DataFrame]:
    """Fit a linear mixed-effects model for Shannon ~ age × delivery_mode.

    Model specification
    -------------------
    Fixed effects : age_days + delivery_mode + age_days:delivery_mode
    Random effects: random intercept + random slope for age_days per subject

    ASSUMPTION: The random-slope model may fail to converge with small cohorts.
    If convergence fails, the function falls back to a random-intercept-only model
    and logs a warning.

    Parameters
    ----------
    df:
        Dataframe with columns *shannon*, *age_days*, *delivery_mode*, *subject_id*.

    Returns
    -------
    result : statsmodels MixedLMResults
        Fitted model object.
    coef_df : pd.DataFrame
        Tidy coefficient table with columns:
        coef, se, z, p_value, ci_lower, ci_upper.
    """
    # Encode delivery_mode as a dummy (vaginal = 0, cesarean = 1)
    # ASSUMPTION: 'vaginal' is the reference category.
    df = df.copy()
    df["delivery_mode_bin"] = (df["delivery_mode"] == "cesarean").astype(int)

    # Centre age_days to reduce multicollinearity with the interaction term.
    age_mean = df["age_days"].mean()
    df["age_c"] = df["age_days"] - age_mean
    log.info("Age centred at %.1f days for model fitting.", age_mean)

    formula = "shannon ~ age_c * delivery_mode_bin"

    # ---- Attempt random intercept + slope ----
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", ConvergenceWarning)
            model = mixedlm(
                formula,
                data=df,
                groups=df["subject_id"],
                re_formula="~age_c",   # random slope for age
            )
            result = model.fit(method="lbfgs", maxiter=500)
        log.info("Random intercept + slope model converged successfully.")
    except (ConvergenceWarning, np.linalg.LinAlgError) as exc:
        log.warning(
            "Random slope model did not converge (%s). "
            "Falling back to random-intercept-only model.",
            exc,
        )
        model = mixedlm(formula, data=df, groups=df["subject_id"])
        result = model.fit(method="lbfgs", maxiter=500)

    # ---- Build tidy coefficient table ----
    coef_df = pd.DataFrame(
        {
            "coef": result.fe_params,
            "se": result.bse_fe,
            "z": result.tvalues,
            "p_value": result.pvalues,
            "ci_lower": result.conf_int().iloc[:, 0],
            "ci_upper": result.conf_int().iloc[:, 1],
        }
    )
    coef_df.index.name = "term"
    coef_df = coef_df.reset_index()

    # Human-readable term names
    term_map = {
        "Intercept": "Intercept (vaginal, mean age)",
        "age_c": "Age (days, centred)",
        "delivery_mode_bin": "Cesarean vs. vaginal",
        "age_c:delivery_mode_bin": "Age × Cesarean interaction",
    }
    coef_df["term"] = coef_df["term"].map(term_map).fillna(coef_df["term"])

    log.info("Model AIC: %.2f | BIC: %.2f", result.aic, result.bic)
    return result, coef_df


# ---------------------------------------------------------------------------
# 4. Visualisation
# ---------------------------------------------------------------------------

def plot_diversity_trajectories(
    summary: pd.DataFrame,
    coef_df: pd.DataFrame,
    outdir: Path,
) -> None:
    """Create a publication-quality figure of Shannon diversity trajectories.

    The figure shows mean ± 95 % CI for each delivery mode across monthly bins,
    with individual data points overlaid as a strip plot.

    Parameters
    ----------
    summary:
        Output of :func:`compute_summary_stats`.
    coef_df:
        Tidy coefficient table from :func:`fit_mixed_model`.
    outdir:
        Directory where the figure files will be saved.
    """
    # ---- Style ----
    sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.dpi": 150,
        }
    )

    fig, ax = plt.subplots(figsize=(9, 5))

    delivery_modes = ["vaginal", "cesarean"]

    for dm in delivery_modes:
        sub = summary[summary["delivery_mode"] == dm].sort_values("month_mid")
        color = PALETTE[dm]
        label = dm.capitalize()

        # ---- Shaded 95 % CI ribbon ----
        ax.fill_between(
            sub["month_mid"],
            sub["ci95_lower"],
            sub["ci95_upper"],
            alpha=0.20,
            color=color,
            linewidth=0,
            label="_nolegend_",
        )

        # ---- Mean line ----
        ax.plot(
            sub["month_mid"],
            sub["mean"],
            color=color,
            linewidth=2.2,
            marker="o",
            markersize=5,
            label=label,
            zorder=3,
        )

        # ---- Error bars (explicit, for clarity at each bin) ----
        ax.errorbar(
            sub["month_mid"],
            sub["mean"],
            yerr=[
                sub["mean"] - sub["ci95_lower"],
                sub["ci95_upper"] - sub["mean"],
            ],
            fmt="none",
            color=color,
            capsize=3,
            linewidth=1.2,
            zorder=2,
        )

    # ---- Axis labels & formatting ----
    ax.set_xlabel("Age (days)", fontsize=
````

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
