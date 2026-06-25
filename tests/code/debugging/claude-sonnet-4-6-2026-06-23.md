# Test Results: code/debugging.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-23.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** code/debugging.md
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
Context: I am working on {BRIEF_PROJECT_DESCRIPTION} in {LANGUAGE}. I'm encountering an error I can't resolve.

The error message:
```
{PASTE_COMPLETE_ERROR_MESSAGE_AND_TRACEBACK}
```

The relevant code:
```{language}
{PASTE_CODE_THAT_CAUSES_THE_ERROR}
```

What I was trying to do: {EXPLAIN_INTENDED_BEHAVIOR}

What I've already tried:
- {LIST_DEBUGGING_STEPS_ALREADY_TAKEN}

Environment details (if relevant):
- {LANGUAGE_VERSION}
- {RELEVANT_PACKAGE_VERSIONS}
- {OPERATING_SYSTEM_IF_RELEVANT}

Task: Please help me debug this issue:

1. **Explain the error**: What does this error message mean in plain language?

2. **Identify the cause**: What specifically in my code is triggering this error?

3. **Provide the fix**: Show the corrected code with comments explaining the changes.

4. **Explain why**: Why does the fix work? What was wrong with my original approach?

5. **Prevention**: How can I avoid similar errors in the future?

Constraints:
- If you need more information to diagnose the issue, ask before guessing
- If there are multiple possible causes, list them in order of likelihood
- If the error might be environment-specific, note that

Context: I am working on a microbiome diversity analysis in Python. I'm encountering an error I can't resolve.

The error message:
```
ValueError: shapes (50,) and (100,) not aligned: 50 (dim 0) != 100 (dim 0)
```

The relevant code:
```python
import numpy as np
from scipy.spatial.distance import braycurtis

# Load OTU table (samples x taxa)
otu_table = np.loadtxt('otu_table.csv', delimiter=',', skiprows=1)
print(f"OTU table shape: {otu_table.shape}")  # prints (50, 100)

# Calculate pairwise Bray-Curtis distances
n_samples = otu_table.shape[0]
distances = np.zeros((n_samples, n_samples))

for i in range(n_samples):
    for j in range(n_samples):
        distances[i,j] = braycurtis(otu_table[i], otu_table[:,j])
```

What I was trying to do: Calculate a pairwise Bray-Curtis distance matrix between all 50 samples.

What I've already tried:
- Verified the OTU table loads correctly (50 samples, 100 taxa)
- Checked that braycurtis works with single vectors
- Confirmed the loop indices are within bounds

Environment details:
- Python 3.10
- scipy 1.11.0
- numpy 1.24.0
```

## Model Output
```
## Debugging Your Bray-Curtis Distance Calculation

### 1. Explain the Error

The `ValueError: shapes (50,) and (100,) not aligned` means you're passing two vectors of **different lengths** to `braycurtis()`. The function requires both vectors to have the same shape — which makes sense, since you can't compare dissimilarity between vectors representing different numbers of features.

---

### 2. Identify the Cause

The bug is a **transposition error** in your indexing:

```python
# What you wrote:
distances[i,j] = braycurtis(otu_table[i], otu_table[:,j])
#                                    ^^^           ^^^
#                            row i → shape (100,)  col j → shape (50,)
#                            ✓ correct             ✗ wrong axis
```

Your OTU table has shape `(50 samples, 100 taxa)`:

| Indexing | What you get | Shape |
|---|---|---|
| `otu_table[i]` | Row `i` = all taxa for sample `i` | `(100,)` ✅ |
| `otu_table[:,j]` | Column `j` = all samples for taxon `j` | `(50,)` ❌ |

You want to compare **sample `i`** against **sample `j`**, but `otu_table[:,j]` gives you **taxon `j`** across all samples instead.

---

### 3. Provide the Fix

```python
import numpy as np
from scipy.spatial.distance import braycurtis, squareform, pdist

# Load OTU table (samples x taxa)
otu_table = np.loadtxt('otu_table.csv', delimiter=',', skiprows=1)
print(f"OTU table shape: {otu_table.shape}")  # (50, 100)

n_samples = otu_table.shape[0]

# ── Fix 1: Minimal change — correct the row indexing ──────────────────────────
distances = np.zeros((n_samples, n_samples))

for i in range(n_samples):
    for j in range(n_samples):
        # FIX: use otu_table[j] (row j) instead of otu_table[:,j] (column j)
        # Both otu_table[i] and otu_table[j] now have shape (100,) ✓
        distances[i, j] = braycurtis(otu_table[i], otu_table[j])

# ── Fix 2: Recommended — use scipy's built-in vectorized approach ──────────────
# pdist computes all pairwise distances without redundant calculations
# squareform converts the condensed result to a full (50, 50) matrix
distances = squareform(pdist(otu_table, metric='braycurtis'))

print(f"Distance matrix shape: {distances.shape}")  # (50, 50)

# ── Sanity checks ──────────────────────────────────────────────────────────────
assert distances.shape == (n_samples, n_samples), "Wrong output shape"
assert np.allclose(distances, distances.T),       "Matrix should be symmetric"
assert np.allclose(np.diag(distances), 0),        "Diagonal should be zero (self-distance)"
```

---

### 4. Why the Fix Works

**Fix 1** corrects the axis: `otu_table[j]` selects **row `j`** (shape `(100,)`), matching the shape of `otu_table[i]`. Both vectors now represent the same thing — taxon abundances for a single sample.

**Fix 2 (recommended)** is better for three reasons:

```
Your loop:  50 × 50 = 2,500 braycurtis() calls
            Computes every pair TWICE (i→j and j→i)
            Pure Python loop overhead

pdist:      50 × 49 / 2 = 1,225 calls (exploits symmetry)
            Implemented in C under the hood
            ~2–10× faster even at this scale; much more at larger scales
```

---

### 5. Prevention

**① Always verify shapes before passing to distance functions:**
```python
# Add this defensively before your loop
assert otu_table.ndim == 2, "Expected 2D array"
u, v = otu_table[0], otu_table[1]
print(f"Vector shapes: {u.shape}, {v.shape}")  # Must match
```

**② Distinguish row vs. column indexing explicitly:**
```python
# Ambiguous — easy to mix up:
otu_table[i]    # row i   → shape (n_taxa,)
otu_table[:,j]  # col j   → shape (n_samples,)

# Use named variables to make intent clear:
sample_i = otu_table[i, :]   # explicit row slice
sample_j = otu_table[j, :]   # explicit row slice
```

**③ Prefer scipy's purpose-built functions** for pairwise distance work:
```python
from scipy.spatial.distance import pdist, squareform
# Handles shape validation, symmetry, and efficiency for you
```

**④ Add a shape assertion after loading data:**
```python
otu_table = np.loadtxt('otu_table.csv', delimiter=',', skiprows=1)
n_samples, n_taxa = otu_table.shape
print(f"Loaded: {n_samples} samples × {n_taxa} taxa")
# Fail fast if the file loaded transposed or malformed
assert n_samples < n_taxa, "Suspiciously more samples than taxa — check orientation"
```
```

## Assessment

_Machine-suggested (UNCONFIRMED) — drafted by Claude Opus 4.7 on 2026-06-24 (refresh) to speed T4 review. An author must independently read the Model Output above and set the real Recommendation. Anything labeled here is triage, not domain expert review. This draft was regenerated after a harness bug (truncated test inputs on this prompt) was fixed and the model was re-run with the full prompt._

**Machine triage:** Correctly diagnoses the row-vs-column indexing bug and matches the prompt's expected fix (`otu_table[j]` plus `pdist`+`squareform` vectorized alternative). Includes a side-by-side shape table, the corrected loop, the vectorized version, and three sanity-check assertions (symmetric matrix, zero diagonal) — these are useful and verifiable. Cross-model agreement with the other 5 models is unanimous on diagnosis and fix. One prevention bullet adds `assert n_samples < n_taxa` as a "fail fast" check; this is a heuristic that holds for typical microbiome datasets but is not a universal rule.

**Suggested verdict (UNCONFIRMED):** Pass with notes

**What still needs human verification:**
- Whether the `assert n_samples < n_taxa` heuristic should be presented as general advice — it would incorrectly fire on valid datasets with more samples than features.
- That the inline assertions (symmetric, zero diagonal) actually pass when the corrected code is executed against a real OTU table.
- That the explanatory shape table accurately reflects scipy 1.11 / numpy 1.24 indexing semantics (it does, but worth a glance).

## Overall Assessment
- **Recommendation:** PENDING AUTHOR REVIEW
- **Notes:**

## Verification Steps Tested
_Which verification requirements from the prompt were checked, and results._
