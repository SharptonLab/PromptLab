# Test Results: writing/methods-drafting.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-25.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** writing/methods-drafting.md
- **Model:** claude-sonnet-4.6
- **Model ID (pinned):** claude-sonnet-4-6
- **Endpoint:** native
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
# Methods

---

## 1. Study Design and Participants

This study was a randomized, double-blind, placebo-controlled trial conducted at two academic medical centers. Eligible participants were adults aged 18–75 years with recurrent *Clostridioides difficile* infection (CDI), defined as three or more episodes. Patients were excluded if they were immunocompromised, pregnant, or had a diagnosis of inflammatory bowel disease. A total of 48 participants were enrolled and randomized in a 1:1 ratio to receive either fecal microbiota transplantation (FMT; n = 24) or placebo (n = 24).

**Flags for your attention:**
- [MISSING: Randomization method — how was allocation generated (e.g., block randomization, stratified by site or age)? Reviewers will expect this.]
- [MISSING: Allocation concealment procedure — how was the sequence concealed from enrolling clinicians?]
- [MISSING: Who was blinded — were endoscopists blinded, or only patients? The notes state patients were blinded; clarify whether clinicians assessing outcomes were also blinded, as this affects the validity of the "double-blind" claim.]
- [MISSING: Ethical approval — IRB/ethics committee name, approval number, and whether written informed consent was obtained. This is required by most clinical journals.]
- [MISSING: Trial registration — registry name and identifier (e.g., ClinicalTrials.gov NCT number).]
- [MISSING: Definition of "recurrent CDI" — was this defined by positive toxin assay, PCR, or clinical criteria? Specify the diagnostic standard used for enrollment.]

---

## 2. FMT Preparation and Administration

Donor stool was obtained from a single healthy donor screened according to current U.S. Food and Drug Administration (FDA) guidelines for FMT donors. Fresh stool was processed within six hours of collection. The stool was homogenized with sterile saline [MISSING: saline concentration — presumably 0.9% NaCl, but confirm], filtered to remove particulate matter [MISSING: filter pore size or filtration method], and brought to a final volume of 50 mL for administration.

Participants randomized to FMT received the prepared suspension via colonoscopy. Participants randomized to placebo received 50 mL of sterile saline with food coloring added to match the visual appearance of the FMT suspension, also administered via colonoscopy. Patients were blinded to treatment allocation. The same delivery route and volume were used for both arms to maintain blinding.

**Flags for your attention:**
- [MISSING: Saline concentration used for stool homogenization.]
- [MISSING: Filtration method and pore size — standard practice varies (e.g., gauze, 500 µm filter); specify what was used.]
- [MISSING: Stool mass or weight used per preparation — the final volume is given (50 mL) but not the amount of donor stool, which is a key reproducibility detail.]
- [MISSING: Storage or handling conditions between processing and administration — was the preparation kept on ice or at room temperature during the interval?]
- [MISSING: Bowel preparation prior to colonoscopy — was a standard prep administered, and if so, what agent and protocol? This affects engraftment and is routinely reported.]
- [MISSING: Colonoscopy delivery site — was the suspension delivered to the cecum, right colon, or another location?]
- [MISSING: Donor screening details — if you wish to be more specific than "per FDA guidelines," list the pathogen panel tested (e.g., SARS-CoV-2, HAV, HBV, HCV, HIV, *Salmonella*, *Shigella*, *E. coli* O157, *Giardia*, etc.). This is increasingly expected in FMT manuscripts.]
- [MISSING: Whether the food coloring used in the placebo was food-grade and considered inert — some journals ask for this.]

---

## 3. Outcome Measures

The primary outcome was CDI recurrence within eight weeks of the intervention. [MISSING: Definition of CDI recurrence — specify the diagnostic criteria used (e.g., ≥3 unformed stools per day plus a positive stool toxin assay or PCR), as this is the central endpoint of the trial.]

Secondary outcomes included intestinal microbiome diversity assessed at weeks 1, 4, and 8 post-intervention. Stool samples for microbiome analysis were collected from all participants at baseline (prior to intervention) and at weeks 1, 4, and 8. Samples were stored at −80°C within two hours of collection.

**Flags for your attention:**
- [MISSING: CDI recurrence diagnostic criteria — see note above; this is critical for the primary endpoint.]
- [MISSING: How recurrence was ascertained — by patient self-report, clinic visit, laboratory testing, or a combination? Was follow-up standardized (e.g., scheduled clinic visits vs. symptom-triggered)?]
- [MISSING: Which diversity metrics were pre-specified as secondary endpoints — alpha diversity (e.g., Shannon index, observed ASVs), beta diversity (e.g., Bray-Curtis dissimilarity), or both? Pre-specifying these avoids the appearance of outcome switching.]
- [MISSING: Whether any adverse events or safety outcomes were monitored and reported — standard for clinical trials.]
- [MISSING: Sample collection method — were patients provided standardized collection kits? Was there a minimum stool volume or mass required?]

---

## 4. Microbiome Analysis

Microbial DNA was extracted from stool samples using the MoBio PowerFecal Kit [MISSING: now marketed as the Qiagen DNeasy PowerSoil Kit following acquisition — confirm which version/catalog number was used, as this affects reproducibility]. The V4 hypervariable region of the 16S rRNA gene was amplified using the primer pair 515F/806R [MISSING: full primer sequences — these are standard Earth Microbiome Project primers, but confirm and provide sequences explicitly, as variants exist]. Sequencing was performed on the Illumina MiSeq platform using paired-end 2 × 250 bp chemistry.

Sequence data were processed using QIIME2 [MISSING: QIIME2 version number — required for reproducibility] with the DADA2 plugin [MISSING: DADA2 version number] for amplicon sequence variant (ASV) inference. DADA2 was used to perform quality filtering, denoising, chimera removal, and ASV table construction.

**Flags for your attention:**
- [MISSING: QIIME2 version — e.g., QIIME2 2023.5; this is essential for reproducibility and is always requested by reviewers.]
- [MISSING: DADA2 version and key parameters — specifically, the truncation lengths applied to forward and reverse reads (e.g., --p-trunc-len-f and --p-trunc-len-r), which directly affect data quality and must be reported.]
- [MISSING: Taxonomic classification method — what classifier and reference database were used (e.g., SILVA 138, Greengenes2, NCBI)? This is a core step in 16S analysis and is absent from your notes.]
- [MISSING: Sequencing depth — minimum read depth per sample, rarefaction depth (if applied), or total reads generated. Journals and reviewers routinely require this.]
- [MISSING: Whether samples were sequenced in a single run or multiple runs — if multiple runs, how was batch effect addressed?]
- [MISSING: Negative and positive controls — were extraction blanks or mock communities included to assess contamination and sequencing accuracy?]
- [MISSING: Data availability — where will raw sequencing data be deposited (e.g., NCBI SRA)? Many journals require this at submission.]

---

## 5. Statistical Analysis

*[No notes were provided for this subsection. The following flags identify the minimum elements that must be addressed for a clinical microbiology journal.]*

**Flags for your attention:**
- [MISSING: Primary analysis method for the primary endpoint — e.g., chi-square test or Fisher's exact test for CDI recurrence proportions between arms.]
- [MISSING: Sample size justification and power calculation — what effect size, alpha level, and power were assumed? With n = 48, reviewers will scrutinize this carefully.]
- [MISSING: Handling of missing data or dropouts — intention-to-treat vs. per-protocol analysis.]
- [MISSING: Statistical tests for microbiome secondary outcomes — e.g., permutational MANOVA (PERMANOVA) for beta diversity, Kruskal-Wallis or linear mixed models for alpha diversity over time.]
- [MISSING: Multiple comparisons correction — given multiple time points and diversity metrics, specify whether and how corrections were applied (e.g., Benjamini-Hochberg FDR).]
- [MISSING: Software used for statistical analysis — e.g., R version x.x, SAS, SPSS, with relevant package names and versions.]
- [MISSING: Significance threshold — state the alpha level used (e.g., p < 0.05).]

---

**Summary of Critical Gaps**

The most consequential missing details for peer review are, in order of priority:

1. **Definition and ascertainment of CDI recurrence** (primary endpoint validity)
2. **QIIME2 and DADA2 version numbers and DADA2 truncation parameters** (reproducibility of microbiome analysis)
3. **Taxonomic classifier and reference database** (core missing analysis step)
4. **Randomization and allocation concealment method** (trial integrity)
5. **Power calculation** (justification of sample size)
6. **IRB approval and trial registration** (required for publication)

Resolving these gaps before submission will substantially reduce the likelihood of a major revision request.
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
