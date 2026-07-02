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
   to test whether delivery mode modifies the diversity trajectory.
5. Export a summary statistics table, model results, and a
   publication-quality figure.

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

# Columns that must be present in the input file
REQUIRED_COLUMNS: list[str] = [
    "sample_id",
    "subject_id",
    "age_days",
    "shannon",
    "observed_features",
    "delivery_mode",
    "feeding_mode",
]

# Allowed category labels (case-insensitive comparison performed at load time)
VALID_DELIVERY_MODES: set[str] = {"vaginal", "cesarean"}
VALID_FEEDING_MODES: set[str] = {"breastfed", "formula"}

# Month bin edges (days).  Covers 0–365 days in 30-day windows.
# ASSUMPTION: "month" is approximated as 30-day intervals; the final bin
#             captures any samples beyond day 330 up to day 365.
BIN_EDGES: list[int] = list(range(0, 361, 30)) + [366]  # 13 bins
BIN_LABELS: list[str] = [f"{e}-{BIN_EDGES[i+1]-1}" for i, e in enumerate(BIN_EDGES[:-1])]

# Colour palette for delivery modes (colour-blind friendly)
PALETTE: dict[str, str] = {"vaginal": "#2196F3", "cesarean": "#FF5722"}

# Figure aesthetics
FIGURE_DPI: int = 300
FIGURE_SIZE: tuple[float, float] = (8.0, 5.0)

# ---------------------------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


# ===========================================================================
# Data loading and validation
# ===========================================================================

def load_and_validate(filepath: str | Path) -> pd.DataFrame:
    """Load the microbiome CSV and perform structural / semantic validation.

    Parameters
    ----------
    filepath:
        Path to the input CSV file.

    Returns
    -------
    pd.DataFrame
        Cleaned and type-coerced DataFrame ready for downstream analysis.

    Raises
    ------
    FileNotFoundError
        If *filepath* does not exist.
    ValueError
        If required columns are missing, categorical values are unexpected,
        or numeric columns contain only NaN.
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Input file not found: {filepath}")

    log.info("Loading data from %s", filepath)
    df = pd.read_csv(filepath)

    # ---- Column presence check -------------------------------------------
    missing_cols = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing_cols:
        raise ValueError(
            f"Input CSV is missing required columns: {sorted(missing_cols)}\n"
            f"Found columns: {sorted(df.columns.tolist())}"
        )

    # ---- Type coercion ------------------------------------------------------
    df["age_days"] = pd.to_numeric(df["age_days"], errors="coerce")
    df["shannon"] = pd.to_numeric(df["shannon"], errors="coerce")
    df["observed_features"] = pd.to_numeric(df["observed_features"], errors="coerce")

    # Normalise categorical columns to lowercase for consistent comparisons
    df["delivery_mode"] = df["delivery_mode"].str.strip().str.lower()
    df["feeding_mode"] = df["feeding_mode"].str.strip().str.lower()

    # ---- Semantic validation ------------------------------------------------
    _check_numeric_column(df, "age_days", min_val=0, max_val=400)
    _check_numeric_column(df, "shannon", min_val=0.0)
    _check_categorical_column(df, "delivery_mode", VALID_DELIVERY_MODES)
    _check_categorical_column(df, "feeding_mode", VALID_FEEDING_MODES)

    # ---- Drop rows with missing key values and report -----------------------
    n_before = len(df)
    df = df.dropna(subset=["age_days", "shannon", "subject_id", "delivery_mode"])
    n_dropped = n_before - len(df)
    if n_dropped > 0:
        log.warning(
            "Dropped %d row(s) with missing values in key columns.", n_dropped
        )

    # ---- Duplicate sample check ---------------------------------------------
    dupes = df.duplicated(subset=["sample_id"])
    if dupes.any():
        log.warning(
            "Found %d duplicate sample_id(s); keeping first occurrence.",
            dupes.sum(),
        )
        df = df[~dupes].copy()

    log.info(
        "Loaded %d samples from %d subjects.",
        len(df),
        df["subject_id"].nunique(),
    )
    return df.reset_index(drop=True)


def _check_numeric_column(
    df: pd.DataFrame,
    col: str,
    min_val: float | None = None,
    max_val: float | None = None,
) -> None:
    """Raise ValueError if a numeric column is all-NaN or out of range."""
    if df[col].isna().all():
        raise ValueError(f"Column '{col}' contains only NaN after coercion.")
    n_nan = df[col].isna().sum()
    if n_nan > 0:
        log.warning("Column '%s' has %d NaN value(s).", col, n_nan)
    if min_val is not None and (df[col].dropna() < min_val).any():
        log.warning("Column '%s' contains values below expected minimum %s.", col, min_val)
    if max_val is not None and (df[col].dropna() > max_val).any():
        log.warning("Column '%s' contains values above expected maximum %s.", col, max_val)


def _check_categorical_column(
    df: pd.DataFrame, col: str, valid_values: set[str]
) -> None:
    """Raise ValueError if unexpected category labels are found."""
    observed = set(df[col].dropna().unique())
    unexpected = observed - valid_values
    if unexpected:
        raise ValueError(
            f"Column '{col}' contains unexpected values: {unexpected}. "
            f"Expected one of: {valid_values}"
        )


# ===========================================================================
# Binning and summary statistics
# ===========================================================================

def bin_by_month(df: pd.DataFrame) -> pd.DataFrame:
    """Assign each sample to a 30-day age bin.

    Parameters
    ----------
    df:
        Validated DataFrame with an ``age_days`` column.

    Returns
    -------
    pd.DataFrame
        Original DataFrame with two new columns:

        * ``age_bin``       – interval label string (e.g. ``"0-29"``)
        * ``age_bin_mid``   – midpoint of the bin in days (used for plotting)
    """
    # pd.cut assigns each value to the half-open interval (left, right]
    # ASSUMPTION: right=True means day 0 falls in the first bin via
    #             include_lowest=True.
    df = df.copy()
    df["age_bin"] = pd.cut(
        df["age_days"],
        bins=BIN_EDGES,
        labels=BIN_LABELS,
        right=True,
        include_lowest=True,
    )
    # Compute bin midpoints for x-axis positioning
    bin_mids = {
        label: (BIN_EDGES[i] + BIN_EDGES[i + 1]) / 2
        for i, label in enumerate(BIN_LABELS)
    }
    df["age_bin_mid"] = df["age_bin"].map(bin_mids)
    return df


def compute_summary_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Compute per-bin, per-delivery-mode summary statistics for Shannon diversity.

    Statistics computed
    -------------------
    * n          – sample count
    * mean       – arithmetic mean
    * sd         – standard deviation
    * sem        – standard error of the mean
    * ci95_lower – lower bound of the 95 % CI (t-distribution)
    * ci95_upper – upper bound of the 95 % CI (t-distribution)
    * median     – median

    Parameters
    ----------
    df:
        DataFrame with columns ``age_bin``, ``age_bin_mid``,
        ``delivery_mode``, and ``shannon``.

    Returns
    -------
    pd.DataFrame
        One row per (age_bin, delivery_mode) combination.
    """
    # NOTE: groupby on Categorical preserves bin order automatically.
    grouped = df.groupby(["age_bin", "age_bin_mid", "delivery_mode"], observed=True)

    summary = grouped["shannon"].agg(
        n="count",
        mean="mean",
        sd="std",
        median="median",
    ).reset_index()

    summary["sem"] = summary["sd"] / np.sqrt(summary["n"])

    # 95 % CI using the t-distribution (appropriate for small per-bin n)
    # scipy.stats.t.ppf returns the quantile for the given probability.
    t_crit = stats.t.ppf(0.975, df=summary["n"] - 1)
    summary["ci95_lower"] = summary["mean"] - t_crit * summary["sem"]
    summary["ci95_upper"] = summary["mean"] + t_crit * summary["sem"]

    # Clip lower CI at 0 (Shannon diversity cannot be negative)
    summary["ci95_lower"] = summary["ci95_lower"].clip(lower=0.0)

    # Sort by bin midpoint for clean plotting
    summary = summary.sort_values(["delivery_mode", "age_bin_mid"]).reset_index(drop=True)

    log.info("Summary statistics computed for %d group-bin combinations.", len(summary))
    return summary


# ===========================================================================
# Linear mixed-effects model
# ===========================================================================

def fit_mixed_model(df: pd.DataFrame) -> tuple[object, pd.DataFrame]:
    """Fit a linear mixed-effects model to test the delivery-mode × age interaction.

    Model specification
    -------------------
    Fixed effects  : shannon ~ age_days * delivery_mode
    Random effects : random intercept + random slope for age_days per subject

        shannon_ij = (β0 + b0_j)
                   + (β1 + b1_j) * age_days_ij
                   + β2 * delivery_mode_j
                   + β3 * age_days_ij * delivery_mode_j
                   + ε_ij

    where j indexes subjects and i indexes observations within subjects.

    ASSUMPTION: delivery_mode is constant within a subject (assigned at birth).
    ASSUMPTION: residuals are approximately normally distributed.
    NOTE: Fitting a random slope model on ~800 observations can take 10–30 s.

    Parameters
    ----------
    df:
        Validated DataFrame with columns ``shannon``, ``age_days``,
        ``delivery_mode``, and ``subject_id``.

    Returns
    -------
    result : statsmodels MixedLMResults
        Fitted model object.
    coef_table : pd.DataFrame
        Coefficient table with estimates, SE, z-scores, and p-values.
    """
    # Encode delivery_mode as a dummy variable (vaginal = reference)
    # ASSUMPTION: "vaginal" is the reference category.
    df_model = df.copy()
    df_model["delivery_mode_cesarean"] = (
        df_model["delivery_mode"] == "cesarean"
    ).astype(int)

    # Centre age_days to reduce multicollinearity with the interaction term
    age_mean = df_model["age_days"].mean()
    df_model["age_days_c"] = df_model["age_days"] - age_mean
    log.info("Age centred at %.1f days for model fitting.", age_mean)

    formula = "shannon ~ age_days_c * delivery_mode_cesarean"

    log.info("Fitting linear mixed model: %s", formula)
    log.info("Random effects: random intercept + slope per subject (may take ~30 s).")

    # Suppress convergence warnings temporarily; we check manually below.
    with warnings.catch_warnings(record=True) as caught_warnings:
        warnings.simplefilter("always")
        try:
            model = mixedlm(
                formula,
                data=df_model,
                groups=df_model["subject_id"],
                # Random intercept + random slope for centred age
                re_formula="~age_days_c",
            )
            result = model.fit(method="lbfgs", maxiter=500)
        except Exception as exc:
            # Fall back to random-intercept-only model if random slope fails
            log.warning(
                "Random slope model failed (%s). "
                "Falling back to random-intercept-only model.",
                exc,
            )
            model = mixedlm(
                formula,
                data=df_model,
                groups=df_model["subject_id"],
            )
            result = model.fit(method="lbfgs", maxiter=500)

    # Report any convergence warnings
    convergence_issues = [
        w for w in caught_warnings if issubclass(w.category, ConvergenceWarning)
    ]
    if convergence_issues:
        log.warning(
            "Model convergence warning(s) detected. "
            "Interpret results with caution. Consider scaling predictors or "
            "simplifying the random-effects structure."
        )

    # Build a tidy coefficient table
    coef_table = pd.DataFrame(
        {
            "term": result.params.index,
            "estimate": result.params.values,
            "std_err": result.bse.values,
            "z_value": result.tvalues.values,
            "p_value": result.pvalues.values,
        }
    )
    coef_table["sig"] = coef_table["p_value"].apply(_significance_stars)

    log.info("Model fitting complete. AIC = %.2f", result.aic)
    return result, coef_table


def _significance_stars(p: float) -> str:
    """Return conventional significance stars for a p-value."""
    if p < 0.001:
        return "***"
    if p < 0.01:
        return "**"
    if p < 0.05:
        return "*"
    return "ns"


def format_model_summary(result: object, coef_table: pd.DataFrame) -> str:
    """Produce a human-readable text summary of the mixed model.

    Parameters
    ----------
    result:
        Fitted statsmodels MixedLMResults object.
    coef_table:
        Tidy coefficient table from :func:`fit_mixed_model`.

    Returns
    -------
    str
        Multi-line summary string suitable for writing to a text file.
    """
    lines = [
        "=" * 70,
        "Linear Mixed-Effects Model Results",
        "=" * 70,
        f"Formula : shannon ~ age_days_c * delivery_mode_cesarean",
        f"Random  : random intercept + slope per subject",
        f"N obs   : {int(result.nobs)}",
        f"N groups: {int(result.ngroups)}",
        f"AIC     : {result.aic:.2f}",
        f"BIC     : {result.bic:.2f}",
        f"Log-lik : {result.llf:.2f}",
        "",
        "Fixed Effects",
        "-" * 70,
        coef_table.to_string(index=False, float_format="{:.4f}".format),
        "",
        "Significance codes: *** p<0.001  ** p<0.01  * p<0.05  ns p≥0.05",
        "=" * 70,
    ]
    return "\n".join(lines)


# ===========================================================================
# Visualisation
# ===========================================================================

def plot_diversity_trajectories(
    summary: pd.DataFrame,
    raw_df: pd.DataFrame,
    outpath: str | Path,
) -> plt.Figure:
    """Create a publication-quality figure of Shannon diversity over time.

    The figure contains two panels:

    * **Top panel** – mean ± 95 % CI ribbon + mean line per delivery mode,
      with individual subject trajectories shown as faint lines.
    * **Bottom panel** – sample size (n) per bin per delivery mode as a
      grouped bar chart (data-density indicator).

    Parameters
    ----------
    summary:
        Per-bin summary statistics from :func:`compute_summary_stats`.
    raw_df:
        Full validated DataFrame (used for individual-level trajectories).
    outpath:
        File path for the saved figure (extension determines format).

    Returns
    -------
    matplotlib.figure.Figure
        The constructed figure object.
    """
    sns.set_theme(style="whitegrid", font_scale=1.1)
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )

    fig, axes = plt.subplots(
        2, 1,
        figsize=FIGURE_SIZE,
        gridspec_kw={"height_ratios": [4, 1], "hspace": 0.08},
        sharex=True,
    )
    ax_main, ax_n = axes

    # ---- Individual subject trajectories (faint background lines) ----------
    # NOTE: Drawing ~100 lines is fast; for >500 subjects consider subsampling.
    for subject, grp in raw_df.groupby("subject_id"):
        grp_sorted = grp.sort_values("age_days")
        delivery = grp_sorted["delivery_mode"].iloc[0]
        ax_main.plot(
            grp_sorted["age_days"],
            grp_sorted["shannon"],
            color=PALETTE[delivery],
            alpha=0.06,
            linewidth=0.6,
            zorder=1,
        )

    # ---- Mean ± 95 % CI per delivery mode ----------------------------------
    for mode, grp in summary.groupby("delivery_mode"):
        color = PALETTE[mode]
        x = grp["age_bin_mid"].values
        y = grp["mean"].values
        lo = grp["ci95_lower"].values
        hi = grp["ci95_upper"].values

        # Shaded CI ribbon
        ax_main.fill_between(x, lo, hi, color=color, alpha=0.20, zorder=2)

        # Mean trajectory line
        ax_main.plot(
            x, y,
            color=color,
            linewidth=2.2,
            marker="o",
            markersize=5,
            label=mode.capitalize(),
            zorder=3,
        )

    ax_main.set_ylabel("Shannon Diversity Index", fontsize=12)
    ax_main.set_ylim(bottom=0)
    ax_main.legend(
        title="Delivery mode",
        title_fontsize=10,
        fontsize=10,
        frameon=False,
        loc="upper left",
    )
    ax_main.set_title(
        "Infant Gut Microbiome Diversity Trajectories\n"
        "by Delivery Mode (Mean ± 95 % CI)",
        fontsize=13,
        pad=10,
    )

    # ---- Sample-size bar chart (bottom panel) -------------------------------
    bar_width = 10  # days
    offsets = {"vaginal": -bar_width / 2, "cesarean": bar_width / 2}

    for mode, grp in summary.groupby("delivery_mode"):
        x = grp["age_bin_mid"].values + offsets[mode]
        ax_n.bar(
            x,
            grp["n"].values,
            width=bar_width * 0.9,
            color=PALETTE[mode],
            alpha=0.75,
            label=mode.capitalize(),
        )

    ax_n.set_ylabel("n", fontsize=10)
    ax_n.set_xlabel("Age (days)", fontsize=12)
    ax_n.yaxis.set_major_locator(mticker.MaxNLocator(integer=True, nbins=3))

    # Shared x-axis ticks at bin midpoints
    tick_positions = summary["age_bin_mid"].unique()
    tick_labels = [str(int(t)) for t in sorted(tick_positions)]
    ax_n.set_xticks(sorted(tick_positions))
    ax_n.set_xticklabels(tick_labels, rotation=45, ha="right", fontsize=9)

    fig.tight_layout()

    outpath = Path(outpath)
    outpath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(outpath, dpi=FIGURE_DPI, bbox_inches="tight")
    log.info("Figure saved to %s", outpath)
    return fig


# ===========================================================================
# Output helpers
# ===========================================================================

def save_summary_table(summary: pd.DataFrame, outpath: str | Path) -> None:
    """Write the summary statistics table to a CSV file.

    Parameters
    ----------
    summary:
        DataFrame from :func:`compute_summary_stats`.
    outpath:
        Destination CSV path.
    """
    outpath = Path(outpath)
    outpath.parent.mkdir(parents=True, exist_ok=True)
    # Round floats for readability
    float_cols = ["mean", "sd", "sem", "ci95_lower", "ci95_upper", "median"]
    out = summary.copy()
    out[float_cols] = out[float_cols].round(4)
    out.to_csv(outpath, index=False)
    log.info("Summary statistics saved to %s", outpath)


def save_model_results(
    coef_table: pd.DataFrame,
    model_text: str,
    outdir: str | Path,
) -> None:
    """Save model coefficient table (CSV) and full text summary.

    Parameters
    ----------
    coef_table:
        Tidy coefficient table from :func:`fit_mixed_model`.
    model_text:
        Formatted text summary from :func:`format_model_summary`.
    outdir:
        Directory in which to write ``model_coefficients.csv`` and
        ``model_summary.txt``.
    """
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    coef_path = outdir / "model_coefficients.csv"
    coef_table.round(6).to_csv(coef_path, index=False)
    log.info("Model coefficients saved to %s", coef_path)

    text_path = outdir / "model_summary.txt"
    text_path.write_text(model_text, encoding="utf-8")
    log.info("Model summary saved to %s", text_path)


# ===========================================================================
# CLI argument parsing
# ===========================================================================

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments.

    Parameters
    ----------
    argv:
        Argument list (defaults to ``sys.argv[1:]``).

    Returns
    -------
    argparse.Namespace
        Parsed arguments with attributes ``input``, ``outdir``,
        and ``no_model``.
    """
    parser = argparse.ArgumentParser(
        description="Infant gut microbiome diversity trajectory analysis.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--input",
        required=True,
        metavar="CSV",
        help="Path to the input CSV file.",
    )
    parser.add_argument(
        "--outdir",
        default="results",
        metavar="DIR",
        help="Directory for all output files.",
    )
    parser.add_argument(
        "--no-model",
        action="store_true",
        help="Skip the mixed-effects model (useful for quick QC runs).",
    )
    parser.add_argument(
        "--figure-format",
        default="pdf",
        choices=["pdf", "png", "svg", "tiff"],
        help="Output format for the figure.",
    )
    return parser.parse_args(argv)


# ===========================================================================
# Main entry point
# ===========================================================================

def main(argv: list[str] | None = None) -> int:
    """Orchestrate the full analysis pipeline.

    Parameters
    ----------
    argv:
        Optional argument list for programmatic invocation.

    Returns
    -------
    int
        Exit code (0 = success, 1 = error).
    """
    args = parse_args(argv)
    outdir = Path(args.outdir)

    # ------------------------------------------------------------------
    # Step 1 – Load and validate
    # ------------------------------------------------------------------
    try:
        df = load_and_validate(args.input)
    except (FileNotFoundError, ValueError) as exc:
        log.error("Data loading failed: %s", exc)
        return 1

    # ------------------------------------------------------------------
    # Step 2 – Bin by month and compute summary statistics
    # ------------------------------------------------------------------
    df = bin_by_month(df)
    summary = compute_summary_stats(df)

    save_summary_table(summary, outdir / "summary_statistics.csv")

    # Print a quick overview to stdout
    print("\n── Summary Statistics (first 10 rows) ──────────────────────────")
    print(summary.head(10).to_string(index=False))
    print()

    # ------------------------------------------------------------------
    # Step 3 – Linear mixed-effects model
    # ------------------------------------------------------------------
    if not args.no_model:
        try:
            result, coef_table = fit_mixed_model(df)
            model_text = format_model_summary(result, coef_table)
            save_model_results(coef_table, model_text, outdir)
            print(model_text)
        except Exception as exc:
            log.error("Model fitting failed: %s", exc)
            log.error("Continuing without model results.")
    else:
        log.info("Skipping mixed-effects model (--no-model flag set).")

    # ------------------------------------------------------------------
    # Step 4 – Figure
    # ------------------------------------------------------------------
    fig_path = outdir / f"diversity_trajectories.{args.figure_format}"
    try:
        plot_diversity_trajectories(summary, df, fig_path)
    except Exception as exc:
        log.error("Figure generation failed: %s", exc)
        return 1

    log.info("Analysis complete. All outputs written to '%s/'.", outdir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

---

## Requirements

### `requirements.txt`
```text
pandas>=2.0
numpy>=1.24
scipy>=1.10
matplotlib>=3.7
seaborn>=0.12
statsmodels>=0.14
```

### `environment.yml` (conda-forge)
```yaml
name: microbiome_diversity
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.10
  - pandas>=2.0
  - numpy>=1.24
  - scipy>=1.10
  - matplotlib>=3.7
  - seaborn>=0.12
  - statsmodels>=0.14
  - pip
```

---

## Assumptions

| # | Assumption | Where flagged |
|---|-----------|---------------|
| 1 | **Delivery mode is time-invariant** — each subject has exactly one delivery mode that does not change across visits | `fit_mixed_model` docstring |
| 2 | **"Month" ≈ 30 days** — bins are 0–29, 30–59, … rather than calendar months | `BIN_EDGES` constant |
| 3 | **"vaginal" is the reference category** for the dummy-coded delivery mode variable | `fit_mixed_model` |
| 4 | **Residuals are approximately normal** — required for valid LMM inference; not formally tested in the script | `fit_mixed_model` docstring |
| 5 | **Age range is 0–365 days** — samples outside this range trigger a warning but are not removed | `_check_numeric_column` |
| 6 | **sample_id is unique per row** — duplicates are dropped with a warning rather than raising an error | `load_and_validate` |
| 7 | **Individual trajectories are plottable** — for >500 subjects the background lines should be subsampled | `plot_diversity_trajectories` comment |

---

## Validation Checks to Run

### 1. Smoke test with synthetic data
```python
import pandas as pd, numpy as np

rng = np.random.default_rng(42)
n = 800
df = pd.DataFrame({
    "sample_id":        [f"S{i:04d}" for i in range(n)],
    "subject_id":       [f"P{i//8:03d}" for i in range(n)],
    "age_days":         rng.integers(0, 365, n),
    "shannon":          rng.uniform(0.5, 4.5, n),
    "observed_features":rng.integers(10, 300, n),
    "delivery_mode":    rng.choice(["vaginal","cesarean"], n),
    "feeding_mode":     rng.choice(["breastfed","formula"], n),
})
df.to_csv("test_data.csv", index=False)
# Then run: python diversity_trajectories.py --input test_data.csv --outdir test_results
```

### 2. Column validation
```bash
# Should raise ValueError listing missing columns
python -c "
from diversity_trajectories import load_and_validate
import pandas as pd
pd.DataFrame({'sample_id':[1],'subject_id':['A']}).to_csv('/tmp/bad.csv',index=False)
load_and_validate('/tmp/bad.csv')
"
```

### 3. Category validation
```bash
# Should raise ValueError for unexpected delivery_mode value
python -c "
from diversity_trajectories import load_and_validate
import pandas as pd
df = pd.read_csv('test_data.csv')
df.loc[0,'delivery_mode'] = 'unknown'
df.to_csv('/tmp/bad_cat.csv', index=False)
load_and_validate('/tmp/bad_cat.csv')
"
```

### 4. Output file checks
```bash
# After a successful run, verify all expected outputs exist
ls -lh results/summary_statistics.csv \
        results/model_coefficients.csv \
        results/model_summary.txt \
        results/diversity_trajectories.pdf
```

### 5. Model sanity checks
- Open `results/model_summary.txt` and confirm:
  - `N obs` matches the number of rows in your cleaned data
  - `N groups` matches the number of unique subjects
  - The `age_days_c` coefficient is positive (diversity increases with age in healthy infants)
  - The interaction term `age_days_c:delivery_mode_cesarean` p-value is interpretable (not NaN)
  - No `ConvergenceWarning` in the log output
````

## Assessment

_Machine-suggested (UNCONFIRMED) — drafted by Claude Opus 4.7 on 2026-06-26 (re-triage after max_tokens bump and re-capture). An author must independently read the Model Output above and set the real Recommendation. Anything labeled here is triage, not domain expert review._

**Machine triage:** Output is complete (script + requirements + assumptions + validation checks), ends cleanly, no truncation. Script follows requested structure (main(), if __name__ guard, type hints, module docstring, grouped imports), uses statsmodels MixedLM with random intercept + slope per subject for the longitudinal design, computes per-bin summary stats with t-based 95% CI, and produces a two-panel figure including a sample-size strip. Format spec from the prompt (script, then requirements, assumptions, validation checks) is honored. I cannot verify statistical correctness of the mixed-model specification for this design or that the binning/centering choices are appropriate for the user's research question.

**Suggested verdict (UNCONFIRMED):** Pass with notes

**What still needs human verification:**
- Statistical appropriateness of random intercept + random slope on age_days_c per subject for ~800 obs / 100 subjects
- Whether the 0–365 day binning (final bin 330–365) is acceptable, given the prompt asked for "0-30, 31-60, etc."
- Whether the t-distribution CI on per-bin means (rather than CI derived from the LMM) is what the user wants
- That the random-slope fallback path actually runs cleanly in statsmodels with this data
- That `seaborn` is a real (used) import — it is loaded but barely used in the figure beyond `set_theme`

**Local code check:** Syntax PASS across 2 block(s) · 5/11 imports available.

## Overall Assessment
- **Recommendation:** Pass
- **Notes:** Alex Alexiev (2026-06-29): **What still needs human verification:**
- Statistical appropriateness of random intercept + random slope on age_days_c per subject for ~800 obs / 100 subjects
- Whether the 0–365 day binning (final bin 330–365) is acceptable, given the prompt asked for "0-30, 31-60, etc."
- Whether the t-distribution CI on per-bin means (rather than CI derived from the LMM) is what the user wants
- That the random-slope fallback path actually runs cleanly in statsmodels with this data
- That `seaborn` is a real (used) import — it is loaded but barely used in the figure beyond `set_theme`

## Verification Steps Tested
_Which verification requirements from the prompt were checked, and results._
