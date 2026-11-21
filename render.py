#!/usr/bin/env python3
"""Draw the front page for Saturday 21 November 2026 as a 1024x1024 PNG.

Newspaper layout, all vector art drawn with Pillow. Deterministic: no
randomness, no clock, no network. Run: python3 render.py -> entry.png
"""
import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (16, 16, 16)
RED = (158, 16, 16)
GREY = (96, 91, 80)
DARKBLUE = (24, 52, 96)
LIGHTBLUE = (214, 228, 240)
GOLD = (201, 162, 39)
GREEN = (46, 125, 50)
ORANGE = (232, 126, 32)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIFB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, fill=INK):
    """Draw wrapped paragraph; returns y after the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def headline(draw, x, y, text, fnt, max_w, leading):
    """Draw a wrapped headline in upper case; returns y after it."""
    return para(draw, x, y, text, fnt, max_w, leading)


def kicker(draw, x, y, text):
    draw.text((x, y), text, font=font(SANSB, 15), fill=RED)
    return y + 22


def hrule(draw, x0, x1, y, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def starburst(draw, cx, cy, r, colour):
    """Explosion burst: alternating long/short spikes."""
    pts = []
    for i in range(24):
        ang = math.pi * 2 * i / 24
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=colour)
    draw.ellipse([cx - r * 0.28, cy - r * 0.28, cx + r * 0.28, cy + r * 0.28],
                 fill=(255, 214, 90))


def lead_art(draw, x, y, w, h):
    """Night sky over a Kyiv-style skyline with two explosions."""
    draw.rectangle([x, y, x + w, y + h], fill=(18, 30, 58))
    # stars
    for sx, sy in [(0.08, 0.15), (0.22, 0.08), (0.35, 0.2), (0.5, 0.1),
                   (0.66, 0.18), (0.8, 0.07), (0.92, 0.2), (0.45, 0.28),
                   (0.58, 0.05), (0.95, 0.35)]:
        px, py = x + int(sx * w), y + int(sy * h)
        draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 255, 255))
    # skyline silhouette
    base = y + h
    skyline = [(0, 0.62), (0.08, 0.62), (0.08, 0.48), (0.14, 0.48),
               (0.14, 0.62), (0.2, 0.62), (0.2, 0.4), (0.24, 0.4),
               (0.24, 0.55), (0.3, 0.55), (0.3, 0.66), (0.38, 0.66),
               (0.38, 0.5), (0.44, 0.5), (0.44, 0.44), (0.47, 0.44),
               (0.47, 0.62), (0.55, 0.62), (0.55, 0.52), (0.62, 0.52),
               (0.62, 0.66), (0.7, 0.66), (0.7, 0.46), (0.76, 0.46),
               (0.76, 0.6), (0.84, 0.6), (0.84, 0.52), (0.9, 0.52),
               (0.9, 0.64), (1.0, 0.64)]
    pts = [(x + int(fx * w), base - int((1 - fy) * h * 0.0) - int(fy * 0 + 0))
           for fx, fy in skyline]
    # build polygon from top edge down to base
    poly = [(x + int(fx * w), y + int(fy * h)) for fx, fy in skyline]
    poly += [(x + w, base), (x, base)]
    draw.polygon(poly, fill=(8, 12, 26))
    # lit windows
    for wx, wy in [(0.1, 0.55), (0.22, 0.5), (0.4, 0.58), (0.58, 0.58),
                   (0.72, 0.55), (0.86, 0.58), (0.32, 0.6), (0.65, 0.6)]:
        px, py = x + int(wx * w), y + int(wy * h)
        draw.rectangle([px, py, px + 5, py + 7], fill=(255, 196, 66))
    # explosions
    starburst(draw, x + int(0.3 * w), y + int(0.3 * h), 26, (232, 110, 20))
    starburst(draw, x + int(0.72 * w), y + int(0.22 * h), 18, (240, 160, 40))
    # missile trail
    draw.line([(x + int(0.55 * w), y + int(0.05 * h)),
               (x + int(0.72 * w), y + int(0.2 * h))],
              fill=(255, 220, 120), width=3)
    # caption bar
    draw.rectangle([x, y + h - 26, x + w, y + h], fill=(0, 0, 0))
    draw.text((x + 10, y + h - 21),
              "KYIV UNDER FIRE — one of the war's largest attacks",
              font=font(SANSB, 12), fill=(255, 255, 255))


def chart_art(draw, x, y, w, h):
    """Falling market line on a pale grid."""
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255),
                   outline=GREY, width=1)
    for gy in range(1, 4):
        gyv = y + h * gy / 4
        draw.line([(x + 6, gyv), (x + w - 6, gyv)], fill=(220, 216, 205),
                  width=1)
    pts = [(0.04, 0.18), (0.18, 0.26), (0.3, 0.22), (0.44, 0.42),
           (0.56, 0.5), (0.68, 0.62), (0.8, 0.72), (0.96, 0.88)]
    xy = [(x + int(fx * w), y + int(fy * h)) for fx, fy in pts]
    area = xy + [(x + int(0.96 * w), y + h - 4), (x + int(0.04 * w), y + h - 4)]
    draw.polygon(area, fill=(248, 220, 218))
    draw.line(xy, fill=RED, width=4, joint="curve")
    draw.ellipse([xy[-1][0] - 5, xy[-1][1] - 5, xy[-1][0] + 5, xy[-1][1] + 5],
                 fill=RED)
    label = "S&P 500  -3.7%"
    dlen = draw.textlength(label, font=font(SANSB, 14))
    draw.text((x + w - dlen - 8, y + 6), label, font=font(SANSB, 14),
              fill=RED)


def globe_art(draw, x, y, w, h):
    """Simple globe, centred in the strip."""
    cx, cy, r = x + w // 2, y + h // 2, min(w, h) // 2 - 4
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(112, 168, 214),
                 outline=DARKBLUE, width=2)
    draw.ellipse([cx - r * 0.55, cy - r * 0.5, cx + r * 0.1, cy + r * 0.15],
                 fill=GREEN)
    draw.ellipse([cx + r * 0.1, cy + r * 0.25, cx + r * 0.6, cy + r * 0.7],
                 fill=GREEN)
    for lat in (-0.5, 0.0, 0.5):
        yy = cy + int(lat * r)
        half = int(math.sqrt(max(r * r - (yy - cy) ** 2, 0)))
        draw.arc([cx - half, yy - 6, cx + half, yy + 6], 0, 180,
                 fill=(255, 255, 255), width=2)


def pill_art(draw, x, y, w, h):
    """Capsule pill and a small cross."""
    cx, cy = x + w // 2 - 14, y + h // 2
    draw.rounded_rectangle([cx - 52, cy - 20, cx + 52, cy + 20], radius=20,
                           fill=(255, 255, 255), outline=INK, width=2)
    draw.rounded_rectangle([cx - 52, cy - 20, cx, cy + 20], radius=20,
                           fill=RED)
    draw.rectangle([cx - 52, cy - 20, cx, cy + 20], fill=RED)
    draw.ellipse([cx - 52, cy - 20, cx - 12, cy + 20], fill=RED)
    # cross badge
    bx, by = x + w - 42, y + 12
    draw.ellipse([bx - 16, by - 16, bx + 16, by + 16], fill=GREEN)
    draw.rectangle([bx - 3, by - 10, bx + 3, by + 10], fill=(255, 255, 255))
    draw.rectangle([bx - 10, by - 3, bx + 10, by + 3], fill=(255, 255, 255))


def eu_art(draw, x, y, w, h):
    """Blue roundel ringed with twelve gold stars."""
    cx, cy, r = x + w // 2, y + h // 2, min(w, h) // 2 - 6
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=DARKBLUE)
    for i in range(12):
        ang = math.pi * 2 * i / 12 - math.pi / 2
        sx, sy = cx + int(0.68 * r * math.cos(ang)), cy + int(0.68 * r * math.sin(ang))
        draw.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=GOLD)


def story(draw, x, y, w, kick, head, deck, art, art_h=48):
    """One column story: kicker, headline, deck, art strip."""
    y = kicker(draw, x, y, kick)
    y = headline(draw, x, y, head, font(SERIFB, 25), w, 30)
    y += 3
    y = para(draw, x, y, deck, font(SANS, 16), w, 20)
    y += 6
    art(draw, x, y, w, art_h)
    return y + art_h


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36  # margin
    X0, X1 = M, W - M

    # ---- masthead ----
    d.text((X0, 20), "THE WORLD IN ONE DAY",
           font=font(SERIFB, 58), fill=INK)
    hrule(d, X0, X1, 100, width=3)
    hrule(d, X0, X1, 105, width=1)
    d.text((X0, 113), "SATURDAY, 21 NOVEMBER 2026",
           font=font(SANSB, 18), fill=INK)
    right = "ONE DAY  •  ONE PAGE  •  THE WORLD"
    d.text((X1 - d.textlength(right, font=font(SANSB, 15)), 115), right,
           font=font(SANSB, 15), fill=GREY)
    hrule(d, X0, X1, 140, width=1)

    # ---- lead story ----
    y = 152
    y = kicker(d, X0, y, "WAR IN UKRAINE  —  LEAD")
    y = headline(d, X0, y,
                 "RUSSIAN MISSILES FALL IN POLAND AS KYIV IS POUNDED",
                 font(SERIFB, 38), X1 - X0, 44)
    y += 4
    # deck left, art right
    deck_w = 520
    dy = para(d, X0, y,
              "Moscow fired more than 400 drones and 110 missiles "
              "overnight — at least 8 killed, three Dnipro bridges "
              "damaged, power cut. Two Russian cruise missiles and a "
              "suspected drone came down in Poland; Warsaw calls it a "
              "deliberate provocation and NATO jets were scrambled.",
              font(SANS, 18), deck_w, 23)
    lead_art(d, X0 + deck_w + 24, y, X1 - (X0 + deck_w + 24), 140)
    y = max(dy, y + 140) + 8
    hrule(d, X0, X1, y, width=1)
    y += 8

    # ---- row two: markets + climate ----
    col_w = (X1 - X0 - 28) // 2
    y2 = story(d, X0, y, col_w,
               "MARKETS",
               "AI ROUT DRAGS S&P 500 INTO CORRECTION",
               "US stocks fell 3.7% on Friday as the sell-off in AI and "
               "chip shares spread. The S&P 500 and the Dow both closed in "
               "correction territory.",
               chart_art)
    y2b = story(d, X0 + col_w + 28, y, col_w,
                "CLIMATE  —  COP31, ANTALYA",
                "CLIMATE TALKS RUN INTO OVERTIME",
                "Negotiators passed their deadline with no deal — the draft "
                "text does not even mention fossil fuels. Nearly 200 nations "
                "remain split; the next summit goes to Addis Ababa.",
                globe_art)
    y = max(y2, y2b) + 6
    hrule(d, X0, X1, y, width=1)
    y += 8

    # ---- row three: health + europe ----
    y3 = story(d, X0, y, col_w,
               "HEALTH",
               "CANCER PILL WIPES OUT TUMOURS IN 1 IN 12",
               "Daraxonrasib with chemotherapy left no detectable cancer in "
               "5 of 61 advanced pancreatic patients, and held the disease "
               "in check in 90%. Results were presented in Barcelona.",
               pill_art)
    y3b = story(d, X0 + col_w + 28, y, col_w,
                "EUROPE",
                "UK AND EU SIGN BIGGEST POST-BREXIT DEALS",
                "Three pacts on food exports, carbon markets and youth "
                "mobility — the deepest reset of Britain's ties with the EU "
                "since Brexit — signed in Brussels.",
                eu_art)
    y = max(y3, y3b) + 6
    hrule(d, X0, X1, y, width=1)
    y += 8

    # ---- also today ----
    d.text((X0, y), "ALSO TODAY", font=font(SANSB, 15), fill=RED)
    y += 22
    briefs = [
        ("GEN Z PROTESTS SPREAD", "Youth-led protests reported in 25 European countries."),
        ("IRAN DOWNS US DRONE", "Tehran says it shot down an MQ-9 over the Strait of Hormuz."),
        ("MYANMAR REJECTS RULING", "Naypyidaw calls the world court's genocide verdict \u201cunfair\u201d."),
        ("FBI DATABASE HACKED", "US officials probe a reported breach as outages continue."),
    ]
    bw = (X1 - X0 - 3 * 20) // 4
    for i, (t, b) in enumerate(briefs):
        bx = X0 + i * (bw + 20)
        d.text((bx, y), t, font=font(SANSB, 13), fill=INK)
        para(d, bx, y + 18, b, font(SANS, 13), bw, 16, fill=GREY)
    y += 54
    hrule(d, X0, X1, y, width=1)
    y += 6
    d.text((X0, y),
           "All events of Saturday 21 November 2026  •  Sources: AP, Reuters, NYT, BBC, HRW, Amnesty International",
           font=font(SANS, 12), fill=GREY)
    return img


if __name__ == "__main__":
    page = build()
    page.save("entry.png", optimize=True)
    print("saved entry.png", page.size)
