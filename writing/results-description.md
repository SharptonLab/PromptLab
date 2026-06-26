# Results Description Prompt

## Task Description

Generate clear, accurate prose describing your research results from figures, tables, or statistical output, focusing on what the data show without over-interpretation.

## When to Use

- Translating statistical output into readable prose
- Describing patterns visible in figures or tables
- Drafting initial results text when you know what you found but struggle to articulate it
- Ensuring you've described all key findings from a complex figure

## When NOT to Use

- When you haven't analyzed the data yourself (you must understand what you're describing)
- To generate interpretations beyond what the data support
- For results outside your expertise where you can't evaluate the description's accuracy
- As a substitute for actually understanding your statistical analyses

## The Prompt

```
Context: I am writing the Results section for a manuscript on {RESEARCH_TOPIC}. I need to describe the findings shown in {FIGURE/TABLE/ANALYSIS DESCRIPTION}.

My data summary:
{PASTE YOUR DATA: statistical output, figure description, table, or key numbers}

Research question this addresses: {SPECIFIC_QUESTION}

Task: Write a results paragraph describing these findings. Follow these guidelines:

1. **State the main finding first**: Lead with what the data show, not the methods used to show it.

2. **Report specific values**: Include effect sizes, confidence intervals, p-values, or other relevant statistics as provided.

3. **Describe patterns accurately**: For figures, describe trends, differences, or distributions visible in the data.

4. **Reference the figure/table**: Include appropriate references (e.g., "Figure 2A").

5. **Maintain appropriate scope**: Describe what IS shown; do not extrapolate beyond the data.

Constraints:
- Use ONLY the data I have provided—do not invent statistics or findings
- Distinguish between statistically significant and non-significant findings
- Do not interpret causation from correlation
- Do not include discussion of mechanisms or implications (that's for Discussion)
- If the data are unclear or seem inconsistent, flag this rather than smoothing over it
- Flag any values that seem unusual with [VERIFY: concern]

Output format: One to three paragraphs of results prose, with figure/table references in parentheses.
```

## Prompt Components Explained

| Component | Purpose |
|-----------|---------|
| **Context** | Research topic provides framing for how to describe findings |
| **Data summary** | The actual numbers/output—essential input |
| **Research question** | Focuses the description on what matters |
| **Guidelines** | Produce well-structured results prose following conventions |
| **Constraints** | Prevent over-interpretation and fabrication; maintain Results vs. Discussion boundary |

## Example Input

```
Context: I am writing the Results section for a manuscript on gut microbiome response to antibiotics. I need to describe the findings shown in Figure 2 (alpha diversity over time).

My data summary:
Shannon diversity (mean ± SD):
- Control Day 0: 4.2 ± 0.3
- Control Day 7: 4.1 ± 0.4
- Antibiotic Day 0: 4.3 ± 0.3
- Antibiotic Day 7: 2.1 ± 0.5

Statistical test: Two-way repeated measures ANOVA
- Time × Treatment interaction: F(1,18) = 45.2, p < 0.001
- Post-hoc (Tukey): Antibiotic Day 7 vs all other groups, p < 0.001
- No significant difference between Control Day 0 vs Day 7 (p = 0.82)

n = 10 mice per group

Research question: Does antibiotic treatment reduce gut microbial diversity?
```

## Example Output

Antibiotic treatment significantly reduced gut microbial alpha diversity. At baseline (Day 0), Shannon diversity indices were comparable between control (4.2 ± 0.3) and antibiotic-treated (4.3 ± 0.3) mice (Figure 2A). Following 7 days of ampicillin treatment, Shannon diversity in antibiotic-treated mice dropped to 2.1 ± 0.5, representing an approximately 50% reduction from baseline. In contrast, control mice maintained stable diversity throughout the experiment (Day 7: 4.1 ± 0.4; p = 0.82 vs. Day 0).

A two-way repeated measures ANOVA revealed a significant time × treatment interaction (F(1,18) = 45.2, p < 0.001), indicating that the trajectory of diversity differed between treatment groups. Post-hoc comparisons confirmed that Day 7 diversity in antibiotic-treated mice was significantly lower than all other group-timepoint combinations (Tukey HSD, p < 0.001 for all comparisons).

## Test Input

Use the following data to test this prompt:

```
Context: I am writing the Results section for a manuscript on probiotic effects on gut barrier function. I need to describe the findings shown in Figure 3 (intestinal permeability assay).

My data summary:
FITC-dextran permeability (serum fluorescence, μg/mL, mean ± SEM):
- Control: 2.1 ± 0.3 (n=8)
- DSS only: 8.7 ± 1.2 (n=8)
- DSS + Probiotic: 4.3 ± 0.6 (n=8)

Statistical test: One-way ANOVA with Tukey post-hoc
- Overall ANOVA: F(2,21) = 18.4, p < 0.001
- DSS vs Control: p < 0.001
- DSS + Probiotic vs DSS: p = 0.003
- DSS + Probiotic vs Control: p = 0.048

Additional notes:
- FITC-dextran administered by oral gavage 4 hours before sacrifice
- Higher fluorescence = increased permeability (leaky gut)
- DSS = dextran sulfate sodium colitis model

Research question: Does probiotic treatment protect against colitis-induced intestinal barrier dysfunction?

Task: Write a results paragraph describing these findings. Follow these guidelines:

1. **State the main finding first**: Lead with what the data show, not the methods used to show it.

2. **Report specific values**: Include effect sizes, confidence intervals, p-values, or other relevant statistics as provided.

3. **Describe patterns accurately**: For figures, describe trends, differences, or distributions visible in the data.

4. **Reference the figure/table**: Include appropriate references (e.g., "Figure 2A").

5. **Maintain appropriate scope**: Describe what IS shown; do not extrapolate beyond the data.

Constraints:
- Use ONLY the data I have provided—do not invent statistics or findings
- Distinguish between statistically significant and non-significant findings
- Do not interpret causation from correlation
- Do not include discussion of mechanisms or implications (that's for Discussion)
- If the data are unclear or seem inconsistent, flag this rather than smoothing over it
- Flag any values that seem unusual with [VERIFY: concern]

Output format: One to three paragraphs of results prose, with figure/table references in parentheses.
```

**Expected output should include:**
- Main finding stated first (probiotic reduces DSS-induced permeability)
- All statistics reported accurately (F value, p values, means ± SEM)
- Correct interpretation of direction (higher = more permeable = worse)
- Figure reference (Figure 3)
- No discussion of mechanisms (that's for Discussion section)

**Verification points:**
- All numbers match the input exactly
- Statistical significance correctly characterized for each comparison
- No causal claims (probiotic "associated with" or "reduced", not "caused")
- No content beyond what's provided in the data summary

## Failure Modes

- **Inventing statistics**: May fabricate p-values, effect sizes, or sample sizes not provided
- **Over-interpretation**: May describe findings as "demonstrating" causation when data are correlational
- **Significance inflation**: May describe non-significant trends as if they were significant
- **Under-description**: May miss important patterns you intended to highlight
- **Discussion creep**: May add mechanistic speculation or implications belonging in Discussion
- **Smoothing inconsistencies**: May gloss over apparent contradictions or unexpected findings in your data

## Verification Requirements

1. **Verify all numbers**: Check that every statistic matches your actual output exactly
2. **Check figure references**: Ensure references point to correct panels/figures
3. **Verify significance claims**: Confirm that findings described as significant actually meet your threshold
4. **Check for additions**: Remove any findings or statistics not in your original data
5. **Verify scope**: Ensure descriptions don't extend beyond what the data actually show
6. **Review for interpretation**: Remove any mechanistic or causal claims that belong in Discussion

## Variations

### Multiple figure panels
For complex figures with multiple panels:
```
Describe findings panel by panel. For each panel:
- State what comparison or analysis it shows
- Report the key finding
- Provide the relevant statistics
```

### Table description
For tabular data:
```
Highlight the key patterns across rows/columns. Identify:
- The most notable findings (largest effects, significant results)
- Any unexpected or counter-intuitive results
- Overall patterns or trends
```

### Supplementary results
For less central findings:
```
Write a brief description (2-3 sentences) suitable for supplementary text. Focus on whether findings were significant and the direction of effects.
```

### Negative results
For null findings:
```
Describe clearly what was tested and that no significant effect was found. Include effect sizes and confidence intervals to characterize the null result. Do not characterize negative results as failures.
```

## Model Notes

```
Tested across the panel; verdicts set by human review.

- Claude Opus 4 (claude-opus-4-5-20251101) (2026-02-04): Pass
- claude-opus-4.7 (2026-06-23): Pass
- claude-sonnet-4.6 (2026-06-23): Pass
- gemini-2.5-pro (2026-06-23): Pass
- gpt-5.5 (2026-06-23): Pass
- nemotron-3-super-120b (2026-06-23): Needs revision
- step-3.7-flash (2026-06-23): Pass

Full per-model raw outputs and reviewer notes: tests/writing/results-description/
```

## Cross-References

- For methods underlying these results, see `writing/methods-drafting.md`
- For statistical test selection, see `statistics/test-selection.md`
- For interpreting results (Discussion), consider the distinct purpose—Results describes, Discussion interprets
- For adversarial review of results claims, see `validation/adversarial-critique.md`
