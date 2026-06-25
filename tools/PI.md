# PI / lead-reviewer instructions

This document walks the project lead through publishing the review page, gathering reviewer verdicts, and producing the canonical verdicts + agreement report.

## One-time setup — enable GitHub Pages

The static review page lives at `docs/index.html`. Publish it once:

1. Push the repo (the `docs/` directory must be in `main`).
2. In the GitHub repo settings: **Settings → Pages**.
3. Under **Source**, pick **Deploy from a branch**. Branch: `main`. **Folder: `/` (root)** — not `/docs`.
4. Save. GitHub takes a minute or two; the review page URL will be `https://<owner>.github.io/<repo>/docs/`. For this repo: **`https://sharptonlab.github.io/PromptLab/docs/`**.

Why root-folder serving (not `/docs`)? The SPA fetches result files from
`tests/...md` at the repo root. Pages can only serve files inside its
configured source folder. If we served from `/docs`, the SPA couldn't reach
`/tests/`; `raw.githubusercontent.com` doesn't set CORS headers, so
cross-origin fetches from there would be blocked. Root-folder serving puts
`/docs/` and `/tests/` on the same origin, making everything Just Work.

The repo's root URL (`https://sharptonlab.github.io/PromptLab/`) will render
the repo's `README.md` as before. The SPA lives at `…/docs/` — link to it
from the README if you want a discoverable entry point.

## Rebuilding the cells manifest

Whenever you add/remove test result files under `tests/`, regenerate the manifest:

```bash
python3 tools/build_manifest.py
git add docs/cells-manifest.json
git commit -m "Rebuild cells manifest"
git push
```

The manifest is what the SPA reads to know which 171 cells exist.

## Assigning reviewers

The matrix is 24 prompts × 7 model columns = 168 cells (plus 3 doc templates). For majority-rules merging to be meaningful you want **at least 3 reviewers per cell**; for the paper's inter-rater story you probably want each cell to be reviewed by 2–3 of the same reviewers.

A reasonable allocation pattern (matches the spirit of TASKS.md):
- **All reviewers review all cells** if you have the bandwidth. Maximum agreement data, slow.
- **Split + spot-check** (faster): each cell has one lead reviewer; one reviewer spot-checks ~20% of every other reviewer's calls. Less full coverage but still gives inter-rater stats on the spot-checked subset.

Send each reviewer the URL plus their assignment ("Tom: code + fundamentals; Ed: literature + statistics; Alexandra: validation + writing; Alexandra also spot-checks 10 random cells from each of Tom and Ed").

## Gathering reviewer files

Each reviewer produces a `<name>-verdicts.json` file. They can send it back via:

- **Email** → save into `verdicts/` locally on your machine.
- **Pull request** → reviewer commits the file under `verdicts/`. The Action at `.github/workflows/verdict-review.yml` runs `tools/merge_verdicts.py` on every such PR and posts the agreement report as a comment. Merge the PR when ready.

## Producing the canonical verdicts

Once you have all the reviewer files in one place:

```bash
python3 tools/merge_verdicts.py verdicts/*.json --policy majority --out-dir evaluation
```

Produces three files in `evaluation/`:

- `T4-canonical-verdicts.json` — one verdict per cell, majority decision. Cells without a majority stay PENDING.
- `T4-audit-trail.json` — every reviewer's vote on every cell, preserved.
- `T4-agreement-report.md` — pairwise Cohen's kappa across reviewers + the disagreement list.

### Policy options

- `--policy majority` (default): wins if >50% of reviewers vote the same. Ties / no-majority leave the cell unresolved (you decide manually).
- `--policy unanimity`: every reviewer must agree, otherwise unresolved. Most conservative.
- `--policy lead-reviewer --lead tom-sharpton`: take the lead reviewer's verdict; other reviewers' votes inform the agreement report but don't override.

### Including the local-server verdicts

If you used the local FSA-server (`harness/t4_review_server.py`) before the SPA, that file (`harness/T4-verdicts.json`) is in a different shape and has no `reviewer` field. Include it with:

```bash
python3 tools/merge_verdicts.py \
  harness/T4-verdicts.json \
  verdicts/*.json \
  --reviewer-for=T4-verdicts.json=tom-local \
  --policy majority
```

## Applying canonical verdicts to the test result files

`tools/apply_canonical.py` takes `evaluation/T4-canonical-verdicts.json` and updates the per-result-file `Recommendation:` line + appends reviewer-supplied notes to the file's `## Overall Assessment` notes.

```bash
python3 tools/apply_canonical.py evaluation/T4-canonical-verdicts.json
# or, if cells already have a Recommendation from a previous canonical:
python3 tools/apply_canonical.py evaluation/T4-canonical-verdicts.json --force
```

Reviewer-supplied notes carry attribution (e.g. `tjs (2026-06-25): <note>`); pure attribution without note content is omitted. The full audit trail lives in `evaluation/T4-audit-trail.json` so per-file notes stay clean.

Then `harness/reconcile_notes.py` updates the source prompts' `## Model Notes` sections from the now-approved results, and `harness/summarize_cross_model.py` produces `tests/SUMMARY.md`.

## Sanity checks before declaring T4 done

- `T4-agreement-report.md` shows pairwise κ; values <0.4 on any pair are a red flag worth discussing.
- The disagreement list should be empty or very small if your reviewers were broadly aligned. If it's large, your reviewers may be applying different criteria.
- Spot-check a few canonical "Pass" cells yourself to confirm the majority decision matches your read.

## Troubleshooting

**Reviewer says "the page just spins forever"**
Probably the `cells-manifest.json` failed to fetch. Check that `docs/cells-manifest.json` is committed and that Pages is serving from `/docs`. They can also try a hard refresh (Cmd-Shift-R).

**Reviewer's file has weird timestamps or repeated entries**
The merge script picks the latest timestamp per (reviewer, cell). You can pass the same reviewer's file multiple times (e.g. partial and full) safely.

**Action fails on PR**
Check the Action log; the merge script writes verbose errors to stderr. Likely cause is malformed JSON from a reviewer (e.g. they edited the file by hand and broke it).
