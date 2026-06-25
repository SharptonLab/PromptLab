# Uncertainty Elicitation Prompt

## Task Description

Prompt an LLM to explicitly state what it's uncertain about, what it might be wrong about, and what claims require verification—counteracting the model's tendency to present everything with equal confidence.

## When to Use

- After getting substantive output from an LLM, to identify what needs verification
- Before relying on LLM-generated content for important decisions
- When an answer seems too clean, too confident, or too convenient
- To generate a verification checklist before publishing or sharing LLM-assisted work

## When NOT to Use

- As a substitute for actual verification (eliciting uncertainty ≠ verifying correctness)
- When you won't act on the uncertainty information
- For trivial tasks where verification overhead exceeds value

## The Prompt

```
Context: You previously provided the following output:
{PASTE_PREVIOUS_LLM_OUTPUT_OR_DESCRIBE_THE_TASK}

Task: Now step back and critically assess your own response. Please identify:

1. **Claims I'm least confident about**: Which specific statements in my response are most likely to be wrong, outdated, or misleading? For each:
   - Quote the claim
   - Explain why I'm uncertain
   - Suggest how to verify

2. **Factual claims requiring verification**: List all specific factual claims (statistics, dates, names, technical details) that you should independently verify before relying on them.

3. **Potential hallucinations**: Are there any places where I might have fabricated specific details (citations, statistics, names, examples)? What are the highest-risk items?

4. **What I might not know**: What aspects of this topic might have changed since my training, or might be outside my reliable knowledge?

5. **Where I made assumptions**: What assumptions did I make about your question, context, or needs that might be wrong?

6. **Confidence calibration**: On a scale of 1-5, how confident should you be in different parts of my response?
   - 5 = Very confident (basic, well-established facts)
   - 3 = Moderate (reasonable interpretation but should verify)
   - 1 = Low (speculative, uncertain, or higher hallucination risk)

Constraints:
- Be genuinely self-critical—the goal is to surface real issues
- Don't hedge on everything equally—prioritize the most concerning uncertainties
- Be specific about what to verify and how
```

## Prompt Components Explained

| Component | Purpose |
|-----------|---------|
| **Previous output reference** | Focuses assessment on specific content |
| **Multiple uncertainty dimensions** | Surfaces different types of problems |
| **Confidence calibration** | Helps prioritize verification effort |
| **Verification suggestions** | Makes output actionable |

## Example Input

```
Context: You previously provided the following output when I asked about appropriate sample sizes for microbiome studies:

"For 16S rRNA studies comparing two groups, you typically need 20-30 samples per group to detect moderate effect sizes (Cohen's d = 0.5-0.8) with 80% power. This is based on simulation studies by Kelly et al. (2015) that specifically examined power in microbiome studies. For shotgun metagenomic studies, sample size requirements are similar, though some metrics like pathway abundance may require 40+ samples per group. The Human Microbiome Project used approximately 250 subjects, which provided excellent power but is beyond most lab budgets. For longitudinal studies, within-subject designs can reduce required n by approximately 30% due to reduced variance."

Task: [Continue with the uncertainty elicitation prompt above]
```

## Example Output

### 1. Claims I'm Least Confident About

**"Kelly et al. (2015) that specifically examined power in microbiome studies"**
> Quote: "based on simulation studies by Kelly et al. (2015)"

**Why I'm uncertain**: I cannot reliably verify this citation. This is exactly the type of specific reference that I might have fabricated or misattributed. There may or may not be a Kelly et al. 2015 paper on microbiome power analysis.

**How to verify**: Search PubMed for "Kelly 2015 microbiome power" or similar. Check if this paper exists and whether it actually contains the claims I attributed to it.

**Hallucination risk: HIGH**

---

**"within-subject designs can reduce required n by approximately 30%"**
> Quote: "reduce required n by approximately 30%"

**Why I'm uncertain**: This specific percentage is suspiciously precise. Power reduction from within-subject designs varies dramatically depending on the correlation structure, effect type, and outcome. A single percentage is an oversimplification that may be fabricated or taken out of context.

**How to verify**: This would require consultation with a statistician or reference to power analysis methodology literature. The 30% figure may not be wrong, but its generalizability is questionable.

**Hallucination risk: MEDIUM-HIGH**

---

### 2. Factual Claims Requiring Verification

| Claim | Verification method |
|-------|-------------------|
| 20-30 samples per group for moderate effect size | Check power analysis literature; run actual power calculation |
| Cohen's d = 0.5-0.8 is "moderate" | Confirm Cohen's benchmarks (this one is likely correct) |
| Kelly et al. (2015) | Search PubMed for exact citation |
| 40+ samples for pathway abundance | Check metagenomic power literature |
| HMP used ~250 subjects | Verify against HMP publications (likely correct but confirm) |
| 30% reduction for longitudinal designs | Verify against power methodology literature |

### 3. Potential Hallucinations

**Highest risk items (most likely fabricated):**

1. **The Kelly et al. citation**: I may have confabulated this reference entirely or conflated multiple sources. This is my highest-confidence concern.

2. **The "30%" figure**: Suspiciously specific numbers without clear sourcing are classic hallucination indicators.

3. **"40+ samples for pathway abundance"**: This is plausible but I don't have a reliable source for this specific threshold.

**Lower risk but still verify:**

4. The HMP subject count is approximately correct but should be confirmed.
5. The 20-30 sample range is in line with general guidance but power depends heavily on specific parameters.

### 4. What I Might Not Know

- **Recent methodological developments**: Power analysis approaches for microbiome data are an active research area. Methods published in 2023-2024 (near or after my training cutoff) may provide better guidance.

- **Field-specific conventions**: Sample size expectations may differ between clinical microbiome studies, environmental microbiome studies, and animal model studies.

- **Software updates**: Specific power calculation tools (micropower, powerSurvEpi, etc.) may have been updated with new recommendations.

- **Study-specific variation**: Power requirements depend heavily on outcome metrics (alpha diversity, beta diversity, differential abundance), and I may have conflated guidance across different outcome types.

### 5. Where I Made Assumptions

- **Assumed you meant taxonomic 16S studies**: You might be asking about functional profiling, which has different considerations.

- **Assumed "moderate effect size" is your target**: Your actual expected effect size might be smaller or larger.

- **Assumed α = 0.05 and power = 0.80**: Standard defaults, but you might have different requirements.

- **Assumed independent samples design**: You might be planning a more complex design (nested, clustered, matched).

- **Assumed you want guidance, not exact calculations**: A power analysis requires specific parameters; I provided ranges.

### 6. Confidence Calibration

| Content | Confidence (1-5) | Notes |
|---------|------------------|-------|
| General principle that 20-30/group is reasonable for moderate effects | 4 | Well-established range, though context-dependent |
| The Kelly et al. citation | 1 | May be fabricated—verify before using |
| Cohen's d definitions | 5 | Standard, well-established |
| 30% reduction claim | 2 | Suspiciously specific; likely oversimplified |
| HMP sample size | 4 | Approximately correct; verify for precision |
| Shotgun requiring 40+ samples | 3 | Plausible but unverified |

---

### Summary: What You Must Verify

**Before citing or relying on this response:**

1. ❌ **Do not cite Kelly et al. (2015) without confirming it exists**
2. ❌ **Do not quote the "30%" reduction figure** without better sourcing
3. ✓ Run an actual power calculation with your specific parameters
4. ✓ Consult your statistician for study-specific guidance
5. ~ The general ranges (20-30 samples) are reasonable starting points but not authoritative

## Test Input

Use the following scenario to test this prompt:

```
Context: You previously provided the following output when I asked about methods for analyzing differential abundance in microbiome data:

"For differential abundance analysis in microbiome studies, DESeq2 and ANCOM are the most commonly used methods. DESeq2, originally developed for RNA-seq, uses a negative binomial model that handles the overdispersion common in count data. According to Weiss et al. (2017), DESeq2 has high sensitivity but can have elevated false positive rates with small sample sizes. ANCOM uses a log-ratio approach that accounts for compositionality and was shown by Mandal et al. (2015) to have better false positive control. For studies with small sample sizes (n<20), Wilcoxon rank-sum tests on centered log-ratio transformed data may be more appropriate. The recommended approach is to use at least two methods and focus on taxa identified by both, as suggested in the McMurdie and Holmes (2014) review of microbiome statistical methods."

Task: [Continue with the uncertainty elicitation prompt above]
```

**Expected output should include:**

- Uncertainty about specific citations (verify Weiss et al. 2017, Mandal et al. 2015 exist and say what was claimed)
- Flag the McMurdie and Holmes (2014) reference for verification
- Acknowledgment that "recommended approach" may be LLM opinion presented as consensus
- Uncertainty about the n<20 threshold (where does this come from?)
- Note that differential abundance methods are rapidly evolving (ANCOM-BC, LinDA, etc.)
- Confidence calibration distinguishing well-established facts from specific claims

**Verification points:**
- High-risk claims (specific citations, specific thresholds) flagged appropriately
- Confidence levels differentiate between general principles and specific details
- Actionable verification suggestions provided
- Model acknowledges potential for citation fabrication

## Failure Modes

- **Performative uncertainty**: May express uncertainty without genuine self-assessment
- **Hedging everything equally**: May not prioritize what's actually most concerning
- **Missing real problems**: May not identify actual hallucinations while flagging things that are correct
- **Overconfidence in self-assessment**: May say "low hallucination risk" about things that are fabricated
- **Not actionable**: May provide vague uncertainty without clear verification paths

## Verification Requirements

1. **Don't take uncertainty assessments at face value**: The model's assessment of its own confidence may be wrong
2. **Verify the high-risk items**: Actually check the flagged citations, statistics, and claims
3. **Consider unflagged items too**: The model may have missed problems
4. **Use this as a checklist, not a guarantee**: Elicitation surfaces concerns; verification confirms them

## Variations

### Targeted uncertainty assessment
```
Focus specifically on {citations / statistics / technical details / recommendations} in your response. Rate confidence and identify verification requirements for each.
```

### Pre-response uncertainty
Before getting an answer:
```
Before answering my question, tell me:
1. What aspects of this question are you likely to be uncertain about?
2. What's most likely to be wrong in your response?
3. What should I definitely verify independently?

Then provide your answer with inline [UNCERTAIN] flags where appropriate.
```

### Multi-turn verification
After any substantive response:
```
Stop. Before I act on this:
- What's the most likely error in what you just told me?
- What single thing should I verify first?
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

Full per-model raw outputs and reviewer notes: tests/validation/uncertainty-elicitation/
```

## Cross-References

- For adversarial critique, see `validation/adversarial-critique.md`
- For verification checklist, see `guides/verification-checklist-extended.md`
- For citation-specific verification, see `guides/citation-warning.md`
- For cross-model validation, see `guides/cross-model-protocols.md`
