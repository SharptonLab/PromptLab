# Methods Disclosure Template

## Task Description

Generate appropriate disclosure language for documenting LLM use in the Methods section of a scientific manuscript, calibrated to the extent and nature of that use.

## When to Use

- Preparing a manuscript for submission where LLMs were used in any capacity
- Drafting Methods section language for LLM-assisted literature review, code generation, or writing assistance
- Ensuring disclosure meets emerging journal requirements for AI transparency
- Documenting LLM use in supplementary materials

## When NOT to Use

- As a substitute for actually documenting your LLM use (the template requires honest input about what you did)
- When you haven't kept records of your LLM interactions (go back and reconstruct records first)
- For generating disclosure language that minimizes or obscures the extent of LLM use

## The Prompt

```
I need to write a disclosure statement for the Methods section of a scientific manuscript describing my use of large language models. Help me draft appropriate disclosure language based on the following information.

Context about the manuscript:
- Field/topic: {FIELD_AND_TOPIC}
- Target journal: {JOURNAL_NAME}
- Journal's AI disclosure requirements (if known): {JOURNAL_REQUIREMENTS}

LLM use in this project:

1. Literature work:
   - Model(s) used: {LIT_MODELS}
   - Tasks performed: {LIT_TASKS}
   - Verification performed: {LIT_VERIFICATION}

2. Writing assistance:
   - Model(s) used: {WRITING_MODELS}
   - Tasks performed: {WRITING_TASKS}
   - Extent: {WRITING_EXTENT}

3. Code generation:
   - Model(s) used: {CODE_MODELS}
   - Tasks performed: {CODE_TASKS}
   - Testing/validation: {CODE_TESTING}

4. Data analysis or interpretation:
   - Model(s) used: {ANALYSIS_MODELS}
   - Tasks performed: {ANALYSIS_TASKS}
   - Verification: {ANALYSIS_VERIFICATION}

5. Other uses:
   - {OTHER_USES}

For any category not applicable, I will write "Not applicable."

Please draft disclosure language that:
- Is specific about what was done (not vague "AI-assisted" language)
- Distinguishes between different types of use
- Documents verification steps taken
- Is appropriate for the Methods section (substantial use) or Acknowledgments (minor use)
- Follows the principle of proactive transparency

Provide the disclosure in two versions:
1. Full Methods section version (for substantial LLM involvement)
2. Brief Acknowledgments version (for light assistance)
```

## Prompt Components Explained

- **Context/Background:** Field, journal, and requirements establish the appropriate level of detail and format
- **Task Specification:** Clear request for disclosure language with specific characteristics
- **Structured Input:** Categories force comprehensive documentation of LLM use
- **Constraints:** "Specific about what was done" prevents vague language; "proactive transparency" sets the ethical stance
- **Output Format:** Two versions address different disclosure needs

## Example Input

```
Field/topic: Microbiome research, 16S rRNA analysis of gut microbiota in IBD patients
Target journal: Gut Microbes
Journal's AI disclosure requirements: Requires disclosure of AI use in Author Statement

LLM use in this project:

1. Literature work:
   - Model(s) used: Claude 3 Opus
   - Tasks performed: Summarizing individual papers for initial literature review; identifying themes across 30 papers on IBD microbiome signatures
   - Verification performed: All citations verified against PubMed; all claims about individual papers checked against originals

2. Writing assistance:
   - Model(s) used: Claude 3 Opus
   - Tasks performed: Editing Methods and Results sections for clarity; suggesting structural improvements to Discussion
   - Extent: Light editing of author-written drafts; no substantial text generation

3. Code generation:
   - Model(s) used: Claude 3 Opus, GPT-4
   - Tasks performed: Generated initial R scripts for alpha diversity analysis and differential abundance testing with DESeq2
   - Testing/validation: All code tested with synthetic datasets with known properties; results validated against manual calculations for subset of samples

4. Data analysis or interpretation:
   - Model(s) used: Not applicable
   - Tasks performed: Not applicable
   - Verification: Not applicable

5. Other uses:
   - Drafting response to reviewer comments (structure and framing only; all scientific content author-generated)
```

## Example Output

**Methods Section Version:**

> Large language models (Claude 3 Opus, Anthropic; GPT-4, OpenAI) were used to assist with several aspects of this work. For literature review, Claude 3 Opus was used to summarize individual papers and identify thematic patterns across the literature on IBD microbiome signatures; all citations were verified against PubMed and all claims about cited works were confirmed by direct review of original publications. Analysis code for alpha diversity calculations and differential abundance testing (DESeq2) was generated with LLM assistance and validated through testing with synthetic datasets containing known properties, with results verified against manual calculations for a subset of samples. Writing assistance (editing for clarity and structural suggestions) was provided for the Methods, Results, and Discussion sections; all scientific content and interpretation are the authors' own work. Complete prompts and interaction logs are available upon request.

**Acknowledgments Version:**

> We acknowledge the use of large language models (Claude 3 Opus, GPT-4) for literature summarization, code generation, and manuscript editing. All LLM-assisted outputs were verified as described in Methods.

## Test Input

Use the following scenario to test this prompt:

```
Field/topic: Gut microbiome and metabolic disease, metagenomic analysis of microbial function in type 2 diabetes patients
Target journal: Nature Communications
Journal's AI disclosure requirements: Requires declaration of AI use in Author Contributions or Methods

LLM use in this project:

1. Literature work:
   - Model(s) used: GPT-4
   - Tasks performed: Summarizing 25 papers on microbiome-diabetes associations; extracting effect sizes from methods sections
   - Verification performed: All citations verified in PubMed; effect size extractions checked against original papers by two co-authors

2. Writing assistance:
   - Model(s) used: Claude 3 Opus
   - Tasks performed: Restructuring Introduction for narrative flow; editing Discussion for concision
   - Extent: Editing of author-written drafts; no new scientific claims introduced

3. Code generation:
   - Model(s) used: Claude 3 Opus
   - Tasks performed: Generated Python scripts for metabolic pathway abundance calculations using HUMAnN3 output
   - Testing/validation: Code tested with published HMP2 dataset; results compared to published values

4. Data analysis or interpretation:
   - Model(s) used: Not applicable
   - Tasks performed: Not applicable
   - Verification: Not applicable

5. Other uses:
   - Generating initial draft of figure legends (all revised by authors)
```

**Expected output should include:**

- Full Methods section version with:
  - Specific model names and versions
  - Distinct sections for literature work, writing assistance, code generation
  - Description of verification procedures for each category
  - Mention of supplementary materials availability
- Brief Acknowledgments version that is concise but complete
- Appropriate hedging (e.g., "assisted with" not "generated")
- No claims about verification steps not described in the input

**Verification points:**
- Disclosure accurately reflects the input provided (doesn't invent verification steps)
- Language is specific, not vague "AI-assisted"
- Two versions address different disclosure needs appropriately
- Tone is transparent without being defensive

## Failure Modes

- **Hallucination risks:** May generate overly specific disclosure language that doesn't match what you actually did (e.g., inventing verification steps you didn't perform)
- **Sycophancy risks:** May produce language that sounds thorough but actually obscures the extent of use; may validate insufficient verification as adequate
- **Overconfidence risks:** May present template language as if it meets all journal requirements when specific journals may have additional needs
- **Omission risks:** Template may not capture unusual or novel uses of LLMs in your workflow

## Verification Requirements

1. **Accuracy check:** Verify that every statement in the generated disclosure accurately reflects what you actually did
2. **Completeness check:** Confirm all LLM use is disclosed, not just the categories in the template
3. **Journal compliance:** Check generated language against specific journal requirements; modify as needed
4. **Verification claims:** Ensure any statements about verification reflect actual verification performed
5. **Colleague review:** Have a co-author review the disclosure for accuracy and completeness

## Variations

**Minimal use version:**
```
I used an LLM ({MODEL_NAME}) for light editing assistance on this manuscript. The LLM was used only to {SPECIFIC_TASK}. All scientific content, analysis, and interpretation are entirely my own work. Generate a brief disclosure statement appropriate for the Acknowledgments section.
```

**Systematic use with full documentation:**
```
[Add to main prompt]
I have complete logs of all LLM interactions. Please also generate a supplementary methods section that could accompany the manuscript, providing detailed documentation of prompts used and verification procedures.
```

## Model Notes

```
Models tested: [To be completed]
Date tested: [To be completed]
Notes: [To be completed]
```

## Related Prompts

- For documenting individual interactions: `documentation/interaction-log-template.md`
- For tracking verification: `documentation/verification-log.md`
- For understanding journal requirements: Search journal author guidelines directly
