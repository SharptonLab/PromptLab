# Changelog

All notable changes to this project are documented in this file. Format
loosely follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versioning follows [SemVer](https://semver.org/).

## [Unreleased]

_Planned for v1.1: extending the test panel with at least one additional
human reviewer for inter-rater Cohen's kappa per cell; an API
structured-output worked example for one extraction prompt (R1.7);
prompt coverage for RNA-seq metadata extraction. See open GitHub issues
for the current cut._

## [1.0.0] — 2026-06-25 (planned release)

This release replaces the unverifiable "all 27 prompts tested" claim
of the initial drop with a complete, human-verified cross-model
evaluation, and adds infrastructure so additional reviewers can extend
the evaluation through normal pull-request flow. The repository now
embodies the methodology the companion paper recommends.

### Added

- **Cross-model test panel** (2026-06-23) covering all 24 runnable prompts
  across 6 models: Claude Sonnet 4.6, Claude Opus 4.7, GPT-5.5, Gemini 2.5
  Pro, NVIDIA Nemotron 3 Super 120B (open weights, on-prem at OSU CQLS),
  StepFun Step-3.7 Flash (open weights, on-prem at OSU CQLS). Result of
  144 per-cell `tests/<category>/<prompt>/<model>-2026-06-23.md` files,
  with raw model outputs captured verbatim.
- **Inline per-prompt `## Model Notes`** in every runnable prompt file,
  showing the verdict each panel model received on that prompt — readers
  see how the panel did without leaving the prompt file.
- **[`tests/SUMMARY.md`](tests/SUMMARY.md)** — cross-model coverage
  matrix with per-cell verdicts (P / PN / N / ? / S) and per-model tally
  rows. Indexes the per-cell drill-down.
- **`evaluation/` directory** holding the paper-cited evidence:
  combined canonical verdicts (`T4-canonical-verdicts.json`), full
  per-reviewer audit trail (`T4-audit-trail.json`), inter-reviewer
  agreement report scaffolding (`T4-agreement-report.md`), and a
  Section-7 manuscript-draft companion (`SECTION_7_DRAFT.md`,
  `AI_DISCLOSURE_DRAFT.md`).
- **Static review SPA** at
  [`docs/index.html`](https://sharptonlab.github.io/PromptLab/docs/),
  served via GitHub Pages. Reviewers click through cells in a browser;
  verdicts save to a file on their disk via the File System Access API
  (Chrome / Edge / Opera) with a localStorage fallback for other
  browsers. See `docs/REVIEWER.md`.
- **Reviewing tooling** at `tools/`:
  `build_manifest.py` (regenerates `docs/cells-manifest.json` from
  `tests/`), `merge_verdicts.py` (combines multiple reviewer verdict
  files into canonical + agreement report with pairwise Cohen's
  kappa), `apply_canonical.py` (writes canonical verdicts back to
  per-cell Recommendation fields), and a full PI walkthrough in
  `tools/PI.md`.
- **GitHub Action** at `.github/workflows/verdict-review.yml` that
  runs the merge script on every PR adding to `verdicts/`, posting
  the agreement report as a PR comment.
- **`verdicts/` directory** as the immutable drop zone for per-reviewer
  verdict files (one per reviewer, never edited after commit). First
  entry: `tjs-verdicts.json` from the lead author's review of all 171
  cells.

### Changed

- **Reclassified 3 reference docs** out of the task directories into
  `guides/`: `citation-warning.md`, `cross-model-protocols.md`, and
  `verification-checklist.md` (renamed to `verification-checklist-extended.md`
  to coexist with the existing concise checklist). The repo had been
  claiming 27 runnable prompts but only 24 had the required
  `## The Prompt` + `## Test Input` sections.
- **README "Testing" section** rewritten to state panel composition and
  dates explicitly, surface the per-model verdict pattern, and link to
  the layered evidence (per-prompt notes → `tests/SUMMARY.md` →
  per-cell files → `evaluation/`). Removed the "all 27 prompts tested"
  framing that triggered the original reviewer complaint.
- **All 27 legacy `claude-opus-4-2026-02-04.md` result files** were
  audited: their self-asserted "Pass" verdicts (written by the original
  Claude Code capture pipeline, not a human) were demoted to
  `PENDING AUTHOR REVIEW` and then re-verified by a human in the same
  T4 review pass as the new panel cells.

### Fixed

- **Harness `prompt_io.py` fence-regex truncation.** A non-greedy
  fence match silently truncated `## Test Input` content for any
  prompt containing nested triple-backtick code blocks, sending
  incomplete prompts to all panel models. Affected 6 prompts
  (`code/{code-explanation, debugging, testing-requirements}`,
  `fundamentals/{chain-of-thought, cross-model-validation,
  meta-prompting}`). Bug was caught during T4 review; fixed and the
  36 affected cells were re-captured with the full prompts. Same
  class of bug subsequently caught and prevented in the review SPA
  and `tests/SUMMARY.md` rendering.

### Removed

- **Per-cell `## Assessment` scaffolding sections** in `tests/`
  result files. These had held machine-suggested triage (Claude
  Opus 4.7 pre-drafts) used to speed the T4 human-verification
  pass; once verdicts were set the scaffolding was no longer
  serving the public repo. The triage drafts remain in
  `evaluation/T4-audit-trail.json` for provenance.

## [0.1.0] — 2026-02-04

- Initial release. 27 task-dir markdown files (later reclassified
  to 24 runnable prompts + 3 reference guides during the 2026-06
  revision) covering core prompting strategies, literature
  synthesis, writing assistance, code, statistics, validation,
  documentation, and worked example case studies. A single
  Claude Opus 4 test capture per prompt is recorded under
  `tests/`, dated 2026-02-04.
