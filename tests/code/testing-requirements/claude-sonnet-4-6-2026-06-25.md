# Test Results: code/testing-requirements.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-25.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** code/testing-requirements.md
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
# CLR Transform Testing Strategy

## Priority Assessment

The most likely failure points in this code are:
1. **Axis confusion** — geometric mean computed over wrong dimension
2. **CLR math** — the log/exp operations could be simplified incorrectly
3. **Pseudocount placement** — added inconsistently
4. **Shape handling** — 1D vs 2D arrays

The zero-mean property is your best automated check because it's mathematically guaranteed for CLR and doesn't require knowing the exact output values.

---

## Test Cases

### 1. Known-Answer Test (Most Valuable)

This is the test you should trust most. Compute by hand first, then verify.

```python
import numpy as np

def clr_transform(counts):
    counts_pseudo = counts + 0.5
    log_counts = np.log(counts_pseudo)
    geometric_mean = np.exp(log_counts.mean(axis=1, keepdims=True))
    clr = np.log(counts_pseudo / geometric_mean)
    return clr

def test_known_answer():
    """
    Hand-computed example so you can verify the math independently.
    
    Input: [[1, 1, 1]]  (one sample, three equal counts)
    After pseudocount: [[1.5, 1.5, 1.5]]
    Geometric mean: 1.5  (all values equal)
    CLR: log(1.5 / 1.5) = log(1) = 0 for all features
    Expected output: [[0, 0, 0]]
    """
    counts = np.array([[1, 1, 1]])
    result = clr_transform(counts)
    expected = np.array([[0.0, 0.0, 0.0]])
    
    assert result.shape == expected.shape, \
        f"Shape mismatch: got {result.shape}, expected {expected.shape}"
    assert np.allclose(result, expected, atol=1e-10), \
        f"Values wrong: got {result}, expected {expected}"
    print("PASS: known answer (equal counts)")

def test_known_answer_two_values():
    """
    Input: [[0, 8]]  (one sample, two features)
    After pseudocount: [[0.5, 8.5]]
    log values: [log(0.5), log(8.5)]
    geometric mean of logs: (log(0.5) + log(8.5)) / 2
    geometric mean: exp of that = sqrt(0.5 * 8.5) = sqrt(4.25)
    CLR[0] = log(0.5 / sqrt(4.25))
    CLR[1] = log(8.5 / sqrt(4.25))
    Key check: CLR[0] + CLR[1] should equal 0 (they're negatives of each other)
    """
    counts = np.array([[0, 8]])
    result = clr_transform(counts)
    
    # Manually compute expected
    pseudo = np.array([[0.5, 8.5]])
    geom_mean = np.sqrt(0.5 * 8.5)  # geometric mean of two values
    expected = np.log(pseudo / geom_mean)
    
    assert np.allclose(result, expected, atol=1e-10), \
        f"Values wrong: got {result}, expected {expected}"
    # Also verify they sum to zero (symmetric property with 2 features)
    assert np.isclose(result[0, 0] + result[0, 1], 0.0, atol=1e-10), \
        "Two-feature CLR values should sum to zero"
    print("PASS: known answer (two values)")

test_known_answer()
test_known_answer_two_values()
```

---

### 2. Mathematical Property Tests (Catches Axis Errors)

These don't require knowing exact values — they test guaranteed properties of CLR.

```python
def test_zero_mean_property():
    """
    CLR MUST produce mean=0 across features for every sample.
    This is the defining property of the transformation.
    If this fails, the axis argument is wrong or the math is broken.
    """
    # Typical microbiome-like data: many zeros, skewed counts
    np.random.seed(42)
    counts = np.random.negative_binomial(n=5, p=0.3, size=(20, 50))
    
    result = clr_transform(counts)
    row_means = result.mean(axis=1)  # mean across features, per sample
    
    assert np.allclose(row_means, 0.0, atol=1e-10), \
        f"Row means should be 0, got: {row_means}"
    print(f"PASS: zero-mean property holds for {counts.shape} matrix")

def test_zero_mean_small():
    """Same test on small data you can inspect manually."""
    counts = np.array([
        [10, 20, 30, 40],
        [1,  1,  1,  1],
        [0,  0, 100, 0],
    ])
    result = clr_transform(counts)
    row_means = result.mean(axis=1)
    
    print("CLR output:\n", result)
    print("Row means (should all be ~0):", row_means)
    
    assert np.allclose(row_means, 0.0, atol=1e-10), \
        f"Row means not zero: {row_means}"
    print("PASS: zero-mean on small inspectable matrix")

def test_shape_preserved():
    """Output shape must match input shape."""
    counts = np.array([[5, 10, 15], [1, 2, 3]])
    result = clr_transform(counts)
    assert result.shape == counts.shape, \
        f"Shape changed: input {counts.shape}, output {result.shape}"
    print("PASS: shape preserved")

def test_relative_ordering():
    """
    Higher counts should produce higher CLR values within a sample.
    If [1, 10, 100] doesn't produce increasing CLR values, something is wrong.
    """
    counts = np.array([[1, 10, 100]])
    result = clr_transform(counts)
    
    assert result[0, 0] < result[0, 1] < result[0, 2], \
        f"Ordering not preserved: {result[0]}"
    print(f"PASS: ordering preserved. CLR values: {result[0]}")

test_zero_mean_property()
test_zero_mean_small()
test_shape_preserved()
test_relative_ordering()
```

---

### 3. Edge Case Tests

```python
def test_single_sample():
    """One sample should still work and produce mean-zero output."""
    counts = np.array([[5, 10, 15, 20]])
    result = clr_transform(counts)
    assert result.shape == (1, 4), f"Wrong shape: {result.shape}"
    assert np.isclose(result.mean(), 0.0, atol=1e-10), \
        f"Mean not zero: {result.mean()}"
    print("PASS: single sample")

def test_single_feature():
    """
    One feature is a degenerate case.
    CLR of a single feature must be 0 (value / geometric_mean = 1).
    Worth checking because axis handling gets weird with 1D data.
    """
    counts = np.array([[5], [10], [15]])
    result = clr_transform(counts)
    assert result.shape == (3, 1), f"Wrong shape: {result.shape}"
    assert np.allclose(result, 0.0, atol=1e-10), \
        f"Single feature CLR should be all zeros, got: {result}"
    print("PASS: single feature")

def test_all_zeros():
    """
    All-zero counts are common in microbiome data.
    Pseudocount saves us from log(0), so this should work.
    All values become 0.5 after pseudocount, so CLR should be all zeros.
    """
    counts = np.array([[0, 0, 0], [0, 0, 0]])
    result = clr_transform(counts)
    assert np.allclose(result, 0.0, atol=1e-10), \
        f"All-zero input should give all-zero CLR, got: {result}"
    print("PASS: all-zero input")

def test_large_values():
    """Large counts shouldn't cause overflow. Check for NaN/Inf."""
    counts = np.array([[1e6, 1e7, 1e8]])
    result = clr_transform(counts)
    assert not np.any(np.isnan(result)), "NaN in output with large values"
    assert not np.any(np.isinf(result)), "Inf in output with large values"
    assert np.isclose(result.mean(), 0.0, atol=1e-10), "Mean not zero"
    print(f"PASS: large values. CLR: {result}")

def test_identical_samples():
    """
    Two identical samples should produce identical CLR rows.
    Tests that samples are processed independently.
    """
    row = np.array([1, 5, 10, 50])
    counts = np.array([row, row])
    result = clr_transform(counts)
    assert np.allclose(result[0], result[1], atol=1e-10), \
        f"Identical samples gave different CLR:\n{result[0]}\n{result[1]}"
    print("PASS: identical samples produce identical CLR rows")

test_single_sample()
test_single_feature()
test_all_zeros()
test_large_values()
test_identical_samples()
```

---

### 4. Axis Confusion Detector (The Sneaky Bug)

This test is specifically designed to catch the most common mistake — computing the geometric mean down columns instead of across features.

```python
def test_axis_direction():
    """
    Explicitly designed to catch axis=0 vs axis=1 confusion.
    
    Use a matrix where samples have very different totals.
    If geometric mean is computed down columns (axis=0), the CLR values
    will be influenced by other samples — which is wrong.
    CLR must be computed independently per sample.
    """
    counts = np.array([
        [100, 100, 100],   # sample 1: high, equal counts
        [1,   1,   1],     # sample 2: low, equal counts
    ])
    result = clr_transform(counts)
    
    # Both samples have equal counts, so both should give all-zero CLR
    # If axis is wrong, sample 2's CLR will be skewed by sample 1's values
    assert np.allclose(result[0], 0.0, atol=1e-10), \
        f"Sample 1 (equal counts) should be all zeros: {result[0]}"
    assert np.allclose(result[1], 0.0, atol=1e-10), \
        f"Sample 2 (equal counts) should be all zeros: {result[1]}"
    print("PASS: axis direction correct (samples processed independently)")

def test_sample_independence():
    """
    Adding a new sample should not change CLR values of existing samples.
    This would fail if geometric mean is computed across samples.
    """
    counts_one = np.array([[1, 10, 100]])
    counts_two = np.array([[1, 10, 100], [999, 999, 999]])
    
    result_one = clr_transform(counts_one)
    result_two = clr_transform(counts_two)
    
    assert np.allclose(result_one[0], result_two[0], atol=1e-10), \
        (f"Adding a sample changed CLR values — geometric mean is being "
         f"computed across samples (axis=0 bug).\n"
         f"Single sample CLR: {result_one[0]}\n"
         f"Same sample in 2-row matrix: {result_two[0]}")
    print("PASS: sample independence (adding rows doesn't affect other rows)")

test_axis_direction()
test_sample_independence()
```

---

### 5. Run All Tests

```python
def run_all_tests():
    tests = [
        test_known_answer,
        test_known_answer_two_values,
        test_zero_mean_property,
        test_zero_mean_small,
        test_shape_preserved,
        test_relative_ordering,
        test_single_sample,
        test_single_feature,
        test_all_zeros,
        test_large_values,
        test_identical_samples,
        test_axis_direction,
        test_sample_independence,
    ]
    
    passed, failed = 0, 0
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"FAIL: {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"ERROR: {test.__name__}: {type(e).__name__}: {e}")
            failed += 1
    
    print(f"\n{'='*40}")
    print(f"Results: {passed} passed, {failed} failed")

run_all_tests()
```

---

## Manual Inspection Checklist

Run this and look at the output directly:

```python
def manual_inspection():
    counts = np.array([
        [1,   10,  100],   # increasing counts
        [50,  50,  50],    # equal counts → should give [0, 0, 0]
        [0,   0,   1000],  # sparse, one dominant feature
    ])
    result = clr_transform(counts)
    
    print("Input counts:")
    print(counts)
    print("\nCLR output:")
    print(result.round(4))
    print("\nRow means (must be ~0):", result.mean(axis=1).round(10))
    print("\nWhat to verify manually:")
    print("  Row 0: values should increase left to right")
    print("  Row 1: should be exactly [0, 0, 0]")
    print("  Row 2: last value should be large positive, first two negative")
    print("  All row means should print as 0.0")

manual_inspection()
```

**Expected output pattern:**
```
Row 0: negative, less-negative, positive  (e.g., [-1.5, 0.0, 1.5])
Row 1: [0.0, 0.0, 0.0]
Row 2: two negative values, one large positive
All row means: 0.0000000000
```

---

## Red Flags Summary

| Symptom | Likely Cause |
|---|---|
| Row means ≠ 0 | Geometric mean computed on wrong axis |
| Adding a row changes other rows' CLR | `axis=0` instead of `axis=1` |
| Equal-count sample ≠ all zeros | Math error in CLR formula |
| Output shape transposed | `keepdims` missing or wrong |
| NaN/Inf with large inputs | Overflow before log (not an issue here) |
| Single-feature output ≠ 0 | Pseudocount applied inconsistently |

The **zero-mean property** and **sample independence** tests are the two you should trust most — if those pass, the core logic is correct.
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
