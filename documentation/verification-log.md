# Verification Log

## Task Description

Provides a structured template for tracking verification of LLM outputs, ensuring that verification is systematic, documented, and appropriately calibrated to the stakes of each output.

## When to Use

- Tracking verification status across multiple LLM outputs in a project
- Documenting verification procedures for Methods section or supplementary materials
- Ensuring high-stakes outputs receive appropriate scrutiny before use
- Creating audit trails showing what was verified, how, and by whom

## When NOT to Use

- As a substitute for actually performing verification (the log documents verification, it doesn't perform it)
- For outputs you don't intend to use in research (casual exploration doesn't require formal verification logs)

## The Prompt

```
I need to create a verification log for LLM outputs in my research project. Help me set up a structured tracking system.

Project context:
{PROJECT_DESCRIPTION}

LLM outputs requiring verification:
1. {OUTPUT_TYPE_1}: {BRIEF_DESCRIPTION}
   - Stakes: {LOW/MEDIUM/HIGH}
   - Verification approach: {PLANNED_APPROACH}

2. {OUTPUT_TYPE_2}: {BRIEF_DESCRIPTION}
   - Stakes: {LOW/MEDIUM/HIGH}
   - Verification approach: {PLANNED_APPROACH}

[Continue as needed]

For each output type, help me define:
1. Specific verification criteria (what must be checked)
2. Verification methods (how to check it)
3. Evidence requirements (what documentation demonstrates verification)
4. Sign-off requirements (who confirms verification is complete)

Then generate a verification log template I can use to track each item.
```

## Prompt Components Explained

- **Context/Background:** Project description establishes domain and overall stakes
- **Task Specification:** Setting up a tracking system, not just a single entry
- **Structured Input:** Forces categorization by output type and stakes level
- **Output Format:** Requests both criteria definitions and tracking template
- **Verification calibration:** Stakes levels ensure proportional verification effort

## Example Input

```
Project context:
Microbiome meta-analysis examining gut microbiota signatures across 15 IBD studies. Manuscript in preparation for Gut Microbes.

LLM outputs requiring verification:

1. Literature summaries: Summaries of 15 individual papers used in meta-analysis
   - Stakes: HIGH (directly affects meta-analysis inclusion/interpretation)
   - Verification approach: Check each summary against original paper

2. R code for meta-analysis: Scripts for effect size calculation and random-effects models
   - Stakes: HIGH (produces primary results)
   - Verification approach: Test with synthetic data; validate against manual calculations

3. Methods section draft: LLM-assisted editing of author-written methods
   - Stakes: MEDIUM (accuracy matters but author reviewed)
   - Verification approach: Author line-by-line review

4. Figure captions: LLM-generated first drafts of figure legends
   - Stakes: LOW (will be heavily edited)
   - Verification approach: Author review and revision
```

## Example Output

### Verification Criteria by Output Type

**1. Literature Summaries (HIGH stakes)**

| Criterion | Method | Evidence |
|-----------|--------|----------|
| Paper exists and is correctly cited | Search PubMed/DOI | Screenshot of database record |
| Main finding accurately represented | Compare summary to abstract and results | Annotated comparison |
| Methods correctly described | Compare to Methods section | Checklist completion |
| Sample sizes and key statistics accurate | Compare to original tables | Side-by-side verification |
| Limitations accurately captured | Compare to Discussion | Annotated comparison |
| No fabricated claims or extrapolations | Full paper review | Reviewer sign-off |

**2. R Code for Meta-Analysis (HIGH stakes)**

| Criterion | Method | Evidence |
|-----------|--------|----------|
| Code executes without errors | Run on test data | Execution log |
| Effect size calculations correct | Compare to manual calculation (3+ studies) | Calculation spreadsheet |
| Random-effects model appropriate | Consult statistician; compare to published methods | Statistician sign-off |
| Heterogeneity statistics correct | Compare to manual calculation | Calculation verification |
| Output format matches requirements | Visual inspection | Sample output |
| Edge cases handled | Test with missing data, single studies | Test results |

**3. Methods Section (MEDIUM stakes)**

| Criterion | Method | Evidence |
|-----------|--------|----------|
| All statements factually accurate | Author review | Author sign-off |
| No unsupported claims introduced | Compare to data/results | Annotated review |
| Technical terms used correctly | Domain expert review | Reviewer sign-off |
| Appropriate level of detail | Compare to journal requirements | Checklist |

**4. Figure Captions (LOW stakes)**

| Criterion | Method | Evidence |
|-----------|--------|----------|
| Accurately describes figure content | Author review | Author sign-off |
| Statistics correctly reported | Compare to analysis output | Spot-check |

---

### Verification Log Template

```markdown
# Verification Log: {PROJECT_NAME}

Last updated: {DATE}
Verification coordinator: {NAME}

## Summary Status

| Category | Total Items | Verified | Pending | Failed |
|----------|-------------|----------|---------|--------|
| Literature summaries | | | | |
| Analysis code | | | | |
| Methods text | | | | |
| Figure captions | | | | |

## Detailed Verification Records

### Literature Summaries

#### Paper 1: {CITATION}
| Criterion | Status | Verified by | Date | Notes |
|-----------|--------|-------------|------|-------|
| Paper exists | ☐ | | | |
| Main finding accurate | ☐ | | | |
| Methods correct | ☐ | | | |
| Statistics accurate | ☐ | | | |
| Limitations captured | ☐ | | | |
| No fabrications | ☐ | | | |

**Overall status:** [ ] Not started [ ] In progress [ ] Complete [ ] Issues found
**Sign-off:** _________________ Date: _______

[Repeat for each paper]

### Analysis Code

#### Script: {SCRIPT_NAME}
| Criterion | Status | Verified by | Date | Notes |
|-----------|--------|-------------|------|-------|
| Executes without errors | ☐ | | | |
| Calculations correct | ☐ | | | |
| Model appropriate | ☐ | | | |
| Edge cases handled | ☐ | | | |

**Test results location:** {PATH}
**Statistician review:** [ ] Not needed [ ] Pending [ ] Complete
**Overall status:** [ ] Not started [ ] In progress [ ] Complete [ ] Issues found
**Sign-off:** _________________ Date: _______

[Repeat for each script]

### Methods Section

| Section | Author review | Technical review | Status |
|---------|--------------|------------------|--------|
| Study selection | ☐ | ☐ | |
| Data extraction | ☐ | ☐ | |
| Statistical analysis | ☐ | ☐ | |

**Sign-off:** _________________ Date: _______

### Figure Captions

| Figure | Author review | Status |
|--------|--------------|--------|
| Figure 1 | ☐ | |
| Figure 2 | ☐ | |
| Figure 3 | ☐ | |

**Sign-off:** _________________ Date: _______

## Issues Log

| Date | Item | Issue | Resolution | Resolved |
|------|------|-------|------------|----------|
| | | | | |

## Final Sign-off

All LLM-assisted outputs have been verified according to the criteria above.

Verified by: _________________ Date: _______
```

## Test Input

Use the following scenario to test this prompt:

```
Project context:
Systematic review of probiotic interventions for antibiotic-associated diarrhea, following PRISMA guidelines. Manuscript in preparation for Clinical Infectious Diseases.

LLM outputs requiring verification:

1. Paper screening summaries: Brief summaries of 45 potentially relevant papers for inclusion/exclusion decisions
   - Stakes: HIGH (affects which studies enter the systematic review)
   - Verification approach: Two independent reviewers check each summary against abstract; discrepancies resolved by third reviewer

2. Data extraction tables: Extracted study characteristics, interventions, and outcomes from 18 included studies
   - Stakes: HIGH (directly used in meta-analysis)
   - Verification approach: All extractions checked against original papers; 20% double-extracted by second reviewer

3. Risk of bias assessments: Initial drafts of Cochrane risk of bias assessments
   - Stakes: MEDIUM (author judgment required regardless)
   - Verification approach: Experienced author reviews and revises all assessments

4. PRISMA flow diagram text: Description of study flow for figure
   - Stakes: LOW (numbers will be verified against actual counts)
   - Verification approach: Author review against screening database
```

**Expected output should include:**

- Verification criteria tables for each output type with:
  - Specific criteria appropriate to the output type
  - Concrete verification methods
  - Evidence requirements
- Sign-off requirements scaled to stakes level
- Verification log template with:
  - Summary status table
  - Detailed records sections for each category
  - Issues log
  - Final sign-off section
- Proportional verification (HIGH stakes = more criteria than LOW stakes)

**Verification points:**
- Criteria are specific to systematic review context (PRISMA, Cochrane tools mentioned)
- Verification methods are actually feasible to perform
- Stakes levels result in proportional verification requirements
- Template is usable for tracking verification throughout project

## Failure Modes

- **Hallucination risks:** May suggest verification methods that sound rigorous but don't actually catch the relevant errors
- **Sycophancy risks:** May validate your verification plan as adequate when critical checks are missing
- **Overconfidence risks:** Structured templates can create false sense of rigor if not actually completed
- **Scope creep:** May generate overly elaborate verification requirements for low-stakes outputs

## Verification Requirements

For this template itself:
1. **Criteria completeness:** Ensure verification criteria actually catch the failure modes relevant to each output type
2. **Method feasibility:** Confirm you can actually perform the verification methods specified
3. **Proportionality:** Verify that verification effort matches stakes (don't over-verify low-stakes items or under-verify high-stakes items)
4. **Domain appropriateness:** Have a domain expert review criteria for technical accuracy

## Variations

**Quick verification checklist for single output:**
```
I need a quick verification checklist for a specific LLM output.

Output type: {TYPE}
Output content: {BRIEF_DESCRIPTION}
Stakes: {LOW/MEDIUM/HIGH}
My domain expertise in this area: {HIGH/MODERATE/LOW}

Generate a concise checklist (5-10 items) of what I should verify before using this output, with specific methods for each item.
```

**Retrospective verification audit:**
```
I need to audit verification that was performed earlier in this project.

Outputs that were verified:
{LIST}

Documentation available:
{LIST}

Help me assess: (1) Was verification adequate for the stakes? (2) What documentation gaps exist? (3) What additional verification, if any, is needed before publication?
```

## Standalone Template

For manual use without LLM assistance:

```markdown
# Verification Record

## Output Information
- **Description:**
- **Source interaction:** [Link to interaction log]
- **Date generated:**
- **Stakes level:** [ ] Low [ ] Medium [ ] High

## Verification Checklist

| Check | Method | Status | Verified by | Date | Notes |
|-------|--------|--------|-------------|------|-------|
| | | ☐ | | | |
| | | ☐ | | | |
| | | ☐ | | | |

## Issues Found

| Issue | Severity | Resolution | Resolved |
|-------|----------|------------|----------|
| | | | ☐ |

## Outcome
[ ] Verified - safe to use
[ ] Verified with modifications - [describe changes]
[ ] Failed verification - do not use
[ ] Requires expert review

## Sign-off
Verified by: _______________ Date: ______
```

## Model Notes

```
Models tested: [To be completed]
Date tested: [To be completed]
Notes: [To be completed]
```

## Related Prompts

- For logging individual interactions: `documentation/interaction-log-template.md`
- For generating Methods disclosures: `documentation/methods-disclosure-template.md`
- For adversarial critique of outputs: `validation/adversarial-critique.md`
- For verification checklists by output type: `guides/verification-checklist-extended.md`
