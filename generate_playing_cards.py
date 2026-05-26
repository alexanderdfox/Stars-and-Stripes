#!/usr/bin/env python3
"""Generate USD playing cards for all U.S. president PNGs."""

from __future__ import annotations

import os
import re
from pathlib import Path

from playing_card_lib import (
    CardSpec,
    build_card,
    card_paths,
    emoji_for_index,
    write_deck_usda,
)

OUTPUT_DIR = "playing_cards_usd"
PNG_SOURCE = "generated_png"


def president_sort_key(name: str) -> int:
    m = re.match(r"^(\d+)", name)
    return int(m.group(1)) if m else 9999


def list_president_pngs(png_dir: Path) -> list[str]:
    files = [f for f in os.listdir(png_dir) if f.lower().endswith(".png")]
    return sorted(files, key=president_sort_key)


def build_specs(png_dir: Path) -> list[tuple[CardSpec, Path]]:
    specs: list[tuple[CardSpec, Path]] = []
    for i, png_name in enumerate(list_president_pngs(png_dir)):
        m = re.match(r"^(\d+)\s*-\s*(.+)\.png$", png_name, re.I)
        if not m:
            continue
        number = int(m.group(1))
        name = m.group(2).strip()
        emoji, rank, suit = emoji_for_index(i)
        slug = f"{number:02d}_{name.replace(' ', '_').replace('.', '')}"
        spec = CardSpec(
            name=name,
            slug=slug,
            rank_label=rank,
            suit_name=suit,
            emoji=emoji,
            label=f"{number:02d} - {name}",
            metadata={"presidentNumber": str(number)},
        )
        specs.append((spec, png_dir / png_name))
    return specs


def write_readme(base: Path, count: int) -> None:
    from playing_card_lib import CARD_H, CARD_T, CARD_W

    readme = f"""# Presidents Playing Cards (USD)

{count} double-sided playing cards for 3D pipelines (Omniverse, Blender, Maya, etc.).

## Layout

| Side | Content |
|------|---------|
| **Front** (`Face`) | President portrait from `generated_png/` |
| **Back** (`CardBack`) | Unicode playing-card glyph (🂡–🂿) with rank/suit |

## Files

- `deck.usda` — master assembly (grid layout)
- `cards/*.usda` — one component per president
- `textures/faces/` — front portraits
- `textures/backs/` — rasterized emoji card faces

## Card size

Poker standard: {CARD_W*1000:.1f} mm × {CARD_H*1000:.1f} mm × {CARD_T*1000:.2f} mm thick

## Regenerate presidents deck

```bash
python3 generate_playing_cards.py
```

## Custom cards

```bash
python3 make_card.py --face photo.png --name "Someone" --rank A --suit Spades
```
"""
    (base / "README.md").write_text(readme, encoding="utf-8")


def main() -> None:
    root = Path(__file__).resolve().parent
    png_dir = root / PNG_SOURCE
    if not png_dir.is_dir():
        raise SystemExit(f"Missing {png_dir} — run export_png.py first.")

    paths = card_paths(root / OUTPUT_DIR)
    entries = build_specs(png_dir)
    if not entries:
        raise SystemExit(f"No PNG files in {png_dir}")

    card_usdas: list[Path] = []
    specs: list[CardSpec] = []
    for spec, face_src in entries:
        card_usdas.append(build_card(spec, face_src, paths))
        specs.append(spec)
        print(f"  {spec.label}  →  {spec.emoji} {spec.rank_label} {spec.suit_name}")

    deck_path = paths["base"] / "deck.usda"
    write_deck_usda(
        specs,
        card_usdas,
        deck_path,
        deck_name="U.S. Presidents playing card deck — portrait faces, Unicode emoji card backs",
    )
    write_readme(paths["base"], len(specs))
    print(f"\nWrote {len(specs)} cards to {paths['base']}/")
    print(f"  Master: {deck_path}")


if __name__ == "__main__":
    main()
