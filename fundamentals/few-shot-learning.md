# Few-Shot Learning

## Task Description

A prompting strategy that provides example input-output pairs to teach the model your specific expectations, dramatically improving consistency for complex or idiosyncratic tasks.

## When to Use

- Standardizing output format across many similar inputs (e.g., extracting the same fields from 50 papers)
- Tasks where natural language descriptions are ambiguous but examples are clear
- When default model behavior differs from what you need
- Matching specific formatting conventions (citation styles, data formats, naming conventions)
- Training the model to recognize patterns in your domain

## When NOT to Use

- Simple tasks where instructions alone suffice
- Highly variable inputs where examples might over-constrain the model
- When you don't have good examples to provide
- Exploratory tasks where you want the model to surprise you
- When context window space is at a premium and examples would crowd out input material

## The Prompt

```
{TASK_DESCRIPTION}

Here are examples of the format I need:

**Example 1:**
Input: {EXAMPLE_INPUT_1}
Output: {EXAMPLE_OUTPUT_1}

**Example 2:**
Input: {EXAMPLE_INPUT_2}
Output: {EXAMPLE_OUTPUT_2}

**Example 3:**
Input: {EXAMPLE_INPUT_3}
Output: {EXAMPLE_OUTPUT_3}

Now process the following using the same format:

Input: {ACTUAL_INPUT}
Output:
```

## Prompt Components Explained

| Component | Purpose | Notes |
|-----------|---------|-------|
| **Task description** | Brief framing of what the examples demonstrate | Keep short; examples do the heavy lifting |
| **Examples** | Demonstrate the exact format and level of detail you want | 3 examples typically optimal; more for complex patterns |
| **Input/Output labels** | Create clear structure the model will replicate | Consistent labeling improves pattern matching |
| **Actual input** | The material you want processed | Follows same format as example inputs |

## Example Input

A researcher needs to extract structured metadata from microbiome paper abstracts in a consistent format for a database.

```
I need to extract structured metadata from microbiome study abstracts. Extract only information explicitly stated in the abstract.

Here are examples of the format I need:

**Example 1:**
Input: "The gut microbiome plays a crucial role in host metabolism. We performed 16S rRNA gene sequencing on fecal samples from 120 participants (60 with type 2 diabetes, 60 healthy controls) recruited from three clinical sites. Using QIIME2 and LEfSe analysis, we identified 23 differentially abundant taxa, with Akkermansia muciniphila significantly depleted in diabetic patients (p < 0.001). Our findings suggest potential therapeutic targets for metabolic disease."

Output:
- Study type: Case-control
- Disease/condition: Type 2 diabetes
- Sample type: Fecal
- Sample size: 120 (60 cases, 60 controls)
- Sequencing: 16S rRNA gene
- Analysis tools: QIIME2, LEfSe
- Key finding: Akkermansia muciniphila depleted in diabetic patients
- Organism: Human

**Example 2:**
Input: "Early-life antibiotic exposure may have lasting effects on the developing microbiome. We followed 85 infants from birth to 24 months, collecting monthly stool samples. Shotgun metagenomic sequencing revealed that antibiotic-exposed infants (n=42) showed reduced bacterial diversity and delayed maturation of metabolic pathways compared to unexposed controls (n=43). Machine learning models predicted antibiotic exposure history with 89% accuracy based on 12-month microbiome profiles."

Output:
- Study type: Longitudinal cohort
- Disease/condition: Antibiotic exposure (not disease)
- Sample type: Stool
- Sample size: 85 infants (42 exposed, 43 controls)
- Sequencing: Shotgun metagenomics
- Analysis tools: Machine learning (not specified further)
- Key finding: Antibiotic exposure reduces diversity and delays metabolic pathway maturation
- Organism: Human (infant)

**Example 3:**
Input: "Dietary fiber modulates gut microbial composition in murine models. C57BL/6 mice (n=40) were randomized to high-fiber or control diet for 8 weeks. 16S rRNA sequencing of cecal contents using Illumina MiSeq showed increased Bacteroidetes and decreased Firmicutes in the high-fiber group. Metabolomic analysis confirmed elevated short-chain fatty acid production."

Output:
- Study type: Randomized controlled (animal)
- Disease/condition: Dietary intervention (not disease)
- Sample type: Cecal contents
- Sample size: 40 mice
- Sequencing: 16S rRNA (Illumina MiSeq)
- Analysis tools: Not specified
- Key finding: High-fiber diet increases Bacteroidetes, decreases Firmicutes, elevates SCFAs
- Organism: Mouse (C57BL/6)

Now process the following using the same format:

Input: "Inflammatory bowel disease is associated with gut dysbiosis, but causal relationships remain unclear. We analyzed 16S rRNA sequences from colonic biopsies of 200 Crohn's disease patients and 150 healthy volunteers using DADA2 and PICRUSt2. Patients showed reduced alpha diversity (Shannon index, p < 0.0001) and enrichment of adherent-invasive E. coli. Predicted metagenomes revealed depleted butyrate biosynthesis pathways in patient samples."

Output:
```

## Example Output

```
- Study type: Case-control
- Disease/condition: Crohn's disease
- Sample type: Colonic biopsies
- Sample size: 350 (200 cases, 150 controls)
- Sequencing: 16S rRNA
- Analysis tools: DADA2, PICRUSt2
- Key finding: Reduced alpha diversity, enriched adherent-invasive E. coli, depleted butyrate pathways in CD patients
- Organism: Human
```

## Test Input

Use the following abstract to test this prompt:

```
I need to extract structured metadata from microbiome study abstracts. Extract only information explicitly stated in the abstract.

Here are examples of the format I need:

**Example 1:**
Input: "The gut microbiome plays a crucial role in host metabolism. We performed 16S rRNA gene sequencing on fecal samples from 120 participants (60 with type 2 diabetes, 60 healthy controls) recruited from three clinical sites. Using QIIME2 and LEfSe analysis, we identified 23 differentially abundant taxa, with Akkermansia muciniphila significantly depleted in diabetic patients (p < 0.001). Our findings suggest potential therapeutic targets for metabolic disease."

Output:
- Study type: Case-control
- Disease/condition: Type 2 diabetes
- Sample type: Fecal
- Sample size: 120 (60 cases, 60 controls)
- Sequencing: 16S rRNA gene
- Analysis tools: QIIME2, LEfSe
- Key finding: Akkermansia muciniphila depleted in diabetic patients
- Organism: Human

**Example 2:**
Input: "Early-life antibiotic exposure may have lasting effects on the developing microbiome. We followed 85 infants from birth to 24 months, collecting monthly stool samples. Shotgun metagenomic sequencing revealed that antibiotic-exposed infants (n=42) showed reduced bacterial diversity and delayed maturation of metabolic pathways compared to unexposed controls (n=43). Machine learning models predicted antibiotic exposure history with 89% accuracy based on 12-month microbiome profiles."

Output:
- Study type: Longitudinal cohort
- Disease/condition: Antibiotic exposure (not disease)
- Sample type: Stool
- Sample size: 85 infants (42 exposed, 43 controls)
- Sequencing: Shotgun metagenomics
- Analysis tools: Machine learning (not specified further)
- Key finding: Antibiotic exposure reduces diversity and delays metabolic pathway maturation
- Organism: Human (infant)

Now process the following using the same format:

Input: "Fecal microbiota transplantation (FMT) shows promise for recurrent Clostridioides difficile infection. This randomized controlled trial enrolled 68 patients with recurrent CDI, assigning them to FMT (n=34) or vancomycin (n=34). Stool samples were analyzed using shotgun metagenomics with MetaPhlAn3. At 8 weeks, FMT achieved 91% cure rate versus 62% for vancomycin (p=0.008). FMT recipients showed rapid engraftment of donor Bacteroidetes species and restoration of secondary bile acid metabolism."

Output:
```

**Expected output should include:**
- Study type: Randomized controlled trial
- Disease/condition: Recurrent Clostridioides difficile infection
- Sample type: Stool
- Sample size: 68 (34 FMT, 34 vancomycin)
- Sequencing: Shotgun metagenomics
- Analysis tools: MetaPhlAn3
- Key finding: FMT 91% cure rate vs 62% vancomycin; donor Bacteroidetes engraftment
- Organism: Human

**Verification points:**
- Output matches the demonstrated format exactly
- All extracted information is present in the abstract
- No information is inferred or fabricated

## Failure Modes

### Hallucination Risks
- Model may infer fields not present in input based on patterns in examples (e.g., guessing organism is "Human" when not stated)
- May invent plausible-sounding tool names if analysis methods aren't mentioned

### Sycophancy Risks
- Minimal for extraction tasks

### Overconfidence Risks
- Model may confidently extract information that requires interpretation rather than direct extraction
- Won't flag when input differs significantly from example patterns

### Context Issues
- Examples consume context window space that could be used for longer inputs
- Too many examples may cause the model to over-fit to superficial patterns

## Verification Requirements

1. **Check that outputs match the demonstrated format** exactly
2. **Verify extracted information against source** for at least the first few outputs
3. **Watch for pattern over-fitting**: if all your examples had "Human" as organism, check that mouse studies are correctly labeled
4. **Test with an edge case** that differs from your examples to ensure generalization

## Variations

### Minimal Few-Shot (2 examples)
Use when examples are long or context window is limited:
```
Here are two examples of the output format:

Example 1: [input] → [output]
Example 2: [input] → [output]

Now process: [actual input]
```

### Few-Shot with Explicit Rules
Combine examples with stated rules for edge cases:
```
Extract metadata using this format. Rules:
- If information isn't stated, write "Not reported"
- For sample size, include breakdown by group if available

Examples:
[examples]

Process: [input]
```

### Few-Shot with Counter-Examples
Show what NOT to do:
```
Good example:
Input: [input]
Output: [correct output]

Bad example (don't do this):
Input: [same input]
Output: [incorrect output showing common mistake]

Now process: [actual input]
```

### Graduated Complexity
Start with simple examples, progress to complex:
```
Simple case:
[straightforward example]

More complex case:
[example with ambiguity or missing data]

Edge case:
[unusual example]

Now process: [actual input]
```

## Selecting Good Examples

1. **Representative**: Cover the range of variation you expect in actual inputs
2. **Correct**: Examples must be accurately formatted—the model will replicate errors
3. **Diverse**: Include different cases so the model generalizes rather than memorizes
4. **Edge cases**: Include at least one example showing how to handle missing data or ambiguity
5. **Appropriate length**: Match the detail level you want in outputs

## Model Notes

```
Tested across the panel; verdicts set by human review.

- Claude Opus 4 (claude-opus-4-5-20251101) (2026-02-04): Pass
- claude-opus-4.7 (2026-06-23): Pass
- claude-sonnet-4.6 (2026-06-23): Pass
- gemini-2.5-pro (2026-06-23): Pass
- gpt-5.5 (2026-06-23): Pass
- nemotron-3-super-120b (2026-06-23): Pass
- step-3.7-flash (2026-06-23): Pass

Full per-model raw outputs and reviewer notes: tests/fundamentals/few-shot-learning/
```

## Related Prompts

- For the base structure examples build on: see `structured-prompt-template.md`
- For multi-step reasoning: see `chain-of-thought.md`
- For developing good examples iteratively: see `meta-prompting.md`
