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

````
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
````

## Prompt Components Explained

| Component | Purpose |
|-----------|---------|
| **Source of code** | Helps calibrate explanation—paper code often has different conventions than tutorials |
| **Your background** | Allows appropriate depth and terminology |
| **What you understand** | Avoids explaining things you already know |
| **What confuses you** | Focuses explanation on your actual gaps |
| **Structured output** | Ensures comprehensive explanation |

## Example Output

For a representative model response to the Test Input, see:

`tests/code/code-explanation/claude-sonnet-4-6-2026-06-25.md`

That cell was captured on 2026-06-25 and human-verified by both project reviewers as passing. Other panel models' responses (Claude Opus 4.7, GPT-5.5, Gemini 2.5 Pro, Nemotron 3 Super 120B, Step-3.7 Flash) are alongside it in the same directory.

## Test Input

Use the following code explanation scenario to test this prompt:

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
Tested across the panel; verdicts set by human review.

- Claude Opus 4 (claude-opus-4-5-20251101) (2026-02-04): Pass
- claude-opus-4.7 (2026-06-25): Pass
- claude-sonnet-4.6 (2026-06-25): Pass
- gemini-2.5-pro (2026-06-25): Pass
- gpt-5.5 (2026-06-25): Pass
- nemotron-3-super-120b (2026-06-25): Pass
- step-3.7-flash (2026-06-25): Pass

Full per-model raw outputs and reviewer notes: tests/code/code-explanation/
```

## Cross-References

- For debugging errors in code, see `code/debugging.md`
- For generating new R code, see `code/r-script-generation.md`
- For generating new Python code, see `code/python-analysis.md`
- For writing tests for code, see `code/testing-requirements.md`
