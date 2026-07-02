# Per-prompt aggregation

Aggregation of the per-cell canonical verdicts (majority of reviewers per cell, with S/? treated as abstention and any real reviewer disagreement resolved conservatively to N). Legacy `claude-opus-4-2026-02-04` column is excluded (not part of the current panel).

**Threshold:** ≥ 4 of 6 panel models must have a passing verdict (P or PN) for the prompt to be reported as "passes overall." Otherwise the prompt is flagged as needing revision.

**Headline:** **24 of 24 prompts pass at the ≥4/6 threshold; 0 need revision.**

## Per-prompt table

| Prompt | P | PN | N | unresolved | Pass rate | Verdict |
|---|---:|---:|---:|---:|---:|---|
| `code/code-explanation` | 6 | 0 | 0 | 0 | 6/6 (100%) | **Passes** |
| `code/debugging` | 6 | 0 | 0 | 0 | 6/6 (100%) | **Passes** |
| `code/python-analysis` | 6 | 0 | 0 | 0 | 6/6 (100%) | **Passes** |
| `code/r-script-generation` | 6 | 0 | 0 | 0 | 6/6 (100%) | **Passes** |
| `code/testing-requirements` | 6 | 0 | 0 | 0 | 6/6 (100%) | **Passes** |
| `fundamentals/chain-of-thought` | 6 | 0 | 0 | 0 | 6/6 (100%) | **Passes** |
| `fundamentals/cross-model-validation` | 5 | 0 | 1 | 0 | 5/6 (83%) | **Passes** |
| `fundamentals/few-shot-learning` | 6 | 0 | 0 | 0 | 6/6 (100%) | **Passes** |
| `fundamentals/meta-prompting` | 6 | 0 | 0 | 0 | 6/6 (100%) | **Passes** |
| `fundamentals/structured-prompt-template` | 5 | 0 | 1 | 0 | 5/6 (83%) | **Passes** |
| `literature/gap-identification` | 6 | 0 | 0 | 0 | 6/6 (100%) | **Passes** |
| `literature/paper-summary` | 6 | 0 | 0 | 0 | 6/6 (100%) | **Passes** |
| `literature/synthesis-across-papers` | 6 | 0 | 0 | 0 | 6/6 (100%) | **Passes** |
| `statistics/assumption-checking` | 5 | 0 | 1 | 0 | 5/6 (83%) | **Passes** |
| `statistics/design-review` | 5 | 0 | 1 | 0 | 5/6 (83%) | **Passes** |
| `statistics/interpretation-brainstorming` | 5 | 0 | 1 | 0 | 5/6 (83%) | **Passes** |
| `statistics/test-selection` | 6 | 0 | 0 | 0 | 6/6 (100%) | **Passes** |
| `validation/adversarial-critique` | 6 | 0 | 0 | 0 | 6/6 (100%) | **Passes** |
| `validation/uncertainty-elicitation` | 6 | 0 | 0 | 0 | 6/6 (100%) | **Passes** |
| `writing/methods-drafting` | 6 | 0 | 0 | 0 | 6/6 (100%) | **Passes** |
| `writing/results-description` | 6 | 0 | 0 | 0 | 6/6 (100%) | **Passes** |
| `writing/reviewer-response` | 6 | 0 | 0 | 0 | 6/6 (100%) | **Passes** |
| `writing/specific-aims` | 6 | 0 | 0 | 0 | 6/6 (100%) | **Passes** |
| `writing/style-matching` | 6 | 0 | 0 | 0 | 6/6 (100%) | **Passes** |

## Cells with real reviewer disagreement (P/PN vs N)

These are cells where one reviewer marked the model output as passing while the other marked it as needing revision. Under the conservative rule (any N wins), these were resolved to N; but you may want to spot-check these individually.

- `statistics/interpretation-brainstorming/nemotron-3-super-120b-2026-06-25` — votes: {'TJS': 'N', 'Alex Alexiev': 'PN'}
- `statistics/design-review/gemini-2-5-pro-2026-06-25` — votes: {'TJS': 'P', 'Alex Alexiev': 'N'}
- `statistics/assumption-checking/nemotron-3-super-120b-2026-06-25` — votes: {'TJS': 'N', 'Alex Alexiev': 'PN'}

## Cells where both reviewers abstained (S/?)

These cells have no canonical verdict. They're counted as "not pass" at the prompt level (denominator stays 6).

- `fundamentals/few-shot-learning/claude-opus-4-2026-02-04` — votes: {'TJS': 'S', 'Alex Alexiev': 'S'}
- `code/testing-requirements/claude-opus-4-2026-02-04` — votes: {'TJS': 'S', 'Alex Alexiev': 'S'}
- `literature/synthesis-across-papers/claude-opus-4-2026-02-04` — votes: {'TJS': 'S', 'Alex Alexiev': 'S'}
- `code/debugging/claude-opus-4-2026-02-04` — votes: {'TJS': 'S', 'Alex Alexiev': 'S'}
- `statistics/assumption-checking/claude-opus-4-2026-02-04` — votes: {'TJS': 'S', 'Alex Alexiev': 'S'}
- `code/r-script-generation/claude-opus-4-2026-02-04` — votes: {'TJS': 'S', 'Alex Alexiev': 'S'}
- `validation/uncertainty-elicitation/claude-opus-4-2026-02-04` — votes: {'TJS': 'S', 'Alex Alexiev': 'S'}
- `statistics/design-review/claude-opus-4-2026-02-04` — votes: {'TJS': 'S', 'Alex Alexiev': 'S'}
- `fundamentals/chain-of-thought/claude-opus-4-2026-02-04` — votes: {'TJS': 'S', 'Alex Alexiev': 'S'}
- `fundamentals/structured-prompt-template/claude-opus-4-2026-02-04` — votes: {'TJS': 'S', 'Alex Alexiev': 'S'}
- `writing/methods-drafting/claude-opus-4-2026-02-04` — votes: {'TJS': 'S', 'Alex Alexiev': 'S'}
- `statistics/test-selection/claude-opus-4-2026-02-04` — votes: {'TJS': 'S', 'Alex Alexiev': 'S'}
- `literature/gap-identification/claude-opus-4-2026-02-04` — votes: {'TJS': 'S', 'Alex Alexiev': 'S'}
- `code/python-analysis/claude-opus-4-2026-02-04` — votes: {'TJS': 'S', 'Alex Alexiev': 'S'}
- `writing/results-description/claude-opus-4-2026-02-04` — votes: {'TJS': 'S', 'Alex Alexiev': 'S'}
- `writing/specific-aims/claude-opus-4-2026-02-04` — votes: {'TJS': 'S', 'Alex Alexiev': 'S'}
- `writing/reviewer-response/claude-opus-4-2026-02-04` — votes: {'TJS': 'S', 'Alex Alexiev': 'S'}
- `documentation/verification-log/claude-opus-4-2026-02-04` — votes: {'TJS': '', 'Alex Alexiev': 'S'}
- `statistics/interpretation-brainstorming/claude-opus-4-2026-02-04` — votes: {'TJS': 'S', 'Alex Alexiev': 'S'}
- `documentation/interaction-log-template/claude-opus-4-2026-02-04` — votes: {'TJS': 'S', 'Alex Alexiev': 'S'}
- `documentation/methods-disclosure-template/claude-opus-4-2026-02-04` — votes: {'TJS': '', 'Alex Alexiev': 'S'}
- `fundamentals/cross-model-validation/claude-opus-4-2026-02-04` — votes: {'TJS': 'S', 'Alex Alexiev': 'S'}
- `code/code-explanation/claude-opus-4-2026-02-04` — votes: {'TJS': 'S', 'Alex Alexiev': 'S'}
- `fundamentals/meta-prompting/claude-opus-4-2026-02-04` — votes: {'TJS': 'S', 'Alex Alexiev': 'S'}
- `literature/paper-summary/claude-opus-4-2026-02-04` — votes: {'TJS': 'S', 'Alex Alexiev': 'S'}
- `validation/adversarial-critique/claude-opus-4-2026-02-04` — votes: {'TJS': 'S', 'Alex Alexiev': 'S'}
