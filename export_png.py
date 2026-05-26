#!/usr/bin/env python3
"""Rasterize president SVGs to PNG in a separate folder."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys

OUTPUT_SUBDIR = "generated"
PNG_SUBDIR = "generated_png"
DEFAULT_WIDTH = 2048
DEFAULT_HEIGHT = 3072
DEFAULT_DENSITY = 192


def _find_magick() -> str | None:
    for name in ("magick", "convert"):
        path = shutil.which(name)
        if path:
            return path
    return None


def export_one_cairo(svg_path: str, png_path: str, width: int, height: int) -> None:
    import cairosvg

    cairosvg.svg2png(
        url=svg_path,
        write_to=png_path,
        output_width=width,
        output_height=height,
    )


def export_one_magick(
    magick: str, svg_path: str, png_path: str, width: int, height: int, density: int
) -> None:
    subprocess.run(
        [
            magick,
            "-density",
            str(density),
            svg_path,
            "-resize",
            f"{width}x{height}!",
            png_path,
        ],
        check=True,
        capture_output=True,
    )


def export_one(
    svg_path: str,
    png_path: str,
    width: int,
    height: int,
    density: int,
    magick: str | None,
) -> None:
    os.makedirs(os.path.dirname(png_path) or ".", exist_ok=True)
    if magick:
        export_one_magick(magick, svg_path, png_path, width, height, density)
        return
    export_one_cairo(svg_path, png_path, width, height)


def main() -> None:
    base = os.path.dirname(os.path.abspath(__file__))
    svg_dir = os.path.join(base, sys.argv[1] if len(sys.argv) > 1 else OUTPUT_SUBDIR)
    png_dir = os.path.join(base, PNG_SUBDIR)
    width = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_WIDTH
    height = int(sys.argv[3]) if len(sys.argv) > 3 else DEFAULT_HEIGHT
    density = int(sys.argv[4]) if len(sys.argv) > 4 else DEFAULT_DENSITY

    if not os.path.isdir(svg_dir):
        raise SystemExit(f"SVG folder not found: {svg_dir}")

    magick = _find_magick()
    if not magick:
        try:
            import cairosvg  # noqa: F401
        except ImportError as e:
            raise SystemExit(
                "Need ImageMagick (brew install imagemagick) or CairoSVG:\n"
                "  pip install cairosvg\n"
                "  brew install cairo pango gdk-pixbuf libffi"
            ) from e

    os.makedirs(png_dir, exist_ok=True)
    files = sorted(f for f in os.listdir(svg_dir) if f.endswith(".svg"))
    if not files:
        raise SystemExit(f"No SVG files in {svg_dir}")

    backend = f"ImageMagick ({magick})" if magick else "CairoSVG"
    print(f"Exporting {len(files)} SVGs → {png_dir}/ ({width}x{height}, {backend})")

    for name in files:
        svg_path = os.path.join(svg_dir, name)
        png_path = os.path.join(png_dir, name.replace(".svg", ".png"))
        try:
            export_one(svg_path, png_path, width, height, density, magick)
            print(f"Wrote {png_path}")
        except subprocess.CalledProcessError as err:
            raise SystemExit(
                f"Failed on {name}: {err.stderr.decode(errors='replace')}"
            ) from err

    print(f"Done. {len(files)} PNGs in {png_dir}/")


if __name__ == "__main__":
    main()
