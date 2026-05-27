#!/usr/bin/env python3
"""Generate mesh-ready House representative portrait SVGs into House/portraits/."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from house_render import generate_representative_svg
from representatives_data import RepresentativeRecord, load_representatives
from representatives_look import NOTABLE_BIOGUIDES, look_for_representative

PORTRAITS_DIR = Path(__file__).resolve().parent / "portraits"


def generate_one(rec: RepresentativeRecord, out_dir: Path) -> Path:
    look = look_for_representative(rec)
    svg = generate_representative_svg(look, rec.name, rec.primary_year, rec.state_slug)
    path = out_dir / rec.filename
    path.write_text(svg, encoding="utf-8")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate House representative portrait SVGs")
    parser.add_argument("--year", type=int, help="Only reps whose primary year matches")
    parser.add_argument("--year-max", type=int, help="Primary year <= this value")
    parser.add_argument("--era", type=str, help="Only reps in this era label (e.g. Founding)")
    parser.add_argument("--limit", type=int, default=0, help="Max portraits to generate (0=all)")
    parser.add_argument("--bioguide", type=str, help="Single bioguide ID")
    parser.add_argument("--notable", action="store_true", help="Only curated notable representatives")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    out_dir = PORTRAITS_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    reps = load_representatives()
    if args.bioguide:
        reps = [r for r in reps if r.bioguide == args.bioguide]
    if args.notable:
        reps = [r for r in reps if r.bioguide in NOTABLE_BIOGUIDES]
    if args.year is not None:
        reps = [r for r in reps if r.primary_year == args.year]
    if args.year_max is not None:
        reps = [r for r in reps if r.primary_year <= args.year_max]
    if args.era:
        reps = [r for r in reps if r.era == args.era]
    if args.limit:
        reps = reps[: args.limit]

    count = 0
    for rec in reps:
        dest = out_dir / rec.filename
        if dest.exists() and not args.force:
            continue
        generate_one(rec, out_dir)
        print(f"Wrote {dest}")
        count += 1

    print(f"Done. Generated {count} SVG(s) in {out_dir}/")


if __name__ == "__main__":
    main()
