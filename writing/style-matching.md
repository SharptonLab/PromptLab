# Style Matching Prompt

## Task Description

Revise text to match the style, tone, and conventions of a reference sample, ensuring consistency when incorporating LLM-assisted drafts into your existing writing.

## When to Use

- Integrating LLM-generated drafts into a manuscript with established voice
- Ensuring new sections match the style of previously written sections
- Adapting writing for a different audience or venue (e.g., journal to grant)
- Revising a collaborator's contribution to match your writing style

## When NOT to Use

- When the reference sample isn't representative of the target style
- To mask that content was generated differently (document LLM use appropriately)
- When substantive revision is needed, not just stylistic (address content first)
- For very short texts where style matching adds more effort than value

## The Prompt

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
```

## Prompt Components Explained

| Component | Purpose |
|-----------|---------|
| **Context** | Purpose affects appropriate style (manuscript vs. grant vs. lay audience) |
| **Reference sample** | Provides the style model—quality of matching depends on quality of sample |
| **Text to revise** | The content to be restyled |
| **Specific dimensions** | Breaks down "style" into concrete, matchable features |
| **Constraints** | Ensures content integrity isn't sacrificed for style |

## Example Output

For a representative model response to the Test Input, see:

`tests/writing/style-matching/claude-sonnet-4-6-2026-06-25.md`

That cell was captured on 2026-06-25 and human-verified by both project reviewers as passing. Other panel models' responses (Claude Opus 4.7, GPT-5.5, Gemini 2.5 Pro, Nemotron 3 Super 120B, Step-3.7 Flash) are alongside it in the same directory.

## Test Input

Use the following materials to test this prompt:

```
Context: I am finalizing a manuscript on microbiome-immune interactions. I need to revise text to match my established writing style.

Reference sample (my existing writing):
"The intestinal immune system faces a unique challenge: it must tolerate the dense commensal microbiota while remaining vigilant against pathogens. This balance depends on continuous crosstalk between epithelial cells, innate immune populations, and the microbiome itself. Disruption of this crosstalk—whether through antibiotic exposure, dietary changes, or genetic susceptibility—can trigger inappropriate immune responses that damage host tissue.

We investigated how specific bacterial metabolites influence regulatory T cell development in the gut. Our approach combined gnotobiotic mouse models with targeted metabolomics to establish causal relationships between microbial products and immune phenotypes. This experimental strategy allowed us to move beyond correlation to identify specific molecular mediators of host-microbe communication."

Text to revise:
"In the present investigation, we sought to elucidate the mechanistic underpinnings of how the gut microbiome modulates host immune responses. Utilizing state-of-the-art methodological approaches including flow cytometric analysis and single-cell RNA sequencing technologies, we comprehensively characterized the immunological landscape of the intestinal mucosa. Our findings demonstrate that microbial colonization status significantly impacts the development and functional capacity of tissue-resident immune cell populations, with particularly notable effects observed in the regulatory T cell compartment."

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
```

**Expected output should include:**
- Shortened sentences (reference averages ~20 words; text to revise averages ~30)
- Reduced passive voice and formal constructions
- Removal of verbose phrases ("In the present investigation" → "We"; "sought to elucidate" → simpler)
- Maintained technical accuracy
- [CONTENT NOTE] if any substantive issues identified
- Summary of key stylistic changes made

**Verification points:**
- All technical content preserved (flow cytometry, scRNA-seq, Tregs mentioned)
- No new information added
- Style noticeably closer to reference sample
- Important qualifications ("significantly") preserved

## Failure Modes

- **Meaning drift**: May subtly alter meaning while changing style, especially with hedging language
- **Over-matching quirks**: May match idiosyncratic features of the sample that aren't representative
- **Losing precision**: May simplify technical language to the point of imprecision
- **Inconsistent matching**: May match some features well but miss others
- **Adding content**: May add transitions or context not in the original
- **Removing qualifications**: May drop important hedges or caveats while "tightening" prose
- **Sample misinterpretation**: May misread the reference style if the sample is too short or atypical

## Verification Requirements

1. **Check meaning preservation**: Compare original and revised versions—ensure no substantive changes
2. **Verify qualifications kept**: Ensure important hedges ("may," "suggests") weren't removed inappropriately
3. **Check technical accuracy**: Verify technical terms are still used correctly
4. **Confirm nothing added**: Ensure no new claims or context were introduced
5. **Verify style match**: Read revised text alongside your reference—does it actually sound like you?
6. **Read aloud**: Often reveals mismatches that visual reading misses

## Variations

### Matching a collaborator's style
When you need to match a co-author's style:
```
Reference sample: [paste collaborator's writing]
Task: Revise my text to better match my co-author's style for consistency across sections they are editing.
Note: This is for internal consistency, not to obscure authorship.
```

### Audience adaptation
For changing audience rather than matching an author:
```
Reference sample: [paste example of writing for target audience]
Task: Adapt this technical text for [TARGET AUDIENCE: e.g., "a general scientific audience," "grant reviewers outside my field," "a lay summary"].
Note: You may need to adjust technical depth, not just style.
```

### Identifying style features
Before style matching, to understand your own style:
```
Task: Analyze this sample of my writing and describe its characteristic features: sentence length and structure, voice, tone, hedging patterns, technical language level, and transition style. I will use this description to guide future revisions.
```

### Batch matching
For multiple sections:
```
Reference sample: [your writing]
Texts to revise:
[Section 1]
---
[Section 2]
---
[Section 3]

Task: Revise each section to match the reference style. Maintain consistent style across all sections.
```

## Model Notes

```
Tested across the panel; verdicts set by human review.

- Claude Opus 4 (claude-opus-4-5-20251101) (2026-02-04): Pass
- claude-opus-4.7 (2026-06-25): Pass
- claude-sonnet-4.6 (2026-06-25): Pass
- gemini-2.5-pro (2026-06-25): Pass
- gpt-5.5 (2026-06-25): Pass
- nemotron-3-super-120b (2026-06-25): Pass
- step-3.7-flash (2026-06-25): Pass

Full per-model raw outputs and reviewer notes: tests/writing/style-matching/
```

## Cross-References

- For drafting methods sections to revise later, see `writing/methods-drafting.md`
- For drafting results to revise later, see `writing/results-description.md`
- For ensuring your writing matches journal conventions, consider also reviewing target journal guidelines directly
