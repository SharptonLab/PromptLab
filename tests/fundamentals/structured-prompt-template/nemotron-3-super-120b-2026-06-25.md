# Test Results: fundamentals/structured-prompt-template.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-25.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** fundamentals/structured-prompt-template.md
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
**Context:**
I'm conducting a systematic review of gut microbiome studies in mouse models of inflammatory bowel disease. I need to extract standardized methodology information from each paper for comparison.

**Your role:**
You are a systematic review assistant extracting methodology details from primary research papers.

**Task:**
Extract the methodology information specified below from the provided paper excerpt. Use only information explicitly stated in the text.

**Input:**
[PAPER EXCERPT - Methods Section]
"Male C57BL/6 mice (8-10 weeks old, n=12 per group) were obtained from Charles River Laboratories. Colitis was induced by administering 3% dextran sulfate sodium (DSS, molecular weight 36,000-50,000; MP Biomedicals) in drinking water for 7 days, followed by 7 days of regular water. Control mice received regular water throughout. Fecal samples were collected on days 0, 7, and 14.

DNA was extracted using the QIAamp PowerFecal Pro DNA Kit (Qiagen). The V3-V4 region of the 16S rRNA gene was amplified using primers 341F/785R and sequenced on the Illumina NovaSeq 6000 platform (2×250 bp paired-end reads). Raw sequences were processed using QIIME2 version 2023.5 with DADA2 for quality filtering and denoising.

Alpha diversity (Shannon index, observed features) was compared between groups using Kruskal-Wallis tests. Beta diversity was assessed using Bray-Curtis dissimilarity and visualized with PCoA. PERMANOVA was used to test for significant differences between groups. Differential abundance analysis was performed using ANCOM-BC with FDR correction. A p-value < 0.05 was considered statistically significant. The study was not pre-registered, and sample size was based on previous experience rather than formal power analysis."

**Constraints:**
- Use only information present in the paper—do not infer or add external knowledge
- If information is not explicitly stated, write "Not reported"
- Do not interpret or evaluate the methodology; only extract what is stated
- Use exact terminology from the paper where possible

**Output format:**
Provide the following fields, one per line:

- Mouse strain:
- Sample size (n per group):
- IBD model (DSS, TNBS, genetic, etc.):
- Sequencing platform:
- 16S region targeted:
- Bioinformatics pipeline:
- Alpha diversity metrics reported:
- Beta diversity methods:
- Statistical tests for differential abundance:
- Key confounds acknowledged:

**Evaluation criteria:**
Accuracy and completeness are paramount. It is better to report "Not reported" than to guess.
````

## Model Output
````


- Mouse strain: Male C57BL/6 mice
- Sample size (n per group): n=12 per group
- IBD model (DSS, TNBS, genetic, etc.): DSS-induced colitis
- Sequencing platform: Illumina NovaSeq 6000 platform
- 16S region targeted: V3-V4 region
- Bioinformatics pipeline: QIIME2 version 2023.5 with DADA2
- Alpha diversity metrics reported: Shannon index, observed features
- Beta diversity methods: Bray-Curtis dissimilarity, PCoA, PERMANOVA
- Statistical tests for differential abundance: ANCOM-BC with FDR correction
- Key confounds acknowledged: The study was not pre-registered, and sample size was based on previous experience rather than formal power analysis.
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
