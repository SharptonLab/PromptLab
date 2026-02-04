# Testing Requirements Prompt

## Task Description

Generate test cases and testing strategies for analysis code, ensuring that scripts produce correct results before relying on their output for research.

## When to Use

- Before using LLM-generated code for real analysis
- When adapting code from papers or tutorials to your data
- When creating reusable analysis functions
- After modifying existing code
- When you need to verify that code produces expected results

## When NOT to Use

- For trivial one-off scripts you'll visually verify
- When you don't have known-answer test cases available
- As a substitute for understanding what the code does
- For code where testing overhead exceeds the code's complexity

## The Prompt

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
```

## Prompt Components Explained

| Component | Purpose |
|-----------|---------|
| **Analysis description** | Helps identify what correctness means |
| **The code** | The specific code to test |
| **Expected behavior** | Defines what "correct" means |
| **Test data available** | Shapes what tests are feasible |
| **Testing approach** | Matches your workflow (formal frameworks vs. simple checks) |

## Example Input

```
Context: I have R code for calculating beta diversity distance matrices from a phyloseq object. I need to verify it produces correct results before using it for my research.

The code to test:
```r
calculate_beta_diversity <- function(ps, method = "bray") {
  # Convert to relative abundance
  ps_rel <- transform_sample_counts(ps, function(x) x / sum(x))

  # Extract OTU table (samples as rows)
  otu <- as(otu_table(ps_rel), "matrix")
  if (taxa_are_rows(ps_rel)) {
    otu <- t(otu)
  }

  # Calculate distance matrix
  dist_matrix <- vegdist(otu, method = method)

  return(dist_matrix)
}
```

What the code should do: Calculate pairwise Bray-Curtis dissimilarity between all samples, returning a distance matrix.

Test data available: I can create a simple phyloseq object with known abundances where I can calculate expected distances by hand.

Task: Help me create a testing strategy using simple assert statements and manual checks.
```

## Example Output

### 1. Test Cases

#### Normal inputs
- **Standard dataset**: phyloseq with multiple samples and taxa, varying abundances
- **Different methods**: Test with "bray", "jaccard", "euclidean" to verify method parameter works

#### Edge cases
- **Two samples only**: Minimum for a distance matrix—should return single distance value
- **Single taxon**: All samples have only one taxon—Bray-Curtis should depend only on that taxon's proportions
- **Sample with zero total counts**: Should this error, return NA, or be handled somehow?
- **Identical samples**: Distance between identical communities should be 0

#### Known-answer tests
- **Hand-calculated example**: Create 2-3 samples where you can manually calculate expected Bray-Curtis

#### Boundary conditions
- **Very low abundances**: Near-zero proportions
- **Highly uneven communities**: One dominant taxon (99% abundance)

### 2. Test Code

```r
library(phyloseq)
library(vegan)
library(testthat)  # optional, for cleaner assertions

# -----------------------------------------------------------------------------
# Test 1: Known-answer test with simple data
# -----------------------------------------------------------------------------
# Create minimal test data where we can calculate expected values by hand

# Two samples, two taxa:
# Sample A: Taxon1 = 100, Taxon2 = 0   → proportions: 1.0, 0.0
# Sample B: Taxon1 = 50,  Taxon2 = 50  → proportions: 0.5, 0.5

# Bray-Curtis = sum(|p_A - p_B|) / sum(p_A + p_B) = (|1-0.5| + |0-0.5|) / (1+1) = 1/2 = 0.5

otu_test <- matrix(c(100, 0, 50, 50), nrow = 2, byrow = TRUE)
rownames(otu_test) <- c("SampleA", "SampleB")
colnames(otu_test) <- c("Taxon1", "Taxon2")

ps_test <- phyloseq(
  otu_table(otu_test, taxa_are_rows = FALSE)
)

result <- calculate_beta_diversity(ps_test, method = "bray")
expected <- 0.5

cat("Test 1: Known-answer test\n")
cat("Expected Bray-Curtis:", expected, "\n")
cat("Got:", as.numeric(result), "\n")
stopifnot(abs(as.numeric(result) - expected) < 1e-10)
cat("PASSED\n\n")

# -----------------------------------------------------------------------------
# Test 2: Identical samples should have distance 0
# -----------------------------------------------------------------------------
otu_identical <- matrix(c(10, 20, 30, 10, 20, 30), nrow = 2, byrow = TRUE)
rownames(otu_identical) <- c("SampleA", "SampleB")
colnames(otu_identical) <- c("T1", "T2", "T3")

ps_identical <- phyloseq(otu_table(otu_identical, taxa_are_rows = FALSE))

result_identical <- calculate_beta_diversity(ps_identical)
expected_identical <- 0

cat("Test 2: Identical samples\n")
cat("Expected:", expected_identical, "\n")
cat("Got:", as.numeric(result_identical), "\n")
stopifnot(as.numeric(result_identical) == 0)
cat("PASSED\n\n")

# -----------------------------------------------------------------------------
# Test 3: Verify output structure
# -----------------------------------------------------------------------------
# Create larger dataset
set.seed(42)
otu_multi <- matrix(sample(1:100, 20), nrow = 4)
rownames(otu_multi) <- paste0("Sample", 1:4)
colnames(otu_multi) <- paste0("Taxon", 1:5)

ps_multi <- phyloseq(otu_table(otu_multi, taxa_are_rows = FALSE))

result_multi <- calculate_beta_diversity(ps_multi)

cat("Test 3: Output structure\n")
cat("Is dist object:", inherits(result_multi, "dist"), "\n")
stopifnot(inherits(result_multi, "dist"))

# 4 samples should give 4*3/2 = 6 pairwise distances
cat("Number of distances:", length(result_multi), "\n")
stopifnot(length(result_multi) == 6)

# All values should be between 0 and 1 for Bray-Curtis
cat("All values in [0,1]:", all(result_multi >= 0 & result_multi <= 1), "\n")
stopifnot(all(result_multi >= 0 & result_multi <= 1))
cat("PASSED\n\n")

# -----------------------------------------------------------------------------
# Test 4: Taxa-as-rows orientation
# -----------------------------------------------------------------------------
# Test that code handles both orientations correctly
otu_rows <- t(otu_test)  # Now taxa are rows

ps_rows <- phyloseq(otu_table(otu_rows, taxa_are_rows = TRUE))

result_rows <- calculate_beta_diversity(ps_rows)

cat("Test 4: Taxa-as-rows orientation\n")
cat("Expected:", expected, "\n")
cat("Got:", as.numeric(result_rows), "\n")
stopifnot(abs(as.numeric(result_rows) - expected) < 1e-10)
cat("PASSED\n\n")

# -----------------------------------------------------------------------------
# Test 5: Cross-check with direct vegan call
# -----------------------------------------------------------------------------
# Verify our function matches manual vegan workflow

# Manually do what the function should do
ps_rel_manual <- transform_sample_counts(ps_multi, function(x) x / sum(x))
otu_manual <- as(otu_table(ps_rel_manual), "matrix")
if (taxa_are_rows(ps_rel_manual)) otu_manual <- t(otu_manual)
expected_manual <- vegdist(otu_manual, method = "bray")

result_check <- calculate_beta_diversity(ps_multi)

cat("Test 5: Cross-check with manual vegan call\n")
cat("Matches manual calculation:", all.equal(result_check, expected_manual), "\n")
stopifnot(isTRUE(all.equal(result_check, expected_manual)))
cat("PASSED\n\n")

cat("=== All tests passed ===\n")
```

### 3. Validation Checks

After running on real data, manually verify:

1. **Matrix dimensions**: n samples should produce n(n-1)/2 distances
2. **Value range**: Bray-Curtis should be [0, 1]; Euclidean can be larger
3. **Symmetry**: Distance from A to B equals distance from B to A (automatic in dist objects)
4. **Diagonal**: Distance from sample to itself should be 0 (implicit in dist objects)
5. **Sanity check known samples**: If you have replicates or samples you expect to be similar, verify they have low distances

### 4. Red Flags

These patterns indicate something is wrong:

- **All distances are 0**: Transformation or extraction failed
- **All distances are identical**: Likely a bug in looping or indexing
- **Any distances > 1 for Bray-Curtis**: Values should be bounded [0, 1]
- **NaN or Inf values**: Division by zero or other numerical issues
- **Unexpected matrix size**: Wrong sample subsetting or transposition
- **Very similar samples show high distance**: Possible transposition or normalization error
- **Results don't match vegan directly**: The wrapper is doing something different

## Test Input

Use the following scenario to test this prompt:

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

**Expected output should include:**
- Test cases for:
  - Known-answer test (simple 2×2 matrix where CLR can be calculated by hand)
  - Verification that row means are 0 (property of CLR)
  - Edge case: row with one very large value
  - Edge case: uniform counts (all same value)
  - Verification that zeros are handled (pseudocount)
- Test code with assertions
- Validation checks for output properties
- Red flags (e.g., non-zero row means, NaN values, inf values)

**Verification points:**
- Known-answer test values can be verified by hand calculation
- Tests cover the key mathematical properties of CLR
- Edge cases relevant to microbiome data (zeros, varying library sizes)

## Failure Modes

- **Tests don't catch real bugs**: May generate tests that pass even when code is wrong
- **Over-testing trivial cases**: May suggest elaborate tests for simple operations
- **Missing edge cases**: May not anticipate your specific data's edge cases
- **Incorrect expected values**: May calculate wrong "expected" values in examples
- **Language version issues**: Test syntax may not work in your R/Python version

## Verification Requirements

1. **Run all suggested tests**: Don't assume they'll pass
2. **Verify expected values**: Double-check any "expected" values provided, especially for known-answer tests
3. **Add your own edge cases**: Think about your specific data's quirks
4. **Test with real data subset**: Run on a small piece of your actual data and inspect manually

## Variations

### Minimal verification (for quick checks)
```
Task: Suggest 2-3 quick manual checks I can do to verify this code works, without writing formal tests.
```

### Regression testing
```
Context: I'm modifying existing code and need to ensure I don't break anything.
Task: Suggest tests that verify the new code produces identical output to the old code.
```

### Performance testing
```
Task: In addition to correctness tests, suggest how to verify the code performs acceptably on large datasets.
```

### Test data generation
```
Task: Help me create synthetic test data with known properties so I can verify the analysis produces expected results.
```

## Model Notes

```
Models tested: [To be completed]
Date tested: [To be completed]
Notes: [To be completed]
```

## Cross-References

- For generating code to test, see `code/r-script-generation.md` or `code/python-analysis.md`
- For debugging failing tests, see `code/debugging.md`
- For understanding what code does before testing, see `code/code-explanation.md`
