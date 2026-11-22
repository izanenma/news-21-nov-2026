#!/usr/bin/env python3
"""Render the news-image-20261121 entry: a one-page newspaper front page
summing up Saturday 21 November 2026's world news, as a 1024x1024 PNG.

Everything is drawn programmatically with Pillow: crisp text, flat colours,
simple schematic motifs. No network, no timestamps, no randomness, so the
output is byte-identical on every run. Run: python3 render.py (writes
entry.png next to this file).
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024
M = 34  # margin
CW = W - 2 * M

PAPER = (247, 243, 234)
INK = (20, 20, 20)
RED = (163, 22, 33)
NAVY = (29, 53, 87)
GRAY = (85, 85, 85)
RULE = (20, 20, 20)

FD = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, fill=INK):
    """Draw wrapped text; returns the y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, x1, y, w=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w)


def kicker(draw, x, y, text, size=22):
    draw.text((x, y), text, font=SANS_B(size), fill=RED)
    return y + size + 8


def gulf_map(draw, x, y, w, h):
    """Schematic of the Gulf: sea, coastline, three sites of 21 Nov."""
    draw.rectangle([x, y, x + w, y + h], fill=NAVY)
    draw.text((x + 14, y + 10), "THE GULF", font=SANS_B(17), fill=(255, 255, 255))
    draw.text((x + 14, y + 32), "SCHEMATIC MAP", font=SANS(14), fill=(180, 195, 220))
    # sea
    draw.rectangle([x + 14, y + 58, x + w - 14, y + h - 14], fill=(58, 95, 140))
    # simplified coastline (Iran above, Arabia below), clear of the sites
    draw.line([(x + 14, y + 72), (x + 90, y + 64), (x + 150, y + 74),
               (x + w - 14, y + 66)], fill=(247, 243, 234), width=3)
    # bottom coastline kept to the right, clear of the HORMUZ labels
    draw.line([(x + 170, y + h - 50), (x + 220, y + h - 58),
               (x + w - 14, y + h - 52)], fill=(247, 243, 234), width=3)
    sites = [
        ("BAHRAIN", "Iran strike", 0.55, 0.42, (255, 176, 0), "start"),
        ("QESHM ISLAND", "Iran: drone downed", 0.78, 0.58, RED, "end"),
        ("HORMUZ", "tankers hit", 0.22, 0.74, (255, 176, 0), "start"),
    ]
    for name, what, fx, fy, col, anchor in sites:
        cx, cy = x + w * fx, y + h * fy
        draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=col,
                     outline=(255, 255, 255), width=2)
        if anchor == "end":
            draw.text((cx - 10, cy - 20), name, font=SANS_B(15),
                      fill=(255, 255, 255), anchor="ra")
            draw.text((cx - 10, cy - 2), what, font=SANS(13),
                      fill=(220, 228, 240), anchor="ra")
        else:
            draw.text((cx + 10, cy - 20), name, font=SANS_B(15), fill=(255, 255, 255))
            draw.text((cx + 10, cy - 2), what, font=SANS(13), fill=(220, 228, 240))
    draw.text((x + 14, y + h - 30), "GULF  ·  IRAN  ·  ARABIAN PENINSULA",
              font=SANS(12), fill=(180, 195, 220))


def barrage_bar(draw, x, y, w):
    """404 drones, 111 missiles: two stacked bars."""
    draw.text((x, y), "RUSSIA'S BIGGEST NOVEMBER BARRAGE", font=SANS_B(14), fill=GRAY)
    y += 22
    dw = int(w * 0.78)
    draw.rectangle([x, y, x + dw, y + 16], fill=(178, 34, 52))
    draw.rectangle([x + dw, y, x + w, y + 16], fill=(216, 210, 194))
    draw.text((x + 6, y + 1), "404 DRONES", font=SANS_B(12), fill=(255, 255, 255))
    y += 22
    mw = int(w * 0.22)
    draw.rectangle([x, y, x + mw, y + 16], fill=(29, 53, 87))
    draw.rectangle([x + mw, y, x + w, y + 16], fill=(216, 210, 194))
    draw.text((x + 6, y + 1), "111 MISSILES", font=SANS_B(12), fill=(255, 255, 255))
    return y + 16


def wanted_badge(draw, x, y, w):
    """FBI 10 most-wanted badge box."""
    draw.rectangle([x, y, x + w, y + 60], outline=RED, width=2)
    draw.text((x + 12, y + 8), "FBI 10 MOST WANTED", font=SANS_B(16), fill=RED)
    draw.text((x + 12, y + 32), "Meza Flores, 62 — Beltran Leyva cartel",
              font=SANS(15), fill=INK)
    return y + 60


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    title = "THE WORLD"
    tf = SERIF_B(88)
    d.text(((W - d.textlength(title, font=tf)) / 2, 22), title, font=tf, fill=INK)
    rule(d, M, W - M, 132)
    date_line = "SATURDAY, 21 NOVEMBER 2026  ·  THE DAY IN ONE PAGE"
    df = SANS_B(21)
    d.text(((W - d.textlength(date_line, font=df)) / 2, 146), date_line,
           font=df, fill=INK)
    rule(d, M, W - M, 180)

    # ---- Lead: Iran strikes U.S. bases in Bahrain ----
    lx, lw = M, 630
    y = kicker(d, lx, 192, "WAR IN THE GULF", 22)
    y = para(d, lx, y, "Iran says it struck U.S. bases in Bahrain",
             SERIF_B(40), lw, 48)
    lead_end = para(d, lx, y + 6,
                    "Guards claim hits at al-Riffa and Awali; Bahrain reports "
                    "an industrial fire, no injuries; air defences intercept "
                    "other attacks as Hormuz tanker strikes cut oil shipments.",
                    SANS(21), lw, 28)
    gulf_map(d, 700, 192, 290, 230)
    lead_end = max(lead_end, 192 + 230)

    # ---- Row 2: Kryvyi Rih | El Chapo Isidro ----
    col_w = (CW - 36) // 2
    x2 = M + col_w + 36
    rule(d, M, W - M, lead_end + 12)
    y = lead_end + 24
    y1 = kicker(d, M, y, "UKRAINE", 21)
    y1 = para(d, M, y1, "Russian missile hits Zelenskyy's hometown",
              SERIF_B(26), col_w, 32)
    y1 = para(d, M, y1 + 4, "2 killed, 60 wounded in Kryvyi Rih; missiles "
              "land in Poland in the same barrage.", SANS(18), col_w, 24)
    y2 = kicker(d, x2, y, "MEXICO", 21)
    y2 = para(d, x2, y2, "Mexico captures \u201cEl Chapo Isidro\u201d",
              SERIF_B(26), col_w, 32)
    y2 = para(d, x2, y2 + 4, "FBI most-wanted cartel boss seized in Sinaloa; "
              "11 dead in the violence that followed.", SANS(18), col_w, 24)
    row2_end = max(y1, y2)
    barrage_bar(d, M, row2_end + 8, col_w)
    wanted_badge(d, x2, row2_end + 8, col_w)
    row2_end += 68

    # ---- Row 3: COP31 | AI sell-off ----
    rule(d, M, W - M, row2_end + 12)
    y = row2_end + 24
    y1 = kicker(d, M, y, "CLIMATE", 21)
    y1 = para(d, M, y1, "COP31 in Antalya runs into overtime, no deal yet",
              SERIF_B(26), col_w, 32)
    y1 = para(d, M, y1 + 4, "Talks pass their deadline; fossil fuels missing "
              "from the draft deal.", SANS(18), col_w, 24)
    y2 = kicker(d, x2, y, "MARKETS", 21)
    y2 = para(d, x2, y2, "AI sell-off drags U.S. stocks into correction",
              SERIF_B(26), col_w, 32)
    y2 = para(d, x2, y2 + 4, "Nasdaq erases its 2026 gains as chip shares "
              "slide.", SANS(18), col_w, 24)
    row3_end = max(y1, y2)

    # ---- Row 4: World Court ----
    rule(d, M, W - M, row3_end + 12)
    y = row3_end + 24
    d.text((M, y), "WORLD COURT — ", font=SANS_B(24), fill=RED)
    hx = M + d.textlength("WORLD COURT — ", font=SANS_B(24))
    d.text((hx, y), "Sanctions urged after Myanmar genocide ruling",
           font=SERIF_B(24), fill=INK)
    y = para(d, M, y + 32, "The Hague found Myanmar committed genocide "
             "against the Rohingya, 9–6 — the first such ruling against a State.",
             SANS(18), CW, 24)

    # ---- ALSO strip ----
    rule(d, M, W - M, y + 12)
    y += 24
    d.text((M, y), "ALSO: ", font=SANS_B(18), fill=RED)
    ax = M + d.textlength("ALSO: ", font=SANS_B(18))
    para(d, ax, y, "Nigeria boat capsizes, 24 dead  ·  Denmark to expel "
         "Russian envoy  ·  Nvidia halts H200 chips to China  ·  Hormuz oil "
         "shipments down 15%", SANS(18), W - M - ax, 24)

    img.save(os.path.join(HERE, "entry.png"), "PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
