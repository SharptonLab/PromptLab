# Contributing to the LLM Life Science Prompts Repository

We welcome contributions from the research community. This repository improves through shared experience: prompts that work, failure modes discovered, and verification approaches refined.

## What We're Looking For

### New Prompts

Prompts for research tasks not currently covered, particularly:
- Domain-specific applications (clinical, ecological, molecular biology)
- Specialized analysis workflows
- Tasks where you've developed effective approaches through iteration

### Improvements to Existing Prompts

- Additional failure modes you've encountered
- Verification approaches that worked well
- Variations for different contexts
- Additional test results from different models

### Case Studies

Worked examples showing complete workflows, especially:
- Workflows combining multiple prompts
- Examples from domains other than microbiome research
- Cases where verification caught significant errors

---

## Contribution Requirements

### For New Prompts

All new prompts must include **12 required sections** (see `PROMPT-STYLE-GUIDE.md`):

1. **Task Description** — What the prompt accomplishes
2. **When to Use** — Appropriate contexts
3. **When NOT to Use** — Inappropriate or risky contexts
4. **The Prompt** — Complete text with `{PLACEHOLDERS}`
5. **Prompt Components Explained** — How the four core components are used
6. **Example Input** — Representative use case
7. **Example Output** — What good output looks like
8. **Test Input** — Standard input for testing this prompt
9. **Failure Modes** — Specific ways this prompt can fail
10. **Verification Requirements** — Concrete steps to check output
11. **Variations** — Optional modifications
12. **Model Notes** — Testing summary and observations

### For All Contributions: Test Results Required

**Every prompt must have at least one documented test result.**

Test results are stored separately from prompt files in `tests/[category]/[prompt-name]/`. Each test result file documents:

- Model used (name and version)
- Date tested
- Complete input and output
- Assessment of task achievement, constraint compliance, and failure modes
- Overall pass/fail recommendation

See `docs/TESTING-GUIDE.md` for complete testing requirements and file format.

---

## Quality Standards

### Prompts Must Be Tested

We don't accept untested prompts. Before submitting:

1. Use the prompt with a real or realistic test input
2. Document complete results in a test result file
3. Assess whether the prompt achieved its task
4. Note any failures or unexpected behaviors

### Failure Modes Must Be Specific

**Not acceptable:** "The model might hallucinate"

**Acceptable:** "When summarizing methods sections, the model sometimes invents sample sizes not present in the text. Verify all numerical claims against the original."

### Verification Must Be Actionable

**Not acceptable:** "Verify the output is correct"

**Acceptable:** "Check each citation against PubMed to confirm the paper exists and the stated findings match the abstract"

### Test Inputs Must Be Representative

The `## Test Input` section should provide:
- A realistic life science research scenario
- Enough detail to meaningfully test the prompt
- Content that exercises the prompt's constraints
- Consideration of potential failure modes

---

## How to Contribute

### Pull Request Workflow

#### For New Prompts

1. **Open an issue first** describing the prompt you want to add
2. **Fork the repository**
3. **Create the prompt file** in the appropriate category directory
   - Follow `PROMPT-STYLE-GUIDE.md` format exactly
   - Include all 12 required sections
   - Ensure `## Test Input` section has a usable test case
4. **Test the prompt** with at least one LLM
5. **Create a test result file** in `tests/[category]/[prompt-name]/`
   - Follow the format in `docs/TESTING-GUIDE.md`
   - Name the file `[model-name]-[date].md`
6. **Submit a pull request** including:
   - The new prompt file
   - At least one test result file
   - PR description explaining the prompt's purpose and your testing context

#### For Improvements to Existing Prompts

1. **Fork the repository**
2. **Make your changes** to the prompt file
3. **Test the updated prompt** if changes affect behavior
4. **Add a new test result file** if you tested (don't replace existing tests)
5. **Submit a pull request** describing:
   - What you changed and why
   - Testing performed (if applicable)

#### For Additional Test Results

We welcome test results for existing prompts, especially from different models:

1. **Run the prompt** using the standard test input
2. **Create a test result file** following `docs/TESTING-GUIDE.md`
3. **Submit a pull request** adding your test result to the appropriate `tests/` subdirectory

#### For Small Changes

For minor edits (typos, clarifications):
- Submit a pull request directly
- No test required for non-behavioral changes

---

## Pull Request Checklist

Before submitting, verify:

**For new prompts:**
- [ ] Prompt file follows `PROMPT-STYLE-GUIDE.md` format
- [ ] All 12 sections are present and complete
- [ ] `## Test Input` provides a usable test case
- [ ] At least one test result file is included
- [ ] Test result follows `docs/TESTING-GUIDE.md` format
- [ ] Test result shows Pass or Pass with notes
- [ ] Files are in correct directories

**For prompt improvements:**
- [ ] Changes are clearly explained in PR description
- [ ] New test result included if changes affect behavior
- [ ] Existing test results preserved (not overwritten)

**For test result additions:**
- [ ] Used standard test input from prompt file
- [ ] Test result follows `docs/TESTING-GUIDE.md` format
- [ ] File named correctly: `[model-name]-[date].md`

---

## Directory Structure

```
repository/
  [category]/
    [prompt-name].md          # Prompt file
  tests/
    [category]/
      [prompt-name]/
        claude-opus-4-2026-02-04.md    # Test results
        gpt-4-turbo-2026-02-04.md
  docs/
    TESTING-GUIDE.md          # Testing instructions
  PROMPT-STYLE-GUIDE.md       # Prompt format requirements
  CONTRIBUTING.md             # This file
```

---

## Review Process

Contributions will be reviewed for:

- **Completeness** — All required sections present, test results included
- **Quality** — Failure modes and verification are specific and useful
- **Testing** — Test results demonstrate the prompt works
- **Fit** — Appropriate for life science research contexts
- **Format compliance** — Follows style guide and testing guide

We aim to review contributions within two weeks. Complex additions may require discussion.

---

## Attribution

Contributors will be acknowledged in:
- The repository's contributor list
- Test result files (tester field)
- The prompt file's Model Notes section (for significant contributions)

---

## Questions?

- **Testing questions:** See `docs/TESTING-GUIDE.md`
- **Format questions:** See `PROMPT-STYLE-GUIDE.md`
- **Other questions:** Open an issue with the "question" label

---

Thank you for helping build resources that support rigorous, transparent use of LLMs in research.
