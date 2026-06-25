# Test Results: fundamentals/meta-prompting.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-23.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** fundamentals/meta-prompting.md
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
I want your help with a task, but before I describe it, I want you to ask me clarifying questions to ensure you understand exactly what I need.

The task involves: {BRIEF_TASK_DESCRIPTION}

What questions do you have about the format, scope, audience, constraints, or purpose that would help you assist me effectively?
```

### Prompt Critique Approach
```
Here's a prompt I'm planning to use for {TASK_DESCRIPTION}:

---
{DRAFT_PROMPT}
---

Please critique this prompt:
1. What's ambiguous or underspecified?
2. What assumptions am I making that might not hold?
3. What failure modes might this prompt produce?
4. How would you improve it to make outputs more consistent and reliable?

Provide a revised version of the prompt incorporating your suggestions.
```

### Reverse Engineering Approach
```
I want to create a prompt that produces outputs like these examples:

Example output 1:
{EXAMPLE_OUTPUT_1}

Example output 2:
{EXAMPLE_OUTPUT_2}

Based on these examples, write a prompt that would reliably produce this type of output. Include:
- Clear task specification
- Appropriate constraints
- Output format specification
- Any examples that would help

Here's a prompt I'm planning to use for analyzing differential gene expression results:

---
Look at my RNA-seq results and tell me which genes are important. The data is from a mouse liver study comparing high-fat diet to control.
---

Please critique this prompt:
1. What's ambiguous or underspecified?
2. What assumptions am I making that might not hold?
3. What failure modes might this prompt produce?
4. How would you improve it to make outputs more consistent and reliable?

Provide a revised version of the prompt incorporating your suggestions.
```

## Model Output
```
## Prompt Critique: RNA-seq Differential Expression Analysis

### 1. What's Ambiguous or Underspecified

**Data-related ambiguities:**
- What format is the data in? (DESeq2 output, edgeR, a raw count matrix, a spreadsheet?)
- What columns are present? (log2FC, p-value, adjusted p-value, baseMean, gene symbols, Ensembl IDs?)
- How many genes are in the dataset? Are results pre-filtered or is this the full output?
- Has normalization already been applied?

**Analysis-related ambiguities:**
- What does "important" mean to you? Statistically significant? Biologically relevant? Both?
- What significance thresholds should be used? (|log2FC| > 1? padj < 0.05? These are conventions, not universal truths)
- Do you want upregulated genes, downregulated genes, or both?
- Should the analysis prioritize known metabolic/liver pathways, or is this exploratory?

**Output ambiguities:**
- What should the response look like? A ranked list? A narrative summary? A table?
- Do you want pathway enrichment interpretation, or just gene-level findings?
- What's the downstream use — a paper, a presentation, deciding what to validate experimentally?

---

### 2. Assumptions That Might Not Hold

| Assumption | Why It's Risky |
|---|---|
| The AI knows your experimental design details | Mouse strain, age, sex, diet duration, n per group all affect interpretation |
| Standard thresholds are appropriate | Your study may be underpowered or have specific biological reasons to use different cutoffs |
| Gene symbols are unambiguous | Mouse gene nomenclature has aliases; Ensembl IDs are safer anchors |
| "High-fat diet liver" context is sufficient | The AI may apply generic knowledge rather than your specific biological question |
| The AI can see your data | The prompt implies data will be shared but doesn't specify how |

---

### 3. Failure Modes This Prompt Could Produce

- **Generic response** — lists well-known HFD genes (Fasn, Srebp1c, Ppara) without actually analyzing your specific results
- **Hallucinated statistics** — invents fold-change values or p-values if data isn't clearly provided
- **Threshold arbitrariness** — applies whatever cutoffs it assumes without justification
- **Missing the biological question** — identifies statistically significant genes without connecting them to what you actually care about (steatosis? inflammation? insulin resistance?)
- **Overconfident pathway claims** — draws strong biological conclusions from a gene list without appropriate caveats
- **Ignores data quality signals** — doesn't flag if your results look unusual (e.g., thousands of significant genes suggesting a normalization problem)

---

### 4. Revised Prompt

```
I have differential gene expression results from a mouse liver RNA-seq experiment 
comparing high-fat diet (HFD) to normal chow control. I will paste the data below.

**Experimental context:**
- Tissue: Liver
- Species: Mus musculus [add strain if known, e.g., C57BL/6J]
- Comparison: HFD vs. control (HFD is the numerator, so positive log2FC = 
  upregulated in HFD)
- Analysis tool used: [e.g., DESeq2 / edgeR / limma]
- Sample sizes: n=[X] per group
- Primary biological question: [e.g., What metabolic and inflammatory pathways 
  are dysregulated by HFD in the liver?]

**Data columns are:** [list them, e.g., gene_symbol, log2FoldChange, pvalue, 
padj, baseMean]

**Data:**
[paste data here]

Please analyze these results as follows:

1. **Quality check** — Does anything about the results look unusual 
   (e.g., unexpected number of significant genes, extreme fold-changes)?

2. **Significant gene summary** — Using thresholds of |log2FC| ≥ 1 and 
   padj ≤ 0.05, report: how many genes are significantly up- and 
   down-regulated, and list the top 10 in each direction ranked by padj.

3. **Biological interpretation** — What functional themes emerge from the 
   top hits? Connect findings to known HFD liver biology where supported 
   by the data. Flag any surprising findings.

4. **Caveats** — Note any limitations in interpreting these results 
   (e.g., genes with low baseMean, anything that warrants experimental 
   validation before drawing conclusions).

Format the output with clear section headers. Distinguish between what 
the data directly shows versus your biological interpretation.
```

---

### Key Improvements Made
- **Grounds the AI in your actual data** rather than generic HFD knowledge
- **Defines "important"** with explicit, justifiable thresholds
- **Requests a QC step** so problems surface before interpretation
- **Separates data description from interpretation** — a critical scientific discipline
- **Asks for caveats explicitly** — prevents overconfident conclusions
- **Specifies directionality** of the comparison to avoid fold-change sign confusion
```

## Assessment

_Machine-suggested (UNCONFIRMED) — drafted by Claude Opus 4.7 on 2026-06-24 (refresh) to speed T4 review. An author must independently read the Model Output above and set the real Recommendation. Anything labeled here is triage, not domain expert review. This draft was regenerated after a harness bug (truncated test inputs on this prompt) was fixed and the model was re-run with the full prompt._

**Machine triage:** Follows the 4-part critique structure with tables for ambiguities and assumptions, list for failure modes, then a revised prompt. Hits all expected critique points: data format, "important" undefined, missing experimental context, sign-of-fold-change directionality, risk of generic well-known-gene answers (calls out Fasn, Srebp1c, Ppara). Revised prompt is notable for explicitly putting a QC step BEFORE biological interpretation ("Does anything about the results look unusual?"), which several other panel members do not do. Also explicitly states fold-change directionality ("HFD is the numerator, so positive log2FC = upregulated in HFD") — preventing a common error. "Key Improvements Made" summary at the end maps each critique to the fix. Cross-model comparison: substantive critique points unanimous across all 6 models. No fabricated citations.

**Suggested verdict (UNCONFIRMED):** Pass

**What still needs human verification:**
- That the QC step ahead of interpretation is the right ordering pedagogically (it is, but worth confirming for the materials).
- That the recommended thresholds (|log2FC| ≥ 1 and padj ≤ 0.05) are appropriate defaults for the audience — they're common but conservative for some designs.
- That the directionality framing prevents the right common error (it does, but verify the exact wording is unambiguous).

## Overall Assessment
- **Recommendation:** PENDING AUTHOR REVIEW
- **Notes:**

## Verification Steps Tested
_Which verification requirements from the prompt were checked, and results._
