# Test Results: code/code-explanation.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-23.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** code/code-explanation.md
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
Context: I am a {RESEARCHER_ROLE} trying to understand code from {SOURCE: e.g., "a published paper," "a collaborator," "a tutorial"}. My programming background: {YOUR_LEVEL: e.g., "intermediate R, learning Python," "comfortable with basic Python, new to pandas"}.

The code I need explained:

Context: I am a microbiome researcher trying to understand code from a published paper on differential abundance analysis. My programming background: comfortable with R basics, new to DESeq2.

The code I need explained:
```

## Model Output
```
# DESeq2 Code Explanation for Microbiome Researchers

Please paste the actual code you need explained! You left the code block empty.

---

**While you're grabbing that code, here's what to include for the best explanation:**

```
# Paste everything between these markers:
# --- START ---

[your code here]

# --- END ---
```

**Also helpful to know:**
- [ ] What your input data looks like (OTU table? phyloseq object? raw counts?)
- [ ] What comparison you're trying to make (e.g., disease vs. healthy, two timepoints)
- [ ] Any error messages you're seeing, if applicable
- [ ] Which part feels most confusing (the statistics? the syntax? the output?)

---

**Once you share the code, I'll break it down by:**

1. **What each line does** in plain language
2. **Why it matters** for microbiome data specifically
3. **The DESeq2 logic** behind key steps (size factors, dispersion, etc.)
4. **Common microbiome-specific gotchas** to watch for
5. **What the output means** biologically

Go ahead and paste the code! 🧬
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
