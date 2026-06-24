# Test Results: code/debugging.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-23.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** code/debugging.md
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
Context: I am working on {BRIEF_PROJECT_DESCRIPTION} in {LANGUAGE}. I'm encountering an error I can't resolve.

The error message:

Context: I am working on a microbiome diversity analysis in Python. I'm encountering an error I can't resolve.

The error message:
```

## Model Output
```
It looks like your message contains **unfilled template placeholders** (`{BRIEF_PROJECT_DESCRIPTION}` and `{LANGUAGE}`) in the first part, but then you provided the actual details in the second part.

Let me work with what you've given me:

---

## What I Have So Far

- **Project:** Microbiome diversity analysis
- **Language:** Python
- **Error message:** *(appears to be missing/cut off)*

---

## To Help You Effectively, I Need:

### 1. The Complete Error Message
```
Paste the full traceback here, for example:
Traceback (most recent call last):
  File "analysis.py", line 42, in <module>
    ...
ValueError: ...
```

### 2. The Relevant Code
```python
# Share the code snippet causing the issue
```

### 3. Additional Context (helpful but optional)
- What libraries are you using? (e.g., `scikit-bio`, `qiime2`, `pandas`, `scipy`)
- What were you trying to do when the error occurred?
- What does your input data look like?

---

## Common Microbiome Analysis Errors I Can Help With:
- Alpha/Beta diversity calculation issues
- OTU/ASV table formatting problems
- Distance matrix errors
- Rarefaction problems
- Metadata alignment issues

**Please share the error message and code and I'll help you debug it!**
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
