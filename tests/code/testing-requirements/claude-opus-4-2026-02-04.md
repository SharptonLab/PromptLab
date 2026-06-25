# Test Results: testing-requirements.md

## Test Metadata
- **Prompt:** code/testing-requirements.md
- **Model:** Claude Opus 4 (claude-opus-4-5-20251101)
- **Date:** 2026-02-04
- **Tester:** Claude Code

## Test Input Used

Standard test input from prompt file:

```
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

## Filled Prompt

```
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
```

## Model Output

### 1. Test Cases

#### Normal/expected inputs
- **Typical microbiome data**: Matrix with varying counts, some zeros, realistic range (0-10000)
- **Multiple samples**: Verify it works across rows, not just single samples
- **Different matrix sizes**: 10x50, 50x100, 100x500

#### Edge cases
- **All-zero row**: What happens when a sample has all zeros? (After pseudocount, should work)
- **Single value per row**: 1x5 matrix (one sample, five features)
- **Single feature per sample**: 5x1 matrix (five samples, one feature—CLR is undefined here, row mean = that value)
- **Very large values**: Counts in millions (numerical stability)
- **Very small values**: Counts near zero

#### Known-answer tests
- **Hand-calculable example**: 2x3 matrix where we can compute expected CLR manually
- **Uniform row**: Row with all equal values should give all-zero CLR (since each value equals the geometric mean)
- **Mathematical property**: Row means of CLR output should be exactly 0

#### Boundary conditions
- **Zero counts**: Verify pseudocount handles zeros correctly
- **Negative values**: Should this error? (Counts shouldn't be negative)
- **Integer vs float input**: Does it handle both?

### 2. Test Code

```python
import numpy as np

def clr_transform(counts):
    """Apply centered log-ratio transformation to count data."""
    counts_pseudo = counts + 0.5
    log_counts = np.log(counts_pseudo)
    geometric_mean = np.exp(log_counts.mean(axis=1, keepdims=True))
    clr = np.log(counts_pseudo / geometric_mean)
    return clr

# =============================================================================
# Test 1: Known-answer test with simple hand-calculable values
# =============================================================================
# Use values where we can calculate expected CLR by hand
#
# Sample: [2, 8] (before pseudocount)
# With pseudocount: [2.5, 8.5]
# Geometric mean = sqrt(2.5 * 8.5) = sqrt(21.25) = 4.6098...
# CLR = [log(2.5/4.6098), log(8.5/4.6098)]
#     = [log(0.5423), log(1.8437)]
#     = [-0.6120, 0.6120]
# Note: These should sum to 0 (and mean to 0)

test_1 = np.array([[2, 8]])
result_1 = clr_transform(test_1)

# Calculate expected values
counts_with_pseudo = np.array([[2.5, 8.5]])
geo_mean = np.sqrt(2.5 * 8.5)  # = 4.6098
expected_1 = np.array([[np.log(2.5/geo_mean), np.log(8.5/geo_mean)]])

print("Test 1: Known-answer test")
print(f"  Input: {test_1}")
print(f"  Result: {result_1}")
print(f"  Expected: {expected_1}")
assert np.allclose(result_1, expected_1), "Known-answer test failed!"
print("  PASSED\n")

# =============================================================================
# Test 2: Row means should be exactly 0 (key CLR property)
# =============================================================================
# This is the defining property of CLR: centering removes the mean
# Test with various inputs

test_inputs = [
    np.array([[1, 2, 3, 4, 5]]),           # Simple sequence
    np.array([[10, 20, 30], [5, 5, 5]]),   # Multiple rows
    np.array([[0, 0, 100, 0, 0]]),         # Mostly zeros
    np.array([[1, 1000, 1, 1000, 1]]),     # High variance
    np.random.randint(0, 1000, (10, 50))   # Random realistic data
]

print("Test 2: Row means should be 0")
for i, test_data in enumerate(test_inputs):
    result = clr_transform(test_data)
    row_means = result.mean(axis=1)

    # Row means should be essentially 0 (within floating point tolerance)
    max_deviation = np.abs(row_means).max()
    passed = max_deviation < 1e-10

    print(f"  Input shape {test_data.shape}: max row mean deviation = {max_deviation:.2e} {'PASSED' if passed else 'FAILED'}")
    assert passed, f"Row means not zero for input {i}!"
print()

# =============================================================================
# Test 3: Uniform values should give all-zero CLR
# =============================================================================
# If all values in a row are equal, each equals the geometric mean
# So log(value/geomean) = log(1) = 0

test_3 = np.array([
    [5, 5, 5, 5],
    [100, 100, 100, 100],
    [0, 0, 0, 0]  # After pseudocount: [0.5, 0.5, 0.5, 0.5]
])
result_3 = clr_transform(test_3)
expected_3 = np.zeros_like(result_3)

print("Test 3: Uniform values should give all-zero CLR")
print(f"  Input:\n{test_3}")
print(f"  Result:\n{result_3}")
assert np.allclose(result_3, expected_3), "Uniform values test failed!"
print("  PASSED\n")

# =============================================================================
# Test 4: Zero handling (pseudocount)
# =============================================================================
# Zeros should not cause errors or produce inf/nan

test_4 = np.array([
    [0, 0, 0, 100],
    [0, 50, 50, 0],
    [1, 0, 0, 0]
])
result_4 = clr_transform(test_4)

print("Test 4: Zero handling")
print(f"  Input:\n{test_4}")
print(f"  Result:\n{result_4}")
assert not np.any(np.isnan(result_4)), "NaN values in output!"
assert not np.any(np.isinf(result_4)), "Inf values in output!"
print("  No NaN or Inf values: PASSED\n")

# =============================================================================
# Test 5: Output shape matches input shape
# =============================================================================
shapes_to_test = [(1, 10), (10, 1), (5, 5), (100, 500)]

print("Test 5: Output shape preservation")
for shape in shapes_to_test:
    test_data = np.random.randint(0, 100, shape)
    result = clr_transform(test_data)
    assert result.shape == shape, f"Shape mismatch: expected {shape}, got {result.shape}"
    print(f"  Shape {shape}: PASSED")
print()

# =============================================================================
# Test 6: Numerical stability with extreme values
# =============================================================================
print("Test 6: Numerical stability")

# Very large values
large_values = np.array([[1e6, 1e7, 1e8]])
result_large = clr_transform(large_values)
assert not np.any(np.isnan(result_large)), "NaN with large values!"
assert not np.any(np.isinf(result_large)), "Inf with large values!"
assert np.allclose(result_large.mean(axis=1), 0), "Row mean not 0 with large values!"
print(f"  Large values (1e6-1e8): PASSED")

# Very small non-zero values
small_values = np.array([[0.001, 0.002, 0.003]])
result_small = clr_transform(small_values)
assert not np.any(np.isnan(result_small)), "NaN with small values!"
assert not np.any(np.isinf(result_small)), "Inf with small values!"
assert np.allclose(result_small.mean(axis=1), 0), "Row mean not 0 with small values!"
print(f"  Small values (0.001-0.003): PASSED")
print()

# =============================================================================
# Test 7: Cross-check with manual calculation (different approach)
# =============================================================================
# Alternative CLR formula: clr_i = log(x_i) - mean(log(x))
# This should give the same result

def clr_alternative(counts):
    """Alternative CLR implementation for verification."""
    counts_pseudo = counts + 0.5
    log_counts = np.log(counts_pseudo)
    clr = log_counts - log_counts.mean(axis=1, keepdims=True)
    return clr

test_7 = np.random.randint(0, 1000, (20, 100))
result_original = clr_transform(test_7)
result_alternative = clr_alternative(test_7)

print("Test 7: Cross-check with alternative formula")
print(f"  Max difference between implementations: {np.abs(result_original - result_alternative).max():.2e}")
assert np.allclose(result_original, result_alternative), "Implementations don't match!"
print("  PASSED\n")

# =============================================================================
# Test 8: Integer vs float input
# =============================================================================
print("Test 8: Integer vs float input")

int_input = np.array([[1, 2, 3, 4]], dtype=np.int64)
float_input = np.array([[1.0, 2.0, 3.0, 4.0]], dtype=np.float64)

result_int = clr_transform(int_input)
result_float = clr_transform(float_input)

assert np.allclose(result_int, result_float), "Integer and float inputs give different results!"
print("  Results match for int and float input: PASSED\n")

# =============================================================================
# Summary
# =============================================================================
print("=" * 50)
print("ALL TESTS PASSED")
print("=" * 50)
```

### 3. Validation Checks

After running the tests above, manually inspect the following:

**1. Spot-check a row from real data:**
```python
# Take one row from your actual data
sample_row = your_data[0:1, :]  # First sample
result = clr_transform(sample_row)

# Manually verify:
# a) No NaN or Inf values
print("Any NaN?", np.any(np.isnan(result)))
print("Any Inf?", np.any(np.isinf(result)))

# b) Row mean is ~0
print("Row mean:", result.mean())

# c) Values are reasonable (typically between -10 and +10 for microbiome data)
print("Value range:", result.min(), "to", result.max())
```

**2. Check the distribution makes sense:**
```python
import matplotlib.pyplot as plt

# Original counts (log-transformed for visualization)
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.hist(np.log1p(your_data.flatten()), bins=50)
plt.title("Original data (log1p)")
plt.xlabel("log(count + 1)")

plt.subplot(1, 2, 2)
clr_result = clr_transform(your_data)
plt.hist(clr_result.flatten(), bins=50)
plt.title("CLR-transformed")
plt.xlabel("CLR value")

plt.tight_layout()
plt.show()

# CLR should be roughly symmetric around 0
```

**3. Verify relative relationships are preserved:**
```python
# If taxon A has higher counts than taxon B in a sample,
# taxon A should have higher CLR value than taxon B (in that sample)

sample_idx = 0
original = your_data[sample_idx, :]
transformed = clr_transform(your_data[sample_idx:sample_idx+1, :])[0]

# Check a few pairs
for i in range(min(5, len(original)-1)):
    if original[i] > original[i+1]:
        assert transformed[i] > transformed[i+1], f"Ordering violated at position {i}"
    elif original[i] < original[i+1]:
        assert transformed[i] < transformed[i+1], f"Ordering violated at position {i}"
    # Equal values should remain equal (both become 0 relative to each other)

print("Relative ordering preserved: PASSED")
```

**4. Compare to established implementation:**
```python
# If you have scikit-bio or another package with CLR
try:
    from skbio.stats.composition import clr as skbio_clr

    # skbio requires positive values, so add pseudocount manually
    test_data = your_data + 0.5

    # Note: skbio may handle rows/columns differently; check orientation
    skbio_result = skbio_clr(test_data)
    our_result = clr_transform(your_data)

    print("Max difference from skbio:", np.abs(skbio_result - our_result).max())
except ImportError:
    print("skbio not installed; skip cross-validation")
```

### 4. Red Flags

These patterns indicate something is wrong with the CLR implementation:

**Critical errors (code is definitely broken):**
- **NaN values**: Should never occur with valid input (pseudocount prevents log(0))
- **Inf values**: Should never occur
- **Row means ≠ 0**: The defining property of CLR; if this fails, the implementation is wrong
- **Output shape differs from input**: Transformation should preserve dimensions

**Likely errors (investigate further):**
- **All values identical across samples**: Suggests the function is collapsing variation somehow
- **All values in a column are identical**: Might indicate column-wise operation when row-wise was intended
- **Values outside expected range**: CLR values typically range from about -15 to +15 for microbiome data; extreme values (>50 or <-50) suggest numerical issues
- **Negative values where originals were equal**: If two features had identical counts in a sample, their CLR values should be equal (not one positive and one negative)

**Subtle errors (harder to catch):**
- **Wrong axis**: Operating on columns instead of rows (or vice versa). The row-mean-equals-zero test catches this
- **Pseudocount applied incorrectly**: Should be added once before all log operations. If applied multiple times or inconsistently, answers will be slightly wrong
- **Wrong log base**: Using log10 instead of natural log would give different scales (but row means would still be 0, so this is hard to catch without known-answer tests)

**How to detect axis confusion:**
```python
# If confused about rows vs columns:
test = np.array([
    [1, 2, 3],      # Row 0
    [10, 20, 30]    # Row 1
])
result = clr_transform(test)

# Row means should be 0
print("Row means:", result.mean(axis=1))  # Should be [0, 0]

# Column means should NOT necessarily be 0
print("Column means:", result.mean(axis=0))  # Probably not [0, 0, 0]

# If column means are 0 but row means aren't, the axis is wrong
```

## Overall Assessment

- **Recommendation:** Pass
- **Notes:** The test strategy effectively covers the mathematical properties of CLR (row means = 0, uniform inputs produce zeros). The cross-check with an alternative formula (Test 7) is particularly valuable as it verifies the implementation against a mathematically equivalent but independently coded approach. The red flags section provides practical guidance for identifying common bugs. The known-answer test (Test 1) values can be verified by hand calculation.

## Verification Steps Tested

1. **Known-answer test values can be verified by hand calculation:** Verified
   - Test 1 shows explicit hand calculation: sqrt(2.5 * 8.5) = 4.6098
   - CLR values derived step by step
   - Can be verified with a calculator

2. **Tests cover the key mathematical properties of CLR:** Verified
   - Row means equal zero (Test 2)
   - Uniform values produce all zeros (Test 3)
   - Cross-check with alternative formula (Test 7)

3. **Edge cases relevant to microbiome data:** Verified
   - Zero handling with pseudocount (Test 4)
   - Sparse data with mostly zeros (Test 2, input 3)
   - Large count values for numerical stability (Test 6)
   - Integer vs float input (Test 8)
