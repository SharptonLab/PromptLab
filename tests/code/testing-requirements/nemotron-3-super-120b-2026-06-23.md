# Test Results: code/testing-requirements.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-23.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** code/testing-requirements.md
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
Context: I have {R/Python} code for {ANALYSIS_DESCRIPTION}. I need to verify it produces correct results before using it for my research.

The code to test:
```{language}
{PASTE_CODE_OR_FUNCTION}
```

What the code should do: {DESCRIBE_EXPECTED_BEHAVIOR}

Test data available: {DESCRIBE_ANY_TEST_DATA_YOU_HAVE: e.g., "I have a small dataset with known results," "I can generate synthetic data"}

Task: Help me create a testing strategy for this code:

1. **Test cases**: Suggest specific test cases covering:
   - Normal/expected inputs (does it work for typical data?)
   - Edge cases (empty input, single row, extreme values)
   - Known-answer tests (if possible)
   - Boundary conditions

2. **Test code**: Write test code I can run to verify each case. Use {TESTING_APPROACH: e.g., "simple assert statements," "testthat for R," "pytest for Python"}.

3. **Validation checks**: What should I manually inspect in the output to verify correctness?

4. **Red flags**: What output patterns would indicate the code is wrong?

Constraints:
- Focus on tests that catch meaningful errors, not pedantic checks
- Prioritize tests for the parts most likely to be wrong
- If full automated testing is overkill, suggest lightweight manual verification
- Note any tests that require me to know the "right" answer in advance

Output format: Test strategy with code examples for each test type.

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

Task: Help me create a testing strategy using simple assert statements and manual checks.
```

## Model Output
```


**Testing Strategy for the CLR‑transform function**  
*(Python – simple `assert` statements + optional manual inspection)*  

---

## 1. Test‑case ideas  

| Category | What to test | Why it matters | Example data (you can generate) |
|----------|--------------|----------------|---------------------------------|
| **Normal / expected** | Typical count matrix (≥2 samples, ≥3 features) with moderate values | Checks the core algorithm on realistic data | `[[10, 20, 30], [5, 15, 25]]` |
| **Edge – empty** | 0‑row or 0‑column matrix | Should raise a clear error or return an empty array of the same shape | `np.empty((0,3))` or `np.empty((2,0))` |
| **Edge – single row / single column** | One sample or one feature | Verifies broadcasting & geometric‑mean handling | `[[1,2,3]]` (1×3) or `[[4],[8],[12]]` (3×1) |
| **Edge – zeros** | Counts that contain true zeros (before pseudocount) | Pseudocount must prevent `log(0)`; after adding 0.5 the result should be finite | `[[0, 5, 10], [2,0,3]]` |
| **Edge – extreme values** | Very large or very small counts (e.g., 1e6 vs 1) | Tests for overflow/underflow in log & exp | `[[1, 1_000_000], [10_000, 1]]` |
| **Known‑answer** | Hand‑crafted matrix where you can compute CLR analytically | Guarantees the implementation matches the definition | See section 2 for a concrete example |
| **Boundary – constant rows** | All counts in a row are identical (after pseudocount) | Geometric mean = that value → CLR should be (approximately) 0 for every feature | `[[5,5,5], [7,7,7]]` |
| **Boundary – single feature** | Only one column → geometric mean = that value → CLR should be 0 (up to rounding) | Checks that `axis=1, keepdims=True` works when dimension size = 1 | `[[4],[9],[16]]` |

---

## 2. Test code (plain `assert` statements)

```python
import numpy as np

def clr_transform(counts):
    """Apply centered log-ratio transformation to count data."""
    counts_pseudo = counts + 0.5
    log_counts = np.log(counts_pseudo)
    geometric_mean = np.exp(log_counts.mean(axis=1, keepdims=True))
    clr = np.log(counts_pseudo / geometric_mean)
    return clr

# ------------------------------------------------------------------
# Helper to compare with a tolerance (avoid exact float equality)
def assert_allclose(a, b, rtol=1e-7, atol=1e-12):
    if not np.allclose(a, b, rtol=rtol, atol=atol):
        raise AssertionError(f"Arrays not close:\n{a}\n!\n{b}")

# ------------------------------------------------------------------
# 1. Normal case
def test_normal():
    X = np.array([[10., 20., 30.],
                  [5., 15., 25.]])
    out = clr_transform(X)
    # each row should sum to ~0 (property of CLR)
    assert_allclose(out.sum(axis=1), 0.)
    # spot‑check one value (computed with a calculator or another implementation)
    # For row 0: pseudo = [10.5,20.5,30.5]; gm = exp(mean(log(pseudo))) ≈ 19.0
    # clr0 = log(10.5/19.0) ≈ -0.5878
    assert_allclose(out[0, 0], -0.587789, atol=1e-5)

# 2. Empty matrix – should return empty array of same shape
def test_empty():
    X = np.empty((0, 3))
    out = clr_transform(X)
    assert out.shape == (0, 3)
    # No values to check; just ensure no exception

# 3. Single row
def test_single_row():
    X = np.array([[1., 2., 3.]])
    out = clr_transform(X)
    assert_allclose(out.sum(), 0.)          # row sum ≈ 0
    # manual check (optional)
    # pseudo = [1.5,2.5,3.5]; gm ≈ exp(mean(log(pseudo))) ≈ 2.24
    # clr ≈ [log(1.5/2.24), log(2.5/2.24), log(3.5/2.24)]
    expected = np.log(np.array([1.5, 2.5, 3.5]) / np.exp(np.log(np.array([1.5,2.5,3.5])).mean()))
    assert_allclose(out, expected)

# 4. Single column
def test_single_column():
    X = np.array([[4.], [9.], [16.]])
    out = clr_transform(X)
    # With one feature, CLR = log(value/gm) where gm = value → should be 0
    assert_allclose(out, 0.)

# 5. Zeros (pseudocount prevents log(0))
def test_zeros():
    X = np.array([[0., 5., 10.],
                  [2., 0., 3.]])
    out = clr_transform(X)
    # No NaN or -inf should appear
    assert np.isfinite(out).all()
    # Row sums ≈ 0
    assert_allclose(out.sum(axis=1), 0.)

# 6. Extreme values
def test_extreme():
    X = np.array([[1., 1_000_000.],
                  [10_000., 1.]])
    out = clr_transform(X)
    assert np.isfinite(out).all()
    assert_allclose(out.sum(axis=1), 0.)

# 7. Constant row (should give ~0)
def test_constant_row():
    X = np.array([[5.,5.,5.],
                  [7.,7.,7.]])
    out = clr_transform(X)
    assert_allclose(out, 0., atol=1e-12)

# 8. Known‑answer test (hand‑derived)
def test_known_answer():
    # Simple 2×2 matrix where we can compute CLR by hand
    X = np.array([[2., 8.],
                  [1., 1.]])
    # Add pseudocount 0.5
    pseudo = X + 0.5          # [[2.5,8.5],[1.5,1.5]]
    gm = np.exp(np.log(pseudo).mean(axis=1, keepdims=True))  # geometric mean per row
    expected = np.log(pseudo / gm)
    out = clr_transform(X)
    assert_allclose(out, expected)

# ------------------------------------------------------------------
# Run all tests (simple script style)
if __name__ == "__main__":
    for name in [obj for obj in dir() if obj.startswith("test_")]:
        func = globals()[name]
        try:
            func()
            print(f"✓ {name}")
        except AssertionError as e:
            print(f"✗ {name}: {e}")
```

**How to use**

* Copy the function `clr_transform` and the test block into a file (e.g., `test_clr.py`).  
* Run `python test_clr.py`.  
* Each test prints a check‑mark or a failure with the offending assertion.

---

## 3. Validation checks (what to look at manually)

Even with the automated asserts, it’s good to eyeball a few outputs:

| Check | What to verify |
|-------|----------------|
| **Row‑wise sum ≈ 0** | CLR forces the mean of log‑ratios to zero; `out.sum(axis=1)` should be ~0 (within numerical tolerance). |
| **No NaN / -Inf** | After adding the pseudocount, every entry must be finite. |
| **Symmetry for constant rows** | If a row contains identical counts (after pseudocount), the CLR row should be (near) all zeros. |
| **Invariance to scaling** | Multiplying an entire row by a constant `c>0` should *not* change the CLR output (because the geometric mean scales the same way). You can test: `assert_allclose(clr_transform(X), clr_transform(X*c))`. |
| **Monotonicity** | For a fixed row, if you increase one count while keeping others fixed, the corresponding CLR value should increase (others decrease slightly to keep row sum zero). Spot‑check a couple of rows. |

---

## 4. Red flags – patterns that signal a bug

| Symptom | Likely cause |
|---------|--------------|
| **Row sums far from 0** (e.g., > 1e‑2) | Mistake in geometric‑mean calculation (wrong axis, missing `keepdims`, or using arithmetic mean). |
| **Presence of `NaN` or `-Inf`** | Pseudocount missing or incorrectly placed; `log(0)` still occurring. |
| **All zeros output for non‑constant data** | Accidentally dividing by the geometric mean *after* taking log (i.e., `log(counts) - log(gm)` vs `log(counts/gm)`). |
| **Output changes when you multiply a row by a constant** | Using the original counts (without pseudocount) in the geometric mean or forgetting to apply the same scaling to the pseudo‑counts. |
| **Very large absolute values (> 50) for moderate counts** | Overflow in `np.exp` or `np.log` due to missing pseudocount or using raw counts in the log step. |
| **Shape mismatch** (output shape ≠ input shape) | Accidentally dropping a dimension (e.g., using `axis=1` without `keepdims=True` and then broadcasting incorrectly). |

If any of these appear, revisit the lines:

```python
counts_pseudo = counts + 0.5
log_counts = np.log(counts_pseudo)
geometric_mean = np.exp(log_counts.mean(axis=1, keepdims=True))
clr = np.log(counts_pseudo / geometric_mean)
```

---

### Quick “lightweight” manual verification (if you don’t want to write the full test suite)

1. **Create a tiny 2×3 matrix** (e.g., `[[1,2,3],[4,5,6]]`).  
2. Compute the CLR by hand or with a trusted tool (R `compositions::clr`, or an online calculator).  
3. Call your function and compare the two matrices with `np.allclose`.  
4. Check that each row sums to zero and that there are no `NaN`s.  

If those three checks pass, you can be reasonably confident the implementation is correct for typical microbiome count data.  

--- 

**Remember:** The only tests that *require* you to know the right answer in advance are the “known‑answer” and the manual spot‑check (step 2 above). All other tests (row‑sum zero, finiteness, scaling invariance, constant‑row zero) are self‑checking and protect against the most common logical mistakes. Happy testing!
```

## Overall Assessment
- **Recommendation:** Pass
- **Notes:**
## Verification Steps Tested
_Which verification requirements from the prompt were checked, and results._
