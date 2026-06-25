# Evaluation evidence

This directory holds the derived artifacts from the cross-model evaluation of
PromptLab's prompts — the paper-cited evidence behind any claim about how
specific models performed. Not needed for using the prompts themselves; see
the top-level README for that.

> **Planned for removal after the manuscript is accepted.** This whole
> directory is scaffolding for the 2026-07 resubmission cycle. The audit
> data is preserved long-term in the Zenodo archive (DOI-pinned) and in
> git history; the prose drafts (`SECTION_7_DRAFT.md`,
> `AI_DISCLOSURE_DRAFT.md`, `MANUSCRIPT_HANDOFF.md`) migrate into the
> published manuscript itself. Once those landing places exist, this
> directory comes out so the public repo's surface area is just the
> prompts and the lightweight evaluation index (`tests/SUMMARY.md`).

## What's here

| File | What it is |
|---|---|
| `T4-canonical-verdicts.json` | One verdict per (prompt × model) cell, after applying the merge policy. Currently 171 cells (24 prompts × 6 panel models + 27 legacy Opus 2026-02-04 cells). |
| `T4-audit-trail.json` | Every reviewer's vote on every cell, preserved with timestamps. The non-collapsed source of truth — `canonical` is derived from this. |
| `T4-agreement-report.md` | Human-readable summary: per-reviewer activity counts, pairwise Cohen's kappa (when ≥2 reviewers), and the full disagreement list. |

## Where the inputs to these came from

- Raw reviewer files: `../verdicts/*.json` (one file per reviewer, immutable)
- Per-cell result files (with raw model outputs + final verdicts): `../tests/<category>/<slug>/<model-slug>-<date>.md`
- Source prompts: `../<category>/<slug>.md` — each has a `## Model Notes` section summarizing how the panel did on it

## Regenerating

When more reviewer files land in `../verdicts/`:

```bash
python3 tools/merge_verdicts.py verdicts/*.json --policy majority --out-dir evaluation
python3 tools/apply_canonical.py evaluation/T4-canonical-verdicts.json --force
```

(`--force` because cells already carry a Recommendation from the previous canonical.)

Then re-run `harness/reconcile_notes.py` to update the source prompts'
`## Model Notes` sections and `harness/summarize_cross_model.py` to regenerate
`../tests/SUMMARY.md`.

## Why this is separate from `verdicts/`

`verdicts/` is the **source** — one file per reviewer, never modified, the
immutable record of who voted what when. `evaluation/` is the **derived**
output — combined, summarized, and human-friendly. Splitting them keeps the
provenance clear and makes it impossible to accidentally edit raw reviewer
data when updating the summary.

See `tools/PI.md` for the full reviewing-and-merging workflow.
