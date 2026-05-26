"""Photo-informed appearance traits for each U.S. president."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Look:
    """Traits derived from period photographs and painted portraits."""

    number: int
    name: str
    filename: str

    # --- body & era ---
    era: str  # colonial, federal, antebellum, civil, gilded, progressive, modern, contemporary
    coat: str  # blue_frock, black, charcoal, brown, navy
    build: str = "average"  # thin, average, stocky, portly
    military: bool = False
    sword: bool = False
    boot_buckles: bool = False
    bg: str = "#f4e8d1"

    # --- complexion ---
    skin: str = "fair"  # fair, ruddy, olive, tan, brown_medium, brown_dark

    # --- hair (hex + style key) ---
    hair_color: str = "#5c4a38"
    hair_style: str = "short"  # see render_hair()

    # --- facial hair ---
    facial_hair: str = "none"  # none, mustache_thin, mustache_full, beard_full, beard_lincoln, mutton_chops

    # --- face structure ---
    face_shape: str = "oval"  # oval, round, long, gaunt, jowly
    nose: str = "straight"  # straight, roman, prominent, wide
    brows: str = "normal"  # normal, heavy, thin
    ears: str = "normal"  # normal, prominent

    # --- accessories ---
    glasses: str = "none"  # none, round, pince_nez, aviator, rectangular
    neckwear: str = "cravat"  # cravat, bow_tie, tie_long
    top_hat: bool = False


LOOKS: list[Look] = [
    # 1–6 Federal era
    Look(1, "George Washington", "Washington", "colonial", "blue_frock",
         build="athletic", military=True, sword=True, skin="ruddy",
         hair_color="#b8b0a0", hair_style="powdered_tied", facial_hair="none",
         face_shape="long", nose="prominent", bg="#f4e8d1"),
    Look(2, "John Adams", "Adams", "federal", "blue_frock",
         skin="ruddy", hair_color="#9a9080", hair_style="bald_fringe",
         face_shape="round", nose="wide", boot_buckles=True, bg="#f5e9d4"),
    Look(3, "Thomas Jefferson", "Jefferson", "federal", "blue_frock",
         build="thin", skin="fair", hair_color="#8a7060", hair_style="reddish_tied",
         face_shape="long", nose="roman"),
    Look(4, "James Madison", "Madison", "federal", "blue_frock",
         build="short", skin="fair", hair_color="#9a9088", hair_style="bald_fringe",
         face_shape="round", nose="straight"),
    Look(5, "James Monroe", "Monroe", "federal", "blue_frock",
         skin="fair", hair_color="#6a6058", hair_style="powdered_short",
         face_shape="jowly", nose="straight"),
    Look(6, "John Quincy Adams", "JohnQuincyAdams", "federal", "blue_frock",
         skin="fair", hair_color="#8a8480", hair_style="bald_side_whiskers",
         face_shape="long", nose="prominent"),
    # 7–15 Antebellum
    Look(7, "Andrew Jackson", "Jackson", "antebellum", "blue_frock",
         build="thin", skin="weathered", hair_color="#e0ddd0", hair_style="white_wild",
         face_shape="gaunt", nose="prominent", brows="heavy"),
    Look(8, "Martin Van Buren", "VanBuren", "antebellum", "blue_frock",
         build="stocky", skin="fair", hair_color="#4a3828", hair_style="sideburns_bald",
         face_shape="round", nose="wide"),
    Look(9, "William Henry Harrison", "WilliamHenryHarrison", "antebellum", "blue_frock",
         build="thin", military=True, skin="fair", hair_color="#c8c0b0", hair_style="gray_thin",
         face_shape="gaunt", nose="prominent"),
    Look(10, "John Tyler", "Tyler", "antebellum", "blue_frock",
         skin="fair", hair_color="#a0a0a0", hair_style="receding_gray",
         face_shape="long", nose="roman"),
    Look(11, "James K. Polk", "Polk", "antebellum", "black",
         build="thin", skin="fair", hair_color="#3a3028", hair_style="dark_neat",
         face_shape="gaunt", nose="straight"),
    Look(12, "Zachary Taylor", "Taylor", "antebellum", "blue_frock",
         build="stocky", military=True, skin="weathered", hair_color="#b0a898",
         hair_style="gray_short", face_shape="broad", nose="wide"),
    Look(13, "Millard Fillmore", "Fillmore", "antebellum", "black",
         skin="fair", hair_color="#a89888", hair_style="sandy_balding",
         face_shape="round", nose="straight"),
    Look(14, "Franklin Pierce", "Pierce", "antebellum", "black",
         skin="fair", hair_color="#2a2018", hair_style="dark_wavy",
         face_shape="oval", nose="straight"),
    Look(15, "James Buchanan", "Buchanan", "antebellum", "black",
         skin="fair", hair_color="#e8e4dc", hair_style="white_full",
         face_shape="jowly", nose="straight"),
    # 16–21 Civil / Gilded
    Look(16, "Abraham Lincoln", "Lincoln", "civil", "black",
         build="thin", skin="fair", hair_color="#1a1a1a", hair_style="black_tousled",
         facial_hair="beard_lincoln", face_shape="gaunt", nose="prominent",
         neckwear="bow_tie", top_hat=True, bg="#e8d9c0"),
    Look(17, "Andrew Johnson", "AndrewJohnson", "civil", "black",
         skin="weathered", hair_color="#4a4038", hair_style="dark_receding",
         face_shape="gaunt", nose="wide", brows="heavy", neckwear="bow_tie"),
    Look(18, "Ulysses S. Grant", "Grant", "gilded", "black",
         skin="fair", hair_color="#5a5048", hair_style="short_dark",
         facial_hair="beard_full", face_shape="oval", nose="straight", neckwear="bow_tie"),
    Look(19, "Rutherford B. Hayes", "Hayes", "gilded", "black",
         skin="fair", hair_color="#b0a8a0", hair_style="bald_fringe",
         facial_hair="beard_full_gray", face_shape="oval", nose="straight", neckwear="ascot"),
    Look(20, "James A. Garfield", "Garfield", "gilded", "black",
         skin="fair", hair_color="#4a3828", hair_style="wavy_brown",
         facial_hair="beard_full", face_shape="oval", nose="straight",
         glasses="round", neckwear="bow_tie"),
    Look(21, "Chester A. Arthur", "Arthur", "gilded", "black",
         skin="fair", hair_color="#2a2018", hair_style="mutton_chop_top",
         facial_hair="mutton_chops", face_shape="oval", nose="straight", neckwear="ascot"),
    Look(22, "Grover Cleveland", "Cleveland", "gilded", "black",
         build="portly", skin="fair", hair_color="#4a4038", hair_style="dark_receding",
         facial_hair="mustache_full", face_shape="jowly", nose="wide", neckwear="bow_tie"),
    Look(23, "Benjamin Harrison", "BenjaminHarrison", "gilded", "black",
         skin="fair", hair_color="#b0a8a0", hair_style="bald_fringe",
         facial_hair="beard_full_gray", face_shape="round", nose="straight",
         neckwear="bow_tie"),
    # 25–31 Progressive / early modern
    Look(25, "William McKinley", "McKinley", "progressive", "black",
         skin="fair", hair_color="#a0a0a0", hair_style="bald_fringe",
         facial_hair="mustache_thin", face_shape="round", nose="straight", neckwear="bow_tie"),
    Look(26, "Theodore Roosevelt", "TheodoreRoosevelt", "progressive", "brown",
         build="stocky", skin="fair", hair_color="#4a3828", hair_style="short_dark",
         facial_hair="mustache_full", face_shape="broad", nose="straight",
         glasses="pince_nez", neckwear="bow_tie"),
    Look(27, "William Howard Taft", "Taft", "progressive", "charcoal",
         build="portly", skin="fair", hair_color="#6a6058", hair_style="short_gray",
         facial_hair="mustache_full", face_shape="jowly", nose="wide", neckwear="bow_tie"),
    Look(28, "Woodrow Wilson", "Wilson", "progressive", "charcoal",
         build="thin", skin="fair", hair_color="#a0a0a0", hair_style="receding_gray",
         face_shape="gaunt", nose="prominent", glasses="round", neckwear="ascot"),
    Look(29, "Warren G. Harding", "Harding", "progressive", "charcoal",
         skin="fair", hair_color="#a89888", hair_style="gray_parted",
         face_shape="oval", nose="straight", neckwear="necktie"),
    Look(30, "Calvin Coolidge", "Coolidge", "progressive", "charcoal",
         skin="fair", hair_color="#c8a878", hair_style="sandy_thin",
         face_shape="long", nose="straight", brows="thin", neckwear="necktie"),
    Look(31, "Herbert Hoover", "Hoover", "modern", "charcoal",
         skin="fair", hair_color="#b0a8a0", hair_style="gray_stiff",
         face_shape="long", nose="prominent", neckwear="necktie"),
    # 32–46 Modern / contemporary
    Look(32, "Franklin D. Roosevelt", "FranklinRoosevelt", "modern", "charcoal",
         skin="fair", hair_color="#a0a0a0", hair_style="gray_temples",
         face_shape="oval", nose="straight", glasses="rectangular", neckwear="necktie"),
    Look(33, "Harry S. Truman", "Truman", "modern", "charcoal",
         skin="fair", hair_color="#c8c0b0", hair_style="gray_thin",
         face_shape="round", nose="straight", glasses="round", neckwear="necktie"),
    Look(34, "Dwight D. Eisenhower", "Eisenhower", "modern", "charcoal",
         skin="fair", hair_color="#d8d4c8", hair_style="bald",
         face_shape="broad", nose="straight", neckwear="necktie"),
    Look(35, "John F. Kennedy", "Kennedy", "modern", "charcoal",
         build="athletic", skin="tan", hair_color="#3a2818", hair_style="brown_parted",
         face_shape="oval", nose="straight", neckwear="necktie"),
    Look(36, "Lyndon B. Johnson", "LyndonJohnson", "modern", "charcoal",
         skin="fair", hair_color="#a0a0a0", hair_style="slicked_gray",
         face_shape="jowly", nose="wide", ears="prominent",
         glasses="rectangular", neckwear="necktie"),
    Look(37, "Richard Nixon", "Nixon", "modern", "charcoal",
         skin="fair", hair_color="#2a2018", hair_style="dark_receding",
         face_shape="long", nose="prominent", brows="heavy", neckwear="necktie"),
    Look(38, "Gerald Ford", "Ford", "contemporary", "charcoal",
         skin="fair", hair_color="#c8c0b0", hair_style="receding_gray",
         face_shape="broad", nose="straight", neckwear="necktie"),
    Look(39, "Jimmy Carter", "Carter", "contemporary", "navy",
         skin="fair", hair_color="#d0c8b8", hair_style="gray_full",
         face_shape="oval", nose="straight", neckwear="necktie"),
    Look(40, "Ronald Reagan", "Reagan", "contemporary", "charcoal",
         skin="tan", hair_color="#8a7868", hair_style="swept_back",
         face_shape="long", nose="straight", neckwear="necktie"),
    Look(41, "George H. W. Bush", "GeorgeHWBush", "contemporary", "navy",
         skin="fair", hair_color="#c8c0b0", hair_style="thin_gray",
         face_shape="long", nose="prominent", neckwear="necktie"),
    Look(42, "Bill Clinton", "Clinton", "contemporary", "charcoal",
         skin="ruddy", hair_color="#e8e4dc", hair_style="gray_wavy",
         face_shape="jowly", nose="straight", neckwear="necktie"),
    Look(43, "George W. Bush", "GeorgeWBush", "contemporary", "charcoal",
         skin="fair", hair_color="#a8a098", hair_style="gray_parted",
         face_shape="oval", nose="straight", neckwear="necktie"),
    Look(44, "Barack Obama", "Obama", "contemporary", "charcoal",
         build="athletic", skin="brown_medium", hair_color="#1a1410", hair_style="short_black",
         face_shape="oval", nose="straight", neckwear="necktie"),
    Look(45, "Donald Trump", "Trump", "contemporary", "charcoal",
         build="stocky", skin="tan", hair_color="#e8c878", hair_style="blonde_combover",
         face_shape="jowly", nose="straight", neckwear="tie_long"),
    Look(46, "Joe Biden", "Biden", "contemporary", "charcoal",
         skin="fair", hair_color="#f0f0f0", hair_style="white_full",
         face_shape="jowly", nose="straight", glasses="aviator", neckwear="necktie"),
    # 47 — duplicate of Trump (second term slot / export numbering)
    Look(47, "Donald Trump", "Trump", "contemporary", "charcoal",
         build="stocky", skin="tan", hair_color="#e8c878", hair_style="blonde_combover",
         face_shape="jowly", nose="straight", neckwear="tie_long"),
]
