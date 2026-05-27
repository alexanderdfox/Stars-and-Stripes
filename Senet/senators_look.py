"""Photo-informed and inferred appearance for U.S. senators."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from presidents_look import Look

from senators_data import SenatorRecord

# Curated by bioguide — likeness tuned from period portraits/photos.
CURATED: dict[str, Look] = {
    # First Congress (1789) and immediate Federal era
    "B000226": Look(1789, "Richard Bassett", "Bassett", "federal", "blue_frock", skin="fair", hair_style="powdered_short"),
    "B001186": Look(1789, "Pierce Butler", "Butler", "federal", "blue_frock", build="stocky", skin="ruddy", hair_style="powdered_tied"),
    "C000185": Look(1789, "Charles Carroll", "Carroll", "federal", "blue_frock", build="thin", skin="fair", hair_color="#e8e4dc", hair_style="white_full", face_shape="long"),
    "R000091": Look(1789, "George Read", "Read", "federal", "blue_frock", skin="fair", hair_style="bald_fringe", face_shape="round"),
    "G000526": Look(1789, "James Gunn", "Gunn", "federal", "blue_frock", build="stocky", skin="weathered", hair_style="dark_neat"),
    "L000067": Look(1789, "John Langdon", "Langdon", "federal", "blue_frock", skin="ruddy", hair_style="powdered_tied"),
    "E000155": Look(1789, "Jonathan Elmer", "Elmer", "federal", "blue_frock", skin="fair", hair_style="bald_fringe"),
    "E000147": Look(1789, "Oliver Ellsworth", "Ellsworth", "federal", "blue_frock", skin="fair", hair_style="powdered_short", face_shape="long", nose="roman"),
    "W000633": Look(1789, "Paine Wingate", "Wingate", "federal", "blue_frock", skin="fair", hair_style="gray_thin"),
    "S000154": Look(1789, "Philip Schuyler", "Schuyler", "federal", "blue_frock", build="athletic", military=True, skin="fair", hair_style="powdered_tied"),
    "I000053": Look(1789, "Ralph Izard", "Izard", "federal", "blue_frock", skin="fair", hair_style="powdered_short", build="portly"),
    "L000201": Look(1789, "Richard Henry Lee", "Lee", "federal", "blue_frock", build="thin", skin="fair", hair_style="gray_thin", face_shape="gaunt"),
    "M000985": Look(1789, "Robert Morris", "Morris", "federal", "blue_frock", build="portly", skin="ruddy", hair_style="bald_fringe", face_shape="jowly"),
    "K000212": Look(1789, "Rufus King", "King", "federal", "blue_frock", skin="fair", hair_style="powdered_tied", face_shape="long"),
    "D000013": Look(1789, "Tristram Dalton", "Dalton", "federal", "blue_frock", skin="fair", hair_style="powdered_short"),
    "F000100": Look(1789, "William Few", "Few", "federal", "blue_frock", skin="fair", hair_style="dark_neat"),
    "M000031": Look(1789, "William Maclay", "Maclay", "federal", "blue_frock", skin="fair", hair_style="dark_wavy"),
    "P000102": Look(1789, "William Paterson", "Paterson", "federal", "blue_frock", skin="fair", hair_style="dark_neat", face_shape="round"),
    "S001009": Look(1789, "Caleb Strong", "Strong", "federal", "blue_frock", skin="fair", hair_style="powdered_short"),
    "H000368": Look(1789, "Benjamin Hawkins", "Hawkins", "federal", "blue_frock", build="stocky", skin="weathered", hair_style="dark_neat"),
    "M000858": Look(1790, "James Monroe", "Monroe", "federal", "blue_frock", skin="fair", hair_color="#6a6058", hair_style="powdered_short", face_shape="jowly"),
    # Great Triumvirate and Civil War era
    "C000482": Look(1806, "Henry Clay", "Clay", "antebellum", "black", build="thin", skin="fair", hair_color="#c8c0b0", hair_style="gray_parted", face_shape="gaunt", nose="prominent"),
    "W000238": Look(1827, "Daniel Webster", "Webster", "antebellum", "black", build="stocky", skin="ruddy", hair_color="#2a2018", hair_style="dark_wavy", face_shape="jowly", nose="roman", facial_hair="mutton_chops"),
    "C000044": Look(1832, "John Caldwell Calhoun", "Calhoun", "antebellum", "black", build="thin", skin="fair", hair_color="#4a4038", hair_style="dark_neat", face_shape="gaunt", nose="prominent"),
    "D000457": Look(1847, "Stephen Arnold Douglas", "Douglas", "antebellum", "black", build="short", skin="fair", hair_color="#3a3028", hair_style="dark_neat", face_shape="round"),
    "S001068": Look(1851, "Charles Sumner", "Sumner", "civil", "black", build="thin", skin="fair", hair_color="#6a6058", hair_style="gray_parted", face_shape="long", glasses="pince_nez"),
    # 20th–21st century notables
    "T000009": Look(1939, "Robert Alphonso Taft", "Taft", "modern", "charcoal", skin="fair", hair_style="gray_parted", neckwear="tie_long"),
    "J000160": Look(1949, "Lyndon Baines Johnson", "LBJ", "modern", "charcoal", build="stocky", skin="weathered", hair_style="gray_thin", ears="prominent"),
    "K000114": Look(1963, "Robert F. Kennedy", "RFK", "modern", "charcoal", build="thin", skin="fair", hair_style="dark_wavy"),
    "O000167": Look(2005, "Barack Obama", "Obama", "contemporary", "charcoal", skin="brown_medium", hair_color="#1a1410", hair_style="short_black", neckwear="tie_long"),
    "M000303": Look(1987, "John S. McCain", "McCain", "contemporary", "navy", build="average", skin="weathered", hair_color="#c8c0b8", hair_style="gray_thin", neckwear="tie_long"),
    "K000107": Look(1953, "John F. Kennedy", "JFK", "modern", "charcoal", build="athletic", skin="fair", hair_color="#2a2018", hair_style="dark_wavy", neckwear="tie_long"),
    "T000387": Look(1935, "Harry S. Truman", "Truman", "modern", "charcoal", skin="fair", hair_color="#8a8480", hair_style="gray_thin", glasses="round", neckwear="bow_tie"),
    "G000267": Look(1953, "Barry Goldwater", "Goldwater", "modern", "charcoal", skin="weathered", hair_color="#c8c0b0", hair_style="gray_thin", glasses="aviator"),
    "K000105": Look(1962, "Edward M. Kennedy", "TedKennedy", "modern", "charcoal", build="stocky", skin="ruddy", hair_color="#6a5040", hair_style="dark_wavy"),
    "H000953": Look(1949, "Hubert H. Humphrey", "Humphrey", "modern", "charcoal", skin="fair", hair_color="#8a8480", hair_style="gray_parted", face_shape="jowly"),
    "D000360": Look(1951, "Everett M. Dirksen", "Dirksen", "modern", "charcoal", skin="fair", hair_color="#6a6058", hair_style="gray_thin", facial_hair="none", glasses="round"),
    "T000254": Look(1954, "Strom Thurmond", "Thurmond", "modern", "charcoal", build="thin", skin="fair", hair_color="#e8e4dc", hair_style="white_full"),
    "C001041": Look(2001, "Hillary Rodham Clinton", "Clinton", "contemporary", "charcoal", skin="fair", hair_color="#c8c0b8", hair_style="short", neckwear="tie_long"),
    "W000817": Look(2013, "Elizabeth Warren", "Warren", "contemporary", "charcoal", skin="fair", hair_color="#b8a898", hair_style="short", glasses="rectangular"),
    "M000355": Look(1985, "Mitch McConnell", "McConnell", "contemporary", "charcoal", skin="fair", hair_color="#e8e4dc", hair_style="gray_thin", neckwear="tie_long"),
}

# Iconic props keyed by filename slug fragment
PROPS: dict[str, str] = {
    "Webster": """
  <g id="prop-books">
    <rect fill="#5c4030" x="548" y="1088" width="88" height="18" rx="2"/>
    <rect fill="#6b4a32" x="554" y="1068" width="76" height="16" rx="2"/>
    <rect fill="#4a3020" x="560" y="1050" width="64" height="14" rx="2"/>
  </g>""",
    "Clay": """
  <g id="prop-scroll">
    <ellipse fill="#e8dcc8" cx="248" cy="1100" rx="14" ry="32"/>
    <rect fill="#c4a878" x="238" y="1068" width="20" height="64" rx="3"/>
  </g>""",
    "Sumner": """
  <g id="prop-cane">
    <path fill="#3a2818" d="M228 820 L234 1060 Q235 1070 242 1070 L248 1060 L244 820 Z"/>
    <ellipse fill="#8b7355" cx="236" cy="814" rx="12" ry="7"/>
  </g>""",
    "Lee": """
  <g id="prop-quill">
    <path fill="#1a1410" d="M562 1020 L572 960 L578 962 L568 1022 Z"/>
    <path fill="#c8a030" d="M570 956 L580 944 L576 940 L566 952 Z"/>
  </g>""",
    "Schuyler": """
  <g id="prop-flag">
    <rect fill="#1e3a6b" x="548" y="980" width="56" height="38"/>
    <path fill="#9c2a2a" d="M548 980 H604 V990 H548 Z"/>
    <path fill="#f0f0f0" d="M548 990 H604 V1000 H548 Z"/>
    <path fill="#9c2a2a" d="M548 1000 H604 V1010 H548 Z"/>
    <rect fill="#8b7355" x="604" y="980" width="5" height="120"/>
  </g>""",
}

HAIR_STYLES = (
    "short", "dark_neat", "gray_thin", "powdered_short", "bald_fringe",
    "dark_wavy", "gray_parted", "white_full", "sandy_balding",
)
COATS = ("blue_frock", "black", "charcoal", "brown", "navy")
FACIAL = ("none", "none", "none", "mustache_thin", "mustache_full", "beard_full_gray")
FACE_SHAPES = ("oval", "round", "long", "gaunt", "jowly")
NOSES = ("straight", "roman", "prominent", "wide")
SKINS = ("fair", "ruddy", "olive", "weathered", "tan")


def era_for_year(year: int) -> str:
    if year < 1800:
        return "federal"
    if year < 1840:
        return "antebellum" if year >= 1820 else "federal"
    if year < 1860:
        return "antebellum"
    if year < 1880:
        return "civil"
    if year < 1900:
        return "gilded"
    if year < 1920:
        return "progressive"
    if year < 1946:
        return "modern"
    return "contemporary"


def coat_for_era(era: str, idx: int) -> str:
    if era in ("colonial", "federal"):
        return "blue_frock"
    if era == "antebellum":
        return COATS[idx % 2]  # blue_frock or black
    if era in ("civil", "gilded", "progressive"):
        return "black" if idx % 2 else "charcoal"
    if era == "modern":
        return "charcoal" if idx % 2 else "navy"
    return "charcoal"


def _hash_idx(seed: str, n: int) -> int:
    h = hashlib.md5(seed.encode()).hexdigest()
    return int(h[:8], 16) % n


def infer_look(rec: SenatorRecord) -> Look:
    era = era_for_year(rec.primary_year)
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
        hair_color=("#5c4a38", "#8a7060", "#c8c0b0", "#e8e4dc", "#2a2018")[_hash_idx(rec.bioguide + "h", 5)],
        hair_style=HAIR_STYLES[_hash_idx(rec.bioguide + "hair", len(HAIR_STYLES))],
        facial_hair=FACIAL[_hash_idx(rec.bioguide + "f", len(FACIAL))],
        face_shape=FACE_SHAPES[_hash_idx(rec.bioguide + "face", len(FACE_SHAPES))],
        nose=NOSES[_hash_idx(rec.bioguide + "n", len(NOSES))],
        neckwear=neck,
        glasses="round" if era in ("gilded", "progressive") and i % 17 == 0 else "none",
    )


def look_for_senator(rec: SenatorRecord) -> Look:
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
