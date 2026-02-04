# Case Study: Manuscript Revision Workflow

## Overview

This case study demonstrates using LLM assistance for manuscript revision, specifically responding to peer reviewer comments. The example follows a researcher revising a microbiome methods paper after receiving a "major revisions" decision.

**Situation:** The manuscript has been reviewed and requires revisions before acceptance. Three reviewers provided comments, ranging from minor clarifications to requests for additional analyses.

**Prompts used in this workflow:**
- `writing/reviewer-response.md`
- `code/r-script-generation.md`
- `validation/adversarial-critique.md`
- `writing/style-matching.md`

---

## The Reviews Received

**Editor Decision:** Major Revisions

**Reviewer 1:** Generally positive; requests clarification on methods and one additional analysis.

**Reviewer 2:** Skeptical of one conclusion; requests additional statistical justification and discussion of limitations.

**Reviewer 3:** Minor comments on presentation and references.

---

## Step 1: Organize and Prioritize Comments

### Initial Triage

The researcher first organizes all comments by type and priority.

**Prompt:**

```
Help me organize these peer reviewer comments into categories and prioritize them.

Reviewer 1:
1. "The rarefaction depth of 10,000 reads should be justified. Why this threshold?"
2. "Please provide alpha diversity results for Shannon and Simpson in addition to observed richness."
3. "Line 156: clarify what 'normalized' means in this context."
4. "The discussion of study limitations is brief. Please expand."

Reviewer 2:
1. "The claim that Treatment A significantly alters community composition (line 203) is not adequately supported. The PERMANOVA R² is only 0.08. Please discuss the biological significance of this small effect size."
2. "Figure 2 should include individual data points, not just box plots."
3. "Why was Bray-Curtis distance used rather than UniFrac? Please justify."
4. "The authors should acknowledge that their sample size (n=15 per group) limits statistical power."

Reviewer 3:
1. "Reference 23 appears to be formatted incorrectly."
2. "Figure 1 legend is missing units for the y-axis."
3. "The abstract exceeds the journal word limit (currently 280 words, limit is 250)."

Categorize as:
- Quick fixes (can address immediately)
- New analyses needed
- Writing/argumentation changes
- Potential pushback (where I might respectfully disagree)

Then suggest an order for tackling them.
```

**LLM Output:**

> **Quick Fixes:**
> - R3.1: Fix reference 23 formatting
> - R3.2: Add units to Figure 1 legend
> - R3.3: Trim abstract to 250 words
> - R1.3: Clarify "normalized" (line 156)
>
> **New Analyses Needed:**
> - R1.2: Calculate Shannon and Simpson diversity (in addition to observed)
> - R2.2: Remake Figure 2 with individual data points
>
> **Writing/Argumentation Changes:**
> - R1.1: Justify rarefaction depth
> - R1.4: Expand limitations section
> - R2.1: Discuss biological significance of R²=0.08 (most substantive)
> - R2.3: Justify Bray-Curtis over UniFrac
> - R2.4: Acknowledge sample size limitation
>
> **Potential Pushback:**
> - R2.1: You could argue that R²=0.08 is actually meaningful in microbiome studies where high individual variation is expected, but you'll need to support this with citations.
>
> **Suggested Order:**
> 1. Quick fixes (get them done)
> 2. New analyses (R1.2, R2.2)—need results before writing response
> 3. Argumentation changes (tackle R2.1 most carefully)
> 4. Draft response letter

---

## Step 2: Perform New Analyses

The researcher needs to add Shannon and Simpson diversity. They use code generation assistance.

**Prompt used:** Adapted from `code/r-script-generation.md`

```
I already have observed richness calculated. Add Shannon and Simpson diversity to my existing results and run the same statistical tests.

Current code calculates observed richness and runs Wilcoxon tests between Treatment A and Control.

Add to this:
1. Shannon diversity
2. Simpson diversity
3. Same Wilcoxon tests for each new metric
4. Update my results table to include all three metrics

Use vegan package. Keep format consistent with existing code.
```

**LLM Output:**

```r
# Add to existing analysis
library(vegan)

# Calculate additional diversity metrics
shannon <- diversity(otu_table, index = "shannon")
simpson <- diversity(otu_table, index = "simpson")

# Add to results dataframe
diversity_results$shannon <- shannon
diversity_results$simpson <- simpson

# Statistical tests
shannon_test <- wilcox.test(shannon ~ treatment, data = diversity_results)
simpson_test <- wilcox.test(simpson ~ treatment, data = diversity_results)

# Results summary table
diversity_summary <- diversity_results %>%
  group_by(treatment) %>%
  summarise(
    observed_mean = mean(observed),
    observed_sd = sd(observed),
    shannon_mean = mean(shannon),
    shannon_sd = sd(shannon),
    simpson_mean = mean(simpson),
    simpson_sd = sd(simpson)
  )

cat("Shannon: W =", shannon_test$statistic, ", p =", shannon_test$p.value, "\n")
cat("Simpson: W =", simpson_test$statistic, ", p =", simpson_test$p.value, "\n")
```

**Results obtained:**
- Shannon: Treatment A mean = 3.42 (SD 0.31), Control mean = 3.67 (SD 0.28), p = 0.042
- Simpson: Treatment A mean = 0.91 (SD 0.03), Control mean = 0.94 (SD 0.02), p = 0.038

**Verification:**
- [x] Code runs correctly
- [x] Results consistent with observed richness pattern
- [x] Added to supplementary table

---

## Step 3: Draft Response Letter

With analyses complete, the researcher drafts the response.

**Prompt used:** Adapted from `writing/reviewer-response.md`

```
Help me draft a response to this reviewer comment. I need to:
1. Acknowledge the valid concern
2. Explain what I did to address it
3. Point to specific changes in the manuscript

Reviewer Comment (R2.1):
"The claim that Treatment A significantly alters community composition (line 203) is not adequately supported. The PERMANOVA R² is only 0.08. Please discuss the biological significance of this small effect size."

My approach:
- I'm keeping the claim but adding context about effect sizes in microbiome studies
- I found citations showing R² values of 0.05-0.15 are typical for treatment effects in gut microbiome studies
- I'm adding a paragraph to Discussion acknowledging this and discussing what 8% explained variance means biologically

Draft a response that is:
- Respectful and non-defensive
- Specific about changes made
- Confident but not dismissive of the concern
```

**LLM Output:**

> **Response to Reviewer 2, Comment 1:**
>
> We thank the reviewer for this important point about effect size interpretation. We agree that statistical significance alone is insufficient and that biological significance must be addressed.
>
> We have revised the manuscript to contextualize our PERMANOVA results. As noted by [citations], treatment effects in gut microbiome studies typically explain 5-15% of community variance, with the majority of variance attributable to inter-individual differences. Our R² of 0.08 falls within this expected range and indicates that treatment explains a meaningful, though modest, portion of community variation above the substantial background of individual-to-individual differences.
>
> We have added a paragraph to the Discussion (lines 287-295, highlighted in revised manuscript) acknowledging that while statistically significant, the effect size indicates Treatment A produces a detectable but not dominant shift in community structure. We discuss what this means for biological interpretation and have tempered our language accordingly, replacing "significantly alters" with "detectably shifts" in the relevant passage.
>
> We believe this revision addresses the reviewer's concern while maintaining the validity of our finding.

---

## Step 4: Handle All Comments Systematically

The researcher continues drafting responses for each comment. Here's the approach for a straightforward comment:

**Comment R1.1:** "The rarefaction depth of 10,000 reads should be justified. Why this threshold?"

**Prompt:**

```
Draft a brief response explaining our rarefaction depth choice.

Facts:
- We chose 10,000 reads based on rarefaction curves showing saturation
- This retained 95% of samples (excluded 3 samples below threshold)
- This is consistent with published studies in this system

Keep response to 3-4 sentences.
```

**LLM Output:**

> **Response to Reviewer 1, Comment 1:**
>
> Rarefaction depth was selected based on rarefaction curve analysis, which indicated that richness estimates plateau by 10,000 reads for samples in this study (Supplementary Figure S1). This threshold retained 95% of samples (47 of 50) while ensuring robust diversity estimates. This depth is consistent with similar studies in murine gut microbiomes [citations]. We have added this justification to the Methods section (lines 134-136).

---

## Step 5: Adversarial Check on Key Response

The most contentious response (R2.1 on effect size) gets an adversarial review.

**Prompt used:** Adapted from `validation/adversarial-critique.md`

```
I'm about to send this response to a skeptical reviewer who questioned our effect size. Play devil's advocate—how might they push back on this response?

[Paste R2.1 response]

What holes might they find? What follow-up questions might they ask?
```

**LLM Output:**

> **Potential Reviewer Pushback:**
>
> 1. "The citations for 5-15% R² being 'typical'—are these from comparable studies (same treatment type, same mouse strain, same body site)? A skeptic would want to see truly comparable studies, not just any microbiome work."
>
> 2. "You say the effect is 'meaningful'—but what does 8% explained variance actually mean for the biology? Can you be more concrete? Does this translate to observable phenotypic differences?"
>
> 3. "You changed 'significantly alters' to 'detectably shifts'—but you still conclude this matters. The reviewer might want you to more explicitly state the limitations or say it's a modest effect."
>
> 4. "If treatment explains only 8%, what explains the other 92%? The reviewer might want you to at least acknowledge what else is driving community variation."
>
> **Suggested Additions:**
> - Add one sentence noting what might explain remaining variance (diet, cage effects, individual genetics)
> - Be more concrete about biological interpretation—does the 8% shift correlate with any measured outcomes?
> - Ensure citations are for comparable study designs

**Revisions made:**
- Added sentence: "The remaining variance is likely attributable to inter-individual differences, cage effects, and stochastic assembly processes common in gut microbiome studies."
- Added reference to correlation with inflammatory markers (Table 2) to anchor biological relevance
- Verified citations are from murine gut studies with similar designs

---

## Step 6: Compile Final Response Letter

**Structure of response letter:**

```markdown
Dear Editor,

Thank you for the opportunity to revise our manuscript [MS#]. We appreciate the constructive feedback from all three reviewers. Below, we provide point-by-point responses to each comment. Changes in the manuscript are highlighted in yellow.

---

## Reviewer 1

**Comment 1.1:** [Quote]
**Response:** [Response text]

**Comment 1.2:** [Quote]
**Response:** [Response text]

[Continue for all comments]

---

## Reviewer 2

[...]

---

## Reviewer 3

[...]

---

We believe these revisions address all reviewer concerns. We thank the reviewers for their thoughtful comments, which have strengthened the manuscript.

Sincerely,
[Author]
```

---

## Step 7: Final Verification

Before submission, the researcher verifies all changes are complete.

**Checklist:**

| Comment | Response Drafted | Manuscript Changed | Change Highlighted | Verified |
|---------|-----------------|-------------------|-------------------|----------|
| R1.1 | ✓ | ✓ (lines 134-136) | ✓ | ✓ |
| R1.2 | ✓ | ✓ (Table 1, Supp) | ✓ | ✓ |
| R1.3 | ✓ | ✓ (line 156) | ✓ | ✓ |
| R1.4 | ✓ | ✓ (lines 312-325) | ✓ | ✓ |
| R2.1 | ✓ | ✓ (lines 203, 287-295) | ✓ | ✓ |
| R2.2 | ✓ | ✓ (Figure 2) | N/A (figure) | ✓ |
| R2.3 | ✓ | ✓ (lines 140-142) | ✓ | ✓ |
| R2.4 | ✓ | ✓ (lines 318-320) | ✓ | ✓ |
| R3.1 | ✓ | ✓ (Ref 23) | N/A | ✓ |
| R3.2 | ✓ | ✓ (Fig 1 legend) | N/A | ✓ |
| R3.3 | ✓ | ✓ (Abstract) | N/A | ✓ |

**Additional checks:**
- [x] Line numbers in response match revised manuscript
- [x] All highlighted changes are actually present
- [x] New analyses are in supplementary materials
- [x] Word count within limits
- [x] Figures updated and formatted correctly

---

## Key Lessons from This Workflow

1. **Organize before responding:** Categorizing comments by type and priority prevents getting overwhelmed and ensures nothing is missed.

2. **Do analyses before writing:** Complete any new analyses first so you can reference actual results in your response.

3. **Adversarial review for contentious points:** The most critical reviewer comments deserve extra scrutiny before you submit your response.

4. **Track everything:** A systematic checklist ensures every comment is addressed and every manuscript change is made.

5. **Tone matters:** Responses should be confident but respectful—never defensive or dismissive.

---

## Prompts Used (Quick Reference)

| Step | Prompt File | Purpose |
|------|-------------|---------|
| 1 | Custom | Organize and prioritize comments |
| 2 | `code/r-script-generation.md` | Generate new analysis code |
| 3-4 | `writing/reviewer-response.md` | Draft individual responses |
| 5 | `validation/adversarial-critique.md` | Check contentious response |
| 7 | Custom | Final verification |
