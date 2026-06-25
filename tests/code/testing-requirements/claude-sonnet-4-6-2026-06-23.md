# Test Results: code/testing-requirements.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-23.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** code/testing-requirements.md
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
# CLR Transformation Testing Strategy

## Understanding What We're Actually Testing

Before writing tests, let's clarify the math so we know what "correct" means:

**CLR formula:** `clr(x_i) = log(x_i / g(x))` where `g(x)` is the geometric mean of the composition

**Key mathematical property:** The CLR values for each sample must sum to zero (equivalently, mean = 0), because:
`sum(log(x_i / g(x))) = sum(log(x_i)) - n * log(g(x)) = n*log(g(x)) - n*log(g(x)) = 0`

This zero-sum property is the primary correctness check.

---

## Potential Issues to Watch For

Looking at the code before writing tests:

```python
# POTENTIAL ISSUE: geometric mean is computed in log space, then exponentiated,
# then used in a ratio, then log'd again. This is mathematically equivalent but
# worth verifying the roundtrip doesn't accumulate floating point error.

geometric_mean = np.exp(log_counts.mean(axis=1, keepdims=True))  # exp(mean(log(x)))
clr = np.log(counts_pseudo / geometric_mean)                      # log(x / exp(mean(log(x))))

# This equals: log(x) - mean(log(x))  -- a simpler form we can use to cross-check
```

---

## Test Suite

```python
import numpy as np

def clr_transform(counts):
    """Original code under test - unchanged."""
    counts_pseudo = counts + 0.5
    log_counts = np.log(counts_pseudo)
    geometric_mean = np.exp(log_counts.mean(axis=1, keepdims=True))
    clr = np.log(counts_pseudo / geometric_mean)
    return clr


# ============================================================
# HELPER: reference implementation using simpler formula
# Use this to cross-check the original, not as ground truth
# ============================================================

def clr_reference(counts):
    """
    Simpler CLR implementation: log(x) - mean(log(x))
    Mathematically identical but computed differently.
    If both agree, floating point errors are unlikely.
    """
    counts_pseudo = counts + 0.5
    log_counts = np.log(counts_pseudo)
    clr = log_counts - log_counts.mean(axis=1, keepdims=True)
    return clr


# ============================================================
# TEST 1: Core mathematical property — rows must sum to zero
# This is the most important test. If this fails, nothing else matters.
# ============================================================

def test_zero_sum_property():
    """CLR values must sum to zero across features for each sample."""
    
    # Typical microbiome-like data: sparse, integer counts, varying totals
    counts = np.array([
        [10,  20,  30,  40],   # sample 1: moderate counts
        [100,  1,   1,   1],   # sample 2: one dominant taxon
        [5,    5,   5,   5],   # sample 3: perfectly even
        [0,    0,   0, 100],   # sample 4: mostly zeros (stresses pseudocount)
    ], dtype=float)
    
    result = clr_transform(counts)
    row_sums = result.sum(axis=1)
    
    print("Row sums (should all be ~0.0):")
    for i, s in enumerate(row_sums):
        print(f"  Sample {i+1}: {s:.2e}")
    
    # Allow small floating point tolerance
    assert np.allclose(row_sums, 0, atol=1e-10), \
        f"Row sums not zero: {row_sums}"
    
    print("PASSED: zero-sum property\n")

test_zero_sum_property()


# ============================================================
# TEST 2: Known-answer test — manually computed expected values
# This catches wrong axis, wrong pseudocount application, etc.
# ============================================================

def test_known_answer():
    """
    Verify against hand-calculated values for a simple case.
    
    For counts = [[1, 1, 1]], with pseudocount 0.5:
      values become [1.5, 1.5, 1.5]
      log values:   [log(1.5), log(1.5), log(1.5)]
      geometric mean = exp(mean of logs) = 1.5
      CLR = log(1.5 / 1.5) = log(1) = 0 for all features
    """
    counts = np.array([[1, 1, 1]], dtype=float)
    result = clr_transform(counts)
    
    expected = np.array([[0.0, 0.0, 0.0]])
    
    print(f"Known answer test (uniform counts):")
    print(f"  Result:   {result}")
    print(f"  Expected: {expected}")
    
    assert np.allclose(result, expected, atol=1e-10), \
        f"Expected all zeros for uniform counts, got {result}"
    
    print("PASSED: known answer (uniform)\n")

    # ---- Second known answer: two features, one twice the other ----
    # counts = [[1, 3]], pseudocount -> [1.5, 3.5]
    # log values: [log(1.5), log(3.5)]
    # mean of logs: (log(1.5) + log(3.5)) / 2 = log(sqrt(1.5 * 3.5))
    # CLR[0] = log(1.5) - mean = log(1.5/sqrt(5.25))
    # CLR[1] = log(3.5) - mean = log(3.5/sqrt(5.25))
    
    counts2 = np.array([[1, 3]], dtype=float)
    result2 = clr_transform(counts2)
    
    geom_mean = np.sqrt(1.5 * 3.5)  # geometric mean of [1.5, 3.5]
    expected2 = np.array([[np.log(1.5 / geom_mean), np.log(3.5 / geom_mean)]])
    
    print(f"Known answer test (unequal counts):")
    print(f"  Result:   {result2}")
    print(f"  Expected: {expected2}")
    
    assert np.allclose(result2, expected2, atol=1e-10), \
        f"Mismatch: got {result2}, expected {expected2}"
    
    print("PASSED: known answer (unequal)\n")

test_known_answer()


# ============================================================
# TEST 3: Cross-check against reference implementation
# If both implementations agree, the logic is likely correct.
# ============================================================

def test_matches_reference_implementation():
    """Both implementations should give identical results."""
    
    np.random.seed(42)
    # Realistic microbiome data: many zeros, some high counts
    counts = np.random.negative_binomial(n=5, p=0.3, size=(20, 50)).astype(float)
    
    result_original  = clr_transform(counts)
    result_reference = clr_reference(counts)
    
    max_diff = np.abs(result_original - result_reference).max()
    print(f"Max difference between implementations: {max_diff:.2e}")
    
    assert np.allclose(result_original, result_reference, atol=1e-10), \
        f"Implementations disagree. Max diff: {max_diff}"
    
    print("PASSED: matches reference implementation\n")

test_matches_reference_implementation()


# ============================================================
# TEST 4: Axis orientation — are we normalizing samples or features?
# This is a common, silent bug. CLR should normalize WITHIN each sample.
# ============================================================

def test_correct_axis():
    """
    Verify transformation is applied per-sample (row), not per-feature (column).
    
    Strategy: create data where row-wise and column-wise results differ,
    then check which one gives zero row sums.
    """
    # Two samples with very different total counts
    counts = np.array([
        [10, 20, 30],   # sample 1: low counts
        [100, 200, 300] # sample 2: 10x higher, same composition
    ], dtype=float)
    
    result = clr_transform(counts)
    
    row_sums = result.sum(axis=1)
    col_sums = result.sum(axis=0)
    
    print(f"Axis test:")
    print(f"  Row sums (should be ~0): {row_sums}")
    print(f"  Col sums (should NOT all be 0): {col_sums}")
    
    # Rows must sum to zero
    assert np.allclose(row_sums, 0, atol=1e-10), \
        "Row sums not zero — transformation may be applied to wrong axis"
    
    # Columns should NOT all sum to zero (if they do, axis is wrong)
    # Note: col sums could coincidentally be zero, so this is a soft check
    print(f"  (Column sums being non-zero confirms row-wise normalization)")
    
    # Stronger check: same composition should give same CLR values
    # Samples above have identical composition, so CLR should be identical
    assert np.allclose(result[0], result[1], atol=1e-10), \
        f"Same composition gave different CLR values: {result[0]} vs {result[1]}"
    
    print("PASSED: correct axis\n")

test_correct_axis()


# ============================================================
# TEST 5: Pseudocount behavior — zeros should not cause crashes or -inf
# ============================================================

def test_zero_handling():
    """Pseudocount should prevent log(0) issues."""
    
    # All zeros in a sample
    counts_all_zero = np.array([[0, 0, 0, 0]], dtype=float)
    
    # One zero among nonzero values
    counts_one_zero = np.array([[0, 5, 10, 20]], dtype=float)
    
    # All zeros matrix
    counts_zero_matrix = np.zeros((5, 10))
    
    for name, counts in [("all-zero sample", counts_all_zero),
                          ("one zero", counts_one_zero),
                          ("zero matrix", counts_zero_matrix)]:
        result = clr_transform(counts)
        
        has_inf = np.any(np.isinf(result))
        has_nan = np.any(np.isnan(result))
        row_sums_ok = np.allclose(result.sum(axis=1), 0, atol=1e-10)
        
        print(f"Zero handling ({name}):")
        print(f"  Result: {result}")
        print(f"  Has inf: {has_inf}, Has nan: {has_nan}, Row sums ~0: {row_sums_ok}")
        
        assert not has_inf, f"Infinite values in output for {name}"
        assert not has_nan, f"NaN values in output for {name}"
        assert row_sums_ok, f"Row sums not zero for {name}"
    
    print("PASSED: zero handling\n")

test_zero_handling()


# ============================================================
# TEST 6: Scale invariance — CLR should be invariant to sample depth
# This is a key biological property: doubling all counts shouldn't change CLR
# ============================================================

def test_scale_invariance():
    """
    CLR should be identical for samples with same composition but different depths.
    
    NOTE: This is only approximately true with pseudocounts — the pseudocount
    breaks exact scale invariance. This test reveals that limitation.
    """
    counts_low  = np.array([[10,  20,  30,  40]], dtype=float)
    counts_high = np.array([[100, 200, 300, 400]], dtype=float)  # 10x deeper
    
    result_low  = clr_transform(counts_low)
    result_high = clr_transform(counts_high)
    
    max_diff = np.abs(result_low - result_high).max()
    
    print(f"Scale invariance test:")
    print(f"  Low depth CLR:  {result_low.round(4)}")
    print(f"  High depth CLR: {result_high.round(4)}")
    print(f"  Max difference: {max_diff:.4f}")
    
    if max_diff < 0.01:
        print("  Results are nearly identical (pseudocount effect is small)")
    else:
        print(f"  WARNING: Pseudocount causes {max_diff:.4f} difference between depths.")
        print(f"  This is expected behavior, not a bug, but worth knowing.")
        print(f"  Consider whether pseudocount = 0.5 is appropriate for your data.")
    
    # This is informational — we don't assert equality here
    # because pseudocounts intentionally break exact scale invariance
    print("INFO: scale invariance check complete (see warning above if any)\n")

test_scale_invariance()


# ============================================================
# TEST 7: Output shape and dtype sanity checks
# ============================================================

def test_output_properties():
    """Output shape should match input; values should be finite reals."""
    
    test_cases = [
        ("single sample",    np.array([[1, 2, 3, 4]], dtype=float)),
        ("single feature",   np.array([[5], [10], [15]], dtype=float)),
        ("square matrix",    np.random.randint(1, 100, (10, 10)).astype(float)),
        ("tall matrix",      np.random.randint(1, 100, (100, 5)).astype(float)),
        ("wide matrix",      np.random.randint(1, 100, (5, 100)).astype(float)),
    ]
    
    for name, counts in test_cases:
        result = clr_transform(counts)
        
        assert result.shape == counts.shape, \
            f"{name}: shape mismatch. Input {counts.shape}, output {result.shape}"
        assert np.all(np.isfinite(result)), \
            f"{name}: non-finite values in output"
        assert np.allclose(result.sum(axis=1), 0, atol=1e-10), \
            f"{name}: row sums not zero"
        
        print(f"PASSED: output properties ({name})")
    
    print()

test_output_properties()


# ============================================================
# SUMMARY: Run all tests and report
# ============================================================

def run_all_tests():
    tests = [
        test_zero_sum_property,
        test_known_answer,
        test_matches_reference_implementation,
        test_correct_axis,
        test_zero_handling,
        test_scale_invariance,
        test_output_properties,
    ]
    
    passed, failed = 0, []
    
    print("=" * 60)
    print("CLR TRANSFORM TEST SUITE")
    print("=" * 60 + "\n")
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            failed.append((test.__name__, str(e)))
            print(f"FAILED: {test.__name__}: {e}\n")
    
    print("=" * 60)
    print(f"Results: {passed}/{len(tests)} passed")
    if failed:
        print("Failed tests:")
        for name, msg in failed:
            print(f"  - {name}: {msg}")
    else:
        print("All tests passed.")
    print("=" * 60)

run_all_tests()
```

---

## Manual Inspection Checklist

After running the tests, visually verify these on your real data:

```python
# Run this on a small slice of your actual data
sample_data = your_real_counts[:5, :10]  # first 5 samples, 10 features
result = clr_transform(sample_data)

print("Input counts (first 5 samples, 10 features):")
print(sample
```

## Overall Assessment
- **Recommendation:** Pass
- **Notes:**
## Verification Steps Tested
_Which verification requirements from the prompt were checked, and results._
