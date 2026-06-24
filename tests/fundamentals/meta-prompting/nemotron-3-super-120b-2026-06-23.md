# Test Results: fundamentals/meta-prompting.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-23.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** fundamentals/meta-prompting.md
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
I want your help with a task, but before I describe it, I want you to ask me clarifying questions to ensure you understand exactly what I need.

The task involves: {BRIEF_TASK_DESCRIPTION}

What questions do you have about the format, scope, audience, constraints, or purpose that would help you assist me effectively?

Here's a prompt I'm planning to use for analyzing differential gene expression results:

---
Look at my RNA-seq results and tell me which genes are important. The data is from a mouse liver study comparing high-fat diet to control.
---

Please critique this prompt:
1. What's ambiguous or underspecified?
2. What assumptions am I making that might not hold?
3. What failure modes might this prompt produce?
4. How would you improve it to make outputs more consistent and reliable?

Provide a revised version of the prompt incorporating your suggestions.
```

## Model Output
```


Sure! To give you the most useful critique and a revised prompt that will produce reliable, consistent outputs, I’d like to understand a few details about how you plan to use the prompt and what you expect from the model’s answer. Feel free to answer only the questions that are relevant; if something isn’t applicable, just let me know.

---

### 1. Format & Output Expectations  
- **What form should the model’s answer take?**  
  - A simple bullet‑list of gene symbols?  
  - A table with additional columns (e.g., log₂FC, adjusted p‑value, annotation)?  
  - A short narrative summary followed by a list?  
  - Something else (e.g., JSON, CSV‑style text)?

- **Do you want any extra information alongside each gene (e.g., fold‑change, significance, functional annotation, pathway membership)?**  

### 2. Scope & Statistical Thresholds  
- **Which columns are present in your RNA‑seq results file?** (e.g., GeneID, log₂FC, p‑value, adj‑p‑value, baseMean, etc.)  
- **What cut‑offs do you consider “important”?** (common choices: |log₂FC| ≥ 1 and FDR < 0.05, but you may have different thresholds)  
- **Do you want the model to filter the data itself, or will you pre‑filter and just ask for interpretation?**  

### 3. Audience & Purpose  
- **Who will read the model’s output?** (e.g., a fellow bioinformatician, a wet‑lab biologist, a clinician, a grant reviewer)  
- **What is the goal of the analysis?**  
  - Quick exploratory glance?  
  - Generation of a shortlist for downstream validation (qPCR, Western blot)?  
  - Input for pathway/enrichment analysis?  
  - Preparation of a figure legend or manuscript text?  

### 4. Constraints & Style  
- **Any length limits?** (e.g., “keep the answer under 150 words”)  
- **Tone preference?** (technical/jargon‑rich vs. plain‑language)  
- **Should the model cite the source of each statistic?** (e.g., “Gene X: log₂FC = +2.3, adj‑p = 0.001”)  

### 5. Data Availability & Handling  
- **Will you paste the relevant excerpt of the results table into the prompt, or will you refer to a file that the model can’t access?**  
- **If you plan to paste data, what format will you use?** (plain‑text tab‑separated, CSV snippet, etc.)  

### 6. Additional Context  
- **Are there any known confounders or batch effects you’d like the model to be aware of?**  
- **Do you want the model to suggest follow‑up analyses (e.g., GO enrichment, network analysis)?**  

---

Your answers to these questions will let me pinpoint exactly where the original prompt is vague or risky, and then craft a revised version that minimizes ambiguity, aligns with your statistical thresholds, and tailors the output to your audience and intended use. Looking forward to your clarification!
```

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
