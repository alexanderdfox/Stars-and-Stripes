# Senet — U.S. Senator Portrait SVG Collection

Production-ready, mesh-optimized full-body vector portraits of every historic United States senator (1789–present).

## Contents

| Path | Description |
|------|-------------|
| `SENATORS_INDEX.md` | Markdown index (2,018 senators): name, birth/death, primary Senate year, state, filename |
| `senators.json` | Machine-readable index |
| `portraits/` | One SVG per senator: `senator-name-year.svg` |
| `STYLE_GUIDE.md` | Canvas, layers, naming, 3D import |
| `build_index.py` | Rebuild index from congress-legislators JSON |
| `generate_senators.py` | Batch SVG generator |
| `senators_look.py` | Curated likenesses + inferred traits |
| `senet_render.py` | Layered 1200×2400 SVG assembly |

## Quick start

```bash
cd Senet
# Refresh legislator data (optional)
curl -fsSL -o legislators-historical.json \
  https://unitedstates.github.io/congress-legislators/legislators-historical.json
curl -fsSL -o legislators-current.json \
  https://unitedstates.github.io/congress-legislators/legislators-current.json

python3 build_index.py
python3 generate_senators.py          # all portraits
python3 generate_senators.py --year 1789 --force   # First Congress only
python3 generate_senators.py --bioguide W000238 --force   # Daniel Webster
```

## Data source

Biographical and service dates: [unitedstates/congress-legislators](https://github.com/unitedstates/congress-legislators).  
Rendering reuses the Presidents project `era_clothing` / `generate_presidents` rig with senator-specific layering and scale.

## Curated likenesses

First Congress (1789), Great Triumvirate (Clay, Webster, Calhoun), Douglas, Sumner, Taft, LBJ, Obama, McCain, and others are hand-tuned in `senators_look.py`. Remaining senators use deterministic era-appropriate inference from service year and bioguide ID.
