# AI Disclosure paragraph (draft)

> **Status: machine-drafted, awaiting author revision.** Drop in wherever
> your venue requires an AI-use disclosure. Edit to match the venue's
> expected verbs (e.g. some require "the authors used X to do Y", others
> prefer passive voice). The factual content should not change.

---

## For the manuscript

Large language models were used during the preparation and evaluation of
this work as tools, not as authors. Specifically: (i) Claude Opus 4.7 and
Claude Code (Anthropic) were used to extend and reorganize the
companion code repository (PromptLab), to author the cross-model test
harness (`harness/`), and to draft machine-suggested triage notes that the
lead author then independently verified against raw model output;
(ii) Claude Sonnet 4.6, Claude Opus 4.7, GPT-5.5, Gemini 2.5 Pro, NVIDIA
Nemotron 3 Super 120B, and StepFun Step-3.7 Flash were the system-under-
test — they generated the LLM responses we then evaluated. Pinned model
identifiers and capture dates are recorded in `harness/models.yaml` and in
each per-cell result file under `tests/`. All test outputs were captured
verbatim and persist unedited in the repository. Every verdict ("Pass",
"Pass with notes", "Needs revision", "Cannot judge from output alone") was
set by a human reviewer (the lead author) against the rubric in
`guides/verification-checklist-extended.md`. The machine-suggested triage
drafts are retained in `evaluation/T4-audit-trail.json` for full
provenance; they did not set any verdict.

---

## For the repository README footer (shorter)

This repository's testing pass was assisted by Claude Opus 4.7 (Anthropic),
which drafted UNCONFIRMED machine triage notes that the lead author then
verified independently. All verdicts shown in `tests/SUMMARY.md` and in
each prompt's `## Model Notes` section were set by a human reviewer; the
machine triage is in `evaluation/T4-audit-trail.json` for provenance.
