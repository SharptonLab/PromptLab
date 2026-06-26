# Test Results: validation/adversarial-critique.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-25.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** validation/adversarial-critique.md
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
Context: I need critical feedback on a manuscript Methods section paragraph about microbiome sample collection.

The text to critique:
"Stool samples were collected from all participants using standard protocols. Samples were immediately frozen at -80°C and DNA was extracted using the Qiagen PowerSoil kit following manufacturer instructions. 16S rRNA gene sequencing was performed using the V4 region primers 515F and 806R on an Illumina MiSeq platform. Sequences were processed using QIIME2 with default parameters, and taxonomy was assigned using the Greengenes database. Alpha diversity was calculated using Shannon index and beta diversity was calculated using Bray-Curtis distances. All statistical analyses were performed using appropriate methods and significance was set at p < 0.05."

Background: This is for a study comparing gut microbiome between healthy controls and patients with inflammatory bowel disease (n=30 per group).

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
````

## Model Output
````
# Adversarial Critique: Microbiome Methods Section

---

## 1. Logical Weaknesses

**"standard protocols"** — This phrase is doing no work and is logically circular. A protocol is only "standard" relative to a defined reference. Which standard? IHMS? HMP? Earth Microbiome Project? This is the methods section's primary job: to specify what was done so it can be replicated. Invoking "standard" is a substitute for that specification, not a fulfillment of it. A reviewer cannot evaluate whether your collection method introduced bias without knowing what it was.

**"immediately frozen"** — This claim is almost certainly false as written, and the logic hasn't been examined. "Immediately" in a clinical setting means samples passed through collection containers, were labeled, transported to a freezer, and logged. That process takes minutes to hours. The actual cold-chain handling — time from defecation to freezer, transport temperature, number of freeze-thaw cycles — is entirely absent. For microbiome studies, this is not a minor omission: bacterial community composition shifts measurably within 15–30 minutes at room temperature. The word "immediately" is doing critical scientific work here without any supporting evidence.

**"following manufacturer instructions"** — This is insufficient and potentially misleading. The PowerSoil kit has multiple optional steps (bead-beating duration, elution volume, input mass). Manufacturer instructions include decision points. Which choices were made? Input mass of stool is particularly important: 0.25g vs. 0.5g affects DNA yield and community representation. This phrase creates a false impression of precision.

---

## 2. Factual Concerns

**Greengenes database** — *Significant concern.* Greengenes was effectively deprecated in 2013 (last update) and has been widely superseded by SILVA and, more recently, the Greengenes2 database (2022). Using the original Greengenes database in a current study is a methodological red flag that reviewers will flag immediately. Taxonomy assignments from Greengenes are known to be less accurate at genus and species level compared to SILVA 138. This is not a minor citation issue — it affects every taxonomic conclusion in the paper. The authors need to either justify this choice explicitly or update to a current reference database.

**"V4 region primers 515F and 806R"** — Partially adequate but incomplete. There are multiple versions of these primers (original Caporaso vs. Earth Microbiome Project modified versions 515F/806Rb). The modified versions were specifically designed to reduce Archaea bias and improve coverage. Which version was used? This matters for reproducibility and cross-study comparison.

**"QIIME2 with default parameters"** — This is a reproducibility failure. QIIME2 default parameters change between versions, and the version is not specified. "Default parameters" in QIIME2 2019.x is not the same as 2023.x. Furthermore, QIIME2 is a framework, not a pipeline — it requires specifying which plugins and methods were used (DADA2 vs. Deblur for denoising, which classifier for taxonomy, etc.). This sentence describes almost nothing about what was actually done.

**"Alpha diversity was calculated using Shannon index and beta diversity was calculated using Bray-Curtis distances"** — These are reasonable choices, but presenting only one metric each is a factual underrepresentation of standard practice. Shannon index alone misses richness (Observed OTUs/ASVs) and evenness components. Bray-Curtis alone misses phylogenetic beta diversity (UniFrac), which is the dominant metric in IBD microbiome literature. Reviewers familiar with IBD microbiome research will notice the absence of weighted/unweighted UniFrac immediately.

---

## 3. Missing Considerations

**No mention of:**

- **Sample size justification for microbiome analysis.** n=30 per group is potentially underpowered for microbiome studies, where effect sizes are often small and inter-individual variation is high. No power calculation is mentioned. This is a significant omission.
- **DNA extraction controls.** No mention of negative extraction controls (critical for detecting kit contamination, which is a known issue with low-biomass samples) or positive controls.
- **Sequencing depth.** No mention of read depth per sample, rarefaction strategy, or minimum read threshold for inclusion. This directly affects alpha diversity comparisons and is a major methodological decision.
- **Stool collection conditions.** Were participants given standardized collection kits? Were samples collected at home or in clinic? Home collection introduces uncontrolled freeze-thaw and transport variables.
- **Exclusion criteria for samples.** What happened to samples that failed QC? What was the failure rate?
- **Medication confounders.** IBD patients are frequently on immunosuppressants, biologics, and antibiotics — all of which dramatically alter gut microbiome. No mention of how this was handled (exclusion criteria, covariate adjustment, stratification).
- **Diet and antibiotic washout period.** Standard in microbiome studies; entirely absent here.
- **Stool consistency/Bristol scale.** IBD patients frequently have loose or liquid stool; this affects microbial composition independently of disease status and is a known confounder.

---

## 4. Overstated Claims

**"All statistical analyses were performed using appropriate methods"** — This sentence should not exist in a scientific manuscript. It is self-validating and content-free. "Appropriate" is defined by the author, not by any external standard. This is the equivalent of writing "the experiment was done correctly." A reviewer will either laugh at this or flag it as a red flag for hidden methodological choices. What software? What specific tests? Were data tested for normality? Were corrections for multiple comparisons applied? Microbiome data is compositional and non-normally distributed — standard parametric tests are inappropriate without transformation. None of this is addressed.

**"significance was set at p < 0.05"** — In a microbiome study testing hundreds to thousands of taxa simultaneously, a raw p < 0.05 threshold without multiple testing correction (Benjamini-Hochberg FDR, Bonferroni, etc.) is not a significance threshold — it is a false discovery generator. This is a serious methodological flaw, not a minor reporting gap.

---

## 5. Structural Issues

- The paragraph conflates **sample collection**, **laboratory processing**, **bioinformatics**, and **statistical analysis** into a single undifferentiated block. These are conventionally separated into subsections for a reason: they involve different expertise, different reproducibility standards, and different reviewer scrutiny.
- The ordering is logical on the surface but skips critical decision points between steps. There is no mention of what happened between DNA extraction and sequencing (library preparation, amplification conditions, pooling strategy, sequencing run quality metrics).
- The final sentence ("All statistical analyses...") is structurally placed as a conclusion to the methods but contains no methodological information. It reads as a placeholder that was never completed.

---

## 6. What a Skeptical Peer Reviewer Would Say

A reviewer with microbiome expertise would likely write something close to the following:

> *"The methods section as written is insufficient for reproducibility and contains several choices that require justification. The use of the Greengenes database without explanation is a significant concern given its known limitations and deprecation. The description of QIIME2 analysis as using 'default parameters' without specifying the version or plugins used is not acceptable. The statistical methods section is essentially empty — the authors state that 'appropriate methods' were used but do not specify them, and the absence of multiple testing correction in a study generating hundreds of taxonomic comparisons is a major flaw. The authors should also address how IBD-related medications were handled as confounders, as this is a well-known issue in this literature that is entirely unaddressed. I cannot evaluate the validity of the findings without substantially more methodological detail."*

---

## Priority Ranking of Issues

| Issue | Severity |
|---|---|
| Greengenes database (deprecated) | **Critical** |
| No multiple testing correction | **Critical** |
| "QIIME2 default parameters" without version/plugins | **Critical** |
| Medication confounders unaddressed | **Critical** |
| "Appropriate statistical methods" — no specification | **Major** |
| No sequencing depth/rarefaction information | **Major** |
| "Immediately frozen" — unverified claim | **Major** |
| Missing extraction/sequencing controls | **Major** |
| Only Shannon + Bray-Curtis (no UniFrac) | **Moderate** |
| Primer version unspecified | **Moderate** |
| "Standard protocols" undefined | **Minor** |

---

**Bottom line:** This paragraph would not survive peer review at a journal with microbiome expertise. It contains critical omissions that make the analysis unreproducible, at least one likely outdated methodological choice (Greengenes), and a statistical framework that is either incomplete or potentially flawed. It reads as a first draft placeholder, not a finished methods section.
````

## Assessment

_Machine-suggested (UNCONFIRMED) — drafted by Claude Opus 4.7 on 2026-06-26 to speed T4 review. An author must independently read the Model Output above and set the real Recommendation. Anything labeled here is triage, not domain expert review._

**Machine triage:** Output covers required dimensions with severity table and bottom-line "would not survive peer review" judgment. Complete, no truncation. Strong cross-model agreement on substantive issues.

**Suggested verdict (UNCONFIRMED):** Pass

**What still needs human verification:**
- Whether the severity ratings (Major/Critical/Minor) match reviewer judgment
- That the Greengenes-as-outdated claim is correct
- Whether the "first draft placeholder" framing is the right tone

## Overall Assessment
- **Recommendation:** PENDING AUTHOR REVIEW
- **Notes:**

## Verification Steps Tested
_Which verification requirements from the prompt were checked, and results._
