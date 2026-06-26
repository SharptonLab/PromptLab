# Section 7: Testing methodology and results (draft)

> **Status: machine-drafted, awaiting author revision.** Drafted by Claude
> Opus 4.7 from the empirical results in this directory + `tests/SUMMARY.md`,
> for the lead author to edit before incorporation into the manuscript. The
> draft sticks to what the artifacts support; check every claim against
> `evaluation/T4-audit-trail.json` and `tests/SUMMARY.md` before publication.

---

## 7.1  Testing methodology

PromptLab contains 24 runnable prompts (those with both a `## The Prompt`
section and a self-contained `## Test Input` section) plus 11 reference
guides and documentation templates. The 24 runnable prompts span six task
categories: code generation and explanation (5), prompting fundamentals (5),
literature analysis (3), statistical reasoning (4), validation workflows (2),
and writing assistance (5).

To answer reviewer R1.8's request for cross-model evidence and to address
R1.5's concern about overclaiming, every runnable prompt was tested across a
fixed six-model panel on 2026-06-23, in addition to a single-model legacy
column captured on 2026-02-04 (Claude Opus 4) that we retain for shelf-life
comparison. The 2026-06-23 panel was selected to span the closed-weight
frontier tier most life-science researchers actually interact with through
chatbots (Claude Sonnet 4.6, Claude Opus 4.7, GPT-5.5, Gemini 2.5 Pro) plus
two open-weight reasoning-capable models served on-prem at OSU's Center for
Quantitative Life Sciences (Nemotron 3 Super 120B, Step-3.7 Flash). All
model versions are pinned in `harness/models.yaml`; the per-result-file
date suffix records when the capture was made.

Capture was driven by a thin harness (`harness/run_tests.py`) that, for each
prompt, assembles the `## The Prompt` and `## Test Input` sections into a
single user-role message and dispatches it to each enabled model. Outputs are
written verbatim into `tests/<category>/<prompt-name>/<model-slug>-<date>.md`
with no post-processing. Two harness-level deviations are worth flagging for
methodological transparency:

1. **Temperature was dropped for reasoning-capable models.** All four
   reasoning-capable models on the panel (GPT-5.5, Claude Opus 4.7, Nemotron
   3 Super, Step-3.7 Flash) reject or ignore explicit temperature settings;
   the harness detects the resulting `BadRequestError` and retries without
   the parameter. Outputs from those four models therefore reflect each
   provider's internal default, not the T=0.0 the harness requested. Claude
   Sonnet 4.6 and Gemini 2.5 Pro accepted T=0.0.

2. **`max_tokens` was bumped above the harness default** (`4 096`) for
   every panel model except Sonnet's stated default-tier behavior could
   span long responses without it. Final values used: Sonnet 4.6 = 16 384;
   Opus 4.7 = 32 000; GPT-5.5 = 32 000; Gemini 2.5 Pro = 32 000;
   Nemotron 3 Super = 16 384; Step-3.7 Flash = 16 384. The default 4 096
   was consumed by internal chain-of-thought on reasoning-capable models
   (the visible answer was empty) and by long-output prompts on the
   non-reasoning models (mid-sentence truncation). The bumps were applied
   in two passes: an initial round before the main capture for the models
   we expected to need it (GPT-5.5, Step-3.7, Nemotron), and a second
   targeted re-run for 19 cells across Sonnet, Opus, and Gemini that
   showed mid-sentence truncation in the first pass. The 19 re-runs used
   `--force --date 2026-06-25` to overwrite in place; the previous
   truncated captures are recoverable from git history. One re-run cell
   (Opus 4.7 on `literature/paper-summary`) still ended mid-sentence at
   the bumped 32 000-token cap, suggesting either a stop-sequence quirk
   or a model-side limit we did not characterize; the captured output is
   substantive and was reviewed as-is.

Captured outputs were then human-verified by the lead author through a
static review SPA (deployed via GitHub Pages, source at `docs/index.html`)
that displays each cell — the source prompt, the test input, the filled
prompt that was actually sent, and the raw model output — and persists
verdicts to a local file on disk. The review rubric was the repository's own
`guides/verification-checklist-extended.md`, satisfying reviewer R1.14's ask
that we apply our own published checklist to our own claims.

All 171 cells (24 prompts × 6 panel models + 27 legacy Opus cells, including
3 documentation templates that are not part of the panel) received a
verdict: Pass, Pass with notes, Needs revision, or Cannot judge from output
alone. Per-cell verdicts are reproduced inline in each source prompt's
`## Model Notes` section. The cross-model coverage matrix is at
`tests/SUMMARY.md`. The combined audit trail, including the full
per-reviewer voting record and pairwise Cohen's kappa machinery for
future multi-reviewer runs, lives in `evaluation/`.

## 7.2  Results

Across the 144-cell panel and the 27-cell legacy column, the lead author's
verdicts were:

| Model                              | Pass | Pass w/ notes | Needs revision | Cannot judge | Pass rate |
|------------------------------------|-----:|--------------:|---------------:|-------------:|----------:|
| Claude Sonnet 4.6                  | 24   | 0             | 0              | 0            | 100%      |
| Claude Opus 4.7                    | 24   | 0             | 0              | 0            | 100%      |
| GPT-5.5                            | 24   | 0             | 0              | 0            | 100%      |
| Gemini 2.5 Pro                     | 22   | 1             | 1              | 0            | 91.7%     |
| Nemotron 3 Super 120B (open)       | 21   | 0             | 2              | 1            | 87.5%     |
| Step-3.7 Flash (open)              | 19   | 0             | 5              | 0            | 79.2%     |
| Claude Opus 4 (2026-02-04 legacy)  | 24   | 0             | 0              | 0            | 100%      |

The frontier closed-weight models (Sonnet 4.6, Opus 4.7, GPT-5.5) passed
every prompt in our suite. Gemini 2.5 Pro passed 22 of 24, with one
"Pass with notes" flagging a response that was truncated mid-answer because
the model's effective output budget was exhausted before it reached the
final step of the requested chain-of-thought — a failure mode that would
have shipped silently to a researcher using the model conversationally
without verification. The two open-weight reasoning models had failure rates
of 8.3% and 20.8% respectively, with Step-3.7 Flash showing the most
distinctive pattern of failure on this suite.

Looking across the failures, several recurring failure modes surfaced:

- **Citation fabrication.** Nemotron cited "McMurdie & Holmes (2014) PLOS
  ONE" on a microbiome cross-validation prompt; the paper exists but in
  PLOS Computational Biology, not PLOS ONE. Step-3.7 Flash invented a
  *Faecalibacterium prausnitzii* / butyrate / r = 0.27 association on a
  reviewer-response prompt whose input notes did not contain that
  association. These are exactly the failure mode the repository's
  `guides/citation-warning.md` warns about, observed in our own evaluation.

- **Syntactically broken code.** Step-3.7 Flash produced R code containing
  `glm(..., family = negative.binomial())` on a cross-model-validation
  prompt; `negative.binomial()` is not a function in the standard R `stats`
  or `MASS` packages and the call would error at runtime.

- **Substantive cross-model disagreement on technical claims.** On a
  DESeq2 code-explanation prompt, Nemotron claimed that the `lfcThreshold`
  argument switches the statistical test to a likelihood ratio test; the
  other five panel models described it correctly as modifying the null
  hypothesis of the Wald test. The cross-model disagreement made the
  candidate error visible; verifying which side was right required
  reading the DESeq2 vignette.

- **Unprompted output structure.** Step-3.7 Flash on the meta-prompting
  prompt produced the requested critique and then appended an unrequested
  "Clarifying Questions" section. The prompt did not ask for clarifying
  questions; the addition reflects a model behavior pattern (apparent
  default to follow-up-question mode after a critique task) that a
  researcher pasting the output into a manuscript would have to manually
  excise.

The reviewer's machine-suggested triage drafts (auto-drafted by Claude
Opus 4.7 to speed the review, retained in
`evaluation/T4-audit-trail.json`) caught a substantial fraction of the
same failures the human reviewer flagged, but it also missed several —
the broken R syntax above, the wrong-journal citation, and the
specific-fabricated-correlation case all required a human reader to
catch with confidence. The audit trail shows where the machine triage
and the human verdict converged and where they diverged.

## 7.3  Cross-model disagreement as a useful signal

The empirical pattern in §7.2 is consistent with prior arguments
(Cohen 2023; Panickssery et al. 2024) that disagreement across a model
panel is itself information. Where five panel models agree on a substantive
claim and one diverges, the divergent answer warrants a closer human read.
In our suite, every cell that received a "Needs revision" verdict from the
human reviewer came from a model whose output substantively diverged from
the panel consensus on the same prompt; the converse is not always true
(divergence sometimes reflected stylistic difference rather than error)
but the heuristic was reliable enough to materially speed the human
verification pass. We do not advocate using model-panel agreement as a
substitute for verification — the four 100%-pass models could in principle
all share a hallucination, and a single human review could still miss
silent errors — but as a *triage* tool that surfaces cells worth closer
scrutiny, the panel approach worked.

## 7.4  Limitations and caveats

We surface five limitations explicitly:

1. **Single reviewer.** The 171 verdicts in this evaluation were set by
   one author (TJS). Inter-rater agreement metrics (Cohen's kappa, etc.)
   require a second independent reviewer and are not reported here. The
   repository's reviewing infrastructure (`docs/`, `tools/merge_verdicts.py`,
   `.github/workflows/verdict-review.yml`) supports multi-reviewer runs and
   computes pairwise kappa automatically; future iterations of this
   evaluation should include at least one additional reviewer per cell.

2. **24 prompts is not exhaustive.** Failure-mode patterns observed here
   may not generalize to prompts outside the suite. The 24 prompts were
   curated for life-science use cases the authors and collaborators
   actually encounter; we make no claim about prompts for other domains.

3. **Pinned model versions.** All results are tied to specific model IDs
   pinned in `harness/models.yaml` on the recorded dates. Model providers
   ship updates that change behavior; results may shift on re-test.

4. **Reasoning-model deviations from T=0.0.** As described in §7.1, four
   of six panel models did not honor the requested temperature. Their
   outputs are not directly comparable, on the temperature axis, to the
   two models that did. We did not re-test those four models at their
   forced internal defaults vs. an explicit different setting; doing so
   would require provider-side configurability we do not have for some of
   the panel.

5. **Machine-suggested triage influenced the human reviewer.** The
   review SPA displayed Claude Opus 4.7-drafted UNCONFIRMED triage above
   the verdict buttons on each cell. The reviewer was instructed (and the
   triage labeled) to treat these as triage, not endorsements, and to read
   the raw output independently. There is no controlled measurement of
   whether the triage drafts biased verdicts toward Pass on cells they
   suggested Pass for. The drafts were left in the audit trail for
   transparency; future iterations should consider a triage-blind reviewer
   condition.
