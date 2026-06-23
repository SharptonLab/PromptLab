# Prompt Library Style Guide

This document provides guidance for creating prompt files in PromptLab. It establishes standards for prompt structure, failure mode documentation, and verification requirements to ensure consistency across the repository.

---

## Core Philosophy

Prompts in this repository should embody these core principles:

1. **Prompting is experimental design for a stochastic system.** Inputs materially affect outputs. Underspecified prompts produce unreliable results.

2. **Trust calibration is the user's responsibility.** Every prompt must document failure modes and verification requirements because the model cannot reliably self-assess.

3. **Verification is non-negotiable.** Prompts should be designed to produce verifiable outputs and should specify what verification is required.

---

## Prompt File Structure

Each prompt file should include these sections in order:

### 1. Task Description
A clear, specific statement of what the prompt accomplishes. One to two sentences.

### 2. When to Use
Appropriate contexts and applications. Be specific about research scenarios where this prompt provides value.

### 3. When NOT to Use
Contexts where this prompt is inappropriate or where the approach carries unacceptable risk. This is as important as "when to use."

### 4. The Prompt
The complete prompt text with customization points marked as `{PLACEHOLDER}`. Use clear placeholder names that indicate what type of content belongs there (e.g., `{PAPER_TEXT}`, `{RESEARCH_QUESTION}`, `{DATA_DESCRIPTION}`).

### 5. Prompt Components Explained
Brief explanation of why each component is included. Standard prompt components:
- Context/Background
- Task Specification
- Constraints
- Output Format
- Role/Persona (if used)
- Examples (if used)
- Evaluation Criteria (if used)

### 6. Example Input
A representative use case showing what the user would provide.

### 7. Example Output
What good output looks like. This helps users recognize when the prompt is working.

### 8. Test Input
A standard test input for evaluating this prompt. This serves two purposes:
- Contributors must test prompts before submission
- Users can verify the prompt works in their environment

The test input should be:
- Realistic (representative of actual research scenarios)
- Comprehensive (exercises the prompt's main features and constraints)
- Self-contained (doesn't require external files or data)
- Life science focused (not generic examples)

This input will be used to generate test result files stored in `tests/[category]/[prompt-name]/`. See `docs/TESTING-GUIDE.md` for the test result format.

### 9. Failure Modes
Specific ways this prompt can fail, drawn from the failure mode categories:
- **Hallucination risks:** What might be fabricated?
- **Sycophancy risks:** Where might the model agree when it shouldn't?
- **Overconfidence risks:** What might be presented with false certainty?
- **Context issues:** What might be missed or truncated?

### 10. Verification Requirements
Specific steps the user must take before relying on output. Match verification effort to stakes.

### 11. Variations
Optional modifications for different contexts (e.g., different output formats, different expertise levels, different model capabilities).

### 12. Model Notes
Leave blank for now; to be filled during testing:
```
Models tested: [To be completed]
Date tested: [To be completed]
Notes: [To be completed]
```

---

## Writing Prompt Text

### Structure Over Prose

Well-structured prompts with clear sections produce more consistent outputs than prose paragraphs. Use explicit structure:

```
Context: {CONTEXT}

Task: {TASK_SPECIFICATION}

Constraints:
- Constraint 1
- Constraint 2

Output format: {FORMAT_SPECIFICATION}
```

### Essential Constraints

Include constraints that prevent common failure modes:

- **Prevent hallucination:** "Do not introduce information not present in the provided text" or "If you cannot determine the answer from the provided material, say so explicitly"
- **Counter overconfidence:** "If the answer is uncertain or the data insufficient, say so explicitly" or "Rate your confidence in each claim"
- **Prevent sycophancy:** "Identify weaknesses and limitations, not just strengths" or "What would argue against this interpretation?"
- **Enable verification:** "Cite specific passages that support each claim" or "For each recommendation, explain the assumptions it requires"

### Specificity Matters

Compare weak vs. strong prompt language:

**Weak:** "Summarize this paper"

**Strong:** "Summarize this paper in three paragraphs for a microbiologist unfamiliar with this specific system. Paragraph one: the central finding and why it matters. Paragraph two: the methodological approach, including model organism and key techniques. Paragraph three: limitations the authors acknowledge and questions that remain open. Use only information present in the paper—do not add context from other sources."

### Role Assignment

Use role framing when it affects how the model approaches the task:

**Useful:** "You are a biostatistician reviewing an experimental design. Evaluate the following study for statistical validity, focusing on power, potential confounds, and appropriateness of the proposed analyses. Be direct about weaknesses."

**Not useful:** For simple factual queries or straightforward text generation where the role adds nothing.

When using role assignment, include instructions that counter sycophancy: "Be direct about weaknesses" or "Prioritize honest assessment over encouragement."

---

## Failure Modes by Task Type

Reference these when writing the "Failure Modes" section:

### Literature Tasks
- Citation fabrication (extremely common)
- Misrepresentation of paper findings
- Overstatement of consensus
- Omission of contradictory evidence
- Outdated information presented as current

### Writing Tasks
- Introducing unsupported claims
- Generic, hedged prose that obscures meaning
- Loss of author's voice
- Subtle distortion of intended meaning
- Excessive praise when asked to critique

### Code Tasks
- Code that runs but produces wrong results
- Deprecated functions or packages
- Inefficient or non-idiomatic implementations
- Logic errors masked by syntactic correctness
- Missing edge case handling

### Statistical Tasks
- Recommending inappropriate tests for data structure
- Missing or incomplete assumption checking
- Overconfident single recommendations when multiple approaches are defensible
- Failure to consider specific experimental context
- Outdated methodological advice

### Data Interpretation Tasks
- Overinterpretation of patterns
- Suggesting mechanisms without evidence
- Missing important caveats
- Confirmation bias toward stated hypotheses

---

## Verification Requirements by Task Type

Reference these when writing the "Verification Requirements" section:

### Literature Tasks
- **Every citation must be manually verified**—no exceptions
- Search databases (PubMed, Google Scholar) for exact citations
- Verify papers say what the LLM claims
- Check citation formatting accuracy

### Code Tasks
- Test with known-answer inputs
- Test edge cases and boundary conditions
- Review logic, not just syntax
- Verify packages/functions are current
- "Runs without errors" ≠ "Produces correct results"

### Statistical Tasks
- Consult authoritative sources (textbooks, methodological papers)
- Verify assumptions hold for your specific data
- Consult a statistician for non-trivial analyses
- Be skeptical of single "correct" recommendations

### Factual Claims
- Identify claims requiring verification
- Locate authoritative sources
- Be especially skeptical of specific numbers/percentages
- Flag unverifiable claims explicitly

---

## Life Science Context

All examples should be drawn from life science research contexts:

- Microbiome analysis (16S, metagenomics)
- Experimental design (mouse studies, clinical trials)
- Statistical analysis (diversity metrics, differential abundance)
- Grant writing (specific aims, methods sections)
- Manuscript preparation (methods, results, discussion)
- Literature synthesis (systematic reviews, gap analysis)

Avoid generic examples that could apply to any field. The repository's value comes from domain-specific, tested prompts.

---

## Formatting Conventions

- Use markdown throughout
- Prompt text in blockquotes (`>`) or fenced code blocks
- Placeholders in `{CURLY_BRACES}` with `SCREAMING_SNAKE_CASE`
- Section headers with `###`
- Lists for failure modes and verification requirements
- Tables where comparison aids clarity

---

## Quality Checklist

Before considering a prompt file complete:

- [ ] Task description is clear and specific
- [ ] "When to use" and "When NOT to use" both populated
- [ ] Prompt includes appropriate constraints for the task type
- [ ] Placeholders are clearly named and explained
- [ ] Example input/output demonstrates realistic use
- [ ] Test input is realistic, comprehensive, and self-contained
- [ ] Failure modes are specific to this task, not generic
- [ ] Verification requirements are actionable and proportional to stakes
- [ ] Examples are from life science research contexts
- [ ] No generic advice ("be careful," "verify outputs")—instead, specify what to verify and how
- [ ] At least one test result file exists in `tests/[category]/[prompt-name]/`

---

## Cross-References

Prompts should reference related prompts where appropriate:

- "For verifying citations in synthesis outputs, see `guides/verification-checklist-extended.md`"
- "For brainstorming statistical approaches, see `statistics/test-selection.md`"
- "For critiquing outputs from this prompt, see `validation/adversarial-critique.md`"

Related documentation:

- `docs/TESTING-GUIDE.md` — How to test prompts and document results
- `CONTRIBUTING.md` — Contribution requirements and PR workflow

---

## Version History

| Date | Change |
|------|--------|
| 2026-02-04 | Added Test Input section (section 8); now 12 required sections |
| 2026-01-06 | Initial version created |
