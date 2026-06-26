# Test Results: code/debugging.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-25.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** code/debugging.md
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
````

## Model Output
````
## Debugging Your Bray-Curtis Distance Calculation

### 1. What the Error Means

In plain language: you're trying to compare two arrays of **different lengths** (50 elements vs. 100 elements), and `braycurtis` requires both inputs to have the **same shape** to compute a meaningful distance between them.

---

### 2. What's Causing It

The bug is a **transposition error** in your indexing on this line:

```python
distances[i,j] = braycurtis(otu_table[i], otu_table[:,j])
#                                         ^^^^^^^^^^^^^^
#                                         This is WRONG
```

| Expression | What it selects | Shape |
|---|---|---|
| `otu_table[i]` | Row `i` → one sample's taxa counts | `(100,)` — 100 taxa |
| `otu_table[:,j]` | Column `j` → one taxon across all samples | `(50,)` — 50 samples |

You're accidentally comparing a **sample vector** (100 taxa) against a **taxon vector** (50 samples). These represent completely different things, which is why the shapes don't align.

---

### 3. The Fix

```python
import numpy as np
from scipy.spatial.distance import braycurtis, squareform, pdist

# Load OTU table (samples x taxa)
otu_table = np.loadtxt('otu_table.csv', delimiter=',', skiprows=1)
print(f"OTU table shape: {otu_table.shape}")  # (50, 100)

n_samples = otu_table.shape[0]

# ── Fix 1: Corrected manual loop (minimal change to your original code) ──────
distances = np.zeros((n_samples, n_samples))

for i in range(n_samples):
    for j in range(n_samples):
        # FIX: index rows for BOTH samples (row i vs row j)
        # otu_table[i] → shape (100,)  ✓
        # otu_table[j] → shape (100,)  ✓
        distances[i, j] = braycurtis(otu_table[i], otu_table[j])

print(f"Distance matrix shape: {distances.shape}")  # (50, 50)

# ── Fix 2: Recommended — use scipy's built-in (faster, less error-prone) ─────
# pdist computes all unique pairs, squareform converts to full symmetric matrix
distances_v2 = squareform(pdist(otu_table, metric='braycurtis'))

print(f"Distance matrix shape: {distances_v2.shape}")  # (50, 50)

# Verify both approaches give the same result
assert np.allclose(distances, distances_v2), "Results don't match!"
print("Both methods produce identical results ✓")

# ── Sanity checks you should always run ──────────────────────────────────────
assert distances.shape == (n_samples, n_samples), "Wrong output shape"
assert np.allclose(distances, distances.T), "Matrix should be symmetric"
assert np.allclose(np.diag(distances), 0), "Diagonal should be all zeros"
print("All sanity checks passed ✓")
```

---

### 4. Why the Fix Works

**Original (broken):**
```
braycurtis( otu_table[i],   otu_table[:,j] )
            shape (100,)    shape (50,)      ← mismatch!
            "sample i"      "taxon j"        ← wrong concept!
```

**Fixed:**
```
braycurtis( otu_table[i],   otu_table[j] )
            shape (100,)    shape (100,)     ← match ✓
            "sample i"      "sample j"       ← correct concept ✓
```

Both vectors now represent the **same kind of thing** (a sample's distribution across 100 taxa), so Bray-Curtis can meaningfully measure the dissimilarity between them.

The `pdist`/`squareform` approach is preferable because:
- It's **~2x faster** (only computes the upper triangle, since distance is symmetric)
- It **eliminates indexing bugs** entirely by handling iteration internally
- It's the **idiomatic scipy pattern** for pairwise distance matrices

---

### 5. How to Prevent This in the Future

**Add shape assertions before calling distance functions:**
```python
# Assert before the loop, not after
assert otu_table.ndim == 2, "Expected 2D array"
sample_a, sample_b = otu_table[0], otu_table[1]
assert sample_a.shape == sample_b.shape, (
    f"Shape mismatch: {sample_a.shape} vs {sample_b.shape}"
)
```

**Use descriptive variable names that encode meaning:**
```python
# Ambiguous — easy to mix up axes
x = otu_table[i]
y = otu_table[:,j]  # looks plausible but is wrong

# Clear — the name tells you what it is
sample_i = otu_table[i]   # shape (n_taxa,)
sample_j = otu_table[j]   # shape (n_taxa,)
```

**Prefer high-level library functions over manual loops** when they exist — `pdist` is specifically designed for this task and removes the opportunity for this class of indexing error entirely.
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
