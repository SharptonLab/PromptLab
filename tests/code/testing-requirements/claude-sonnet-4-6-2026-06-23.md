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

Context: I have Python code for normalizing microbiome count data using centered log-ratio (CLR) transformation. I need to verify it produces correct results before using it for my research.

The code to test:
```

## Model Output
```
# Testing CLR Transformation Code for Microbiome Data

I'll help you verify your CLR transformation implementation. First, please share your code — but in the meantime, let me provide a **comprehensive testing framework** you can apply to it.

---

## What CLR Transformation Should Do

For a composition **x** = [x₁, x₂, ..., xₙ]:

```
CLR(x) = [log(x₁/g(x)), log(x₂/g(x)), ..., log(xₙ/g(x))]
```

Where **g(x)** is the geometric mean of all components.

**Key mathematical properties to verify:**
1. CLR values sum to zero (per sample)
2. Scale invariance (multiplying counts by constant → same CLR)
3. Zeros must be handled (CLR is undefined for zeros)
4. Relative differences between features are preserved

---

## Complete Test Suite

```python
import numpy as np
import pandas as pd
import pytest
from scipy.stats import pearsonr

# ============================================================
# PASTE YOUR FUNCTION HERE FOR TESTING
# ============================================================
# Example: from your_module import clr_transform
# Or define it here temporarily

def clr_transform_reference(counts):
    """
    Reference implementation for comparison.
    Assumes counts is a 2D array: rows=samples, cols=features.
    Zeros replaced with small pseudocount before transformation.
    """
    counts = np.array(counts, dtype=float)
    
    # Replace zeros with pseudocount (common approach)
    counts[counts == 0] = 0.5
    
    # Log transform
    log_counts = np.log(counts)
    
    # Subtract geometric mean (= mean of logs) per sample
    geometric_mean_log = log_counts.mean(axis=1, keepdims=True)
    
    return log_counts - geometric_mean_log


# ============================================================
# TEST 1: MATHEMATICAL PROPERTIES
# ============================================================

class TestCLRMathematicalProperties:
    """Verify fundamental mathematical properties of CLR."""
    
    def test_row_sums_to_zero(self, your_clr_function=clr_transform_reference):
        """CLR values must sum to zero for each sample."""
        counts = np.array([
            [10, 20, 30, 40],
            [100, 200, 50, 150],
            [5, 5, 5, 5],        # uniform → all CLR should be 0
        ])
        
        result = your_clr_function(counts)
        row_sums = result.sum(axis=1)
        
        print(f"Row sums (should be ~0): {row_sums}")
        assert np.allclose(row_sums, 0, atol=1e-10), \
            f"CLR rows do not sum to zero: {row_sums}"
        print("✓ PASSED: All rows sum to zero")
    
    def test_uniform_composition_gives_zero(self, your_clr_function=clr_transform_reference):
        """Uniform composition should give all-zero CLR values."""
        uniform = np.array([[5, 5, 5, 5],
                            [100, 100, 100, 100]])  # same composition, different scale
        
        result = your_clr_function(uniform)
        
        print(f"CLR of uniform composition:\n{result}")
        assert np.allclose(result, 0, atol=1e-10), \
            f"Uniform composition should give zero CLR, got:\n{result}"
        print("✓ PASSED: Uniform composition gives zero CLR")
    
    def test_scale_invariance(self, your_clr_function=clr_transform_reference):
        """
        CLR should be identical for same composition at different scales.
        [10, 20, 30] and [100, 200, 300] represent same composition.
        """
        counts_original = np.array([[10, 20, 30, 40]])
        counts_scaled   = np.array([[100, 200, 300, 400]])  # 10x scale
        
        result_original = your_clr_function(counts_original)
        result_scaled   = your_clr_function(counts_scaled)
        
        print(f"Original CLR: {result_original}")
        print(f"Scaled CLR:   {result_scaled}")
        assert np.allclose(result_original, result_scaled, atol=1e-10), \
            "CLR is not scale invariant!"
        print("✓ PASSED: Scale invariance holds")
    
    def test_output_shape(self, your_clr_function=clr_transform_reference):
        """Output shape must match input shape."""
        counts = np.random.randint(1, 100, size=(20, 50))  # 20 samples, 50 features
        result = your_clr_function(counts)
        
        assert result.shape == counts.shape, \
            f"Shape mismatch: input {counts.shape}, output {result.shape}"
        print(f"✓ PASSED: Output shape {result.shape} matches input shape")
    
    def test_known_values(self, your_clr_function=clr_transform_reference):
        """
        Manually computed example.
        counts = [1, 2, 4]
        geometric mean = (1*2*4)^(1/3) = 8^(1/3) = 2
        CLR = [log(1/2), log(2/2), log(4/2)]
            = [log(0.5), log(1), log(2)]
            = [-0.6931, 0, 0.6931]
        """
        counts = np.array([[1, 2, 4]])
        expected = np.array([[-np.log(2), 0, np.log(2)]])
        
        result = your_clr_function(counts)
        
        print(f"Expected: {expected}")
        print(f"Got:      {result}")
        assert np.allclose(result, expected, atol=1e-6), \
            f"Known value test failed!\nExpected: {expected}\nGot: {result}"
        print("✓ PASSED: Known values match")


# ============================================================
# TEST 2: ZERO HANDLING
# ============================================================

class TestZeroHandling:
    """Zeros are common in microbiome data — must be handled explicitly."""
    
    def test_zeros_dont_crash(self, your_clr_function=clr_transform_reference):
        """Function should not crash or return NaN/Inf with zero counts."""
        counts_with_zeros = np.array([
            [0, 10, 20, 30],
            [5, 0, 0, 15],
            [0, 0, 0, 100],   # extreme case
        ])
        
        try:
            result = your_clr_function(counts_with_zeros)
            has_nan = np.any(np.isnan(result))
            has_inf = np.any(np.isinf(result))
            
            print(f"Result with zeros:\n{result}")
            print(f"Contains NaN: {has_nan}")
            print(f"Contains Inf: {has_inf}")
            
            assert not has_nan, "Result contains NaN values!"
            assert not has_inf, "Result contains Inf values!"
            print("✓ PASSED: Zeros handled without NaN/Inf")
            
        except Exception as e:
            print(f"✗ FAILED: Function crashed with zeros: {e}")
            raise
    
    def test_all_zero_sample_behavior(self, your_clr_function=clr_transform_reference):
        """Document behavior for all-zero sample (empty sample)."""
        all_zero_sample = np.array([[0, 0, 0, 0]])
        
        try:
            result = your_clr_function(all_zero_sample)
            print(f"⚠ WARNING: All-zero sample returned: {result}")
            print("  Verify this behavior is intentional for your use case")
        except Exception as e:
            print(f"⚠ WARNING: All-zero sample raises exception: {e}")
            print("  Consider whether your data can contain empty samples")
    
    def test_pseudocount_consistency(self, your_clr_function=clr_transform_reference):
        """
        If using pseudocounts, verify they're applied consistently.
        The same pseudocount should be used for ALL zeros.
        """
        # Two samples with zeros in different positions
        counts = np.array([
            [0, 10, 20],
            [10, 0, 20],
        ])
        
        result = your_clr_function(counts)
        
        # By symmetry, CLR[0, feature_0] should equal CLR[1, feature_1]
        # (both are the "zero" feature with same pseudocount)
        print(f"CLR of zero-containing samples:\n{result}")
        print(f"CLR[0,0] = {result[0,0]:.4f} (zero in sample 0)")
        print(f"CLR[1,1] = {result[1,1]:.4f} (zero in sample 1)")
        
        # These won't be exactly equal (different compositions) but
        # flagging for manual inspection
        print("  → Inspect these values to confirm pseudocount logic is consistent")


# ============================================================
# TEST 3: BIOLOGICAL VALIDITY
# ============================================================

class TestBiologicalValidity:
    """Verify behavior makes sense for microbiome research context."""
    
    def test_dominant_taxon_has_positive_clr(self, your_clr_function=clr_transform_reference):
        """
        A taxon with higher-than-average relative abundance
        should have positive CLR value.
        """
        # Feature 0 is clearly dominant
        counts = np.array([[1000, 10, 10, 10]])
        result = your_clr_function(counts)
        
        print(f"Dominant taxon CLR: {result[0, 0]:.4f} (should be positive)")
        print(f"Rare taxon CLR:     {result[0, 1]:.4f} (should be negative)")
        
        assert result[0, 0] > 0, "Dominant taxon should have positive CLR"
        assert result[0, 1] < 0, "Rare taxon should have negative CLR"
        print("✓ PASSED: Dominant/rare taxa have correct CLR sign")
    
    def test_relative_ordering_preserved(self, your_clr_function=clr_transform_reference):
        """
        If taxon A is more abundant than taxon B,
        CLR(A) should be greater than CLR(B).
        """
        counts = np.array([[5, 20, 10, 80, 1]])  # known ordering: 4>1>2>0>3... wait
        # Ordering by abundance: index 3(80) > 1(20) > 2(10) > 0(5) > 4(1)
        
        result = your_clr_function(counts)
        clr_values = result[0]
        
        print(f"Counts:     {counts[0]}")
        print(f"CLR values: {np.round(clr_values, 4)}")
        
        # Check ordering is preserved
        count_order = np.argsort(counts[0])
        clr_order   = np.argsort(clr_values)
        
        assert np.array_equal(count_order, clr_order), \
            f"Relative ordering not preserved!\nCount order: {count_order}\nCLR order: {clr_order}"
        print("✓ PASSED: Relative ordering preserved")
    
    def test_two_samples_same_composition(self, your_clr_function=clr_transform_reference):
        """
        Two samples with identical relative composition but different
        total counts should have identical CLR profiles.
        """
        sample_a = np.array([[10, 20, 30, 40]])    # total = 100
        sample_b = np.array([[100, 200, 300, 400]]) # total = 1000, same composition
        
        clr_a = your_clr_function(sample_a)
        clr_b = your_clr_function(sample_b)
        
        print(f"CLR sample A: {np.round(clr_a, 6)}")
        print(f"CLR sample B: {np.round(clr_b, 6)}")
        
        assert np.allclose(clr_a, clr_b, atol=1e-10), \
            "Same composition at different depths should give identical CLR!"
        print("✓ PASSED: Same composition → same CLR regardless of depth")


# ============================================================
# TEST 4: EDGE CASES
# ============================================================

class TestEdgeCases:
    
    def test_single_sample(self, your_clr_function=clr_transform_reference):
        """Should work with just one sample."""
        single = np.array([[10, 20, 30]])
        result = your_clr_function(single)
        assert result.shape == (1, 3)
        assert np.isclose(result.sum(), 0, atol=1e-10)
        print(f"✓ PASSED: Single sample → {result}")
    
    def test_single_feature(self, your_clr_function=clr_transform_reference):
        """Single feature: CLR should be 0 (only one component)."""
        single_feature = np.array([[42], [100], [7]])
        result = your_clr_function(single_feature)
        
        print(f"Single feature CLR: {result} (should be all zeros)")
        assert np.allclose(result, 0, atol=1e-10), \
            "Single feature CLR should be zero"
        print("✓ PASSED: Single feature gives zero CLR")
    
    def test_large_count_range(self, your_clr_function=clr_transform_reference):
        """
        Microbiome data often spans many orders of magnitude.
        Should handle without overflow/underflow.
        """
        extreme_counts = np.array([[1, 10, 100, 1000, 10000, 100000]])
        result = your_clr_function(extreme_counts)
        
        has_nan = np.any(np.isnan(result))
        has_inf = np.any(np.isinf(result))
        
        print(f"Extreme range CLR: {np.round(result, 4)}")
        assert not has_nan and not has_inf, "Extreme values produced NaN/Inf"
        print("✓ PASSED: Large count range handled correctly")
    
    def test_dataframe_input(self, your_clr_function=clr_transform_reference):
        """Many microbiome workflows use pandas DataFrames."""
        df = pd.DataFrame({
            'taxon_A': [10, 20, 30],
            'taxon_B': [40, 50, 60],
            'taxon_C': [70, 80, 90],
        })
        
        try:
            result = your_clr_function(df)
            print(f"✓ DataFrame input accepted, output type: {type(result)}")
        except Exception as e:
            print(f"⚠ DataFrame input failed: {e}")
            print("  Consider converting: your_clr_function(df.values)")


# ============================================================
# TEST 5: COMPARISON WITH REFERENCE IMPLEMENTATIONS
# ============================================================

class TestAgainstReferenceImplementations:
    """Compare against established libraries."""
    
    def test_against_skbio(self, your_clr_function=clr_transform_reference):
        """Compare against scikit-bio's CLR implementation."""
        try:
            from skbio.stats.composition import clr as skbio_clr
            
            # skbio requires no zeros
            counts = np.array([
                [10.0, 20.0, 30.
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
