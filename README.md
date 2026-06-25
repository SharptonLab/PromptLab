# PromptLab

**Tested prompts for using large language models in life science research.**

A collection of ready-to-use prompts designed for researchers who want to use LLMs effectively and responsibly. Every prompt includes failure modes, verification requirements, and has been tested with real inputs.

## Why PromptLab?

LLMs can accelerate research workflows, but they fail in predictable ways—hallucinating citations, giving overconfident statistical advice, and producing plausible-but-wrong outputs. PromptLab provides prompts engineered to mitigate these failures, with explicit guidance on what to verify before trusting any output.

## Contents

**Prompts and guides** (the working surface — most users only need these):

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

**Evaluation evidence** (the paper's testing record — drill in if you want to verify our claims):

| Directory | Description |
|-----------|-------------|
| `tests/` | Per-cell test results: one Markdown file per (prompt × model) capture, with raw model output and the human reviewer's verdict. The matrix overview is at `tests/SUMMARY.md`. |
| `evaluation/` | Combined verdicts, audit trail, and inter-reviewer agreement report. Paper-cited evidence; not needed for using the prompts. |
| `verdicts/` | Immutable per-reviewer verdict files (the raw input that produced `evaluation/`). |

**Reviewing infrastructure** (for adding new reviewer rounds — see [`docs/REVIEWER.md`](docs/REVIEWER.md)):

| Directory | Description |
|-----------|-------------|
| `docs/` | Static review web app, served via GitHub Pages at <https://sharptonlab.github.io/PromptLab/docs/>. Reviewers click through cells in a browser; verdicts save to a file on their disk. |
| `tools/` | Scripts that build the cells manifest, merge reviewer verdicts, and apply canonical verdicts back to per-cell files. See [`tools/PI.md`](tools/PI.md) for the lead-reviewer workflow. |

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

The repository contains 24 runnable prompts plus reference guides and templates in `guides/`. Every runnable prompt has been tested on 2026-06-23 across a fixed 6-model panel — Claude Sonnet 4.6, Claude Opus 4.7, GPT-5.5, Gemini 2.5 Pro, NVIDIA Nemotron 3 Super 120B, StepFun Step-3.7 Flash — with verdicts set by a human reviewer (lead author) against the rubric in [`guides/verification-checklist-extended.md`](guides/verification-checklist-extended.md). A single-model legacy column from 2026-02-04 (Claude Opus 4) is retained for shelf-life comparison.

**Headline pattern across 168 panel cells:** the three frontier closed-weight models passed 100% of prompts in the suite; Gemini 2.5 Pro passed 22 of 24 (one notes-flagged token-budget truncation, one needs-revision); the two open-weight reasoning models had 8.3% and 20.8% failure rates respectively. Failure modes observed include citation fabrication, syntactically broken code, and substantive cross-model disagreement on technical claims.

Where to find the results, by depth:

- **In each prompt file** — every prompt has an inline `## Model Notes` section listing the seven models and their per-prompt verdicts. Fastest path to "did this prompt work for the model I'm planning to use?".
- **[`tests/SUMMARY.md`](tests/SUMMARY.md)** — cross-model coverage matrix (24 prompts × 7 models, per-cell verdicts P / PN / N / ? / S, plus per-model tally rows).
- **`tests/<category>/<prompt>/`** — per-cell result files: raw verbatim model output and the reviewer's verdict, one file per (prompt × model) pair.
- **[`evaluation/`](evaluation/)** — combined canonical verdicts, full audit trail (every reviewer vote with timestamp), and the agreement-report scaffold (pairwise Cohen's kappa for future multi-reviewer runs). Paper-cited evidence; not needed to use the prompts.

See [`docs/TESTING-GUIDE.md`](docs/TESTING-GUIDE.md) for the testing methodology and `evaluation/SECTION_7_DRAFT.md` for the longer write-up.

To contribute additional reviewer verdicts, see [`docs/REVIEWER.md`](docs/REVIEWER.md) — the [static review page](https://sharptonlab.github.io/PromptLab/docs/) lets anyone with a browser click through the cells and produce a verdicts file that can be merged into the canonical evaluation via pull request.

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

If you use PromptLab in your research, please cite this repository. See [`CITATION.cff`](CITATION.cff) for the canonical record (GitHub renders it as a "Cite this repository" widget in the right sidebar of the repo page).

Once the v1.0.0 release is archived on Zenodo, a citable DOI will appear in both `CITATION.cff` and below. Until then, cite the GitHub repository at the commit you used (`https://github.com/SharptonLab/PromptLab/commit/<sha>`).

## Maintainers

[Tom Sharpton](https://github.com/sharpton) - Oregon State University
