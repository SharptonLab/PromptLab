# Test Results: meta-prompting.md

## Test Metadata
- **Prompt:** fundamentals/meta-prompting.md
- **Model:** Claude Opus 4 (claude-opus-4-5-20251101)
- **Date:** 2026-02-04
- **Tester:** Claude Code (automated testing)

## Test Input Used
Standard test input from prompt file (RNA-seq prompt critique scenario)

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
```
**Critique:**

**1. Ambiguities and underspecification:**

- **"Important" is undefined**: This is the most critical problem. "Important" could mean:
  - Statistically significant (p < 0.05 or FDR < 0.05)?
  - Large effect size (|log2FC| > 1? > 2?)?
  - Biologically relevant to a specific pathway or process?
  - Novel/unexpected findings?
  - Genes with known disease relevance?

- **No output format specified**: Will you get a list? A table? A narrative? Ranked how?

- **"My RNA-seq results" is vague**: What format? DESeq2 output? Raw counts? A results table? The model can't work with data it doesn't have.

- **No information about the analysis already performed**: Has differential expression analysis been done? What tool (DESeq2, edgeR, limma)? What comparisons?

- **"High-fat diet to control" but no research question**: Are you interested in lipid metabolism? Inflammation? Insulin signaling? Without context, the model will guess what you care about.

- **No scope constraints**: Should the response focus on 5 genes? 50? All significant genes? Specific pathways?

**2. Assumptions that might not hold:**

- Assumes the model knows what "important" means to you
- Assumes the model can see your data (it cannot unless you provide it)
- Assumes a single correct answer exists
- Assumes the model understands your experimental design from one sentence
- Assumes the model knows your field and what findings would be interesting

**3. Likely failure modes:**

- **Inconsistent outputs**: Without defined criteria, each query will emphasize different genes
- **Hallucination of gene functions**: Model may confidently describe gene functions that are inaccurate or outdated
- **Generic responses**: Model may list well-known genes involved in fat/liver without actually analyzing your data
- **Overinterpretation**: Model may draw biological conclusions not supported by DE analysis alone
- **Missing your actual question**: You may care about one aspect (e.g., fibrosis) and get responses about another (e.g., lipogenesis)

**4. Improvements needed:**

- Define "important" with specific, objective criteria
- Specify what data you'll provide and in what format
- State your research question or hypothesis
- Constrain the scope of the response
- Prevent overinterpretation with explicit boundaries
- Request uncertainty acknowledgment

---

**Revised prompt:**

```
Context: I've completed differential gene expression analysis on RNA-seq data from a mouse liver study comparing 12 weeks of high-fat diet (n=6) versus control diet (n=6). Analysis was performed using DESeq2. I'm interested in identifying genes that may drive the metabolic dysfunction phenotype we observe (hepatic steatosis).

Data I'm providing:
[Paste DESeq2 results table with columns: gene_symbol, log2FoldChange, lfcSE, pvalue, padj]

Task: Identify the most relevant differentially expressed genes based on the criteria below.

Selection criteria for "important" genes:
- Statistically significant: padj < 0.05
- Meaningful effect size: |log2FoldChange| > 1.0
- Priority given to genes with known roles in lipid metabolism, insulin signaling, or hepatic steatosis

Output format:
Provide a table with:
| Gene | log2FC | padj | Biological relevance (1-2 sentences) |

Include:
- Top 10-15 upregulated genes meeting criteria
- Top 10-15 downregulated genes meeting criteria
- Brief summary (3-4 sentences) of key biological themes

Constraints:
- Only include genes that meet the statistical criteria above
- For biological relevance, cite the specific process or pathway (e.g., "involved in fatty acid synthesis via SREBP1 pathway")
- Acknowledge if a gene's function is unclear or its relevance to metabolic disease is speculative
- Do not infer causation from differential expression alone
- Flag any claims about gene function that should be verified

Evaluation criteria:
Prioritize accuracy over comprehensiveness. I would rather have fewer genes with solid justification than many genes with uncertain relevance.
```

This revised prompt:
- Defines "important" with objective criteria (padj < 0.05, |log2FC| > 1)
- Specifies the biological context (hepatic steatosis, metabolic dysfunction)
- Provides a clear output format (table with specific columns)
- Sets scope (top 10-15 per direction)
- Includes constraints against overinterpretation
- Requires uncertainty acknowledgment
```

## Overall Assessment

- **Recommendation:** Pass
- **Notes:** The meta-prompting approach worked effectively. The critique correctly identified that "important" is undefined—the central ambiguity in the original prompt. The revised prompt demonstrates excellent prompt engineering: specific statistical criteria (padj < 0.05, |log2FC| > 1), clear output format (table with defined columns), biological context (hepatic steatosis), scope constraints (top 10-15 genes), and explicit instructions to acknowledge uncertainty and avoid overinterpretation. The revised prompt follows all principles from the structured-prompt-template.

## Verification Steps Tested
- [x] Critique identifies "important" as undefined - **Yes, first point**
- [x] Critique notes no output format specified - **Yes**
- [x] Critique notes missing analysis information - **Yes**
- [x] Critique notes missing research question/context - **Yes**
- [x] Revised prompt includes specific criteria - **Yes (padj < 0.05, |log2FC| > 1)**
- [x] Revised prompt defines output format - **Yes (table with specified columns)**
- [x] Revised prompt includes data placeholders - **Yes**
- [x] Revised prompt includes constraints against overinterpretation - **Yes**
