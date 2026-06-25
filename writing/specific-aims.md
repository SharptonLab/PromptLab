# Specific Aims Page Drafting Prompt

## Task Description

Generate a structured first draft of a grant Specific Aims page from your research plan notes, producing the conventional structure (opening paragraph, aims, closing) that can be refined into a compelling funding request.

## When to Use

- Converting a research plan into Specific Aims format
- Structuring your thinking about how aims relate to each other
- Drafting when you know your science but struggle with grant rhetoric
- Checking that your aims are logically connected and appropriately scoped

## When NOT to Use

- When you haven't developed the research plan yourself (this structures your ideas, doesn't generate them)
- To fabricate preliminary data or cite papers you haven't read
- For aims outside your expertise where you can't evaluate feasibility claims
- As a substitute for understanding the funding agency's priorities

## The Prompt

```
Context: I am drafting a Specific Aims page for a {GRANT_TYPE: e.g., "NIH R01," "NSF CAREER," "foundation grant"} on {RESEARCH_TOPIC}. The funding agency emphasizes {AGENCY_PRIORITIES: e.g., "mechanistic understanding," "translational potential," "innovative methods"}.

My research plan notes:
{YOUR_NOTES: Include the problem, your approach, preliminary data if any, and what each aim will accomplish}

Target length: {LENGTH: e.g., "1 page," "500 words"}

Task: Draft a Specific Aims page with the following structure:

**Opening paragraph (The Hook):**
- First sentence: Establish the problem and its significance (the "so what")
- Knowledge gap: What critical barrier limits progress?
- Your solution: How does your approach address this gap?
- Long-term goal and overall objective for this proposal

**Specific Aims (2-3 typically):**
For each aim:
- State the aim as a clear objective (what you will do)
- Brief rationale (why this aim matters)
- Approach summary (1-2 sentences on how)
- Expected outcome (what you'll learn)

**Closing paragraph:**
- How the aims integrate and build on each other
- Impact statement: what will be possible after this work that isn't possible now?
- Connection to agency mission (if applicable)

Constraints:
- Use ONLY information from my notes—do not fabricate preliminary data, citations, or capabilities
- Flag any claims that need preliminary data support as [NEEDS PRELIM DATA]
- Flag any citations needed as [CITE]
- Keep within target length
- Use active, confident language—avoid excessive hedging
- Make aims concrete and achievable within the funding period

Output format: Formatted aims page with section headers. Flag gaps for my attention.
```

## Prompt Components Explained

| Component | Purpose |
|-----------|---------|
| **Grant type and agency** | Different agencies have different expectations and rhetoric |
| **Agency priorities** | Tailors framing to what reviewers value |
| **Your research plan notes** | The substance—LLM structures but doesn't invent science |
| **Target length** | Specific Aims are typically strictly length-limited |
| **Structural template** | Conventional aims page structure that reviewers expect |
| **Constraints** | Prevent fabrication; flag gaps rather than fill them with invention |

## Example Input

```
Context: I am drafting a Specific Aims page for an NIH R01 on the gut-brain axis in depression. The funding agency emphasizes mechanistic understanding and translational potential.

My research plan notes:

Problem: Depression affects 280 million people globally. Current treatments fail ~30% of patients. Emerging evidence suggests gut microbiome plays a role, but we don't understand the causal mechanisms well enough to develop microbiome-based treatments.

My approach: Use gnotobiotic mice to establish causality and identify mechanisms linking specific gut bacteria to depression-like behaviors. We have preliminary data showing FMT from depressed patients induces anhedonia in mice.

Aim 1: Determine which bacterial species are sufficient to induce depression-like behaviors
- Use gnotobiotic colonization with defined communities
- Identify minimal community that reproduces the phenotype
- Have pilot data showing 3 candidate species from preliminary FMT work

Aim 2: Identify the molecular mechanisms linking candidate bacteria to brain function
- Look at bacterial metabolites (we have metabolomics capability)
- Examine gut-brain signaling pathways (vagus, immune, HPA)
- Measure brain neurochemistry and inflammation

Aim 3: Test if targeting the microbiome can reverse depression-like behaviors
- Therapeutic intervention study—can we fix it once it's established?
- Tests translational potential

Long-term goal: Develop microbiome-based therapies for treatment-resistant depression

My lab: expertise in gnotobiotics, microbiome analysis, mouse behavior (have established FST, SPT, and OFT protocols)

Target length: 1 page
```

## Example Output

# Specific Aims

Major depressive disorder affects over 280 million people worldwide and remains inadequately treated: approximately 30% of patients fail to respond to existing therapies [CITE]. Emerging evidence implicates the gut microbiome in depression pathophysiology, with observational studies revealing altered microbial communities in depressed individuals and transplantation studies suggesting these alterations may contribute to behavioral symptoms [CITE]. However, the specific bacteria responsible and the mechanistic pathways linking gut microbes to brain function remain undefined. **This critical gap prevents the rational development of microbiome-based interventions for depression.**

We address this gap using gnotobiotic mouse models that enable controlled manipulation of the gut microbiome. Our preliminary studies demonstrate that fecal microbiota transplantation from patients with major depression into germ-free mice induces anhedonia-like behavior (reduced sucrose preference), establishing a tractable model system [NEEDS PRELIM DATA: include effect size and n]. Building on this foundation, **our overall objective is to identify specific gut bacteria that induce depression-like behaviors and define the mechanisms by which they influence brain function.** Our long-term goal is to develop microbiome-based therapeutic strategies for treatment-resistant depression.

**Aim 1: Identify bacterial species sufficient to induce depression-like behaviors in gnotobiotic mice.** We hypothesize that a defined subset of the depression-associated microbiome is sufficient to reproduce behavioral effects. Using gnotobiotic colonization with progressively simplified communities derived from our FMT model, we will identify the minimal bacterial consortium that induces anhedonia and behavioral despair. Preliminary data implicate three candidate species [NEEDS PRELIM DATA: name species]. This aim will pinpoint causal organisms for mechanistic investigation.

**Aim 2: Define molecular mechanisms linking depression-associated bacteria to brain function.** We hypothesize that candidate bacteria influence the brain through metabolite production, immune activation, or vagal signaling. We will characterize the metabolomic output of causal bacteria, assess gut and systemic immune activation, and evaluate vagal involvement through selective denervation. Brain tissue will be analyzed for neurochemical and inflammatory changes. This aim will identify therapeutic targets at the microbiome-gut-brain interface.

**Aim 3: Test whether microbiome-targeted interventions can reverse established depression-like behaviors.** We hypothesize that correcting the microbial imbalance will ameliorate behavioral symptoms even after they are established. Using our gnotobiotic model, we will test whether introduction of "protective" bacteria or removal of causal species reverses anhedonia. This aim directly tests translational potential.

**Impact:** These aims are integrated and synergistic: Aim 1 identifies causal bacteria; Aim 2 defines mechanisms; Aim 3 tests therapeutic potential. Completion of this project will establish which specific microbes drive depression-like behaviors, how they influence the brain, and whether the microbiome is a viable therapeutic target—essential knowledge for developing microbiome-based treatments for the millions of patients who do not respond to existing antidepressants.

## Test Input

Use the following notes to test this prompt:

```
Context: I am drafting a Specific Aims page for an NIH R21 (exploratory/developmental) on microbiome biomarkers for colorectal cancer screening. The funding agency emphasizes innovative approaches and high-risk/high-reward research.

My research plan notes:

Problem: Colorectal cancer is the 2nd leading cause of cancer death in the US. Colonoscopy screening is effective but has low compliance (~60%). Non-invasive biomarkers could improve screening rates. Current fecal tests (FIT, Cologuard) have limited sensitivity for adenomas.

My approach: Develop a microbiome-based classifier that detects precancerous adenomas from stool samples. Leverage the known microbiome changes in CRC to detect disease earlier.

Preliminary data:
- Pilot study with 25 adenoma cases, 25 controls
- 16S sequencing identified 12 differentially abundant taxa
- Random forest classifier achieved 78% AUC (needs validation)

Aim 1: Validate and refine the microbiome classifier in an independent cohort
- Partner with GI clinic for prospective sample collection
- Target 100 adenoma cases, 100 controls
- Test classifier performance and refine features

Aim 2: Integrate microbiome data with existing biomarkers (FIT)
- Hypothesis: combined model outperforms either alone
- Collect FIT results alongside microbiome samples
- Build integrated classifier

Innovation: First study to combine microbiome signatures with established screening biomarkers for adenoma detection

My lab: expertise in microbiome bioinformatics, machine learning, established GI collaborations

Target length: 1 page (R21 limit)
```

**Expected output should include:**
- Appropriate hook establishing the screening compliance problem
- Clear knowledge gap (current tests miss adenomas)
- Reference to preliminary data with [NEEDS PRELIM DATA] flags for specific numbers
- Two aims appropriate for R21 scope (exploratory, 2-year timeline)
- [CITE] flags for statistics (CRC death rates, colonoscopy compliance)
- Innovation statement
- Impact statement appropriate for exploratory mechanism

**Verification points:**
- All preliminary data numbers match input exactly (25/25, 12 taxa, 78% AUC)
- Scope appropriate for R21 (not overambitious)
- No fabricated capabilities or collaborations beyond what's stated
- Appropriate [CITE] and [NEEDS PRELIM DATA] flags

## Failure Modes

- **Fabricating preliminary data**: May invent pilot results you didn't provide
- **Inventing citations**: May create fake references to support claims
- **Over-promising**: May claim achievable outcomes beyond what's realistic
- **Generic framing**: May produce boilerplate that doesn't capture what's innovative about your work
- **Misrepresenting expertise**: May claim capabilities you didn't mention having
- **Ignoring scope**: May produce aims too large for the funding mechanism
- **Sycophantic enthusiasm**: May oversell significance rather than make a measured case

## Verification Requirements

1. **Verify all claims**: Every factual statement should be either from your notes or flagged for citation
2. **Check preliminary data references**: Ensure any mentioned prelim data exists and is accurately described
3. **Verify feasibility**: Confirm you actually have the expertise, resources, and access claimed
4. **Check scope**: Ensure aims are achievable in the funding period (typically 3-5 years for R01)
5. **Verify no fabrication**: Compare to your notes—remove anything substantive that was added
6. **Test the logic**: Confirm aims actually build on each other as claimed
7. **Check institutional claims**: Verify references to your capabilities are accurate

## Variations

### R21/exploratory mechanism
For smaller, exploratory grants:
```
Constrain to 2 aims. Emphasize innovation and risk-taking over guaranteed outcomes. Frame as establishing feasibility for larger proposals.
```

### Foundation grants
For foundation or philanthropic funding:
```
Emphasize patient impact and translational timeline. Reduce jargon. Include a patient-facing impact statement.
```

### Renewal/competing continuation
For renewing an existing project:
```
Include: progress on previous aims, what new questions emerged, how proposed aims build on established work. Reference publications and preliminary data from the previous funding period.
```

### Multiple PI structure
For collaborative proposals:
```
Clarify which PI leads each aim. Include integration plan describing how the team will work together.
```

## Model Notes

```
Tested across the panel; verdicts set by human review.

- Claude Opus 4 (claude-opus-4-5-20251101) (2026-02-04): Pass
- claude-opus-4.7 (2026-06-23): Pass
- claude-sonnet-4.6 (2026-06-23): Pass
- gemini-2.5-pro (2026-06-23): Pass
- gpt-5.5 (2026-06-23): Pass
- nemotron-3-super-120b (2026-06-23): Pass
- step-3.7-flash (2026-06-23): Needs revision

Full per-model raw outputs and reviewer notes: tests/writing/specific-aims/
```

## Cross-References

- For methods sections in grant proposals, see `writing/methods-drafting.md`
- For literature synthesis supporting significance, see `literature/synthesis-across-papers.md`
- For identifying gaps that motivate your aims, see `literature/gap-identification.md`
- For critique of your aims before submission, see `validation/adversarial-critique.md`
