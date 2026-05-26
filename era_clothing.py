"""Era-accurate clothing with unified body topology."""

from __future__ import annotations

from mesh_ready import SHOE_SOLE, path_closed
from presidents_look import Look

VEST = {
    "buff": "#c4a878",
    "cream": "#e8dcc8",
    "gold": "#d4b878",
    "burgundy": "#6a2830",
    "charcoal_vest": "#3a4048",
    "stripe": "#d8d0c0",
}

SHIRT = "#f5f2ea"
SHIRT_COLLAR = "#faf8f4"

WAIST_Y = 684
KNEE_Y = 862
ANKLE_Y = 952
SHOE_TOP_COLONIAL = 958
SHOE_TOP_MODERN = 944
SHOULDER_Y = 528
COLLAR_Y = 452
SHIRT_TOP = COLLAR_Y + 20  # shirt panel meets collar / neck base


def _w(look: Look) -> int:
    if look.build == "portly":
        return 32
    if look.build == "stocky":
        return 18
    return 0


def _lerp(a: int, b: int, t: float) -> int:
    return int(a + (b - a) * t)


def body_metrics(look: Look) -> dict[str, int]:
    """Shared anchors: waist → knee → ankle; outer x is always toward the body side."""
    w = _w(look)
    wl = 378 + w // 5
    wr = 422 - w // 5
    lo = 318 - w // 3
    ro = 482 + w // 3
    shoe_top = SHOE_TOP_COLONIAL if uses_breeches(look) else SHOE_TOP_MODERN

    # Left leg: outer (smaller x) … inner (toward center). Right leg: mirrored.
    if uses_breeches(look):
        fol, fil = lo + 32 + w // 6, wl - 8
        for_, fir = ro - 32 - w // 6, wr + 8
        sol, sor = fol - 14, for_ + 14
    else:
        fol, fil = lo + 30 + w // 6, wl - 10
        for_, fir = ro - 30 - w // 6, wr + 10
        sol, sor = fol - 16, for_ + 16

    t_knee = (KNEE_Y - WAIST_Y) / max(shoe_top - WAIST_Y, 1)
    kin_l = _lerp(wl, fil, t_knee)
    kout_l = _lerp(lo, fol, t_knee)
    kin_r = _lerp(wr, fir, t_knee)
    kout_r = _lerp(ro, for_, t_knee)

    return {
        "w": w,
        "waist_in_l": wl,
        "waist_in_r": wr,
        "waist_out_l": lo,
        "waist_out_r": ro,
        "shoulder_l": 326 - w // 2,
        "shoulder_r": 474 + w // 2,
        "arm_l": 276 - w // 2,
        "arm_r": 524 + w // 2,
        "shoe_top": shoe_top,
        "foot_in_l": fil,
        "foot_out_l": fol,
        "foot_in_r": fir,
        "foot_out_r": for_,
        "knee_in_l": kin_l,
        "knee_out_l": kout_l,
        "knee_in_r": kin_r,
        "knee_out_r": kout_r,
        "shoe_outer_l": sol,
        "shoe_outer_r": sor,
    }


def uses_breeches(look: Look) -> bool:
    return look.era in ("colonial", "federal")


def neck_geometry(look: Look, cy: int, ry: int, rx: int) -> tuple[int, int, int]:
    """Jaw-to-collar neck bounds: (top_y, bottom_y, half_width)."""
    jaw = cy + int(ry * 0.78)
    if look.facial_hair == "beard_lincoln":
        jaw = cy + int(ry * 0.80)
    elif look.facial_hair in ("beard_full", "beard_full_gray"):
        jaw = cy + int(ry * 0.76)
    elif look.facial_hair in ("mustache_full", "mutton_chops", "mustache_thin"):
        jaw = cy + int(ry * 0.77)
    if look.face_shape == "jowly":
        jaw = cy + int(ry * 0.77)
    if look.top_hat:
        jaw = min(jaw, cy + int(ry * 0.82))
    bottom = COLLAR_Y + 8
    if look.era in ("modern", "contemporary"):
        bottom = COLLAR_Y + 10
    half_w = max(18, min(int(rx * 0.38), 30))
    if look.facial_hair == "beard_lincoln":
        half_w = max(16, half_w - 4)
    return jaw, bottom, half_w


def shows_vest(look: Look) -> bool:
    return look.era in ("colonial", "federal", "antebellum", "civil", "gilded", "progressive")


def trouser_color(look: Look, coat_main: str) -> str:
    if look.coat == "navy":
        return "#141e32"
    if look.coat == "brown":
        return "#352418"
    if look.coat in ("black", "charcoal"):
        if look.era in ("civil", "gilded"):
            return coat_main
        return "#1a2028" if look.coat == "charcoal" else "#121820"
    return "#1f2a38"


def _darken(hex_color: str, amount: float) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    f = 1 - amount
    return f"#{int(r*f):02x}{int(g*f):02x}{int(b*f):02x}"


def shoes(look: Look) -> str:
    m = body_metrics(look)
    top = m["shoe_top"]
    fil, fir = m["foot_in_l"], m["foot_in_r"]
    fol, for_ = m["foot_out_l"], m["foot_out_r"]
    sol, sor = m["shoe_outer_l"], m["shoe_outer_r"]
    heel = top + 118

    if uses_breeches(look):
        buckles = (
            f"""
  <path fill="#111" d="M{sol + 8} 988 Q{sol + 30} 998 {sol + 55} 988 L{sol + 52} 996 Q{sol + 28} 1006 {sol + 6} 996 Z"/>
  <path fill="#111" d="M{sor - 8} 988 Q{sor - 30} 998 {sor - 55} 988 L{sor - 52} 996 Q{sor - 28} 1006 {sor - 6} 996 Z"/>"""
            if look.military and look.era == "colonial"
            else f"""
  <rect fill="#d4b030" rx="2" height="10" width="32" y="{heel - 34}" x="{(fol + fil) // 2 - 16}"/>
  <rect fill="#d4b030" rx="2" height="10" width="32" y="{heel - 34}" x="{(for_ + fir) // 2 - 16}"/>"""
        )
        return f"""
  <path fill="#1a1a1a" d="M{fol} {top} L{sol} {top} L{sol - 8} {heel} L{fil + 6} {heel} L{fil} {top} Z"/>
  <path fill="#1a1a1a" d="M{for_} {top} L{sor} {top} L{sor + 8} {heel} L{fir - 6} {heel} L{fir} {top} Z"/>{buckles}"""

    sole_l = (fol + fil) // 2
    sole_r = (for_ + fir) // 2
    return f"""
  <path fill="#1c1410" d="M{fol} {top} L{sol} {top} L{sol - 6} {heel} L{fil + 6} {heel} L{fil} {top} Z"/>
  <path fill="#1c1410" d="M{for_} {top} L{sor} {top} L{sor + 6} {heel} L{fir - 6} {heel} L{fir} {top} Z"/>
  <ellipse fill="{SHOE_SOLE}" ry="5" rx="26" cy="{heel - 16}" cx="{sole_l}"/>
  <ellipse fill="{SHOE_SOLE}" ry="5" rx="26" cy="{heel - 16}" cx="{sole_r}"/>"""


def _leg_panel(
    top_in: int,
    top_out: int,
    mid_in: int,
    mid_out: int,
    bot_in: int,
    bot_out: int,
    y_top: int,
    y_mid: int,
    y_bot: int,
    fill: str,
) -> str:
    """One leg panel: top → mid → bottom, outer edge on the body side."""
    if y_mid == y_top:
        return f"""
  <path fill="{fill}" d="M{top_in} {y_top} L{top_out} {y_top} L{bot_out} {y_bot} L{bot_in} {y_bot} Z"/>"""
    if y_mid == y_bot:
        return f"""
  <path fill="{fill}" d="M{top_in} {y_top} L{top_out} {y_top} L{bot_out} {y_bot} L{bot_in} {y_bot} Z"/>"""
    return f"""
  <path fill="{fill}" d="M{top_in} {y_top} L{top_out} {y_top} L{mid_out} {y_mid} L{bot_out} {y_bot} L{bot_in} {y_bot} L{mid_in} {y_mid} Z"/>"""


def legs_breeches_stockings(look: Look, s: tuple) -> str:
    m = body_metrics(look)
    _, hand, _, stocking, _, _ = s
    top = m["shoe_top"]

    def quad(ti, to, bi, bo, yt, yb, fill):
        return f"""
  <path fill="{fill}" d="M{ti} {yt} L{to} {yt} L{bo} {yb} L{bi} {yb} Z"/>"""

    return (
        quad(m["waist_in_l"], m["waist_out_l"], m["knee_in_l"], m["knee_out_l"], WAIST_Y, KNEE_Y, hand)
        + quad(m["waist_in_r"], m["waist_out_r"], m["knee_in_r"], m["knee_out_r"], WAIST_Y, KNEE_Y, hand)
        + quad(m["knee_in_l"], m["knee_out_l"], m["foot_in_l"], m["foot_out_l"], KNEE_Y, top, stocking)
        + quad(m["knee_in_r"], m["knee_out_r"], m["foot_in_r"], m["foot_out_r"], KNEE_Y, top, stocking)
    )


def legs_trousers(look: Look, color: str) -> str:
    m = body_metrics(look)
    top = m["shoe_top"]
    left = _leg_panel(
        m["waist_in_l"], m["waist_out_l"],
        m["knee_in_l"], m["knee_out_l"],
        m["foot_in_l"], m["foot_out_l"],
        WAIST_Y, KNEE_Y, top, color,
    )
    right = _leg_panel(
        m["waist_in_r"], m["waist_out_r"],
        m["knee_in_r"], m["knee_out_r"],
        m["foot_in_r"], m["foot_out_r"],
        WAIST_Y, KNEE_Y, top, color,
    )
    return left + right


def waist_band(look: Look, fill: str) -> str:
    """Cover the trouser–torso seam so no background shows between layers."""
    m = body_metrics(look)
    wl, wr = m["waist_in_l"], m["waist_in_r"]
    lo, ro = m["waist_out_l"], m["waist_out_r"]
    return f"""
  <path fill="{fill}" d="M{wl - 2} {WAIST_Y} L{wr + 2} {WAIST_Y} L{ro} {WAIST_Y + 2} L{lo} {WAIST_Y + 2} Z"/>"""


def torso_base(look: Look, s: tuple) -> str:
    """Shirt/torso block linking waist to shoulders — everything else layers on top."""
    m = body_metrics(look)
    _, hand, _, _, _, _ = s
    fill = SHIRT if shows_vest(look) or look.era in ("modern", "contemporary", "progressive") else hand
    wl, wr = m["waist_in_l"], m["waist_in_r"]
    sl, sr = m["shoulder_l"], m["shoulder_r"]
    return f"""
  <path fill="{fill}" d="M{wl} {WAIST_Y} L{wr} {WAIST_Y} Q{sr} {620} {sr+6} {SHOULDER_Y} Q400 512 {sl-6} {SHOULDER_Y} Q{sl} {620} {wl} {WAIST_Y} Z"/>"""


def shirt_layer(look: Look) -> str:
    m = body_metrics(look)
    w = m["w"]
    st = SHIRT_TOP
    if look.era in ("modern", "contemporary"):
        return f"""
  <path fill="{SHIRT}" d="M{362 - w // 4} {st} L{438 + w // 4} {st} L434 {st + 42} Q400 {st + 52} {366 - w // 4} {st + 42} Z"/>
  <path fill="{SHIRT}" d="M{372 - w // 4} {st + 42} Q400 {st + 36} {428 + w // 4} {st + 42} L{m['waist_in_r'] - 2} {WAIST_Y} Q400 {WAIST_Y + 8} {m['waist_in_l'] + 2} {WAIST_Y} Z"/>"""
    if not shows_vest(look):
        return ""
    return f"""
  <path fill="{SHIRT}" d="M{362 - w // 5} {st} L{438 + w // 5} {st} L434 {st + 44} Q400 {st + 54} {366 - w // 5} {st + 44} Z"/>
  <path fill="{SHIRT}" d="M{375 - w // 5} {st + 44} Q400 {st + 38} {425 + w // 5} {st + 44} L{m['waist_in_r'] - 2} {WAIST_Y} Q400 {WAIST_Y + 6} {m['waist_in_l'] + 2} {WAIST_Y} Z"/>"""


def waistcoat(look: Look, vest_color: str) -> str:
    m = body_metrics(look)
    w = m["w"]
    buttons = ""
    if look.era in ("colonial", "federal", "antebellum", "gilded"):
        buttons = """
  <circle fill="#c8a030" r="6" cy="558" cx="400"/>
  <circle fill="#c8a030" r="6" cy="595" cx="400"/>
  <circle fill="#c8a030" r="6" cy="630" cx="400"/>"""
    elif look.era == "progressive":
        buttons = """
  <circle fill="#888" r="4" cy="560" cx="400"/>
  <circle fill="#888" r="4" cy="598" cx="400"/>"""
    return f"""
  <path fill="{vest_color}" d="M{358-w//4} {SHOULDER_Y-18} Q400 {SHOULDER_Y-28} {442+w//4} {SHOULDER_Y-18} Q448 568 400 576 Q352 568 {358-w//4} {SHOULDER_Y-18} Z"/>
  <path fill="{_darken(vest_color, 0.05)}" d="M{364-w//4} {SHOULDER_Y-8} L400 {SHOULDER_Y+2} L{436+w//4} {SHOULDER_Y-8} L434 562 Q400 570 366 562 Z"/>{buttons}"""


def wrist_bridges(look: Look, hand: str, sl: int, sr: int, al: int, ar: int) -> str:
    """Solid cuffs linking sleeves to hands (no floating hands in 3D)."""
    left_cx, right_cx = 234, 566
    if look.era in ("modern", "contemporary"):
        left_cx, right_cx = 235, 565
    return f"""
  <path fill="{hand}" d="M{sl - 14} 768 L{left_cx - 28} 785 L{left_cx - 22} 822 L{sl - 10} 808 Z"/>
  <path fill="{hand}" d="M{sr + 14} 768 L{right_cx + 28} 785 L{right_cx + 22} 822 L{sr + 10} 808 Z"/>"""


def arms_for_era(look: Look, s: tuple, coat_main: str) -> str:
    m = body_metrics(look)
    _, hand, stroke, _, _, _ = s
    al, ar = m["arm_l"], m["arm_r"]
    sl, sr = m["shoulder_l"], m["shoulder_r"]
    ay = SHOULDER_Y
    bridges = wrist_bridges(look, hand, sl, sr, al, ar)

    if look.era in ("colonial", "federal", "antebellum"):
        sleeve = hand
    elif look.era in ("civil", "gilded", "progressive"):
        sleeve = SHIRT
    else:
        sleeve = SHIRT

    if look.era in ("modern", "contemporary"):
        return f"""
  <path fill="{coat_main}" d="M{al} {ay} Q{al-18} 638 {al-8} 778 L{sl-8} 778 Q{sl-20} 638 {sl} {ay} Z"/>
  <path fill="{coat_main}" d="M{ar} {ay} Q{ar+18} 638 {ar+8} 778 L{sr+8} 778 Q{sr+20} 638 {sr} {ay} Z"/>
  <path fill="{sleeve}" d="M{al-6} 668 Q{al-10} 728 {al-8} 798 L{sl-12} 798 Q{sl-16} 728 {sl-10} 668 Z"/>
  <path fill="{sleeve}" d="M{ar+6} 668 Q{ar+10} 728 {ar+8} 798 L{sr+12} 798 Q{sr+16} 728 {sr+10} 668 Z"/>{bridges}
  <ellipse transform="rotate(-35 235 808)" fill="{hand}" ry="21" rx="27" cy="808" cx="235"/>
  <ellipse transform="rotate(45 565 798)" fill="{hand}" ry="20" rx="26" cy="798" cx="565"/>"""

    return f"""
  <path fill="{sleeve}" d="M{al} {ay} Q{al-22} 660 {al-10} 802 L{sl-6} 802 Q{sl-18} 660 {sl} {ay} Z"/>
  <path fill="{sleeve}" d="M{ar} {ay} Q{ar+22} 650 {ar+8} 792 L{sr+6} 792 Q{sr+18} 650 {sr} {ay} Z"/>{bridges}
  <ellipse transform="rotate(-35 234 808)" fill="{hand}" ry="21" rx="27" cy="808" cx="234"/>
  <ellipse transform="rotate(45 566 798)" fill="{hand}" ry="20" rx="26" cy="798" cx="566"/>"""


def coat_for_era(look: Look, main: str, trim: str) -> str:
    m = body_metrics(look)
    w = m["w"]
    wl, wr = m["waist_in_l"], m["waist_in_r"]
    sl, sr = m["shoulder_l"], m["shoulder_r"]
    lo, ro = m["waist_out_l"], m["waist_out_r"]

    if look.era == "colonial" and look.military:
        return f"""
  <path fill="{main}" d="M{292-w} {SHOULDER_Y} Q{262-w} 658 {278-w} 786 Q{318} 872 {344-w} 682 Q400 558 {456+w} 682 Q482 872 {522+w} 786 Q{542+w} 658 {512+w} {SHOULDER_Y} Z"/>
  <path fill="{main}" d="M{wl-2} {WAIST_Y} L{wr+2} {WAIST_Y} L{ro} {WAIST_Y} L{lo} {WAIST_Y} Z"/>
  <path fill="{trim}" d="M{280-w} 548 Q{264-w} 610 {284-w} 658 L{292-w} 652 Q{278-w} 600 {286-w} 552 Z"/>
  <path fill="{trim}" d="M{520+w} 548 Q{536+w} 610 {516+w} 658 L{508+w} 652 Q{522+w} 600 {514+w} 552 Z"/>
  <circle fill="#e8c030" r="9" cy="568" cx="294"/><circle fill="#e8c030" r="9" cy="622" cx="290"/><circle fill="#e8c030" r="9" cy="676" cx="294"/>
  <circle fill="#e8c030" r="9" cy="568" cx="506"/><circle fill="#e8c030" r="9" cy="622" cx="510"/><circle fill="#e8c030" r="9" cy="676" cx="506"/>
  <path fill="#e8c030" d="M{290-w} 532 Q400 504 {510+w} 532 L{508+w} 538 Q400 512 {292-w} 538 Z"/>"""

    if look.era == "federal":
        return f"""
  <path fill="{main}" d="M{sl} {SHOULDER_Y} Q{lo} 668 {lo+2} {WAIST_Y-2} L{wl-2} {WAIST_Y} L{wr+2} {WAIST_Y} L{ro-2} {WAIST_Y-2} Q{sr} 668 {sr} {SHOULDER_Y} Z"/>
  <path fill="{main}" d="M{284-w} {SHOULDER_Y+4} Q{256-w} 662 {282-w} 788 Q{322} 872 {344-w} 682 Q400 562 {456+w} 682 Q{478} 872 {518+w} 788 Q{544+w} 662 {516+w} {SHOULDER_Y+4} Z"/>
  <path fill="{main}" d="M{284-w} 788 L{282-w} 792 Q{270-w} 862 {306} 898 L{318} {WAIST_Y} Z"/>
  <path fill="{main}" d="M{516+w} 788 L{518+w} 792 Q{530+w} 862 {494} 898 L{482} {WAIST_Y} Z"/>
  <path fill="{trim}" d="M{280-w} 548 Q{264-w} 610 {284-w} 658 L{290-w} 650 Q{272-w} 598 {286-w} 552 Z"/>
  <path fill="{trim}" d="M{520+w} 548 Q{536+w} 610 {516+w} 658 L{510+w} 650 Q{528+w} 598 {514+w} 552 Z"/>
  <circle fill="#e8c93a" r="8" cy="568" cx="298"/><circle fill="#e8c93a" r="8" cy="620" cx="295"/><circle fill="#e8c93a" r="8" cy="672" cx="298"/>
  <circle fill="#e8c93a" r="8" cy="568" cx="502"/><circle fill="#e8c93a" r="8" cy="620" cx="505"/><circle fill="#e8c93a" r="8" cy="672" cx="502"/>"""

    if look.era == "antebellum":
        tails = f"""
  <path fill="{main}" d="M{288-w} 788 L{282-w} 792 Q{270-w} 862 {306} 898 L{318} {WAIST_Y} Z"/>
  <path fill="{main}" d="M{512+w} 788 L{518+w} 792 Q{530+w} 862 {494} 898 L{482} {WAIST_Y} Z"/>"""
        lapels = "" if look.military else f"""
  <path fill="{trim}" d="M{288-w} 550 Q{276-w} 608 {290-w} 658 L{296-w} 648 Q{284-w} 592 {292-w} 548 Z"/>
  <path fill="{trim}" d="M{512+w} 550 Q{524+w} 608 {510+w} 658 L{504+w} 648 Q{516+w} 592 {508+w} 548 Z"/>"""
        buttons = "" if look.coat == "black" else """
  <circle fill="#d4b030" r="7" cy="574" cx="300"/><circle fill="#d4b030" r="7" cy="628" cx="297"/><circle fill="#d4b030" r="7" cy="682" cx="300"/>
  <circle fill="#d4b030" r="7" cy="574" cx="500"/><circle fill="#d4b030" r="7" cy="628" cx="503"/><circle fill="#d4b030" r="7" cy="682" cx="500"/>"""
        mil = """
  <path fill="#c8a030" d="M268 530 L292 514 L292 544 Z"/>
  <path fill="#c8a030" d="M532 530 L508 514 L508 544 Z"/>""" if look.military else ""
        return f"""
  <path fill="{main}" d="M{sl} {SHOULDER_Y} Q{lo} 662 {lo} {WAIST_Y} L{wl} {WAIST_Y} L{wr} {WAIST_Y} L{ro} {WAIST_Y} Q{sr} 662 {sr} {SHOULDER_Y} Z"/>
  <path fill="{main}" d="M{288-w} 522 Q{264-w} 662 {280-w} 790 Q{324} 868 {346-w} 686 Q400 558 {454+w} 686 Q{476} 868 {520+w} 790 Q{536+w} 662 {512+w} 522 Z"/>{tails}{lapels}{buttons}{mil}"""

    if look.era == "civil":
        return f"""
  <path fill="{main}" d="M{sl} {SHOULDER_Y} Q{lo} 658 {lo+2} {WAIST_Y} L{wl} {WAIST_Y} L{wr} {WAIST_Y} L{ro-2} {WAIST_Y} Q{sr} 658 {sr} {SHOULDER_Y} Z"/>
  <path fill="{main}" d="M{292-w} 518 Q{262-w} 658 276 786 Q{320} 872 {344-w} 682 Q400 536 {456+w} 682 Q{480} 872 {524+w} 786 Q{538+w} 658 {508+w} 518 Z"/>
  <path fill="#2a3040" d="M{330-w} 546 L400 564 L{470+w} 546 L{468+w} 552 L400 572 L{332-w} 552 Z"/>"""

    if look.era == "gilded":
        return f"""
  <path fill="{main}" d="M{sl} {SHOULDER_Y-4} Q{lo} 648 {lo} {WAIST_Y} L{wl} {WAIST_Y} L{wr} {WAIST_Y} L{ro} {WAIST_Y} Q{sr} 648 {sr} {SHOULDER_Y-4} Z"/>
  <path fill="{main}" d="M{298-w} 508 Q{272-w} 642 284 778 Q{328} 862 {348-w} 696 Q400 570 {452+w} 696 Q{474} 862 {516+w} 778 Q{528+w} 642 {502+w} 508 Z"/>"""

    if look.era == "progressive":
        return f"""
  <path fill="{main}" d="M{sl} {SHOULDER_Y-4} Q{lo} 638 {lo+2} {WAIST_Y} L{wl} {WAIST_Y} L{wr} {WAIST_Y} L{ro-2} {WAIST_Y} Q{sr} 638 {sr} {SHOULDER_Y-4} Z"/>
  <path fill="{main}" d="M{300-w} 506 Q{276-w} 638 288 772 Q{330} 858 {350-w} 700 Q400 566 {450+w} 700 Q{470} 858 {512+w} 772 Q{524+w} 638 {500+w} 506 Z"/>"""

    if look.era == "modern":
        return f"""
  <path fill="{main}" d="M{sl} {SHOULDER_Y} Q{lo} 632 {lo} {WAIST_Y} L{wl} {WAIST_Y} L{wr} {WAIST_Y} L{ro} {WAIST_Y} Q{sr} 632 {sr} {SHOULDER_Y} Z"/>
  <path fill="{main}" d="M{304-w} 502 Q{280-w} 632 292 768 Q{334} 852 {350-w} 696 Q400 566 {450+w} 696 Q{466} 852 {508+w} 768 Q{520+w} 632 {496+w} 502 Z"/>"""

    return f"""
  <path fill="{main}" d="M{sl} {SHOULDER_Y} Q{lo} 628 {lo} {WAIST_Y} L{wl} {WAIST_Y} L{wr} {WAIST_Y} L{ro} {WAIST_Y} Q{sr} 628 {sr} {SHOULDER_Y} Z"/>
  <path fill="{main}" d="M{306-w} 498 Q{282-w} 625 294 755 Q{336} 838 {352-w} 690 Q400 564 {448+w} 690 Q{464} 838 {506+w} 755 Q{518+w} 625 {494+w} 498 Z"/>"""


def neckwear_layer(look: Look) -> str:
    n = look.neckwear
    cy = COLLAR_Y
    base = (
        f'<path fill="{SHIRT_COLLAR}" d="M362 {cy} Q400 {cy - 12} 438 {cy} '
        f"L434 {cy + 20} Q400 {cy + 30} 366 {cy + 20} Z\"/>"
    )
    if n == "cravat":
        cravat = path_closed("M374 468 Q400 494 426 468 Q420 512 400 526 Q380 512 374 468")
        fold = path_closed("M388 498 Q400 508 412 498 L412 504 Q400 512 388 504")
        return base + f"""
  <path fill="#f8f4ec" d="{cravat}"/>
  <path fill="#e0d8cc" d="{fold}"/>"""
    if n == "ascot":
        ascot = path_closed("M366 464 Q400 502 434 464 Q428 492 400 510 Q372 492 366 464")
        return base + f"""
  <path fill="#f2ece2" d="{ascot}"/>"""
    if n == "bow_tie":
        return base + """
  <path fill="#1a1a1a" d="M372 476 Q386 464 400 476 Q414 464 428 476 Q414 488 400 482 Q386 488 372 476"/>"""
    if n == "tie_long":
        return base + """
  <path fill="#c41e3a" d="M384 496 Q400 646 400 736 Q400 646 416 496 Z"/>
  <path fill="#b01830" d="M376 492 L424 492 L420 502 L380 502 Z"/>"""
    tie = "#8b2020" if look.coat in ("charcoal", "black", "navy") else "#1e3a6b"
    return base + f"""
  <path fill="{tie}" d="M388 498 Q400 512 412 498 L409 504 Q400 514 391 504 Z"/>
  <path fill="{tie}" d="M384 502 Q400 686 400 750 Q400 686 416 502 Z"/>"""


def shirt_collar(look: Look) -> str:
    return ""


def military_extras(look: Look) -> str:
    parts: list[str] = []
    if look.military and look.era == "colonial":
        parts.append("""
  <ellipse transform="rotate(-25 275 515)" fill="#d4b030" ry="16" rx="42" cy="515" cx="275"/>
  <ellipse transform="rotate(25 525 515)" fill="#d4b030" ry="16" rx="42" cy="515" cx="525"/>""")
    if look.sword:
        parts.append("""
  <rect transform="rotate(35 580 800)" fill="#b89740" height="55" width="18" y="780" x="575"/>
  <path fill="#b89740" d="M565 790 Q590 775 615 795 L608 802 Q585 788 562 798 Z"/>
  <path fill="#d4d4d4" d="M590 775 L710 650 L705 655 L588 782 Z"/>
  <path fill="#a8a8a8" d="M592 778 L708 652 L704 658 L590 784 Z"/>""")
    if look.filename == "Washington":
        parts.append("""
  <circle fill="#9c2a2a" r="20" cy="228" cx="468"/>
  <circle fill="#e8c030" r="12" cy="228" cx="468"/>""")
    return "".join(parts)


def vest_color_for(look: Look) -> str:
    if look.era == "colonial":
        return VEST["buff"]
    if look.era == "federal":
        return VEST["cream"]
    if look.era == "antebellum":
        return VEST["gold"] if look.coat != "black" else VEST["burgundy"]
    if look.era == "civil":
        return VEST["charcoal_vest"]
    if look.era == "gilded":
        return VEST["burgundy"]
    if look.era == "progressive":
        return VEST["stripe"]
    return VEST["cream"]


def render_clothing(look: Look, main: str, trim: str, s: tuple, _shirt: str) -> str:
    parts: list[str] = [shoes(look)]

    if uses_breeches(look):
        parts.append(legs_breeches_stockings(look, s))
    else:
        parts.append(legs_trousers(look, trouser_color(look, main)))

    parts.append(waist_band(look, trouser_color(look, main) if not uses_breeches(look) else s[1]))
    parts.append(torso_base(look, s))
    parts.append(shirt_layer(look))
    if shows_vest(look):
        parts.append(waistcoat(look, vest_color_for(look)))

    parts.append(arms_for_era(look, s, main))
    parts.append(coat_for_era(look, main, trim))
    parts.append(neckwear_layer(look))
    parts.append(shirt_collar(look))
    parts.append(military_extras(look))

    return "\n".join(parts)
