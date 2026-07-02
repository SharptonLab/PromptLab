# Test Results: fundamentals/meta-prompting.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-25.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** fundamentals/meta-prompting.md
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
````

## Model Output
````
## Critique of Your Prompt

### 1. What's Ambiguous or Underspecified

**"Important" is doing enormous, undefined work here.**
- Important by statistical significance? Effect size? Biological relevance? Clinical relevance? Novelty?
- Important to whom and for what purpose?

**The data itself is unspecified:**
- What format is the data in? (DESeq2 output, edgeR, a raw count matrix, a spreadsheet?)
- What columns exist? (log2FC, p-value, adjusted p-value, baseMean?)
- What thresholds were already applied, if any?
- How many genes are in the results — 20? 20,000?

**The analysis goal is undefined:**
- Are you doing pathway enrichment? Building a hypothesis? Writing a paper? Prioritizing targets for follow-up experiments?
- Do you want a ranked list, a narrative summary, a table, or something else?

**"High-fat diet vs. control" lacks detail:**
- Duration of diet? (4 weeks vs. 24 weeks produces very different biology)
- Mouse strain? (C57BL/6 responds very differently than BALB/c)
- Sex? Age? Sample sizes?
- Were there any covariates or batch effects?

---

### 2. Assumptions You're Making That May Not Hold

| Assumption | Why It's Risky |
|---|---|
| The AI knows what "important" means in your context | It will guess, and its guess may not match your scientific question |
| The AI can see and parse your data correctly | Format issues, truncation, or encoding problems can silently corrupt interpretation |
| Standard thresholds (p<0.05, \|log2FC\|>1) are appropriate | Your study may be underpowered or overpowered, making these thresholds misleading |
| The AI has current knowledge of liver/HFD biology | Training cutoffs mean recent literature may be missing |
| Gene symbols are unambiguous | Mouse/human symbol conflicts, aliases, and retired symbols cause real errors |
| The AI will flag its own uncertainty | Without instruction, it may state things confidently that warrant skepticism |

---

### 3. Failure Modes This Prompt Will Likely Produce

**Hallucinated biological relevance.** The model will confidently describe gene functions that sound plausible but may be subtly wrong or context-inappropriate.

**Threshold arbitrariness.** It will pick cutoffs (probably p<0.05, |log2FC|>1) without justification, and you won't know why or whether they suit your data.

**Generic, non-specific output.** You'll get a list of "metabolism genes are upregulated, inflammatory genes are downregulated" — true of almost every HFD study, therefore not useful.

**Survivorship bias in interpretation.** It will focus on genes it recognizes, systematically ignoring potentially important uncharacterized genes.

**No uncertainty quantification.** You won't know which claims are well-supported versus speculative.

**Inconsistent outputs across runs.** The same prompt will produce meaningfully different gene lists and interpretations on repeated queries.

---

### 4. How to Improve It

- **Define "important" operationally** with explicit, prioritized criteria
- **Specify the exact data format** and what columns mean
- **State your downstream purpose** so the analysis is goal-directed
- **Set explicit thresholds** or ask for threshold sensitivity analysis
- **Request structured output** so results are comparable across runs
- **Ask for uncertainty flagging** explicitly
- **Provide biological context** that constrains interpretation
- **Separate tasks** — don't ask for selection, interpretation, and summarization in one vague request

---

## Revised Prompt

```
I have differential gene expression results from a mouse liver RNA-seq study. 
The experimental comparison is high-fat diet (60% kcal fat, 16 weeks) vs. 
normal chow control in male C57BL/6J mice (n=5 per group). Analysis was 
performed with DESeq2.

## Data format
I will provide a table with these columns:
- gene_symbol: MGI official mouse gene symbol
- baseMean: mean normalized count across all samples
- log2FoldChange: HFD relative to control (positive = upregulated in HFD)
- lfcSE: standard error of log2FC estimate
- padj: Benjamini-Hochberg adjusted p-value

[PASTE DATA HERE]

## Your task
Please complete the following steps in order, labeling each section clearly:

**Step 1 — Filter and rank**
Apply these thresholds: padj < 0.05 AND |log2FoldChange| > 1 AND baseMean > 50.
Report how many genes pass each threshold individually and in combination.
If fewer than 10 or more than 500 genes pass all filters, flag this and explain 
what it might indicate before continuing.

**Step 2 — Structured gene table**
For genes passing all filters, produce a markdown table with columns:
gene_symbol | direction | log2FC (rounded to 2 decimal places) | padj | 
known_liver_function | confidence_in_annotation

For known_liver_function, briefly describe the gene's role specifically in 
hepatic metabolism, lipid handling, or inflammation if known.
For confidence_in_annotation, use: High / Medium / Low / Unknown — and use 
"Unknown" if you are not confident in the gene's function.

**Step 3 — Pattern summary**
Identify functional patterns among the significant genes. For each pattern:
- Name the pattern
- List supporting genes
- Note whether this is a well-established HFD/liver finding or a potentially 
  novel observation in this dataset
- Rate your confidence: High / Medium / Low, with one sentence of justification

**Step 4 — Genes to prioritize for follow-up**
Suggest up to 5 genes as highest-priority candidates for experimental follow-up.
For each, explain your reasoning using this structure:
- Why statistically compelling
- Why biologically interesting in this specific context
- What is uncertain or would need verification
- One suggested follow-up experiment

**Step 5 — Caveats and limitations**
List at least three specific limitations of this analysis, including at least 
one related to what you (the AI) cannot reliably assess.

## Constraints
- Do not invent gene functions. If you are uncertain, say so explicitly.
- Do not assume human gene findings translate directly to mouse liver without 
  noting the assumption.
- If gene symbols are ambiguous or have common aliases, flag them.
- Base claims on the data provided, not on what "typically" happens in HFD 
  studies unless you explicitly label it as prior expectation.
```

---

**Why this revision is more reliable:**

The key architectural change is **decomposing one vague request into five explicit, ordered subtasks** with defined inputs and outputs for each. This forces the model to show its work at each stage, makes failures visible rather than hidden, and produces output you can actually evaluate and reproduce. The explicit uncertainty requirements counteract the model's tendency toward false confidence, which is the single most dangerous failure mode in scientific AI assistance.
````

## Assessment

_Machine-suggested (UNCONFIRMED) — drafted by Claude Opus 4.7 on 2026-06-26 to speed T4 review. An author must independently read the Model Output above and set the real Recommendation. Anything labeled here is triage, not domain expert review._

**Machine triage:** Output produces critique + rewrite. Complete, no truncation. Rewrite decomposes the request into 5 explicit ordered subtasks with defined inputs/outputs. Includes explicit caveat against assuming human→mouse translation and against using "what typically happens in HFD studies" as prior. **Strong cross-model agreement** with peers on the critique substance.

**Suggested verdict (UNCONFIRMED):** Pass

**What still needs human verification:**
- Whether decomposition into 5 subtasks vs. peers' single structured prompt is the preferred approach
- The framing "single most dangerous failure mode in scientific AI assistance" — verify reviewer comfort

## Overall Assessment
- **Recommendation:** Pass
- **Notes:** Alex Alexiev (2026-06-30): **What still needs human verification:**
- Whether decomposition into 5 subtasks vs. peers' single structured prompt is the preferred approach: yes
- The framing "single most dangerous failure mode in scientific AI assistance" — verify reviewer comfort: yes

## Verification Steps Tested
_Which verification requirements from the prompt were checked, and results._
