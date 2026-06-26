# Test Results: writing/results-description.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-25.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** writing/results-description.md
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
````

## Model Output
````
## Results Paragraph

Probiotic treatment partially attenuated the increase in intestinal permeability induced by DSS colitis (Figure 3). Serum FITC-dextran concentrations, measured 4 hours after oral gavage, were significantly elevated in DSS-treated animals compared to controls (8.7 ± 1.2 μg/mL vs. 2.1 ± 0.3 μg/mL, respectively; Tukey post-hoc, p < 0.001), confirming that DSS treatment produced substantial barrier disruption. Animals receiving DSS plus probiotic supplementation showed intermediate serum fluorescence levels (4.3 ± 0.6 μg/mL), which were significantly lower than the DSS-only group (p = 0.003), indicating a partial reduction in permeability with probiotic treatment. However, FITC-dextran levels in the DSS + Probiotic group remained significantly elevated relative to untreated controls (p = 0.048), demonstrating that probiotic treatment did not fully restore barrier function to baseline levels. One-way ANOVA confirmed an overall significant effect of treatment group (F(2,21) = 18.4, p < 0.001).

---

**Flagged for your attention:**

> [VERIFY: The DSS + Probiotic group mean (4.3 μg/mL) represents approximately a 51% reduction from the DSS-only peak but remains roughly double the control value. This pattern is internally consistent and the statistics align with the means and SEMs as reported. No values appear implausible. However, you may wish to confirm that the p = 0.048 for DSS + Probiotic vs. Control is correctly attributed to that specific comparison in your statistical output, as it sits close to the α = 0.05 threshold and warrants precise reporting.]
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
