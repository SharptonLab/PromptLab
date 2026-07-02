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

````
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
````

## Prompt Components Explained

| Component | Purpose |
|-----------|---------|
| **Analysis description** | Helps identify what correctness means |
| **The code** | The specific code to test |
| **Expected behavior** | Defines what "correct" means |
| **Test data available** | Shapes what tests are feasible |
| **Testing approach** | Matches your workflow (formal frameworks vs. simple checks) |

## Example Output

For a representative model response to the Test Input, see:

`tests/code/testing-requirements/claude-sonnet-4-6-2026-06-25.md`

That cell was captured on 2026-06-25 and human-verified by both project reviewers as passing. Other panel models' responses (Claude Opus 4.7, GPT-5.5, Gemini 2.5 Pro, Nemotron 3 Super 120B, Step-3.7 Flash) are alongside it in the same directory.

## Test Input

Use the following scenario to test this prompt:

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
Tested across the panel; verdicts set by human review.

- Claude Opus 4 (claude-opus-4-5-20251101) (2026-02-04): Pass
- claude-opus-4.7 (2026-06-25): Pass
- claude-sonnet-4.6 (2026-06-25): Pass
- gemini-2.5-pro (2026-06-25): Pass
- gpt-5.5 (2026-06-25): Pass
- nemotron-3-super-120b (2026-06-25): Pass
- step-3.7-flash (2026-06-25): Pass

Full per-model raw outputs and reviewer notes: tests/code/testing-requirements/
```

## Cross-References

- For generating code to test, see `code/r-script-generation.md` or `code/python-analysis.md`
- For debugging failing tests, see `code/debugging.md`
- For understanding what code does before testing, see `code/code-explanation.md`
