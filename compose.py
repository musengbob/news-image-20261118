#!/usr/bin/env python3
"""Compose the round-2 front page for make.fun news-image-20261118.

Dense broadsheet: masthead + date, hero illustration of the Gulf strikes,
one-line lead, a world map with numbered story markers, and 33 more verified
18 November 2026 stories across six continents in three columns.
Output: entry.png, exactly 1024x1024, <= 1 MiB.
"""
import json
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 28
CW = W - 2 * MARGIN  # 968 content width
PAPER = (248, 243, 230)
INK = (20, 20, 20)
RED = (163, 22, 33)
SEA = (214, 224, 228)
LAND = (221, 210, 184)
LAND_EDGE = (178, 164, 128)
GREY = (90, 90, 90)

FDIR = "/usr/share/fonts/truetype/noto/"
def font(name, size):
    return ImageFont.truetype(FDIR + name, size)

F_MAST = font("NotoSerifDisplay-Black.ttf", 76)
F_DATE = font("NotoSans-Bold.ttf", 23)
F_STRAP = font("NotoSans-Bold.ttf", 12)
F_LEAD = font("NotoSerifDisplay-Black.ttf", 47)
F_DECK = font("NotoSerif-Regular.ttf", 17)
F_CAP = font("NotoSerif-Italic.ttf", 13)
F_MAPHEAD = font("NotoSans-Bold.ttf", 12)
F_LEGEND = font("NotoSans-Regular.ttf", 11)
F_COLHEAD = font("NotoSans-Bold.ttf", 12)
F_KICK = font("NotoSans-Bold.ttf", 10)
F_HEAD = font("NotoSerif-Bold.ttf", 12)
F_HEAD_SM = font("NotoSerif-Bold.ttf", 11)
F_FOOT = font("NotoSans-Regular.ttf", 10)
F_NUM = font("NotoSans-Bold.ttf", 9)

# ---------------------------------------------------------------- stories
# (kicker, headline) — every headline verified against 18 Nov 2026 briefings.
COLUMNS = [
    ("ASIA", [
        ("SHENZHEN", "Xi hosts Putin at APEC; Trump joins summit on Thursday"),
        ("MANILA", "Trump meets Quad partners; Thailand trade pact signed"),
        ("BAY OF BENGAL", "Cyclone Akvan strengthens; Andhra braces for Friday landfall"),
        ("TOKYO", "India and Japan open 2+2 defence and foreign talks"),
        ("DHAKA", "India beat Pakistan 2-1 to win a 10th SAFF title"),
        ("RAWALPINDI", "Pakistan bowl Sri Lanka out for 98 in second Test"),
        ("CHENNAI", "Dhoni calls time on IPL playing career"),
        ("SEOUL", "South Korea lifts 2027 growth forecast to 3.9%"),
        ("KUALA LUMPUR", "France-Malaysia rare-earths pact signed on Macron visit"),
        ("ADEN", "Houthis press toward Aden as Yemen fighting spreads"),
        ("NEW DELHI", "Wholesale inflation hits a four-year high of 12.29%"),
    ]),
    ("EUROPE", [
        ("KERCH", "Bridge span collapses after second day of strikes"),
        ("THE HAGUE", "World Court to rule on Myanmar genocide case"),
        ("PARIS", "140,000 join pay protests across France"),
        ("BERLIN", "US scolds Kyiv on deep strikes; Germany pushes back"),
        ("ISTANBUL", "Turkey takes over opposition channel Sozcu TV"),
        ("BELGRADE", "Serbia parliament opens with student-list majority"),
        ("LONDON", "England end Spain's 43-match unbeaten run, 3-2"),
    ]),
    ("AFRICA", [
        ("BUNIA", "Ebola in DR Congo doubles: 11,000 cases, 5,400 dead"),
        ("KIGALI", "Five EU states plan migrant return hubs in Rwanda"),
        ("TIGRAY", "Clashes near Eritrea border raise wider-war fears"),
        ("LAGOS", "Fela Kuti first African in Rock and Roll Hall of Fame"),
    ]),
    ("AMERICAS", [
        ("ALASKA", "Peltola wins Senate seat; Democrats reach 56"),
        ("WASHINGTON", "US loses measles-free status after 26 years"),
        ("USA", "NSA network down in latest of eight US outages"),
        ("SILICON VALLEY", "Nvidia revenue doubles to $115.8bn on AI demand"),
        ("SAN FRANCISCO", "Anthropic to list on Nasdaq on Thursday"),
        ("NEW YORK", "Merchant gets 27 1/2 years over plot on Trump"),
        ("BRASILIA", "Real falls as Lula fiscal plan disappoints"),
        ("AMAZON", "Isolated Awa group emerges in Brazilian rainforest"),
    ]),
    ("OCEANIA", [
        ("COOK ISLANDS", "Category 5 Cyclone Xavier hits with 315 km/h gusts"),
        ("SUVA", "Fiji declares national disaster over El Nino drought"),
        ("PORT MORESBY", "6.0 quake strikes Papua New Guinea"),
    ]),
]
# Column layout: (sections, x) — three columns, col2/col3 split into two regions.
LAYOUT = [
    ([COLUMNS[0]], MARGIN),
    ([COLUMNS[1], COLUMNS[2]], MARGIN + 332),
    ([COLUMNS[3], COLUMNS[4]], MARGIN + 664),
]
COL_W = 304

# Map markers: (number, lon, lat) — positions nudged slightly so neighbours
# (Paris/The Hague, Shenzhen/Manila) do not collide on the small map.
MARKERS = [
    (1, 56.5, 26.5), (2, 114.0, 23.5), (3, 121.5, 13.5), (4, 80.0, 15.0),
    (5, 139.5, 36.0), (6, 90.0, 24.5), (7, 73.0, 34.0), (8, 36.5, 45.5),
    (9, 6.0, 54.0), (10, 1.0, 47.0), (11, 30.0, 1.5), (12, -150.0, 62.0),
]
LEGEND = [
    "1 Gulf strikes  ·  2 Shenzhen summit  ·  3 Manila Quad  ·  4 Cyclone Akvan  ·  5 Tokyo talks  ·  6 Dhaka final",
    "7 Rawalpindi Test  ·  8 Kerch Bridge  ·  9 The Hague  ·  10 Paris protests  ·  11 Ebola in DRC  ·  12 Alaska vote",
]

LEAD = "U.S. STRIKES IRAN AS GULF WAR WIDENS"
DECK = ("US jets hit a Revolutionary Guard missile site on Qeshm Island; "
        "Iran fired drones at American bases in Bahrain and Kuwait.")
CAPTION = ("Illustration: US jets over the Strait of Hormuz after the strike on Qeshm Island. "
           "Iran answered with drones aimed at US bases in Bahrain and Kuwait.")

# ---------------------------------------------------------------- helpers
def center(draw, cx, y, text, fnt, fill=INK):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return w

def wrap_segments(draw, kicker, headline, max_w, head_font):
    """Wrap one story item: red kicker leads line 1, serif headline follows.
    Returns list of lines; each line is a list of (text, font, fill)."""
    kick = kicker + " \u2014 "
    words = headline.split(" ")
    lines = []
    cur = [(kick, F_KICK, RED)]
    cur_w = draw.textlength(kick, font=F_KICK)
    for word in words:
        piece = word + " "
        pw = draw.textlength(piece, font=head_font)
        if cur_w + pw > max_w and cur:
            lines.append(cur)
            cur = [(piece, head_font, INK)]
            cur_w = pw
        else:
            cur.append((piece, head_font, INK))
            cur_w += pw
    if cur:
        lines.append(cur)
    return lines

def draw_map(box):
    """Render the world map layer: equirectangular, land from GeoJSON."""
    x0, y0, mw, mh = box
    layer = Image.new("RGB", (mw, mh), SEA)
    d = ImageDraw.Draw(layer)
    lat_top, lat_bot = 84.0, -58.0
    def proj(lon, lat):
        px = (lon + 180.0) / 360.0 * mw
        py = (lat_top - lat) / (lat_top - lat_bot) * mh
        return px, py
    with open("/tmp/world.geo.json") as fh:
        geo = json.load(fh)
    for feat in geo["features"]:
        geom = feat["geometry"]
        if geom is None:
            continue
        polys = []
        if geom["type"] == "Polygon":
            polys = [geom["coordinates"][0]]
        elif geom["type"] == "MultiPolygon":
            polys = [p[0] for p in geom["coordinates"]]
        for ring in polys:
            # Unwrap longitudes so antimeridian-crossing rings stay whole,
            # then draw shifted copies so both edges of the map show them.
            pts, prev = [], None
            for lon, lat in ring:
                if prev is not None:
                    while lon - prev > 180:
                        lon -= 360
                    while lon - prev < -180:
                        lon += 360
                pts.append((lon, lat))
                prev = lon
            for shift in (0, -360, 360):
                xy = [proj(lon + shift, lat) for lon, lat in pts]
                d.polygon(xy, fill=LAND, outline=LAND_EDGE)
    # Graticule
    for lon in range(-150, 181, 30):
        px = (lon + 180.0) / 360.0 * mw
        d.line([(px, 0), (px, mh)], fill=(198, 210, 214), width=1)
    for lat in range(-60, 91, 30):
        py = (lat_top - lat) / (lat_top - lat_bot) * mh
        d.line([(0, py), (mw, py)], fill=(198, 210, 214), width=1)
    # Markers
    for num, lon, lat in MARKERS:
        px, py = proj(lon, lat)
        r = 7
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED, outline=(255, 255, 255), width=1)
        t = str(num)
        tw = d.textlength(t, font=F_NUM)
        th = F_NUM.size
        d.text((px - tw / 2, py - th / 2 - 1), t, font=F_NUM, fill=(255, 255, 255))
    return layer

# ---------------------------------------------------------------- compose
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    cx = W / 2

    # Top rule + strap line
    d.rectangle([MARGIN, 6, W - MARGIN, 9], fill=INK)
    d.text((MARGIN, 13), "WORLD EDITION", font=F_STRAP, fill=INK)
    right = "34 STORIES  \u00b7  6 CONTINENTS  \u00b7  ONE DAY"
    d.text((W - MARGIN - d.textlength(right, font=F_STRAP), 13), right, font=F_STRAP, fill=INK)

    # Masthead + date
    center(d, cx, 30, "THE WORLD TODAY", F_MAST)
    center(d, cx, 108, "WEDNESDAY  \u00b7  18 NOVEMBER 2026", F_DATE)
    d.rectangle([MARGIN, 138, W - MARGIN, 140], fill=INK)
    d.rectangle([MARGIN, 143, W - MARGIN, 143], fill=INK)

    # Hero: centre-crop the generated Gulf illustration to 968x195
    hero = Image.open("hero.webp").convert("RGB")
    hw, hh = hero.size
    target = CW / 195.0
    ch = int(hw / target)
    crop_y = 180
    hero = hero.crop((0, crop_y, hw, crop_y + ch)).resize((CW, 195), Image.LANCZOS)
    img.paste(hero, (MARGIN, 148))
    d.rectangle([MARGIN, 148, W - MARGIN - 1, 342], outline=INK, width=2)

    # Caption, lead, deck
    center(d, cx, 347, CAPTION, F_CAP)
    lead_font = F_LEAD
    while d.textlength(LEAD, font=lead_font) > CW and lead_font.size > 30:
        lead_font = font("NotoSerifDisplay-Black.ttf", lead_font.size - 1)
    center(d, cx, 366, LEAD, lead_font)
    center(d, cx, 420, DECK, F_DECK)
    d.rectangle([MARGIN, 446, W - MARGIN, 446], fill=INK)

    # Map panel
    center(d, cx, 452, "THE WORLD TODAY \u2014 WHERE THE NEWS HAPPENED", F_MAPHEAD)
    map_layer = draw_map((MARGIN, 470, CW, 120))
    img.paste(map_layer, (MARGIN, 470))
    d.rectangle([MARGIN, 470, W - MARGIN - 1, 589], outline=GREY, width=1)
    center(d, cx, 594, LEGEND[0], F_LEGEND, fill=GREY)
    center(d, cx, 608, LEGEND[1], F_LEGEND, fill=GREY)
    d.rectangle([MARGIN, 626, W - MARGIN, 626], fill=INK)

    # Story columns
    y_top = 634
    item_h = 27
    for sections, x in LAYOUT:
        y = y_top
        for name, stories in sections:
            d.rectangle([x, y, x + COL_W, y + 2], fill=RED)
            d.text((x, y + 5), name, font=F_COLHEAD, fill=INK)
            y += 22
            for kicker, headline in stories:
                lines = wrap_segments(d, kicker, headline, COL_W, F_HEAD)
                if len(lines) > 2:
                    lines = wrap_segments(d, kicker, headline, COL_W, F_HEAD_SM)
                ly = y
                for line in lines[:2]:
                    lx = x
                    for text, fnt, fill in line:
                        d.text((lx, ly), text, font=fnt, fill=fill)
                        lx += d.textlength(text, font=fnt)
                    ly += 13
                y += item_h
            y += 2
    # Footer
    d.rectangle([MARGIN, 990, W - MARGIN, 990], fill=INK)
    center(d, cx, 995,
           "MARKETS  \u2014  S&P 500 7,341 -1.03%  \u00b7  FTSE 100 10,690 -1.76%  \u00b7  "
           "Brent $92.47 -0.72%  \u00b7  Gold -2.05%  \u00b7  VIX 25.46", F_FOOT, fill=GREY)
    center(d, cx, 1008,
           "Sources: Reuters, AP, AFP, BBC, Al Jazeera, UN, IMD, NOAA  \u00b7  "
           "Every story reported on 18 November 2026", F_FOOT, fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)

if __name__ == "__main__":
    main()
