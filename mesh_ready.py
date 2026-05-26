"""Helpers so SVGs export to PNG / image-to-3D with closed, opaque, connected regions."""

from __future__ import annotations

import re

# Opaque sole color (replaces semi-transparent shoe ellipses)
SHOE_SOLE = "#241c18"


def path_closed(d: str) -> str:
    """Ensure path data ends with Z for a filled region."""
    d = d.strip()
    if not d:
        return d
    if d[-1].upper() != "Z":
        return f"{d} Z"
    return d


def solid(hex_color: str, opacity: float) -> str:
    """Blend color to opaque (against green) for PNG → 3D without alpha halos."""
    if opacity >= 0.99:
        return hex_color
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    bg = (0x3C, 0xB8, 0x68)  # GREEN_BACKGROUND
    t = opacity
    return "#{:02x}{:02x}{:02x}".format(
        int(r * t + bg[0] * (1 - t)),
        int(g * t + bg[1] * (1 - t)),
        int(b * t + bg[2] * (1 - t)),
    )


def strip_decorative_3d(svg: str) -> str:
    """Remove stroke-only / line details that break image-to-3D meshing."""
    drop = (
        r'\s*<line[^>]*/>\s*',
        r'\s*<path[^>]*fill="none"[^>]*/>\s*',
        r'\s*<ellipse[^>]*opacity="[^"]*"[^>]*/>\s*',
        r'\s*<path[^>]*opacity="0\.(?:0[0-9]|[1-9])"[^>]*/>\s*',
    )
    out = svg
    for pat in drop:
        out = re.sub(pat, "\n", out, flags=re.IGNORECASE)
    return out


def close_unclosed_paths(svg: str) -> str:
    """Add Z to any <path fill=...> that lacks a close (hair, tails, cravat)."""

    def fix(m: re.Match[str]) -> str:
        tag = m.group(0)
        if 'fill="none"' in tag or "stroke=" in tag and 'fill="' not in tag:
            return tag
        dm = re.search(r'\sd="([^"]*)"', tag)
        if not dm:
            return tag
        d = dm.group(1).strip()
        if d and d[-1].upper() != "Z":
            new_d = path_closed(d)
            return tag.replace(f'd="{dm.group(1)}"', f'd="{new_d}"', 1)
        return tag

    return re.sub(r"<path\s[^>]*/>", fix, svg)


def finalize_svg_for_3d(svg: str) -> str:
    return close_unclosed_paths(strip_decorative_3d(svg))
