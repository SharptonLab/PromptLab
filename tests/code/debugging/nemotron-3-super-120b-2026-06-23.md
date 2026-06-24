# Test Results: code/debugging.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-23.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** code/debugging.md
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
Context: I am working on {BRIEF_PROJECT_DESCRIPTION} in {LANGUAGE}. I'm encountering an error I can't resolve.

The error message:

Context: I am working on a microbiome diversity analysis in Python. I'm encountering an error I can't resolve.

The error message:
```

## Model Output
```


I'd be happy to help you troubleshoot your microbiome diversity analysis error in Python! However, **I need to see the actual error message** (including the traceback) to provide a specific solution. Microbiome analysis often involves specific libraries and data formats where errors can stem from subtle issues.

**Please reply with:**
1. **The full error message** (including the traceback lines starting with `Traceback (most recent call last):`)
2. **Key context** (if possible):
   - Which libraries you're using (e.g., `scikit-bio`, `pandas`, `numpy`, `QIIME 2` artifacts, `biom-format`, `statsmodels`, `seaborn`/`matplotlib`)
   - What step you were performing (e.g., loading data, calculating alpha/beta diversity, running PERMANOVA, plotting PCoA)
   - A minimal code snippet that reproduces the error (if shareable)
   - Your Python version and key library versions (e.g., `pip list | grep -E "scikit-bio|pandas|numpy"`)

---

### 🔍 While you gather that, here are **common microbiome-specific pitfalls** in Python to check:

| Error Type                  | Typical Cause                                                                 | Quick Check                                                                 |
|-----------------------------|-------------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| **`ValueError: Unknown metric`** | Incorrect distance metric name (e.g., `'braycurtis'` vs `'bray-curtis'`)      | Verify metric names in [`skbio.diversity.beta_diversity`](https://scikit-bio.org/docs/latest/generated/skbio.diversity.beta_diversity.html) |
| **`KeyError` or `IndexError`**  | Mismatched sample IDs between metadata and OTU/ASV table                      | Ensure sample IDs are **exact strings** (no extra spaces) and present in both files |
| **`MemoryError`**           | Large BIOM file or distance matrix (common with >10k samples)                 | Use sparse matrices (`scipy.sparse`) or subset data early                   |
| **`ImportError: No module named 'qiime2'`** | Trying to use QIIME 2 artifacts without `qiime2` installed                  | Install via `conda install -c qiime2/label/r2024.5 qiime2` (or use `q2types` if just handling artifacts) |
| **`LinAlgError: SVD did not converge`** | Issues in PCoA/PCA (often due to constant columns or NaNs in distance matrix) | Check for zero-variance features; use `skbio.stats.distance.ztree` for robust PCoA |
| **File parsing errors**     | BIOM format v1.0 vs v2.1 incompatibility; incorrect TSV/CSV delimiters        | Validate BIOM with `biom validate`; use `pd.read_csv(..., sep='\t')` for TSV |

---

### 💡 Pro Tips for Microbiome Debugging:
1. **Validate inputs early**:  
   ```python
   import pandas as pd
   table = pd.read_csv("otu_table.tsv", sep="\t", index_col=0)
   print("Table shape:", table.shape)
   print("Sample IDs match metadata?", table.index.isin(metadata.index).all())
   ```
2. **Use scikit-bio's built-in validators**:  
   ```python
   from skbio import TabularMSA, DistanceMatrix
   # DistanceMatrix will raise clear errors for invalid inputs
   dm = DistanceMatrix(data, ids=sample_ids)
   ```
3. **Check for hidden characters**:  
   Sample IDs often have trailing spaces (`"Sample_A "` vs `"Sample_A"`). Use:  
   ```python
   table.index = table.index.str.strip()
   metadata.index = metadata.index.str.strip()
   ```

**Once you share the error, I’ll give you a precise fix!**  
*(If you can’t share the full error, even the first 2-3 lines of the traceback and the exact function call that failed will help immensely.)*  

**Example of what to paste:**  
> ```
> Traceback (most recent call last):
>   File "analysis.py", line 42, in <module>
>     beta_div = skbio.diversity.beta_diversity("braycurtis", table_df.values, ids=table_df.index)
>   File ".../skbio/diversity/_beta_diversity.py", line 123, in beta_diversity
>     raise ValueError("Metric 'braycurtis' is not valid.")
> ValueError: Metric 'braycurtis' is not valid.
> ```  
> *(Fix: Use `"braycurtis"` → `"braycurtis"` is invalid; correct name is `"braycurtis"` [no hyphen] or check [skbio docs](https://scikit-bio.org/docs/latest/generated/skbio.diversity.beta_diversity.html))*  

Just paste your error, and I’ll break it down! 🧫🔬
```

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
