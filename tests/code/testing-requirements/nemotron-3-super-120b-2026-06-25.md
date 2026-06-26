# Test Results: code/testing-requirements.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-25.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** code/testing-requirements.md
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
Context: I have Python code for normalizing microbiome count data using centered log-ratio (CLR) transformation. I need to verify it produces correct results before using it for my research.

The code to test:
```python
import numpy as np

def clr_transform(counts):
    """Apply centered log-ratio transformation to count data."""
    # Add pseudocount to avoid log(0)
    counts_pseudo = counts + 0.5

    # Calculate geometric mean per sample (row)
    log_counts = np.log(counts_pseudo)
    geometric_mean = np.exp(log_counts.mean(axis=1, keepdims=True))

    # CLR = log(value / geometric mean)
    clr = np.log(counts_pseudo / geometric_mean)

    return clr
```

What the code should do: Transform count data using CLR, which centers each sample's log-transformed values by subtracting the geometric mean. Output should have mean of 0 across features for each sample.

Test data available: I can create simple test matrices with known values.

Task: Help me create a testing strategy for this code:

1. **Test cases**: Suggest specific test cases covering:
   - Normal/expected inputs (does it work for typical data?)
   - Edge cases (empty input, single row, extreme values)
   - Known-answer tests (if possible)
   - Boundary conditions

2. **Test code**: Write test code I can run to verify each case. Use simple assert statements.

3. **Validation checks**: What should I manually inspect in the output to verify correctness?

4. **Red flags**: What output patterns would indicate the code is wrong?

Constraints:
- Focus on tests that catch meaningful errors, not pedantic checks
- Prioritize tests for the parts most likely to be wrong
- If full automated testing is overkill, suggest lightweight manual verification
- Note any tests that require me to know the "right" answer in advance

Output format: Test strategy with code examples for each test type.
````

## Model Output
````


Below is a **light‑weight testing strategy** you can copy‑paste into a Python file or notebook and run immediately.  
It focuses on the parts of the function that are most likely to hide bugs:

* the pseudocount addition  
* the geometric‑mean calculation (axis = 1, keepdims)  
* the final log‑ratio  

Each test is written with plain `assert` (or `numpy.testing.assert_allclose` when a tolerance is needed) so you can see exactly which condition failed.

---

## 1. Test‑case catalogue  

| Category | What we test | Why it matters |
|----------|--------------|----------------|
| **Normal / expected** | A modest‑size matrix with a mix of zeros, small and large counts. | Checks the happy‑path – the code should run and give a sensible CLR. |
| **Known‑answer (analytic)** | A 2 × 2 matrix where the geometric mean can be computed by hand. | Gives an exact reference value; any deviation points to a formula error. |
| **Single‑row** | One sample (1 × N). | Verifies that `axis=1, keepdims` still works when there is only one row. |
| **Single‑column** | One feature (M × 1). | Makes sure the geometric mean is computed per‑row, not per‑column. |
| **All zeros** | Every entry = 0 (after pseudocount becomes 0.5). | Tests the log of a constant and that the output is all zeros (since log(0.5/0.5)=0). |
| **Extreme values** | Very large numbers (e.g. 1e6) mixed with very small (e.g. 1). | Checks for overflow/under‑flow in `np.log` and the division step. |
| **Non‑integer / float input** | Counts supplied as floats (e.g. after prior normalization). | The function should still work; it only uses `+`, `log`, `mean`, `exp`. |
| **Shape preservation** | Output shape must equal input shape. | A simple sanity check that no accidental broadcasting changed dimensions. |
| **Row‑mean‑zero property** | For any input, the mean of each row of the CLR output should be (numerically) zero. | This is the defining characteristic of CLR; catching a mistake here is the strongest test. |

---

## 2. Test code (run as‑is)

```python
import numpy as np

# ---- function under test -------------------------------------------------
def clr_transform(counts):
    """Apply centered log-ratio transformation to count data."""
    counts_pseudo = counts + 0.5               # pseudocount
    log_counts = np.log(counts_pseudo)
    geometric_mean = np.exp(log_counts.mean(axis=1, keepdims=True))
    clr = np.log(counts_pseudo / geometric_mean)
    return clr
# -------------------------------------------------------------------------

def assert_close(a, b, rtol=1e-7, atol=1e-12):
    """Wrapper that gives a clear error message."""
    np.testing.assert_allclose(a, b, rtol=rtol, atol=atol,
                               err_msg=f"\n{ a }\n!=\n{ b }")

# -------------------------- 1. Normal / expected -------------------------
def test_normal():
    X = np.array([[10,  0,  5],
                  [ 1, 100,  2],
                  [ 0,  0,  0]], dtype=float)
    Y = clr_transform(X)
    # shape check
    assert Y.shape == X.shape
    # row‑mean‑zero (within numerical tolerance)
    assert_close(Y.mean(axis=1), np.zeros(X.shape[0]))
    # no NaNs / infs
    assert np.isfinite(Y).all()

# -------------------------- 2. Known‑answer (analytic) --------------------
def test_known_answer():
    # 2×2 matrix, easy to compute geometric mean by hand
    X = np.array([[1., 4.],
                  [9., 16.]])
    # add pseudocount 0.5
    Xp = X + 0.5          # [[1.5, 4.5], [9.5, 16.5]]
    # geometric mean per row (log‑space)
    gm = np.exp(np.log(Xp).mean(axis=1, keepdims=True))  # [[2.598..., 12.5...]]
    expected = np.log(Xp / gm)
    Y = clr_transform(X)
    assert_close(Y, expected)

# -------------------------- 3. Single‑row --------------------------------
def test_single_row():
    X = np.array([[0, 1, 2, 3]], dtype=float)
    Y = clr_transform(X)
    assert Y.shape == (1, 4)
    assert_close(Y.mean(axis=1), np.zeros(1))
    # after pseudocount: [0.5,1.5,2.5,3.5]; geometric mean = exp(mean(log))
    # we can also check that the sum of CLR values is zero (property of CLR)
    assert_close(Y.sum(), 0.0)

# -------------------------- 4. Single‑column ------------------------------
def test_single_column():
    X = np.array([[0], [5], [10]], dtype=float)
    Y = clr_transform(X)
    assert Y.shape == (3, 1)
    assert_close(Y.mean(axis=1), np.zeros(3))
    # With one column, CLR should be identically zero because gm == value
    assert_close(Y, np.zeros_like(Y))

# -------------------------- 5. All zeros --------------------------------
def test_all_zeros():
    X = np.zeros((4, 3))
    Y = clr_transform(X)
    # after pseudocount every entry = 0.5 → log(0.5/0.5)=0
    assert_close(Y, np.zeros_like(Y))

# -------------------------- 6. Extreme values ---------------------------
def test_extreme():
    X = np.array([[1e-6, 1e6],
                  [1,    1]],
                  dtype=float)
    Y = clr_transform(X)
    assert Y.shape == X.shape
    assert_close(Y.mean(axis=1), np.zeros(2))
    assert np.isfinite(Y).all()

# -------------------------- 7. Float input -------------------------------
def test_float_input():
    X = np.array([[0.2, 0.3, 0.5],
                  [0.1, 0.8, 0.1]], dtype=float)
    Y = clr_transform(X)
    assert Y.shape == X.shape
    assert_close(Y.mean(axis=1), np.zeros(2))
    assert np.isfinite(Y).all()

# -------------------------- 8. Row‑mean‑zero property (generic) ----------
def test_row_mean_zero_generic():
    rng = np.random.default_rng(42)
    for _ in range(5):
        X = rng.integers(0, 100, size=(7, 5)).astype(float)
        Y = clr_transform(X)
        assert_close(Y.mean(axis=1), np.zeros(7), atol=1e-12)

# -------------------------- 9. Shape preservation ------------------------
def test_shape_preservation():
    shapes = [(1,1), (2,3), (5,5), (10,2)]
    for s in shapes:
        X = np.random.randint(0, 50, size=s).astype(float)
        Y = clr_transform(X)
        assert Y.shape == s, f"shape mismatch for input shape {s}"

# -------------------------------------------------------------------------
if __name__ == "__main__":
    # Run all tests; any AssertionError will pinpoint the failing case.
    for name in globals():
        if name.startswith("test_"):
            print(f"Running {name} ...", end=" ")
            globals()[name]()
            print("OK")
    print("\nAll tests passed.")
```

**How to use**

* Copy the block above into a file `test_clr.py` (or a notebook cell).  
* Execute it – it will print `OK` for each test that passes.  
* If a test fails, the `AssertionError` will show the mismatched arrays, making it easy to locate the bug (e.g., wrong axis, missing `keepdims`, incorrect pseudocount, etc.).

---

## 3. Validation checks you can do manually (optional)

| What to look at | How to check | What it tells you |
|-----------------|--------------|-------------------|
| **Row means** | `np.mean(clr_output, axis=1)` | Should be (≈) 0 for every row. |
| **Sum of each row** | `np.sum(clr_output, axis=1)` | For CLR the sum is also 0 (because mean = 0 and number of columns is constant). |
| **Effect of pseudocount** | Compare output with and without the `+0.5` on a tiny matrix that contains zeros. | Without the pseudocount you’ll get `-inf` where the count was 0; with it you should get finite numbers. |
| **Invariance to scaling** (optional) | Multiply a whole row by a constant `c>0` and recompute CLR; the result should be unchanged (the geometric mean scales the same way). | Confirms the ratio‑based nature of the transform. |
| **Symmetry** | Swap two columns in a row; the two CLR values should swap accordingly. | Checks that the function treats each feature independently. |

---

## 4. Red‑flag patterns (output that means the code is wrong)

| Symptom | Likely cause |
|---------|--------------|
| **Row means far from zero** (e.g., 0.3, -1.2) | Geometric mean computed on the wrong axis (`axis=0`) or `keepdims` missing → broadcasting error. |
| **NaN or `-inf` values** | Log taken of a non‑positive number → pseudocount not added or added incorrectly (e.g., `counts - 0.5`). |
| **All rows identical** (or all zeros) regardless of input | Geometric mean calculated over the *entire* array (`np.exp(np.log(counts_pseudo).mean())`) instead of per‑row. |
| **Output shape differs from input** (e.g., `(n_samples,)` instead of `(n_samples, n_features)`) | Accidental squeezing (`np.squeeze`) or misuse of `keepdims`. |
| **Values change when you multiply a whole row by a constant** | Indicates the code is using an additive constant (like the pseudocount) inside the log rather than a pure ratio. |
| **Large absolute values (> 1e6) for modest counts** | Possible overflow in `np.exp(log_counts.mean())` when the geometric mean is huge; usually a sign that the log‑mean was taken on the wrong axis (producing a scalar instead of a vector). |

If you see any of the above, inspect the corresponding line in the function:

* `log_counts.mean(axis=1, keepdims=True)` – **must** be axis = 1 and keepdims.  
* `counts_pseudo = counts + 0.5` – **must** be addition, not subtraction.  
* `np.log(counts_pseudo / geometric_mean)` – **must** be division, not subtraction or multiplication.

---

### TL;DR checklist

1. **Run the automated test suite** above – any failure points directly to a logical mistake.  
2. **Spot‑check** the row‑mean‑zero property on a few random matrices.  
3. **Verify** that adding a pseudocount truly removes `-inf`/`nan`.  
4. **Watch out** for the axis/`keepdims` combo – that’s the most common slip‑up.  

Passing all tests gives you high confidence that the CLR implementation behaves as expected for typical microbiome count data and the edge cases you’re likely to encounter. Happy testing!
````

## Assessment

_Machine-suggested (UNCONFIRMED) — drafted by Claude Opus 4.7 on 2026-06-26 to speed T4 review. An author must independently read the Model Output above and set the real Recommendation. Anything labeled here is triage, not domain expert review._

**Machine triage:** Output is complete — focused, copy-paste-ready test code with explicit "watch out for axis/keepdims" advice. Strong cross-model agreement with peers on priority tests (pseudocount, geometric mean axis, row-sum-zero).

**Suggested verdict (UNCONFIRMED):** Pass

**What still needs human verification:**
- Verify the "passing all tests gives high confidence" claim isn't overconfident given the test scope
- That suggested snippets execute without modification on typical numpy

**Local code check:** Syntax PASS across 1 block(s) · 0/1 imports available.

## Overall Assessment
- **Recommendation:** PENDING AUTHOR REVIEW
- **Notes:**

## Verification Steps Tested
_Which verification requirements from the prompt were checked, and results._
