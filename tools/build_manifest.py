#!/usr/bin/env python3
"""
Generate docs/cells-manifest.json — the list of (prompt, model) review cells
the static SPA at docs/index.html will load.

Run from the repo root (or anywhere; paths are computed from this file's location):

    python3 tools/build_manifest.py

Re-run any time the contents of tests/ change.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TESTS_DIR = REPO_ROOT / "tests"
OUT = REPO_ROOT / "docs" / "cells-manifest.json"

# Categories that contain runnable task prompts. documentation/ holds templates
# that have old-pipeline result files but no source prompt in the task dirs.
PROMPT_CATEGORIES = ["code", "fundamentals", "literature", "statistics",
                     "validation", "writing", "documentation"]

# Display order for models within a prompt section (used for stable sort).
MODEL_DISPLAY_ORDER = [
    ("claude-sonnet-4-6",       "claude-sonnet-4.6"),
    ("claude-opus-4-7",         "claude-opus-4.7"),
    ("gpt-5-5",                 "gpt-5.5"),
    ("gemini-2-5-pro",          "gemini-2.5-pro"),
    ("nemotron-3-super-120b",   "nemotron-3-super-120b"),
    ("step-3-7-flash",          "step-3.7-flash"),
    ("claude-opus-4",           "claude-opus-4 (2026-02-04 legacy)"),
]


def model_index_and_display(model_key: str) -> tuple[int, str]:
    for i, (prefix, display) in enumerate(MODEL_DISPLAY_ORDER):
        if model_key.startswith(prefix):
            return (i, display)
    return (999, model_key)


def discover_cells() -> list[dict]:
    cells: list[dict] = []
    for cat in PROMPT_CATEGORIES:
        cat_dir = TESTS_DIR / cat
        if not cat_dir.is_dir():
            continue
        for prompt_dir in sorted(cat_dir.iterdir()):
            if not prompt_dir.is_dir():
                continue
            slug = prompt_dir.name
            prompt_src = REPO_ROOT / cat / f"{slug}.md"
            prompt_url = f"{cat}/{slug}.md" if prompt_src.exists() else None
            for result_file in sorted(prompt_dir.glob("*.md")):
                model_key = result_file.stem  # e.g. "claude-sonnet-4-6-2026-06-23"
                idx, display = model_index_and_display(model_key)
                # date suffix: trailing -YYYY-MM-DD if present
                date = ""
                if len(model_key) >= 10 and model_key[-10] == "-" \
                        and model_key[-10:][1:5].isdigit():
                    date = model_key[-10:][1:]
                cells.append({
                    "key": f"{cat}/{slug}/{model_key}",
                    "category": cat,
                    "slug": slug,
                    "model_key": model_key,
                    "model_display": display,
                    "model_sort_index": idx,
                    "date": date,
                    "result_url": f"tests/{cat}/{slug}/{model_key}.md",
                    "prompt_url": prompt_url,
                })
    # stable sort: category then slug then model_sort_index
    cells.sort(key=lambda c: (PROMPT_CATEGORIES.index(c["category"]),
                              c["slug"],
                              c["model_sort_index"]))
    return cells


def main() -> None:
    cells = discover_cells()
    manifest = {
        "schema": "promptlab-cells-manifest/v1",
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "cell_count": len(cells),
        "models_display_order": [d for _, d in MODEL_DISPLAY_ORDER],
        "cells": cells,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO_ROOT)} — {len(cells)} cells")


if __name__ == "__main__":
    main()
