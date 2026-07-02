# Synthesis Across Papers Prompt

## Task Description

Synthesize findings, methods, or themes across multiple research papers you have read, identifying areas of agreement, disagreement, and methodological variation.

## When to Use

- Writing literature review sections for manuscripts or grants
- Identifying consensus and controversy in a field
- Comparing methodological approaches across studies
- Preparing comprehensive background for a research proposal
- Understanding the state of evidence on a specific question

## When NOT to Use

- When you haven't read the papers yourself (you cannot verify the synthesis)
- To generate citations for papers you haven't provided (citation fabrication risk is extreme)
- For systematic reviews requiring formal synthesis protocols (use PRISMA-compliant approaches)
- When the papers span topics too diverse for meaningful comparison

## The Prompt

```
Context: I am synthesizing literature on {RESEARCH_TOPIC} for {PURPOSE: e.g., a review section, grant background, comprehensive exam}. I have read the following papers and am providing their content below.

Papers provided:
{PAPER_1_TEXT}
---
{PAPER_2_TEXT}
---
{PAPER_3_TEXT}
[Add more as needed]

Task: Synthesize these papers with respect to {SPECIFIC_SYNTHESIS_FOCUS}. Structure your synthesis as follows:

1. **Overview**: One paragraph summarizing the collective state of knowledge across these papers.

2. **Points of Agreement**: What do these papers consistently find or conclude? Be specific about which papers support each point.

3. **Points of Disagreement or Tension**: Where do findings, interpretations, or recommendations conflict? Characterize the nature of the disagreement.

4. **Methodological Comparison**: How do the approaches differ? Consider:
   - Study systems/organisms
   - Sample sizes and designs
   - Analytical techniques
   - Outcome measures

5. **Gaps and Limitations**: What questions remain unaddressed across this literature? What limitations are shared?

6. **Synthesis Statement**: Two to three sentences capturing the bottom line for {YOUR_SPECIFIC_RESEARCH_QUESTION}.

Constraints:
- Use ONLY information from the papers I have provided
- Do NOT introduce findings, citations, or context from other sources
- When attributing a claim to a paper, be specific (e.g., "Smith et al. found..." not "studies show...")
- If papers contradict each other, present both positions without resolving the disagreement
- If you cannot determine something from the provided texts, state this explicitly

Output format: Use the numbered structure above. For Points of Agreement and Disagreement, use bullet points with specific paper attributions.
```

## Prompt Components Explained

| Component | Purpose |
|-----------|---------|
| **Context** | Specifies the purpose of synthesis, which affects framing and emphasis |
| **Paper texts provided** | Full text ensures the model works from your sources, not its training data |
| **Specific synthesis focus** | Narrows the comparison to a tractable question rather than "compare everything" |
| **Constraints** | "ONLY information from papers provided" is critical—prevents hallucinated citations and fabricated findings |
| **Attribution requirement** | "Be specific about which papers" creates verifiable claims |
| **Output format** | Structured sections ensure comprehensive coverage and facilitate verification |

## Example Output

For a representative model response to the Test Input, see:

`tests/literature/synthesis-across-papers/claude-sonnet-4-6-2026-06-25.md`

That cell was captured on 2026-06-25 and human-verified by both project reviewers as passing. Other panel models' responses (Claude Opus 4.7, GPT-5.5, Gemini 2.5 Pro, Nemotron 3 Super 120B, Step-3.7 Flash) are alongside it in the same directory.

## Test Input

Use the following simulated paper summaries to test this prompt:

```
Context: I am synthesizing literature on antibiotic effects on the gut microbiome for a review section. I have read the following papers and am providing summaries below.

Papers provided:

**Paper 1 Summary:**
Anderson et al. (2023). "Broad-spectrum antibiotics cause rapid and persistent microbiome disruption in healthy adults."
- Study: 30 healthy adults given 7-day amoxicillin course
- Finding: 50% reduction in bacterial diversity within 3 days
- Recovery: Partial recovery by 30 days, but some taxa remained depleted at 90 days
- Notable: Proteobacteria expanded during treatment; Bacteroides recovery was slowest

---
**Paper 2 Summary:**
Martinez & Lee (2022). "Microbiome resilience varies by antibiotic class and host factors."
- Study: Meta-analysis of 12 studies (n=340 total subjects)
- Finding: Macrolides caused less diversity loss than fluoroquinolones
- Recovery: Younger subjects (<40) showed faster recovery (mean 21 days vs 45 days)
- Notable: Prior antibiotic exposure associated with slower recovery

---
**Paper 3 Summary:**
Thompson et al. (2024). "Probiotic co-administration does not prevent antibiotic-induced dysbiosis."
- Study: RCT, 60 subjects, probiotic vs placebo during antibiotic treatment
- Finding: No significant difference in diversity loss between groups
- Recovery: Similar recovery trajectories in both arms
- Notable: Probiotic strains did not engraft during antibiotic treatment

Synthesis focus: What is known about microbiome recovery after antibiotic exposure?

My specific research question: Whether there are interventions that could accelerate microbiome recovery.

Task: Synthesize these papers with respect to what is known about microbiome recovery after antibiotic exposure. Structure your synthesis as follows:

1. **Overview**: One paragraph summarizing the collective state of knowledge across these papers.

2. **Points of Agreement**: What do these papers consistently find or conclude? Be specific about which papers support each point.

3. **Points of Disagreement or Tension**: Where do findings, interpretations, or recommendations conflict? Characterize the nature of the disagreement.

4. **Methodological Comparison**: How do the approaches differ? Consider:
   - Study systems/organisms
   - Sample sizes and designs
   - Analytical techniques
   - Outcome measures

5. **Gaps and Limitations**: What questions remain unaddressed across this literature? What limitations are shared?

6. **Synthesis Statement**: Two to three sentences capturing the bottom line for whether there are interventions that could accelerate microbiome recovery.

Constraints:
- Use ONLY information from the papers I have provided
- Do NOT introduce findings, citations, or context from other sources
- When attributing a claim to a paper, be specific (e.g., "Smith et al. found..." not "studies show...")
- If papers contradict each other, present both positions without resolving the disagreement
- If you cannot determine something from the provided texts, state this explicitly

Output format: Use the numbered structure above. For Points of Agreement and Disagreement, use bullet points with specific paper attributions.
```

**Expected output should include:**
- Overview paragraph synthesizing all three papers
- Points of agreement: All show antibiotics disrupt microbiome; recovery takes weeks to months
- Points of disagreement: Different recovery timelines across studies (potentially explained by antibiotic class, per Paper 2)
- Methodological comparison table noting study types, sample sizes, antibiotics used
- Gaps: No effective intervention identified; Thompson et al. shows probiotics don't help
- Synthesis statement addressing the specific research question

**Verification points:**
- All attributions match the correct paper
- No outside sources or citations introduced
- Disagreements accurately characterized
- Synthesis statement follows from the evidence presented

## Failure Modes

- **Citation fabrication**: May introduce papers not in your provided set, especially when claiming "other studies show..."
- **False consensus**: May overstate agreement when studies measured different things or used different definitions
- **Oversimplification of disagreement**: May miss subtle but important methodological differences that explain conflicting results
- **Sycophancy toward your hypothesis**: If your research question implies a desired answer, may emphasize supportive evidence
- **Context truncation**: With multiple long papers, may incompletely process later papers or later sections
- **Attribution errors**: May attribute findings to the wrong paper in the set

## Verification Requirements

1. **Verify all paper attributions**: Check that each "Smith et al. found X" claim matches what that paper actually says
2. **Check for introduced sources**: Search the output for any citations not in your provided set—these are likely fabricated
3. **Verify the disagreements**: Confirm that papers actually conflict where the synthesis claims they do
4. **Check for omitted findings**: Review your papers for major results not captured in the synthesis
5. **Verify the synthesis statement**: Ensure the bottom-line conclusion is supported by the evidence presented

**Critical**: If you plan to cite these papers in your writing, verify every specific claim against the original papers. The synthesis is a scaffold, not a substitute for proper citation practices.

## Variations

### Focused methodological comparison
Replace sections 2-3 with expanded methodological analysis: protocols, sample handling, sequencing approaches, statistical methods, reproducibility features.

### Controversy mapping
For contentious topics, add: "Key Debates" section explicitly mapping the positions, proponents, and evidence on each side.

### Evidence grading
Add a section rating the strength of evidence for each major claim using a simple scale (strong/moderate/weak/insufficient).

### Smaller synthesis (2-3 papers)
Reduce to: Overview, Key Agreements, Key Differences, Implications for Your Work.

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

Full per-model raw outputs and reviewer notes: tests/literature/synthesis-across-papers/
```

## Cross-References

- For summarizing individual papers before synthesis, see `literature/paper-summary.md`
- For identifying gaps to pursue, see `literature/gap-identification.md`
- For verifying citations in the synthesis, see `guides/citation-warning.md`
- For having another model critique the synthesis, see `validation/adversarial-critique.md`
