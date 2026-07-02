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

## Example Output

For a representative model response to the Test Input, see:

`tests/validation/uncertainty-elicitation/claude-sonnet-4-6-2026-06-25.md`

That cell was captured on 2026-06-25 and human-verified by both project reviewers as passing. Other panel models' responses (Claude Opus 4.7, GPT-5.5, Gemini 2.5 Pro, Nemotron 3 Super 120B, Step-3.7 Flash) are alongside it in the same directory.

## Test Input

Use the following scenario to test this prompt:

```
Context: You previously provided the following output when I asked about methods for analyzing differential abundance in microbiome data:

"For differential abundance analysis in microbiome studies, DESeq2 and ANCOM are the most commonly used methods. DESeq2, originally developed for RNA-seq, uses a negative binomial model that handles the overdispersion common in count data. According to Weiss et al. (2017), DESeq2 has high sensitivity but can have elevated false positive rates with small sample sizes. ANCOM uses a log-ratio approach that accounts for compositionality and was shown by Mandal et al. (2015) to have better false positive control. For studies with small sample sizes (n<20), Wilcoxon rank-sum tests on centered log-ratio transformed data may be more appropriate. The recommended approach is to use at least two methods and focus on taxa identified by both, as suggested in the McMurdie and Holmes (2014) review of microbiome statistical methods."

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
- claude-opus-4.7 (2026-06-25): Pass
- claude-sonnet-4.6 (2026-06-25): Pass
- gemini-2.5-pro (2026-06-25): Pass
- gpt-5.5 (2026-06-25): Pass
- nemotron-3-super-120b (2026-06-25): Pass
- step-3.7-flash (2026-06-25): Pass

Full per-model raw outputs and reviewer notes: tests/validation/uncertainty-elicitation/
```

## Cross-References

- For adversarial critique, see `validation/adversarial-critique.md`
- For verification checklist, see `guides/verification-checklist-extended.md`
- For citation-specific verification, see `guides/citation-warning.md`
- For cross-model validation, see `guides/cross-model-protocols.md`
