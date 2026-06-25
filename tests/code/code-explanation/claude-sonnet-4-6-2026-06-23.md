# Test Results: code/code-explanation.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-23.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** code/code-explanation.md
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
Context: I am a {RESEARCHER_ROLE} trying to understand code from {SOURCE: e.g., "a published paper," "a collaborator," "a tutorial"}. My programming background: {YOUR_LEVEL: e.g., "intermediate R, learning Python," "comfortable with basic Python, new to pandas"}.

The code I need explained:
```{language}
{PASTE_CODE}
```

What I already understand: {WHAT_YOU_KNOW_ABOUT_IT}

What confuses me: {SPECIFIC_QUESTIONS_OR_CONFUSING_PARTS}

Task: Explain this code clearly. Please provide:

1. **Overview**: What does this code accomplish overall? (2-3 sentences)

2. **Step-by-step walkthrough**: Go through the code section by section, explaining:
   - What each section does
   - Why it's done this way
   - Any non-obvious operations or syntax

3. **Key concepts**: Explain any programming concepts, patterns, or library features I might not know based on my stated background.

4. **Inputs and outputs**: What does this code expect as input? What does it produce?

5. **Potential issues**: Are there any limitations, edge cases, or potential problems with this code?

Constraints:
- Adjust explanation depth to my stated background level
- If the code has errors or poor practices, note them
- Don't assume I know jargon—define terms as needed
- If parts are unclear without more context, say so

Output format: Structured explanation with numbered sections and code snippets where helpful.

Context: I am a microbiome researcher trying to understand code from a published paper on differential abundance analysis. My programming background: comfortable with R basics, new to DESeq2.

The code I need explained:
```r
dds <- DESeqDataSetFromMatrix(countData = otu_counts,
                               colData = sample_metadata,
                               design = ~ treatment + batch)

dds <- dds[rowSums(counts(dds)) >= 10, ]

dds <- DESeq(dds)

res <- results(dds, contrast = c("treatment", "diseased", "healthy"),
               alpha = 0.05, lfcThreshold = 1)

res_sig <- res[which(res$padj < 0.05 & abs(res$log2FoldChange) > 1), ]
```

What I already understand: I know this is analyzing count data and comparing treatments.

What confuses me:
- What does the design formula (~ treatment + batch) mean?
- Why is there a filter for rowSums >= 10?
- What does contrast = c("treatment", "diseased", "healthy") do?
- What is lfcThreshold and why use it?
- Why check padj AND log2FoldChange when lfcThreshold was already set?
```

## Model Output
```
# DESeq2 Differential Abundance Analysis: Code Explanation

---

## 1. Overview

This code uses the DESeq2 package to identify microbial taxa (OTUs) that differ in abundance between diseased and healthy samples. It takes raw count data, filters out rare taxa, runs a statistical model that accounts for both treatment group and batch effects, and extracts a final list of significantly different taxa. Think of it as a rigorous way to answer: *"Which microbes are genuinely more or less abundant in disease, after controlling for technical noise?"*

---

## 2. Step-by-Step Walkthrough

### Step 1: Building the DESeq2 Object

```r
dds <- DESeqDataSetFromMatrix(countData = otu_counts,
                               colData = sample_metadata,
                               design = ~ treatment + batch)
```

**What it does:** Packages your data into a special DESeq2 container object called `dds` (short for *DESeqDataSet*).

**The three arguments:**

| Argument | What it expects | Your data |
|----------|----------------|-----------|
| `countData` | Matrix of raw integer counts | Rows = OTUs/taxa, Columns = samples |
| `colData` | Table of sample information | Rows = samples, Columns = metadata variables |
| `design` | Formula describing your experiment | Which variables explain the data |

**About the design formula `~ treatment + batch`:**

The `~` symbol means *"is modeled by"* — read it as *"abundance is modeled by treatment and batch."*

- **`treatment`** is your biological variable of interest (diseased vs. healthy)
- **`batch`** refers to technical batches — for example, if samples were processed in two separate sequencing runs, they may have systematic differences unrelated to biology

The `+` means *"include both variables in the model simultaneously."* DESeq2 will mathematically separate the batch effect from the treatment effect, so your results reflect true biological differences rather than technical artifacts.

> **Analogy:** Imagine measuring plant growth under two fertilizers, but half the plants were grown in summer and half in winter. Adding `batch` (season) to your model lets you ask: *"What's the fertilizer effect, holding season constant?"*

---

### Step 2: Filtering Low-Count Taxa

```r
dds <- dds[rowSums(counts(dds)) >= 10, ]
```

**What it does:** Removes any OTU (row) where the total count across *all* samples is fewer than 10 reads.

**Breaking down the syntax:**
- `counts(dds)` — extracts the raw count matrix from the DESeq2 object
- `rowSums(...)` — adds up all counts for each OTU across every sample
- `>= 10` — creates a TRUE/FALSE value for each OTU
- `dds[..., ]` — keeps only the rows (OTUs) where the condition is TRUE

**Why do this?**

Taxa with very few total reads are problematic for two reasons:

1. **Statistical power:** DESeq2 cannot reliably detect differences in something you barely observed. A taxon seen 3 times total could easily be noise.
2. **Multiple testing burden:** Every OTU you test increases the penalty applied to your p-values (more on this below). Removing hopeless tests makes your remaining results stronger.

> ⚠️ **Note:** A threshold of 10 is common but somewhat arbitrary. Some researchers use stricter filters (e.g., present in at least X% of samples). The right threshold depends on your dataset size and sequencing depth.

---

### Step 3: Running the DESeq2 Analysis

```r
dds <- DESeq(dds)
```

**What it does:** This single function call does the heavy statistical lifting — it runs three things internally:

1. **Size factor estimation** — Normalizes for differences in sequencing depth between samples (some samples may have been sequenced more deeply than others)
2. **Dispersion estimation** — Estimates how variable each taxon's counts are across samples (microbiome data is notoriously variable)
3. **Model fitting** — Fits a negative binomial statistical model to each taxon and tests for differences

**Why negative binomial?** Regular count data often follows a Poisson distribution, but microbiome counts are *overdispersed* — meaning they're even more variable than Poisson predicts. The negative binomial distribution handles this extra variability.

---

### Step 4: Extracting Results for Your Comparison

```r
res <- results(dds, contrast = c("treatment", "diseased", "healthy"),
               alpha = 0.05, lfcThreshold = 1)
```

**What it does:** Pulls out the statistical results specifically comparing diseased vs. healthy samples.

**The `contrast` argument:**

```r
contrast = c("treatment", "diseased", "healthy")
#             ^variable    ^numerator   ^denominator
```

This tells DESeq2:
- Look at the `treatment` variable
- Calculate fold change as: **diseased ÷ healthy**
- So a *positive* log2FoldChange means higher in diseased; *negative* means lower in diseased

> **Why specify this?** Your model includes multiple variables. DESeq2 needs to know exactly which comparison you want from the `treatment` variable.

**The `alpha = 0.05` argument:**

Sets your significance threshold for the adjusted p-value. DESeq2 uses this internally to optimize a statistical procedure (independent filtering) that improves power. It does *not* automatically filter your results — that happens in Step 5.

**The `lfcThreshold = 1` argument:**

This is subtle and important. Normally, DESeq2 tests: *"Is the fold change different from zero?"* Setting `lfcThreshold = 1` changes the test to: *"Is the fold change significantly **greater than 1** (in log2 units)?"*

- A log2FoldChange of 1 = a **2-fold** difference (2¹ = 2)
- A log2FoldChange of 2 = a **4-fold** difference (2² = 4)

This means you're only flagging taxa with *both* statistical significance *and* a biologically meaningful effect size built into the test itself. This is more conservative and reduces false positives.

---

### Step 5: Filtering Significant Results

```r
res_sig <- res[which(res$padj < 0.05 & abs(res$log2FoldChange) > 1), ]
```

**What it does:** Creates a final filtered table containing only the statistically significant, biologically meaningful taxa.

**Breaking down the syntax:**
- `res$padj` — the adjusted p-value column (the `$` accesses a column by name)
- `res$log2FoldChange` — the effect size column
- `abs(...)` — absolute value, so you capture both increased AND decreased taxa
- `&` — both conditions must be TRUE
- `which(...)` — returns the row numbers where conditions are TRUE
- `res[..., ]` — keeps only those rows

**Your key question: Why filter again if `lfcThreshold = 1` was already set?**

This is a genuinely good question, and the answer reveals a subtle distinction:

| | `lfcThreshold = 1` in `results()` | `abs(res$log2FoldChange) > 1` in filter |
|---|---|---|
| **What it does** | Changes the *statistical test* — tests whether LFC is significantly beyond 1 | Filters the *observed estimate* — keeps rows where the estimated LFC exceeds 1 |
| **Why it matters** | Affects p-value calculation (more rigorous) | Removes any edge cases where the estimate is borderline |

In practice, if `lfcThreshold = 1` was set correctly, the second filter on `log2FoldChange` should rarely remove additional rows — but it acts as a safety net and makes the intent of the code explicit to readers. Some researchers argue the second filter is redundant; others keep it for clarity.

> ⚠️ **Potential issue:** The `padj` column will contain `NA` for some taxa (those filtered out by DESeq2's internal procedures). The `which()` function safely handles NAs by ignoring them, which is why `which()` is used here instead of direct bracket indexing.

---

## 3. Key Concepts to Know

**Adjusted p-values (`padj`) vs. regular p-values (`pvalue`):**
When you test thousands of OTUs simultaneously, you'd expect ~5% to appear significant by chance even if nothing is real. The adjusted p-value (using the Benjamini-Hochberg method by default) corrects for this *multiple testing problem*. Always use `padj` for microbiome studies.

**Log2 fold change:**
Fold changes are expressed in log base-2 because it's symmetric:
- LFC of +1 = 2× higher in diseased
- LFC of -1 = 2× lower in diseased (not -2×)
- LFC of 0 = no change

**The `$` operator in R:**
Used to access a named column in a data frame or results object. `res$padj` means "the `padj` column inside `res`."

---

## 4. Inputs and Outputs

**Inputs required:**

| Object | Format | Requirements |
|--------|--------|--------------|
| `otu_counts` | Matrix or data frame | Rows = taxa, Columns = samples; **must be raw integer counts** (not normalized, not rarefied) |
| `sample_metadata` | Data frame | Rows = samples (matching column names of `otu_counts`); must contain `treatment` and `batch` columns |

**Output (`res_sig`):**

A table where each row is a significantly differentially abundant taxon, with columns including:

| Column | Meaning |
|--------|---------|
| `baseMean` | Average normalized count across all samples |
| `log2FoldChange` | Effect size (positive = higher in diseased) |
| `lfcSE` | Uncertainty in the fold change estimate |
| `stat` | Test statistic |
| `pvalue` | Raw p-value |
| `padj` | Multiple-testing corrected p-value |

---

## 5. Potential Issues and Limitations

**⚠️ Critical: DESeq2 requires raw counts**
If your `otu_counts` have been normalized, rarefied, or transformed (e.g., relative abundance), DESeq2's internal normalization will be invalid. Always use raw read counts.

**⚠️ The batch variable must be in your metadata**
If `sample_metadata` doesn't have a column literally named `batch`, this code will throw an error. Check that column names match exactly.

**⚠️ Sample order must match**
The column names of `otu_counts` must match the row names of `sample_metadata` in the same order. Mismatches will silently assign wrong metadata to samples — a serious error.

**⚠️ DESeq2 for microbiome data is debated**
DESeq2 was designed for RNA-seq. Some researchers argue it has inflated false positive rates for microbiome data due to compositional effects. Alternatives like `ANCOM-BC`, `MaAsLin2`, or `ALDEx2` are worth considering and comparing.

**⚠️ The rowSums >= 10 filter is simplistic**
A taxon present in only one sample with 10 reads will pass this filter, but a taxon present in 9 of 10 samples with 1 read each will also pass. A presence-based filter (e.g., present in ≥ 20% of samples) may be more biologically meaningful.

---

## Quick Reference Summary

```
Raw counts + metadata
        ↓
DESeqDataSetFromMatrix()  → Package data with experimental design
        ↓
Filter rowSums >= 10      → Remove rare/uninformative taxa
        ↓
DESeq()                   → Normalize, estimate variance, fit models
        ↓
results() with contrast   → Extract diseased vs. healthy comparison
        ↓
Filter padj & LFC         → Keep only significant, large-effect taxa
        ↓
res_sig                   → Your differentially abundant microbes
```
```

## Assessment

_Machine-suggested (UNCONFIRMED) — drafted by Claude Opus 4.7 on 2026-06-24 (refresh) to speed T4 review. An author must independently read the Model Output above and set the real Recommendation. Anything labeled here is triage, not domain expert review. This draft was regenerated after a harness bug (truncated test inputs on this prompt) was fixed and the model was re-run with the full prompt._

**Machine triage:** Complete 5-section walkthrough, well-calibrated depth for stated audience ("comfortable with R basics, new to DESeq2"). Explicitly answers all five user confusion points and includes a comparison table for the lfcThreshold-in-results-call vs the post-hoc |LFC|>1 filter, with the correct conceptual distinction (test-statistic vs estimate filter). Defines jargon (negative binomial, overdispersion, padj/BH, log2FoldChange). Closes with a useful pipeline-flow ASCII summary. Recommends ANCOM-BC, MaAsLin2, ALDEx2 as microbiome alternatives. Cross-model comparison: agrees with opus-4.7, gpt-5.5, nemotron, and step-3.7 on substance; nemotron diverges on whether lfcThreshold triggers an LRT vs modifying the Wald null. No fabricated citations or refusals.

**Suggested verdict (UNCONFIRMED):** Pass with notes

**What still needs human verification:**
- That the lfcThreshold-vs-filter conceptual table is correct (it is in agreement with DESeq2 docs, but worth a domain check).
- The contrast-format claim that the format is `c(variable, numerator, denominator)`.
- Whether the recommended alternatives (ANCOM-BC, MaAsLin2, ALDEx2) and the implicit suggestion to use `lfcShrink()` are conventions you want students to be shown.

## Overall Assessment
- **Recommendation:** PENDING AUTHOR REVIEW
- **Notes:**

## Verification Steps Tested
_Which verification requirements from the prompt were checked, and results._
