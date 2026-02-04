# Structured Prompt Template

## Task Description

A general-purpose template for constructing well-formed prompts that include all essential components for reliable LLM outputs in research contexts.

## When to Use

- Starting any new LLM-assisted task where you want consistent, verifiable outputs
- Complex tasks requiring clear specification of context, constraints, and format
- Tasks you'll repeat across multiple inputs (standardization)
- When previous informal prompts have produced unreliable results
- Teaching others to construct effective prompts

## When NOT to Use

- Simple, one-off queries where the overhead isn't justified (e.g., "What R function calculates standard deviation?")
- Exploratory brainstorming where constraints would limit useful divergence
- When you're still figuring out what you need—use meta-prompting first (see `meta-prompting.md`)

## The Prompt

```
**Context:**
{RESEARCH_CONTEXT}

**Your role:**
{ROLE_SPECIFICATION}

**Task:**
{TASK_SPECIFICATION}

**Input:**
{INPUT_MATERIAL}

**Constraints:**
- {CONSTRAINT_1}
- {CONSTRAINT_2}
- {CONSTRAINT_3}

**Output format:**
{FORMAT_SPECIFICATION}

**Evaluation criteria:**
{WHAT_MAKES_OUTPUT_GOOD}
```

## Prompt Components Explained

| Component | Purpose | When to Include |
|-----------|---------|-----------------|
| **Context** | Provides background the model needs to understand your situation | Always for non-trivial tasks |
| **Role** | Frames how the model should approach the task | When expertise framing affects interpretation |
| **Task** | Explicit statement of what you want done | Always |
| **Input** | The material the model will work with | When providing documents, data, or code |
| **Constraints** | Boundaries on acceptable outputs; prevents failure modes | Always for important tasks |
| **Output format** | Structure and formatting requirements | When you need consistent, comparable outputs |
| **Evaluation criteria** | How output will be judged; guides trade-offs | When multiple valid approaches exist |

## Example Input

A researcher needs to extract methodology information from a microbiology paper for a systematic review.

```
**Context:**
I'm conducting a systematic review of gut microbiome studies in mouse models of inflammatory bowel disease. I need to extract standardized methodology information from each paper for comparison.

**Your role:**
You are a systematic review assistant extracting methodology details from primary research papers.

**Task:**
Extract the methodology information specified below from the provided paper. Use only information explicitly stated in the paper.

**Input:**
[Full text of research paper provided here]

**Constraints:**
- Use only information present in the paper—do not infer or add external knowledge
- If information is not explicitly stated, write "Not reported"
- Do not interpret or evaluate the methodology; only extract what is stated
- Use exact terminology from the paper where possible

**Output format:**
Provide the following fields, one per line:

- Mouse strain:
- Sample size (n per group):
- IBD model (DSS, TNBS, genetic, etc.):
- Sequencing platform:
- 16S region targeted:
- Bioinformatics pipeline:
- Alpha diversity metrics reported:
- Beta diversity methods:
- Statistical tests for differential abundance:
- Key confounds acknowledged:

**Evaluation criteria:**
Accuracy and completeness are paramount. It is better to report "Not reported" than to guess.
```

## Example Output

```
- Mouse strain: C57BL/6J (Jackson Laboratory)
- Sample size (n per group): 10 mice per group (4 groups, 40 total)
- IBD model (DSS, TNBS, genetic, etc.): DSS (2.5% w/v in drinking water, 7 days)
- Sequencing platform: Illumina MiSeq
- 16S region targeted: V4 region (515F/806R primers)
- Bioinformatics pipeline: QIIME2 (version 2021.11) with DADA2 for denoising
- Alpha diversity metrics reported: Shannon diversity, observed ASVs, Faith's PD
- Beta diversity methods: Bray-Curtis dissimilarity, weighted UniFrac; PCoA visualization
- Statistical tests for differential abundance: DESeq2 with Benjamini-Hochberg correction
- Key confounds acknowledged: Cage effects (addressed by distributing treatments across cages), sex not controlled (all male mice used)
```

## Test Input

Use the following self-contained test case to verify this prompt template works correctly:

```
**Context:**
I'm conducting a systematic review of gut microbiome studies in mouse models of inflammatory bowel disease. I need to extract standardized methodology information from each paper for comparison.

**Your role:**
You are a systematic review assistant extracting methodology details from primary research papers.

**Task:**
Extract the methodology information specified below from the provided paper excerpt. Use only information explicitly stated in the text.

**Input:**
[PAPER EXCERPT - Methods Section]
"Male C57BL/6 mice (8-10 weeks old, n=12 per group) were obtained from Charles River Laboratories. Colitis was induced by administering 3% dextran sulfate sodium (DSS, molecular weight 36,000-50,000; MP Biomedicals) in drinking water for 7 days, followed by 7 days of regular water. Control mice received regular water throughout. Fecal samples were collected on days 0, 7, and 14.

DNA was extracted using the QIAamp PowerFecal Pro DNA Kit (Qiagen). The V3-V4 region of the 16S rRNA gene was amplified using primers 341F/785R and sequenced on the Illumina NovaSeq 6000 platform (2×250 bp paired-end reads). Raw sequences were processed using QIIME2 version 2023.5 with DADA2 for quality filtering and denoising.

Alpha diversity (Shannon index, observed features) was compared between groups using Kruskal-Wallis tests. Beta diversity was assessed using Bray-Curtis dissimilarity and visualized with PCoA. PERMANOVA was used to test for significant differences between groups. Differential abundance analysis was performed using ANCOM-BC with FDR correction. A p-value < 0.05 was considered statistically significant. The study was not pre-registered, and sample size was based on previous experience rather than formal power analysis."

**Constraints:**
- Use only information present in the paper—do not infer or add external knowledge
- If information is not explicitly stated, write "Not reported"
- Do not interpret or evaluate the methodology; only extract what is stated
- Use exact terminology from the paper where possible

**Output format:**
Provide the following fields, one per line:

- Mouse strain:
- Sample size (n per group):
- IBD model (DSS, TNBS, genetic, etc.):
- Sequencing platform:
- 16S region targeted:
- Bioinformatics pipeline:
- Alpha diversity metrics reported:
- Beta diversity methods:
- Statistical tests for differential abundance:
- Key confounds acknowledged:

**Evaluation criteria:**
Accuracy and completeness are paramount. It is better to report "Not reported" than to guess.
```

**Expected output should include:**
- Mouse strain: C57BL/6
- Sample size: 12 per group
- IBD model: DSS (3%)
- Sequencing platform: Illumina NovaSeq 6000
- 16S region: V3-V4 (341F/785R primers)
- Pipeline: QIIME2 version 2023.5 with DADA2
- Alpha diversity: Shannon index, observed features
- Beta diversity: Bray-Curtis, PCoA, PERMANOVA
- Differential abundance: ANCOM-BC with FDR correction
- Key confounds: Should note "Not reported" or mention lack of pre-registration/power analysis

## Failure Modes

### Hallucination Risks
- Model may fill in "reasonable" values for fields marked "Not reported" if constraint isn't explicit enough
- May conflate information from different sections or studies cited in the paper
- May invent specific version numbers or parameters not stated in the paper

### Sycophancy Risks
- Minimal for extraction tasks; more relevant for evaluative tasks

### Overconfidence Risks
- May present uncertain extractions without hedging
- May not flag ambiguous passages where multiple interpretations exist

### Context Issues
- Long papers may be incompletely processed; critical details in supplementary methods may be missed
- Information stated early in the paper may receive less attention than later sections

## Verification Requirements

1. **Spot-check extracted values** against the original paper for at least 3-4 fields per extraction
2. **Pay special attention to specific numbers** (sample sizes, p-values, version numbers)—these are frequently wrong
3. **Verify "Not reported" entries** are genuinely absent, not just missed by the model
4. **For systematic reviews**: Verify 100% of extractions for papers that will be included in quantitative synthesis

## Variations

### Minimal Version (for simple tasks)
```
Context: {BRIEF_CONTEXT}

Task: {TASK_SPECIFICATION}

Constraints:
- {KEY_CONSTRAINT}

Output format: {FORMAT}
```

### With Few-Shot Examples
Add before the task:
```
**Examples of the format I need:**

Example 1:
Input: [example input]
Output: [example output]

Example 2:
Input: [example input]
Output: [example output]

Now process my input using the same format:
```

### With Uncertainty Elicitation
Add to constraints:
```
- For any field where you are uncertain, add [UNCERTAIN] after your answer
- If information could be interpreted multiple ways, note the ambiguity
```

## Model Notes

```
Models tested: [To be completed]
Date tested: [To be completed]
Notes: [To be completed]
```

## Related Prompts

- For developing prompts iteratively: see `meta-prompting.md`
- For teaching format through examples: see `few-shot-learning.md`
- For complex reasoning tasks: see `chain-of-thought.md`
