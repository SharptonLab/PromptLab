# Test Results: writing/methods-drafting.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-25.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** writing/methods-drafting.md
- **Model:** nemotron-3-super-120b
- **Model ID (pinned):** Nemotron-3-Super-120B-A12B-NVFP4
- **Endpoint:** https://copilot-dev.cqls.oregonstate.edu/llm/nemotron3-super-120b-nvfp4/v1
- **Date:** 2026-06-25
- **Tester:** cross-model-harness
- **Assembly strategy:** test-only
- **Temperature:** 0.0

## Test Input Used
Standard test input from prompt file (`## Test Input`).

## Filled Prompt
````
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
````

## Model Output
````


**Study Design and Participants**  
A randomized, double‑blind, placebo‑controlled trial was conducted at two academic medical centers. Patients with recurrent *Clostridioides difficile* infection (≥3 episodes) were enrolled. Eligible participants were aged 18–75 years, of either sex, and were excluded if they were immunocompromised, pregnant, or had inflammatory bowel disease. A total of 48 patients were randomized, receiving either fecal microbiota transplantation (FMT) or placebo (n = 24 per group).

**FMT Preparation and Administration**  
Stool from a single healthy donor, screened according to FDA guidelines, was collected and processed within 6 hours of defecation. The fresh stool was mixed with sterile saline, filtered to remove particulate matter, and adjusted to a final volume of 50 mL. The FMT preparation was administered via colonoscopy. The placebo consisted of sterile saline containing food coloring to match the visual appearance of the FMT preparation. Patients and study personnel were blinded to group allocation throughout the intervention.

**Outcome Measures**  
The primary outcome was the occurrence of *C. difficile* infection recurrence within 8 weeks after treatment. Secondary outcomes included assessment of microbiome diversity at weeks 1, 4, and 8. Stool samples were collected at baseline and at weeks 1, 4, and 8 for each participant. All samples were placed at −80 °C within 2 hours of collection.

**Microbiome Analysis**  
Total DNA was extracted from stool samples using the MoBio PowerFecal kit. The V4 region of the 16S rRNA gene was amplified with the primers 515F and 806R. Amplicons were sequenced on an Illumina MiSeq instrument using a 2 × 250 bp paired‑end run. Resulting reads were processed with QIIME2, employing the DADA2 algorithm to infer amplicon sequence variants (ASVs).

**Statistical Analysis**  
[MISSING: description of statistical tests, software, significance level, handling of missing data, and any adjustments for multiple comparisons.]
````

## Assessment
_To be completed by a human reviewer. Do not mark Pass without reading the output._

### Task Achievement
- **Achieved:** [Yes / No / Partial]
- **Notes:**

### Constraint Compliance
- **All constraints respected:** [Yes / No]
- **Violations noted:**

### Failure Modes
- **Failure modes observed:** [None / list]
- **Mitigation effectiveness:**

### Output Format
- **Format correct:** [Yes / No]
- **Deviations:**

## Overall Assessment
- **Recommendation:** PENDING AUTHOR REVIEW
- **Notes:**

## Verification Steps Tested
_Which verification requirements from the prompt were checked, and results._
