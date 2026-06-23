# Gap Identification Prompt

## Task Description

Identify research gaps, open questions, and opportunities for future investigation based on a set of papers you have read, structured to inform research planning or grant development.

## When to Use

- Developing specific aims for a grant proposal
- Identifying dissertation or thesis research directions
- Finding angles for a new manuscript or review article
- Scoping a new research area to identify tractable questions
- Justifying the significance of proposed work

## When NOT to Use

- When you haven't read the source papers (gaps identified may not reflect actual literature)
- To identify gaps in fields where you lack expertise to evaluate feasibility
- As the sole basis for research direction (gaps require human judgment about importance and tractability)
- When you need comprehensive gap analysis (this generates hypotheses to investigate, not definitive gap mapping)

## The Prompt

```
Context: I am a {RESEARCHER_ROLE} working on {RESEARCH_AREA}. I am trying to identify research gaps and opportunities based on the following papers I have read.

Papers provided:
{PAPER_1_TEXT}
---
{PAPER_2_TEXT}
---
{PAPER_3_TEXT}
[Add more as needed]

My research capabilities: {BRIEF_DESCRIPTION: e.g., "mouse microbiome studies, 16S and metagenomic sequencing, gnotobiotic facilities"}

Task: Analyze these papers to identify research gaps and opportunities. Structure your analysis as follows:

1. **Explicit Gaps**: Questions or limitations the authors themselves identify as needing future work. Quote or paraphrase directly from the papers.

2. **Implicit Gaps**: Questions that arise from the work but are not explicitly flagged by authors:
   - Untested assumptions
   - Missing controls or comparisons
   - Unexplored mechanisms
   - Populations or systems not studied
   - Methodological limitations that could be addressed

3. **Contradictions Requiring Resolution**: Conflicting findings across papers that represent opportunities to resolve through new experiments.

4. **Methodological Opportunities**: New techniques, larger samples, or improved designs that could advance understanding.

5. **Translation Gaps**: For basic research—what would be needed to move toward application? For applied research—what mechanistic understanding is missing?

6. **Prioritized Opportunities**: Based on my stated research capabilities, which 2-3 gaps are most tractable and impactful for me to address?

Constraints:
- Base your analysis ONLY on the papers provided—do not introduce gaps from your general knowledge
- For each gap, cite which paper(s) suggest it
- Distinguish between "authors say this is needed" and "I infer this is needed"
- Do not overstate the significance of gaps—some are minor or already being addressed
- If a gap seems important but may already be addressed in literature not provided, note this uncertainty

Output format: Use the numbered structure above. Use bullet points within each section with specific paper attributions.
```

## Prompt Components Explained

| Component | Purpose |
|-----------|---------|
| **Researcher role and area** | Focuses gap identification on relevant directions |
| **Research capabilities** | Enables practical prioritization based on what you can actually do |
| **Explicit vs. implicit gaps** | Distinguishes gaps authors acknowledge from those requiring inference |
| **Constraints** | "ONLY on papers provided" prevents fabricating gaps from training data; uncertainty notes prevent overconfidence |
| **Prioritization request** | Produces actionable output tailored to your situation |

## Example Input

```
Context: I am a microbiome researcher working on host-microbiome interactions in inflammatory bowel disease. I am trying to identify research gaps and opportunities based on the following papers I have read.

Papers provided:
[Full text of Paper 1: Lloyd-Price et al. (2019). Multi-omics of the gut microbial ecosystem in inflammatory bowel diseases. Nature.]
---
[Full text of Paper 2: Schirmer et al. (2019). Compositional and temporal changes in the gut microbiome of pediatric ulcerative colitis patients. Cell Host & Microbe.]
---
[Full text of Paper 3: Franzosa et al. (2019). Gut microbiome structure and metabolic activity in inflammatory bowel disease. Nature Microbiology.]

My research capabilities: Mouse models of colitis, gnotobiotic facilities, 16S and shotgun metagenomics, targeted metabolomics, immune profiling (flow cytometry, cytokine panels).
```

## Example Output

**1. Explicit Gaps**
Authors directly identify these as areas needing further investigation:

- Causal relationships remain unestablished: "whether the microbial changes we observe are causes or consequences of inflammation remains to be determined" (Lloyd-Price et al., Discussion)
- Temporal dynamics in early disease: "the initiating events that precede clinical presentation are not captured by studies of established disease" (Schirmer et al., p. 12)
- Functional significance of metabolic changes: "whether altered metabolite profiles directly contribute to disease pathology requires experimental validation" (Franzosa et al., Discussion)
- Individual variability: "the high inter-individual variability in microbiome composition complicates identification of universal disease signatures" (Lloyd-Price et al.)

**2. Implicit Gaps**

*Untested assumptions:*
- All studies assume fecal samples reflect mucosal community; none validate this in their IBD cohorts (Lloyd-Price et al., Franzosa et al. use fecal; Schirmer et al. uses rectal swabs but doesn't compare to fecal)
- Antibiotic and medication effects on microbiome not fully deconvolved from disease effects

*Missing comparisons:*
- No direct comparison of adult vs. pediatric IBD microbiomes across these studies using matched methods
- Limited comparison between Crohn's disease and ulcerative colitis at the functional/metabolic level

*Unexplored mechanisms:*
- Specific immune pathways activated by the altered metabolites identified by Franzosa et al. are not characterized
- Whether bacterial strains within the same species differ in their pro- or anti-inflammatory properties

*Populations not studied:*
- Pre-clinical or at-risk populations (e.g., first-degree relatives)
- Non-Western populations with different IBD incidence patterns

**3. Contradictions Requiring Resolution**

- Butyrate-producing bacteria: Lloyd-Price et al. report depletion correlates with inflammation; Franzosa et al. show reduced butyrate in feces. However, Schirmer et al. find recovery of butyrate producers doesn't consistently correlate with remission in pediatric UC. Resolution needed: Is butyrate restoration sufficient for benefit?
- Proteobacteria expansion: Consistently observed during active disease, but whether this is pathogenic or opportunistic is unresolved across all three studies.

**4. Methodological Opportunities**

- Longitudinal sampling before and during flare onset (current studies sample during or after)
- Integration of host transcriptomics/proteomics with microbial data (Lloyd-Price et al. do this partially; could be expanded)
- Culture-based isolation of patient-derived strains for mechanistic studies (all studies are culture-independent)
- Spatial organization studies: none examine where specific taxa reside relative to mucosa

**5. Translation Gaps**

- No studies test whether restoring "healthy" microbiome features ameliorates disease
- Biomarker development: signatures identified but not validated prospectively
- Personalized microbiome-based treatment strategies: individual variability noted but not leveraged for personalized approaches

**6. Prioritized Opportunities**

Based on your capabilities (mouse colitis models, gnotobiotics, metabolomics, immune profiling):

1. **Test causality of specific metabolites**: Isolate metabolites identified by Franzosa et al. as depleted in IBD (bile acids, short-chain fatty acids); administer to colitis mice; profile immune response. This leverages your metabolomics and immune profiling capabilities and addresses the explicit causal gap.

2. **Strain-level functional variation**: Culture Proteobacteria strains from healthy vs. IBD patients; colonize gnotobiotic mice; test whether patient-derived strains exacerbate colitis. Addresses the implicit gap about strain-level variation using your gnotobiotic facilities.

3. **Pre-disease microbiome dynamics**: If you can access an at-risk cohort (e.g., first-degree relatives enrolled in a study), characterize microbiome longitudinally before disease onset. Addresses the explicit gap about initiating events, though requires clinical collaboration.

*Note*: Gaps #1 and #2 are within your stated capabilities. Gap #3 would require clinical collaborators with access to pre-diagnosis samples.

## Test Input

Use the following simulated paper summaries to test this prompt:

```
Context: I am a microbiome researcher working on probiotic development. I am trying to identify research gaps and opportunities based on the following papers I have read.

Papers provided:

**Paper 1 Summary:**
Kim et al. (2023). "Lactobacillus rhamnosus GG reduces intestinal inflammation in mouse colitis models."
- Study: DSS-induced colitis in C57BL/6 mice; L. rhamnosus GG administered daily
- Finding: 40% reduction in histological inflammation score; reduced IL-6 and TNF-α
- Limitations noted by authors: Single mouse strain tested; mechanism not fully elucidated
- Future directions: Authors suggest testing in genetic models of IBD

---
**Paper 2 Summary:**
Patel & Johnson (2022). "Human trials of probiotics for IBD show inconsistent results."
- Study: Systematic review of 18 RCTs of probiotics in IBD
- Finding: Only 6/18 trials showed significant benefit; high heterogeneity
- Limitations noted: Variable probiotic strains, doses, and formulations across studies
- Future directions: Authors call for standardized protocols and strain-specific trials

---
**Paper 3 Summary:**
Wong et al. (2024). "Engraftment of probiotic strains is rare and transient in adult humans."
- Study: Shotgun metagenomics tracking of probiotic strains in 50 healthy adults
- Finding: Probiotic strains detected in <20% of subjects; gone within 1 week of cessation
- Limitations noted: Only tested 3 commercial probiotic products
- Future directions: Authors suggest personalized approaches based on baseline microbiome

My research capabilities: Mouse models of colitis (DSS and IL-10 knockout), gnotobiotic facilities, 16S and shotgun sequencing, bacterial culture and strain isolation.
```

**Expected output should include:**
- Explicit gaps quoted from papers (mechanism not elucidated, need standardized protocols, etc.)
- Implicit gaps (translation from mouse to human is weak; engraftment problem not addressed in efficacy trials)
- Contradiction: Kim et al. shows mouse efficacy, but Patel & Johnson meta-analysis shows poor human translation
- Methodological opportunity: Test if engraftment correlates with efficacy using gnotobiotic models
- Prioritized opportunities matching stated capabilities (gnotobiotic facilities, mouse models)

**Verification points:**
- Explicit gaps are actually stated in the paper summaries
- Implicit gaps are reasonable inferences, clearly labeled as such
- Prioritization aligns with stated research capabilities
- No gaps introduced from outside the provided papers

## Failure Modes

- **Fabricating gaps from general knowledge**: May introduce gaps not evident in the provided papers but known from training data
- **Overstating significance**: May present minor limitations as major research opportunities
- **Missing the obvious**: May identify subtle gaps while missing obvious ones because they seem too simple
- **Ignoring feasibility**: May suggest gaps that are technically intractable or would require unavailable resources
- **Sycophancy**: May tailor gaps to seem perfectly suited to your stated capabilities even when the fit is poor
- **Incomplete reading**: With long papers, may miss gaps discussed in later sections or supplementary material

## Verification Requirements

1. **Verify explicit gaps**: Check that "authors say X is needed" claims appear in the papers
2. **Evaluate implicit gaps**: Assess whether inferred gaps are reasonable interpretations or overreaches
3. **Check for false novelty**: Search literature beyond these papers to confirm gaps haven't already been addressed
4. **Assess feasibility**: Evaluate whether gaps are tractable given actual resources, timelines, and expertise
5. **Get external input**: Discuss prioritized gaps with colleagues or mentors before committing research effort

**Critical**: This output generates hypotheses, not validated research directions. Human judgment about importance, feasibility, and fit with your program is essential.

## Variations

### Grant-focused version
Add section: "Gap-to-Aim Translation"—for each prioritized gap, draft a one-sentence specific aim that addresses it.

### Narrow focus
If papers are closely related, focus on a single dimension: "Identify methodological gaps only" or "Identify gaps in mechanistic understanding only."

### Competitive landscape awareness
Add: "What resources or expertise would be needed to address each gap?"—helps assess whether others are likely to close gaps before you can.

### Student-oriented version
Add: "Dissertation-scale opportunities"—flag which gaps could be addressed in 3-5 years by a trainee.

## Model Notes

```
Models tested: [To be completed]
Date tested: [To be completed]
Notes: [To be completed]
```

## Cross-References

- For summarizing papers before gap analysis, see `literature/paper-summary.md`
- For broader synthesis across papers, see `literature/synthesis-across-papers.md`
- For citation verification, see `guides/citation-warning.md`
- For critiquing the gap analysis, see `validation/adversarial-critique.md`
