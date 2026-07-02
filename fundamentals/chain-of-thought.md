# Chain-of-Thought Prompting

## Task Description

A prompting strategy that asks the model to show its reasoning step by step before reaching a conclusion, improving performance on complex tasks and making the reasoning process visible for evaluation.

## When to Use

- Multi-step analyses where errors compound
- Problems requiring several considerations to be weighed
- Tasks where the reasoning path matters for your work (experimental design, statistical decisions)
- Debugging, where systematic elimination of possibilities is valuable
- When you need to evaluate the model's logic, not just its conclusion
- Complex comparisons or trade-off analyses

## When NOT to Use

- Simple factual queries with clear answers
- Tasks where the reasoning process is trivial
- Situations where you only care about the answer, not the path
- When brevity is essential and reasoning would add unwanted length
- Extraction or formatting tasks where reasoning adds no value

## The Prompt

### Basic Version
```
{TASK_DESCRIPTION}

Think through this step by step:
1. First, identify {RELEVANT_FACTORS}
2. Then, consider {KEY_CONSIDERATIONS}
3. Finally, {REACH_CONCLUSION}

Show your reasoning at each step before providing your final answer.
```

### Structured Version
```
{CONTEXT}

{TASK_SPECIFICATION}

Work through this systematically:

**Step 1 - {FIRST_PHASE}:**
[Explain what to analyze first]

**Step 2 - {SECOND_PHASE}:**
[Explain what to consider next]

**Step 3 - {THIRD_PHASE}:**
[Explain how to synthesize]

**Final recommendation:**
[Specify what the conclusion should include]

Show your reasoning explicitly at each step.
```

## Prompt Components Explained

| Component | Purpose | Notes |
|-----------|---------|-------|
| **Task description** | Frames the problem requiring analysis | Should clearly indicate complexity |
| **Step structure** | Breaks problem into tractable sub-problems | 3-5 steps typically optimal |
| **"Show reasoning" instruction** | Elicits explicit intermediate steps | Critical for evaluation |
| **Final answer request** | Ensures clear conclusion after reasoning | Prevents trailing off |

## Example Output

For a representative model response to the Test Input, see:

`tests/fundamentals/chain-of-thought/claude-sonnet-4-6-2026-06-25.md`

That cell was captured on 2026-06-25 and human-verified by both project reviewers as passing. Other panel models' responses (Claude Opus 4.7, GPT-5.5, Gemini 2.5 Pro, Nemotron 3 Super 120B, Step-3.7 Flash) are alongside it in the same directory.

## Test Input

Use the following scenario to test the chain-of-thought prompt:

```
I need to select a statistical approach for analyzing my microbiome data. Here's my study:

- 20 mice, 10 per treatment group (probiotic vs. placebo)
- Fecal samples collected at 3 time points (days 0, 14, 28)
- Outcome: relative abundances of bacterial taxa (compositional data)
- Question: Does probiotic treatment affect community composition over time?
- Additional context: Some mice were co-housed (2-3 per cage), creating potential cage effects

Think through this step by step:

**Step 1 - Data structure:**
What are the key features of my data that affect analysis choice? Consider the experimental design, the nature of the outcome variable, and any dependencies in the data.

**Step 2 - Candidate approaches:**
What statistical approaches could address my question? For each, briefly note what it assumes and what it tests.

**Step 3 - Assumption evaluation:**
For each candidate approach, which assumptions might be problematic for my specific data structure?

**Step 4 - Practical considerations:**
What practical factors (software availability, interpretability, field conventions) should influence the choice?

**Step 5 - Recommendation:**
Based on the above, what approach or approaches would you suggest I discuss with a statistician? What specific questions should I ask them?

Show your reasoning explicitly at each step.
```

**Expected output should demonstrate:**
- Step 1 identifies: repeated measures, compositional data, cage effects as clustering, small sample size
- Step 2 lists multiple approaches (PERMANOVA, mixed models, etc.) with assumptions
- Step 3 addresses: how repeated measures complicate PERMANOVA, how cage effects create non-independence
- Step 4 mentions software (vegan, lme4) and field conventions
- Step 5 provides actionable recommendation with specific questions for a statistician

**Verification points:**
- Each step shows explicit reasoning, not just conclusions
- Statistical claims (test assumptions, software capabilities) should be verified against documentation
- Recommendation acknowledges limitations of sample size

## Failure Modes

### Hallucination Risks
- May cite statistical methods or software that don't exist
- May describe properties of statistical tests incorrectly
- May invent "standard practice" that isn't actually standard

### Sycophancy Risks
- If you mention a preferred approach, the model may reason toward it rather than objectively
- May avoid recommending against approaches you seem invested in

### Overconfidence Risks
- **Critical**: Fluent, well-structured reasoning can be completely wrong. The steps may look valid while resting on incorrect premises
- May present contested statistical advice as settled
- May recommend a single "correct" approach when multiple are defensible

### Context Issues
- Long reasoning chains may lose track of constraints stated earlier
- Complex problems may exceed the model's ability to maintain logical coherence

## Verification Requirements

1. **Evaluate each step independently**: Does the claim about the data structure accurately describe your data? Does the description of each method match authoritative sources?

2. **Check factual claims within reasoning**: Statistical properties, method assumptions, and software capabilities should all be verified against documentation or textbooks

3. **Watch for logical gaps**: Does each step actually follow from the previous? Are there unstated assumptions?

4. **Consult domain experts**: For statistical recommendations specifically, the reasoning provides good material for discussion with a statistician—but does not replace that consultation

5. **Be skeptical of confident conclusions**: A well-reasoned recommendation may still be inappropriate for reasons the model didn't consider

## Variations

### Simple Chain-of-Thought
```
{QUESTION}

Think through this step by step before answering.
```

### Chain-of-Thought with Uncertainty
```
{TASK}

Work through this step by step. At each step:
- State your reasoning
- Note any uncertainties or assumptions you're making
- Indicate your confidence level

Then provide your conclusion with appropriate caveats.
```

### Contrastive Chain-of-Thought
```
{TASK}

Consider two possible approaches:

Approach A: {FIRST_OPTION}
Approach B: {SECOND_OPTION}

For each approach, reason through:
1. What assumptions does it make?
2. What are its strengths for my situation?
3. What are its weaknesses for my situation?

Then recommend which approach (or combination) is most appropriate and why.
```

### Chain-of-Thought with Self-Critique
```
{TASK}

First, reason through this step by step to reach a preliminary conclusion.

Then, critique your own reasoning:
- What might be wrong with this analysis?
- What have I assumed that might not hold?
- What alternative conclusions could the evidence support?

Finally, provide your revised conclusion accounting for this critique.
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

Full per-model raw outputs and reviewer notes: tests/fundamentals/chain-of-thought/
```

## Related Prompts

- For basic prompt structure: see `structured-prompt-template.md`
- For consistency across multiple inputs: see `few-shot-learning.md`
- For developing the reasoning structure: see `meta-prompting.md`
- For checking reasoning with another model: see `cross-model-validation.md`
