# Citation Warning: Verification Protocol

## Task Description

A meta-prompt and workflow for handling citations in LLM-assisted literature work. This is not a prompt to use with an LLM—it is guidance for users on the critical risk of citation fabrication and mandatory verification procedures.

## The Core Problem

**LLMs routinely fabricate citations.** This is not a bug that will be fixed; it is an architectural feature of how these models work. They generate plausible text, and plausible-sounding citations are fluent continuations of academic writing. The fabricated citations often:

- Use real author names in combinations that never published together
- Cite real journals with plausible but non-existent articles
- Create realistic-sounding titles that match the topic
- Include properly formatted but invented DOIs
- Mix real and fabricated elements (real first author, fake paper)

**Every citation from an LLM must be verified. No exceptions.**

## When This Applies

This warning applies whenever:

- You ask an LLM to provide citations or references
- You ask an LLM to summarize papers you haven't provided in full
- You use LLM output that includes any citation, even in passing
- An LLM references "studies show" or "research indicates" without you providing the sources
- You ask an LLM to write any text that should include citations

## When You Are Safer (But Still Verify)

Risk is reduced when:

- You provide the full text of papers and ask only about their contents
- You use retrieval-augmented systems that cite from a known database
- You explicitly instruct the model not to introduce outside sources

Even in these cases, verify that the model accurately represents what the papers say.

## The Verification Protocol

### Step 1: Extract All Citations

Before using any LLM output containing citations:

1. List every citation, reference, or paper mentioned
2. Include implicit citations ("Smith and colleagues found...")
3. Include vague references ("studies show," "research indicates")

### Step 2: Verify Existence

For each citation:

1. **Search exact title** in Google Scholar, PubMed, or relevant database
2. **Search author combinations** if title doesn't match
3. **Check DOI** if provided (doi.org/[DOI] should resolve)
4. **Mark status**:
   - ✓ Verified: Paper exists exactly as cited
   - ⚠ Partially correct: Paper exists but details wrong (year, journal, authors)
   - ✗ Fabricated: Paper does not exist

### Step 3: Verify Content

For citations that exist:

1. **Retrieve the actual paper**
2. **Compare claims**: Does the paper say what the LLM claims it says?
3. **Check for distortion**: Is the finding accurately represented, or is it oversimplified, overstated, or taken out of context?

### Step 4: Document Verification

Keep a log:

```
| Citation | Existence | Content Verified | Notes |
|----------|-----------|------------------|-------|
| Smith et al. 2020, Nature | ✓ | ✓ | Correct |
| Jones 2019, Science | ✗ | N/A | Fabricated—no such paper exists |
| Lee et al. 2021, Cell | ⚠ | ✓ | Year wrong (2022), content accurate |
```

## What To Do With Fabricated Citations

1. **Remove them entirely** from your work
2. **Do not try to find a "similar" paper** to substitute—this introduces confirmation bias
3. **If the claim matters**, search the literature independently to find actual support
4. **If you cannot find support**, the claim may be unsupported or false—do not include it

## Prompts That Reduce (But Do Not Eliminate) Risk

When using LLMs for literature-related tasks, include constraints like:

```
Do not provide citations or references. I will add citations myself.
```

```
Base your response ONLY on the papers I have provided. Do not introduce information from other sources.
```

```
If you are unsure about a fact, say so explicitly rather than providing a citation.
```

These reduce risk but do not eliminate it. The model may still:
- Introduce implicit citations ("research has shown...")
- Reference papers not in your provided set
- Misremember details from its training data

**Verification remains mandatory.**

## Red Flags That Suggest Fabrication

Be especially skeptical when:

- Citation is unusually specific (exact page numbers, precise statistics)
- Citation perfectly supports the point being made
- Author names are common in the field but the specific combination seems unlikely
- The journal seems appropriate but you haven't heard of the specific paper
- DOI format looks correct but you haven't checked it
- Citation is for a very recent paper (closer to knowledge cutoff)

## A Note on LLM Self-Reports

Do not ask an LLM if its citations are real. The model will typically:

- Confidently assert the citations are accurate (even when fabricated)
- Offer to "double-check" by generating the same fabricated citations again
- Express uncertainty performatively but still provide fabricated sources

**External verification is the only reliable method.**

## Example Fabricated Citation (Illustrative)

If you asked an LLM about microbiome and depression, it might generate:

> "Thompson, R.J., & Martinez, K.L. (2021). Gut microbiota composition predicts treatment response in major depressive disorder: A prospective cohort study. *Nature Neuroscience*, 24(3), 412-425."

This citation has:
- Plausible author names
- Realistic journal for the topic
- Appropriate year
- Specific page numbers
- A title that perfectly matches the query

**This paper does not exist.** Searching for it would reveal no results.

## For Literature Synthesis Workflows

When using prompts from this repository for literature work:

1. **paper-summary.md**: Verify citation format and check spot-claims against original
2. **synthesis-across-papers.md**: Verify every paper attribution; confirm no papers were introduced beyond your provided set
3. **gap-identification.md**: Verify that "Author X said Y is needed" claims actually appear in the papers

## Integration With Verification Checklist

For any publishable work involving LLM-generated text:

1. Run the citation verification protocol above
2. Complete the verification checklist from `guides/verification-checklist-extended.md`
3. Document both in your research notes

## Summary

| Risk Level | Scenario | Required Action |
|------------|----------|-----------------|
| **Critical** | LLM asked to provide citations | Verify 100% of citations |
| **High** | LLM summarizes papers not provided in full | Verify claims against originals |
| **Moderate** | LLM works only with provided paper text | Spot-check accuracy of representation |
| **Lower** (not zero) | LLM explicitly instructed not to cite | Check for implicit citations; verify any that appear |

**The bottom line**: Treat every citation from an LLM as fabricated until you have personally verified it against a reliable source.

## Model Notes

```
This file is a workflow document, not a prompt to be used with an LLM.
```

## Cross-References

- For summarizing papers safely, see `literature/paper-summary.md`
- For synthesis with citation controls, see `literature/synthesis-across-papers.md`
- For comprehensive output verification, see `guides/verification-checklist-extended.md`
