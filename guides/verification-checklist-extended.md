# Verification Checklist Template

## Purpose

A structured checklist for verifying LLM-assisted outputs before publication, sharing, or reliance. This is a workflow document to be used by researchers, not a prompt for an LLM.

## When to Use

- Before publishing any work that included LLM assistance
- Before sharing LLM-generated content with collaborators
- Before making decisions based on LLM outputs
- As part of your research documentation workflow

---

## Pre-Verification: Output Characterization

Before verifying, characterize what you're checking:

**Type of output** (check all that apply):
- [ ] Contains factual claims
- [ ] Contains citations or references
- [ ] Contains statistics or quantitative claims
- [ ] Contains code
- [ ] Contains recommendations or advice
- [ ] Contains synthesized information from multiple sources
- [ ] Will be published or shared externally

**Stakes assessment**:
- [ ] Low (personal notes, brainstorming)
- [ ] Medium (shared with collaborators, informal use)
- [ ] High (publication, grant submission, decisions affecting others)

**Verification effort should scale with stakes.**

---

## Verification Checklist by Content Type

### Citations and References

For any citation, reference, or claim about what a paper says:

- [ ] **Citation exists**: Search for the exact citation in PubMed, Google Scholar, or relevant database
  - Author names correct?
  - Title correct?
  - Journal/year correct?
  - DOI resolves (if provided)?

- [ ] **Citation says what's claimed**: Retrieve the paper and verify the attributed claim
  - Does the paper actually contain this finding?
  - Is the finding represented accurately (not oversimplified or distorted)?
  - Is context preserved (not cherry-picked)?

- [ ] **No fabricated citations**: List every citation and confirm each exists
  - Warning: LLMs routinely fabricate plausible-sounding citations

| Citation | Exists? | Says what claimed? | Notes |
|----------|---------|-------------------|-------|
| | | | |
| | | | |

---

### Factual Claims

For specific factual assertions (dates, names, statistics, definitions):

- [ ] **Identify all factual claims** that could be verified
- [ ] **Prioritize by importance**: Focus on claims you'll rely on or publish
- [ ] **Verify against authoritative sources**:
  - Primary literature (for scientific facts)
  - Official documentation (for technical specifications)
  - Authoritative references (textbooks, standards organizations)

| Claim | Source checked | Verified? | Notes |
|-------|---------------|-----------|-------|
| | | | |
| | | | |

---

### Statistics and Quantitative Claims

For any numbers, percentages, effect sizes, p-values:

- [ ] **Source identified**: Where does this number come from?
- [ ] **Number verified**: Does the source actually contain this statistic?
- [ ] **Context preserved**: Is the statistic used appropriately (not out of context)?
- [ ] **Recency checked**: Is this current or outdated?

Red flags for fabricated statistics:
- Suspiciously round numbers (exactly 50%, exactly 1000)
- Unusually precise numbers without citation (42.7% of studies show...)
- Numbers that perfectly support the argument

---

### Code

For any generated or suggested code:

- [ ] **Code runs**: Execute without errors
- [ ] **Output correct**: Test with known-answer inputs
- [ ] **Logic verified**: Trace through logic manually for critical operations
- [ ] **Edge cases tested**: Empty input, single item, boundary conditions
- [ ] **Packages/functions current**: Check that suggested packages exist and functions aren't deprecated
- [ ] **No security issues**: Review for obvious vulnerabilities (if applicable)

| Test case | Expected output | Actual output | Pass? |
|-----------|----------------|---------------|-------|
| | | | |
| | | | |

---

### Recommendations and Advice

For any suggestions, recommendations, or guidance:

- [ ] **Basis verified**: What is this recommendation based on?
- [ ] **Alternatives considered**: Is this the only reasonable approach?
- [ ] **Context appropriate**: Does this apply to my specific situation?
- [ ] **Expert check**: For important decisions, have I consulted a human expert?
- [ ] **Not just agreeing**: Is the LLM telling me what I want to hear?

---

### Synthesized Content

For information synthesized across multiple sources:

- [ ] **Sources identified**: What sources were used?
- [ ] **No additional sources introduced**: Are all sources from your provided materials (not hallucinated)?
- [ ] **Synthesis accurate**: Does the synthesis accurately represent each source?
- [ ] **Conflicts noted**: Are disagreements between sources acknowledged?
- [ ] **Attribution correct**: Are claims attributed to the correct sources?

---

## Verification Log

Document your verification for reproducibility:

**Output being verified**: [Description]

**Date**: [Date]

**Verification performed by**: [Name]

**Summary of checks performed**:


**Issues found**:


**Actions taken**:


**Final status**: [ ] Verified for use / [ ] Requires revision / [ ] Cannot verify—do not use

---

## Quick Checklist for Common Tasks

### Literature Synthesis Output
- [ ] Every citation verified to exist
- [ ] Every citation verified to say what's claimed
- [ ] No citations introduced beyond provided sources
- [ ] Synthesis checked against original papers

### Code Generation Output
- [ ] Runs without error
- [ ] Produces correct output on test cases
- [ ] Logic reviewed for critical sections

### Statistical Guidance Output
- [ ] Recommendations verified against authoritative sources
- [ ] Consulted with statistician for non-trivial analyses
- [ ] Assumptions checked against my actual data

### Writing Assistance Output
- [ ] No unsupported claims introduced
- [ ] All facts traceable to my data or cited sources
- [ ] Voice and meaning preserved in edits

---

## Red Flags Requiring Extra Scrutiny

Apply extra verification when you notice:

- [ ] Output is unusually clean or convenient
- [ ] Claims align perfectly with your hypothesis
- [ ] Specific statistics without clear sourcing
- [ ] References you've never encountered
- [ ] Confident assertions on topics you know are contested
- [ ] Recommendations that seem too simple for a complex problem
- [ ] The answer came too easily for a hard question

---

## Integration with Your Workflow

### For Manuscript Preparation
1. Use this checklist before submitting
2. Include verification notes in your research documentation
3. Consider adding "LLM Use Disclosure" to your methods section

### For Grant Writing
1. Verify all factual claims in significance section
2. Confirm cited preliminary data is accurately represented
3. Check that proposed approaches match actual capabilities

### For Code Development
1. Test all generated code before incorporating into pipelines
2. Document which functions were LLM-assisted
3. Retest after any modifications

---

## Documentation Template

For published work, consider documenting LLM assistance with:

```
LLM Assistance Disclosure:
- Task: [What you used LLM for]
- Model: [Which model, version if known]
- Date: [When used]
- Verification: [What checks you performed]
```

See `documentation/methods-disclosure-template.md` for Methods section language.

---

## Cross-References

- For citation-specific verification, see `guides/citation-warning.md`
- For adversarial critique before verification, see `validation/adversarial-critique.md`
- For uncertainty assessment, see `validation/uncertainty-elicitation.md`
- For cross-model validation, see `guides/cross-model-protocols.md`
