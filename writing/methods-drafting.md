# Methods Section Drafting Prompt

## Task Description

Generate a structured first draft of a Methods section from detailed notes, protocols, or bullet points, producing clear technical prose that can be refined into publication-ready text.

## When to Use

- Converting lab notebook entries or protocol documents into Methods prose
- Structuring a Methods section from scattered notes across multiple experiments
- Ensuring all required methodological details are captured before refinement
- Overcoming blank-page paralysis when you know what you did but struggle to write it

## When NOT to Use

- When you lack detailed notes about your actual procedures (garbage in, garbage out)
- To fabricate or embellish methods you didn't actually perform
- For methods outside your expertise where you can't verify technical accuracy
- As a substitute for understanding what you did and why

## The Prompt

```
Context: I am preparing a Methods section for a manuscript on {RESEARCH_TOPIC} targeting {JOURNAL_TYPE: e.g., "a microbiology journal," "a broad-audience journal like Nature Communications"}. Below are my detailed notes on the methods I used.

My notes:
{DETAILED_NOTES}

Task: Draft a Methods section based on my notes. Structure the section with the following subsections:

1. {SUBSECTION_1: e.g., "Study Design and Sample Collection"}
2. {SUBSECTION_2: e.g., "DNA Extraction and Sequencing"}
3. {SUBSECTION_3: e.g., "Bioinformatic Analysis"}
4. {SUBSECTION_4: e.g., "Statistical Analysis"}
[Adjust subsections to match your study]

For each subsection:
- Write in past tense, passive or active voice as appropriate for the target journal
- Include specific details: reagent names, concentrations, instrument settings, software versions
- State the purpose of each step where not obvious
- Note sample sizes and replicates

Constraints:
- Use ONLY information from my notes—do not add steps, reagents, or parameters I didn't specify
- If my notes are missing critical details, flag them as [MISSING: description] rather than inventing values
- Do not add interpretation or results—this is Methods only
- Keep prose clear and direct; avoid unnecessary hedging

Output format: Structured prose with subsection headers. Flag any gaps or ambiguities for my attention.
```

## Prompt Components Explained

| Component | Purpose |
|-----------|---------|
| **Context** | Journal type affects style and expected detail level |
| **Detailed notes** | The raw material—quality of output depends entirely on quality of input |
| **Explicit subsections** | Ensures structure matches your study design and journal expectations |
| **Constraints** | "ONLY from my notes" prevents hallucinated methods; [MISSING] flags prevent fabrication |
| **Output format** | Prose with headers produces a usable first draft |

## Example Output

For a representative model response to the Test Input, see:

`tests/writing/methods-drafting/claude-sonnet-4-6-2026-06-25.md`

That cell was captured on 2026-06-25 and human-verified by both project reviewers as passing. Other panel models' responses (Claude Opus 4.7, GPT-5.5, Gemini 2.5 Pro, Nemotron 3 Super 120B, Step-3.7 Flash) are alongside it in the same directory.

## Test Input

Use the following notes to test this prompt:

```
Context: I am preparing a Methods section for a manuscript on fecal microbiota transplantation efficacy targeting a clinical microbiology journal. Below are my detailed notes.

My notes:

Study design:
- Randomized, double-blind, placebo-controlled trial
- Patients with recurrent C. difficile infection (≥3 episodes)
- Enrolled at two academic medical centers

Participants:
- n=48 patients randomized (24 FMT, 24 placebo)
- Age 18-75, both sexes
- Exclusion: immunocompromised, pregnant, IBD

FMT preparation:
- Single healthy donor, screened per FDA guidelines
- Fresh stool processed within 6 hours
- Mixed with saline, filtered, 50mL final volume

Intervention:
- FMT or placebo via colonoscopy
- Placebo was saline with food coloring to match appearance
- Patients blinded to allocation

Outcomes:
- Primary: CDI recurrence within 8 weeks
- Secondary: microbiome diversity at weeks 1, 4, 8

Sample collection:
- Stool samples at baseline, week 1, 4, 8
- Stored -80C within 2 hours

Microbiome analysis:
- DNA extraction: MoBio PowerFecal kit
- 16S V4 region, 515F/806R primers
- Illumina MiSeq 2x250bp
- QIIME2 with DADA2 for ASV inference

Task: Draft a Methods section based on my notes. Structure the section with the following subsections:

1. Study Design and Participants
2. FMT Preparation and Administration
3. Outcome Measures
4. Microbiome Analysis
5. Statistical Analysis [notes missing for this]

For each subsection:
- Write in past tense, passive or active voice as appropriate for the target journal
- Include specific details: reagent names, concentrations, instrument settings, software versions
- State the purpose of each step where not obvious
- Note sample sizes and replicates

Constraints:
- Use ONLY information from my notes—do not add steps, reagents, or parameters I didn't specify
- If my notes are missing critical details, flag them as [MISSING: description] rather than inventing values
- Do not add interpretation or results—this is Methods only
- Keep prose clear and direct; avoid unnecessary hedging

Output format: Structured prose with subsection headers. Flag any gaps or ambiguities for my attention.
```

**Expected output should include:**
- All provided details incorporated accurately
- [MISSING: IACUC/IRB approval number]
- [MISSING: Statistical Analysis section details]
- [MISSING: Clinical trial registration number]
- No fabricated details (concentrations, volumes, timings not in notes)

**Verification points:**
- Every specific value matches the input notes exactly
- All [MISSING] flags identify genuine gaps in the notes
- No interpretation or results content included
- Appropriate past tense, passive voice for clinical methods

## Failure Modes

- **Fabricating details**: May invent specific concentrations, incubation times, or instrument settings not in your notes
- **Adding interpretation**: May include phrases like "to ensure adequate..." or "which confirmed..." that belong in Results
- **Standardizing incorrectly**: May use generic protocols when your actual methods differed
- **Missing the missing**: May not flag all gaps—some may be silently filled with plausible but incorrect defaults
- **Over-hedging**: May add unnecessary caveats ("approximately," "roughly") when you have exact values

## Verification Requirements

1. **Verify every specific value**: Check concentrations, temperatures, times, sample sizes against your actual records
2. **Check reagent/kit names**: Confirm exact product names and catalog numbers if required
3. **Verify software versions**: Confirm you used the versions stated
4. **Address all [MISSING] flags**: Fill in from your records or note if information is genuinely unavailable
5. **Check for additions**: Compare to your notes—remove anything added that you didn't actually do
6. **Read for interpretation creep**: Ensure no results or conclusions snuck into the Methods

## Variations

### Computational methods focus
For bioinformatics-heavy papers, expand computational subsection structure:
- Data preprocessing and quality control
- Taxonomic/functional assignment
- Statistical analysis
- Software and code availability

### Brief methods (for journals with limits)
Add constraint: "Keep total Methods under 500 words. Prioritize reproducibility-critical details; refer to Supplementary Methods for full protocols."

### Supplementary methods
For extended protocols: "Write in sufficient detail that another lab could reproduce the experiment without additional information."

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

Full per-model raw outputs and reviewer notes: tests/writing/methods-drafting/
```

## Cross-References

- For results section drafting, see `writing/results-description.md`
- For documenting LLM assistance in Methods, see `documentation/methods-disclosure-template.md`
- For grant methods sections, see `writing/specific-aims.md`
