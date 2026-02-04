# PromptLab

**Tested prompts for using large language models in life science research.**

A collection of ready-to-use prompts designed for researchers who want to use LLMs effectively and responsibly. Every prompt includes failure modes, verification requirements, and has been tested with real inputs.

## Why PromptLab?

LLMs can accelerate research workflows, but they fail in predictable ways—hallucinating citations, giving overconfident statistical advice, and producing plausible-but-wrong outputs. PromptLab provides prompts engineered to mitigate these failures, with explicit guidance on what to verify before trusting any output.

## Contents

| Directory | Description |
|-----------|-------------|
| `fundamentals/` | Core prompting strategies (structured prompts, few-shot learning, chain-of-thought, meta-prompting, cross-validation) |
| `literature/` | Literature synthesis and review |
| `writing/` | Manuscripts, grants, and reviewer responses |
| `code/` | Code generation, debugging, and explanation |
| `statistics/` | Statistical reasoning and experimental design |
| `validation/` | Verification, critique, and uncertainty elicitation |
| `documentation/` | Templates for documenting LLM use |
| `examples/` | Worked case studies demonstrating complete workflows |
| `guides/` | Quick-reference guides |
| `tests/` | Test results showing prompt performance |

## Quick Start

1. Find a prompt for your task (e.g., `literature/paper-summary.md`)
2. Read the **When to Use** and **When NOT to Use** sections
3. Copy the prompt and fill in the `{PLACEHOLDERS}`
4. Run it with your preferred LLM
5. **Follow the Verification Requirements** before using the output

## Prompt File Format

Each prompt includes:

| Section | Purpose |
|---------|---------|
| **Task Description** | What this prompt accomplishes |
| **When to Use / When NOT to Use** | Appropriate and inappropriate contexts |
| **The Prompt** | Complete text with `{PLACEHOLDERS}` for customization |
| **Example Input/Output** | Representative use case |
| **Test Input** | Standardized test case for validation |
| **Failure Modes** | What can go wrong (hallucination, sycophancy, overconfidence) |
| **Verification Requirements** | What to check before trusting output |
| **Model Notes** | Testing history |

## Key Principles

**Prompts are experiments.** Like any research tool, prompts need validation. We provide test inputs and expected outputs so you can verify prompts work for your use case.

**Verification is not optional.** Every prompt includes specific verification requirements. LLM outputs require checking—the prompts help you know what to check.

**Failure modes are features.** We document how each prompt can fail so you know what to watch for. Acknowledging limitations makes tools more trustworthy, not less.

## Testing

All 27 prompts have been tested with standardized inputs. Test results are in `tests/[category]/[prompt-name]/`. See `docs/TESTING-GUIDE.md` for the testing methodology.

## Contributing

We welcome contributions of tested prompts. See `CONTRIBUTING.md` for guidelines.

Requirements:
- Prompt must follow the standard format (see `PROMPT-STYLE-GUIDE.md`)
- Must include realistic failure modes and verification requirements
- Must include a Test Input section with expected output
- Must include at least one test result file

## License

CC-BY-4.0

## Citation

If you use PromptLab in your research, please cite:

```
[Citation information to be added after publication]
```

## Maintainers

[Tom Sharpton](https://github.com/sharpton) - Oregon State University
