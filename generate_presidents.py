#!/usr/bin/env python3
"""Generate photo-informed full-body president SVGs."""

from __future__ import annotations

import os

from era_clothing import COLLAR_Y, SHIRT_COLLAR, neck_geometry, render_clothing
from mesh_ready import finalize_svg_for_3d, path_closed
from presidents_look import LOOKS, Look

VIEWBOX = "0 0 800 1200"
GREEN_BACKGROUND = "#3cb868"  # uniform chroma-friendly green for all presidents

COAT_COLORS = {
    "blue_frock": ("#2a4a8c", "#1e3a6b", "#9c2a2a"),
    "black": ("#1a2333", "#111820", "#8b2020"),
    "charcoal": ("#2c3444", "#1a2028", "#7a2828"),
    "brown": ("#4a3528", "#352418", "#8b3020"),
    "navy": ("#1e2d4a", "#141e32", "#7a2828"),
}

SKIN = {
    "fair": ("#f8e4c8", "#f0d8b8", "#deb97c", "#f8f1e0", "#e8c8a8", "#c88c70"),
    "ruddy": ("#f0d0b8", "#e8c4a8", "#deb97c", "#f8f1e0", "#e0b898", "#c08068"),
    "olive": ("#e8d0b0", "#dcc0a0", "#c8a878", "#f0e8d8", "#d8b090", "#b88868"),
    "weathered": ("#e8d4b8", "#dcc8a8", "#c8b090", "#f0e4d0", "#d0b898", "#b89070"),
    "tan": ("#e8c8a0", "#dcb890", "#c8a070", "#f0e0c8", "#d0a880", "#b87858"),
    "brown_medium": ("#c89660", "#b88850", "#a87848", "#d4a574", "#c8a080", "#a06850"),
    "brown_dark": ("#8d5524", "#7a4818", "#6b3c14", "#a07050", "#a07050", "#6b4028"),
}

FACE = {
    "oval": (68, 78, 360),
    "round": (72, 76, 362),
    "long": (64, 82, 358),
    "gaunt": (62, 80, 358),
    "jowly": (74, 76, 365),
    "broad": (70, 74, 362),
}

BUILD_SCALE = {
    "short": 0.88,
    "thin": 0.94,
    "average": 1.0,
    "athletic": 1.0,
    "stocky": 1.06,
    "portly": 1.14,
}


def skin_tones(look: Look) -> tuple[str, str, str, str, str, str]:
    return SKIN.get(look.skin, SKIN["fair"])


def face_ellipse(look: Look) -> tuple[int, int, int]:
    return FACE.get(look.face_shape, FACE["oval"])


def render_hair(look: Look, hc: str, head: str) -> str:
    h = look.hair_style
    if h == "powdered_tied":
        return f"""
  <path fill="{hc}" d="M335 295 Q280 315 268 370 Q278 400 350 405"/>
  <path fill="{hc}" d="M465 295 Q520 315 532 370 Q522 400 450 405"/>
  <ellipse fill="{hc}" ry="40" rx="90" cy="252" cx="400"/>
  <path fill="{hc}" d="M455 250 Q520 280 540 340 Q530 380 480 400 Q460 320 455 250"/>"""
    if h in ("powdered_short", "powdered_tied"):
        return f"""
  <path fill="#f8f6f0" d="M335 290 Q280 310 265 380 Q280 410 355 415"/>
  <path fill="#f8f6f0" d="M465 290 Q520 310 535 380 Q520 410 445 415"/>
  <ellipse fill="{hc}" ry="42" rx="92" cy="248" cx="400"/>
  <path fill="#1e1e1e" d="M305 245 Q260 210 290 170 Q400 145 510 170 Q540 210 495 245"/>"""
    if h == "bald_fringe":
        return f"""
  <path fill="{hc}" d="M318 300 Q300 340 305 390 Q330 400 355 395"/>
  <path fill="{hc}" d="M482 300 Q500 340 495 390 Q470 400 445 395"/>
  <ellipse fill="{hc}" ry="14" rx="75" cy="268" cx="400"/>"""
    if h == "bald_side_whiskers":
        return f"""
  <path fill="{hc}" d="M312 310 Q285 360 290 430 Q320 440 350 420"/>
  <path fill="{hc}" d="M488 310 Q515 360 510 430 Q480 440 450 420"/>
  <ellipse fill="{hc}" ry="10" rx="70" cy="272" cx="400"/>"""
    if h == "reddish_tied":
        return f"""
  <path fill="{hc}" d="M332 292 Q278 312 270 368 Q288 398 352 402"/>
  <path fill="{hc}" d="M468 292 Q522 312 530 368 Q512 398 448 402"/>
  <ellipse fill="{hc}" ry="38" rx="88" cy="250" cx="400"/>
  <path fill="{hc}" d="M450 248 Q510 275 528 335 Q500 375 465 395"/>"""
    if h == "white_wild":
        return f"""
  <path fill="{hc}" d="M325 270 Q260 290 255 360 Q275 400 340 395"/>
  <path fill="{hc}" d="M475 270 Q540 290 545 360 Q525 400 460 395"/>
  <ellipse fill="{hc}" ry="48" rx="95" cy="235" cx="400"/>"""
    if h == "sideburns_bald":
        return f"""
  <path fill="{hc}" d="M305 305 Q275 370 285 450 Q320 455 350 420"/>
  <path fill="{hc}" d="M495 305 Q525 370 515 450 Q480 455 450 420"/>
  <ellipse fill="{head}" ry="8" rx="72" cy="278" cx="400"/>"""
    if h in ("gray_thin", "gray_short", "receding_gray", "sandy_balding", "sandy_thin"):
        return f"""
  <path fill="{hc}" d="M332 298 Q288 318 282 368 Q298 395 348 398"/>
  <path fill="{hc}" d="M468 298 Q512 318 518 368 Q502 395 452 398"/>
  <ellipse fill="{hc}" ry="22" rx="72" cy="262" cx="400"/>"""
    if h == "dark_neat":
        return f"""
  <path fill="{hc}" d="M334 296 Q290 312 286 362 Q300 388 348 392"/>
  <path fill="{hc}" d="M466 296 Q510 312 514 362 Q500 388 452 392"/>
  <ellipse fill="{hc}" ry="30" rx="82" cy="255" cx="400"/>"""
    if h == "dark_wavy":
        return f"""
  <path fill="{hc}" d="M328 288 Q275 308 268 358 Q285 392 345 398"/>
  <path fill="{hc}" d="M472 288 Q525 308 532 358 Q515 392 455 398"/>
  <ellipse fill="{hc}" ry="34" rx="86" cy="248" cx="400"/>"""
    if h == "white_full":
        return f"""
  <path fill="{hc}" d="M330 285 Q270 305 265 365 Q285 400 350 402"/>
  <path fill="{hc}" d="M470 285 Q530 305 535 365 Q515 400 450 402"/>
  <ellipse fill="{hc}" ry="36" rx="90" cy="245" cx="400"/>"""
    if h == "black_tousled":
        if look.top_hat:
            return _lincoln_hair_under_hat(hc, look)
        return f"""
  <path fill="{hc}" d="M328 278 Q275 295 270 350 Q288 382 342 388"/>
  <path fill="{hc}" d="M472 278 Q525 295 530 350 Q512 382 458 388"/>
  <ellipse fill="{hc}" ry="28" rx="85" cy="248" cx="400"/>"""
    if h == "dark_receding":
        return f"""
  <path fill="{hc}" d="M338 300 Q300 320 298 370 Q315 392 355 390"/>
  <path fill="{hc}" d="M462 300 Q500 320 502 370 Q485 392 445 390"/>
  <ellipse fill="{hc}" ry="16" rx="68" cy="272" cx="400"/>"""
    if h in ("short_dark", "wavy_brown"):
        return f"""
  <path fill="{hc}" d="M330 292 Q285 310 280 360 Q295 388 345 392"/>
  <path fill="{hc}" d="M470 292 Q515 310 520 360 Q505 388 455 392"/>
  <ellipse fill="{hc}" ry="28" rx="84" cy="252" cx="400"/>"""
    if h == "mutton_chop_top":
        return f"""
  <ellipse fill="{head}" ry="12" rx="70" cy="275" cx="400"/>"""
    if h == "gray_parted":
        return f"""
  <path fill="{hc}" d="M335 292 Q290 308 285 358 Q300 385 348 388"/>
  <path fill="{hc}" d="M465 292 Q510 308 515 358 Q500 385 452 388"/>
  <ellipse fill="{hc}" ry="30" rx="85" cy="250" cx="400"/>
  <line stroke="{hc}" stroke-width="3" x1="400" y1="220" x2="400" y2="280"/>"""
    if h == "gray_stiff":
        return f"""
  <path fill="{hc}" d="M332 290 Q285 305 280 352 Q295 380 345 385"/>
  <path fill="{hc}" d="M468 290 Q515 305 520 352 Q505 380 455 385"/>
  <ellipse fill="{hc}" ry="26" rx="80" cy="252" cx="400"/>"""
    if h == "gray_temples":
        return f"""
  <path fill="{hc}" d="M332 295 Q288 312 285 358 Q300 382 345 385"/>
  <path fill="{hc}" d="M468 295 Q512 312 515 358 Q500 382 455 385"/>
  <ellipse fill="#5a5048" ry="28" rx="82" cy="252" cx="400"/>
  <path fill="{hc}" d="M318 310 Q305 340 310 365"/><path fill="{hc}" d="M482 310 Q495 340 490 365"/>"""
    if h == "gray_thin":
        return f"""
  <path fill="{hc}" d="M334 298 Q292 315 288 360 Q302 382 348 385"/>
  <path fill="{hc}" d="M466 298 Q508 315 512 360 Q498 382 452 385"/>
  <ellipse fill="{hc}" ry="24" rx="78" cy="254" cx="400"/>"""
    if h == "bald":
        return f"""
  <ellipse fill="{head}" ry="18" rx="78" cy="268" cx="400"/>
  <ellipse fill="#d8d4cc" ry="12" rx="55" cy="258" cx="400"/>"""
    if h == "brown_parted":
        return f"""
  <path fill="{hc}" d="M334 288 Q288 302 282 348 Q298 378 348 382"/>
  <path fill="{hc}" d="M466 288 Q512 302 518 348 Q502 378 452 382"/>
  <ellipse fill="{hc}" ry="32" rx="86" cy="246" cx="400"/>
  <line stroke="{hc}" stroke-width="4" x1="400" y1="215" x2="400" y2="275"/>"""
    if h == "slicked_gray":
        return f"""
  <path fill="{hc}" d="M330 285 Q275 300 268 345 Q285 375 345 378"/>
  <path fill="{hc}" d="M470 285 Q525 300 532 345 Q515 375 455 378"/>
  <ellipse fill="{hc}" ry="26" rx="84" cy="248" cx="400"/>"""
    if h == "gray_full":
        return f"""
  <path fill="{hc}" d="M328 286 Q272 302 265 352 Q282 382 342 386"/>
  <path fill="{hc}" d="M472 286 Q528 302 535 352 Q518 382 458 386"/>
  <ellipse fill="{hc}" ry="32" rx="88" cy="246" cx="400"/>"""
    if h == "swept_back":
        return f"""
  <path fill="{hc}" d="M328 282 Q270 298 262 340 Q278 368 340 372"/>
  <path fill="{hc}" d="M472 282 Q530 298 538 340 Q522 368 460 372"/>
  <ellipse fill="{hc}" ry="28" rx="86" cy="244" cx="400"/>"""
    if h == "thin_gray":
        return f"""
  <path fill="{hc}" d="M336 292 Q298 308 294 352 Q308 378 352 380"/>
  <path fill="{hc}" d="M464 292 Q502 308 506 352 Q492 378 448 380"/>
  <ellipse fill="{hc}" ry="22" rx="76" cy="256" cx="400"/>"""
    if h == "gray_wavy":
        return f"""
  <path fill="{hc}" d="M326 284 Q268 300 260 348 Q278 378 338 382"/>
  <path fill="{hc}" d="M474 284 Q532 300 540 348 Q522 378 462 382"/>
  <ellipse fill="{hc}" ry="30" rx="88" cy="246" cx="400"/>"""
    if h == "short_black":
        return f"""
  <path fill="{hc}" d="M334 292 Q290 308 286 352 Q300 378 348 380"/>
  <path fill="{hc}" d="M466 292 Q510 308 514 352 Q500 378 452 380"/>
  <ellipse fill="{hc}" ry="22" rx="78" cy="254" cx="400"/>"""
    if h == "blonde_combover":
        return f"""
  <path fill="{hc}" d="M300 260 Q350 220 420 235 Q480 250 500 290 Q470 310 400 295 Q330 310 300 260"/>
  <path fill="{hc}" d="M330 295 Q290 315 288 355 Q305 378 350 378"/>
  <path fill="{hc}" d="M470 295 Q510 315 512 355 Q495 378 450 378"/>
  <ellipse fill="{hc}" ry="20" rx="75" cy="268" cx="400"/>"""
    # default short
    return f"""
  <path fill="{hc}" d="M334 294 Q288 310 284 360 Q298 386 348 390"/>
  <path fill="{hc}" d="M466 294 Q512 310 516 360 Q502 386 452 390"/>
  <ellipse fill="{hc}" ry="28" rx="82" cy="252" cx="400"/>"""


def render_facial_hair(look: Look, hc: str) -> str:
    fh = look.facial_hair
    if fh == "beard_lincoln":
        return f"""
  <path fill="{hc}" d="{path_closed('M338 388 Q345 445 365 468 Q400 478 435 468 Q458 440 462 388')}"/>"""
    if fh == "beard_full":
        return f"""
  <path fill="{hc}" d="M328 382 Q335 450 365 472 Q400 480 435 472 Q465 445 472 382"/>
  <path fill="{hc}" d="M328 278 Q275 298 270 358 Q288 388 328 382"/>
  <path fill="{hc}" d="M472 278 Q525 298 530 358 Q512 388 472 382"/>"""
    if fh == "beard_full_gray":
        return f"""
  <path fill="{hc}" d="M330 380 Q338 448 368 470 Q400 478 432 470 Q462 442 470 380"/>
  <path fill="{hc}" d="M330 282 Q278 302 272 360 Q290 390 330 380"/>
  <path fill="{hc}" d="M470 282 Q522 302 528 360 Q510 390 470 380"/>"""
    if fh == "mustache_thin":
        return f"""
  <path fill="{hc}" d="M372 402 Q400 410 428 402 Q425 406 400 408 Q375 406 372 402 Z"/>"""
    if fh == "mustache_full":
        return f"""
  <path fill="{hc}" d="M362 398 Q400 412 438 398 Q435 405 400 410 Q365 405 362 398"/>"""
    if fh == "mutton_chops":
        return f"""
  <path fill="{hc}" d="M302 310 Q268 380 275 455 Q310 460 345 420"/>
  <path fill="{hc}" d="M498 310 Q532 380 525 455 Q490 460 455 420"/>"""
    return ""


def render_glasses(look: Look) -> str:
    g = look.glasses
    if g == "round":
        return """
  <ellipse fill="#2a3038" ry="19" rx="23" cy="348" cx="368"/>
  <ellipse fill="#9ec4e0" ry="14" rx="18" cy="348" cx="368"/>
  <ellipse fill="#2a3038" ry="19" rx="23" cy="348" cx="432"/>
  <ellipse fill="#9ec4e0" ry="14" rx="18" cy="348" cx="432"/>
  <path fill="#2a3038" d="M389 346 L411 346 L411 350 L389 350 Z"/>"""
    if g == "pince_nez":
        return """
  <ellipse fill="#222" ry="16" rx="20" cy="346" cx="372"/>
  <ellipse fill="#88b0c8" ry="11" rx="15" cy="346" cx="372"/>
  <ellipse fill="#222" ry="16" rx="20" cy="346" cx="428"/>
  <ellipse fill="#88b0c8" ry="11" rx="15" cy="346" cx="428"/>
  <path fill="#222" d="M390 346 Q400 338 410 346 L408 350 Q400 344 392 350 Z"/>
  <path fill="#222" d="M398 328 L402 328 L402 338 L398 338 Z"/>"""
    if g == "aviator":
        return """
  <path fill="#1a1a1a" d="M348 340 Q368 320 392 340 Q392 360 368 365 Q348 360 348 340 Z"/>
  <path fill="#a8c8e0" d="M354 342 Q368 328 386 342 Q386 354 368 358 Q354 354 354 342 Z"/>
  <path fill="#1a1a1a" d="M452 340 Q432 320 408 340 Q408 360 432 365 Q452 360 452 340 Z"/>
  <path fill="#a8c8e0" d="M446 342 Q432 328 414 342 Q414 354 432 358 Q446 354 446 342 Z"/>
  <path fill="#1a1a1a" d="M392 346 L408 346 L408 350 L392 350 Z"/>"""
    if g == "rectangular":
        return """
  <rect fill="#333" rx="4" height="36" width="42" y="330" x="346"/>
  <rect fill="#9ec4e0" rx="2" height="26" width="32" y="335" x="351"/>
  <rect fill="#333" rx="4" height="36" width="42" y="330" x="412"/>
  <rect fill="#9ec4e0" rx="2" height="26" width="32" y="335" x="417"/>
  <path fill="#333" d="M386 346 L414 346 L414 350 L386 350 Z"/>"""
    return ""


def render_nose(look: Look, nose_color: str) -> str:
    n = look.nose
    shade = nose_color
    if n == "roman":
        return f'<path fill="{shade}" d="M400 352 Q408 378 402 392 Q398 388 396 368 Q398 358 400 352 Z"/>'
    if n == "prominent":
        return f'<path fill="{shade}" d="M400 350 Q395 382 392 398 Q398 394 402 368 Q401 358 400 350 Z"/>'
    if n == "wide":
        return f'<path fill="{shade}" d="M398 355 Q400 385 396 392 Q392 382 394 362 Q396 355 398 355 Z"/>'
    return f'<path fill="{shade}" d="M400 355 Q398 385 395 390 Q397 372 399 358 Q400 355 400 355 Z"/>'


def render_brows(look: Look) -> str:
    if look.brows == "heavy":
        return """
  <path fill="#2c2c2c" d="M350 318 Q378 308 395 322 Q392 328 370 326 Q352 324 350 318 Z"/>
  <path fill="#2c2c2c" d="M405 322 Q422 308 450 318 Q448 324 426 326 Q408 328 405 322 Z"/>"""
    if look.brows == "thin":
        return """
  <path fill="#4a4a4a" d="M358 322 Q378 318 392 322 Q390 326 372 326 Q360 325 358 322 Z"/>
  <path fill="#4a4a4a" d="M408 322 Q422 318 442 322 Q440 326 422 326 Q410 325 408 322 Z"/>"""
    return """
  <path fill="#2c2c2c" d="M355 325 Q375 315 390 320 Q388 326 368 324 Q356 326 355 325 Z"/>
  <path fill="#2c2c2c" d="M410 320 Q425 315 445 325 Q443 331 423 328 Q412 326 410 320 Z"/>"""


def render_ears(look: Look, head: str) -> str:
    if look.ears != "prominent":
        return ""
    return f"""
  <ellipse fill="{head}" ry="22" rx="12" cy="362" cx="318"/>
  <ellipse fill="{head}" ry="22" rx="12" cy="362" cx="482"/>"""


def render_face_extras(look: Look, head: str) -> str:
    extras = ""
    if look.name == "Abraham Lincoln":
        extras += """
  <circle fill="#3a2820" r="3" cy="378" cx="428"/>"""
    if look.build == "short":
        extras += """
  <!-- shorter stature -->"""
    return extras


def _lincoln_hair_under_hat(hc: str, look: Look) -> str:
    """Sideburns only — hair stays below the hat brim (Lincoln)."""
    rx, ry, cy = face_ellipse(look)
    brim_y = cy - ry + 12
    temple_y = cy - int(ry * 0.12)
    jaw_side = cy + int(ry * 0.42)
    ear_top = brim_y + 4
    return f"""
  <path fill="{hc}" d="M{400 - rx - 4} {ear_top} Q{352} {temple_y} {336} {cy + 6} Q{328} {cy + 26} {344} {jaw_side} L{358} {ear_top + 6} Z"/>
  <path fill="{hc}" d="M{400 + rx + 4} {ear_top} Q{448} {temple_y} {464} {cy + 6} Q{472} {cy + 26} {456} {jaw_side} L{442} {ear_top + 6} Z"/>"""


def top_hat_crown(cy: int, ry: int, rx: int) -> str:
    brim_y = cy - ry + 12
    crown_top = max(68, brim_y - 192)
    crown_h = brim_y - crown_top
    band_y = brim_y - 22
    x0 = 400 - 61
    return f"""
  <rect fill="#141414" x="{x0}" y="{crown_top}" width="122" height="{crown_h}" rx="5"/>
  <rect fill="#2a2a2a" x="{x0 + 4}" y="{band_y}" width="114" height="11" rx="2"/>"""


def top_hat_brim(cy: int, ry: int, rx: int) -> str:
    brim_y = cy - ry + 12
    brim_rx = rx + 50
    return f"""
  <ellipse fill="#0a0a0a" cx="400" cy="{brim_y}" rx="{brim_rx}" ry="12"/>
  <path fill="#1c1c1c" d="M{400 - brim_rx} {brim_y - 5} Q400 {brim_y - 12} {400 + brim_rx} {brim_y - 5} L{400 + brim_rx - 5} {brim_y + 7} Q400 {brim_y + 15} {400 - brim_rx + 5} {brim_y + 7} Z"/>"""


def top_hat(look: Look, cy: int, ry: int, rx: int) -> str:
    if not look.top_hat:
        return ""
    return top_hat_crown(cy, ry, rx) + top_hat_brim(cy, ry, rx)


def hair_temple_band(look: Look, hc: str, head: str, cy: int, ry: int) -> str:
    """Connects side hair paths to the face (closed region for 3D)."""
    if look.top_hat or look.hair_style in ("bald", "mutton_chop_top", "sideburns_bald"):
        return ""
    y = cy + int(ry * 0.52)
    return f"""
  <path fill="{hc}" d="M330 {y} Q400 {y + 18} 470 {y} L468 {y + 28} Q400 {y + 38} 332 {y + 28} Z"/>
  <ellipse fill="{head}" ry="{int(ry * 0.22)}" rx="{int(ry * 0.55)}" cy="{y + 12}" cx="400"/>"""


def render_neck(look: Look, head: str, cy: int, ry: int, rx: int) -> str:
    """Neck from jaw line into shirt collar (aligned with era_clothing COLLAR_Y)."""
    top, bottom, w = neck_geometry(look, cy, ry, rx)
    collar_mid = COLLAR_Y + 14
    return f"""
  <path fill="{head}" d="M{400 - w} {top} Q{400 - w - 2} {(top + bottom) // 2} {400 - 12} {bottom} Q400 {bottom + 6} {400 + 12} {bottom} Q{400 + w + 2} {(top + bottom) // 2} {400 + w} {top} Q400 {top - 3} {400 - w} {top} Z"/>
  <path fill="{SHIRT_COLLAR}" d="M{400 - w - 4} {bottom - 2} Q400 {collar_mid} {400 + w + 4} {bottom - 2} L{400 + w + 2} {bottom + 4} Q400 {collar_mid + 4} {400 - w - 2} {bottom + 4} Z"/>"""


def head_face(look: Look, s: tuple) -> str:
    head, hand, _, _, nose_c, mouth_c = s
    rx, ry, cy = face_ellipse(look)
    hc = look.hair_color
    neck = render_neck(look, head, cy, ry, rx)
    mouth = f'<path fill="{mouth_c}" d="M375 408 Q400 418 425 408 Q420 412 400 414 Q380 412 375 408 Z"/>'

    hair = render_hair(look, hc, head)
    beard = render_facial_hair(look, hc)
    if look.top_hat:
        face_stack = f"""{hair}
  {top_hat_crown(cy, ry, rx)}
  {beard}
  {top_hat_brim(cy, ry, rx)}"""
    else:
        face_stack = f"""{hair_temple_band(look, hc, head, cy, ry)}
  {hair}
  {beard}"""

    return f"""
  <ellipse fill="{head}" ry="{ry}" rx="{rx}" cy="{cy}" cx="400"/>
  {neck}
  {face_stack}
  {render_ears(look, head)}
  <ellipse fill="#1a2a4a" ry="13" rx="8" cy="348" cx="372"/>
  <ellipse fill="#1a2a4a" ry="13" rx="8" cy="348" cx="428"/>
  {render_brows(look)}
  {render_nose(look, nose_c)}
  {mouth}
  {render_face_extras(look, head)}
  {render_glasses(look)}
"""


def generate(look: Look) -> str:
    main, _, trim = COAT_COLORS.get(look.coat, COAT_COLORS["charcoal"])
    s = skin_tones(look)
    shirt = "#f5f2ea"  # passed to render_clothing for API compat; layers use SHIRT constant
    desc = (
        f"Vector illustration of {look.name}, {ordinal(look.number)} President "
        f"of the United States — likeness informed by historical photographs and portraits"
    )

    raw = f'''<svg aria-labelledby="title desc" xmlns="http://www.w3.org/2000/svg" viewBox="{VIEWBOX}" height="1200" width="800" shape-rendering="geometricPrecision">
  <title>Highly Detailed Full-Body {look.name} SVG</title>
  <desc id="desc">{desc}</desc>
  <metadata>Mesh-ready export: closed opaque paths, connected figure for PNG and image-to-3D.</metadata>

  <g id="background">
    <rect fill="{GREEN_BACKGROUND}" height="1200" width="800"/>
  </g>
  <g id="figure" fill-rule="nonzero">
{render_clothing(look, main, trim, s, shirt)}
{head_face(look, s)}
  </g>
</svg>
'''
    return finalize_svg_for_3d(raw)


def ordinal(n: int) -> str:
    suffix = "th"
    if n % 100 not in (11, 12, 13):
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


OUTPUT_SUBDIR = "generated"


def output_filename(look: Look) -> str:
    """Numbered label for filesystem: '01 - George Washington.svg'."""
    return f"{look.number:02d} - {look.name}.svg"


def main(output_subdir: str = OUTPUT_SUBDIR) -> None:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(base_dir, output_subdir)
    os.makedirs(out_dir, exist_ok=True)

    # Remove prior exports (numbered or legacy short names)
    for name in os.listdir(out_dir):
        if name.endswith(".svg"):
            os.remove(os.path.join(out_dir, name))

    seen: set[int] = set()
    count = 0
    for look in LOOKS:
        if look.number in seen:
            continue
        seen.add(look.number)
        path = os.path.join(out_dir, output_filename(look))
        with open(path, "w", encoding="utf-8") as f:
            f.write(generate(look))
        print(f"Wrote {path}")
        count += 1
    print(f"Done. Wrote {count} SVGs to {out_dir}/")


if __name__ == "__main__":
    import sys

    subdir = sys.argv[1] if len(sys.argv) > 1 else OUTPUT_SUBDIR
    main(subdir)
