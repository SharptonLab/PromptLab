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

## Example Input

```
Context: I am a bioinformatician working on metagenomics data. I need a Python script to process BLAST output and summarize taxonomic hits.

Data description:
- Input: BLAST tabular output (outfmt 6) with columns: qseqid, sseqid, pident, length, mismatch, gapopen, qstart, qend, sstart, send, evalue, bitscore
- Sample size: ~500,000 hits
- Key variables: qseqid (query sequence ID), sseqid (subject, contains taxonomy), pident (percent identity), evalue

Environment:
- Python version: 3.10+
- Key packages: pandas, numpy, matplotlib
- Environment: conda

Task: Write a Python script that:
1. Loads BLAST tabular output
2. Filters hits by identity (≥90%) and e-value (≤1e-10)
3. Extracts genus from sseqid (format: "genus_species_strain")
4. Counts hits per query per genus, keeping top genus per query
5. Summarizes total hits per genus across all queries
6. Outputs: filtered CSV, genus summary table, bar plot of top 20 genera

Requirements as specified above.
```

## Example Output

```python
#!/usr/bin/env python3
"""
BLAST Output Taxonomic Summarization

Processes BLAST tabular output (outfmt 6) to extract and summarize
taxonomic assignments at the genus level. Filters by identity and
e-value thresholds, assigns each query to its best-matching genus,
and produces summary statistics and visualizations.

Usage:
    python blast_taxonomy_summary.py input.blast output_prefix

Author: [Your name]
Date: [Date]
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Column names for BLAST outfmt 6
BLAST_COLUMNS = [
    'qseqid', 'sseqid', 'pident', 'length', 'mismatch', 'gapopen',
    'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore'
]


def load_blast_output(filepath: Path) -> pd.DataFrame:
    """
    Load BLAST tabular output file.

    Parameters
    ----------
    filepath : Path
        Path to BLAST output file (outfmt 6)

    Returns
    -------
    pd.DataFrame
        DataFrame with BLAST hits

    Raises
    ------
    FileNotFoundError
        If input file doesn't exist
    ValueError
        If file doesn't have expected number of columns
    """
    if not filepath.exists():
        raise FileNotFoundError(f"Input file not found: {filepath}")

    logger.info(f"Loading BLAST output from {filepath}")

    df = pd.read_csv(
        filepath,
        sep='\t',
        names=BLAST_COLUMNS,
        dtype={'qseqid': str, 'sseqid': str}
    )

    if len(df.columns) != len(BLAST_COLUMNS):
        raise ValueError(
            f"Expected {len(BLAST_COLUMNS)} columns, found {len(df.columns)}. "
            "Ensure input is BLAST outfmt 6."
        )

    logger.info(f"Loaded {len(df):,} BLAST hits")
    return df


def filter_hits(
    df: pd.DataFrame,
    min_identity: float = 90.0,
    max_evalue: float = 1e-10
) -> pd.DataFrame:
    """
    Filter BLAST hits by identity and e-value thresholds.

    Parameters
    ----------
    df : pd.DataFrame
        BLAST hits DataFrame
    min_identity : float
        Minimum percent identity (default: 90.0)
    max_evalue : float
        Maximum e-value (default: 1e-10)

    Returns
    -------
    pd.DataFrame
        Filtered DataFrame
    """
    n_before = len(df)

    filtered = df[
        (df['pident'] >= min_identity) &
        (df['evalue'] <= max_evalue)
    ].copy()

    n_after = len(filtered)
    logger.info(
        f"Filtered {n_before:,} → {n_after:,} hits "
        f"(identity ≥{min_identity}%, e-value ≤{max_evalue:.0e})"
    )

    return filtered


def extract_genus(sseqid: str) -> Optional[str]:
    """
    Extract genus from subject sequence ID.

    ASSUMPTION: sseqid format is "genus_species_strain" or similar,
    with genus as the first underscore-delimited field.

    Parameters
    ----------
    sseqid : str
        Subject sequence identifier

    Returns
    -------
    str or None
        Genus name, or None if extraction fails
    """
    if pd.isna(sseqid) or not sseqid:
        return None

    parts = str(sseqid).split('_')
    if len(parts) >= 1:
        return parts[0]
    return None


def assign_top_genus_per_query(df: pd.DataFrame) -> pd.DataFrame:
    """
    Assign each query to its best-matching genus.

    For each query, counts hits per genus and assigns the query
    to the genus with the most hits (ties broken by highest mean identity).

    Parameters
    ----------
    df : pd.DataFrame
        Filtered BLAST hits with 'genus' column

    Returns
    -------
    pd.DataFrame
        DataFrame with one row per query: qseqid, genus, hit_count, mean_pident
    """
    # Aggregate hits per query-genus pair
    query_genus_stats = df.groupby(['qseqid', 'genus']).agg(
        hit_count=('genus', 'size'),
        mean_pident=('pident', 'mean')
    ).reset_index()

    # For each query, select genus with most hits (break ties by identity)
    # NOTE: This operation may be slow for very large datasets (>1M queries)
    top_genus = (
        query_genus_stats
        .sort_values(['qseqid', 'hit_count', 'mean_pident'],
                     ascending=[True, False, False])
        .groupby('qseqid')
        .first()
        .reset_index()
    )

    logger.info(f"Assigned {len(top_genus):,} queries to genera")
    return top_genus


def summarize_genera(query_assignments: pd.DataFrame) -> pd.DataFrame:
    """
    Summarize total query counts per genus.

    Parameters
    ----------
    query_assignments : pd.DataFrame
        Output from assign_top_genus_per_query

    Returns
    -------
    pd.DataFrame
        Genus summary with columns: genus, query_count, mean_hit_count
    """
    summary = query_assignments.groupby('genus').agg(
        query_count=('qseqid', 'size'),
        mean_hit_count=('hit_count', 'mean'),
        mean_identity=('mean_pident', 'mean')
    ).reset_index()

    summary = summary.sort_values('query_count', ascending=False)

    logger.info(f"Summarized {len(summary):,} genera")
    return summary


def plot_top_genera(
    genus_summary: pd.DataFrame,
    output_path: Path,
    n_top: int = 20
) -> None:
    """
    Create bar plot of top genera by query count.

    Parameters
    ----------
    genus_summary : pd.DataFrame
        Output from summarize_genera
    output_path : Path
        Path to save figure
    n_top : int
        Number of top genera to plot (default: 20)
    """
    top = genus_summary.head(n_top)

    fig, ax = plt.subplots(figsize=(10, 6))

    bars = ax.barh(
        y=range(len(top)),
        width=top['query_count'],
        color='steelblue',
        edgecolor='black',
        linewidth=0.5
    )

    ax.set_yticks(range(len(top)))
    ax.set_yticklabels(top['genus'])
    ax.invert_yaxis()  # Highest at top
    ax.set_xlabel('Number of Queries')
    ax.set_title(f'Top {n_top} Genera by Query Count')

    # Add count labels
    for bar, count in zip(bars, top['query_count']):
        ax.text(
            bar.get_width() + 0.5,
            bar.get_y() + bar.get_height()/2,
            f'{count:,}',
            va='center',
            fontsize=8
        )

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    logger.info(f"Saved figure to {output_path}")


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Summarize BLAST output by taxonomic genus'
    )
    parser.add_argument(
        'input_file',
        type=Path,
        help='BLAST tabular output file (outfmt 6)'
    )
    parser.add_argument(
        'output_prefix',
        type=str,
        help='Prefix for output files'
    )
    parser.add_argument(
        '--min-identity',
        type=float,
        default=90.0,
        help='Minimum percent identity (default: 90)'
    )
    parser.add_argument(
        '--max-evalue',
        type=float,
        default=1e-10,
        help='Maximum e-value (default: 1e-10)'
    )

    args = parser.parse_args()

    try:
        # Load and process
        df = load_blast_output(args.input_file)
        filtered = filter_hits(df, args.min_identity, args.max_evalue)

        if len(filtered) == 0:
            logger.warning("No hits passed filters. Check thresholds.")
            sys.exit(1)

        # Extract genus
        filtered['genus'] = filtered['sseqid'].apply(extract_genus)
        n_missing_genus = filtered['genus'].isna().sum()
        if n_missing_genus > 0:
            logger.warning(f"{n_missing_genus} hits could not be assigned genus")
            filtered = filtered.dropna(subset=['genus'])

        # Assign and summarize
        query_assignments = assign_top_genus_per_query(filtered)
        genus_summary = summarize_genera(query_assignments)

        # Output
        filtered_path = Path(f"{args.output_prefix}_filtered.csv")
        filtered.to_csv(filtered_path, index=False)
        logger.info(f"Saved filtered hits to {filtered_path}")

        summary_path = Path(f"{args.output_prefix}_genus_summary.csv")
        genus_summary.to_csv(summary_path, index=False)
        logger.info(f"Saved genus summary to {summary_path}")

        plot_path = Path(f"{args.output_prefix}_top_genera.png")
        plot_top_genera(genus_summary, plot_path)

        # Print top genera to console
        print("\n=== Top 10 Genera ===")
        print(genus_summary.head(10).to_string(index=False))

    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

**Requirements (requirements.txt):**
```
pandas>=1.5.0
numpy>=1.21.0
matplotlib>=3.5.0
```

**Assumptions made:**
1. Subject sequence IDs follow "genus_species_strain" format with underscore delimiter
2. Input file is tab-delimited BLAST outfmt 6 with standard 12 columns
3. Genus is the first field before the underscore
4. "Best" genus assignment defined by hit count, then mean identity

**Validation checks:**
1. Test with a small file (~100 lines) where you can verify counts manually
2. Check that genus extraction works on sample sseqid values from your data
3. Verify filter thresholds produce expected number of passing hits
4. Confirm output CSVs are readable and have expected columns

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

Requirements as specified in the prompt template.
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
Models tested: [To be completed]
Date tested: [To be completed]
Notes: [To be completed]
```

## Cross-References

- For R equivalent, see `code/r-script-generation.md`
- For debugging Python errors, see `code/debugging.md`
- For understanding existing code, see `code/code-explanation.md`
- For test requirements, see `code/testing-requirements.md`
