# Test Results: writing/results-description.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-25.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** writing/results-description.md
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


In the intestinal permeability assay, serum fluorescence of oral FITC‑dextran was markedly elevated in mice receiving DSS alone compared with untreated controls (8.7 ± 1.2 μg/mL vs 2.1 ± 0.3 μg/mL), indicating a leaky gut (Figure 3). Administration of the probiotic alongside DSS reduced the fluorescence to an intermediate level (4.3 ± 0.6 μg/mL), which was significantly lower than DSS‑only mice (p = 0.003) but remained significantly higher than controls (p = 0.048 [VERIFY: borderline significance]). One‑way ANOVA confirmed overall differences among the three groups (F(2,21)=18.4, p < 0.001), with Tukey’s post‑hoc tests showing a significant increase in permeability for DSS versus control (p < 0.001) and a significant attenuation by probiotic treatment versus DSS (p = 0.003). The probiotic did not fully restore permeability to baseline, as the DSS + probiotic group remained significantly different from control (p = 0.048 [VERIFY: borderline significance]).
````

## Assessment

_Machine-suggested (UNCONFIRMED) — drafted by Claude Opus 4.7 on 2026-06-26 to speed T4 review. An author must independently read the Model Output above and set the real Recommendation. Anything labeled here is triage, not domain expert review._

**Machine triage:** Output produces Results paragraph faithfully using source numbers. Complete, no truncation. Uses **[VERIFY: borderline significance]** flags around the p=0.048 — more cautious framing than peers (e.g., Sonnet's [VERIFY]). Strong cross-model agreement on substance.

**Suggested verdict (UNCONFIRMED):** Pass

**What still needs human verification:**
- Whether the in-text [VERIFY: borderline significance] flag belongs in a draft submitted for author review or should be a margin comment
- Confirm all numbers match source
- That the "leaky gut" colloquial framing is appropriate

## Overall Assessment
- **Recommendation:** PENDING AUTHOR REVIEW
- **Notes:**

## Verification Steps Tested
_Which verification requirements from the prompt were checked, and results._
