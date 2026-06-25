# PromptLab repo revision — manuscript handoff

> **Temporary artifact, tied to the 2026-07 journal resubmission cycle.**
> This document briefs the manuscript-revision agent on what the repo-side
> work produced and what's still pending. After resubmission, this and the
> rest of `evaluation/` will be removed from the public repo (the audit
> trail and drafts are not part of the long-term public surface, just
> evidence for this revision cycle). Last updated 2026-06-25.

---

## What changed in this revision cycle

- **v1.0.0 released and DOI minted.** Repo is now citable.
  - Concept DOI (preferred for paper citation; resolves to current version):
    **`10.5281/zenodo.20855199`** → <https://doi.org/10.5281/zenodo.20855199>
  - GitHub release: <https://github.com/SharptonLab/PromptLab/releases/tag/v1.0.0>
  - Suggested citation: *Sharpton, T. (2026). PromptLab: Tested prompts for
    using large language models in life science research (v1.0.0). Zenodo.
    <https://doi.org/10.5281/zenodo.20855199>*
- **Repo metadata complete:** `CITATION.cff`, `CHANGELOG.md`, and a DOI
  badge on the README are live at commit `c78e1d2`.

## Repository state

- **Public repo:** <https://github.com/SharptonLab/PromptLab>
- **Static review SPA:** <https://sharptonlab.github.io/PromptLab/docs/>
- **Latest commit:** `c78e1d2` (T7 DOI patch); branch `main`, clean.
- **T1–T7 complete.** T8 (R1.7 API structured-output example) still open.

## Empirical data ready for Section 7

24 runnable prompts × 6-model panel + 27 legacy single-model cells = **171
cells, single reviewer (TJS), 2026-06-23 capture + 2026-06-25 review**.

| Model | Pass | PN | N | ? | Pass rate |
|---|---:|---:|---:|---:|---:|
| Claude Sonnet 4.6 | 24 | 0 | 0 | 0 | **100%** |
| Claude Opus 4.7 | 24 | 0 | 0 | 0 | **100%** |
| GPT-5.5 | 24 | 0 | 0 | 0 | **100%** |
| Gemini 2.5 Pro | 22 | 1 | 1 | 0 | **91.7%** |
| Nemotron 3 Super 120B (open) | 21 | 0 | 2 | 1 | **87.5%** |
| Step-3.7 Flash (open) | 19 | 0 | 5 | 0 | **79.2%** |
| Claude Opus 4 (2026-02-04 legacy) | 24 | 0 | 0 | 0 | **100%** |

Cross-model matrix: `tests/SUMMARY.md`. Full audit trail:
`evaluation/T4-audit-trail.json`.

### Concrete failure-mode examples (to ground §7.2 discussion)

- **Citation fabrication:** Nemotron cited "McMurdie & Holmes (2014) PLOS
  ONE" — paper exists but in PLOS Comp Biol. Step-3.7 invented a
  *F. prausnitzii*/butyrate/r=0.27 association not in the input notes.
- **Syntactically broken code:** Step-3.7 produced R:
  `glm(..., family = negative.binomial())` — not a real function.
- **Substantive cross-model disagreement:** Nemotron claimed DESeq2's
  `lfcThreshold` triggers a likelihood ratio test; the other five panel
  models described it correctly as modifying the Wald test's null. Panel
  disagreement made the candidate error visible.
- **Silent failure on a frontier model:** Gemini 2.5 Pro on a chain-of-
  thought prompt produced a response truncated mid-final-step because its
  output budget was exhausted on internal reasoning — would have shipped
  looking fine without verification.

## Manuscript-bound drafts (already in the repo, committed)

| File | What it is |
|---|---|
| `evaluation/SECTION_7_DRAFT.md` | ~1100-word draft of Section 7: Methodology (§7.1), Results with per-model tally (§7.2), Cross-model disagreement as useful signal citing Cohen 2023 + Panickssery 2024 (§7.3), five-point Limitations (§7.4). Marked clearly as machine-drafted-awaiting-author-revision; every quantitative claim is sourced from the audit. |
| `evaluation/AI_DISCLOSURE_DRAFT.md` | Full manuscript paragraph + a shorter README-footer variant. Distinguishes AI-as-tool from AI-as-system-under-test, names specific models. |
| `README.md` Testing section | Already rewritten to drop the "all 27 tested" overclaim; states panel composition + dates + headline pass-rate pattern + layered links to evidence. |

Treat the drafts as starting prose to refine and integrate, not final text.

## Reviewer-comment coverage

| Reviewer comment | Status | Where the evidence lives |
|---|---|---|
| **R1.5** — "all 27 prompts tested" overclaim | **Done.** Counts now 24 runnable + 11 guides; every claim per-cell-attributable. | README Testing; `tests/SUMMARY.md`; `evaluation/T4-canonical-verdicts.json` |
| **R1.8** — cross-model agreement as evidence | **Done (data).** Per-model pass-rate table + failure-mode catalogue + cross-model-disagreement subsection in Section 7 draft. Paper text needs integration. | `tests/SUMMARY.md`; `evaluation/SECTION_7_DRAFT.md §7.2-7.3` |
| **R1.14** — apply our own verification checklist | **Done (data).** Used `guides/verification-checklist-extended.md` rubric during T4. Disclosed in §7.1 draft + AI Disclosure draft. | `evaluation/SECTION_7_DRAFT.md §7.1`; `evaluation/AI_DISCLOSURE_DRAFT.md` |
| **R1.7** — API structured-output example | **Pending (T8).** Not yet implemented in the repo. | n/a |

## What to do *now* in the manuscript

1. **Add the DOI citation** to the references section (or wherever the
   venue puts software citations). Use the suggested string above.
2. **Integrate `evaluation/SECTION_7_DRAFT.md`** — read, edit voice/length
   to match the manuscript style, drop in.
3. **Add the AI Disclosure** from `evaluation/AI_DISCLOSURE_DRAFT.md` to
   wherever the venue requires it (Author Contributions, Methods,
   dedicated section).
4. **Draft the response-to-reviewers letter** using the coverage table
   above as the skeleton.
5. **Decide on R1.7 / T8:** required for resubmission, or acceptable as
   committed future work? If required, the repo work is ~half a day and
   triggers a v1.0.1 / v1.1.0 release with a new DOI. If not, the
   response letter cites it as committed work pointing to a GitHub issue
   or milestone.

## Pending items that affect the manuscript

1. **Ed + Alex reviews still incoming.** Once their verdict files land in
   `verdicts/` (via SPA + PR or emailed in), the merge script will
   produce:
   - Inter-reviewer Cohen's kappa (§7.4 currently says single-reviewer-
     only with kappa as future work)
   - Updated `evaluation/T4-agreement-report.md`
   - A disagreement list (cells where reviewers split — needs attention
     if non-empty)
   - **If Ed/Alex are broadly consistent with TJS:** §7.4's "single
     reviewer" limitation is promoted to "multi-reviewer with κ = X.XX,"
     strengthening R1.8. v1.1.0 release with new DOI; manuscript
     footnote update.
   - **If they diverge meaningfully:** the divergence is itself paper
     material — disagreement among trained reviewers reinforces the
     paper's core argument. Worth discussing in §7.3 rather than
     averaging away.
2. **T8 — structured-output API example** still open. Addresses R1.7.
   ~half-day in the repo. Should be done before any v1.0.x / v1.1.0
   follow-up release if R1.7 needs to be answered in the resubmission.

## How to verify any claim above

Every number above comes from a specific file. Don't take any quantitative
claim on faith — open the referenced file and read it.

- Per-cell narrative: per-cell result files under `tests/<category>/<slug>/`.
- Verdict tally: `tests/SUMMARY.md`, or regenerate by running
  `python3 tools/merge_verdicts.py verdicts/*.json --policy majority`.
- Audit trail of every reviewer vote with timestamps:
  `evaluation/T4-audit-trail.json`.

## Lifespan note

The entire `evaluation/` directory (including this file, the audit-trail
JSON, the drafts, and the report) is scheduled for removal from the
public repo after the manuscript is accepted and the resubmission cycle
closes. The data is preserved permanently in:

- the Zenodo archive (immutable, DOI-pinned)
- git history (`git log evaluation/` will recover everything)
- the manuscript itself, where the relevant prose lives long-term

So once the paper is out, the public repo trims back to: prompts, guides,
tests/, docs/ (the review SPA), tools/, and verdicts/. The evidence stays
discoverable via the DOI and git history.
