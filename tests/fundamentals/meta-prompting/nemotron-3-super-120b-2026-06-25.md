# Test Results: fundamentals/meta-prompting.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-25.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** fundamentals/meta-prompting.md
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


**Critique of the original prompt**

| # | Issue | Why it matters | Example of how it can go wrong |
|---|-------|----------------|--------------------------------|
| 1 | **Ambiguous / underspecified** | The request “tell me which genes are important” does not define what “important” means (statistical significance, effect size, biological relevance, pathway enrichment, etc.) nor what thresholds or multiple‑testing correction should be applied. | The model might return a list of genes with the largest fold‑change even if they are not statistically significant, or it might give a generic answer that ignores the user’s actual analysis pipeline. |
| 2 | **Unstated assumptions** | Implicitly assumes: <br>• The user has already performed differential expression (DE) testing and has a table of results (log₂FC, p‑value, FDR). <br>• The data are from a mouse liver RNA‑seq experiment with a high‑fat diet vs. control comparison. <br>• The user wants a simple gene list rather than downstream interpretation (GO, KEGG, network analysis). | If the raw FASTQ files are supplied instead of a processed table, the model cannot comply. If the user expects pathway enrichment but only gets a gene list, the output will feel incomplete. |
| 3 | **Potential failure modes** | • **Over‑inclusion** – returning dozens or hundreds of genes without prioritisation, overwhelming the user. <br>• **Under‑inclusion** – applying overly strict thresholds (e.g., FDR < 0.01) and missing biologically relevant genes with modest but consistent changes. <br>• **Mis‑interpretation of direction** – forgetting to note whether genes are up‑ or down‑regulated. <br>• **Species‑specific confusion** – giving human gene symbols when the data are mouse. <br>• **Lack of context** – no mention of batch effects, covariates, or model used (e.g., DESeq2, edgeR, limma‑voom). | The user may receive a list that is hard to act upon, or they may mistakenly follow up on false positives. |
| 4 | **Missing guidance for reproducibility** | No request for the version of the reference genome, annotation (e.g., GENCODE M25), or the software/settings used to generate the DE table. | Different annotations can shift gene identifiers, making downstream validation difficult. |

---

### Revised prompt

> **You are given a processed differential‑expression table from a mouse liver RNA‑seq experiment comparing high‑fat diet (HFD) to control.**  
> The table contains at least the following columns: Gene ID (Ensembl or MGI symbol), log₂ fold‑change (HFD vs. control), raw p‑value, and adjusted p‑value (FDR).  
>   
> **Task:** Identify and return a concise, biologically interpretable set of “important” genes that satisfy **all** of the following criteria:  
> 1. **Statistical significance:** Adjusted p‑value (FDR) ≤ 0.05.  
> 2. **Effect size:** |log₂FC| ≥ 1 (i.e., at least a two‑fold change).  
> 3. **Directionality:** Separate the results into **up‑regulated** (log₂FC > 0) and **down‑regulated** (log₂FC < 0) groups.  
>   
> **Output format:**  
> - For each direction, provide a bullet‑list of genes.  
> - Each bullet should show: `Gene Symbol (Ensembl ID): log₂FC = X.XX, FDR = Y.YYY`.  
> - After the lists, add a brief interpretation (2‑3 sentences) highlighting any notable patterns (e.g., enrichment of lipid‑metabolism genes among up‑regulated genes, or enrichment of inflammatory pathways among down‑regulated genes).  
>   
> **Optional (if you have the data):** If you can perform a quick over‑representation analysis (e.g., GO Biological Process or KEGG) on the up‑ and down‑regulated sets, report the top 3 enriched terms (with FDR < 0.1) for each set.  
>   
> **Assumptions you may state:**  
> - The input table was generated with a standard DE pipeline (e.g., DESeq2, edgeR, or limma‑voom) using the mouse reference genome GRCm38/mm10 and annotation (e.g., GENCODE M25 or Ensembl release 108).  
> - No additional covariates (batch, sex, age) were included in the model; if they were, please note them.  
>   
> **If the supplied data do not meet the above format,** ask for clarification (e.g., request the DE table or specify which columns are present) before proceeding.

---

#### How the revision addresses the critiques

| Issue | How the revision fixes it |
|-------|---------------------------|
| Ambiguity | Explicitly defines “important” via statistical (FDR ≤ 0.05) and effect‑size (|log₂FC| ≥ 1) thresholds, and separates up/down regulation. |
| Assumptions | States assumptions about the DE pipeline, reference genome, and annotation; invites the user to correct them if needed. |
| Failure modes | Provides clear cut‑offs to avoid over‑/under‑inclusion, requires directionality, and asks for optional enrichment to add context. |
| Reproducibility | Requests version‑specific genome/annotation and notes the DE method used, making downstream validation easier. |
| Usability | Gives a concrete output format (bullet list with gene symbol, ID, log₂FC, FDR) and a short interpretation, reducing the chance of overwhelming or vague answers. |

Feel free to adjust the thresholds (e.g., FDR ≤ 0.1 or |log₂FC| ≥ 0.58) depending on the stringency you need for your specific study. The structure, however, ensures that the model’s response will be consistent, transparent, and directly actionable.
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
