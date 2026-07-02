# T4 Agreement Report

- **Policy:** `abstention-aware majority` (S/? treated as abstention; stricter verdict wins on real P/PN vs N disagreement)
- **Reviewers:** Alex Alexiev, TJS
- **Cells with at least one vote:** 171
- **Canonical verdicts set:** 145
- **Real reviewer disagreements (P/PN vs N):** 3

## Per-reviewer activity

| Reviewer | Total | P | PN | N | ? | S |
|---|---:|---:|---:|---:|---:|---:|
| Alex Alexiev | 171 | 97 | 20 | 3 | 6 | 45 |
| TJS | 168 | 139 | 0 | 4 | 0 | 25 |

## Pairwise agreement (Cohen's kappa, real verdicts only)

| Reviewer A | Reviewer B | κ | n overlap |
|---|---|---:|---:|
| Alex Alexiev | TJS | 0.196 | 118 |

  Interpretation (Landis & Koch): **slight**

## Real disagreements (3)

Cells where the two reviewers voted actual (non-abstain) verdicts that differed. Under the conservative rule, N wins.

### `statistics/assumption-checking/nemotron-3-super-120b-2026-06-25`

- **TJS** → `N`
- **Alex Alexiev** → `PN` — **What still needs human verification:**
cut off output
- Whether the ASCII decision tree format would render cleanly: I think it would
- That the captured priority ordering (independence > dispersion) matches peer ordering: yes

### `statistics/design-review/gemini-2-5-pro-2026-06-25`

- **TJS** → `P` — Updated 2026-07-02 after truncation re-run produced complete output.
- **Alex Alexiev** → `N` — **What still needs human verification:**
ran out of space and cuts off
- That the captured content (diet timing concern, mouse strain limit) is technically sound: yes
- Whether the truncated material would change the overall design critique: I think it would need to be rerun, half the prompt isn't addressed.

### `statistics/interpretation-brainstorming/nemotron-3-super-120b-2026-06-25`

- **TJS** → `N`
- **Alex Alexiev** → `PN` — **What still needs human verification:**
- That the captured content covers the main alternative interpretations: yes
- Whether the partial bottom-line bullets match peer recommendations: seems it cuts off

