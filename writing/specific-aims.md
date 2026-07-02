# Specific Aims Page Drafting Prompt

## Task Description

Generate a structured first draft of a grant Specific Aims page from your research plan notes, producing the conventional structure (opening paragraph, aims, closing) that can be refined into a compelling funding request.

## When to Use

- Converting a research plan into Specific Aims format
- Structuring your thinking about how aims relate to each other
- Drafting when you know your science but struggle with grant rhetoric
- Checking that your aims are logically connected and appropriately scoped

## When NOT to Use

- When you haven't developed the research plan yourself (this structures your ideas, doesn't generate them)
- To fabricate preliminary data or cite papers you haven't read
- For aims outside your expertise where you can't evaluate feasibility claims
- As a substitute for understanding the funding agency's priorities

## The Prompt

```
Context: I am drafting a Specific Aims page for a {GRANT_TYPE: e.g., "NIH R01," "NSF CAREER," "foundation grant"} on {RESEARCH_TOPIC}. The funding agency emphasizes {AGENCY_PRIORITIES: e.g., "mechanistic understanding," "translational potential," "innovative methods"}.

My research plan notes:
{YOUR_NOTES: Include the problem, your approach, preliminary data if any, and what each aim will accomplish}

Target length: {LENGTH: e.g., "1 page," "500 words"}

Task: Draft a Specific Aims page with the following structure:

**Opening paragraph (The Hook):**
- First sentence: Establish the problem and its significance (the "so what")
- Knowledge gap: What critical barrier limits progress?
- Your solution: How does your approach address this gap?
- Long-term goal and overall objective for this proposal

**Specific Aims (2-3 typically):**
For each aim:
- State the aim as a clear objective (what you will do)
- Brief rationale (why this aim matters)
- Approach summary (1-2 sentences on how)
- Expected outcome (what you'll learn)

**Closing paragraph:**
- How the aims integrate and build on each other
- Impact statement: what will be possible after this work that isn't possible now?
- Connection to agency mission (if applicable)

Constraints:
- Use ONLY information from my notes—do not fabricate preliminary data, citations, or capabilities
- Flag any claims that need preliminary data support as [NEEDS PRELIM DATA]
- Flag any citations needed as [CITE]
- Keep within target length
- Use active, confident language—avoid excessive hedging
- Make aims concrete and achievable within the funding period

Output format: Formatted aims page with section headers. Flag gaps for my attention.
```

## Prompt Components Explained

| Component | Purpose |
|-----------|---------|
| **Grant type and agency** | Different agencies have different expectations and rhetoric |
| **Agency priorities** | Tailors framing to what reviewers value |
| **Your research plan notes** | The substance—LLM structures but doesn't invent science |
| **Target length** | Specific Aims are typically strictly length-limited |
| **Structural template** | Conventional aims page structure that reviewers expect |
| **Constraints** | Prevent fabrication; flag gaps rather than fill them with invention |

## Example Output

For a representative model response to the Test Input, see:

`tests/writing/specific-aims/claude-sonnet-4-6-2026-06-25.md`

That cell was captured on 2026-06-25 and human-verified by both project reviewers as passing. Other panel models' responses (Claude Opus 4.7, GPT-5.5, Gemini 2.5 Pro, Nemotron 3 Super 120B, Step-3.7 Flash) are alongside it in the same directory.

## Test Input

Use the following notes to test this prompt:

```
Context: I am drafting a Specific Aims page for an NIH R21 (exploratory/developmental) on microbiome biomarkers for colorectal cancer screening. The funding agency emphasizes innovative approaches and high-risk/high-reward research.

My research plan notes:

Problem: Colorectal cancer is the 2nd leading cause of cancer death in the US. Colonoscopy screening is effective but has low compliance (~60%). Non-invasive biomarkers could improve screening rates. Current fecal tests (FIT, Cologuard) have limited sensitivity for adenomas.

My approach: Develop a microbiome-based classifier that detects precancerous adenomas from stool samples. Leverage the known microbiome changes in CRC to detect disease earlier.

Preliminary data:
- Pilot study with 25 adenoma cases, 25 controls
- 16S sequencing identified 12 differentially abundant taxa
- Random forest classifier achieved 78% AUC (needs validation)

Aim 1: Validate and refine the microbiome classifier in an independent cohort
- Partner with GI clinic for prospective sample collection
- Target 100 adenoma cases, 100 controls
- Test classifier performance and refine features

Aim 2: Integrate microbiome data with existing biomarkers (FIT)
- Hypothesis: combined model outperforms either alone
- Collect FIT results alongside microbiome samples
- Build integrated classifier

Innovation: First study to combine microbiome signatures with established screening biomarkers for adenoma detection

My lab: expertise in microbiome bioinformatics, machine learning, established GI collaborations

Target length: 1 page (R21 limit)

Task: Draft a Specific Aims page with the following structure:

**Opening paragraph (The Hook):**
- First sentence: Establish the problem and its significance (the "so what")
- Knowledge gap: What critical barrier limits progress?
- Your solution: How does your approach address this gap?
- Long-term goal and overall objective for this proposal

**Specific Aims (2-3 typically):**
For each aim:
- State the aim as a clear objective (what you will do)
- Brief rationale (why this aim matters)
- Approach summary (1-2 sentences on how)
- Expected outcome (what you'll learn)

**Closing paragraph:**
- How the aims integrate and build on each other
- Impact statement: what will be possible after this work that isn't possible now?
- Connection to agency mission (if applicable)

Constraints:
- Use ONLY information from my notes—do not fabricate preliminary data, citations, or capabilities
- Flag any claims that need preliminary data support as [NEEDS PRELIM DATA]
- Flag any citations needed as [CITE]
- Keep within target length
- Use active, confident language—avoid excessive hedging
- Make aims concrete and achievable within the funding period

Output format: Formatted aims page with section headers. Flag gaps for my attention.
```

**Expected output should include:**
- Appropriate hook establishing the screening compliance problem
- Clear knowledge gap (current tests miss adenomas)
- Reference to preliminary data with [NEEDS PRELIM DATA] flags for specific numbers
- Two aims appropriate for R21 scope (exploratory, 2-year timeline)
- [CITE] flags for statistics (CRC death rates, colonoscopy compliance)
- Innovation statement
- Impact statement appropriate for exploratory mechanism

**Verification points:**
- All preliminary data numbers match input exactly (25/25, 12 taxa, 78% AUC)
- Scope appropriate for R21 (not overambitious)
- No fabricated capabilities or collaborations beyond what's stated
- Appropriate [CITE] and [NEEDS PRELIM DATA] flags

## Failure Modes

- **Fabricating preliminary data**: May invent pilot results you didn't provide
- **Inventing citations**: May create fake references to support claims
- **Over-promising**: May claim achievable outcomes beyond what's realistic
- **Generic framing**: May produce boilerplate that doesn't capture what's innovative about your work
- **Misrepresenting expertise**: May claim capabilities you didn't mention having
- **Ignoring scope**: May produce aims too large for the funding mechanism
- **Sycophantic enthusiasm**: May oversell significance rather than make a measured case

## Verification Requirements

1. **Verify all claims**: Every factual statement should be either from your notes or flagged for citation
2. **Check preliminary data references**: Ensure any mentioned prelim data exists and is accurately described
3. **Verify feasibility**: Confirm you actually have the expertise, resources, and access claimed
4. **Check scope**: Ensure aims are achievable in the funding period (typically 3-5 years for R01)
5. **Verify no fabrication**: Compare to your notes—remove anything substantive that was added
6. **Test the logic**: Confirm aims actually build on each other as claimed
7. **Check institutional claims**: Verify references to your capabilities are accurate

## Variations

### R21/exploratory mechanism
For smaller, exploratory grants:
```
Constrain to 2 aims. Emphasize innovation and risk-taking over guaranteed outcomes. Frame as establishing feasibility for larger proposals.
```

### Foundation grants
For foundation or philanthropic funding:
```
Emphasize patient impact and translational timeline. Reduce jargon. Include a patient-facing impact statement.
```

### Renewal/competing continuation
For renewing an existing project:
```
Include: progress on previous aims, what new questions emerged, how proposed aims build on established work. Reference publications and preliminary data from the previous funding period.
```

### Multiple PI structure
For collaborative proposals:
```
Clarify which PI leads each aim. Include integration plan describing how the team will work together.
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

Full per-model raw outputs and reviewer notes: tests/writing/specific-aims/
```

## Cross-References

- For methods sections in grant proposals, see `writing/methods-drafting.md`
- For literature synthesis supporting significance, see `literature/synthesis-across-papers.md`
- For identifying gaps that motivate your aims, see `literature/gap-identification.md`
- For critique of your aims before submission, see `validation/adversarial-critique.md`
