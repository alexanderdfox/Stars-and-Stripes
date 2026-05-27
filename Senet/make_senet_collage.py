#!/usr/bin/env python3
"""Build Instagram carousel collages of Senet portraits, sorted by primary Senate year."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from math import ceil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

DATA_DIR = Path(__file__).resolve().parent
PORTRAITS = DATA_DIR / "portraits"
INDEX = DATA_DIR / "senators.json"
THUMB_DIR = DATA_DIR / "portraits_thumb"
OUT_DIR = DATA_DIR / "collage_instagram"

INSTAGRAM_SIZE = (1080, 1080)
GREEN = (60, 184, 104)
COLS = 10
ROWS = 9
PER_PAGE = COLS * ROWS
THUMB_W = INSTAGRAM_SIZE[0] // COLS
THUMB_H = INSTAGRAM_SIZE[1] // ROWS


def _find_magick() -> str:
    for name in ("magick", "convert"):
        path = shutil.which(name)
        if path:
            return path
    raise SystemExit("ImageMagick required (brew install imagemagick)")


def load_senators() -> list[dict]:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    return sorted(data, key=lambda s: (s["primary_senate_year"], s["name"].lower()))


def thumb_path(svg_name: str) -> Path:
    return THUMB_DIR / svg_name.replace(".svg", ".png")


def ensure_thumb(magick: str, svg_name: str) -> Path:
    src = PORTRAITS / svg_name
    dst = thumb_path(svg_name)
    if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
        return dst
    THUMB_DIR.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            magick,
            "-density",
            "120",
            str(src),
            "-background",
            "#3cb868",
            "-flatten",
            "-resize",
            f"{THUMB_W}x{THUMB_H}^",
            "-gravity",
            "center",
            "-extent",
            f"{THUMB_W}x{THUMB_H}",
            str(dst),
        ],
        check=True,
        capture_output=True,
    )
    return dst


def fit_tile(im: Image.Image) -> Image.Image:
    """Center-crop fill to cell (full-body reads best)."""
    scale = max(THUMB_W / im.width, THUMB_H / im.height)
    nw, nh = max(1, int(im.width * scale)), max(1, int(im.height * scale))
    resized = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - THUMB_W) // 2
    top = (nh - THUMB_H) // 2
    return resized.crop((left, top, left + THUMB_W, top + THUMB_H)).convert("RGB")


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
    ):
        if os.path.isfile(path):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


def year_range_label(chunk: list[dict]) -> str:
    y0 = chunk[0]["primary_senate_year"]
    y1 = chunk[-1]["primary_senate_year"]
    return str(y0) if y0 == y1 else f"{y0}–{y1}"


def build_page(
    chunk: list[dict],
    page_num: int,
    total_pages: int,
    magick: str,
) -> Image.Image:
    canvas = Image.new("RGB", INSTAGRAM_SIZE, GREEN)
    draw = ImageDraw.Draw(canvas)
    title_font = _font(36)
    year_font = _font(14)

    label = year_range_label(chunk)
    header = f"Senet · {label}  ({page_num}/{total_pages})"
    draw.rectangle((0, 0, INSTAGRAM_SIZE[0], 44), fill=(40, 120, 70))
    draw.text((12, 6), header, fill=(255, 255, 255), font=title_font)

    grid_top = 44
    cell_h = (INSTAGRAM_SIZE[1] - grid_top) // ROWS
    cell_w = INSTAGRAM_SIZE[0] // COLS

    last_year: int | None = None
    for i, rec in enumerate(chunk):
        row, col = divmod(i, COLS)
        png = ensure_thumb(magick, rec["svg"])
        with Image.open(png) as im:
            tile = fit_tile(im)
        x = col * cell_w
        y = grid_top + row * cell_h
        canvas.paste(tile, (x, y))

        year = rec["primary_senate_year"]
        if year != last_year:
            draw.rectangle((x, y, x + cell_w - 1, y + 3), fill=(212, 175, 55))
            draw.text((x + 3, y + 5), str(year), fill=(255, 255, 220), font=year_font)
            last_year = year

    return canvas


def build_cover(total: int, magick: str) -> Image.Image:
    canvas = Image.new("RGB", INSTAGRAM_SIZE, GREEN)
    draw = ImageDraw.Draw(canvas)
    title = _font(52)
    sub = _font(28)
    draw.text((48, 420), "SENET", fill=(255, 255, 255), font=title)
    draw.text((48, 490), "U.S. Senators", fill=(240, 240, 230), font=sub)
    draw.text((48, 530), "1789 – 2026", fill=(240, 240, 230), font=sub)
    draw.text((48, 600), f"{total} portraits by year of service", fill=(220, 235, 220), font=_font(22))
    draw.text((48, 980), "Swipe for chronological carousel →", fill=(230, 245, 230), font=_font(20))

    # Preview strip: first 20 thumbs
    senators = load_senators()[:20]
    pw, ph = 48, 96
    for i, rec in enumerate(senators):
        png = ensure_thumb(magick, rec["svg"])
        with Image.open(png) as im:
            tile = im.resize((pw, ph), Image.Resampling.LANCZOS)
        canvas.paste(tile.convert("RGB"), (48 + i * (pw + 4), 660))
    return canvas


def build_collages(out_dir: Path | None = None) -> list[Path]:
    magick = _find_magick()
    senators = load_senators()
    if not senators:
        raise SystemExit(f"No data in {INDEX}")

    dest = out_dir or OUT_DIR
    dest.mkdir(parents=True, exist_ok=True)

    pages: list[list[dict]] = [
        senators[i : i + PER_PAGE] for i in range(0, len(senators), PER_PAGE)
    ]
    total = len(pages)
    written: list[Path] = []

    cover = build_cover(len(senators), magick)
    cover_path = dest / "slide-00-cover.png"
    cover.save(cover_path, format="PNG", optimize=True)
    written.append(cover_path)
    print(f"Wrote {cover_path}")

    for n, chunk in enumerate(pages, start=1):
        img = build_page(chunk, n, total, magick)
        path = dest / f"slide-{n:02d}.png"
        img.save(path, format="PNG", optimize=True)
        written.append(path)
        print(f"Wrote {path}  ({year_range_label(chunk)}, {len(chunk)} senators)")

    # Single contact sheet sorted by year (1080 wide, tall) for Stories / save
    story = _build_year_timeline(senators, magick)
    story_path = dest / "senet_timeline_by_year.png"
    story.save(story_path, format="PNG", optimize=True)
    written.append(story_path)
    print(f"Wrote {story_path} ({story.size[0]}x{story.size[1]})")

    return written


def _build_year_timeline(senators: list[dict], magick: str) -> Image.Image:
    """Vertical timeline: one row per year, portraits left-to-right."""
    by_year: dict[int, list[dict]] = {}
    for s in senators:
        by_year.setdefault(s["primary_senate_year"], []).append(s)

    years = sorted(by_year)
    thumb_w, thumb_h = 36, 72
    row_h = thumb_h + 22
    width = 1080
    height = 56 + len(years) * row_h
    canvas = Image.new("RGB", (width, height), GREEN)
    draw = ImageDraw.Draw(canvas)
    draw.text((12, 12), "Senet — senators by first Senate year", fill=(255, 255, 255), font=_font(24))
    y = 56
    label_font = _font(16)
    for year in years:
        draw.text((8, y + thumb_h // 2 - 8), str(year), fill=(255, 248, 200), font=label_font)
        x = 56
        for rec in by_year[year]:
            png = ensure_thumb(magick, rec["svg"])
            with Image.open(png) as im:
                tile = im.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
            canvas.paste(tile.convert("RGB"), (x, y))
            x += thumb_w + 2
            if x > width - thumb_w:
                break
        y += row_h
    return canvas


def main() -> None:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else OUT_DIR
    build_collages(out)


if __name__ == "__main__":
    main()
