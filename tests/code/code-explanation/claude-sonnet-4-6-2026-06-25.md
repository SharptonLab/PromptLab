# Test Results: code/code-explanation.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-25.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** code/code-explanation.md
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
````

## Model Output
````
# DESeq2 Differential Abundance Analysis: Code Explanation

## 1. Overview

This code identifies which microbial taxa (OTUs) are significantly more or less abundant between diseased and healthy samples, while accounting for batch effects. It takes raw count data, runs a statistical model, and filters the results down to only the taxa with both statistically significant and biologically meaningful differences. Think of it as asking: *"Which microbes are genuinely behaving differently in disease, and not just due to technical noise?"*

---

## 2. Step-by-Step Walkthrough

### Step 1: Building the DESeq2 Object

```r
dds <- DESeqDataSetFromMatrix(countData = otu_counts,
                               colData = sample_metadata,
                               design = ~ treatment + batch)
```

**What it does:** Packages your data into a special DESeq2 container object (`dds` = DESeq Dataset).

**The three inputs:**
- `countData = otu_counts` — Your OTU table, where **rows are taxa and columns are samples**, containing raw integer counts (not normalized, not log-transformed)
- `colData = sample_metadata` — Your sample information table, where **rows are samples** and columns are variables like treatment group, batch, patient ID, etc.
- `design = ~ treatment + batch` — The statistical formula (explained below)

**What does `~ treatment + batch` mean?**

The `~` means *"is modeled by"* — it's R's way of writing a statistical formula. This tells DESeq2:

> "When testing for differences, account for both treatment group AND batch."

Think of it like this: imagine your samples were processed in two separate lab runs (batches). Batch effects can create artificial differences that have nothing to do with disease. The formula tells the model:

```
OTU abundance ~ treatment effect + batch effect + random noise
```

By including `batch`, the model mathematically "subtracts out" batch variation before testing treatment differences. This is called **covariate correction** — `batch` is a covariate you're controlling for, not testing.

> ⚠️ **Important:** Both `treatment` and `batch` must be column names that actually exist in your `sample_metadata` table, or you'll get an error.

---

### Step 2: Filtering Low-Count Taxa

```r
dds <- dds[rowSums(counts(dds)) >= 10, ]
```

**What it does:** Removes any OTU (row) where the total counts across ALL samples add up to less than 10.

**Breaking down the syntax:**
```r
counts(dds)          # extracts the count matrix from the dds object
rowSums(...)         # adds up counts across each row (each OTU)
... >= 10            # creates TRUE/FALSE for each row
dds[TRUE/FALSE, ]    # keeps only rows marked TRUE
                     # the comma means "keep all columns (samples)"
```

**Why do this?**

Taxa seen only 1-2 times total across your entire study are essentially undetectable noise. Keeping them causes two problems:

1. **Statistical power problem:** DESeq2 can't reliably estimate fold changes for something it barely observed — the uncertainty is enormous
2. **Multiple testing problem:** Every extra OTU you test increases your chances of false positives (explained more in Step 4)

> ⚠️ **Potential issue:** A threshold of 10 *total* counts is quite lenient. If you have 50 samples, an OTU could pass this filter while appearing in only 1 sample with 10 counts. Many researchers use stricter filters like: *"must have at least X counts in at least Y samples."* The right threshold depends on your study size and goals.

---

### Step 3: Running the DESeq2 Model

```r
dds <- DESeq(dds)
```

**What it does:** This single function call does a lot of heavy lifting internally:

| Internal Step | What It Means in Plain Language |
|--------------|--------------------------------|
| Size factor estimation | Corrects for the fact that some samples were sequenced more deeply than others |
| Dispersion estimation | Learns how variable each OTU is across samples |
| Model fitting | Fits the statistical model you specified in `design` |
| Hypothesis testing | Tests whether treatment differences are real |

You don't need to call these steps separately — `DESeq()` handles them in sequence. This is why DESeq2 is popular: it wraps complex statistics into one function.

---

### Step 4: Extracting Results for a Specific Comparison

```r
res <- results(dds, contrast = c("treatment", "diseased", "healthy"),
               alpha = 0.05, lfcThreshold = 1)
```

**What it does:** Pulls out the statistical results for one specific comparison.

**What does `contrast = c("treatment", "diseased", "healthy")` mean?**

The contrast tells DESeq2 exactly which comparison to make. The three elements are always:
```
c("variable name", "numerator group", "denominator group")
```

So this means: *"Compare diseased vs. healthy within the treatment variable"*

The result will be expressed as:
```
log2(average abundance in diseased / average abundance in healthy)
```
- **Positive values** → OTU is more abundant in diseased
- **Negative values** → OTU is more abundant in healthy

> ⚠️ **Order matters:** Flipping "diseased" and "healthy" would flip the sign of all your fold changes. Always double-check which group is your numerator.

**What is `lfcThreshold = 1`?**

`lfc` stands for **log2 Fold Change**. A threshold of 1 means you're only interested in OTUs that are at least **2-fold different** between groups (because 2¹ = 2).

This changes the statistical test itself. Instead of asking:
> "Is the fold change different from zero?" *(default)*

It asks:
> "Is the fold change significantly *greater than 2-fold*?" *(with lfcThreshold = 1)*

This is a stricter, more biologically meaningful test. A tiny but statistically significant difference (say, 1.1-fold) might be real but irrelevant in practice.

**What is `alpha = 0.05`?**

This sets the significance threshold for the **adjusted p-value** (explained next). It affects how DESeq2 reports which results pass the significance cutoff in summary outputs.

---

### Step 5: Filtering to Significant Results

```r
res_sig <- res[which(res$padj < 0.05 & abs(res$log2FoldChange) > 1), ]
```

**What it does:** Creates a final filtered table keeping only OTUs that meet both criteria simultaneously.

**Breaking down the syntax:**
```r
res$padj              # the adjusted p-value column from results
res$log2FoldChange    # the fold change column
abs(...)              # absolute value (so we catch both + and - changes)
condition1 & condition2  # both must be TRUE
which(...)            # returns the row numbers where condition is TRUE
res[row_numbers, ]    # keeps only those rows
```

**What is `padj` (adjusted p-value)?**

When you test thousands of OTUs simultaneously, you'd expect some to look significant purely by chance. For example, at p < 0.05, if you test 1,000 OTUs, ~50 would appear significant by random chance alone — these are **false positives**.

`padj` corrects for this using a method called **Benjamini-Hochberg correction** (also called FDR — False Discovery Rate). A `padj < 0.05` means: *"Among all the OTUs I'm calling significant, I expect at most 5% to be false positives."*

> Always use `padj`, not `pvalue`, for your final results.

**Why check `log2FoldChange > 1` again if `lfcThreshold = 1` was already set?**

This is your excellent question, and it reveals a subtle but important distinction:

| Setting | What it does |
|---------|-------------|
| `lfcThreshold = 1` in `results()` | Changes the **statistical test** — tests whether LFC is significantly beyond ±1 |
| `abs(res$log2FoldChange) > 1` in filtering | Filters on the **estimated LFC value** itself |

These are not redundant — they're doing different things. However, in practice, if `lfcThreshold = 1` was applied, most results passing `padj < 0.05` will already have `abs(log2FoldChange) > 1`. The manual filter is being used as an **extra safety net**, possibly out of caution or habit.

> ⚠️ **Potential issue:** This double-filtering is not wrong, but it's worth knowing it's somewhat redundant here. If someone removed `lfcThreshold = 1` from the `results()` call but kept the manual filter, the statistical test would change but the output table might look similar — that would be a meaningful difference in rigor.

---

## 3. Key Concepts to Know

**DESeq2 was designed for RNA-seq but works for microbiome data** — with caveats. Microbiome count data is often more sparse (lots of zeros) and compositional (counts are relative, not absolute) than gene expression data. Some researchers prefer tools like `ANCOM-BC` or `MaAsLin2` for microbiome specifically. This doesn't make the code wrong, just worth knowing.

**The `$` operator** accesses a column by name from a data frame or results object:
```r
res$padj           # gets the padj column from res
res$log2FoldChange # gets the log2FoldChange column
```

**Row/column indexing with `[rows, columns]`:**
```r
dds[rowSums(counts(dds)) >= 10, ]  # filter rows, keep all columns
res[which(res$padj < 0.05), ]      # filter rows, keep all columns
```
The empty space after the comma means "keep everything."

---

## 4. Inputs and Outputs

### Inputs Required

| Object | Structure | Requirements |
|--------|-----------|--------------|
| `otu_counts` | Matrix or data frame | Rows = OTUs/taxa, Columns = samples; **raw integer counts only** |
| `sample_metadata` | Data frame | Rows = samples (matching column names of `otu_counts`); must contain columns named `treatment` and `batch` |

> ⚠️ **Critical:** The column names of `otu_counts` must exactly match the row names of `sample_metadata`. DESeq2 will error or silently misalign data if these don't correspond.

### Outputs Produced

| Object | What It Is |
|--------|-----------|
| `dds` (after `DESeq()`) | Fitted model object — contains everything, used for downstream analysis |
| `res` | Results table for all OTUs tested: columns include `log2FoldChange`, `pvalue`, `padj`, standard error, etc. |
| `res_sig` | Filtered subset of `res` — only the statistically significant, biologically meaningful hits |

---

## 5. Potential Issues and Limitations

**1. Sample size in `colData` vs. `countData` mismatch**
If the samples in your metadata don't match the columns in your count table, DESeq2 will throw an error. Always verify:
```r
all(colnames(otu_counts) == rownames(sample_metadata))  # should return TRUE
```

**2. The filter threshold of 10 may be too lenient**
As mentioned, consider a more stringent filter based on your sample size. A common alternative:
```r
# Keep OTUs with >= 5 counts in at least 20% of samples
keep <- rowSums(counts(dds) >= 5) >= (0.2 * ncol(dds))
dds <- dds[keep, ]
```

**3. DESeq2 may not be optimal for microbiome data**
DESeq2 assumes a negative binomial distribution for counts. Microbiome data often has excess zeros and compositional constraints that can inflate false positives. This is an active area of research — the code isn't wrong, but you should be aware of this debate in the field.

**4. `batch` must be a factor, not continuous**
If your batch variable is stored as numbers (1, 2, 3...), R might treat it as continuous rather than categorical. Check with:
```r
class(sample_metadata$batch)  # should say "factor" or "character"
# If it says "numeric" or "integer", convert it:
sample_metadata$batch <- as.factor(sample_metadata$batch)
```

**5. NAs in `padj`**
DESeq2 automatically sets `padj` to `NA` for OTUs with very low counts or extreme outliers. The `which()` function in the filtering step handles this correctly (it ignores NAs), but be aware that your `res_sig` table won't include these flagged OTUs.

---

**Summary in one sentence:** This code builds a corrected statistical model on your OTU counts, tests each taxon for disease-associated changes while controlling for batch effects, and returns a filtered table of taxa that are both statistically reliable and meaningfully different in abundance.
````

## Assessment

_Machine-suggested (UNCONFIRMED) — drafted by Claude Opus 4.7 on 2026-06-26 to speed T4 review. An author must independently read the Model Output above and set the real Recommendation. Anything labeled here is triage, not domain expert review._

**Machine triage:** Output covers all 5 requested sections, uses tables to organize material, and explicitly addresses each user-stated confusion. No truncation; concludes with a one-sentence summary. Cross-model: substantively agrees with Opus 4.7, GPT-5.5, Nemotron, and Step on every major concept (design formula, low-count filter rationale, contrast direction, lfcThreshold semantics, padj). Cannot verify DESeq2 internals are technically correct without domain review.

**Suggested verdict (UNCONFIRMED):** Pass with notes

**What still needs human verification:**
- Claim that `lfcThreshold = 1` and `abs(log2FoldChange) > 1` are "doing different things" but the post-filter is mostly redundant — Step flags a one-sided test concern that should be checked
- Recommendation to "always use `padj`, not `pvalue`" is correct in spirit but absolutist; verify reviewer comfort
- The suggested alternative filter (`rowSums(counts(dds) >= 5) >= (0.2 * ncol(dds))`) — confirm it is well-formed R and a sensible default
- Whether explanation depth is appropriately calibrated to the stated background

**Local code check:** N/A — this prompt asks the model to explain existing code, no model-generated runnable code to test.

## Overall Assessment
- **Recommendation:** PENDING AUTHOR REVIEW
- **Notes:**

## Verification Steps Tested
_Which verification requirements from the prompt were checked, and results._
