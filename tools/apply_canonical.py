#!/usr/bin/env python3
"""
Apply a T4-canonical-verdicts.json file to the per-result-file Recommendation
fields under tests/. Reviewer notes (and attribution) are written into the
Notes field of each file's ## Overall Assessment section.

Run after producing the canonical with tools/merge_verdicts.py:

    python3 tools/apply_canonical.py T4-canonical-verdicts.json
    python3 tools/apply_canonical.py T4-canonical-verdicts.json --dry-run

By default, refuses to overwrite a file whose Recommendation line isn't the
PENDING AUTHOR REVIEW default (assumes you've already applied verdicts or
edited it by hand). Pass --force to override.

What this script touches:
  - "- **Recommendation:** PENDING AUTHOR REVIEW" → "- **Recommendation:** <mapped>"
  - "- **Notes:**" → "- **Notes:** <reviewer attribution + any reviewer-supplied notes>"

What it leaves alone:
  - ## Model Output (raw model output, never touched per CLAUDE.md rule #2)
  - ## Assessment (machine-suggested triage, kept as historical context)
  - Test Metadata, Filled Prompt, etc.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PENDING = "PENDING AUTHOR REVIEW"

# Map SPA shortcode verdicts to the words that appear in Recommendation:
VERDICT_DISPLAY = {
    "P":  "Pass",
    "PN": "Pass with notes",
    "N":  "Needs revision",
    "?":  "Cannot judge from output alone",
    "S":  "Skip",
}


def cell_key_to_path(key: str) -> Path:
    """code/python-analysis/claude-sonnet-4-6-2026-06-23 → tests/code/python-analysis/claude-sonnet-4-6-2026-06-23.md"""
    return REPO_ROOT / "tests" / f"{key}.md"


def format_notes(votes: list[dict]) -> str:
    """Build the Notes field body from one or more reviewer votes.

    Only reviewers who supplied substantive notes contribute. Pure attribution
    is noise — the full audit trail lives in evaluation/T4-audit-trail.json,
    so per-file Notes only carry real reviewer-written content.
    """
    parts = []
    for v in votes:
        note = (v.get("notes") or "").strip()
        if not note:
            continue
        reviewer = v.get("reviewer", "unknown")
        ts = v.get("ts", "")
        date = ts[:10] if ts else ""
        head = f"{reviewer}" + (f" ({date})" if date else "")
        parts.append(f"{head}: {note}")
    return " · ".join(parts)


def apply_to_file(path: Path, verdict: str, notes_body: str, *, dry_run: bool, force: bool) -> str:
    """Returns one of: 'updated', 'unchanged', 'skipped-not-pending', 'missing-fields', 'no-file'."""
    if not path.exists():
        return "no-file"
    text = path.read_text(encoding="utf-8")

    rec_line_re = re.compile(r"^- \*\*Recommendation:\*\* (.+?)$", re.MULTILINE)
    notes_line_re = re.compile(r"^- \*\*Notes:\*\*(.*)$", re.MULTILINE)

    rec_match = rec_line_re.search(text)
    notes_match = notes_line_re.search(text)
    if not (rec_match and notes_match):
        return "missing-fields"

    current_rec = rec_match.group(1).strip()
    if current_rec != PENDING and not force:
        return "skipped-not-pending"

    new_text = rec_line_re.sub(f"- **Recommendation:** {verdict}", text, count=1)
    new_notes_line = f"- **Notes:** {notes_body}" if notes_body else "- **Notes:**"
    new_text = notes_line_re.sub(new_notes_line, new_text, count=1)

    if new_text == text:
        return "unchanged"

    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return "updated"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("canonical", type=Path,
                    help="Path to T4-canonical-verdicts.json from merge_verdicts.py")
    ap.add_argument("--dry-run", action="store_true",
                    help="Show what would change without writing")
    ap.add_argument("--force", action="store_true",
                    help="Overwrite even if the Recommendation line isn't PENDING")
    args = ap.parse_args()

    data = json.loads(args.canonical.read_text(encoding="utf-8"))
    if data.get("schema", "").startswith("promptlab-t4-canonical"):
        canonical = data["canonical"]
    else:
        # Tolerate a flat "{cell: {verdict, ...}}" shape just in case.
        canonical = data

    counts = {"updated": 0, "unchanged": 0, "skipped-not-pending": 0,
              "missing-fields": 0, "no-file": 0, "unknown-verdict": 0}
    issues: list[tuple[str, str]] = []

    for cell_key, entry in canonical.items():
        verdict_code = entry.get("verdict", "")
        if verdict_code not in VERDICT_DISPLAY:
            counts["unknown-verdict"] += 1
            issues.append((cell_key, f"unknown verdict code: {verdict_code!r}"))
            continue
        verdict_display = VERDICT_DISPLAY[verdict_code]
        notes_body = format_notes(entry.get("votes") or [])

        path = cell_key_to_path(cell_key)
        outcome = apply_to_file(path, verdict_display, notes_body,
                                dry_run=args.dry_run, force=args.force)
        counts[outcome] += 1
        if outcome in ("skipped-not-pending", "missing-fields", "no-file"):
            issues.append((cell_key, outcome))

    print(f"\n{'DRY-RUN ' if args.dry_run else ''}Applied {counts['updated']} verdict(s) across {len(canonical)} canonical cells.")
    for k in ("unchanged", "skipped-not-pending", "missing-fields",
              "no-file", "unknown-verdict"):
        if counts[k]:
            print(f"  {counts[k]:4d}  {k}")
    if issues:
        print(f"\nIssues ({len(issues)}):")
        for k, why in issues[:25]:
            print(f"  {k}  →  {why}")
        if len(issues) > 25:
            print(f"  ... and {len(issues) - 25} more")
        sys.exit(1 if counts["updated"] == 0 else 0)


if __name__ == "__main__":
    main()
