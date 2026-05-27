#!/usr/bin/env python3
"""Generate mesh-ready senator portrait SVGs into Senet/portraits/."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from senators_data import SenatorRecord, load_senators
from senators_look import look_for_senator
from senet_render import generate_senator_svg

PORTRAITS_DIR = Path(__file__).resolve().parent / "portraits"


def generate_one(rec: SenatorRecord, out_dir: Path) -> Path:
    look = look_for_senator(rec)
    svg = generate_senator_svg(look, rec.name, rec.primary_year)
    path = out_dir / rec.filename
    path.write_text(svg, encoding="utf-8")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate senator portrait SVGs")
    parser.add_argument("--year", type=int, help="Only senators whose primary year matches")
    parser.add_argument("--year-max", type=int, help="Primary year <= this value")
    parser.add_argument("--limit", type=int, default=0, help="Max portraits to generate (0=all)")
    parser.add_argument("--bioguide", type=str, help="Single bioguide ID")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    out_dir = PORTRAITS_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    senators = load_senators()
    if args.bioguide:
        senators = [s for s in senators if s.bioguide == args.bioguide]
    if args.year is not None:
        senators = [s for s in senators if s.primary_year == args.year]
    if args.year_max is not None:
        senators = [s for s in senators if s.primary_year <= args.year_max]
    if args.limit:
        senators = senators[: args.limit]

    count = 0
    for rec in senators:
        dest = out_dir / rec.filename
        if dest.exists() and not args.force:
            continue
        generate_one(rec, out_dir)
        print(f"Wrote {dest}")
        count += 1

    print(f"Done. Generated {count} SVG(s) in {out_dir}/")


if __name__ == "__main__":
    main()
