# House — U.S. Representative Portrait SVG Collection

Production-ready, mesh-optimized full-body vector portraits of every historic United States House member (1789–present).

## Contents

| Path | Description |
|------|-------------|
| `HOUSE_INDEX.md` | Markdown index (~11,000 representatives) grouped by historical era |
| `representatives.json` | Machine-readable index |
| `portraits/` | One SVG per representative: `name-state-year.svg` |
| `STYLE_GUIDE.md` | Canvas, layers, naming, 3D import |
| `build_index.py` | Rebuild index from congress-legislators JSON |
| `generate_representatives.py` | Batch SVG generator |
| `representatives_look.py` | Curated likenesses + inferred traits |
| `house_render.py` | Layered 1200×2400 SVG assembly |

## Quick start

```bash
cd House
# Refresh legislator data (optional — reads from Senet/ if not present locally)
curl -fsSL -o legislators-historical.json \
  https://unitedstates.github.io/congress-legislators/legislators-historical.json
curl -fsSL -o legislators-current.json \
  https://unitedstates.github.io/congress-legislators/legislators-current.json

python3 build_index.py
python3 generate_representatives.py --year 1789 --force   # First Congress batch
python3 generate_representatives.py --notable --force     # Curated historic figures
python3 generate_representatives.py                       # Full collection (11k+ files)
```

## File naming

`{firstname-lastname}-{state}-{primary-house-year}.svg`

Examples:
- `henry-clay-kentucky-1811.svg`
- `frederick-augustus-conrad-muhlenberg-pennsylvania-1789.svg`
- `thaddeus-stevens-pennsylvania-1849.svg`

## Data source

Biographical and service dates: [unitedstates/congress-legislators](https://github.com/unitedstates/congress-legislators).

Rendering reuses the Presidents project `era_clothing` / `generate_presidents` rig with House-specific layering, state-aware filenames, and era-grouped indexing.

## Curated likenesses

First Congress (1789), Henry Clay, Thaddeus Stevens, Joseph Cannon, Sam Rayburn, Tip O'Neill, Newt Gingrich, Nancy Pelosi, and other Speakers and landmark legislators are hand-tuned in `representatives_look.py`. Remaining members use deterministic era-appropriate inference from service year and bioguide ID.

## Batch generation by era

```bash
python3 generate_representatives.py --era Founding --force
python3 generate_representatives.py --era Antebellum --force
python3 generate_representatives.py --year-max 1865 --force
```
