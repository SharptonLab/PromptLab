# Reviewer Response Drafting Prompt

## Task Description

Generate structured, professional responses to peer reviewer comments, organizing your replies and helping articulate how you have (or will) address each concern.

## When to Use

- Drafting initial responses to organize your thinking before refinement
- Ensuring you've addressed every reviewer point systematically
- Articulating technical responses when you know the answer but struggle to phrase it diplomatically
- Structuring responses to complex or multi-part reviewer comments

## When NOT to Use

- When you don't actually have a response (the LLM cannot answer scientific questions for you)
- To generate dismissive or defensive responses
- For fabricating additional experiments or analyses you haven't done
- When reviewer comments require substantive intellectual work you haven't completed

## The Prompt

```
Context: I am preparing a response to reviewers for a manuscript on {RESEARCH_TOPIC}. I need to draft responses to reviewer comments. My goal is to be professional, thorough, and collegial while firmly defending valid aspects of the work.

Reviewer comment:
{PASTE_REVIEWER_COMMENT}

My planned response/action:
{YOUR_NOTES: what you've done or plan to do in response}

Task: Draft a response to this reviewer comment. Follow these guidelines:

1. **Acknowledge the point**: Start by thanking the reviewer for the observation or showing you understood their concern.

2. **Summarize the issue**: Briefly restate what the reviewer raised (shows you understood).

3. **Provide your response**: Explain what you did in response, with specifics:
   - If you made changes: describe what was changed and where
   - If you did additional analysis: summarize the approach and findings
   - If you respectfully disagree: explain your reasoning clearly

4. **Quote new text if applicable**: If the manuscript was revised, show the new/revised text.

5. **Be specific about locations**: Reference page numbers, line numbers, figure numbers, or section names.

Constraints:
- Maintain a professional, collegial tone throughout
- Do not be defensive or dismissive—even if the comment seems unfair
- Do not fabricate experiments, analyses, or results you haven't done
- If you disagree with the reviewer, provide scientific reasoning, not assertions
- Do not over-promise changes you won't make

Output format: Response suitable for inclusion in a point-by-point response document.
```

## Prompt Components Explained

| Component | Purpose |
|-----------|---------|
| **Context** | Manuscript topic helps tailor technical language |
| **Reviewer comment** | The exact text you're responding to |
| **Your planned response** | Critical input—the LLM structures your response, not invents it |
| **Guidelines** | Produce responses following effective rebuttal conventions |
| **Constraints** | Prevent defensiveness, fabrication, and empty promises |

## Example Input

```
Context: I am preparing a response to reviewers for a manuscript on gut microbiome changes during antibiotic treatment in mice.

Reviewer comment:
"The authors use Shannon diversity as their sole measure of alpha diversity. However, Shannon diversity is sensitive to both richness and evenness, and it would strengthen the paper to also report observed ASVs or Chao1 richness estimates. Without these additional metrics, it is difficult to know whether the antibiotic treatment reduced the number of taxa or simply altered their relative abundances."

My planned response/action:
- Good point, we should have included this
- Re-ran analysis with Observed ASVs and Chao1
- Results show: Observed ASVs dropped from ~150 to ~45 with antibiotics; Chao1 showed similar pattern
- This confirms it's a richness reduction, not just evenness change
- Added new supplementary figure (Fig S3) and updated Results text
- Added sentence to Methods about multiple diversity metrics
```

## Example Output

We thank the reviewer for this suggestion to strengthen our diversity analyses. The reviewer correctly notes that Shannon diversity conflates richness and evenness components, making it difficult to determine the nature of community changes.

We have now expanded our alpha diversity analysis to include Observed ASVs (a direct richness measure) and Chao1 richness estimates. These additional metrics confirm that antibiotic treatment substantially reduced taxonomic richness: Observed ASVs decreased from 152 ± 18 (mean ± SD) at baseline to 45 ± 12 following treatment, and Chao1 estimates showed a parallel decline (167 ± 22 to 52 ± 15). These reductions are consistent with the Shannon diversity patterns and indicate that the antibiotic-driven diversity loss reflects genuine loss of taxa rather than solely altered relative abundances.

We have made the following changes to the manuscript:

**Methods (lines 145-147):** "Alpha diversity was assessed using the Shannon diversity index, Observed ASVs, and Chao1 richness estimator to distinguish effects on evenness versus richness."

**Results (lines 198-202):** "Consistent with Shannon diversity reductions, antibiotic treatment markedly reduced taxonomic richness. Observed ASVs declined from 152 ± 18 to 45 ± 12 (Supplementary Figure 3A), and Chao1 estimates showed parallel reductions (Supplementary Figure 3B), indicating that diversity loss reflected reduced species number rather than altered evenness alone."

**Supplementary Figure 3:** New figure showing Observed ASVs and Chao1 estimates across treatment groups and timepoints.

## Test Input

Use the following scenario to test this prompt:

```
Context: I am preparing a response to reviewers for a manuscript on microbiome-metabolome interactions in inflammatory bowel disease.

Reviewer comment:
"The authors correlate microbiome composition with metabolite profiles and identify several significant associations. However, the analysis appears to suffer from multiple testing issues. With hundreds of taxa and dozens of metabolites, the number of comparisons is very large. The authors mention using FDR correction, but do not report how many tests were performed or what the effective correction threshold was. Additionally, some of the highlighted correlations have r-values below 0.3, which may not be biologically meaningful even if statistically significant. The authors should address the multiple testing concern more rigorously and discuss the biological relevance of weak correlations."

My planned response/action:
- Reviewer raises valid concern about multiple testing transparency
- We did use Benjamini-Hochberg FDR correction at q<0.05
- Total tests: 847 (77 taxa × 11 metabolites)
- Will add this information to Methods
- For weak correlations (r<0.3): we agree these should be interpreted cautiously
- Added new sentence to Discussion acknowledging this limitation
- However, some weak correlations are still biologically interesting as part of networks
- Did not remove any results but added appropriate caveats
```

**Expected output should include:**
- Acknowledgment of the valid concern about transparency
- Specific numbers: 847 tests, 77 taxa, 11 metabolites, q<0.05 threshold
- Reference to specific manuscript locations for changes
- Balanced response on weak correlations (acknowledge limitation but justify inclusion)
- Professional, collegial tone throughout

**Verification points:**
- All numbers match planned response exactly
- Tone is professional, not defensive
- Response addresses both parts of reviewer concern (multiple testing AND weak correlations)
- No fabricated analyses or claims beyond what's in planned response

## Failure Modes

- **Fabricating results**: May invent statistics or experimental outcomes you didn't provide
- **Over-promising**: May commit to changes beyond what you've actually planned
- **False agreement**: May agree with reviewer points that aren't actually valid
- **Defensive tone**: May become argumentative despite instructions (especially if your notes are defensive)
- **Missing specifics**: May produce vague responses that don't actually address the concern
- **Inconsistent voice**: May not match the professional tone of the rest of your response document

## Verification Requirements

1. **Verify all numbers**: Confirm any statistics in the response match your actual new analyses
2. **Check manuscript references**: Verify page/line numbers are accurate for the revised manuscript
3. **Verify promises**: Ensure every "we have done X" statement is actually true
4. **Check tone**: Read for any phrases that might come across as defensive or dismissive
5. **Verify technical accuracy**: Ensure the response correctly characterizes your methods and results
6. **Consistency check**: Ensure the response doesn't contradict other parts of your rebuttal

## Variations

### Disagreeing with reviewer
When you believe the reviewer is incorrect:
```
My planned response: I respectfully disagree because [REASONING]. I don't plan to make this change because [JUSTIFICATION].

Additional instruction: Frame the disagreement as a scientific discussion, not a challenge to the reviewer's competence. Acknowledge any valid underlying concern even if you disagree with the proposed solution.
```

### Partial agreement
When you'll address part of a concern:
```
My planned response: I agree with [PART A] and have addressed it by [ACTION]. However, I believe [PART B] is already adequately addressed because [REASONING], so I have not made additional changes to that aspect.
```

### Complex multi-part comments
For reviewer comments with multiple points:
```
Structure the response with numbered sub-responses matching each distinct point in the reviewer's comment. Use format:
(a) Regarding [first point]: ...
(b) Regarding [second point]: ...
```

### Major revision required
When significant new work was done:
```
Additional context: This addresses a major concern. We conducted [NEW EXPERIMENT/ANALYSIS]. Results are summarized here, with full details in [LOCATION].
```

## Model Notes

```
Models tested: [To be completed]
Date tested: [To be completed]
Notes: [To be completed]
```

## Cross-References

- For describing new results added in revision, see `writing/results-description.md`
- For matching the style of previous responses, see `writing/style-matching.md`
- For checking your response for weaknesses, see `validation/adversarial-critique.md`
