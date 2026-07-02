# Cross-Model Validation

## Task Description

Using multiple LLMs to validate outputs, identify errors, and increase confidence in results. Different models have different training data, fine-tuning approaches, and failure modes—this diversity is a resource for verification.

## When to Use

- High-stakes outputs where correctness matters
- Factual claims you need to verify
- Statistical or methodological recommendations where you're uncertain
- Code generation where bugs would be costly
- Any output that will be published or shared
- When a single model's response feels uncertain or too convenient
- Literature-related tasks where hallucination risk is high

## When NOT to Use

- Routine, low-stakes tasks where single-model output suffices
- Simple queries with easily verifiable answers
- When you lack access to multiple models
- Time-critical situations where validation overhead is prohibitive
- Tasks where all models are likely to share the same limitations (e.g., knowledge cutoff issues)

## The Prompt

### Cross-Validation (Same Prompt to Multiple Models)
```
{YOUR_ORIGINAL_PROMPT}
```
Run identical prompt through 2-3 different models. Compare outputs.

### Adversarial Critique (Model B Critiques Model A)
```
Here is a response from another AI system to the following question:

**Question:** {ORIGINAL_QUESTION}

**Response to critique:**
{MODEL_A_OUTPUT}

Your task is to critically evaluate this response:

1. **Factual accuracy:** Identify any claims that may be incorrect, outdated, or unverifiable
2. **Logical validity:** Are there gaps in reasoning or unsupported conclusions?
3. **Completeness:** What important considerations are missing?
4. **Alternative perspectives:** What other approaches or interpretations weren't considered?
5. **Confidence calibration:** Where is the response more confident than warranted?

Be specific and direct. Identify concrete problems rather than vague concerns.
```

### Synthesis Across Models
```
I asked multiple AI systems the same question and received these responses:

**Response 1:**
{MODEL_A_OUTPUT}

**Response 2:**
{MODEL_B_OUTPUT}

**Response 3 (optional):**
{MODEL_C_OUTPUT}

Synthesize these responses:
1. Where do they agree? (Higher confidence)
2. Where do they disagree? (Requires verification)
3. What does each response include that others miss?
4. What's the most defensible answer given the combination?
```

## Prompt Components Explained

| Component | Purpose | Notes |
|-----------|---------|-------|
| **Original prompt** | Ensures identical task across models | Must be exactly the same for valid comparison |
| **Output to critique** | Material for adversarial review | Include full context, not excerpts |
| **Critique dimensions** | Structures the critical analysis | Prevents vague or superficial critique |
| **Request for specificity** | Counters tendency toward mild feedback | Models are more critical of other models' outputs |

## Example Output

For a representative model response to the Test Input, see:

`tests/fundamentals/cross-model-validation/claude-sonnet-4-6-2026-06-25.md`

That cell was captured on 2026-06-25 and human-verified by both project reviewers as passing. Other panel models' responses (Claude Opus 4.7, GPT-5.5, Gemini 2.5 Pro, Nemotron 3 Super 120B, Step-3.7 Flash) are alongside it in the same directory.

## Test Input

Use the following adversarial critique scenario to test this prompt:

```
Here is a response from another AI system to the following question:

**Question:** What statistical test should I use to compare alpha diversity between two groups in my microbiome study?

**Response to critique:**
"For comparing alpha diversity between two groups, you should use a t-test. Alpha diversity metrics like Shannon diversity and observed species richness are continuous variables, making the t-test appropriate. Simply calculate the alpha diversity for each sample, then perform an independent samples t-test to compare the means between your two groups.

For example, if comparing gut microbiome diversity between healthy controls and IBD patients, calculate Shannon diversity for each sample, then use t.test() in R to compare. This is the standard approach used in most microbiome studies and will give you a p-value indicating whether the groups differ significantly."

Your task is to critically evaluate this response:

1. **Factual accuracy:** Identify any claims that may be incorrect, outdated, or unverifiable
2. **Logical validity:** Are there gaps in reasoning or unsupported conclusions?
3. **Completeness:** What important considerations are missing?
4. **Alternative perspectives:** What other approaches or interpretations weren't considered?
5. **Confidence calibration:** Where is the response more confident than warranted?

Be specific and direct. Identify concrete problems rather than vague concerns.
```

**Expected critique should identify:**

**Factual accuracy issues:**
- T-test assumes normality, which alpha diversity metrics often violate
- "Standard approach" claim is questionable—Wilcoxon/Mann-Whitney is often more appropriate

**Completeness gaps:**
- No mention of checking normality assumptions
- No mention of non-parametric alternatives (Wilcoxon rank-sum test)
- No discussion of rarefaction before calculating alpha diversity
- No mention of multiple alpha diversity metrics and whether to correct for multiple comparisons

**Alternative perspectives:**
- Kruskal-Wallis for more than two groups
- Permutation tests
- Linear models if covariates need adjustment

**Confidence calibration:**
- "Standard approach" is overconfident given heterogeneous practices in the field

## Failure Modes

### Hallucination Risks
- Models may agree on incorrect information if they share training data sources
- Critique model may invent problems that don't exist
- Synthesis may introduce errors not present in any original response

### Sycophancy Risks
- Critique may be softer than warranted if the model detects its own previous output
- Frame outputs as coming from "another AI system" to reduce this bias

### Overconfidence Risks
- Agreement across models doesn't guarantee correctness—they may share the same misconceptions
- Critique model may be overconfident about identified "errors" that aren't actually wrong

### Context Issues
- Long outputs to critique may exceed effective processing capacity
- Cross-validation requires access to multiple models and time to run comparisons

## Verification Requirements

1. **Agreement is not proof:** When models agree, confidence increases but verification is still needed for important claims
2. **Disagreement requires resolution:** Don't average or arbitrarily choose between conflicting recommendations—investigate which is correct
3. **Verify the critique:** When a model identifies an "error," check whether it's actually wrong
4. **Cross-check citations:** Models critiquing other models may also hallucinate citations or claim citations are fabricated when they're real
5. **Use domain expertise:** Cross-model validation helps identify areas requiring attention but doesn't replace your ability to evaluate claims in your area of expertise

## Variations

### Quick Cross-Check
```
A colleague suggested: "{CLAIM_OR_RECOMMENDATION}"

Is this accurate? What caveats or qualifications should I be aware of?
```
(Run on a different model than the source)

### Structured Disagreement Analysis
```
I received these two different recommendations for the same task:

Option A: {RECOMMENDATION_A}
Option B: {RECOMMENDATION_B}

1. What does each option assume?
2. Under what circumstances would each be correct?
3. What information would I need to determine which is appropriate for my situation?
```

### Iterative Critique
```
Original response: {RESPONSE}

Critique from Model B: {CRITIQUE}

Respond to this critique:
- Which criticisms are valid?
- Which are incorrect or overstated?
- How should the original response be revised?
```

### Citation Verification Request
```
The following response contains citations. For each citation:
1. Assess whether it looks plausible (author names, journal, year make sense)
2. Flag any that seem suspicious (unusually convenient, vague details)
3. Note which claims would need verification regardless of citation

Response to evaluate:
{RESPONSE_WITH_CITATIONS}

I will verify flagged citations through PubMed/Google Scholar myself.
```

## Practical Workflow

1. **Run original prompt** on your primary model
2. **Identify claims to validate**: factual assertions, statistical recommendations, citations
3. **Run same prompt** on 1-2 additional models
4. **Compare outputs**: Note agreements (higher confidence) and disagreements (flag for verification)
5. **Run adversarial critique** if output quality is critical
6. **Verify externally**: Use the critique and disagreements to guide verification against authoritative sources

## Model Notes

```
Tested across the panel; verdicts set by human review.

- Claude Opus 4 (claude-opus-4-5-20251101) (2026-02-04): Pass
- claude-opus-4.7 (2026-06-25): Pass
- claude-sonnet-4.6 (2026-06-25): Pass
- gemini-2.5-pro (2026-06-25): Pass
- gpt-5.5 (2026-06-25): Pass
- nemotron-3-super-120b (2026-06-25): Pass
- step-3.7-flash (2026-06-25): Needs revision

Full per-model raw outputs and reviewer notes: tests/fundamentals/cross-model-validation/
```

## Related Prompts

- For the prompts you're validating: see `structured-prompt-template.md`
- For developing better prompts: see `meta-prompting.md`
- For complex reasoning that benefits from validation: see `chain-of-thought.md`
- For systematic validation workflows: see `guides/verification-checklist-extended.md`
