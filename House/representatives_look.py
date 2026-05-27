"""Photo-informed and inferred appearance for U.S. House representatives."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from presidents_look import Look

from representatives_data import RepresentativeRecord, era_for_year

# Curated by bioguide — likeness tuned from period portraits/photos.
CURATED: dict[str, Look] = {
    # First Congress (1789) — Founding Fathers and inaugural Speaker
    "M001063": Look(
        1789, "Frederick Muhlenberg", "Muhlenberg", "federal", "blue_frock",
        build="portly", skin="fair", hair_style="powdered_tied", face_shape="round",
    ),
    "M000043": Look(
        1789, "James Madison", "Madison", "federal", "blue_frock",
        build="short", skin="fair", hair_color="#e8e4dc", hair_style="white_full", face_shape="jowly",
    ),
    "B000084": Look(
        1789, "Abraham Baldwin", "Baldwin", "federal", "blue_frock",
        build="thin", skin="fair", hair_style="dark_neat", face_shape="long",
    ),
    "G000139": Look(
        1789, "Elbridge Gerry", "Gerry", "federal", "blue_frock",
        build="thin", skin="fair", hair_style="gray_thin", face_shape="gaunt",
    ),
    "B000388": Look(
        1789, "Egbert Benson", "Benson", "federal", "blue_frock",
        skin="fair", hair_style="powdered_short",
    ),
    "C000187": Look(
        1789, "Daniel Carroll", "Carroll", "federal", "blue_frock",
        build="portly", skin="fair", hair_style="gray_parted", face_shape="jowly",
    ),
    "H000570": Look(
        1789, "Daniel Hiester", "Hiester", "federal", "blue_frock",
        build="stocky", skin="ruddy", hair_style="dark_neat",
    ),
    "B000661": Look(
        1789, "Elias Boudinot", "Boudinot", "federal", "blue_frock",
        skin="fair", hair_style="powdered_short", face_shape="long",
    ),
    "F000224": Look(
        1789, "William Floyd", "Floyd", "federal", "blue_frock",
        build="stocky", skin="weathered", hair_style="gray_thin",
    ),
    "F000297": Look(
        1789, "Abiel Foster", "Foster", "federal", "blue_frock",
        skin="fair", hair_style="powdered_short",
    ),
    "M000034": Look(
        1791, "Nathaniel Macon", "Macon", "federal", "blue_frock",
        build="thin", skin="fair", hair_style="dark_neat", face_shape="gaunt",
    ),
    # Antebellum giants
    "C000482": Look(
        1811, "Henry Clay", "Clay", "antebellum", "black",
        build="thin", skin="fair", hair_color="#c8c0b0", hair_style="gray_parted",
        face_shape="gaunt", nose="prominent",
    ),
    "C000044": Look(
        1811, "John Caldwell Calhoun", "Calhoun", "antebellum", "black",
        build="thin", skin="fair", hair_color="#4a4038", hair_style="dark_neat",
        face_shape="gaunt", nose="prominent",
    ),
    "A000041": Look(
        1831, "John Quincy Adams", "JQA", "antebellum", "black",
        build="thin", skin="fair", hair_color="#e8e4dc", hair_style="white_full",
        face_shape="jowly", nose="prominent",
    ),
    "D000457": Look(
        1843, "Stephen Arnold Douglas", "Douglas", "antebellum", "black",
        build="short", skin="fair", hair_color="#3a3028", hair_style="dark_neat", face_shape="round",
    ),
    "L000313": Look(
        1847, "Abraham Lincoln", "Lincoln", "antebellum", "black",
        build="thin", skin="fair", hair_color="#2a2018", hair_style="dark_wavy",
        face_shape="gaunt", facial_hair="beard_lincoln", ears="prominent",
    ),
    "J000116": Look(
        1843, "Andrew Johnson", "Johnson", "antebellum", "black",
        build="average", skin="fair", hair_color="#6a6058", hair_style="dark_neat",
        face_shape="jowly",
    ),
    "G000507": Look(
        1851, "Galusha Grow", "Grow", "antebellum", "black",
        build="stocky", skin="fair", hair_style="gray_parted",
    ),
    # Civil War / Reconstruction
    "S000887": Look(
        1849, "Thaddeus Stevens", "Stevens", "civil", "black",
        build="thin", skin="fair", hair_color="#e8e4dc", hair_style="white_full",
        face_shape="gaunt", facial_hair="none", nose="prominent",
    ),
    "C000626": Look(
        1855, "Schuyler Colfax", "Colfax", "civil", "black",
        skin="fair", hair_style="dark_neat", facial_hair="mustache_full",
    ),
    "B000519": Look(
        1863, "James Gillespie Blaine", "Blaine", "civil", "black",
        build="average", skin="fair", hair_color="#6a6058", hair_style="gray_parted",
        facial_hair="mustache_full",
    ),
    # Gilded Age / Progressive Speakers
    "C000121": Look(
        1873, "Joseph Gurney Cannon", "Cannon", "gilded", "black",
        build="portly", skin="ruddy", hair_color="#e8e4dc", hair_style="white_full",
        face_shape="jowly", facial_hair="mustache_full",
    ),
    "B000995": Look(
        1891, "William Jennings Bryan", "Bryan", "gilded", "black",
        build="average", skin="fair", hair_color="#2a2018", hair_style="dark_wavy",
        face_shape="round",
    ),
    "L000007": Look(
        1917, "Fiorello La Guardia", "LaGuardia", "progressive", "charcoal",
        build="short", skin="olive", hair_color="#2a2018", hair_style="dark_neat",
        face_shape="round",
    ),
    "R000055": Look(
        1917, "Jeannette Rankin", "Rankin", "progressive", "charcoal",
        build="average", skin="fair", hair_color="#6a5040", hair_style="short", neckwear="tie_long",
    ),
    # New Deal / Post-WWII Speakers
    "R000082": Look(
        1913, "Sam Rayburn", "Rayburn", "modern", "charcoal",
        build="average", skin="weathered", hair_color="#8a8480", hair_style="gray_thin",
        face_shape="jowly", neckwear="tie_long",
    ),
    "F000260": Look(
        1949, "Gerald Ford", "Ford", "modern", "charcoal",
        build="athletic", skin="fair", hair_color="#8a8480", hair_style="gray_thin", neckwear="tie_long",
    ),
    "A000073": Look(
        1947, "Carl Bert Albert", "Albert", "modern", "charcoal",
        build="thin", skin="fair", hair_color="#6a6058", hair_style="gray_parted", neckwear="tie_long",
    ),
    "O000098": Look(
        1953, "Thomas Phillip O'Neill", "ONeill", "modern", "charcoal",
        build="portly", skin="ruddy", hair_color="#e8e4dc", hair_style="white_full",
        face_shape="jowly", neckwear="tie_long",
    ),
    # Modern / Contemporary
    "C000371": Look(
        1969, "Shirley Chisholm", "Chisholm", "modern", "charcoal",
        skin="brown_medium", hair_color="#1a1410", hair_style="short", neckwear="tie_long",
    ),
    "J000266": Look(
        1973, "Barbara Jordan", "Jordan", "modern", "charcoal",
        skin="brown_dark", hair_color="#1a1410", hair_style="short", glasses="round", neckwear="tie_long",
    ),
    "G000225": Look(
        1979, "Newt Gingrich", "Gingrich", "contemporary", "charcoal",
        build="portly", skin="fair", hair_color="#e8e4dc", hair_style="gray_thin", neckwear="tie_long",
    ),
    "P000197": Look(
        1987, "Nancy Pelosi", "Pelosi", "contemporary", "charcoal",
        skin="fair", hair_color="#6a5040", hair_style="short", neckwear="tie_long",
    ),
    "H000323": Look(
        1987, "J. Dennis Hastert", "Hastert", "contemporary", "charcoal",
        build="portly", skin="fair", hair_color="#c8c0b0", hair_style="gray_thin", neckwear="tie_long",
    ),
    "B000589": Look(
        1991, "John Boehner", "Boehner", "contemporary", "charcoal",
        build="average", skin="weathered", hair_color="#c8c0b0", hair_style="gray_thin", neckwear="tie_long",
    ),
    "R000570": Look(
        1999, "Paul Ryan", "Ryan", "contemporary", "charcoal",
        build="athletic", skin="fair", hair_color="#5c4a38", hair_style="short", neckwear="tie_long",
    ),
    "M001165": Look(
        2007, "Kevin McCarthy", "McCarthy", "contemporary", "charcoal",
        skin="fair", hair_color="#c8c0b0", hair_style="short", neckwear="tie_long",
    ),
}

# Iconic props keyed by filename slug fragment
PROPS: dict[str, str] = {
    "Clay": """
  <g id="prop-scroll">
    <ellipse fill="#e8dcc8" cx="248" cy="1100" rx="14" ry="32"/>
    <rect fill="#c4a878" x="238" y="1068" width="20" height="64" rx="3"/>
  </g>""",
    "Stevens": """
  <g id="prop-cane">
    <path fill="#3a2818" d="M228 820 L234 1060 Q235 1070 242 1070 L248 1060 L244 820 Z"/>
    <ellipse fill="#8b7355" cx="236" cy="814" rx="12" ry="7"/>
  </g>""",
    "Muhlenberg": """
  <g id="prop-gavel">
    <rect fill="#5c4030" x="552" y="1048" width="72" height="14" rx="3"/>
    <rect fill="#8b7355" x="618" y="1040" width="8" height="80" rx="2"/>
    <ellipse fill="#6b4a32" cx="556" cy="1055" rx="10" ry="8"/>
  </g>""",
    "Madison": """
  <g id="prop-quill">
    <path fill="#1a1410" d="M562 1020 L572 960 L578 962 L568 1022 Z"/>
    <path fill="#c8a030" d="M570 956 L580 944 L576 940 L566 952 Z"/>
  </g>""",
    "Lincoln": """
  <g id="prop-documents">
    <rect fill="#f5f2ea" x="540" y="1060" width="64" height="48" rx="2"/>
    <path fill="#1a1410" stroke="none" d="M548 1076 H596 M548 1088 H588 M548 1100 H592"/>
  </g>""",
    "Rayburn": """
  <g id="prop-gavel">
    <rect fill="#5c4030" x="552" y="1048" width="72" height="14" rx="3"/>
    <rect fill="#8b7355" x="618" y="1040" width="8" height="80" rx="2"/>
    <ellipse fill="#6b4a32" cx="556" cy="1055" rx="10" ry="8"/>
  </g>""",
    "Cannon": """
  <g id="prop-gavel">
    <rect fill="#5c4030" x="552" y="1048" width="72" height="14" rx="3"/>
    <rect fill="#8b7355" x="618" y="1040" width="8" height="80" rx="2"/>
    <ellipse fill="#6b4a32" cx="556" cy="1055" rx="10" ry="8"/>
  </g>""",
    "ONeill": """
  <g id="prop-flag">
    <rect fill="#1e3a6b" x="548" y="980" width="56" height="38"/>
    <path fill="#9c2a2a" d="M548 980 H604 V990 H548 Z"/>
    <path fill="#f0f0f0" d="M548 990 H604 V1000 H548 Z"/>
    <path fill="#9c2a2a" d="M548 1000 H604 V1010 H548 Z"/>
    <rect fill="#8b7355" x="604" y="980" width="5" height="120"/>
  </g>""",
    "Gingrich": """
  <g id="prop-books">
    <rect fill="#5c4030" x="548" y="1088" width="88" height="18" rx="2"/>
    <rect fill="#6b4a32" x="554" y="1068" width="76" height="16" rx="2"/>
    <rect fill="#4a3020" x="560" y="1050" width="64" height="14" rx="2"/>
  </g>""",
    "Jordan": """
  <g id="prop-gavel">
    <rect fill="#5c4030" x="552" y="1048" width="72" height="14" rx="3"/>
    <rect fill="#8b7355" x="618" y="1040" width="8" height="80" rx="2"/>
    <ellipse fill="#6b4a32" cx="556" cy="1055" rx="10" ry="8"/>
  </g>""",
}

NOTABLE_BIOGUIDES: frozenset[str] = frozenset(CURATED.keys())

HAIR_STYLES = (
    "short", "dark_neat", "gray_thin", "powdered_short", "bald_fringe",
    "dark_wavy", "gray_parted", "white_full", "sandy_balding", "powdered_tied",
)
COATS = ("blue_frock", "black", "charcoal", "brown", "navy")
FACIAL = ("none", "none", "none", "mustache_thin", "mustache_full", "beard_full_gray")
FACE_SHAPES = ("oval", "round", "long", "gaunt", "jowly")
NOSES = ("straight", "roman", "prominent", "wide")
SKINS = ("fair", "ruddy", "olive", "weathered", "tan", "brown_medium", "brown_dark")


def _look_era(year: int) -> str:
    y = era_for_year(year)
    mapping = {
        "Founding": "federal",
        "Antebellum": "antebellum",
        "Civil War": "civil",
        "Reconstruction": "civil",
        "Gilded Age": "gilded",
        "Progressive": "progressive",
        "New Deal": "modern",
        "Post-WWII": "modern",
        "Modern": "modern",
        "Contemporary": "contemporary",
    }
    return mapping.get(y, "modern")


def coat_for_era(era: str, idx: int) -> str:
    if era in ("colonial", "federal"):
        return "blue_frock"
    if era == "antebellum":
        return COATS[idx % 2]
    if era in ("civil", "gilded", "progressive"):
        return "black" if idx % 2 else "charcoal"
    if era == "modern":
        return "charcoal" if idx % 2 else "navy"
    return "charcoal"


def _hash_idx(seed: str, n: int) -> int:
    h = hashlib.md5(seed.encode()).hexdigest()
    return int(h[:8], 16) % n


def infer_look(rec: RepresentativeRecord) -> Look:
    era = _look_era(rec.primary_year)
    i = _hash_idx(rec.bioguide, 10_000)
    coat = coat_for_era(era, i)
    neck = "cravat" if era in ("colonial", "federal", "antebellum") else "tie_long"
    if era in ("civil", "gilded"):
        neck = "bow_tie" if i % 3 == 0 else "tie_long"
    return Look(
        rec.primary_year,
        rec.name,
        rec.bioguide,
        era,
        coat,
        build=("stocky", "thin", "average", "portly")[_hash_idx(rec.bioguide + "b", 4)],
        skin=SKINS[_hash_idx(rec.bioguide + "s", len(SKINS))],
        hair_color=("#5c4a38", "#8a7060", "#c8c0b0", "#e8e4dc", "#2a2018")[
            _hash_idx(rec.bioguide + "h", 5)
        ],
        hair_style=HAIR_STYLES[_hash_idx(rec.bioguide + "hair", len(HAIR_STYLES))],
        facial_hair=FACIAL[_hash_idx(rec.bioguide + "f", len(FACIAL))],
        face_shape=FACE_SHAPES[_hash_idx(rec.bioguide + "face", len(FACE_SHAPES))],
        nose=NOSES[_hash_idx(rec.bioguide + "n", len(NOSES))],
        neckwear=neck,
        glasses="round" if era in ("gilded", "progressive") and i % 17 == 0 else "none",
    )


def look_for_representative(rec: RepresentativeRecord) -> Look:
    if rec.bioguide in CURATED:
        base = CURATED[rec.bioguide]
        return Look(
            rec.primary_year,
            rec.name,
            base.filename,
            base.era,
            base.coat,
            build=base.build,
            military=base.military,
            sword=base.sword,
            boot_buckles=base.boot_buckles,
            skin=base.skin,
            hair_color=base.hair_color,
            hair_style=base.hair_style,
            facial_hair=base.facial_hair,
            face_shape=base.face_shape,
            nose=base.nose,
            brows=base.brows,
            ears=base.ears,
            glasses=base.glasses,
            neckwear=base.neckwear,
            top_hat=base.top_hat,
        )
    return infer_look(rec)


def props_for(look: Look) -> str:
    for key, svg in PROPS.items():
        if key in look.filename or key.replace("Dup", "") in look.name:
            return svg
    return ""
