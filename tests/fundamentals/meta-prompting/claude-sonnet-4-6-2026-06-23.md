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
## Prompt Critique

### 1. What's Ambiguous or Underspecified?

**"Important" is doing enormous, undefined work here.**
- Important by statistical significance? Effect size? Biological relevance? Clinical translatability?
- Important to *whom* — a statistician, a biologist, a grant reviewer?
- Important relative to what prior knowledge or pathway context?

**The data itself is unspecified:**
- What format is the data in? (DESeq2 output, edgeR, a raw count matrix, a spreadsheet?)
- What columns exist? (log2FC, p-value, adjusted p-value, baseMean?)
- How many genes total? How many are differentially expressed?
- What thresholds, if any, have already been applied?

**"Tell me which genes" is an unclear deliverable:**
- A ranked list? A narrative summary? A table? A pathway analysis?
- How many genes — top 10? Top 100? All significant ones?

**The biological context is thin:**
- What's the specific hypothesis or research question?
- What timepoint? What sex/age of mice? What duration of diet?
- Are there covariates (batch effects, animal IDs)?

---

### 2. Assumptions You're Making That May Not Hold

| Assumption | Why It's Risky |
|---|---|
| The model knows what "important" means in your context | It will guess, and guess differently each time |
| The model can infer data format from context | It may hallucinate column interpretations |
| Standard thresholds (p<0.05, \|log2FC\|>1) are appropriate | These may be too lenient or too strict for your data |
| The model has relevant domain knowledge about liver metabolism | It does, but it may over-rely on well-known genes and miss novel findings |
| A single prompt can replace analytical judgment | It cannot — it will produce plausible-sounding but potentially misleading prioritization |

---

### 3. Failure Modes This Prompt Will Likely Produce

- **Confident vagueness:** A narrative about "upregulated metabolic genes" that sounds authoritative but isn't grounded in your actual data
- **Threshold hallucination:** The model invents or assumes cutoffs you didn't specify
- **Recency/fame bias:** Over-emphasis on well-known genes (e.g., *Ppara*, *Fasn*) regardless of what your data actually shows
- **Inconsistent outputs:** Running this prompt twice will produce meaningfully different answers
- **Missing the actual question:** Without knowing *why* you're doing this study, "important" genes for one purpose may be noise for another
- **No uncertainty flagging:** The model won't tell you when it's guessing

---

### 4. How to Improve It

**Core principles to apply:**
- Define "important" operationally with explicit criteria
- Specify the data format and available columns
- State the biological question, not just the experimental design
- Request a structured output format
- Ask for reasoning to be shown, so you can catch errors
- Set explicit thresholds or ask the model to apply and *state* the ones it uses

---

## Revised Prompt

```
I have differential gene expression results from a mouse liver RNA-seq study 
comparing high-fat diet (HFD, n=X) to normal chow controls (n=X) after [duration]. 
Mice were [age, sex]. The analysis was performed using [DESeq2/edgeR/limma].

The data is provided as a table with the following columns:
- gene_symbol
- log2FoldChange (HFD vs. control)
- pvalue
- padj (Benjamini-Hochberg adjusted)
- baseMean (mean normalized counts)

[PASTE DATA HERE or describe it]

My primary research question is: [e.g., "What metabolic pathways are disrupted 
by HFD in the liver?" OR "Are there transcription factors driving the 
transcriptional response?"]

Please do the following, in order:

1. **Filter** for statistically significant DEGs using padj < 0.05 and 
   |log2FoldChange| > 1. State how many genes pass this filter.

2. **Separate** into upregulated and downregulated gene lists. 
   Show the top 20 by absolute log2FoldChange in each direction as a table.

3. **Prioritize** genes by these criteria (apply in order):
   a. Highest statistical confidence (lowest padj)
   b. Largest effect size (|log2FC|)
   c. Adequate expression level (baseMean > 50, to exclude lowly expressed genes)
   
4. **Interpret** the top hits in the context of liver lipid metabolism, 
   insulin signaling, and inflammation. For each gene you highlight, state:
   - Direction and magnitude of change
   - Known function relevant to this context
   - Confidence level in your interpretation (high/medium/low) and why

5. **Flag** any results that seem unusual, potentially artifactual, 
   or that require experimental validation before interpretation.

Do not speculate beyond what the data supports. If you are uncertain about 
a gene's function in this specific context, say so explicitly.
```

---

**The core improvement:** You've shifted from asking for a judgment call ("which are important") to asking for a defined analytical procedure with explicit criteria, structured outputs, and built-in uncertainty acknowledgment. This makes the output reproducible, auditable, and much harder to silently get wrong.
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
