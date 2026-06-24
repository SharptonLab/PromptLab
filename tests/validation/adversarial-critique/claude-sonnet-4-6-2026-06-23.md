# Test Results: validation/adversarial-critique.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-23.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** validation/adversarial-critique.md
- **Model:** claude-sonnet-4.6
- **Model ID (pinned):** claude-sonnet-4-6
- **Endpoint:** native
- **Date:** 2026-06-23
- **Tester:** cross-model-harness
- **Assembly strategy:** concat
- **Temperature:** 0.0

## Test Input Used
Standard test input from prompt file (`## Test Input`).

## Filled Prompt
```
Context: I need critical feedback on {WHAT_YOU'RE_EVALUATING: e.g., "a manuscript Discussion section," "an LLM-generated analysis," "my grant specific aims"}.

The text/content to critique:
{PASTE_CONTENT_TO_EVALUATE}

Background (optional): {ANY_RELEVANT_CONTEXT}

Task: Provide an adversarial critique of this content. Your job is to find problems, not to validate. Please identify:

1. **Logical weaknesses**: Flaws in reasoning, unsupported leaps, circular arguments

2. **Factual concerns**: Claims that seem unsupported, incorrect, or unverifiable
   - Flag specific claims that should be checked
   - Note anything that seems too convenient or too clean

3. **Missing considerations**: Important perspectives, alternatives, or caveats that are absent

4. **Overstated claims**: Where has the author gone beyond what the evidence supports?

5. **Structural issues**: Problems with organization, flow, or clarity

6. **What a skeptical reviewer would say**: If this were submitted for peer review, what objections would a critical reviewer raise?

Constraints:
- Be genuinely critical—I want problems surfaced, not reassurance
- Distinguish between minor issues and significant concerns
- Be specific: quote the problematic text and explain the issue
- If something is actually good, you can note it briefly, but focus on problems
- Do not soften criticism or sandwich it between praise

Output format: Structured critique with specific issues and recommended fixes where applicable.

Context: I need critical feedback on a manuscript Methods section paragraph about microbiome sample collection.

The text to critique:
"Stool samples were collected from all participants using standard protocols. Samples were immediately frozen at -80°C and DNA was extracted using the Qiagen PowerSoil kit following manufacturer instructions. 16S rRNA gene sequencing was performed using the V4 region primers 515F and 806R on an Illumina MiSeq platform. Sequences were processed using QIIME2 with default parameters, and taxonomy was assigned using the Greengenes database. Alpha diversity was calculated using Shannon index and beta diversity was calculated using Bray-Curtis distances. All statistical analyses were performed using appropriate methods and significance was set at p < 0.05."

Background: This is for a study comparing gut microbiome between healthy controls and patients with inflammatory bowel disease (n=30 per group).
```

## Model Output
```
## Adversarial Critique: Microbiome Methods Paragraph

---

### 1. Logical Weaknesses

**"Samples were immediately frozen at -80°C"**
This is almost certainly false as written. Immediate freezing at -80°C in a clinical/field collection setting is logistically implausible for most study designs. What actually happened? Were samples collected at home? At a clinic? Was there a stabilization buffer used (e.g., OMNIgene·GUT)? What was the time-to-freezing? This matters enormously—microbiome composition shifts measurably within hours at room temperature. The word "immediately" is doing heavy lifting here and will draw skeptic fire.

**"standard protocols"**
This phrase is meaningless. There is no single standard for stool collection. Did participants self-collect? Were specific containers used? Was there a volume/weight requirement? Were dietary or antibiotic restrictions imposed pre-collection? "Standard" is a placeholder that obscures methodological decisions reviewers need to evaluate.

---

### 2. Factual Concerns — Significant

**Greengenes database is outdated and should be flagged as a major problem.**
Greengenes (the version commonly used in QIIME2 pipelines, GG 13_8) has been largely deprecated in the field. SILVA 138 or the newer Greengenes2 (2022+) are current standards. Using the old Greengenes database introduces known taxonomic errors, particularly at genus level, and a reviewer familiar with the field will flag this immediately. This is not a minor issue—it affects every taxonomic assignment in the paper.

**"QIIME2 with default parameters"**
Default parameters are version-dependent and change between releases. Without specifying the QIIME2 version, this analysis is not reproducible. Additionally, "default parameters" for what, exactly? Denoising (DADA2 vs. Deblur)? Truncation lengths? Chimera filtering? These choices materially affect OTU/ASV counts and downstream diversity metrics. This sentence fails the reproducibility standard.

**V4 primers 515F/806R — version unspecified**
There are multiple versions of these primers (original Caporaso et al. vs. Earth Microbiome Project modified versions). They have different coverage profiles. Which were used?

---

### 3. Missing Considerations — Significant Gaps

- **No mention of rarefaction or sequencing depth normalization.** How was unequal sequencing depth handled before diversity calculations? This is a contested but mandatory-to-address methodological choice.
- **No mention of contaminant removal.** For low-biomass or clinical samples, decontam or equivalent steps are expected.
- **No negative or positive controls mentioned.** Extraction blanks, PCR controls? Their absence (or non-reporting) is a red flag for reviewers.
- **No mention of antibiotic use exclusion criteria.** In an IBD cohort, this is critical—antibiotic use is a major confounder and must be addressed in Methods.
- **IBD disease activity not characterized.** Were IBD patients in remission or active flare? On biologics? On 5-ASA? These are not statistical covariates—they are fundamental to interpreting any microbiome difference found.
- **No mention of sequencing depth achieved** (mean reads per sample, range, samples excluded for low depth).
- **No mention of whether 16S data were processed as OTUs or ASVs.** QIIME2 supports both; they are not equivalent.

---

### 4. Overstated / Vague Claims

**"All statistical analyses were performed using appropriate methods"**
This sentence should be deleted. It conveys zero information and reads as evasion. What software? What tests? Were parametric or non-parametric tests used for diversity comparisons? Was multiple testing correction applied? PERMANOVA for beta diversity? If so, how many permutations? What covariates were included in models?

**"significance was set at p < 0.05"**
With microbiome data involving hundreds to thousands of taxa, a raw p < 0.05 threshold without specifying multiple testing correction (FDR/Benjamini-Hochberg, Bonferroni, etc.) is a serious methodological flaw. A reviewer will ask this directly.

---

### 5. Structural Issues

- The paragraph conflates collection, processing, sequencing, bioinformatics, and statistics into a single undifferentiated block. Standard practice is to separate these into subsections or at minimum clearly delineated sentences with enough detail to permit replication.
- The ordering is logical but the level of detail is inverted: more words are spent on obvious steps (kit name) than on critical analytical decisions (diversity normalization, statistical models).
- No citations are provided for the pipeline (QIIME2), primers, or database. These require citations.

---

### 6. What a Skeptical Peer Reviewer Would Say

> *"The Methods section as written does not provide sufficient detail for replication. The use of the deprecated Greengenes 13_8 database requires justification or replacement. QIIME2 version and key plugin parameters (DADA2 truncation lengths, minimum frequency thresholds) must be specified. The statement that 'all statistical analyses were performed using appropriate methods' is uninformative and must be replaced with explicit descriptions of tests used. The authors must clarify how sequencing depth variation was handled prior to diversity analyses, and whether multiple testing correction was applied to taxonomic comparisons. The claim that samples were 'immediately' frozen requires clarification of the collection protocol and time-to-freezing. Given the IBD cohort, medication status and disease activity at time of collection must be reported."*

---

### Priority Ranking of Issues

| Issue | Severity |
|---|---|
| Greengenes database (outdated) | **Critical** |
| QIIME2 version/parameters unspecified | **Critical** |
| No multiple testing correction stated | **Critical** |
| "Appropriate methods" — no statistical detail | **Major** |
| "Immediately frozen" — implausible/unverified | **Major** |
| No rarefaction/depth normalization described | **Major** |
| IBD disease activity/medications absent | **Major** |
| No controls (negative/positive) mentioned | **Major** |
| "Standard protocols" undefined | **Moderate** |
| Primer version unspecified | **Moderate** |
| No sequencing depth reported | **Moderate** |

---

**Bottom line:** This paragraph would not pass peer review at a rigorous microbiome journal. It reads as a placeholder draft. The most urgent fixes are the database issue, statistical reporting, and QIIME2 versioning—these are not stylistic problems but reproducibility and validity failures.
```

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
