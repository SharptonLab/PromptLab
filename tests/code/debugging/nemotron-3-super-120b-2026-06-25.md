# Test Results: code/debugging.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-25.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** code/debugging.md
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


**1. Explain the error (plain language)**  

```
ValueError: shapes (50,) and (100,) not aligned: 50 (dim 0) != 100 (dim 0)
```

`scipy.spatial.distance.braycurtis` expects **two 1‑D arrays that have the same number of elements** – each array represents one observation (e.g., one sample) measured across the same set of features (taxa).  
The error tells us that the first argument you gave has length 50, the second has length 100, so the function cannot pair up the elements to compute the distance.

---

**2. Identify the cause**  

In your double loop you are doing:

```python
braycurtis(otu_table[i], otu_table[:,j])
```

* `otu_table[i]` → the *i‑th row* → a vector of **100 taxa** (shape `(100,)`).  
* `otu_table[:,j]` → the *j‑th column* → a vector of **50 samples** for that single taxon (shape `(50,)`).

You are therefore comparing a **sample‑vector (100 taxa)** with a **taxon‑vector (50 samples)**. Their lengths differ, hence the shape mismatch.

What you actually want is the distance **between two samples**, i.e. between two rows:

```python
braycurtis(otu_table[i], otu_table[j])   # both are (100,)
```

---

**3. Provide the fix**  

Here is a corrected version (with a small optimisation that only computes the upper‑triangular part and mirrors it, because the distance matrix is symmetric):

```python
import numpy as np
from scipy.spatial.distance import braycurtis

# Load OTU table (samples x taxa)
otu_table = np.loadtxt('otu_table.csv', delimiter=',', skiprows=1)
print(f"OTU table shape: {otu_table.shape}")   # (50, 100)

n_samples = otu_table.shape[0]
distances = np.zeros((n_samples, n_samples))

# Compute pairwise Bray‑Curtis distances
for i in range(n_samples):
    for j in range(i, n_samples):               # i ≤ j → upper triangle + diagonal
        d = braycurtis(otu_table[i], otu_table[j])  # both are length‑100 vectors
        distances[i, j] = d
        distances[j, i] = d   # mirror because D(i,j) = D(j,i)

# Optional: verify symmetry & zero diagonal
assert np.allclose(distances, distances.T)
assert np.allclose(np.diag(distances), 0.0)
```

*If you prefer a fully vectorised approach (much faster for larger matrices):*

```python
from scipy.spatial.distance import pdist, squareform

# pdist computes the condensed distance matrix; squareform expands it to a full matrix
distances = squareform(pdist(otu_table, metric='braycurtis'))
```

Both snippets produce a `(50, 50)` matrix where `distances[i, j]` is the Bray‑Curtis dissimilarity between sample *i* and sample *j*.

---

**4. Explain why the fix works**  

* `braycurtis` internally does something like:

```python
num = np.sum(np.abs(u - v))
den = np.sum(np.abs(u) + np.abs(v))
return num / den
```

where `u` and `v` must be **element‑wise comparable** (same length).  
By passing `otu_table[i]` and `otu_table[j]` we give it two vectors that each contain the abundances of the **same 100 taxa** for two different samples, satisfying the length requirement.  

The original code passed a taxon‑vector (`otu_table[:,j]`) of length 50, so the subtraction `u - v` tried to align a 100‑element array with a 50‑element array, leading to the shape mismatch error.

---

**5. Prevention tips**  

| Situation | Defensive practice | Example |
|-----------|--------------------|---------|
| **Mismatched array sizes** | Add an explicit shape check before calling the distance function. | `assert otu_table[i].shape == otu_table[j].shape, f"Shapes {otu_table[i].shape} vs {otu_table[j].shape}"` |
| **Looping over rows vs columns** | Keep a mental model: rows = observations, columns = features. Name variables accordingly (`sample_i`, `sample_j`). | `sample_i = otu_table[i]; sample_j = otu_table[j]` |
| **Repeated distance calculations** | Use SciPy’s built‑in pairwise functions (`pdist`, `cdist`, `squareform`) which are tested and handle shape checks internally. | `distances = squareform(pdist(otu_table, metric='braycurtis'))` |
| **Debugging shape issues** | Print shapes right before the problematic call, or use `np.shape` in an `if` statement. | `print(f"i={i}, j={j}, shapes: {otu_table[i].shape}, {otu_table[:,j].shape}")` |
| **Unit testing** | Write a small test that feeds known vectors (e.g., identical vectors → distance 0) and asserts the output. | `assert braycurtis(np.ones(5), np.ones(5)) == 0.0` |

By consistently checking shapes, using the correct axis (rows for samples), and leveraging vectorised SciPy helpers, you’ll avoid this class of error in future microbiome (or any other) distance‑matrix calculations.
````

## Assessment

_Machine-suggested (UNCONFIRMED) — drafted by Claude Opus 4.7 on 2026-06-26 to speed T4 review. An author must independently read the Model Output above and set the real Recommendation. Anything labeled here is triage, not domain expert review._

**Machine triage:** Output covers all 5 requested sections, correctly diagnoses the indexing bug, and notably **goes beyond peers** by showing the actual Bray-Curtis formula `num/den` to demonstrate why same-length vectors are required. Includes an upper-triangle-only optimization (with symmetric mirror) plus a vectorized `pdist`/`squareform` alternative, plus prevention table including a unit-test suggestion. Complete, no truncation. **Strong cross-model agreement** on the root cause.

**Suggested verdict (UNCONFIRMED):** Pass

**What still needs human verification:**
- Confirm the inlined Bray-Curtis formula is accurate (it shows the numerator/denominator form, which matches the standard definition)
- That the upper-triangle loop snippet is correct (i ≤ j range, mirror assignment)
- Whether the unit-test prevention tip (`assert braycurtis(ones, ones) == 0.0`) is appropriate for this reader

**Local code check:** Syntax FAIL (1/5) across 5 block(s) · 0/2 imports available · fails — block 5 (python): line 3: 'return' outside function.

## Overall Assessment
- **Recommendation:** PENDING AUTHOR REVIEW
- **Notes:**

## Verification Steps Tested
_Which verification requirements from the prompt were checked, and results._
