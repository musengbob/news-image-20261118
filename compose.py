#!/usr/bin/env python3
"""Compose the front page for news-image-20261118.

Builds a 1024x1024 newspaper front page for Wednesday 18 November 2026
from a fresh hero illustration (hero.webp, generated in-session) and
verified 18-November-2026 stories. Pure Pillow; no network at build time.

Layout (1024 x 1024, paper background):
  masthead / dateline / hero photo + caption / lead headline + deck /
  2x2 story grid / also-strip / footer with sources.
Run:  python3 compose.py   (writes entry.png next to this file)
"""
import hashlib
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
HERO_SRC = os.path.join(HERE, "hero.webp")
OUT_PNG = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MARGIN = 28
PAPER = (246, 241, 230)      # warm newsprint
INK = (18, 18, 18)           # near-black
RED = (163, 18, 18)          # kicker red
GREY = (96, 92, 84)          # footer grey
RULE = (18, 18, 18)
GRID_LINE = (196, 188, 172)

FONT_DIRS = [
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/truetype/liberation",
]


def find_font(names):
    """Return the first existing font path from the candidate names."""
    for directory in FONT_DIRS:
        for name in names:
            path = os.path.join(directory, name)
            if os.path.exists(path):
                return path
    raise FileNotFoundError("none of %s found under %s" % (names, FONT_DIRS))


SERIF_BOLD = find_font(["DejaVuSerif-Bold.ttf", "LiberationSerif-Bold.ttf"])
SERIF = find_font(["DejaVuSerif.ttf", "LiberationSerif-Regular.ttf"])
SERIF_ITALIC = find_font(["DejaVuSerif-Italic.ttf", "LiberationSerif-Italic.ttf"])
SANS = find_font(["DejaVuSans.ttf", "LiberationSans-Regular.ttf"])
SANS_BOLD = find_font(["DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf"])


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if text_w(draw, trial, fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, y, text, fnt, fill=INK, x0=0, x1=W, tracking=0):
    """Draw text centered between x0 and x1; tracking adds px between chars."""
    if tracking == 0:
        w = text_w(draw, text, fnt)
        draw.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)
        return
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = (x0 + x1 - total) / 2
    for ch, cw in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += cw + tracking


def draw_rule(draw, y, weight=2, x0=MARGIN, x1=W - MARGIN, fill=RULE):
    draw.rectangle([x0, y, x1, y + weight - 1], fill=fill)


def hero_image():
    """Crop the hero to the wide front-page band and resize it."""
    im = Image.open(HERO_SRC).convert("RGB")
    # The bridge, smoke and fallen span sit in the middle band of the frame.
    # Keep that band: cut empty sky above and foreground water below.
    left, top = 0, 360
    right, bottom = im.width, 955
    band = im.crop((left, top, right, bottom))
    target_w, target_h = W - 2 * MARGIN, 300
    return band.resize((target_w, target_h), Image.LANCZOS)


def story_cell(draw, x, y, w, h, kicker, headline, deck, accent):
    """One grid story: accent bar, kicker, headline (<=2 lines), deck (<=2)."""
    draw.rectangle([x, y, x + w, y + 5], fill=accent)
    cx = x
    cy = y + 10
    kf = font(SANS_BOLD, 19)
    draw.text((cx, cy), kicker, font=kf, fill=RED)
    cy += 24
    hf = font(SERIF_BOLD, 27)
    for line in wrap(draw, headline, hf, w)[:2]:
        draw.text((cx, cy), line, font=hf, fill=INK)
        cy += 32
    cy += 2
    df = font(SANS, 19)
    for line in wrap(draw, deck, df, w)[:2]:
        draw.text((cx, cy), line, font=df, fill=(52, 50, 46))
        cy += 22


def build():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)

    # --- Masthead -------------------------------------------------------
    y = 22
    draw_rule(d, y, 3)
    y += 12
    mast = font(SERIF_BOLD, 76)
    draw_centered(d, y, "THE WORLD TODAY", mast)
    y += 92
    date_f = font(SANS_BOLD, 29)
    draw_centered(d, y, "WEDNESDAY  ·  18 NOVEMBER 2026", date_f, tracking=2)
    y += 40
    draw_rule(d, y, 2)
    draw_rule(d, y + 5, 1)

    # --- Hero photo + caption -------------------------------------------
    hy = y + 14
    page.paste(hero_image(), (MARGIN, hy))
    d.rectangle([MARGIN, hy, W - MARGIN, hy + 300], outline=RULE, width=2)
    cy = hy + 300 + 8
    cap_f = font(SERIF_ITALIC, 19)
    caption = ("Illustration: a span of the Kerch Bridge lies in the strait after "
               "Ukrainian strikes. Russia hit two Kyiv bridges in reply.")
    for line in wrap(d, caption, cap_f, W - 2 * MARGIN):
        draw_centered(d, cy, line, cap_f, fill=(52, 50, 46))
        cy += 22

    # --- Lead headline + deck -------------------------------------------
    hy2 = cy + 6
    lead_f = font(SERIF_BOLD, 72)
    draw_centered(d, hy2, "BRIDGE WAR", lead_f)
    hy2 += 80
    deck_f = font(SANS, 23)
    deck = ("Ukraine strikes the Kerch crossing for a second day, collapsing a "
            "road span \u2014 as Moscow pounds Kyiv\u2019s bridges.")
    for line in wrap(d, deck, deck_f, W - 2 * MARGIN - 40):
        draw_centered(d, hy2, line, deck_f)
        hy2 += 29

    # --- Story grid ------------------------------------------------------
    gy = hy2 + 12
    draw_rule(d, gy, 2)
    gy += 14
    col_w = (W - 2 * MARGIN - 28) // 2
    row_h = 148
    stories = [
        ("MANILA", "Trump opens Asia tour in Manila",
         "Quad summit first; a Marcos welcome, then nuclear talks with Xi and Putin.",
         (24, 64, 110)),
        ("LONDON", "Britain sanctions settlement builders",
         "Eight West Bank firms hit, plus a group accused of blocking Gaza aid.",
         (120, 28, 28)),
        ("BAY OF BENGAL", "Cyclone Akvan bears down on India",
         "Severe storm by Wednesday; landfall due Friday with winds to 145 km/h.",
         (16, 96, 96)),
        ("SPORT", "Dhoni calls time on IPL career",
         "Chennai great to mentor the Super Kings as his playing days end.",
         (150, 104, 16)),
    ]
    for i, (kicker, head, deck_text, accent) in enumerate(stories):
        cx = MARGIN + (i % 2) * (col_w + 28)
        cy2 = gy + (i // 2) * (row_h + 8)
        story_cell(d, cx, cy2, col_w, row_h, kicker, head, deck_text, accent)
    fy = gy + 2 * row_h + 8 + 6

    # --- Footer: also-stories + sources on one line ----------------------
    draw_rule(d, fy, 1)
    fy += 9
    foot_f = font(SANS, 18)
    draw_centered(
        d, fy,
        "Also: Knesset elects a new speaker \u00b7 Baidu chief warns of an AI bubble  \u00b7  Sources: Reuters, AP, CNN, IMD",
        foot_f, fill=GREY)

    # --- Write out, keeping the file inside the 1 MiB cap -----------------
    page.save(OUT_PNG, format="PNG", optimize=True)
    size = os.path.getsize(OUT_PNG)
    if size > 1048576:
        page.save(OUT_PNG, format="JPEG", quality=88, optimize=True)
        size = os.path.getsize(OUT_PNG)
    digest = hashlib.sha256(open(OUT_PNG, "rb").read()).hexdigest()
    print("wrote %s  %dx%d  %d bytes  sha256=%s" % (OUT_PNG, W, H, size, digest))
    if size > 1048576:
        print("ERROR: still over 1 MiB", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(build())
