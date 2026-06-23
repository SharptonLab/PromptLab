# Test Results: structured-prompt-template.md

## Test Metadata
- **Prompt:** fundamentals/structured-prompt-template.md
- **Model:** Claude Opus 4 (claude-opus-4-5-20251101)
- **Date:** 2026-02-04
- **Tester:** Claude Code (automated testing)

## Test Input Used
Standard test input from prompt file (methods extraction from IBD microbiome paper excerpt)

## Filled Prompt
```
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
```

## Model Output
```
- Mouse strain: C57BL/6
- Sample size (n per group): 12 per group
- IBD model (DSS, TNBS, genetic, etc.): DSS (3% dextran sulfate sodium, molecular weight 36,000-50,000; MP Biomedicals) in drinking water for 7 days
- Sequencing platform: Illumina NovaSeq 6000 (2×250 bp paired-end reads)
- 16S region targeted: V3-V4 region (primers 341F/785R)
- Bioinformatics pipeline: QIIME2 version 2023.5 with DADA2 for quality filtering and denoising
- Alpha diversity metrics reported: Shannon index, observed features
- Beta diversity methods: Bray-Curtis dissimilarity, PCoA visualization, PERMANOVA
- Statistical tests for differential abundance: ANCOM-BC with FDR correction
- Key confounds acknowledged: Study was not pre-registered; sample size was based on previous experience rather than formal power analysis
```

## Assessment

### Task Achievement
- **Achieved:** Yes
- **Notes:** All requested fields were extracted accurately from the provided text. The model correctly identified all methodology details and used terminology from the paper.

### Constraint Compliance
- **All constraints respected:** Yes
- **Violations noted:** None. The model used only information from the provided text and did not add external knowledge. All values were explicitly stated in the excerpt.

### Failure Modes
- **Failure modes observed:** None
- **Mitigation effectiveness:** The constraint "If information is not explicitly stated, write 'Not reported'" was not needed as all fields had extractable information. The constraint "Use exact terminology from the paper" was followed (e.g., "observed features" rather than "observed ASVs").

### Output Format
- **Format correct:** Yes
- **Deviations:** None. Output followed the specified format with one field per line.

## Overall Assessment

*This assessment was auto-drafted by Claude Code on 2026-02-04 and demoted to PENDING during the 2026-06-23 audit (T2). No human verification is on record. The detailed analysis below is preserved as a machine-suggested (UNCONFIRMED) starting point for T4 review — an author must independently read the raw output above and set the real Recommendation.*

- **Recommendation:** PENDING AUTHOR REVIEW
- **Notes:** The prompt template successfully guided extraction of methodology information. The output matched all expected values from the test input specification. The model appropriately captured the nuanced information about study limitations (no pre-registration, experience-based sample size) in the "Key confounds acknowledged" field, demonstrating good extraction of methodological limitations.

## Verification Steps Tested
- [x] Extracted values match source text: Verified all 10 fields against the paper excerpt
- [x] "Not reported" used appropriately: Not applicable (all fields had values)
- [x] Terminology matches paper: Confirmed (e.g., "observed features" not "observed ASVs")
- [x] No hallucinated details: Confirmed, all values traceable to source text
