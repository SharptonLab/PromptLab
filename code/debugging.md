# Code Debugging Prompt

## Task Description

Diagnose and fix errors in code by providing error messages, relevant code, and context. Get explanations of what went wrong and corrected code.

## When to Use

- Interpreting cryptic error messages
- Finding bugs when code runs but produces wrong results
- Understanding why code that worked before now fails
- Debugging issues in code from tutorials, papers, or collaborators

## When NOT to Use

- For code you don't understand at all (understand it first, then debug)
- When the error requires access to your specific data or environment to reproduce
- For security-sensitive code where sharing context could be risky
- When you haven't tried basic debugging steps first (check typos, read the error)

## The Prompt

````
Context: I am working on {BRIEF_PROJECT_DESCRIPTION} in {LANGUAGE}. I'm encountering an error I can't resolve.

The error message:
```
{PASTE_COMPLETE_ERROR_MESSAGE_AND_TRACEBACK}
```

The relevant code:
```{language}
{PASTE_CODE_THAT_CAUSES_THE_ERROR}
```

What I was trying to do: {EXPLAIN_INTENDED_BEHAVIOR}

What I've already tried:
- {LIST_DEBUGGING_STEPS_ALREADY_TAKEN}

Environment details (if relevant):
- {LANGUAGE_VERSION}
- {RELEVANT_PACKAGE_VERSIONS}
- {OPERATING_SYSTEM_IF_RELEVANT}

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

## Prompt Components Explained

| Component | Purpose |
|-----------|---------|
| **Project context** | Helps interpret error in context |
| **Complete error message** | Full traceback is essential for diagnosis |
| **Relevant code** | The code that triggers the error |
| **Intended behavior** | Clarifies what "correct" looks like |
| **What you've tried** | Avoids redundant suggestions |
| **Environment details** | Many errors are version-specific |
| **Structured response request** | Gets comprehensive explanation, not just a fix |

## Example Output

For a representative model response to the Test Input, see:

`tests/code/debugging/claude-sonnet-4-6-2026-06-25.md`

That cell was captured on 2026-06-25 and human-verified by both project reviewers as passing. Other panel models' responses (Claude Opus 4.7, GPT-5.5, Gemini 2.5 Pro, Nemotron 3 Super 120B, Step-3.7 Flash) are alongside it in the same directory.

## Test Input

Use the following debugging scenario to test this prompt:

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

**Expected output should include:**
- Explanation: braycurtis expects two 1D vectors of same length; error occurs because otu_table[i] has 100 elements but otu_table[:,j] is selecting all 50 rows of column j
- Cause identification: Indexing error - should be otu_table[j] not otu_table[:,j]
- Fixed code with the correction
- Explanation of why: need to compare row i to row j, not row i to column j
- Prevention tip: understanding numpy indexing (row vs column selection)

**Verification points:**
- Diagnosis correctly identifies the indexing error
- Fixed code would actually run without error
- Explanation is clear for someone unfamiliar with numpy indexing

## Failure Modes

- **Missing context**: May guess wrong if the error requires seeing more code or environment details
- **Wrong diagnosis**: May identify a plausible but incorrect cause, especially for complex errors
- **Over-complicated fix**: May suggest complex solutions when a simple fix exists
- **Version-specific issues**: May not account for differences between package versions
- **Incomplete fix**: May fix the immediate error but introduce new issues
- **Environment-specific**: May miss issues that depend on your specific data or system

## Verification Requirements

1. **Test the fix**: Run the corrected code to confirm it resolves the error
2. **Check for new errors**: Ensure the fix doesn't introduce different problems
3. **Understand the explanation**: Make sure you understand *why* the fix works
4. **Test edge cases**: If the fix involved logic changes, test with different inputs
5. **Verify intended behavior**: Confirm the code now produces the expected output, not just that it runs

## Variations

### Logic bug (no error message)
When code runs but produces wrong results:
```
Context: My code runs without errors but produces incorrect output.

The code:
{CODE}

Expected output: {WHAT_YOU_EXPECTED}
Actual output: {WHAT_YOU_GOT}

Sample input used: {INPUT_DATA}

Task: Help me find the logic error causing the wrong output.
```

### Performance issue
When code is too slow:
```
Context: My code works correctly but is too slow.

The code:
{CODE}

Current performance: {HOW_SLOW: e.g., "takes 30 minutes on 10,000 rows"}
Target performance: {GOAL}
Data size: {SIZE}

Task: Identify performance bottlenecks and suggest optimizations.
```

### Intermittent error
When errors occur inconsistently:
```
Context: This code sometimes fails and sometimes works.

Error when it fails: {ERROR}
Conditions when it fails: {WHAT_YOU'VE_NOTICED}
Conditions when it works: {WHAT_YOU'VE_NOTICED}

Task: Help me identify what causes the inconsistent behavior.
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

Full per-model raw outputs and reviewer notes: tests/code/debugging/
```

## Cross-References

- For understanding code before debugging, see `code/code-explanation.md`
- For writing tests to catch bugs, see `code/testing-requirements.md`
- For generating new R code, see `code/r-script-generation.md`
- For generating new Python code, see `code/python-analysis.md`
