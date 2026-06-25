# Adversarial Critique Prompt

## Task Description

Use an LLM to critically evaluate text, arguments, or outputs—including outputs from other LLM interactions—to identify weaknesses, errors, and areas for improvement.

## When to Use

- Reviewing your own writing before submission
- Getting a "devil's advocate" perspective on your arguments
- Evaluating outputs from a previous LLM interaction
- Identifying weaknesses in a manuscript draft
- Preparing for reviewer criticism

## When NOT to Use

- When you need genuine expert peer review (LLM critique ≠ human expertise)
- For final validation of correctness (critique surfaces issues but doesn't verify accuracy)
- When you're not prepared to evaluate whether the critique is valid
- As a substitute for domain-expert feedback on technical content

## The Prompt

```
Context: I need critical feedback on {WHAT_YOU'RE_EVALUATING: e.g., "a manuscript Discussion section," "an LLM-generated analysis," "my grant specific aims"}.

The text/content to critique:
{PASTE_CONTENT_TO_EVALUATE}

Background (optional): {ANY_RELEVANT_CONTEXT}

Task: Provide an adversarial critique of this content. Your job is to find problems, not to validate. Please identify:

1. **Logical weaknesses**: Flaws in reasoning, unsupported leaps, circular arguments

2. **Factual concerns**: Claims that seem unsupported, incorrect, or unverifiable
   - Flag specific claims that should be checked
   - Note anything that seems too convenient or too clean

3. **Missing considerations**: Important perspectives, alternatives, or caveats that are absent

4. **Overstated claims**: Where has the author gone beyond what the evidence supports?

5. **Structural issues**: Problems with organization, flow, or clarity

6. **What a skeptical reviewer would say**: If this were submitted for peer review, what objections would a critical reviewer raise?

Constraints:
- Be genuinely critical—I want problems surfaced, not reassurance
- Distinguish between minor issues and significant concerns
- Be specific: quote the problematic text and explain the issue
- If something is actually good, you can note it briefly, but focus on problems
- Do not soften criticism or sandwich it between praise

Output format: Structured critique with specific issues and recommended fixes where applicable.
```

## Prompt Components Explained

| Component | Purpose |
|-----------|---------|
| **What you're evaluating** | Shapes the type of critique (manuscript vs. code vs. plan) |
| **The content** | The material to critique |
| **Background** | Helps contextualize the critique |
| **Adversarial framing** | Explicitly counters LLM tendency to be agreeable |
| **Multiple dimensions** | Ensures comprehensive critique |
| **Skeptical reviewer frame** | Evokes peer review standards |

## Example Input

```
Context: I need critical feedback on a manuscript Discussion section paragraph about my gut microbiome findings.

The text to critique:
"Our findings definitively establish that antibiotic treatment disrupts the gut microbiome, with Shannon diversity decreasing by approximately 50% after 7 days of ampicillin exposure. This dramatic reduction demonstrates the profound impact of antibiotics on the gut ecosystem and underscores the urgent need for probiotic co-therapy whenever antibiotics are prescribed. The strong correlation (r = 0.85) between antibiotic exposure and diversity loss provides compelling evidence for a direct causal relationship. These results have immediate clinical implications, suggesting that physicians should routinely prescribe probiotics alongside any antibiotic course to prevent dysbiosis."

Background: This is from a mouse study with n=10 per group.
```

## Example Output

## Adversarial Critique

### 1. Logical Weaknesses

**"definitively establish"**
> "Our findings definitively establish that antibiotic treatment disrupts the gut microbiome"

**Problem**: A single mouse study cannot "definitively establish" anything. Scientific knowledge is built through replication, and this is one study in one strain with one antibiotic. This language will immediately draw reviewer criticism.

**Recommended fix**: "Our findings demonstrate that antibiotic treatment significantly reduces gut microbial diversity in this model" or "consistent with prior work, we observed..."

---

**Correlation ≠ causation conflation**
> "The strong correlation (r = 0.85) between antibiotic exposure and diversity loss provides compelling evidence for a direct causal relationship"

**Problem**: This is a textbook logical error. Correlation, even strong correlation, does not establish causation. Additionally, if "antibiotic exposure" is binary (treated vs. not), reporting a Pearson r is questionable—what was actually correlated with what?

**Recommended fix**: Either justify causation through experimental design (randomization, controls) rather than correlation, or use appropriate causal language: "Randomized assignment to antibiotic treatment resulted in significantly lower diversity, consistent with a causal effect."

---

### 2. Factual Concerns

**Specific claims to verify**:

- "Shannon diversity decreasing by approximately 50%": Is this the actual effect size from your data? Verify exact numbers.

- "r = 0.85": What exactly was correlated? This needs clarification. If you measured a continuous antibiotic exposure variable, state it. If groups were simply treated vs. control, a correlation coefficient is the wrong summary measure.

**Too clean**: A correlation of 0.85 in biological data is unusually high. Double-check this isn't an artifact of the analysis.

---

### 3. Missing Considerations

**Absent from this paragraph**:

- **Limitations**: No mention of mouse-to-human translation issues, single antibiotic limitation, or sample size
- **Mechanism**: The claim about "direct causal relationship" implies mechanism, but no mechanism is discussed
- **Probiotic evidence**: The recommendation for probiotic co-therapy cites no evidence that probiotics actually help. Was this tested in your study?
- **Baseline variation**: No acknowledgment of individual variation or baseline differences

---

### 4. Overstated Claims

**Clinical recommendations from mouse data**
> "physicians should routinely prescribe probiotics alongside any antibiotic course"

**Problem**: This is a dramatic overreach. You conducted a mouse study. Making clinical prescribing recommendations requires:
- Human trials
- Safety data
- Efficacy data for specific probiotics
- Consideration of antibiotic type, indication, patient population

**This claim could genuinely harm your paper's credibility.** A reviewer will use this sentence to argue the authors lack scientific rigor.

**Recommended fix**: "These results in a mouse model suggest that the impact of antibiotics on the gut microbiome warrants further investigation, including exploration of whether probiotic co-administration might mitigate these effects in clinical settings."

---

**"urgent need"**
> "underscores the urgent need for probiotic co-therapy"

**Problem**: Advocacy language that undermines scientific objectivity. The data don't speak to urgency.

---

### 5. Structural Issues

- Paragraph moves too quickly from result to clinical recommendation without bridging evidence
- No hedging language anywhere—every sentence is an assertion
- Mixes specific results (Shannon diversity %) with broad claims (clinical implications) without transition

---

### 6. What a Skeptical Reviewer Would Say

1. "The authors overinterpret their findings from a small mouse study to make broad clinical recommendations. This is inappropriate and undermines confidence in the authors' scientific judgment."

2. "The statement that correlation 'provides compelling evidence for a direct causal relationship' suggests a fundamental misunderstanding of the difference between correlation and causation."

3. "No limitations are acknowledged. What about mouse-human differences? Antibiotic specificity? Sample size?"

4. "Where is the evidence that probiotics would help? This appears to be speculation presented as if it follows from the data."

5. "The effect size should be reported with confidence intervals, not just point estimates."

---

### Priority Fixes

1. **Critical**: Remove or heavily qualify clinical prescribing recommendation
2. **Critical**: Fix correlation/causation language
3. **High**: Add limitations paragraph
4. **Medium**: Replace "definitively establish" with appropriate hedging
5. **Medium**: Verify the r = 0.85 claim and clarify what was correlated

## Test Input

Use the following scenario to test this prompt:

```
Context: I need critical feedback on a manuscript Methods section paragraph about microbiome sample collection.

The text to critique:
"Stool samples were collected from all participants using standard protocols. Samples were immediately frozen at -80°C and DNA was extracted using the Qiagen PowerSoil kit following manufacturer instructions. 16S rRNA gene sequencing was performed using the V4 region primers 515F and 806R on an Illumina MiSeq platform. Sequences were processed using QIIME2 with default parameters, and taxonomy was assigned using the Greengenes database. Alpha diversity was calculated using Shannon index and beta diversity was calculated using Bray-Curtis distances. All statistical analyses were performed using appropriate methods and significance was set at p < 0.05."

Background: This is for a study comparing gut microbiome between healthy controls and patients with inflammatory bowel disease (n=30 per group).
```

**Expected output should include:**

- Critique of vague "standard protocols" (undefined)
- Concern about "immediately frozen" without specifying collection-to-freezing time
- Note that Greengenes database is outdated (replaced by Silva, GTDB)
- Criticism of "default parameters" (non-reproducible)
- Strong objection to "appropriate methods" (meaningless, undefined)
- Missing details: sequencing depth, quality filtering thresholds, rarefaction approach
- Missing information about IBD disease status confirmation, medications, diet
- Concern about p < 0.05 without multiple testing correction discussion

**Verification points:**
- Critique is genuinely critical, not just mildly suggestive
- Domain-specific issues identified (outdated database, missing key methods details)
- Priority issues distinguished from minor concerns
- Suggested fixes are specific and actionable

## Failure Modes

- **Insufficient criticism**: May still be too gentle despite adversarial framing
- **Invalid criticism**: May raise objections that aren't actually problems
- **Missing domain issues**: May miss field-specific problems a domain expert would catch
- **Overconfident corrections**: May suggest fixes that introduce new errors
- **Focusing on minor issues**: May emphasize trivial issues while missing serious ones
- **Sycophancy leaking through**: May include unnecessary positive framing despite instructions

## Verification Requirements

1. **Evaluate each critique**: Is this objection valid? Some may be misunderstandings.
2. **Prioritize**: Focus on critiques that would actually affect your work's reception
3. **Get human feedback**: Use this as input for revision, but also get human reviewer input
4. **Check suggested fixes**: Verify that recommended fixes don't introduce new problems

## Variations

### Cross-model adversarial critique
Feed output from one LLM to another for critique:
```
Context: The following text was generated by another AI system. I need you to critically evaluate it for errors, weaknesses, and problems.

[Paste output from Claude/GPT/etc.]

Task: As an adversarial reviewer, identify all potential problems with this text.
```

### Specific focus areas
```
Focus your critique specifically on {statistical claims / logical coherence / citation accuracy / prose quality}.
```

### Comparative critique
```
Here are two versions of the same text. Critique each and explain which is stronger and why:
Version A: [text]
Version B: [text]
```

### Constructive rewrite request
```
After identifying problems, provide a rewritten version that addresses the major issues while preserving the core message.
```

## Model Notes

```
Tested across the panel; verdicts set by human review.

- Claude Opus 4 (claude-opus-4-5-20251101) (2026-02-04): Pass
- claude-opus-4.7 (2026-06-23): Pass
- claude-sonnet-4.6 (2026-06-23): Pass
- gemini-2.5-pro (2026-06-23): Pass
- gpt-5.5 (2026-06-23): Pass
- nemotron-3-super-120b (2026-06-23): Pass
- step-3.7-flash (2026-06-23): Pass

Full per-model raw outputs and reviewer notes: tests/validation/adversarial-critique/
```

## Cross-References

- For using multiple models for validation, see `guides/cross-model-protocols.md`
- For interpretation brainstorming, see `statistics/interpretation-brainstorming.md`
- For citation verification, see `guides/citation-warning.md`
- For experimental design review, see `statistics/design-review.md`
