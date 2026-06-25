# Meta-Prompting

## Task Description

Using the LLM to help develop, refine, and improve prompts before using them for your actual task. This strategy surfaces hidden assumptions, identifies ambiguities, and produces more effective prompts than most users write unaided.

## When to Use

- Developing prompts for complex or unfamiliar tasks
- Creating reusable prompts that will be used many times
- When initial prompts produce inconsistent or unsatisfactory results
- When you're unsure what information the model needs to complete a task well
- Before investing significant time in a prompt-driven workflow
- When you know what you want but struggle to specify it precisely

## When NOT to Use

- Simple, one-off queries where the overhead isn't justified
- Tasks where you already have well-tested prompts
- When you're exploring and don't yet know what you want
- Time-critical situations where prompt development would cause delays

## The Prompt

### Interview Approach
```
I want your help with a task, but before I describe it, I want you to ask me clarifying questions to ensure you understand exactly what I need.

The task involves: {BRIEF_TASK_DESCRIPTION}

What questions do you have about the format, scope, audience, constraints, or purpose that would help you assist me effectively?
```

### Prompt Critique Approach
```
Here's a prompt I'm planning to use for {TASK_DESCRIPTION}:

---
{DRAFT_PROMPT}
---

Please critique this prompt:
1. What's ambiguous or underspecified?
2. What assumptions am I making that might not hold?
3. What failure modes might this prompt produce?
4. How would you improve it to make outputs more consistent and reliable?

Provide a revised version of the prompt incorporating your suggestions.
```

### Reverse Engineering Approach
```
I want to create a prompt that produces outputs like these examples:

Example output 1:
{EXAMPLE_OUTPUT_1}

Example output 2:
{EXAMPLE_OUTPUT_2}

Based on these examples, write a prompt that would reliably produce this type of output. Include:
- Clear task specification
- Appropriate constraints
- Output format specification
- Any examples that would help
```

## Prompt Components Explained

| Component | Purpose | Notes |
|-----------|---------|-------|
| **Brief task description** | Gives model enough context to ask relevant questions | Don't over-specify—let questions surface gaps |
| **Request for questions** | Prompts the model to identify missing information | Be prepared to answer honestly |
| **Draft prompt** | Material for the model to critique | Include your best attempt |
| **Example outputs** | Demonstrate what success looks like | Choose representative, well-formed examples |

## Example Input

### Example 1: Interview Approach

A researcher wants to develop a prompt for summarizing microbiome papers but isn't sure how to specify the task.

```
I want your help with a task, but before I describe it, I want you to ask me clarifying questions to ensure you understand exactly what I need.

The task involves: summarizing research papers about the gut microbiome for a literature review I'm writing.

What questions do you have about the format, scope, audience, constraints, or purpose that would help you assist me effectively?
```

### Example Output 1: Interview Response

```
Before I can help effectively, I have several questions:

**About the output format:**
1. What length should each summary be? (A paragraph? A page? Bullet points?)
2. Should summaries follow a consistent structure (e.g., objective/methods/findings/limitations)?
3. Do you want summaries suitable for a specific citation format (e.g., narrative synthesis vs. tabular comparison)?

**About the content focus:**
4. What aspects of each paper matter most for your review? (Methods? Findings? Population studied?)
5. Are you comparing papers on a specific question, or surveying a broad area?
6. Should I include critical evaluation, or just descriptive summary?

**About the audience:**
7. Who is the literature review for? (Grant reviewers? Journal readers? Your own reference?)
8. What's the expected level of technical detail?

**About constraints:**
9. Should I only use information in the papers, or can I note connections to other literature?
10. How should I handle papers with conflicting findings?
11. Are there specific things you do NOT want included (e.g., statistical details, funding sources)?

**About the papers:**
12. How will you provide the papers? (Full text? Abstracts only?)
13. Approximately how many papers are we talking about?

Answering these will help me suggest an effective prompt structure for your task.
```

### Example 2: Prompt Critique Approach

```
Here's a prompt I'm planning to use for extracting methodology from microbiome papers:

---
Read this paper and extract the methodology information. Tell me what sequencing they used, what bioinformatics tools, and what statistics.
---

Please critique this prompt:
1. What's ambiguous or underspecified?
2. What assumptions am I making that might not hold?
3. What failure modes might this prompt produce?
4. How would you improve it to make outputs more consistent and reliable?

Provide a revised version of the prompt incorporating your suggestions.
```

### Example Output 2: Critique Response

```
**Critique:**

1. **Ambiguities and underspecification:**
   - "Sequencing" is vague: Do you want the platform (Illumina, PacBio)? The region (V4, full-length 16S)? The read depth?
   - "Bioinformatics tools" could mean anything from quality control to differential abundance testing
   - "Statistics" doesn't specify: Descriptive? Inferential? For which comparisons?
   - No output format specified—you'll get inconsistent structures across papers
   - No instruction on what to do if information isn't reported

2. **Assumptions that might not hold:**
   - Assumes the paper clearly reports all methodological details (many don't)
   - Assumes single sequencing approach (some papers use multiple)
   - Assumes "methodology" means the same thing to the model as to you

3. **Likely failure modes:**
   - Inconsistent output format across papers
   - Model may infer or guess at unreported details rather than flagging gaps
   - May miss important methodological elements you care about but didn't mention
   - May include excessive detail on aspects you don't need

**Revised prompt:**

---
Extract methodology information from this microbiome research paper using the following format. Use only information explicitly stated in the paper.

**Sequencing:**
- Platform (e.g., Illumina MiSeq, NovaSeq, PacBio):
- Target region (e.g., 16S V4, 16S V3-V4, shotgun, ITS):
- Primers used (if reported):
- Read depth or sequencing depth (if reported):

**Bioinformatics:**
- Pipeline or primary software (e.g., QIIME2, mothur, DADA2):
- Taxonomy database (e.g., SILVA, Greengenes, RDP):
- Key processing steps explicitly mentioned:

**Statistical analysis:**
- Alpha diversity metrics:
- Beta diversity metrics and tests:
- Differential abundance method:
- Multiple testing correction:
- Key statistical tests for primary hypothesis:

**Instructions:**
- If information is not explicitly stated, write "Not reported"
- Do not infer or guess—only extract what is clearly stated
- If multiple approaches were used, list all
---

This revision specifies exact fields, defines output format, and prevents hallucination of unreported details.
```

## Test Input

Use the following prompt critique scenario to test this prompt:

```
Here's a prompt I'm planning to use for analyzing differential gene expression results:

---
Look at my RNA-seq results and tell me which genes are important. The data is from a mouse liver study comparing high-fat diet to control.
---

Please critique this prompt:
1. What's ambiguous or underspecified?
2. What assumptions am I making that might not hold?
3. What failure modes might this prompt produce?
4. How would you improve it to make outputs more consistent and reliable?

Provide a revised version of the prompt incorporating your suggestions.
```

**Expected output should include:**

**Critique identifying:**
- "Important" is undefined (statistically significant? biologically relevant? largest fold change?)
- No output format specified
- No information about the analysis already performed (DESeq2? edgeR?)
- No context about research question or hypothesis
- No constraints on interpretation scope

**Revised prompt should include:**
- Specific criteria for "important" (e.g., FDR < 0.05 AND |log2FC| > 1)
- Defined output format (table, ranked list, etc.)
- Placeholders for actual results data
- Constraints preventing overinterpretation
- Request for uncertainty acknowledgment

**Verification points:**
- Critique is specific and actionable, not generic
- Revised prompt addresses each identified issue
- Revised prompt follows good prompting principles

## Failure Modes

### Hallucination Risks
- Model may suggest prompt improvements that sound good but don't actually help
- Reverse-engineered prompts may not reliably reproduce the example patterns

### Sycophancy Risks
- Model may not critique your prompt harshly enough
- May suggest mild refinements when significant restructuring is needed
- Add explicit instruction: "Be direct about weaknesses—gentle suggestions won't help me improve the prompt"

### Overconfidence Risks
- Model may confidently suggest changes that make prompts worse
- Critique may miss actual problems while focusing on minor issues

### Context Issues
- For reverse engineering, the model may focus on superficial patterns rather than underlying structure

## Verification Requirements

1. **Test the improved prompt**: The only real validation is whether the new prompt produces better outputs than the original
2. **Compare before/after**: Run both versions on the same input to assess improvement
3. **Check multiple inputs**: A prompt that works on one input may fail on others
4. **Verify critique accuracy**: If the model claims something is ambiguous, consider whether it actually is
5. **Iterate**: Meta-prompting often requires 2-3 rounds of refinement

## Variations

### Comprehensive Interview
```
I want to develop a robust, reusable prompt for {TASK}. Interview me about this task—ask detailed questions about:
- What success looks like
- What failure looks like
- Edge cases and exceptions
- How outputs will be used
- What I care most about

After I answer your questions, draft a complete prompt and explain your design choices.
```

### Comparative Critique
```
Here are two versions of a prompt for the same task:

Version A:
{PROMPT_A}

Version B:
{PROMPT_B}

Compare these prompts:
1. What does each do well?
2. What problems does each have?
3. Which would produce more reliable outputs and why?
4. How would you combine the best elements of both?
```

### Failure Analysis
```
I used this prompt:

{PROMPT}

And got this output:

{PROBLEMATIC_OUTPUT}

The problem is: {DESCRIPTION_OF_PROBLEM}

Diagnose what in my prompt led to this failure and suggest specific changes to prevent it.
```

### Progressive Refinement
```
Here's my current prompt:

{CURRENT_PROMPT}

It works reasonably well, but I want to improve {SPECIFIC_ASPECT}.

Suggest 2-3 targeted modifications that address this issue without breaking what's already working.
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

Full per-model raw outputs and reviewer notes: tests/fundamentals/meta-prompting/
```

## Related Prompts

- For the prompts you're developing: see `structured-prompt-template.md`
- For consistency across outputs: see `few-shot-learning.md`
- For complex reasoning tasks: see `chain-of-thought.md`
- For validating improved prompts: see `cross-model-validation.md`
