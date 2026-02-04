# Code Explanation Prompt

## Task Description

Get clear explanations of unfamiliar code—what it does, how it works, and why it's written that way. Useful for understanding code from papers, tutorials, collaborators, or your own past work.

## When to Use

- Understanding code accompanying a published paper
- Learning from tutorials or examples
- Reviewing a collaborator's contribution
- Revisiting your own code after time has passed
- Evaluating whether code does what documentation claims

## When NOT to Use

- As a substitute for learning the language fundamentals
- When you need to verify the code is correct (explanation ≠ validation)
- For code that contains sensitive or proprietary information you shouldn't share
- When the code is so simple that explanation adds no value

## The Prompt

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
```

## Prompt Components Explained

| Component | Purpose |
|-----------|---------|
| **Source of code** | Helps calibrate explanation—paper code often has different conventions than tutorials |
| **Your background** | Allows appropriate depth and terminology |
| **What you understand** | Avoids explaining things you already know |
| **What confuses you** | Focuses explanation on your actual gaps |
| **Structured output** | Ensures comprehensive explanation |

## Example Input

```
Context: I am a microbiome researcher trying to understand code from a published paper on 16S analysis. My programming background: comfortable with basic R, new to the tidyverse.

The code I need explained:
```r
ps_rel <- transform_sample_counts(ps, function(x) x / sum(x))

top_taxa <- names(sort(taxa_sums(ps_rel), decreasing = TRUE))[1:20]

ps_top <- prune_taxa(top_taxa, ps_rel)

plot_data <- psmelt(ps_top) %>%
  group_by(Sample, Phylum) %>%
  summarise(Abundance = sum(Abundance), .groups = "drop") %>%
  mutate(Phylum = fct_reorder(Phylum, Abundance, .fun = sum, .desc = TRUE))

ggplot(plot_data, aes(x = Sample, y = Abundance, fill = Phylum)) +
  geom_bar(stat = "identity") +
  theme(axis.text.x = element_text(angle = 90, hjust = 1))
```

What I already understand: I know phyloseq objects contain OTU tables and metadata. I know ggplot makes plots.

What confuses me:
- What does transform_sample_counts do exactly?
- I don't understand the pipe (%>%) and what group_by/summarise do
- What is fct_reorder doing?
- Why is stat = "identity" needed?
```

## Example Output

### 1. Overview

This code creates a stacked bar chart showing the relative abundance of bacterial phyla across samples. It first converts counts to proportions, selects the 20 most abundant taxa, aggregates by phylum, and then plots the result. This is a standard visualization for exploring microbiome composition.

### 2. Step-by-Step Walkthrough

#### Converting to relative abundance
```r
ps_rel <- transform_sample_counts(ps, function(x) x / sum(x))
```
**What it does**: Converts raw read counts to relative abundances (proportions). For each sample, every taxon's count is divided by the total counts in that sample.

**Why**: Raw counts can't be compared across samples with different sequencing depths. If Sample A has 10,000 reads and Sample B has 50,000, raw counts are misleading. Proportions normalize this.

**How it works**: `transform_sample_counts()` applies a function to each sample column. The function `function(x) x / sum(x)` takes a vector of counts and divides each by the total.

#### Identifying top taxa
```r
top_taxa <- names(sort(taxa_sums(ps_rel), decreasing = TRUE))[1:20]
```
**What it does**: Finds the 20 taxa with highest total abundance across all samples.

**Breaking it down**:
- `taxa_sums(ps_rel)`: Sums each taxon across all samples, returning a named vector
- `sort(..., decreasing = TRUE)`: Sorts from highest to lowest
- `names(...)[1:20]`: Gets the taxon names (not values) for the top 20

**Why**: Plots with hundreds of taxa are unreadable. Focusing on the top 20 captures the major players while keeping the visualization clear.

#### Subsetting to top taxa
```r
ps_top <- prune_taxa(top_taxa, ps_rel)
```
**What it does**: Creates a new phyloseq object containing only the top 20 taxa.

#### Preparing plot data (the tidyverse pipeline)
```r
plot_data <- psmelt(ps_top) %>%
  group_by(Sample, Phylum) %>%
  summarise(Abundance = sum(Abundance), .groups = "drop") %>%
  mutate(Phylum = fct_reorder(Phylum, Abundance, .fun = sum, .desc = TRUE))
```

**The pipe (`%>%`)**: This operator passes the result of the left side as the first argument to the right side. It's read as "then." So this says: take the result of `psmelt`, THEN group it, THEN summarize it, THEN mutate it.

**`psmelt(ps_top)`**: Converts the phyloseq object to a "long" data frame where each row is one taxon in one sample, with columns for Sample, OTU, Abundance, and all taxonomy levels (Kingdom, Phylum, etc.).

**`group_by(Sample, Phylum)`**: Marks the data for grouped operations. Subsequent operations will be performed separately for each Sample-Phylum combination.

**`summarise(Abundance = sum(Abundance), .groups = "drop")`**: For each group (each Sample-Phylum pair), calculates the sum of all abundances. This aggregates multiple species within the same phylum. `.groups = "drop"` removes the grouping structure afterward.

**`mutate(Phylum = fct_reorder(...))`**: Reorders the Phylum factor levels based on total abundance (sum across all samples), in descending order. This ensures the legend and color assignment puts the most abundant phyla first.

#### Creating the plot
```r
ggplot(plot_data, aes(x = Sample, y = Abundance, fill = Phylum)) +
  geom_bar(stat = "identity") +
  theme(axis.text.x = element_text(angle = 90, hjust = 1))
```

**`stat = "identity"`**: By default, `geom_bar()` counts rows (like a histogram). `stat = "identity"` tells it to use the actual y values you provide (the Abundance column) rather than counting. Without this, you'd get wrong results.

**`theme(axis.text.x = ...)`**: Rotates x-axis labels 90 degrees so sample names don't overlap. `hjust = 1` right-aligns them.

### 3. Key Concepts

- **Pipe operator (`%>%`)**: From the magrittr package (loaded with tidyverse). Chains operations together. `x %>% f() %>% g()` is equivalent to `g(f(x))` but reads more naturally.

- **Factors**: R's way of handling categorical data. Factor levels determine the order in plots and tables. `fct_reorder()` is from the forcats package and reorders levels based on another variable.

- **Long vs. wide data**: phyloseq stores data in a specialized format. `psmelt()` converts it to "long" format where each observation is one row—the format ggplot expects.

### 4. Inputs and Outputs

**Input**: `ps` — a phyloseq object containing an OTU table with counts, taxonomy assignments, and sample metadata

**Output**: A ggplot stacked bar chart object. If assigned to a variable, it can be modified further. If printed, it displays the plot.

### 5. Potential Issues

- **Rare taxa disappear**: By taking only top 20 taxa, rare but potentially important taxa are excluded
- **Proportions don't sum to 1**: After filtering to top 20, the proportions no longer sum to 1.0 per sample (the excluded taxa's proportions are missing)
- **Sample order**: Samples are plotted in alphabetical order by default. You might want to order them by treatment group or a metadata variable
- **No statistical summary**: This is purely descriptive—no error bars or significance testing

## Test Input

Use the following code explanation scenario to test this prompt:

```
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

**Expected output should include:**
- Overview explaining DESeq2 differential abundance testing
- Explanation of design formula (treatment as variable of interest, batch as covariate)
- Rationale for low-count filtering (statistical power, unreliable estimates)
- Contrast explanation (comparing "diseased" to "healthy" reference)
- lfcThreshold explanation (testing for fold change greater than threshold, not just different from zero)
- Clarification that lfcThreshold affects the test, but additional filtering ensures both statistical and practical significance

**Verification points:**
- Explanations are accurate per DESeq2 documentation
- Appropriate depth for stated background level
- Confusing parts specifically addressed

## Failure Modes

- **Incorrect interpretation**: May misunderstand what code does, especially with complex or unusual patterns
- **Missing context**: May miss important details that depend on the broader codebase
- **Outdated syntax**: May explain deprecated approaches without noting they're outdated
- **Over-explanation**: May belabor points you already understand
- **False confidence**: May explain confidently even when uncertain
- **Missing errors**: May not notice bugs or problems in the code

## Verification Requirements

1. **Run the code**: Execute it yourself to confirm the explanation matches behavior
2. **Test your understanding**: Modify the code based on your understanding—does it behave as expected?
3. **Check key claims**: Verify specific claims (e.g., "this function does X") against documentation
4. **Cross-reference**: Compare explanation to package documentation or tutorials

## Variations

### Annotation request
For adding comments to code:
```
Task: Add clear comments to this code explaining each section. The comments should be suitable for someone at my background level.
```

### Comparison explanation
For understanding differences:
```
I have two versions of code that do similar things but are written differently:
Version 1: {CODE}
Version 2: {CODE}
Task: Explain the differences—what does each approach do differently, and what are the trade-offs?
```

### Refactoring explanation
For understanding "better" approaches:
```
Task: In addition to explaining what this code does, suggest how it could be written more clearly or efficiently, with explanations of why the changes are improvements.
```

## Model Notes

```
Models tested: [To be completed]
Date tested: [To be completed]
Notes: [To be completed]
```

## Cross-References

- For debugging errors in code, see `code/debugging.md`
- For generating new R code, see `code/r-script-generation.md`
- For generating new Python code, see `code/python-analysis.md`
- For writing tests for code, see `code/testing-requirements.md`
