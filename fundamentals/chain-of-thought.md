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

## Example Input

A researcher needs help selecting an appropriate statistical approach for a complex microbiome study design.

```
I need to select a statistical approach for analyzing my microbiome data. Here's my study:

- 24 mice, 12 per treatment group (antibiotic vs. control)
- Fecal samples collected at 5 time points (days 0, 7, 14, 21, 28)
- Outcome: relative abundances of bacterial taxa (compositional data)
- Question: How does antibiotic treatment affect community composition over time?

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

## Example Output

```
**Step 1 - Data structure:**

Key features affecting analysis choice:

- **Repeated measures**: Same mice sampled across 5 time points creates within-subject correlation. Observations are not independent—day 7 samples from a mouse are correlated with day 14 samples from the same mouse.

- **Compositional data**: Relative abundances sum to 1 (or 100%), creating artificial negative correlations between taxa. Standard methods assuming independence of features will give misleading results.

- **Multivariate outcome**: Interest is in community composition (many taxa simultaneously), not just individual taxa.

- **Two-level structure**: Mice nested within treatment groups; time points nested within mice.

- **Modest sample size**: 12 mice per group limits power for complex models and taxa-specific analyses.

**Step 2 - Candidate approaches:**

1. **PERMANOVA with repeated measures considerations**
   - Tests: Whether community composition differs by treatment, time, and their interaction
   - Assumes: Exchangeability of samples under null; homogeneity of dispersions
   - Note: Standard PERMANOVA doesn't account for repeated measures

2. **Distance-based linear mixed models (e.g., PERMANOVA with blocking)**
   - Tests: Treatment effects while accounting for mouse-level correlation
   - Assumes: Appropriate distance metric for compositional data; linear effects

3. **Compositional data approaches (e.g., centered log-ratio transformation + mixed models)**
   - Tests: Treatment and time effects on transformed abundances
   - Assumes: No zeros or zeros appropriately handled; normality of transformed data

4. **Generalized linear mixed models for individual taxa (e.g., negative binomial with random effects)**
   - Tests: Per-taxon treatment effects accounting for repeated measures
   - Assumes: Appropriate distribution; sufficient counts per taxon

5. **Multivariate longitudinal methods (e.g., MixMC, SPLS-DA with repeated measures)**
   - Tests: Discriminant features between groups over time
   - Assumes: Latent structure approach is appropriate

**Step 3 - Assumption evaluation:**

- **PERMANOVA (standard)**: Problematic—doesn't handle repeated measures. Would inflate false positives due to within-mouse correlation.

- **Blocked PERMANOVA**: Better, but blocking by mouse may not fully capture the longitudinal correlation structure. Worth exploring with permutation constrained within mice.

- **CLR + mixed models**: Reasonable, but zero handling is critical for microbiome data. Many taxa will have zeros, requiring pseudo-counts or zero-specific methods. Also assumes multivariate normality after transformation.

- **Per-taxon GLMMs**: Appropriate distribution for count data, but multiple testing across many taxa is a concern. Also requires sufficient counts—rare taxa may need to be filtered or aggregated.

- **MixMC/SPLS-DA**: Designed for this type of data, but interpretability and validation approach differ from hypothesis testing frameworks.

**Step 4 - Practical considerations:**

- **Software**: PERMANOVA widely available (vegan in R); mixed models available in lme4, glmmTMB. MixMC in mixOmics package.

- **Field conventions**: Microbiome literature commonly uses PERMANOVA for community-level questions, but repeated measures designs are often handled incorrectly or incompletely.

- **Interpretability**: PERMANOVA pseudo-F and R² are intuitive. Mixed model coefficients may be harder to interpret for compositional outcomes.

- **Reviewer expectations**: Showing you've accounted for repeated measures and compositionality will strengthen the analysis.

**Step 5 - Recommendation:**

Suggested approaches to discuss with a statistician:

1. **Primary recommendation**: Distance-based approach (e.g., PERMANOVA) using a compositional distance metric (Aitchison distance) with permutations constrained to account for the repeated measures structure. This addresses both compositionality and non-independence.

2. **Complementary approach**: For specific taxa of interest, negative binomial GLMMs with mouse as random effect, using appropriate multiple testing correction.

**Questions for the statistician:**

- How should I structure permutations to respect the longitudinal design? Is permuting within mouse sufficient, or do I need a more complex scheme?
- For the distance metric, is Aitchison distance appropriate, or would you recommend robust Aitchison (for zeros)?
- What's the best strategy for handling the time variable—as categorical (each time point) or continuous (days)?
- For per-taxon analyses, what count threshold should I use for filtering rare taxa?
- How should I handle the interaction between treatment and time—is my sample size sufficient to detect this interaction?
```

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
Models tested: [To be completed]
Date tested: [To be completed]
Notes: [To be completed]
```

## Related Prompts

- For basic prompt structure: see `structured-prompt-template.md`
- For consistency across multiple inputs: see `few-shot-learning.md`
- For developing the reasoning structure: see `meta-prompting.md`
- For checking reasoning with another model: see `cross-model-validation.md`
