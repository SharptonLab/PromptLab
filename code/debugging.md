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

```
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
```

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

## Example Input

```
Context: I am working on a microbiome analysis pipeline in R. I'm encountering an error I can't resolve.

The error message:
```
Error in sample_data(ps) :
  error in evaluating the argument 'object' in selecting a method for function 'sample_data': object 'ps' not found
Traceback:
 1: sample_data(ps)
```

The relevant code:
```r
library(phyloseq)

# Load OTU table
otu <- read.csv("data/otu_table.csv", row.names = 1)
otu_mat <- as.matrix(otu)

# Load metadata
meta <- read.csv("data/metadata.csv", row.names = 1)

# Create phyloseq object
OTU <- otu_table(otu_mat, taxa_are_rows = TRUE)
META <- sample_data(meta)
ps <- phyloseq(OTU, META)

# Later in the script, in a function:
analyze_diversity <- function() {
  sample_df <- sample_data(ps)
  # ... more analysis
}

analyze_diversity()
```

What I was trying to do: Extract sample metadata from my phyloseq object inside a function.

What I've already tried:
- Verified ps exists after creation (it does)
- Checked that phyloseq loaded correctly
- Tried running sample_data(ps) outside the function (it works)

Environment details:
- R 4.3.1
- phyloseq 1.44.0
- Running in RStudio on Windows
```

## Example Output

### 1. Explain the Error

The error "object 'ps' not found" means that when R tries to execute `sample_data(ps)` inside your function, it cannot find a variable called `ps` in the environment where the function is running. This is a **scoping issue**—the variable exists in your global environment but is not accessible inside the function.

### 2. Identify the Cause

The problem is that your function `analyze_diversity()` doesn't have access to `ps`. In R, functions have their own local scope and can only access:
- Variables passed as arguments
- Variables defined inside the function
- Variables in the global environment (with some caveats)

When you define a function without parameters and then call it, R looks for `ps` first in the function's local environment, then in the function's enclosing environment. If you defined this function in a script that runs in a fresh environment or within a package, `ps` from the global environment may not be visible.

**Most likely cause**: You may have defined the function in a separate file/session, or there's an environment isolation issue (common in RStudio when using "Source" vs running line-by-line).

### 3. Provide the Fix

**Option A: Pass ps as an argument (recommended)**
```r
analyze_diversity <- function(ps) {
  # ps is now explicitly passed to the function
  sample_df <- sample_data(ps)
  # ... more analysis
  return(sample_df)
}

# Call with the phyloseq object
result <- analyze_diversity(ps)
```

**Option B: Explicitly reference global environment (less recommended)**
```r
analyze_diversity <- function() {
  # Explicitly get ps from global environment
  ps <- get("ps", envir = globalenv())
  sample_df <- sample_data(ps)
  # ... more analysis
}
```

### 4. Explain Why

**Option A works** because you explicitly tell R which phyloseq object to use. The function no longer depends on finding `ps` in some external scope—it receives the object directly. This is more robust and makes the function's dependencies clear.

**Option B works** but is fragile because:
- It creates a hidden dependency on global state
- The function will break if `ps` is renamed or doesn't exist
- It makes code harder to test and reuse

### 5. Prevention

To avoid scoping issues in the future:

1. **Make dependencies explicit**: Pass all needed objects as function arguments
2. **Avoid relying on global variables inside functions**: If a function needs data, pass it in
3. **Use consistent environments**: Be aware that "Source" in RStudio runs code in a fresh environment, while running line-by-line uses the console's global environment
4. **Test functions in isolation**: Call your function in a fresh R session to catch scoping issues early

**General rule**: If a function uses a variable, that variable should either be:
- A parameter of the function
- Created inside the function
- A constant or configuration that's documented

## Test Input

Use the following debugging scenario to test this prompt:

```
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
```

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
Models tested: [To be completed]
Date tested: [To be completed]
Notes: [To be completed]
```

## Cross-References

- For understanding code before debugging, see `code/code-explanation.md`
- For writing tests to catch bugs, see `code/testing-requirements.md`
- For generating new R code, see `code/r-script-generation.md`
- For generating new Python code, see `code/python-analysis.md`
