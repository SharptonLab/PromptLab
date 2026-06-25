# Reviewer verdict files

Each file in this directory is one reviewer's verdict file from the T4 review
of PromptLab's cross-model panel. Files are named `<reviewer>-verdicts.json`.

These are research artifacts — they're the immutable record of who voted what
on which (prompt, model) cell. Don't edit them by hand after they're committed.

## How files get here

**Reviewer-initiated pull requests:** a reviewer opens the static review page
at https://sharptonlab.github.io/PromptLab/docs/, marks verdicts, downloads their
verdict file, then opens a PR adding it to this directory. A GitHub Action
runs `tools/merge_verdicts.py` on every such PR and posts the agreement
report (pairwise Cohen's kappa + disagreement list) as a PR comment.

**PI-initiated commits:** if a reviewer emails their verdict file instead, the
PI can drop it here directly. The same merge produces the same agreement
report.

## Combining them

```bash
python3 tools/merge_verdicts.py verdicts/*.json --policy majority
```

Produces `T4-canonical-verdicts.json`, `T4-audit-trail.json`, and
`T4-agreement-report.md` in the current directory.

See `tools/PI.md` for the full lead-reviewer workflow.
