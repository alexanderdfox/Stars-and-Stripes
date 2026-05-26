#!/usr/bin/env python3
"""Build an Instagram-sized grid collage from president PNG exports."""

from __future__ import annotations

import os
import re
import sys
from math import ceil

from PIL import Image

PNG_DIR = "generated_png"
DEFAULT_OUT = "collage_instagram.png"
# Instagram feed square (1:1)
INSTAGRAM_SIZE = (1080, 1080)
GREEN = (60, 184, 104)


def president_sort_key(name: str) -> int:
    m = re.match(r"^(\d+)", name)
    return int(m.group(1)) if m else 9999


def list_pngs(png_dir: str) -> list[str]:
    files = [f for f in os.listdir(png_dir) if f.lower().endswith(".png")]
    return sorted(files, key=president_sort_key)


def grid_shape(count: int, aspect: float) -> tuple[int, int]:
    """Pick cols×rows close to target aspect (width/height)."""
    best: tuple[int, int, float] | None = None
    for cols in range(1, count + 1):
        rows = ceil(count / cols)
        score = abs((cols / rows) - aspect)
        if best is None or score < best[2]:
            best = (cols, rows, score)
    assert best is not None
    return best[0], best[1]


def fit_in_cell(img: Image.Image, cell_w: int, cell_h: int) -> Image.Image:
    """Scale to fill cell height, crop sides if needed (full-body reads best)."""
    scale = cell_h / img.height
    new_w = max(1, int(img.width * scale))
    resized = img.resize((new_w, cell_h), Image.Resampling.LANCZOS)
    if new_w > cell_w:
        left = (new_w - cell_w) // 2
        resized = resized.crop((left, 0, left + cell_w, cell_h))
    elif new_w < cell_w:
        canvas = Image.new("RGB", (cell_w, cell_h), GREEN)
        canvas.paste(resized, ((cell_w - new_w) // 2, 0))
        return canvas
    return resized.convert("RGB")


def build_collage(
    png_dir: str,
    out_path: str,
    size: tuple[int, int] = INSTAGRAM_SIZE,
) -> None:
    files = list_pngs(png_dir)
    if not files:
        raise SystemExit(f"No PNG files in {png_dir}")

    width, height = size
    cols, rows = grid_shape(len(files), width / height)
    cell_w = width // cols
    cell_h = height // rows

    collage = Image.new("RGB", (width, height), GREEN)

    for i, name in enumerate(files):
        row, col = divmod(i, cols)
        path = os.path.join(png_dir, name)
        with Image.open(path) as im:
            tile = fit_in_cell(im.convert("RGB"), cell_w, cell_h)
        x = col * cell_w
        y = row * cell_h
        collage.paste(tile, (x, y))

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    collage.save(out_path, format="PNG", optimize=True)
    print(f"Wrote {out_path} ({width}x{height}, {cols}x{rows} grid, {len(files)} presidents)")


def main() -> None:
    base = os.path.dirname(os.path.abspath(__file__))
    png_dir = os.path.join(base, sys.argv[1] if len(sys.argv) > 1 else PNG_DIR)
    out = os.path.join(base, sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUT)
    w = int(sys.argv[3]) if len(sys.argv) > 3 else INSTAGRAM_SIZE[0]
    h = int(sys.argv[4]) if len(sys.argv) > 4 else INSTAGRAM_SIZE[1]
    build_collage(png_dir, out, (w, h))


if __name__ == "__main__":
    main()
