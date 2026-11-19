#!/usr/bin/env python3
"""Compose THE WORLD TODAY front page for 18 November 2026.

Round 3 of news-image-20261118. Dense broadsheet: masthead, hero lead on
the Qeshm strike, six illustrated stories, 30 briefs in three columns, a
world map with numbered markers, a day-in-figures strip, a markets strip
and a footer ticker. 51 verified stories in total.

Output: entry.png, 1024x1024, at most 1 MiB. Deterministic: no random
inputs, fixed fonts, fixed crop/resize, so re-runs are byte-identical.
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (18, 18, 18)
RED = (163, 22, 33)
NAVY = (27, 58, 92)
GREY = (96, 92, 84)
RULE = (30, 30, 30)
SEA = (196, 219, 232)
LAND = (231, 220, 192)
LAND_EDGE = (148, 138, 108)
PANEL = (238, 231, 216)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, width):
    """Greedy word wrap to a pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(d, text, fnt, width):
    """Truncate to one line with an ellipsis if needed."""
    if d.textlength(text, font=fnt) <= width:
        return text
    while text and d.textlength(text + "\u2026", font=fnt) > width:
        text = text[:-1]
    return text + "\u2026"


def photo(name, box):
    """Center-crop an asset photo to fill box, LANCZOS resize."""
    im = Image.open(os.path.join(ASSETS, name)).convert("RGB")
    bw, bh = box[2] - box[0], box[3] - box[1]
    sw, sh = im.size
    target = bw / bh
    if sw / sh > target:
        nw = int(sh * target)
        x0 = (sw - nw) // 2
        im = im.crop((x0, 0, x0 + nw, sh))
    else:
        nh = int(sw / target)
        y0 = (sh - nh) // 2
        im = im.crop((0, y0, sw, y0 + nh))
    return im.resize((bw, bh), Image.LANCZOS)


# ---------------------------------------------------------------- stories

LEAD_DECK = (
    "US fighter jets hit a Revolutionary Guard missile site on Qeshm Island "
    "in answer to Iranian attacks on US personnel. Iran answered with drones "
    "over Kuwait and Bahrain as the Gulf went on alert."
)

LEAD_BULLETS = [
    ("KUWAIT \u2014 ", "Iran says it fired on US drone and missile sites in "
     "Kuwait overnight; Kuwait's air defences countered hostile drones."),
    ("BAHRAIN \u2014 ", "Bahrain says it intercepted Iranian attacks three "
     "times in a week; no casualties reported."),
    ("GULF \u2014 ", "USS Theodore Roosevelt joins two carrier groups; more "
     "than a dozen destroyers now in the region."),
    ("ISRAEL \u2014 ", "Mossad chief Roman Gofman lobbied Washington last "
     "week for new joint strikes on Iran."),
]

THUMBS = [
    ("xi-trump-hug.jpg", "XI HUGS TRUMP IN SHENZHEN",
     "Rare welcome before Thursday's talks."),
    ("kerch-bridge.jpg", "KERCH BRIDGE ARCH FALLS",
     "Road span falls after two strikes."),
    ("voyager.jpg", "VOYAGER 1: A LIGHT-DAY OUT",
     "25.9bn km out; signals take a day."),
    ("cyclone-akvan.jpg", "CYCLONE AKVAN STRENGTHENS",
     "Severe storm nears Andhra Pradesh."),
    ("dhoni-farewell.jpg", "DHONI CALLS TIME ON IPL",
     "18 seasons done; mentor from 2027."),
    ("apec-shenzhen.jpg", "APEC OPENS IN SHENZHEN",
     "21 economies talk trade and AI."),
]

COLUMNS = [
    ("ASIA & PACIFIC", [
        ("XI, PUTIN MEET BEFORE TRUMP LANDS",
         "Xi urges free trade; Putin says sanctions backfired."),
        ("TRUMP SHAKES PUTIN'S HAND AT BANQUET",
         "First in-person meeting since the Alaska summit."),
        ("QUAD MEETS IN MANILA AT TOP LEVEL",
         "First leaders' meeting in more than two years."),
        ("TRUMP UNVEILS PHILIPPINES DEAL",
         "Unveiled during the Manila stop of his Asia tour."),
        ("BAIDU CHIEF WARNS OF AN AI BUBBLE",
         "Li: adoption must lift profits or fears come true."),
        ("TAIWAN LOGS 10 PLA SORTIES, 11 SHIPS",
         "Latest published window around the island."),
        ("MYANMAR ARSENIC HITS THE MEKONG",
         "Thailand races to supply safe drinking water."),
        ("ROHINGYA AWAIT ICJ GENOCIDE VERDICT",
         "Nearly a million exiles watch the court."),
        ("AUSTRALIA JOBLESS UP TO 4.9%",
         "Canberra sanctions settlers over West Bank violence."),
        ("NZ HOSTS INDIA IN WELLINGTON TEST",
         "World Test Championship match under way."),
    ]),
    ("EUROPE & MIDDLE EAST", [
        ("EU PROPOSES \u20ac45BN LOAN FOR UKRAINE",
         "\u20ac25bn arms, \u20ac20bn budget; repaid after reparations."),
        ("DRONES OVER DNIPRO INJURE SIX",
         "141 drones; 126 downed or suppressed."),
        ("RUSSIA TO DOUBLE DRONE OUTPUT",
         "EU's Kubilius: Moscow plans 20 million in 2027."),
        ("ECB WARNS BOND MARKETS LOOK FRAGILE",
         "Stability Review flags sovereign debt strain."),
        ("NATO UNVEILS COMMS STRATEGY",
         "Alliance-wide plan for future networks announced."),
        ("UK SANCTIONS 8 SETTLEMENT FIRMS",
         "Tzav 9 also listed for blocking aid to Gaza."),
        ("UK INFLATION RISES TO 3.6%",
         "Fuel pushes prices up in the year to October."),
        ("KAHANA ELECTED KNESSET SPEAKER 66\u201352",
         "Eisenkot ally takes the gavel from Netanyahu's bloc."),
        ("BOARD OF PEACE FAULTS BOTH SIDES",
         "Trump panel blames Israel and Hamas over ceasefire."),
        ("950,000 GAZANS ON FLOOD GROUND",
         "WHO warns as a fourth winter of displacement bites."),
    ]),
    ("AMERICAS & WORLD", [
        ("PELTOLA WINS ALASKA; DEMOCRATS 56\u201344",
         "Ninth Senate flip; largest majority since 2009."),
        ("US LOSES MEASLES-FREE STATUS",
         "5,412 cases in 2026, most since 1991; 10 dead."),
        ("VANCE: NO FOREVER WAR IN THE GULF",
         "VP pledges US role will not become a two-year war."),
        ("NVIDIA POSTS $115.8BN QUARTER",
         "Revenue doubles; board rules out Huang's return."),
        ("HUANG TO FACE SENATE BANKING PANEL",
         "Ex-CEO agrees to testify on AI competition."),
        ("OPENAI SHIPS GPT-6.2 ASTRA AND SOL",
         "Astra API prices cut 20%; Sol for everyday work."),
        ("HOUSE DEMOCRATS PLAN SHAKE-UP",
         "Leadership transition readied for the new Congress."),
        ("CARNEY MEETS TRUMP AT APEC",
         "Canadian PM holds talks on Shenzhen sidelines."),
        ("HAITI HAILS EL SALVADOR GANG MODEL",
         "Port-au-Prince praises Bukele-style crackdown."),
        ("CALIFORNIA SUES OPENAI",
         "State takes the AI lab to court."),
    ]),
]

FIGURES = [
    ("\u20ac45BN", "EU LOAN FOR UKRAINE"),
    ("$115.8BN", "NVIDIA Q3 REVENUE"),
    ("25.9BN KM", "VOYAGER 1 FROM EARTH"),
    ("11,000+", "EBOLA CASES, DR CONGO"),
    ("5,412", "US MEASLES CASES"),
    ("56\u201344", "SENATE MAJORITY"),
]

MARKETS = ("MARKETS \u2014 GOLD $3,770/OZ \u22122.1%  \u00b7  NASDAQ-100 FUT "
           "+1.17%  \u00b7  NVIDIA GUIDES $130BN Q4  \u00b7  UK CPI 3.6%  "
           "\u00b7  AUS JOBLESS 4.9%  \u00b7  SA CPI 5.2%")

TICKER = ("ALSO TODAY: GTA VI OUT TOMORROW \u00b7 EBOLA PASSES 11,000 IN "
          "DR CONGO \u00b7 ETHIOPIA\u2013ERITREA CLASHES NEAR BADME \u00b7 "
          "ANC FACES HISTORIC DECLINE \u00b7 CHELSEA BEAT PSG 1\u20130 \u00b7 "
          "DUCKETT TON SEALS ODI SERIES \u00b7 ETHIOPIAN AIRLINES "
          "CYBERATTACK \u00b7 NIGERIA LAUNCHES EDTECH PLAN \u00b7 SIERRA "
          "LEONE'S $45M 2ND CABLE \u00b7 COP31: $120BN CLIMATE TARGET")

# ------------------------------------------------------------------- map
# Coarse continent outlines as (lon, lat) pairs, equirectangular.

CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69), (-85, 66),
     (-80, 73), (-65, 60), (-55, 52), (-60, 45), (-70, 42), (-75, 35),
     (-80, 32), (-81, 25), (-90, 21), (-97, 16), (-94, 16), (-86, 13),
     (-83, 9), (-79, 9), (-85, 15), (-90, 14), (-97, 22), (-105, 23),
     (-110, 30), (-114, 32), (-120, 34), (-125, 40), (-124, 48),
     (-130, 55), (-145, 60), (-158, 58)],
    # Greenland
    [(-45, 60), (-30, 68), (-22, 70), (-25, 76), (-45, 80), (-60, 76),
     (-55, 70)],
    # South America
    [(-79, 9), (-75, 11), (-71, 12), (-64, 10), (-52, 5), (-50, 0),
     (-44, -3), (-35, -8), (-38, -15), (-40, -22), (-48, -28), (-52, -33),
     (-58, -38), (-62, -41), (-65, -45), (-68, -50), (-69, -55),
     (-71, -54), (-73, -45), (-73, -37), (-71, -30), (-70, -20),
     (-75, -15), (-77, -8), (-81, -4), (-80, 1), (-77, 4)],
    # Africa
    [(-17, 15), (-17, 21), (-10, 31), (-5, 35), (10, 37), (11, 34),
     (20, 32), (30, 31), (32, 31), (35, 28), (37, 18), (43, 12), (51, 11),
     (48, 2), (41, -2), (40, -10), (35, -18), (33, -26), (28, -33),
     (20, -35), (17, -29), (14, -22), (12, -18), (13, -12), (9, -1),
     (9, 4), (-8, 4), (-13, 8)],
    # Eurasia
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (3, 53), (8, 55), (8, 57),
     (11, 58), (18, 56), (21, 55), (24, 58), (28, 60), (30, 60), (32, 66),
     (40, 68), (50, 69), (60, 69), (70, 72), (80, 73), (90, 75), (100, 76),
     (110, 74), (120, 73), (130, 71), (140, 72), (150, 70), (160, 69),
     (170, 67), (178, 65), (178, 62), (170, 60), (162, 56), (158, 52),
     (150, 45), (142, 42), (140, 38), (135, 34), (129, 33), (127, 35),
     (122, 38), (120, 32), (118, 25), (110, 20), (108, 18), (105, 10),
     (103, 8), (100, 7), (98, 10), (94, 17), (92, 21), (88, 22), (86, 20),
     (80, 15), (77, 8), (75, 12), (72, 20), (68, 23), (66, 25), (61, 25),
     (57, 26), (52, 28), (50, 29), (48, 30), (44, 29), (39, 21), (35, 28),
     (36, 36), (30, 36), (27, 37), (23, 36), (19, 40), (16, 42), (12, 44),
     (8, 44), (3, 43), (-2, 37), (-6, 36), (-9, 37)],
    # Britain
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (1, 53), (1, 51),
     (-3, 50)],
    # Japan
    [(130, 31), (133, 34), (137, 35), (140, 36), (141, 40), (142, 44),
     (145, 44), (143, 42), (140, 38), (137, 35), (133, 33)],
    # Indonesia
    [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8), (120, -9),
     (125, -9), (130, -4), (131, 0), (128, 2), (122, 0), (115, 1),
     (110, 2), (105, 1), (100, 4)],
    # Australia
    [(114, -22), (114, -28), (115, -33), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (147, -38),
     (150, -37), (153, -30), (153, -27), (151, -24), (146, -19), (142, -15),
     (142, -11), (137, -12), (135, -15), (132, -12), (130, -13), (126, -14),
     (122, -17), (118, -20)],
    # New Zealand
    [(167, -45), (171, -43), (174, -41), (177, -38), (178, -38), (175, -40),
     (172, -42), (168, -46)],
    # Madagascar
    [(44, -16), (47, -15), (50, -16), (49, -20), (47, -25), (45, -25),
     (44, -20)],
]

# (lon, lat, label, dx, dy) - dx/dy nudge the marker so close pairs separate
MARKERS = [
    (114.1, 22.5, "Shenzhen", 0, -7),
    (121.0, 14.6, "Manila", 0, 7),
    (56.3, 26.9, "Qeshm I.", -8, -6),
    (47.5, 29.4, "Kuwait", -7, 7),
    (50.6, 26.2, "Bahrain", 8, 6),
    (36.5, 45.4, "Kerch", 0, -6),
    (4.35, 50.85, "Brussels", 7, 6),
    (-0.1, 51.5, "London", -7, -6),
    (-149.9, 61.2, "Alaska", 0, -6),
    (-77.0, 38.9, "Washington", 0, 7),
    (85.5, 13.0, "Bay of Bengal", 0, 7),
    (15.3, -4.3, "DR Congo", 0, 7),
]


def project(lon, lat, mx, my, mw, mh):
    x = mx + (lon + 180.0) / 360.0 * mw
    y = my + (90.0 - lat) / 180.0 * mh
    return x, y


def draw_map(d, mx, my, mw, mh):
    d.rectangle([mx, my, mx + mw, my + mh], fill=SEA, outline=RULE, width=1)
    for poly in CONTINENTS:
        pts = [project(lon, lat, mx, my, mw, mh) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    num_font = F(SANS_B, 8)
    for i, (lon, lat, _label, dx, dy) in enumerate(MARKERS, 1):
        x, y = project(lon, lat, mx, my, mw, mh)
        cx, cy = x + dx, y + dy
        if dx or dy:
            d.line([x, y, cx, cy], fill=RED, width=1)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED,
                  outline=(255, 255, 255), width=1)
        label = str(i)
        tw = d.textlength(label, font=num_font)
        d.text((cx - tw / 2, cy - 5), label, font=num_font,
               fill=(255, 255, 255))


# ----------------------------------------------------------------- build

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    f_mast = F(SERIF_B, 54)
    f_date = F(SANS_B, 13)
    f_date2 = F(SANS, 11)
    f_kick = F(SANS_B, 13)
    f_head = F(SERIF_B, 33)
    f_deck = F(SERIF_R, 15)
    f_bull = F(SANS, 11)
    f_bull_b = F(SANS_B, 11)
    f_cap = F(SERIF_I, 11)
    f_thumb_t = F(SANS_B, 9)
    f_thumb_d = F(SANS, 8)
    f_sect = F(SANS_B, 13)
    f_col = F(SANS_B, 11)
    f_item = F(SANS_B, 10)
    f_deck2 = F(SANS, 9)
    f_leg = F(SANS, 8)
    f_fig_n = F(SANS_B, 16)
    f_fig_l = F(SANS_B, 8)
    f_mkt = F(SANS_B, 10)
    f_tick = F(SANS, 9)
    f_foot = F(SANS, 8)

    # ---- masthead
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, 6), title, font=f_mast, fill=INK)
    d.line([8, 64, W - 8, 64], fill=RULE, width=1)
    d.text((8, 70), "WEDNESDAY \u00b7 18 NOVEMBER 2026", font=f_date, fill=INK)
    mid = "51 STORIES \u00b7 6 CONTINENTS \u00b7 ONE DAY"
    d.text(((W - d.textlength(mid, font=f_date)) / 2, 70), mid,
           font=f_date, fill=RED)
    right = "SOURCES: REUTERS \u00b7 AP \u00b7 AFP \u00b7 NASA \u00b7 IMD"
    d.text((W - 8 - d.textlength(right, font=f_date2), 71), right,
           font=f_date2, fill=GREY)
    d.line([8, 90, W - 8, 90], fill=RULE, width=2)
    d.line([8, 94, W - 8, 94], fill=RULE, width=1)

    # ---- hero + lead
    hero_box = (8, 102, 512, 352)
    img.paste(photo("hero-qeshm.jpg", hero_box), hero_box[:2])
    d.rectangle(hero_box, outline=RULE, width=1)
    d.text((8, 356), "Illustration: US jets over the Strait of Hormuz after "
           "the strike on Qeshm Island.", font=f_cap, fill=GREY)
    d.text((8, 372), "Generated image \u2014 all photographs on this page "
           "are illustrations.", font=f_cap, fill=GREY)

    lx = 524
    d.text((lx, 102), "GULF WAR \u2014 LEAD STORY", font=f_kick, fill=RED)
    head = "U.S. STRIKES IRAN AS GULF WAR WIDENS"
    y = 122
    for line in wrap(d, head, f_head, 492):
        d.text((lx, y), line, font=f_head, fill=INK)
        y += 38
    y += 4
    for line in wrap(d, LEAD_DECK, f_deck, 492):
        d.text((lx, y), line, font=f_deck, fill=INK)
        y += 19
    y += 6
    d.line([lx, y, W - 8, y], fill=GREY, width=1)
    y += 8
    for lead_in, body in LEAD_BULLETS:
        d.text((lx, y), "\u25aa  ", font=f_bull, fill=RED)
        bx = lx + 12
        d.text((bx, y), lead_in, font=f_bull_b, fill=INK)
        off = d.textlength(lead_in, font=f_bull_b)
        lines = wrap(d, body, f_bull, 492 - 12 - off)
        d.text((bx + off, y), lines[0], font=f_bull, fill=INK)
        yy = y + 14
        for extra in lines[1:]:
            d.text((bx, yy), extra, font=f_bull, fill=INK)
            yy += 14
        y = yy + 3

    # ---- six illustrated stories
    ty, th = 400, 104
    tw_, gap = 164, 4
    for i, (name, title, deck) in enumerate(THUMBS):
        x = 8 + i * (tw_ + gap)
        box = (x, ty, x + tw_, ty + th)
        img.paste(photo(name, box), box[:2])
        d.rectangle(box, outline=RULE, width=1)
        d.text((x, ty + th + 3), fit(d, title, f_thumb_t, tw_),
               font=f_thumb_t, fill=INK)
        d.text((x, ty + th + 15), fit(d, deck, f_thumb_d, tw_),
               font=f_thumb_d, fill=GREY)

    # ---- section header
    d.line([8, 552, W - 8, 552], fill=RULE, width=2)
    d.text((8, 558), "THE DAY IN BRIEF", font=f_sect, fill=INK)
    note = "ASIA \u00b7 EUROPE \u00b7 MIDDLE EAST \u00b7 AMERICAS \u00b7 AFRICA \u00b7 OCEANIA"
    d.text((W - 8 - d.textlength(note, font=f_date2), 559), note,
           font=f_date2, fill=GREY)
    d.line([8, 578, W - 8, 578], fill=RULE, width=1)

    # ---- three brief columns + map column
    col_w = 248
    col_xs = [8, 264, 520, 776]
    cy = 586
    for ci, (header, items) in enumerate(COLUMNS):
        x = col_xs[ci]
        d.rectangle([x, cy, x + col_w, cy + 18], fill=NAVY)
        d.text((x + 5, cy + 3), header, font=f_col, fill=(255, 255, 255))
        iy = cy + 24
        for headline, deck in items:
            d.text((x, iy), fit(d, headline, f_item, col_w),
                   font=f_item, fill=INK)
            d.text((x, iy + 12), fit(d, deck, f_deck2, col_w),
                   font=f_deck2, fill=GREY)
            iy += 25

    # map column
    mx = col_xs[3]
    d.rectangle([mx, cy, mx + col_w, cy + 18], fill=RED)
    d.text((mx + 5, cy + 3), "WHERE IT HAPPENED", font=f_col,
           fill=(255, 255, 255))
    draw_map(d, mx, cy + 24, col_w, 124)
    ly = cy + 24 + 124 + 6
    for row in range(6):
        left = MARKERS[row]
        right_m = MARKERS[row + 6]
        d.text((mx, ly), f"{row + 1} {left[2]}", font=f_leg, fill=INK)
        d.text((mx + 124, ly), f"{row + 7} {right_m[2]}", font=f_leg,
               fill=INK)
        ly += 12
    d.text((mx, ly + 2), "Numbers mark the day's datelines.",
           font=f_leg, fill=GREY)

    # ---- day in figures
    fy = 864
    d.rectangle([8, fy, W - 8, fy + 46], fill=NAVY)
    d.text((16, fy + 16), "THE DAY\nIN FIGURES", font=f_fig_l,
           fill=(255, 255, 255))
    cell_w = (W - 16 - 110) // 6
    for i, (num, label) in enumerate(FIGURES):
        cx = 8 + 110 + i * cell_w
        d.text((cx + 8, fy + 6), num, font=f_fig_n, fill=(255, 255, 255))
        d.text((cx + 8, fy + 27), fit(d, label, f_fig_l, cell_w - 12),
               font=f_fig_l, fill=(200, 215, 230))

    # ---- markets strip
    d.text((8, 920), fit(d, MARKETS, f_mkt, W - 16), font=f_mkt, fill=INK)
    d.line([8, 940, W - 8, 940], fill=RULE, width=1)

    # ---- footer ticker
    d.rectangle([8, 948, W - 8, 986], fill=INK)
    lines = wrap(d, TICKER, f_tick, W - 32)
    ty2 = 952
    for line in lines[:2]:
        d.text((16, ty2), line, font=f_tick, fill=(255, 255, 255))
        ty2 += 13
    foot = ("THE WORLD TODAY \u00b7 WEDNESDAY 18 NOVEMBER 2026 \u00b7 All "
            "stories verified against same-day reporting \u00b7 "
            "Illustrations generated in-session")
    d.text(((W - d.textlength(foot, font=f_foot)) / 2, 994), foot,
           font=f_foot, fill=GREY)
    return img


def main():
    img = build()
    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    size = os.path.getsize(out)
    print(f"PNG bytes: {size}")
    if size > 1048576:
        img.save(out, "JPEG", quality=90)
        size = os.path.getsize(out)
        print(f"JPEG fallback bytes: {size}")
    print(f"wrote {out} ({img.size[0]}x{img.size[1]}, {size} bytes)")


if __name__ == "__main__":
    main()
