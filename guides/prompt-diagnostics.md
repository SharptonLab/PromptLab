# Prompt Diagnostics Guide

When large language model outputs disappoint, the problem usually traces to an underspecified prompt component. This guide links common failure patterns to their likely causes and solutions.

## Diagnostic Reference

| Failure Pattern | Likely Cause | Solution |
|-----------------|--------------|----------|
| Output misses the point entirely | Task specification was unclear or ambiguous | Rewrite the core instruction. State exactly what is needed, in terms specific enough that success is recognizable. |
| Output is inconsistent across runs | Too many degrees of freedom; the model fills gaps differently each time | Add constraints and specify output format precisely. Reduce the space of acceptable responses. |
| Output includes unwanted content | Constraints are missing or inadequate | Specify what to exclude. Statements like "Do not include..." or "Limit your response to..." are often necessary. |
| Output uses wrong framing or makes incorrect assumptions | Context is insufficient; the model infers the situation from training data patterns | Provide more background on the specific research context, data structure, or constraints. |
| Output uses unexpected structure or format | Output format was unspecified or ambiguous | Define structure explicitly. For repeated tasks, provide an example of the exact format needed. |
| Output is generic or superficial | The prompt lacks specificity, so the model defaults to the most common case | Add domain-specific context and constraints. Request specific details rather than general overviews. |
| Output confidently provides wrong information | Hallucination, an architectural feature rather than a prompt failure | No prompt change prevents this entirely. Verify all specific claims independently. Consider adding: "If you are uncertain, say so." |

## The Iterative Approach

Prompt development is rarely successful on the first attempt. When an output fails:

1. Identify which component is underspecified using the patterns above
2. Revise that specific component
3. Test the revised prompt
4. Repeat until outputs meet requirements

Expect three to ten iterations for complex tasks. Save successful prompts for reuse; a well-developed prompt is a reusable research tool.

## Prompt Components Checklist

When diagnosing failures, check whether the prompt adequately specifies each component:

**Context:** Does the prompt provide enough background for the model to understand the situation? Research domain, data structure, project stage, and relevant constraints should be explicit rather than assumed.

**Task specification:** Is the instruction specific enough that success is recognizable? "Help with my paper" is not a task specification; "identify gaps in logical flow in the Discussion section" is.

**Constraints:** Does the prompt establish boundaries on acceptable outputs? Common constraints include instructing the model not to introduce information beyond provided text, to state uncertainty explicitly, or to cite specific passages supporting each claim.

**Output format:** Does the prompt specify how results should be structured? Format specification ensures consistency, which proves essential when processing multiple items or comparing results across queries.

**Examples (when needed):** For complex or unusual formats, do examples demonstrate expected output? Examples communicate expectations more reliably than descriptions for many tasks.
