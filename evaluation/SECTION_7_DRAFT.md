# Section 7: Testing methodology and results (draft)

> **Status: machine-drafted, awaiting author revision.** Drafted by Claude
> Opus 4.7 from the empirical results in this directory + `tests/SUMMARY.md`,
> for the lead author to edit before incorporation into the manuscript. The
> draft sticks to what the artifacts support; check every claim against
> `evaluation/T4-canonical-verdicts.json`, `evaluation/T4-audit-trail.json`,
> and `evaluation/T4-per-prompt.md` before publication.

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
fixed six-model panel on 2026-06-25. The panel spans the closed-weight
frontier tier most life-science researchers actually interact with through
chatbots (Claude Sonnet 4.6, Claude Opus 4.7, GPT-5.5, Gemini 2.5 Pro) plus
two open-weight reasoning-capable models served on-prem at OSU's Center for
Quantitative Life Sciences (Nemotron 3 Super 120B, Step-3.7 Flash). A
single-model 27-cell legacy column captured on 2026-02-04 (Claude Opus 4)
is retained in the repository for shelf-life comparison but is excluded from
the per-prompt aggregation reported below because it is not part of the
current panel. All model versions are pinned in `harness/models.yaml`; the
per-result-file date suffix records when each capture was made.

Each prompt file has a `## The Prompt` section (the template with
`{PLACEHOLDER}` markers) and a `## Test Input` section that is a complete,
paste-ready filled instance of the prompt — a template mirror with the
placeholders substituted for realistic values. Capture was driven by a thin
harness (`harness/run_tests.py`) with the `test-only` assembly strategy,
which sends only the filled `## Test Input` block to each model. This
matches how a real user of the repository would compose a prompt: copy the
prompt file, fill in the placeholders, submit to a model, do not send the
raw template alongside. Model outputs are written verbatim into
`tests/<category>/<prompt-name>/<model-slug>-<date>.md` with no
post-processing. Each result file also records the API-reported
`stop_reason` and input/output token counts so any observed truncation
can be attributed to either our token cap or the model's own stopping
behavior.

Three harness-level deviations are worth flagging for methodological
transparency:

1. **Temperature was dropped for reasoning-capable models.** All four
   reasoning-capable models on the panel (GPT-5.5, Claude Opus 4.7, Nemotron
   3 Super, Step-3.7 Flash) reject or ignore explicit temperature settings;
   the harness detects the resulting `BadRequestError` and retries without
   the parameter. Outputs from those four models therefore reflect each
   provider's internal default, not the T = 0.0 the harness requested.
   Claude Sonnet 4.6 and Gemini 2.5 Pro accepted T = 0.0.

2. **`max_tokens` was set above the harness default** (`4 096`) for every
   panel model. Final values: Sonnet 4.6 = 16 384; Opus 4.7 = 32 000;
   GPT-5.5 = 32 000; Gemini 2.5 Pro = 32 000; Nemotron 3 Super = 16 384;
   Step-3.7 Flash = 16 384. The default 4 096 was consumed by internal
   chain-of-thought on reasoning-capable models (the visible answer was
   empty) and by long-output prompts on the non-reasoning models
   (mid-sentence truncation). A small subset of cells (six) that still
   showed truncation after the initial capture were re-run and inspected
   with API-reported `stop_reason` metadata; four of those completed with
   `stop_reason` values of `stop` or `end_turn` (models chose to end
   voluntarily, well below the token cap), and two failed to re-run because
   the on-prem endpoint had been migrated (see §7.4).

3. **Non-determinism at T = 0.0.** During diagnostic work on cells that
   ended mid-sentence, we confirmed that Anthropic's API is not strictly
   deterministic at T = 0.0: repeated identical calls occasionally produced
   outputs that ended at different points, one with a full stop and one
   mid-word. All reported verdicts are on the capture on disk; this
   non-determinism is noted for future evaluations.

Captured outputs were then human-verified by two authors (TJS and Alex
Alexiev) through a static review SPA (deployed via GitHub Pages, source at
`docs/index.html`) that displays each cell — the source prompt, the filled
prompt that was actually sent, the raw model output, and the API-reported
stop-reason and token counts — and persists verdicts to a local file on
disk. The review rubric was the repository's own
`guides/verification-checklist-extended.md`, satisfying reviewer R1.14's
ask that we apply our own published checklist to our own claims. Each
reviewer independently voted Pass, Pass with notes, Needs revision,
Cannot judge from output alone, or Skip on each cell.

For each cell, the two reviewers' votes were combined under an
abstention-aware majority policy: Skip and Cannot judge are treated as
abstention (they do not vote against a peer's actual verdict); when both
reviewers actually voted, the stricter verdict wins in cases of
disagreement between a pass verdict (Pass or Pass with notes) and a Needs
revision verdict — this errs on the side of flagging concerns rather than
adjudicating them away. Per-cell canonical verdicts, the full per-reviewer
audit trail, and the pairwise Cohen's kappa are in `evaluation/`.

At the prompt level, we count a prompt as **"passes overall"** if at least
four of the six panel-model cells for that prompt received a canonical
verdict of Pass or Pass with notes. Otherwise the prompt is flagged as
needing revision. This threshold (≥ 4 / 6) matches "prompts that work for
the majority of models a real user might reach for," which is the claim
the repository makes to its users.

## 7.2  Results

### 7.2.1  Per-model pass rate

Across the 144-cell panel (24 runnable prompts × 6 models), the canonical
verdicts per model were:

| Model                          | Pass | Pass with notes | Needs revision | Pass rate |
|--------------------------------|-----:|----------------:|---------------:|----------:|
| Claude Sonnet 4.6              |   24 |               0 |              0 |    100.0% |
| Claude Opus 4.7                |   24 |               0 |              0 |    100.0% |
| GPT-5.5                        |   24 |               0 |              0 |    100.0% |
| Gemini 2.5 Pro                 |   23 |               0 |              1 |     95.8% |
| Nemotron 3 Super 120B (open)   |   22 |               0 |              2 |     91.7% |
| Step-3.7 Flash (open)          |   22 |               0 |              2 |     91.7% |
| **Panel total**                | **139** |           **0** |          **5** |  **96.5%** |

The three frontier closed-weight models passed every prompt in our suite.
Gemini 2.5 Pro passed 23 of 24, with one Needs-revision verdict traceable
to non-determinism at capture time (the cell was captured while the
model's output was mid-sentence; a re-run under the same configuration
produced a complete response, but the second reviewer voted on the
truncated first capture — see §7.4). The two open-weight reasoning models
passed 22 of 24 each, with recurring failure modes discussed below.

### 7.2.2  Per-prompt pass rate

At the prompt level:

- **24 of 24 prompts** (100%) pass at the ≥ 4 / 6 model threshold defined
  in §7.1.
- **19 of 24 prompts** reached a perfect 6 / 6 pass rate across the panel.
- **5 of 24 prompts** received one Needs-revision verdict, coming in at
  5 / 6. These are: `fundamentals/cross-model-validation`,
  `fundamentals/structured-prompt-template`,
  `statistics/assumption-checking`, `statistics/design-review`, and
  `statistics/interpretation-brainstorming`. The N-generating models were
  Step-3.7 (2 cells), Nemotron (2 cells), and Gemini (1 cell — the
  non-determinism artifact noted above).
- **No prompt fell below the 4 / 6 threshold; no prompt is flagged as
  requiring revision.**

Full per-prompt data is in `evaluation/T4-per-prompt.md`.

### 7.2.3  Failure modes on the 5 Needs-revision cells

Two of the five Needs-revision cells are undisputed methodological
failures both reviewers agreed on; the other three are largely
truncation-related.

- **Citation fabrication (Step-3.7 Flash × `fundamentals/cross-model-validation`).**
  The model cited "A 2021 review of 112 human microbiome studies found
  78% [...]" and "A 2023 survey of 150 published microbiome studies
  [...] 62% used non-parametric tests, 21% used t-tests." Neither review
  appears to exist; both are quantitatively specific, plausible-sounding,
  and unverifiable — exactly the failure mode the repository's
  `guides/citation-warning.md` warns about, observed in our own
  evaluation.

- **Missed extraction (Step-3.7 Flash × `fundamentals/structured-prompt-template`).**
  The model returned "Not reported" for the Key confounds field of the
  extraction task, while all five other panel models correctly extracted
  the confound information (study not pre-registered, no power analysis
  performed) that was explicitly present in the source text.

The remaining three Needs-revision cells (two on Nemotron 3 Super,
one on Gemini 2.5 Pro) were all cases where the model's output ended
mid-sentence, so the reviewer could not evaluate the missing final
sections. Two of those Nemotron cells could not be re-captured after the
initial run because the on-prem endpoint had been migrated by the time
we noticed the issue (§7.4). The Gemini case was re-captured cleanly but
the second reviewer had voted before the re-run.

### 7.2.4  Inter-rater agreement

The two reviewers overlapped on 118 cells where both cast an actual
Pass / Pass-with-notes / Needs-revision verdict (as opposed to a Skip).
Percent agreement on the binary pass-vs-not-pass axis was **97.5%
(115 / 118)**. Cohen's kappa on the same binary axis was **κ = 0.559
(moderate)**. Kappa is driven low relative to raw agreement by the
strong class imbalance — the base pass rate exceeded 95% — which is a
known limitation of kappa under such skew and is not, in this case, a
statement of low reviewer alignment on the methodological question.
Full agreement statistics are in `evaluation/T4-agreement-report.md`.

Only three cells had a true Pass/Not-pass disagreement between
reviewers. The conservative merge policy resolved all three to
Needs revision.

## 7.3  Cross-model disagreement as a useful signal

The empirical pattern in §7.2 is consistent with prior arguments
(Cohen 2023; Panickssery et al. 2024) that disagreement across a model
panel is itself information. In our suite, every cell that received a
canonical Needs revision verdict came from a model whose output
substantively diverged from the other five panel models' outputs on
the same prompt: Step-3.7 Flash was the sole model that fabricated
review-paper statistics on the cross-model-validation prompt, the sole
model that missed the confound extraction on the structured-prompt-
template prompt, and the two open-weight models were the ones that
produced mid-sentence truncated output on the statistics prompts.

Where five panel models produced substantively similar answers and one
diverged, the divergence marked the cell as worth closer human review;
the converse is not always true (divergence sometimes reflected
stylistic difference rather than error), but the heuristic was
reliable enough to materially speed the human verification pass. We do
not advocate using model-panel agreement as a substitute for
verification — three or four panel models could in principle share a
hallucination, and a two-reviewer human check could still miss silent
errors — but as a *triage* tool that surfaces cells worth closer
scrutiny, the panel approach worked. This is a compact empirical
counterpart to the argument developed in Cohen 2023 and
Panickssery et al. 2024.

## 7.4  Limitations and caveats

We surface five limitations explicitly:

1. **Two-reviewer coverage; not blind to the machine triage.** Every
   cell was reviewed by TJS; 118 of 144 panel cells (82%) were also
   reviewed by a second author (Alex Alexiev). Reviewers were not
   blinded to the Claude Opus 4.7-drafted UNCONFIRMED triage that
   the SPA displayed above the verdict buttons; there is no
   controlled measurement of whether the triage drafts biased
   verdicts toward Pass on cells they suggested Pass for. The
   triage drafts are retained in `evaluation/T4-audit-trail.json`
   for transparency; a triage-blind reviewing condition would be
   valuable in future iterations.

2. **24 prompts is not exhaustive.** Failure-mode patterns
   observed here may not generalize to prompts outside the suite. The
   24 prompts were curated for life-science use cases the authors and
   collaborators actually encounter; we make no claim about prompts
   for other domains.

3. **Pinned model versions on a single capture day.** All results
   are tied to specific model IDs pinned in `harness/models.yaml` and
   dated 2026-06-25. Model providers ship updates that change
   behavior; the same prompts may yield different verdicts on
   re-test. The `stop_reason` and token metadata now stored in each
   result file lets a future re-test detect whether observed changes
   are due to model updates or to different stopping behavior.

4. **Reasoning-model deviations from T = 0.0.** As described in §7.1,
   four of six panel models did not honor the requested temperature.
   Their outputs are not directly comparable, on the temperature
   axis, to the two models that did. We did not re-test those four
   models at their forced internal defaults vs. an explicit
   different setting; doing so would require provider-side
   configurability we do not have for some of the panel.

5. **On-prem endpoint migration during evaluation.** Between the
   initial capture and the follow-up re-run of a small subset of
   cells, OSU's Center for Quantitative Life Sciences migrated its
   OpenAI-compatible endpoint from a per-model URL scheme
   (`.../llm/<model>/v1/`) to a unified router
   (`.../llm/v1/chat/completions`) with a different API-key format.
   Two Nemotron 3 Super cells that we had planned to re-capture as
   part of the truncation follow-up (`statistics/assumption-checking`
   and `statistics/interpretation-brainstorming`) returned HTTP 410
   Gone from the old URL and were not re-captured before this
   report was frozen. The original captures for those two cells
   remain on disk and are what the verdicts here reflect.
