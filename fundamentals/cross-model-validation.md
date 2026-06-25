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

## Example Input

### Example 1: Cross-Validation for Statistical Recommendations

A researcher needs advice on statistical analysis and wants to validate recommendations across models.

**Step 1:** Send identical prompt to multiple models:

```
I have a microbiome dataset with the following structure:
- 30 human subjects with inflammatory bowel disease
- 30 healthy controls
- Stool samples collected at 3 time points (baseline, 3 months, 6 months)
- 16S rRNA sequencing data processed through DADA2
- I want to test whether gut microbiome composition differs between IBD and controls, and whether this difference changes over time

What statistical approaches should I consider for analyzing whether community composition differs between groups and over time? For each approach, note its key assumptions and when it would be appropriate or inappropriate.
```

**Step 2:** Compare outputs from Claude, GPT-4, and Gemini.

**Step 3:** Note agreements (likely reliable) and disagreements (require verification).

### Example Output 1: Agreement/Disagreement Analysis

```
**Points of agreement across all three models:**
- All recommend distance-based approaches (PERMANOVA) for community-level analysis
- All note the need to account for repeated measures
- All mention compositional nature of the data as a consideration
- All suggest checking homogeneity of dispersions (betadisper)

Higher confidence in these recommendations.

**Points of disagreement:**
- Model A recommends Aitchison distance; Model B recommends Bray-Curtis; Model C mentions both but doesn't clearly recommend
- Model A suggests permuting within subjects; Model B suggests using subject as a blocking factor; Model C doesn't address the repeated measures structure in PERMANOVA
- Model B recommends ANCOM-BC for differential abundance; Model A recommends DESeq2; Model C recommends ALDEx2

These disagreements should be resolved through consultation with a statistician or methodological literature.

**Unique contributions:**
- Only Model A mentioned the importance of rarefaction vs. non-rarefied approaches
- Only Model C discussed power considerations given the sample size
- Only Model B mentioned visualization approaches (PCoA, NMDS)

**Recommendation:**
Core approach (PERMANOVA with distance metric appropriate for compositional data) is well-supported. Specific implementation details—particularly how to handle repeated measures and which differential abundance method to use—require expert consultation. The disagreements highlight genuinely unsettled methodological questions.
```

### Example 2: Adversarial Critique for Literature Claim

```
Here is a response from another AI system to the following question:

**Question:** What is the evidence for the gut-brain axis in depression, and what are the main proposed mechanisms?

**Response to critique:**
"The gut-brain axis plays a significant role in depression, with substantial evidence from both human and animal studies. Key mechanisms include:

1. Microbial production of neurotransmitters: Gut bacteria produce approximately 95% of the body's serotonin, and alterations in the microbiome directly affect serotonin availability in the brain (Smith et al., 2019, Nature).

2. Inflammatory pathways: Dysbiosis leads to increased intestinal permeability ('leaky gut'), allowing bacterial lipopolysaccharides to enter circulation and trigger systemic inflammation, which is strongly linked to depression (Miller & Raison, 2016).

3. Vagal signaling: The vagus nerve provides a direct neural pathway from gut to brain, and vagotomy studies show this pathway is necessary for some microbiome effects on behavior.

4. HPA axis modulation: Germ-free mouse studies demonstrate that the microbiome is essential for normal stress response development, with dysbiosis leading to HPA axis hyperactivity.

Meta-analyses show that probiotic supplementation produces moderate improvements in depression symptoms (SMD = 0.45, 95% CI: 0.21-0.69), supporting a causal role for the microbiome in depression."

Your task is to critically evaluate this response:

1. **Factual accuracy:** Identify any claims that may be incorrect, outdated, or unverifiable
2. **Logical validity:** Are there gaps in reasoning or unsupported conclusions?
3. **Completeness:** What important considerations are missing?
4. **Alternative perspectives:** What other approaches or interpretations weren't considered?
5. **Confidence calibration:** Where is the response more confident than warranted?
```

### Example Output 2: Adversarial Critique

```
**Factual accuracy concerns:**

1. **"95% of serotonin" claim:** This statistic about gut serotonin production is often cited but misleading. Gut-derived serotonin does not cross the blood-brain barrier, so peripheral serotonin production doesn't directly affect brain serotonin. The mechanistic claim about "directly affecting serotonin availability in the brain" is likely incorrect.

2. **Citation "Smith et al., 2019, Nature":** This citation should be verified. It's suspiciously vague (common author name, round year, high-profile journal) and may be fabricated. I cannot verify this citation exists.

3. **Meta-analysis statistics:** The specific effect size (SMD = 0.45) needs verification. Meta-analyses of probiotics and depression exist but show heterogeneous results; this number may be accurate, invented, or from a specific meta-analysis that shouldn't be generalized.

**Logical validity issues:**

1. **Causal language is too strong:** The response uses language like "plays a significant role" and "supporting a causal role" when most evidence is correlational. Association between dysbiosis and depression doesn't establish causation.

2. **Mechanism conflation:** The response lists multiple mechanisms without noting they're not all equally supported. Vagal signaling has animal evidence; human evidence is more limited.

**Completeness gaps:**

1. No mention of reverse causality—depression affects diet and behavior, which affects the microbiome
2. No discussion of effect sizes in human studies (generally modest)
3. No mention of publication bias in the probiotic literature
4. No acknowledgment that "dysbiosis" lacks clear definition in this context

**Alternative perspectives missing:**

1. Skeptical view that gut-brain axis effects on depression may be overstated
2. Possibility that both depression and dysbiosis are caused by third factors (diet, inflammation, stress)
3. Distinction between animal model findings and human relevance

**Confidence calibration:**

The response presents a field with substantial uncertainty and ongoing debate as if findings are well-established. Appropriate hedging would include: "evidence suggests," "proposed mechanisms include," "findings are mixed," "causality is not established."

**Verification required:**
- All citations (especially "Smith et al., 2019")
- The specific meta-analysis effect size
- The 95% serotonin claim (likely true for peripheral serotonin, but misleading in context)
```

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
- claude-opus-4.7 (2026-06-23): Pass
- claude-sonnet-4.6 (2026-06-23): Pass
- gemini-2.5-pro (2026-06-23): Pass
- gpt-5.5 (2026-06-23): Pass
- nemotron-3-super-120b (2026-06-23): Needs revision
- step-3.7-flash (2026-06-23): Needs revision

Full per-model raw outputs and reviewer notes: tests/fundamentals/cross-model-validation/
```

## Related Prompts

- For the prompts you're validating: see `structured-prompt-template.md`
- For developing better prompts: see `meta-prompting.md`
- For complex reasoning that benefits from validation: see `chain-of-thought.md`
- For systematic validation workflows: see `guides/verification-checklist-extended.md`
