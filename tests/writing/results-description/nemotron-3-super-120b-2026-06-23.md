# Test Results: writing/results-description.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-23.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** writing/results-description.md
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
```

## Model Output
```


In the intestinal permeability assay, serum FITC‑dextran fluorescence was markedly elevated in mice treated with DSS compared with untreated controls, indicating increased gut barrier permeability (Figure 3). The mean fluorescence in the DSS group was 8.7 ± 0.6 μg/mL (n = 8), which was significantly higher than the control value of 2.1 ± 0.3 μg/mL (p < 0.001). Administration of the probiotic alongside DSS reduced the fluorescence to 4.3 ± 0.6 μg/mL, a value that was significantly lower than DSS alone (p = 0.003) but remained significantly higher than control (p = 0.048). Overall, one‑way ANOVA revealed a significant effect of treatment (F(2,21) = 18.4, p < 0.001).
```

## Assessment

_Machine-suggested (UNCONFIRMED) — drafted by Claude Opus 4.7 on 2026-06-24 to speed T4 review. An author must independently read the Model Output above and set the real Recommendation. Anything labeled here is triage, not domain expert review._

**Machine triage:** **Numerical transcription error**: writes the DSS group SEM as `8.7 ± 0.6 μg/mL` when the input was `8.7 ± 1.2`. This is a fabricated number — the prompt's most important constraint ('every statistic matches your actual output exactly') is violated. Other values (F, p, control, DSS+Probiotic) appear correct.

**Suggested verdict (UNCONFIRMED):** Needs revision

**What still needs human verification:**
- Numerical error: DSS SEM is 0.6 in the response but 1.2 in the input notes — confirm this is a transcription error (not e.g., a user-side typo).
- All other numbers should also be re-verified, since one transcription error suggests other numbers should not be trusted at face value.
- Cross-model: this is the only output of the six with a numerical error in the means/SEMs.

## Overall Assessment
- **Recommendation:** PENDING AUTHOR REVIEW
- **Notes:**

## Verification Steps Tested
_Which verification requirements from the prompt were checked, and results._
