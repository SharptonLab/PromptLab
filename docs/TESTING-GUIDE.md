# Prompt Testing Guide

This guide explains how to test prompts and document results for the LLM Life Science Research Prompts repository.

## Why Test Prompts

Every prompt in this repository must be tested with at least one LLM before acceptance. Testing serves three purposes:

1. **Verification**: Confirms the prompt achieves its stated task
2. **Failure mode validation**: Checks whether constraints actually mitigate predicted failures
3. **Documentation**: Provides users with evidence of real-world performance

## Testing Workflow

### Step 1: Locate the Test Input

Each prompt file includes a `## Test Input` section with a representative test case. Use this input for your test, or create a variation appropriate to your research context.

### Step 2: Run the Prompt

1. Copy the prompt from the `## The Prompt` section
2. Fill in all `{PLACEHOLDER}` values using the test input
3. Submit to an LLM (any capable model: Claude, GPT-4, Gemini, etc.)
4. Save the complete output

### Step 3: Evaluate the Output

Assess the output against:

- **Task achievement**: Did it accomplish what the prompt describes?
- **Constraint compliance**: Were all constraints in the prompt respected?
- **Failure mode check**: Did any predicted failure modes occur?
- **Output format**: Does the output match the specified format?

### Step 4: Document Results

Create a test result file following the format below and save it to the appropriate location in `tests/`.

## Test Result File Format

```markdown
# Test Results: [prompt-filename.md]

## Test Metadata
- **Prompt:** [category]/[prompt-filename.md]
- **Model:** [Full model name and version, e.g., "Claude Opus 4 (claude-opus-4-5-20251101)"]
- **Date:** YYYY-MM-DD
- **Tester:** [Name or GitHub handle]

## Test Input Used
[Copy of the test input, or "Standard test input from prompt file"]

## Filled Prompt
[The complete prompt with all placeholders filled in]

## Model Output
[Complete output from the LLM, or representative excerpt for very long outputs]

## Assessment

### Task Achievement
- **Achieved:** Yes / No / Partial
- **Notes:** [Brief explanation]

### Constraint Compliance
- **All constraints respected:** Yes / No
- **Violations noted:** [List any, or "None"]

### Failure Modes
- **Failure modes observed:** None / [List any that occurred]
- **Mitigation effectiveness:** [Did the prompt's constraints help?]

### Output Format
- **Format correct:** Yes / No
- **Deviations:** [List any, or "None"]

## Overall Assessment
- **Recommendation:** Pass / Pass with notes / Needs revision
- **Notes:** [Any additional observations, edge cases, or suggestions]

## Verification Steps Tested
[Which verification requirements from the prompt were checked, and results]
```

## File Organization

Test results are stored in `repository/tests/` with a structure mirroring the prompt categories:

```
repository/
  tests/
    fundamentals/
      structured-prompt-template/
        claude-opus-4-2026-02-04.md
        gpt-4-turbo-2026-02-04.md
      few-shot-learning/
        claude-opus-4-2026-02-04.md
    literature/
      paper-summary/
        claude-opus-4-2026-02-04.md
```

### Naming Convention

Test result files: `[model-name]-[date].md`

Examples:
- `claude-opus-4-2026-02-04.md`
- `gpt-4-turbo-2026-02-04.md`
- `gemini-pro-2026-02-04.md`
- `llama-3-70b-2026-02-04.md`

Use lowercase with hyphens. Include the date to track when the test was run.

## Minimum Requirements

For a prompt to be accepted into the repository:

1. **At least one test result** must be provided
2. Test must use **the prompt's standard test input** (or document why a variation was used)
3. Test result must include **complete assessment** (all sections filled)
4. Overall assessment must be **Pass** or **Pass with notes**

## Testing Tips

### Creating Good Test Inputs

When writing the `## Test Input` section for a new prompt:

- Use realistic life science research scenarios
- Include enough detail to meaningfully test the prompt
- Avoid inputs that are trivially easy or impossibly hard
- Consider edge cases that might trigger failure modes

### Evaluating Outputs

Be honest in assessments:

- A prompt can pass even if the output isn't perfect
- Note any concerns in the "Notes" sections
- If failure modes occur, document them—this helps improve prompts
- Partial task achievement is acceptable if documented

### Multiple Test Runs

Additional test results are welcome:

- Different models may behave differently
- Edge case inputs help validate robustness
- Retesting after prompt updates confirms improvements

## Updating Test Results

When a prompt is modified:

1. Existing test results remain (they document historical behavior)
2. New tests should be run with the updated prompt
3. Add new test result files with current dates
4. Note in the test file if testing a revised version

## Cross-References

- `PROMPT-STYLE-GUIDE.md` — Required prompt structure including Test Input section
- `CONTRIBUTING.md` — Full contribution workflow including PR requirements
