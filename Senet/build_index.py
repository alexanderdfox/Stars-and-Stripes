#!/usr/bin/env python3
"""Build SENATORS_INDEX.md and senators.json from congress-legislators data."""

from __future__ import annotations

import json
from pathlib import Path

from senators_data import DATA_DIR, load_senators


def main() -> None:
    senators = load_senators()
    out_json = DATA_DIR / "senators.json"
    out_md = DATA_DIR / "SENATORS_INDEX.md"

    payload = [
        {
            "bioguide": s.bioguide,
            "name": s.name,
            "birth_year": s.birth_year,
            "death_year": s.death_year,
            "primary_senate_year": s.primary_year,
            "state": s.state,
            "party": s.party,
            "svg": s.filename,
        }
        for s in senators
    ]
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "# United States Senators (1789–Present)",
        "",
        f"Complete index of **{len(senators)}** historic senators with primary Senate service year.",
        "Portrait files live in `portraits/` as `senator-name-year.svg`.",
        "",
        "| # | Name | Birth | Death | Primary Senate | State | SVG |",
        "|---:|------|-------|-------|----------------|-------|-----|",
    ]
    for i, s in enumerate(senators, 1):
        birth = s.birth_year or "—"
        death = s.death_year or "—"
        lines.append(
            f"| {i} | {s.name} | {birth} | {death} | {s.primary_year} | {s.state} | `{s.filename}` |"
        )

    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out_json} ({len(senators)} records)")
    print(f"Wrote {out_md}")


if __name__ == "__main__":
    main()
