#!/usr/bin/env python3
"""Build HOUSE_INDEX.md and representatives.json from congress-legislators data."""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from representatives_data import DATA_DIR, load_representatives
from representatives_look import NOTABLE_BIOGUIDES

ERA_ORDER = [
    "Founding",
    "Antebellum",
    "Civil War",
    "Reconstruction",
    "Gilded Age",
    "Progressive",
    "New Deal",
    "Post-WWII",
    "Modern",
    "Contemporary",
]


def main() -> None:
    reps = load_representatives()
    out_json = DATA_DIR / "representatives.json"
    out_md = DATA_DIR / "HOUSE_INDEX.md"

    payload = [
        {
            "bioguide": r.bioguide,
            "name": r.name,
            "birth_year": r.birth_year,
            "death_year": r.death_year,
            "primary_house_year": r.primary_year,
            "state": r.state,
            "state_slug": r.state_slug,
            "party": r.party,
            "era": r.era,
            "notable": r.bioguide in NOTABLE_BIOGUIDES,
            "svg": r.filename,
        }
        for r in reps
    ]
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    by_era: dict[str, list] = defaultdict(list)
    for r in reps:
        by_era[r.era].append(r)

    lines = [
        "# United States House of Representatives (1789–Present)",
        "",
        f"Complete index of **{len(reps)}** historic representatives with primary House service year.",
        "Portrait files live in `portraits/` as `representative-name-state-year.svg`.",
        "",
        "## Eras",
        "",
    ]
    for era in ERA_ORDER:
        group = by_era.get(era, [])
        if not group:
            continue
        y0 = min(r.primary_year for r in group)
        y1 = max(r.primary_year for r in group)
        notables = [r for r in group if r.bioguide in NOTABLE_BIOGUIDES]
        lines.append(f"### {era} ({y0}–{y1}) — {len(group)} members")
        if notables:
            lines.append("")
            lines.append("**Notable (curated likeness):** " + ", ".join(r.name for r in notables[:20]))
            if len(notables) > 20:
                lines.append(f"… and {len(notables) - 20} more curated figures.")
        lines.append("")
        lines.append("| # | Name | Birth | Death | Primary House | State | Notable | SVG |")
        lines.append("|---:|------|-------|-------|---------------|-------|:-------:|-----|")
        for i, r in enumerate(group, 1):
            birth = r.birth_year or "—"
            death = r.death_year or "—"
            star = "★" if r.bioguide in NOTABLE_BIOGUIDES else ""
            lines.append(
                f"| {i} | {r.name} | {birth} | {death} | {r.primary_year} | "
                f"{r.state} | {star} | `{r.filename}` |"
            )
        lines.append("")

    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out_json} ({len(reps)} records)")
    print(f"Wrote {out_md}")


if __name__ == "__main__":
    main()
