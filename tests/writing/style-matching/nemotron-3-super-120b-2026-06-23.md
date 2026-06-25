# Test Results: writing/style-matching.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-23.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** writing/style-matching.md
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
Context: I am {PURPOSE: e.g., "finalizing a manuscript," "preparing a grant," "writing a review article"}. I need to revise text to match my established writing style.

Reference sample (my existing writing):
{PASTE 300-500 WORDS OF YOUR WRITING THAT EXEMPLIFIES YOUR STYLE}

Text to revise:
{PASTE TEXT THAT NEEDS STYLE MATCHING}

Task: Revise the "text to revise" to match the style of my reference sample. Preserve all substantive content while adjusting:

1. **Sentence structure**: Match my typical sentence length and complexity
2. **Voice and tone**: Match my level of formality, confidence, and directness
3. **Word choice**: Use vocabulary consistent with my writing; replace words I wouldn't use
4. **Hedging patterns**: Match how I express uncertainty or qualification
5. **Transition style**: Match how I connect ideas between sentences and paragraphs
6. **Technical language**: Match my balance of technical vs. accessible language

Constraints:
- Do NOT change the meaning or substance of the content
- Do NOT add new information or claims
- Do NOT remove important details or qualifications
- Flag any content issues (not style issues) as [CONTENT NOTE: description]
- If the reference sample is too short or inconsistent to reliably match, note this

Output format: Revised text, followed by a brief note on the key stylistic changes made.

Context: I am finalizing a manuscript on microbiome-immune interactions. I need to revise text to match my established writing style.

Reference sample (my existing writing):
"The intestinal immune system faces a unique challenge: it must tolerate the dense commensal microbiota while remaining vigilant against pathogens. This balance depends on continuous crosstalk between epithelial cells, innate immune populations, and the microbiome itself. Disruption of this crosstalk—whether through antibiotic exposure, dietary changes, or genetic susceptibility—can trigger inappropriate immune responses that damage host tissue.

We investigated how specific bacterial metabolites influence regulatory T cell development in the gut. Our approach combined gnotobiotic mouse models with targeted metabolomics to establish causal relationships between microbial products and immune phenotypes. This experimental strategy allowed us to move beyond correlation to identify specific molecular mediators of host-microbe communication."

Text to revise:
"In the present investigation, we sought to elucidate the mechanistic underpinnings of how the gut microbiome modulates host immune responses. Utilizing state-of-the-art methodological approaches including flow cytometric analysis and single-cell RNA sequencing technologies, we comprehensively characterized the immunological landscape of the intestinal mucosa. Our findings demonstrate that microbial colonization status significantly impacts the development and functional capacity of tissue-resident immune cell populations, with particularly notable effects observed in the regulatory T cell compartment."
```

## Model Output
```


We investigated how the gut microbiome modulates host immune responses. Using flow cytometry and single‑cell RNA sequencing, we characterized the immunological landscape of the intestinal mucosa. Our findings show that microbial colonization status significantly influences the development and functional capacity of tissue‑resident immune cells, with pronounced effects in the regulatory T cell compartment.

**Stylistic notes:**  
- Replaced lengthy, nominalized openings (“In the present investigation, we sought to elucidate the mechanistic underpinnings…”) with a direct, active‑voice clause.  
- Simplified methodological description (“Utilizing state-of-the-art methodological approaches including…”) to a concise instrumental phrase.  
- Substituted “demonstrate” and “comprehensively” with the more plain “show” and dropped unnecessary adverbs.  
- Matched sentence length and complexity to the reference sample (≈20‑25 words per sentence) and retained the confident, modestly formal tone.  
- Preserved all substantive content while aligning word choice and transition style with the original writing.
```

## Assessment

_Machine-suggested (UNCONFIRMED) — drafted by Claude Opus 4.7 on 2026-06-24 to speed T4 review. An author must independently read the Model Output above and set the real Recommendation. Anything labeled here is triage, not domain expert review._

**Machine triage:** Compact revision (8 lines, 1.1K chars). Preserves 'significantly influences' — correct retention of the statistical hedge. Retains 'immunological landscape' and 'functional capacity' (which Sonnet/Opus removed as inflated), so it's slightly less aggressive in stripping formality than the Claude responses. Still substantially closer to reference style than the original.

**Suggested verdict (UNCONFIRMED):** Pass

**What still needs human verification:**
- Retains 'significantly' — correct.
- Whether 'immunological landscape' and 'functional capacity' are kept-or-cut depends on the user's preference; the reference sample uses neither phrase, so the Claude trims are slightly more on-style.
- Cross-model: see Sonnet cell.

## Overall Assessment
- **Recommendation:** PENDING AUTHOR REVIEW
- **Notes:**

## Verification Steps Tested
_Which verification requirements from the prompt were checked, and results._
