# Test Results: fundamentals/meta-prompting.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-23.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** fundamentals/meta-prompting.md
- **Model:** nemotron-3-super-120b
- **Model ID (pinned):** Nemotron-3-Super-120B-A12B-NVFP4
- **Endpoint:** https://copilot-dev.cqls.oregonstate.edu/llm/nemotron3-super-120b-nvfp4/v1
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


Here's a thorough critique of your draft prompt for analyzing differential gene expression results, followed by a revised version designed to eliminate ambiguity and improve reliability:

---

### **Critique of Your Draft Prompt**  
**Original Prompt:**  
> *"Look at my RNA-seq results and tell me which genes are important. The data is from a mouse liver study comparing high-fat diet to control."*

#### **1. Ambiguities & Underspecified Elements**  
- **"Important" is undefined**: Does this mean statistically significant (e.g., FDR < 0.05)? Biologically relevant (e.g., |log₂FC| > 1)? Involved in specific pathways? No criteria provided.  
- **Data format unspecified**: Are you providing raw counts, normalized values, a DEG table (e.g., from DESeq2/edgeR), or a file path? LLMs cannot access external data—this prompt assumes I can "look at" your results, which is impossible.  
- **Missing statistical context**: No mention of multiple testing correction, thresholds for significance, or software used (e.g., DESeq2, limma).  
- **No output instructions**: Should I return a gene list? A ranked table? With what columns (gene ID, log₂FC, p-value, etc.)?  

#### **2. Unstated Assumptions**  
- You assume I can access your local/data files (I cannot—this is a critical flaw).  
- You assume "important" aligns with your biological intent (e.g., you might care about metabolic genes, but I could prioritize transcription factors by default).  
- You assume standard analysis parameters (e.g., FDR < 0.05) without stating them, risking mismatched expectations.  
- You assume the study design is simple (just HFD vs. control), ignoring potential confounders (e.g., sex, batch effects, age).  

#### **3. Likely Failure Modes**  
- **False positives/negatives**: Without thresholds, I might return genes with marginal changes (|log₂FC| < 0.5) or miss key drivers due to arbitrary cutoffs.  
- **Misinterpretation of "important"**: I could prioritize genes with low p-values but tiny effect sizes (statistically significant but biologically irrelevant) or vice versa.  
- **Useless output**: Returning a raw gene list without context (e.g., no fold-change, no annotation) would require manual follow-up, defeating the purpose of automation.  
- **Hallucination**: If forced to "analyze" nonexistent data, I might invent plausible-sounding but false gene names or pathways.  
- **Ignoring domain nuance**: Missing liver-specific context (e.g., not highlighting *Srebp1c* or *Fasn* for HFD studies) due to lack of biological guidance.  

#### **4. How to Improve for Consistency & Reliability**  
- **Explicitly state data handling**: Clarify that you’ll *provide a snippet* of results (e.g., top 20 rows of a DEG table) since I can’t access files.  
- **Quantify "important"**: Define thresholds (e.g., "FDR < 0.05 AND |log₂FC| ≥ 1").  
- **Specify output format**: Demand a structured table with required columns.  
- **Add biological constraints**: Narrow scope to relevant pathways (if known) or request functional enrichment.  
- **Acknowledge limitations**: Remind the user to validate findings experimentally.  

---

### **Revised Prompt**  
*(Incorporating all critique points)*  

> **Task**: Analyze a provided snippet of differential gene expression (DGE) results from a mouse liver RNA-seq study (high-fat diet vs. control) to identify biologically and statistically significant genes.  
>   
> **Critical Constraints**:  
> - **I CANNOT access external files or databases**. You **MUST** paste a representative snippet of your DGE results (e.g., 10–20 rows) directly into your query.  
> - Define "important" using **BOTH**:  
>    • Statistical significance: **FDR-adjusted p-value < 0.05**  
>    • Biological relevance: **|log₂(fold change)| ≥ 1.0**  
> - If your snippet lacks FDR or log₂FC columns, state this explicitly—I will note the limitation.  
>   
> **Required Output Format**:  
> A **markdown table** with **EXACTLY these columns**, sorted by |log₂FC| (descending):  
> | Gene Symbol | Entrez ID | log₂FC (HFD vs. Control) | FDR (adj. p-value) | Primary Biological Relevance (Liver/HFD Context) |  
> - **Gene Symbol**: Official MGI symbol (e.g., *Fasn*, *Srebp1c*)  
> - **Entrez ID**: Numeric ID (for cross-referencing)  
> - **log₂FC**: Positive = upregulated in HFD; Negative = downregulated  
> - **FDR**: False discovery rate (must be < 0.05 to appear in table)  
> - **Primary Biological Relevance**: **1-sentence summary** of *why this gene matters in liver HFD studies* (e.g., "Key regulator of hepatic lipogenesis; HFD induces *Fasn* to promote steatosis"). **Do not guess—if unsure, write "Function requires literature validation."**  
>   
> **Failure Prevention**:  
> - If **no genes** meet both criteria, state: *"No genes satisfy FDR < 0.05 AND |log₂FC| ≥ 1.0 in the provided snippet. Suggest relaxing thresholds or checking data quality."*  
> - **Never** invent gene names, pathways, or data not in your snippet.  
> - If snippet lacks critical columns (e.g., no FDR), output: *"Snippet missing [column]. Cannot apply FDR < 0.05 threshold. Provide DESeq2/edgeR output with standard columns."*  
>   
> **Example Input Snippet (for clarity)**:  
> | Gene Symbol | log₂FC | p-value |  
> |-------------|--------|---------|  
> | *Fasn*      | 2.3    | 0.0008  |  
> | *Pparg*     | 1.1    | 0.03    |  
> | *Gapdh*     | 0.2    | 0.45    |  
>   
> **Example Output**:  
> | Gene Symbol | Entrez ID | log₂FC | FDR       | Primary Biological Relevance                     |  
> |-------------|-----------|--------|-----------|--------------------------------------------------|  
> | *Fasn*      | 14118     | 2.3    | 0.004     | Rate-limiting enzyme in fatty acid synthesis; HFD-induced expression drives hepatic steatosis. |  
> | *Pparg*     | 19016     | 1.1    | 0.12      | *Excluded: FDR > 0.05*                           |  
>   
> **Notes for You**:  
> - Always validate top hits with qPCR or pathway analysis (e.g., GSEA for lipid metabolism).  
> - If your study includes covariates (e.g., sex, batch), mention them in your query—I’ll adjust interpretation accordingly.  

---

### **Why This Revision Works**  
- **Eliminates ambiguity**: "Important" is replaced with objective, measurable thresholds.  
- **Solves data access issue**: Explicitly requires user-provided snippet (no false assumptions).  
- **Prevents hallucination**: Output is constrained to user-provided data + liver/HFD biological knowledge (no wild guesses).  
- **Actionable output**: Table format enables direct use in papers/reports; relevance column adds immediate value.  
- **Error handling**: Clear protocols for missing data or no significant genes reduce frustration.  
- **Domain-aware**: Forces liver/HFD context (e.g., prioritizing *Fasn* over generic genes) while acknowledging limits.  

This prompt turns a vague request into a precise, reproducible workflow—critical for avoiding misleading conclusions in genomic analysis. Would you like to adjust any constraints (e.g., different FDR/log₂FC thresholds, specific pathway focus, or output details)? I can refine this further based on your actual data structure or study goals.
```

## Assessment

_Machine-suggested (UNCONFIRMED) — drafted by Claude Opus 4.7 on 2026-06-24 (refresh) to speed T4 review. An author must independently read the Model Output above and set the real Recommendation. Anything labeled here is triage, not domain expert review. This draft was regenerated after a harness bug (truncated test inputs on this prompt) was fixed and the model was re-run with the full prompt._

**Machine triage:** Follows the 4-part critique structure. Hits all expected critique points: "important" undefined, data access ambiguity, missing statistical thresholds, no output format, risk of confabulation. Revised prompt is the most explicit on the panel about file-access limits ("I CANNOT access external files or databases. You MUST paste a representative snippet"). Includes a full worked example (input snippet + expected output table) inside the revised prompt itself — this is a useful few-shot scaffolding pattern. Specifies the output table columns including an Entrez ID anchor (a good defensive choice against gene-symbol ambiguity). Cross-model comparison: substantive critique points unanimous across all 6 models. **Flag**: the worked example uses specific Entrez ID `14118` for *Fasn* and `19016` for *Pparg* — these are verifiable claims; the model should not be inventing Entrez IDs but these particular numbers are within typical ranges and look plausible. No fabricated paper citations.

**Suggested verdict (UNCONFIRMED):** Pass with notes

**What still needs human verification:**
- That the specific Entrez IDs `14118` (Fasn) and `19016` (Pparg) given in the example output are correct — these are easily verifiable against NCBI and should be checked.
- Whether including a worked example inside the revised prompt is a pattern you want to demonstrate (it shows few-shot scaffolding but adds length).
- Whether the heavy use of bold/all-caps emphasis in the revised prompt is the style you want.

## Overall Assessment
- **Recommendation:** PENDING AUTHOR REVIEW
- **Notes:**

## Verification Steps Tested
_Which verification requirements from the prompt were checked, and results._
