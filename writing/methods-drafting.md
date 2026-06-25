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

## Example Input

```
Context: I am preparing a Methods section for a manuscript on gut microbiome changes in antibiotic-treated mice targeting a microbiology journal. Below are my detailed notes.

My notes:

Animals:
- C57BL/6J mice, 8 weeks old, male, from Jackson Labs
- Housed 4/cage, 12h light/dark, standard chow (LabDiet 5010)
- n=10 per group (control, antibiotic)
- 7-day acclimation before experiment

Antibiotic treatment:
- Ampicillin 1g/L in drinking water, 7 days
- Control got regular water
- Water changed every 2 days
- Monitored water consumption daily

Sample collection:
- Fecal pellets collected day 0, 3, 7
- Fresh pellets, 2 per mouse per timepoint
- Snap frozen in liquid nitrogen, stored -80C

DNA extraction:
- Used QIAGEN DNeasy PowerSoil Pro kit
- Followed manufacturer protocol
- Quantified with Qubit dsDNA HS assay
- Checked quality on Nanodrop (260/280 ratios)

Sequencing:
- 16S V4 region
- Primers: 515F/806R (Caporaso et al.)
- Illumina MiSeq, 2x250bp paired-end
- Sequenced at OSU CGRB

Subsections needed:
1. Animals and Housing
2. Antibiotic Treatment
3. Sample Collection
4. DNA Extraction and 16S rRNA Gene Sequencing
```

## Example Output

### Animals and Housing

Male C57BL/6J mice (8 weeks old) were obtained from Jackson Laboratories. Mice were housed four per cage under a 12-hour light/dark cycle with ad libitum access to standard chow (LabDiet 5010) and water. Animals were acclimated to the facility for 7 days before the start of the experiment. All experiments included n=10 mice per treatment group.

[MISSING: IACUC protocol number and institutional approval statement]

### Antibiotic Treatment

Mice in the antibiotic group received ampicillin (1 g/L) in drinking water for 7 days. Control mice received untreated drinking water. Water bottles were replaced every 2 days, and water consumption was monitored daily to ensure adequate antibiotic intake.

### Sample Collection

Fresh fecal pellets (2 pellets per mouse) were collected on days 0, 3, and 7 of treatment. Samples were snap-frozen in liquid nitrogen immediately upon collection and stored at -80°C until DNA extraction.

### DNA Extraction and 16S rRNA Gene Sequencing

DNA was extracted from fecal pellets using the DNeasy PowerSoil Pro kit (QIAGEN) according to the manufacturer's protocol. DNA concentration was measured using the Qubit dsDNA HS assay (Thermo Fisher Scientific), and purity was assessed by 260/280 absorbance ratio on a NanoDrop spectrophotometer.

The V4 region of the 16S rRNA gene was amplified using the 515F/806R primer pair [MISSING: cite Caporaso et al. with year]. Amplicon libraries were sequenced on an Illumina MiSeq platform using 2×250 bp paired-end chemistry at the Oregon State University Center for Quantitative Life Sciences [MISSING: verify current name of sequencing core].

[MISSING: Library preparation details—was there a specific kit? Index strategy?]
[MISSING: Sequencing depth target or actual reads obtained]

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

Subsections needed:
1. Study Design and Participants
2. FMT Preparation and Administration
3. Outcome Measures
4. Microbiome Analysis
5. Statistical Analysis [notes missing for this]
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
- claude-opus-4.7 (2026-06-23): Pass
- claude-sonnet-4.6 (2026-06-23): Pass
- gemini-2.5-pro (2026-06-23): Pass
- gpt-5.5 (2026-06-23): Pass
- nemotron-3-super-120b (2026-06-23): Pass
- step-3.7-flash (2026-06-23): Pass

Full per-model raw outputs and reviewer notes: tests/writing/methods-drafting/
```

## Cross-References

- For results section drafting, see `writing/results-description.md`
- For documenting LLM assistance in Methods, see `documentation/methods-disclosure-template.md`
- For grant methods sections, see `writing/specific-aims.md`
