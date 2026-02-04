# Documentation Templates for LLM-Assisted Research

This document provides template language for disclosing large language model assistance in manuscripts. The appropriate level of detail depends on the extent of model use and its relevance to scientific claims. All templates should be adapted to specific circumstances and target venue requirements.

## Template 1: Light Assistance (Writing and Editing)

Use this template when model assistance was limited to prose refinement without contribution to scientific content.

> We used [MODEL NAME, e.g., Claude 3.5 Sonnet] to assist with manuscript preparation, including [specify: editing for clarity / improving prose flow / checking grammar]. All scientific content, analysis, and interpretation are the authors' own work. The model did not generate novel claims, analyze data, or contribute to the scientific conclusions.

## Template 2: Code Generation

Use this template when models assisted with developing analysis code.

> Analysis scripts were developed with assistance from [MODEL NAME]. The model was used to [specify: generate initial code templates / debug errors / translate between programming languages]. All generated code was reviewed for correctness, tested against known inputs with expected outputs, and validated before use in the reported analyses. Final scripts are available at [REPOSITORY LINK].

## Template 3: Literature Processing

Use this template when models assisted with literature synthesis tasks.

> We used [MODEL NAME] to assist with literature synthesis, specifically for [specify: summarizing individual papers / identifying themes across sources / structuring comparative analyses]. All citations were independently verified against primary sources, and all factual claims attributed to cited works were confirmed by direct review of the original publications. The model was not used to identify papers or generate citations.

## Template 4: Systematic or Substantial Use

Use this template when model assistance was extensive or central to the work.

> Large language model assistance was used in this work as detailed below. For all model-assisted components, we used [MODEL NAME AND VERSION] accessed via [interface: API / web interface / local deployment] during [DATE RANGE]. Temperature was set to [VALUE]; other parameters were [specify or note defaults were used].
>
> **Literature review:** [Describe specific use and verification procedures]
>
> **Code development:** [Describe specific use and testing procedures]
>
> **Writing:** [Describe specific use]
>
> **Data processing:** [Describe specific use and validation procedures]
>
> Verification procedures included [specify: manual citation verification, code testing with known-answer validation, cross-referencing with primary sources, expert review of statistical approaches, etc.]. Prompts used for systematic analyses are available in [supplementary materials / repository / upon request].

## Key Principles

**Specificity matters.** "AI-assisted" is insufficient. Name the model, describe the task, explain the verification approach.

**Distinguish contribution types.** Writing polish differs from data analysis. Make clear what the model did and did not contribute to.

**Document verification.** Readers need to know not only that a model was used but how outputs were validated before inclusion.

**Retain records.** Even if not published, maintain records sufficient to answer questions about model use during peer review.

**Check current requirements.** Journal policies vary and continue evolving. Verify current guidelines for target venues before submission.

## Four Questions to Be Prepared to Answer

Regardless of disclosure format, researchers should be prepared to answer:

1. What models were used, including version or access date where available?
2. What purposes did model assistance serve?
3. How were outputs verified before use?
4. What human judgment was applied to model outputs?

Being prepared to answer these questions honestly satisfies both the spirit of transparency and current disclosure requirements for most venues.
