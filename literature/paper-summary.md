# Paper Summary Prompt

## Task Description

Generate a structured summary of a single research paper, extracting key findings, methods, and limitations in a format suitable for literature review notes.

## When to Use

- Building a personal literature database with consistent annotations
- Preparing to synthesize multiple papers on a topic
- Creating reading notes for lab meetings or journal clubs
- Quickly capturing the essence of a paper you've read but need to document

## When NOT to Use

- As a substitute for reading the paper yourself (the summary is only useful if you can verify it)
- For papers outside your expertise where you cannot evaluate accuracy
- When you need to cite specific claims (verify against the original, not the summary)
- For systematic reviews requiring standardized extraction protocols (use domain-specific tools)

## The Prompt

```
Context: I am a {RESEARCHER_ROLE} reviewing literature on {RESEARCH_TOPIC}. I need a structured summary of the following paper for my literature notes.

Paper text:
{PAPER_TEXT}

Task: Summarize this paper using the following structure.

1. **Citation**: Format as: Authors (Year). Title. Journal.

2. **Central Finding**: One to two sentences stating the main result or conclusion. Be specific about what was found, not just what was studied.

3. **Research Question/Hypothesis**: What question did the authors set out to answer?

4. **Methods Overview**:
   - Study system/organism
   - Key techniques or approaches
   - Sample size and design (if applicable)

5. **Key Results**: Three to five bullet points of specific findings. Include effect sizes or quantitative results where available.

6. **Limitations**: What limitations do the authors acknowledge? What limitations are apparent but not discussed?

7. **Open Questions**: What questions remain unanswered? What would logical next steps be?

8. **Relevance to My Work**: How might this paper inform {SPECIFIC_ASPECT_OF_YOUR_RESEARCH}?

Constraints:
- Use only information present in the paper—do not add context from other sources
- If a section cannot be completed from the available text, state "Not available in provided text"
- Distinguish between what authors claim and what the data support
- Note if sample sizes or effect sizes are not reported

Output format: Use the numbered structure above with headers in bold.
```

## Prompt Components Explained

| Component | Purpose |
|-----------|---------|
| **Context** | Frames the summarization for your specific research area, improving relevance of the "Relevance to My Work" section |
| **Task Specification** | The 8-point structure ensures consistent, comparable summaries across papers |
| **Constraints** | "Use only information present" prevents hallucination; "If not available, state so" prevents fabrication of missing details |
| **Output Format** | Explicit structure produces consistent outputs suitable for a literature database |

## Example Output

For a representative model response to the Test Input, see:

`tests/literature/paper-summary/claude-sonnet-4-6-2026-06-25.md`

That cell was captured on 2026-06-25 and human-verified by both project reviewers as passing. Other panel models' responses (Claude Opus 4.7, GPT-5.5, Gemini 2.5 Pro, Nemotron 3 Super 120B, Step-3.7 Flash) are alongside it in the same directory.

## Test Input

Use the following simulated paper excerpt to test this prompt:

```
Context: I am a microbiome researcher reviewing literature on diet-microbiome interactions. I need a structured summary of the following paper for my literature notes.

Paper text:
[SIMULATED PAPER EXCERPT]

Title: Short-chain fatty acid production is reduced in patients with irritable bowel syndrome and correlates with symptom severity

Authors: Chen Y, Roberts K, Nakamura T, Wilson D, et al.

Abstract: Background: Irritable bowel syndrome (IBS) affects 10-15% of the global population, but its etiology remains unclear. Gut microbiome alterations have been implicated, yet functional consequences are understudied. We investigated short-chain fatty acid (SCFA) production in IBS patients versus healthy controls.

Methods: We recruited 45 IBS patients (Rome IV criteria) and 40 age- and sex-matched healthy controls. Fecal samples were analyzed using 16S rRNA gene sequencing (V4 region, Illumina MiSeq) and gas chromatography for SCFA quantification. Symptom severity was assessed using the IBS Severity Scoring System (IBS-SSS).

Results: IBS patients showed significantly reduced fecal butyrate (p=0.003) and propionate (p=0.02) compared to controls, while acetate levels were similar. Butyrate concentration negatively correlated with IBS-SSS scores (r=-0.42, p=0.004). Patients with IBS showed depletion of Faecalibacterium prausnitzii and Roseburia species, both known butyrate producers. No significant differences were observed in alpha diversity metrics (Shannon, observed ASVs).

Discussion: Our findings suggest that reduced SCFA production, particularly butyrate, may contribute to IBS symptoms. The correlation with symptom severity supports a functional role for these metabolites. Limitations include the cross-sectional design, which cannot establish causality, and recruitment from a single clinical center. Future longitudinal studies and intervention trials targeting SCFA production are warranted.

Relevance aspect: how microbial metabolites affect gut health in my mouse models

Task: Summarize this paper using the following structure.

1. **Citation**: Format as: Authors (Year). Title. Journal.

2. **Central Finding**: One to two sentences stating the main result or conclusion. Be specific about what was found, not just what was studied.

3. **Research Question/Hypothesis**: What question did the authors set out to answer?

4. **Methods Overview**:
   - Study system/organism
   - Key techniques or approaches
   - Sample size and design (if applicable)

5. **Key Results**: Three to five bullet points of specific findings. Include effect sizes or quantitative results where available.

6. **Limitations**: What limitations do the authors acknowledge? What limitations are apparent but not discussed?

7. **Open Questions**: What questions remain unanswered? What would logical next steps be?

8. **Relevance to My Work**: How might this paper inform how microbial metabolites affect gut health in my mouse models?

Constraints:
- Use only information present in the paper—do not add context from other sources
- If a section cannot be completed from the available text, state "Not available in provided text"
- Distinguish between what authors claim and what the data support
- Note if sample sizes or effect sizes are not reported

Output format: Use the numbered structure above with headers in bold.
```

**Expected output should include:**
- Correct citation format with all authors listed
- Central finding about reduced SCFAs correlating with IBS symptoms
- Methods noting sample sizes (45 IBS, 40 controls), 16S sequencing, GC for SCFAs
- Key results with specific statistics (p=0.003 for butyrate, r=-0.42 correlation)
- Limitations section including cross-sectional design, single center
- Appropriate relevance statement connecting to mouse model work

**Verification points:**
- All statistics match the provided text exactly
- No information is fabricated beyond what's in the excerpt
- "Not available in provided text" used appropriately for any gaps

## Failure Modes

- **Hallucination risks**: May fabricate specific statistics, p-values, or sample sizes not present in the paper. May invent author conclusions or claims.
- **Misrepresentation**: May oversimplify nuanced findings or miss important caveats the authors provide.
- **Overconfidence**: May present uncertain or preliminary findings as established results.
- **Context truncation**: For very long papers, may miss information from later sections (particularly limitations and discussion).

## Verification Requirements

1. **Verify the citation**: Check that authors, year, title, and journal are correct
2. **Spot-check key results**: Compare 2-3 specific claims against the original paper
3. **Verify limitations**: Ensure stated limitations actually appear in the paper
4. **Check for omissions**: Scan the original for major findings not captured in the summary
5. **If you will cite this summary**: Verify every specific claim against the original before use

## Variations

### Shorter summary (for rapid screening)
Remove sections 4, 7, and 8. Keep only: Citation, Central Finding, Key Results (3 bullets max), Limitations.

### Methods-focused summary (for replication)
Expand section 4 to include: detailed protocols, reagents, analysis pipelines, software versions, and statistical approaches.

### Critical reading summary
Add a section: "Strengths and Weaknesses of Study Design" with explicit evaluation of internal and external validity.

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

Full per-model raw outputs and reviewer notes: tests/literature/paper-summary/
```

## Cross-References

- For synthesizing multiple paper summaries, see `literature/synthesis-across-papers.md`
- For identifying gaps across papers, see `literature/gap-identification.md`
- For verifying any citations in outputs, see `guides/citation-warning.md`
- For critiquing the summary output, see `validation/adversarial-critique.md`
