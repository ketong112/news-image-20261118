#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news front page, 1024x1024 PNG.

ATM study (leaderboard, 18 Nov 2026 ~21:10 WIB): the top entries pack
35-45 stories on one page — 3 big illustrated leads, 6-10 medium stories,
a "By the numbers" strip, a dotted world map with numbered pins, and a long
"Also on ..." briefs list. This page follows that winning shape with 35
stories: 9 featured + 26 briefs, 6 continents, one world map.

All 35 stories verified against the day's digests (One Turn News 48-story
roundup, Just Security Early Edition, Zark News, Horizon):
  Featured: Gulf strikes (US hits Qeshm, Iran drones at Bahrain/Kuwait);
  Kerch bridge span falls; Xi-Putin-Trump APEC Shenzhen; Peltola wins
  Alaska, Senate 56-44; Congo Ebola passes 11,000 cases; Cyclone Akvan
  bears down on India; stocks fall on Gulf tensions; Board of Peace warns
  Gaza truce may collapse; Fiji declares disaster over El Nino drought.
  Briefs: Nvidia, Knesset/Kahana, US-Ukraine deep strikes, measles,
  Voyager 1, Siberia plane crash, Cyclone Xavier, Myanmar genocide case,
  MQ-9 drone, PNG and Romania quakes, Trump-Manila, US tech outages,
  Myanmar-ASEAN, UK spy case, EU-Rwanda return hubs, Trump plot sentence,
  Awa group emerges in Amazon, Sozcu TV, Serbia parliament, Eritrea
  clashes, South Korea growth, France-Malaysia rare earths, US chip rules,
  Anthropic Nasdaq, Fela Kuti Hall of Fame.

Deterministic: fixed text, fixed layout, no randomness, no timestamps.
Run: python3 draw_image.py  ->  writes entry.png next to this file.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (20, 20, 20)
RED = (178, 34, 34)
DARKRED = (120, 20, 22)
NAVY = (29, 58, 130)
TEAL = (13, 110, 110)
MAROON = (120, 30, 70)
GREY = (92, 86, 74)
SKY = (214, 230, 240)
SEA = (198, 220, 235)
LAND = (196, 178, 140)
GREEN = (34, 110, 60)
GOLD = (176, 124, 24)
BROWN = (140, 82, 30)
BODY = (60, 56, 48)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def font(name, size):
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}", size)


F_TOP = font("DejaVuSans-Bold.ttf", 20)
F_MAST = font("DejaVuSerif-Bold.ttf", 56)
F_TAG = font("DejaVuSans-Bold.ttf", 19)
F_TAG_SM = font("DejaVuSans-Bold.ttf", 16)
F_BIG_HEAD = font("DejaVuSans-Bold.ttf", 24)
F_BIG_BODY = font("DejaVuSans.ttf", 17)
F_MED_HEAD = font("DejaVuSans-Bold.ttf", 20)
F_MED_BODY = font("DejaVuSans.ttf", 16)
F_NUM = font("DejaVuSans-Bold.ttf", 30)
F_NUM_LBL = font("DejaVuSans.ttf", 15)
F_SEC = font("DejaVuSans-Bold.ttf", 19)
F_BRIEF = font("DejaVuSans.ttf", 13)
F_BRIEF_N = font("DejaVuSans-Bold.ttf", 13)
F_LEG = font("DejaVuSans.ttf", 13)
F_SRC = font("DejaVuSans.ttf", 15)


def wrap(text, f, max_w):
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(x, y, lines, f, fill, leading):
    for line in lines:
        d.text((x, y), line, font=f, fill=fill)
        y += leading
    return y


def fit(text, f, max_w):
    """Shorten with an ellipsis so the text fits max_w."""
    if d.textlength(text, font=f) <= max_w:
        return text
    while len(text) > 4 and d.textlength(text + "…", font=f) > max_w:
        text = text[:-1]
    return text + "…"


MX = 36
RX = W - MX

# ---- Masthead --------------------------------------------------------------
d.text((MX, 12), "THE DAY IN WORLD NEWS", font=F_TOP, fill=GREY)
right = "35 STORIES  •  6 CONTINENTS  •  ONE DAY"
rw = d.textlength(right, font=F_TOP)
d.text((RX - rw, 12), right, font=F_TOP, fill=RED)
title = "Wednesday 18 November 2026"
tw = d.textlength(title, font=F_MAST)
d.text(((W - tw) / 2, 38), title, font=F_MAST, fill=INK)
d.line([(MX, 106), (RX, 106)], fill=INK, width=3)

# ---- Illustration helpers ---------------------------------------------------
def gulf_map(x, y, w, h):
    """Schematic of the Gulf: sea, land, strait, three red dots."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.polygon([(x, y), (x + w, y), (x + w, y + 26), (x + w * 0.62, y + 40),
               (x + w * 0.55, y + h), (x, y + h)], fill=(232, 214, 178))
    d.polygon([(x + w * 0.55, y + 52), (x + w, y + 34), (x + w, y + h),
               (x + w * 0.72, y + h)], fill=(222, 200, 160))
    d.text((x + 8, y + 6), "IRAN", font=F_LEG, fill=GREY)
    d.text((x + w - 52, y + h - 20), "ARABIA", font=F_LEG, fill=GREY)
    d.text((x + w - 66, y + 30), "HORMUZ", font=F_LEG, fill=NAVY)
    for (px, py, lbl) in [(0.46, 0.42, "QESHM"), (0.22, 0.52, "BAHRAIN"),
                          (0.30, 0.30, "KUWAIT")]:
        cx, cy = x + w * px, y + h * py
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED)
        d.text((cx + 9, cy - 8), lbl, font=F_LEG, fill=INK)


def kerch_bridge(x, y, w, h):
    """Bridge deck with one arch standing, one span fallen into the sea."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 232, 238))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(120, 160, 195))
    d.rectangle([x, y + h - 30, x + w, y + h - 26], fill=(90, 90, 90))
    d.arc([x + 18, y + 18, x + 118, y + h - 20], 180, 360, fill=INK, width=4)
    d.line([(x + 68, y + 18), (x + 68, y + h - 30)], fill=INK, width=4)
    d.arc([x + w - 118, y + 18, x + w - 18, y + h - 20], 180, 270,
          fill=INK, width=4)
    d.line([(x + w - 88, y + 62), (x + w - 48, y + h - 30)], fill=INK, width=4)
    d.polygon([(x + w - 118, y + h - 30), (x + w - 78, y + h - 8),
               (x + w - 62, y + h - 12)], fill=(70, 70, 70))
    d.text((x + 8, y + 6), "KERCH STRAIT", font=F_LEG, fill=GREY)


def apec_table(x, y, w, h):
    """Skyline, round table, three leaders."""
    d.rectangle([x, y, x + w, y + h], fill=(233, 228, 214))
    for (bx, bw, bh) in [(0, 34, 44), (40, 26, 62), (72, 40, 36),
                         (120, 30, 56), (158, 34, 40), (200, 28, 66),
                         (234, 36, 46), (276, 30, 58)]:
        d.rectangle([x + bx, y + h - 30 - bh, x + bx + bw, y + h - 30],
                    fill=(150, 148, 138))
    d.ellipse([x + 55, y + h - 34, x + w - 55, y + h - 8], fill=(196, 120, 40))
    for (cx, col) in [(0.28, RED), (0.5, NAVY), (0.72, DARKRED)]:
        px = x + w * cx
        d.ellipse([px - 9, y + h - 52, px + 9, y + h - 34], fill=col)
    d.text((x + 8, y + 6), "SHENZHEN", font=F_LEG, fill=GREY)


def icon_capitol(x, y, s, col):
    d.rectangle([x, y + s - 14, x + s, y + s], fill=col)
    d.pieslice([x + s * 0.28, y + 6, x + s * 0.72, y + s * 0.55], 180, 360,
               fill=(255, 255, 255))
    d.rectangle([x + s * 0.24, y + s * 0.5, x + s * 0.76, y + s * 0.62],
                fill=(255, 255, 255))
    d.line([(x + s * 0.5, y + 2), (x + s * 0.5, y + 12)], fill=(255, 255, 255),
           width=2)


def icon_virus(x, y, s, col):
    cx, cy, r = x + s / 2, y + s / 2, s * 0.26
    for ang in range(0, 360, 45):
        dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        d.line([(cx + dx * r, cy + dy * r), (cx + dx * (r + 9),
               cy + dy * (r + 9))], fill=col, width=3)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)


def icon_cyclone(x, y, s, col):
    cx, cy = x + s / 2, y + s / 2
    for r in (20, 14, 8):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=col, width=4)


def icon_chart(x, y, s, col):
    d.line([(x + 8, y + s - 10), (x + s - 8, y + s - 10)], fill=INK, width=2)
    d.line([(x + 8, y + s - 10), (x + 8, y + 8)], fill=INK, width=2)
    d.line([(x + 12, y + 18), (x + 22, y + 30), (x + 32, y + 26),
            (x + 44, y + 44)], fill=col, width=4)
    d.polygon([(x + 44, y + 44), (x + 50, y + 40), (x + 50, y + 50)],
              fill=col)


def icon_warning(x, y, s, col):
    d.polygon([(x + s / 2, y + 6), (x + s - 6, y + s - 8), (x + 6, y + s - 8)],
              fill=col)
    d.text((x + s / 2 - 4, y + s * 0.32), "!", font=font("DejaVuSans-Bold.ttf", 26),
           fill=(255, 255, 255))


def icon_drought(x, y, s, col):
    d.ellipse([x + 10, y + 8, x + 34, y + 32], fill=(232, 164, 32))
    d.line([(x + 8, y + s - 12), (x + s - 8, y + s - 12)], fill=BROWN, width=3)
    d.line([(x + 16, y + s - 12), (x + 24, y + s - 22)], fill=BROWN, width=2)
    d.line([(x + 34, y + s - 12), (x + 30, y + s - 20)], fill=BROWN, width=2)

# ---- Big stories ------------------------------------------------------------
BIG = [
    ("01", "MIDDLE EAST · IRAN WAR", RED, gulf_map,
     "U.S. strikes Qeshm, Iran hits back",
     "U.S. jets hit a missile site on Qeshm; Iran drones strike U.S. "
     "bases in Bahrain and Kuwait."),
    ("02", "EUROPE · UKRAINE WAR", NAVY, kerch_bridge,
     "Kerch bridge span falls into the sea",
     "Ukraine hits the Crimea bridge for a second day; part of its road "
     "span collapses into the strait."),
    ("03", "ASIA · DIPLOMACY", TEAL, apec_table,
     "Xi, Putin and Trump set for Shenzhen",
     "Xi and Putin open APEC against protectionism and sanctions; Trump "
     "joins the talks on Thursday."),
]
bx0, by0, bw, bgap = MX, 118, 310, 21
for i, (num, tag, color, draw, head, body) in enumerate(BIG):
    x = bx0 + i * (bw + bgap)
    draw(x, by0, bw, 94)
    d.text((x, by0 + 102), num, font=F_TAG, fill=RED)
    nw = d.textlength(num + "  ", font=F_TAG)
    d.text((x + nw, by0 + 102), tag, font=F_TAG, fill=color)
    hl = wrap(head, F_BIG_HEAD, bw)
    yy = text_block(x, by0 + 126, hl, F_BIG_HEAD, INK, 28)
    bl = wrap(body, F_BIG_BODY, bw)
    text_block(x, yy + 3, bl, F_BIG_BODY, BODY, 21)
d.line([(MX, 374), (RX, 374)], fill=INK, width=2)

# ---- Medium stories -----------------------------------------------------------
MED = [
    ("04", "AMERICAS · POLITICS", MAROON, icon_capitol,
     "Peltola wins Alaska; Senate now 56–44",
     "Democrats take 56–44, largest since 2009; ninth flip."),
    ("05", "AFRICA · HEALTH", DARKRED, icon_virus,
     "Ebola outbreak passes 11,000 cases",
     "5,400 dead; children under five hit hardest."),
    ("06", "ASIA · DISASTER", TEAL, icon_cyclone,
     "Cyclone Akvan bears down on India",
     "Landfall due Friday in Andhra Pradesh; Odisha evacuates."),
    ("07", "GLOBAL · MARKETS", NAVY, icon_chart,
     "Stocks fall on Gulf tensions",
     "The S&P 500 slips 1.03% and Euro Stoxx 50 drops 2.15%."),
    ("08", "MIDDLE EAST · GAZA", RED, icon_warning,
     "Board warns Gaza truce may collapse",
     "Accuses Israel and Hamas of failing to keep it."),
    ("09", "OCEANIA · CLIMATE", GOLD, icon_drought,
     "Fiji declares disaster over drought",
     "El Niño drought forces Fiji into a national disaster."),
]
mx0, my0, mw, mh, mgap = MX, 386, 310, 104, 21
for i, (num, tag, color, icon, head, body) in enumerate(MED):
    x = mx0 + (i % 3) * (mw + mgap)
    y = my0 + (i // 3) * (mh + 10)
    icon(x, y + 4, 56, color)
    tx = x + 66
    d.text((tx, y), num + "  " + tag, font=F_TAG_SM, fill=color)
    hl = wrap(head, F_MED_HEAD, mw - 66)
    yy = text_block(tx, y + 22, hl, F_MED_HEAD, INK, 23)
    bl = wrap(body, F_MED_BODY, mw - 66)
    text_block(tx, yy + 2, bl, F_MED_BODY, BODY, 19)

# ---- By the numbers -----------------------------------------------------------
ny = 622
d.line([(MX, ny), (RX, ny)], fill=INK, width=2)
d.text((MX, ny + 10), "BY THE", font=F_TAG, fill=RED)
d.text((MX, ny + 32), "NUMBERS", font=F_TAG, fill=RED)
NUMS = [
    ("56–44", "Democrats' Senate majority"),
    ("$92.47", "Brent crude, down 0.72%"),
    ("315 km/h", "Cyclone Xavier's gusts"),
    ("11,000", "Ebola cases in Congo"),
]
nx = 140
for val, lbl in NUMS:
    d.text((nx, ny + 6), val, font=F_NUM, fill=INK)
    d.text((nx, ny + 44), lbl, font=F_NUM_LBL, fill=GREY)
    nx += 225
d.line([(MX, ny + 66), (RX, ny + 66)], fill=INK, width=2)

# ---- World map (dotted, from a coarse land grid) ------------------------------
# Land spans per row (col 0-55 = lon -180..180, row 0-27 = lat 84..-56).
MAP_SPANS = [
    [],
    [(8, 12), (15, 17), (34, 48)],
    [(3, 6), (7, 14), (15, 17), (27, 28), (31, 52)],
    [(3, 6), (7, 14), (15, 16), (26, 29), (30, 52)],
    [(4, 6), (7, 14), (24, 24), (26, 29), (31, 51)],
    [(7, 13), (25, 25), (27, 28), (31, 50), (49, 50)],
    [(8, 13), (25, 25), (26, 31), (32, 47), (49, 50)],
    [(8, 13), (26, 32), (33, 46), (49, 49)],
    [(8, 13), (26, 31), (34, 45), (49, 49)],
    [(8, 12), (27, 30), (31, 34), (38, 45)],
    [(8, 12), (26, 30), (31, 35), (38, 40), (41, 45)],
    [(7, 9), (26, 31), (32, 35), (38, 40), (42, 45)],
    [(8, 10), (26, 32), (33, 34), (39, 40), (43, 46)],
    [(9, 11), (26, 33), (39, 39), (43, 46)],
    [(10, 11), (26, 33), (44, 46)],
    [(12, 15), (27, 32), (44, 47)],
    [(12, 16), (27, 32), (44, 48)],
    [(12, 16), (28, 32), (45, 48)],
    [(12, 16), (28, 31), (45, 47)],
    [(13, 16), (28, 31), (45, 49)],
    [(13, 15), (29, 31), (45, 50)],
    [(13, 15), (29, 30), (45, 50)],
    [(13, 15), (29, 30), (46, 49)],
    [(14, 15), (29, 30), (46, 49)],
    [(14, 15), (46, 48), (52, 53)],
    [(14, 14), (52, 52)],
    [(14, 14)],
    [],
]
MAP = ["".join("#" if any(s <= c <= e for s, e in spans) else "."
               for c in range(56)) for spans in MAP_SPANS]
assert all(len(row) == 56 for row in MAP), "map rows must be 56 wide"
map_x, map_y, map_w, map_h = MX, 726, 280, 176
d.text((MX, 700), "WHERE IT HAPPENED", font=F_SEC, fill=INK)
d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=SEA)
cw, chh = map_w / 56.0, map_h / 28.0
for r, row in enumerate(MAP):
    for c, ch in enumerate(row):
        if ch == "#":
            px = map_x + (c + 0.5) * cw
            py = map_y + (r + 0.5) * chh
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=LAND)
PINS = [
    (1, 37, 11, RED), (2, 34, 8, NAVY), (3, 46, 12, TEAL),
    (4, 5, 4, GREEN), (5, 33, 16, BROWN), (6, 42, 13, TEAL),
    (7, 16, 8, GREEN), (8, 33, 10, RED), (9, 53, 20, GOLD),
]
for num, c, r, col in PINS:
    px = map_x + (c + 0.5) * cw
    py = map_y + (r + 0.5) * chh
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=col,
              outline=(255, 255, 255), width=1)
    tw = d.textlength(str(num), font=F_BRIEF_N)
    d.text((px - tw / 2, py - 7), str(num), font=F_BRIEF_N,
           fill=(255, 255, 255))
d.text((MX, map_y + map_h + 6),
       "Numbered dots mark stories 1–9.",
       font=F_LEG, fill=GREY)
for li, items in enumerate([[(RED, "Middle East"), (NAVY, "Europe"),
                            (TEAL, "Asia")],
                           [(GREEN, "Americas"), (BROWN, "Africa"),
                            (GOLD, "Oceania")]]):
    ly = map_y + map_h + 26 + li * 18
    lx = MX
    for col, name in items:
        d.ellipse([lx, ly, lx + 10, ly + 10], fill=col)
        d.text((lx + 14, ly - 2), name, font=F_LEG, fill=INK)
        lx += 14 + d.textlength(name, font=F_LEG) + 12

# ---- Also on ... briefs ---------------------------------------------------------
BRIEFS = [
    (10, "Nvidia beats forecasts; AI caution weighs"),
    (11, "Knesset elects Kahana as speaker"),
    (12, "U.S. faults Ukraine strikes; Berlin objects"),
    (13, "Measles: U.S. loses status held since 2000"),
    (14, "Voyager 1 reaches one light-day from Earth"),
    (15, "Russian military plane crashes; 19 dead"),
    (16, "Cyclone Xavier, Category 5, hits Cooks"),
    (17, "World Court to rule on Myanmar case"),
    (18, "Iran downs U.S. MQ-9 drone near Hormuz"),
    (19, "6.0 quake strikes Papua New Guinea"),
    (20, "5.3 quake strikes Romania"),
    (21, "Trump meets Marcos, then flies to China"),
    (22, "Tech outages hit U.S. banks, flights, NSA"),
    (23, "Myanmar to review its ASEAN relationship"),
    (24, "UK-held U.S. soldier moved to U.S. custody"),
    (25, "Five EU states plan migrant hubs in Rwanda"),
    (26, "27 years for Iran-linked plot against Trump"),
    (27, "Isolated Awa group emerges in Amazon"),
    (28, "Turkey takes over Sozcu TV"),
    (29, "Serbia parliament opens with student list"),
    (30, "Eritrea border clashes raise war fears"),
    (31, "South Korea raises 2027 growth outlook"),
    (32, "France, Malaysia in rare-earths partnership"),
    (33, "U.S. tightens chip access rules for China"),
    (34, "Anthropic set to list on Nasdaq on Nov. 19"),
    (35, "Fela Kuti first African in Rock Hall of Fame"),
]
bx, by = 336, 700
d.text((bx, by), "ALSO ON WEDNESDAY 18 NOVEMBER — 26 MORE STORIES",
       font=F_SEC, fill=INK)
d.line([(bx, by + 24), (RX, by + 24)], fill=RED, width=2)
col_w = 326
for i, (num, text) in enumerate(BRIEFS):
    cx = bx + (i // 13) * col_w
    cy = by + 34 + (i % 13) * 20
    d.text((cx, cy), str(num), font=F_BRIEF_N, fill=RED)
    nw = d.textlength(str(num) + "  ", font=F_BRIEF_N)
    t = fit(text, F_BRIEF, col_w - nw - 4)
    d.text((cx + nw, cy), t, font=F_BRIEF, fill=INK)

# ---- Footer ---------------------------------------------------------------------
d.line([(MX, 996), (RX, 996)], fill=INK, width=1)
d.text((MX, 1004),
       "Every story was reported on Wednesday 18 November 2026. "
       "Sources: Reuters, AP, AFP, BBC, Al Jazeera, UN.",
       font=F_SRC, fill=GREY)

img.save("entry.png")
print("saved entry.png", img.size)
