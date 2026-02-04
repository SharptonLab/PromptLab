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

## Example Input

```
Context: I am finalizing a manuscript on gut microbiome methods. I need to revise text to match my established writing style.

Reference sample (my existing writing):
"The gut microbiome varies substantially between individuals, and this variation complicates efforts to identify disease-associated microbial signatures. We addressed this challenge by collecting samples longitudinally from each participant, allowing us to distinguish within-individual fluctuations from between-individual differences. Samples were collected weekly for twelve weeks, yielding 480 samples from 40 participants. This design provides statistical power to detect temporal patterns while accounting for the baseline heterogeneity that confounds cross-sectional studies.

We processed samples using established protocols with modifications for high-throughput analysis. DNA was extracted within 24 hours of collection to minimize degradation artifacts. Library preparation followed the Earth Microbiome Project protocol, which we selected for compatibility with existing datasets. Sequencing was performed on a NovaSeq 6000, generating approximately 50,000 reads per sample after quality filtering."

Text to revise:
"In this study, we utilized 16S rRNA gene sequencing methodologies to characterize the microbial communities present in fecal samples. The amplification of the V4 hypervariable region was accomplished through the employment of previously validated primer sequences. Subsequent to amplification, library construction was performed and samples were subjected to sequencing on an Illumina platform. The bioinformatic pipeline that was employed for data processing included quality filtering, chimera removal, and taxonomic classification utilizing the SILVA database."
```

## Example Output

**Revised text:**

We characterized microbial communities in fecal samples using 16S rRNA gene sequencing. We amplified the V4 region with validated primers and prepared libraries for Illumina sequencing. Our bioinformatic pipeline included quality filtering, chimera removal, and taxonomic classification against the SILVA database.

**Key stylistic changes:**

1. **Sentence structure**: Shortened sentences to match the direct, declarative style of the reference (~15-20 words vs. original ~25-30)
2. **Voice**: Changed passive constructions ("was accomplished," "was employed") to active voice ("We amplified," "We characterized")
3. **Word choice**: Replaced formal/verbose phrases with simpler alternatives ("utilized" → used/implicit; "subsequent to" → removed; "subjected to sequencing" → "sequencing")
4. **Hedging**: Removed unnecessary hedging ("methodologies" → "sequencing"; "that was employed" → eliminated)
5. **Technical language**: Maintained technical precision while reducing wordiness, matching reference style

[CONTENT NOTE: The original text lacks specific details present in the reference sample—e.g., no mention of sequencing platform model, read counts, or processing timeline. Consider adding these details if available.]

## Test Input

Use the following materials to test this prompt:

```
Context: I am finalizing a manuscript on microbiome-immune interactions. I need to revise text to match my established writing style.

Reference sample (my existing writing):
"The intestinal immune system faces a unique challenge: it must tolerate the dense commensal microbiota while remaining vigilant against pathogens. This balance depends on continuous crosstalk between epithelial cells, innate immune populations, and the microbiome itself. Disruption of this crosstalk—whether through antibiotic exposure, dietary changes, or genetic susceptibility—can trigger inappropriate immune responses that damage host tissue.

We investigated how specific bacterial metabolites influence regulatory T cell development in the gut. Our approach combined gnotobiotic mouse models with targeted metabolomics to establish causal relationships between microbial products and immune phenotypes. This experimental strategy allowed us to move beyond correlation to identify specific molecular mediators of host-microbe communication."

Text to revise:
"In the present investigation, we sought to elucidate the mechanistic underpinnings of how the gut microbiome modulates host immune responses. Utilizing state-of-the-art methodological approaches including flow cytometric analysis and single-cell RNA sequencing technologies, we comprehensively characterized the immunological landscape of the intestinal mucosa. Our findings demonstrate that microbial colonization status significantly impacts the development and functional capacity of tissue-resident immune cell populations, with particularly notable effects observed in the regulatory T cell compartment."
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
Models tested: [To be completed]
Date tested: [To be completed]
Notes: [To be completed]
```

## Cross-References

- For drafting methods sections to revise later, see `writing/methods-drafting.md`
- For drafting results to revise later, see `writing/results-description.md`
- For ensuring your writing matches journal conventions, consider also reviewing target journal guidelines directly
