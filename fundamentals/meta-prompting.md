# Meta-Prompting

## Task Description

Using the LLM to help develop, refine, and improve prompts before using them for your actual task. This strategy surfaces hidden assumptions, identifies ambiguities, and produces more effective prompts than most users write unaided.

## When to Use

- Developing prompts for complex or unfamiliar tasks
- Creating reusable prompts that will be used many times
- When initial prompts produce inconsistent or unsatisfactory results
- When you're unsure what information the model needs to complete a task well
- Before investing significant time in a prompt-driven workflow
- When you know what you want but struggle to specify it precisely

## When NOT to Use

- Simple, one-off queries where the overhead isn't justified
- Tasks where you already have well-tested prompts
- When you're exploring and don't yet know what you want
- Time-critical situations where prompt development would cause delays

## The Prompt

### Interview Approach
```
I want your help with a task, but before I describe it, I want you to ask me clarifying questions to ensure you understand exactly what I need.

The task involves: {BRIEF_TASK_DESCRIPTION}

What questions do you have about the format, scope, audience, constraints, or purpose that would help you assist me effectively?
```

### Prompt Critique Approach
```
Here's a prompt I'm planning to use for {TASK_DESCRIPTION}:

---
{DRAFT_PROMPT}
---

Please critique this prompt:
1. What's ambiguous or underspecified?
2. What assumptions am I making that might not hold?
3. What failure modes might this prompt produce?
4. How would you improve it to make outputs more consistent and reliable?

Provide a revised version of the prompt incorporating your suggestions.
```

### Reverse Engineering Approach
```
I want to create a prompt that produces outputs like these examples:

Example output 1:
{EXAMPLE_OUTPUT_1}

Example output 2:
{EXAMPLE_OUTPUT_2}

Based on these examples, write a prompt that would reliably produce this type of output. Include:
- Clear task specification
- Appropriate constraints
- Output format specification
- Any examples that would help
```

## Prompt Components Explained

| Component | Purpose | Notes |
|-----------|---------|-------|
| **Brief task description** | Gives model enough context to ask relevant questions | Don't over-specify—let questions surface gaps |
| **Request for questions** | Prompts the model to identify missing information | Be prepared to answer honestly |
| **Draft prompt** | Material for the model to critique | Include your best attempt |
| **Example outputs** | Demonstrate what success looks like | Choose representative, well-formed examples |

## Example Output

For a representative model response to the Test Input, see:

`tests/fundamentals/meta-prompting/claude-sonnet-4-6-2026-06-25.md`

That cell was captured on 2026-06-25 and human-verified by both project reviewers as passing. Other panel models' responses (Claude Opus 4.7, GPT-5.5, Gemini 2.5 Pro, Nemotron 3 Super 120B, Step-3.7 Flash) are alongside it in the same directory.

## Test Input

Use the following prompt critique scenario to test this prompt:

```
Here's a prompt I'm planning to use for analyzing differential gene expression results:

---
Look at my RNA-seq results and tell me which genes are important. The data is from a mouse liver study comparing high-fat diet to control.
---

Please critique this prompt:
1. What's ambiguous or underspecified?
2. What assumptions am I making that might not hold?
3. What failure modes might this prompt produce?
4. How would you improve it to make outputs more consistent and reliable?

Provide a revised version of the prompt incorporating your suggestions.
```

**Expected output should include:**

**Critique identifying:**
- "Important" is undefined (statistically significant? biologically relevant? largest fold change?)
- No output format specified
- No information about the analysis already performed (DESeq2? edgeR?)
- No context about research question or hypothesis
- No constraints on interpretation scope

**Revised prompt should include:**
- Specific criteria for "important" (e.g., FDR < 0.05 AND |log2FC| > 1)
- Defined output format (table, ranked list, etc.)
- Placeholders for actual results data
- Constraints preventing overinterpretation
- Request for uncertainty acknowledgment

**Verification points:**
- Critique is specific and actionable, not generic
- Revised prompt addresses each identified issue
- Revised prompt follows good prompting principles

## Failure Modes

### Hallucination Risks
- Model may suggest prompt improvements that sound good but don't actually help
- Reverse-engineered prompts may not reliably reproduce the example patterns

### Sycophancy Risks
- Model may not critique your prompt harshly enough
- May suggest mild refinements when significant restructuring is needed
- Add explicit instruction: "Be direct about weaknesses—gentle suggestions won't help me improve the prompt"

### Overconfidence Risks
- Model may confidently suggest changes that make prompts worse
- Critique may miss actual problems while focusing on minor issues

### Context Issues
- For reverse engineering, the model may focus on superficial patterns rather than underlying structure

## Verification Requirements

1. **Test the improved prompt**: The only real validation is whether the new prompt produces better outputs than the original
2. **Compare before/after**: Run both versions on the same input to assess improvement
3. **Check multiple inputs**: A prompt that works on one input may fail on others
4. **Verify critique accuracy**: If the model claims something is ambiguous, consider whether it actually is
5. **Iterate**: Meta-prompting often requires 2-3 rounds of refinement

## Variations

### Comprehensive Interview
```
I want to develop a robust, reusable prompt for {TASK}. Interview me about this task—ask detailed questions about:
- What success looks like
- What failure looks like
- Edge cases and exceptions
- How outputs will be used
- What I care most about

After I answer your questions, draft a complete prompt and explain your design choices.
```

### Comparative Critique
```
Here are two versions of a prompt for the same task:

Version A:
{PROMPT_A}

Version B:
{PROMPT_B}

Compare these prompts:
1. What does each do well?
2. What problems does each have?
3. Which would produce more reliable outputs and why?
4. How would you combine the best elements of both?
```

### Failure Analysis
```
I used this prompt:

{PROMPT}

And got this output:

{PROBLEMATIC_OUTPUT}

The problem is: {DESCRIPTION_OF_PROBLEM}

Diagnose what in my prompt led to this failure and suggest specific changes to prevent it.
```

### Progressive Refinement
```
Here's my current prompt:

{CURRENT_PROMPT}

It works reasonably well, but I want to improve {SPECIFIC_ASPECT}.

Suggest 2-3 targeted modifications that address this issue without breaking what's already working.
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

Full per-model raw outputs and reviewer notes: tests/fundamentals/meta-prompting/
```

## Related Prompts

- For the prompts you're developing: see `structured-prompt-template.md`
- For consistency across outputs: see `few-shot-learning.md`
- For complex reasoning tasks: see `chain-of-thought.md`
- For validating improved prompts: see `cross-model-validation.md`
