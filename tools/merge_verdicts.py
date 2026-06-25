#!/usr/bin/env python3
"""
Combine multiple reviewer verdicts files into canonical verdicts + an
agreement report.

Inputs: one or more JSON files, in either format we support:
  - SPA format:    {"schema": "promptlab-t4-verdicts/v1",
                    "reviewer": "tom-sharpton",
                    "started": "...",
                    "verdicts": {"<cell-key>": {"verdict": "P", ...}}}
  - Local server:  {"<cell-key>": {"verdict": "P", "notes": "...", "ts": "..."}}
                   (no reviewer field — pass --reviewer-for=FILE=NAME to set one)

Default policy: majority. With three reviewers, 2-of-3 wins; ties leave the cell
as DISAGREEMENT (canonical verdict not set; goes to manual resolution).

Outputs (next to the inputs, into --out-dir):
  T4-canonical-verdicts.json   — one verdict per cell after policy
  T4-audit-trail.json          — every reviewer's vote on every cell, preserved
  T4-agreement-report.md       — pairwise Cohen's kappa + disagreement list

Run:
    python3 tools/merge_verdicts.py verdicts/*.json
    python3 tools/merge_verdicts.py verdicts/tom.json verdicts/ed.json \\
        --policy majority --out-dir .
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

POLICIES = ("majority", "unanimity", "lead-reviewer")
VERDICT_VALUES = ("P", "PN", "N", "?", "S", "")


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def load_file(path: Path, reviewer_override: str | None = None) -> tuple[str, dict[str, dict]]:
    """
    Returns (reviewer_name, {cell_key: {verdict, notes, ts}}).
    Handles both SPA format and the local-server flat format.
    """
    text = path.read_text(encoding="utf-8")
    data = json.loads(text)
    # SPA shape?
    if isinstance(data, dict) and data.get("schema", "").startswith("promptlab-t4-verdicts"):
        reviewer = reviewer_override or data.get("reviewer") or path.stem
        verdicts = data.get("verdicts", {}) or {}
        return reviewer, verdicts
    # Local-server flat shape?
    if isinstance(data, dict) and all(
        isinstance(v, dict) and "verdict" in v for v in data.values() if v is not None
    ):
        reviewer = reviewer_override or path.stem
        return reviewer, data
    raise ValueError(f"{path}: unrecognized verdicts format")


def parse_overrides(specs: Iterable[str]) -> dict[str, str]:
    """--reviewer-for=tom.json=tom-sharpton -> {'tom.json': 'tom-sharpton'}"""
    out = {}
    for s in specs:
        if "=" not in s:
            raise SystemExit(f"--reviewer-for must be FILE=NAME, got: {s}")
        fname, name = s.split("=", 1)
        out[fname] = name
    return out


# ---------------------------------------------------------------------------
# Policy application
# ---------------------------------------------------------------------------

def apply_policy(votes: list[tuple[str, str]], policy: str,
                 lead: str | None = None) -> tuple[str | None, str]:
    """
    votes: [(reviewer, verdict), ...]
    Returns (canonical_verdict_or_None, reason_string).
    A None canonical means the cell stays PENDING (goes to manual resolution).
    """
    verdicts_only = [v for _, v in votes if v]
    if not verdicts_only:
        return None, "no votes"

    if policy == "majority":
        counter = Counter(verdicts_only)
        ((top_v, top_n),) = counter.most_common(1)
        if top_n > len(verdicts_only) / 2:
            return top_v, f"majority {top_n}/{len(verdicts_only)}"
        # tie / no majority
        return None, f"no majority among {dict(counter)}"

    if policy == "unanimity":
        if len(set(verdicts_only)) == 1:
            return verdicts_only[0], f"unanimous {len(verdicts_only)}"
        return None, f"split: {Counter(verdicts_only)}"

    if policy == "lead-reviewer":
        if not lead:
            raise SystemExit("--policy=lead-reviewer requires --lead=NAME")
        for r, v in votes:
            if r == lead and v:
                return v, f"lead ({lead})"
        return None, f"lead reviewer {lead} did not vote"

    raise SystemExit(f"unknown policy: {policy}")


# ---------------------------------------------------------------------------
# Agreement metrics
# ---------------------------------------------------------------------------

def cohens_kappa(votes_a: dict[str, str], votes_b: dict[str, str]) -> tuple[float, int]:
    """
    Cohen's kappa for two raters on categorical labels. Computed over the
    cells they both voted on (excluding "" / unrated).
    Returns (kappa, n_overlap).
    """
    overlap = [(votes_a[k], votes_b[k]) for k in votes_a
               if k in votes_b and votes_a[k] and votes_b[k]]
    n = len(overlap)
    if n == 0:
        return float("nan"), 0
    # observed agreement
    po = sum(1 for a, b in overlap if a == b) / n
    # expected agreement under independence
    cat_a = Counter(a for a, _ in overlap)
    cat_b = Counter(b for _, b in overlap)
    cats = set(cat_a) | set(cat_b)
    pe = sum((cat_a.get(c, 0) / n) * (cat_b.get(c, 0) / n) for c in cats)
    if pe == 1.0:
        return 1.0 if po == 1.0 else 0.0, n
    return (po - pe) / (1 - pe), n


def interpret_kappa(k: float) -> str:
    if k != k:  # NaN
        return "N/A"
    if k < 0:    return "worse than chance"
    if k < 0.20: return "slight"
    if k < 0.40: return "fair"
    if k < 0.60: return "moderate"
    if k < 0.80: return "substantial"
    return "almost perfect"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+", help="reviewer verdict JSON files")
    ap.add_argument("--policy", choices=POLICIES, default="majority")
    ap.add_argument("--lead", help="lead reviewer name (required for lead-reviewer policy)")
    ap.add_argument("--reviewer-for", action="append", default=[],
                    metavar="FILE=NAME",
                    help="assign reviewer name to a file lacking one "
                         "(repeatable). Useful for the local-server format.")
    ap.add_argument("--out-dir", default=".", type=Path,
                    help="where to write the three output files (default: cwd)")
    args = ap.parse_args()

    overrides = parse_overrides(args.reviewer_for)
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    # ---- 1. Load all files, indexed by reviewer ----
    by_reviewer: dict[str, dict[str, dict]] = {}
    for f in args.files:
        path = Path(f)
        override = overrides.get(path.name)
        reviewer, verdicts = load_file(path, override)
        if reviewer in by_reviewer:
            # Merge later-timestamped entries
            for k, entry in verdicts.items():
                existing = by_reviewer[reviewer].get(k)
                if not existing or entry.get("ts", "") > existing.get("ts", ""):
                    by_reviewer[reviewer][k] = entry
        else:
            by_reviewer[reviewer] = dict(verdicts)
        print(f"  loaded {path}: reviewer='{reviewer}', {len(verdicts)} verdict(s)",
              file=sys.stderr)

    if not by_reviewer:
        raise SystemExit("no verdicts loaded")

    # ---- 2. Build per-cell vote map ----
    cell_votes: dict[str, list[dict]] = defaultdict(list)
    for reviewer, vs in by_reviewer.items():
        for cell_key, entry in vs.items():
            verdict = entry.get("verdict", "")
            cell_votes[cell_key].append({
                "reviewer": reviewer,
                "verdict": verdict,
                "notes": entry.get("notes", ""),
                "ts": entry.get("ts", ""),
            })

    # ---- 3. Apply policy → canonical ----
    canonical: dict[str, dict] = {}
    disagreements: list[dict] = []
    for cell_key, votes in cell_votes.items():
        # filter empty verdicts (e.g. notes-only updates) for policy calc
        scored = [(v["reviewer"], v["verdict"]) for v in votes if v["verdict"]]
        verdict, reason = apply_policy(scored, args.policy, args.lead)
        if verdict is None:
            # disagreement OR no votes — leave canonical PENDING
            disagreements.append({
                "cell": cell_key,
                "reason": reason,
                "votes": votes,
            })
        else:
            canonical[cell_key] = {
                "verdict": verdict,
                "reason": reason,
                "votes": votes,
            }

    # ---- 4. Pairwise Cohen's kappa ----
    reviewers = sorted(by_reviewer.keys())
    kappa_table = {}
    for i, r1 in enumerate(reviewers):
        for r2 in reviewers[i + 1:]:
            vs1 = {k: e["verdict"] for k, e in by_reviewer[r1].items()
                   if e.get("verdict")}
            vs2 = {k: e["verdict"] for k, e in by_reviewer[r2].items()
                   if e.get("verdict")}
            k, n = cohens_kappa(vs1, vs2)
            kappa_table[(r1, r2)] = (k, n)

    # ---- 5. Per-reviewer stats ----
    per_reviewer_stats = {}
    for r in reviewers:
        verdicts = [e.get("verdict", "") for e in by_reviewer[r].values()]
        c = Counter(v for v in verdicts if v)
        per_reviewer_stats[r] = {"total": sum(c.values()), "by_verdict": dict(c)}

    # ---- 6. Write outputs ----

    canonical_out = out_dir / "T4-canonical-verdicts.json"
    canonical_out.write_text(json.dumps({
        "schema": "promptlab-t4-canonical/v1",
        "policy": args.policy,
        "lead": args.lead,
        "reviewers": reviewers,
        "canonical": canonical,
        "disagreements_count": len(disagreements),
    }, indent=2, sort_keys=True))

    audit_out = out_dir / "T4-audit-trail.json"
    audit_out.write_text(json.dumps({
        "schema": "promptlab-t4-audit/v1",
        "reviewers": reviewers,
        "cell_votes": cell_votes,
    }, indent=2, sort_keys=True, default=list))

    # ---- 7. Markdown agreement report ----
    lines = [
        "# T4 Agreement Report",
        "",
        f"- **Policy:** `{args.policy}`" + (f" (lead: {args.lead})" if args.lead else ""),
        f"- **Reviewers:** {', '.join(reviewers)}",
        f"- **Cells with at least one vote:** {len(cell_votes)}",
        f"- **Canonical verdicts set:** {len(canonical)}",
        f"- **Unresolved (disagreements / no majority):** {len(disagreements)}",
        "",
        "## Per-reviewer activity",
        "",
        "| Reviewer | Total votes | P | PN | N | ? | S |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for r in reviewers:
        s = per_reviewer_stats[r]
        c = s["by_verdict"]
        lines.append(f"| {r} | {s['total']} | {c.get('P',0)} | {c.get('PN',0)} "
                     f"| {c.get('N',0)} | {c.get('?',0)} | {c.get('S',0)} |")
    lines.append("")

    if len(reviewers) >= 2:
        lines += [
            "## Pairwise agreement (Cohen's kappa, over overlap only)",
            "",
            "| Reviewer A | Reviewer B | κ | n overlap | Interpretation |",
            "|---|---|---:|---:|---|",
        ]
        for (r1, r2), (k, n) in kappa_table.items():
            k_str = f"{k:.3f}" if k == k else "N/A"
            lines.append(f"| {r1} | {r2} | {k_str} | {n} | {interpret_kappa(k)} |")
        lines.append("")
        lines.append("> Landis & Koch interpretation bands: <0 worse than chance · "
                     "0–0.20 slight · 0.20–0.40 fair · 0.40–0.60 moderate · "
                     "0.60–0.80 substantial · 0.80–1 almost perfect.")
        lines.append("")

    if disagreements:
        lines += [
            f"## Disagreements / unresolved ({len(disagreements)} cell(s))",
            "",
            "Each of these stayed PENDING because the policy didn't produce a "
            "single verdict. Resolve by re-reading the model output, discussing "
            "with the disagreeing reviewer(s), and writing a final verdict by "
            "hand to the canonical file (or splitting the cell with `?`).",
            "",
        ]
        for d in sorted(disagreements, key=lambda x: x["cell"]):
            lines.append(f"### `{d['cell']}`")
            lines.append("")
            lines.append(f"_Reason: {d['reason']}_")
            lines.append("")
            for v in d["votes"]:
                vd = v["verdict"] or "(no verdict)"
                lines.append(f"- **{v['reviewer']}** → `{vd}`"
                             + (f" — {v['notes']}" if v.get("notes") else ""))
            lines.append("")

    report_out = out_dir / "T4-agreement-report.md"
    report_out.write_text("\n".join(lines), encoding="utf-8")

    # ---- 8. Stderr summary ----
    print(file=sys.stderr)
    print(f"  wrote {canonical_out}", file=sys.stderr)
    print(f"  wrote {audit_out}", file=sys.stderr)
    print(f"  wrote {report_out}", file=sys.stderr)
    print(f"  canonical: {len(canonical)} cells | disagreements: {len(disagreements)} cells",
          file=sys.stderr)


if __name__ == "__main__":
    main()
