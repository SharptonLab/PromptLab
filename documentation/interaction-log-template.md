# Interaction Log Template

## Task Description

Provides a structured template for documenting LLM interactions during research, capturing the metadata necessary for reproducibility and the context necessary for later evaluation.

## When to Use

- Documenting any LLM interaction that contributes to research outputs
- Building a record for Methods section disclosure
- Creating audit trails for systematic LLM use in a project
- Preparing supplementary materials for publication

## When NOT to Use

- For casual exploration unrelated to research outputs (though even exploratory use may be worth logging if it shaped your thinking)
- As a substitute for verification (logging is documentation, not validation)

## The Prompt

This prompt helps generate a structured log entry for an LLM interaction you've just completed.

```
I just completed an LLM interaction that I need to document for research purposes. Help me create a structured log entry.

Interaction details:
- Model: {MODEL_NAME_AND_VERSION}
- Date: {DATE}
- Time: {TIME}
- Interface: {API/WEB_INTERFACE/OTHER}

Purpose of interaction:
{BRIEF_DESCRIPTION_OF_WHY}

My prompt (paste the full prompt):
{FULL_PROMPT_TEXT}

Model response (paste full response or note if too long):
{FULL_RESPONSE_OR_NOTE}

Parameters (if known):
- Temperature: {TEMPERATURE}
- Max tokens: {MAX_TOKENS}
- Other: {OTHER_PARAMETERS}

Please format this as a structured log entry with the following sections:
1. Metadata (model, date, time, interface, parameters)
2. Purpose (one sentence)
3. Prompt (full text)
4. Response summary (2-3 sentences capturing key content)
5. Full response (or reference to where it's stored)
6. Verification status: [Not yet verified / Partially verified / Fully verified]
7. Verification notes: [To be completed]
8. Usage notes: [How this output was used in the research]
```

## Prompt Components Explained

- **Context/Background:** Interaction details and purpose establish what's being documented
- **Task Specification:** Creating a structured log entry
- **Structured Input:** Forces capture of essential metadata often forgotten
- **Output Format:** Explicit sections ensure consistent documentation across interactions
- **Verification placeholder:** Reminds user that logging is not verification

## Example Input

```
Model: Claude 3 Opus (claude-3-opus-20240229)
Date: 2024-03-15
Time: 14:32 EST
Interface: API via Python script

Purpose of interaction:
Generate initial R code for calculating beta diversity metrics from a phyloseq object

My prompt:
"Write an R function that takes a phyloseq object and calculates Bray-Curtis dissimilarity, Jaccard distance, and UniFrac distance (both weighted and unweighted) between all samples. Return a list containing the four distance matrices. Include comments explaining each step and note any required packages. The input phyloseq object will have an OTU table, sample data, taxonomy table, and phylogenetic tree."

Model response:
[Full code response - approximately 60 lines of R code with comments]

Parameters:
- Temperature: 0.3
- Max tokens: 2000
- Other: Default
```

## Example Output

```markdown
## Interaction Log Entry

### Metadata
| Field | Value |
|-------|-------|
| Model | Claude 3 Opus (claude-3-opus-20240229) |
| Date | 2024-03-15 |
| Time | 14:32 EST |
| Interface | API via Python script |
| Temperature | 0.3 |
| Max tokens | 2000 |
| Other parameters | Default |

### Purpose
Generate R function for calculating multiple beta diversity metrics from phyloseq object.

### Prompt
```
Write an R function that takes a phyloseq object and calculates Bray-Curtis dissimilarity, Jaccard distance, and UniFrac distance (both weighted and unweighted) between all samples. Return a list containing the four distance matrices. Include comments explaining each step and note any required packages. The input phyloseq object will have an OTU table, sample data, taxonomy table, and phylogenetic tree.
```

### Response Summary
Model generated a 60-line R function using phyloseq and vegan packages. Function calculates all four requested distance metrics and returns them as a named list. Includes input validation checking for presence of phylogenetic tree (required for UniFrac).

### Full Response
[Stored in: /logs/2024-03-15_beta-diversity-code.md]

### Verification Status
Partially verified

### Verification Notes
- [x] Code runs without errors on test phyloseq object
- [x] Bray-Curtis output matches manual vegan::vegdist() call
- [ ] UniFrac calculations not yet validated against known values
- [ ] Edge cases (samples with zero reads) not yet tested

### Usage Notes
Function incorporated into analysis pipeline (scripts/diversity_analysis.R). UniFrac validation pending before manuscript submission.
```

## Test Input

Use the following scenario to test this prompt:

```
Model: Claude 3.5 Sonnet (claude-3-5-sonnet-20241022)
Date: 2025-01-20
Time: 09:15 PST
Interface: Web interface (claude.ai)

Purpose of interaction:
Generate a linear mixed model formula in R for analyzing longitudinal microbiome diversity data with treatment and time as fixed effects, and subject as random effect

My prompt:
"I have longitudinal microbiome data: Shannon diversity measured at 4 timepoints (baseline, 1 week, 4 weeks, 12 weeks) in 2 treatment groups (control, antibiotic). Each of 20 subjects has all 4 timepoints. I want to test for treatment effect, time effect, and treatment × time interaction, accounting for repeated measures on subjects. Write the lmer() formula and explain the interpretation."

Model response:
[Response included lmer formula: diversity ~ treatment * time + (1|subject), explanation of fixed effects, random intercept interpretation, and code for fitting and testing with lmerTest package - approximately 40 lines]

Parameters:
- Temperature: Unknown (web interface)
- Max tokens: Unknown (web interface)
- Other: Default web interface settings
```

**Expected output should include:**

- Structured log entry with all metadata fields populated
- Purpose summarized in one sentence
- Full prompt text preserved exactly
- Response summary capturing key content (formula, approach)
- Verification status as "Not yet verified" (appropriate for new entry)
- Placeholder verification notes for what should be checked
- Usage notes section (empty or with placeholder)

**Verification points:**
- Log entry format is consistent and structured
- All provided metadata captured correctly
- Response summary accurately reflects what was described
- Verification status appropriately set to pending
- Template is usable for documentation purposes

## Failure Modes

- **Hallucination risks:** Low for this documentation task, but model may suggest verification steps that aren't actually sufficient
- **Sycophancy risks:** May validate your documentation as "complete" when important details are missing
- **Overconfidence risks:** Generated log structure may imply more rigor than actually applied
- **Format drift:** If used inconsistently, logs may become incomparable across interactions

## Verification Requirements

1. **Metadata accuracy:** Confirm model name, version, date, and parameters are correct
2. **Prompt completeness:** Verify the logged prompt is the exact text submitted (not paraphrased)
3. **Response accuracy:** Confirm response summary accurately represents the full response
4. **Verification honesty:** Ensure verification status reflects actual verification performed, not intended verification

## Variations

**Batch logging for multiple interactions:**
```
I completed {NUMBER} related LLM interactions for {PROJECT_COMPONENT}. Help me create a summary log entry that captures the overall workflow while referencing individual interaction logs.

Interactions:
1. {BRIEF_DESCRIPTION_1} - logged at {LOCATION_1}
2. {BRIEF_DESCRIPTION_2} - logged at {LOCATION_2}
...

Generate a workflow summary that documents the sequence, decision points, and cumulative verification status.
```

**Minimal quick-log for low-stakes interactions:**
```
Quick log entry needed:
Model: {MODEL}
Date: {DATE}
Task: {ONE_SENTENCE}
Prompt: {BRIEF_OR_FULL}
Result: {USEFUL/NOT_USEFUL/PARTIALLY_USEFUL}
Verification needed: {YES/NO}
Notes: {BRIEF}
```

## Standalone Template

For manual logging without LLM assistance, use this template directly:

```markdown
## Interaction Log: {DESCRIPTIVE_TITLE}

### Metadata
| Field | Value |
|-------|-------|
| Model | |
| Date | |
| Time | |
| Interface | |
| Temperature | |
| Max tokens | |
| Other parameters | |

### Purpose
[One sentence describing why this interaction was performed]

### Prompt
```
[Full prompt text]
```

### Response Summary
[2-3 sentences capturing key content of response]

### Full Response
[Full text OR reference to storage location]

### Verification Status
[ ] Not yet verified
[ ] Partially verified
[ ] Fully verified

### Verification Notes
- [ ] [Specific verification step 1]
- [ ] [Specific verification step 2]
- [ ] [Specific verification step 3]

### Usage Notes
[How this output was or will be used]
```

## Model Notes

```
Models tested: [To be completed]
Date tested: [To be completed]
Notes: [To be completed]
```

## Related Prompts

- For tracking verification across multiple outputs: `documentation/verification-log.md`
- For generating Methods disclosures from logs: `documentation/methods-disclosure-template.md`
