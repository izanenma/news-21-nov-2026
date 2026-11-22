#!/usr/bin/env python3
"""Saturday 21 November 2026, drawn as a one-page newspaper front page.

The picture is painted entirely in code with Pillow: flat colours, crisp
type, a small sketch map and two data bars. It needs no network and no
clock, so every run paints the same bytes. Usage: python3 render.py,
which writes entry.png beside this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
SIZE = 1024
EDGE = 34
SPAN = SIZE - 2 * EDGE

PAPER_RGB = (247, 243, 234)
INK_RGB = (20, 20, 20)
RED_RGB = (163, 22, 33)
NAVY_RGB = (29, 53, 87)
GREY_RGB = (85, 85, 85)
SAND_RGB = (216, 210, 194)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


class FrontPage:
    """A blank sheet plus the drawing helpers for the front page."""

    def __init__(self):
        self.canvas = Image.new("RGB", (SIZE, SIZE), PAPER_RGB)
        self.pen = ImageDraw.Draw(self.canvas)
        self.ink = INK_RGB
        self.red = RED_RGB
        self.navy = NAVY_RGB
        self.grey = GREY_RGB

    def face(self, filename, size):
        return ImageFont.truetype(os.path.join(FONT_DIR, filename), size)

    def serif_b(self, size):
        return self.face("DejaVuSerif-Bold.ttf", size)

    def sans_b(self, size):
        return self.face("DejaVuSans-Bold.ttf", size)

    def sans(self, size):
        return self.face("DejaVuSans.ttf", size)

    def fit(self, text, fnt, width):
        """Split text into lines that fit width (greedy word wrap)."""
        lines, current = [], ""
        for word in text.split(" "):
            trial = word if not current else current + " " + word
            if self.pen.textlength(trial, font=fnt) <= width or not current:
                current = trial
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    def block(self, x, y, text, fnt, width, gap, fill=None):
        """Paint wrapped text; return the y below its last line."""
        for line in self.fit(text, fnt, width):
            self.pen.text((x, y), line, font=fnt, fill=fill or self.ink)
            y += gap
        return y

    def hline(self, y, weight=2):
        self.pen.line([(EDGE, y), (SIZE - EDGE, y)], fill=self.ink, width=weight)

    def tag(self, x, y, text, size=22):
        self.pen.text((x, y), text, font=self.sans_b(size), fill=self.red)
        return y + size + 8

    def masthead(self):
        title = "THE WORLD"
        face = self.serif_b(88)
        left = (SIZE - self.pen.textlength(title, font=face)) / 2
        self.pen.text((left, 22), title, font=face, fill=self.ink)
        self.hline(132)
        dateline = "SATURDAY, 21 NOVEMBER 2026  ·  THE DAY IN ONE PAGE"
        dface = self.sans_b(21)
        dleft = (SIZE - self.pen.textlength(dateline, font=dface)) / 2
        self.pen.text((dleft, 146), dateline, font=dface, fill=self.ink)
        self.hline(180)

    def gulf(self, x, y, w, h):
        """A sketch map of the Gulf with the day's three flashpoints."""
        self.pen.rectangle([x, y, x + w, y + h], fill=self.navy)
        self.pen.text((x + 14, y + 10), "THE GULF", font=self.sans_b(17),
                      fill=(255, 255, 255))
        self.pen.text((x + 14, y + 32), "SKETCH MAP", font=self.sans(14),
                      fill=(180, 195, 220))
        self.pen.rectangle([x + 14, y + 58, x + w - 14, y + h - 14],
                           fill=(58, 95, 140))
        # Iran's shore above, Arabia's below; both kept clear of the dots.
        self.pen.line([(x + 14, y + 72), (x + 90, y + 64), (x + 150, y + 74),
                       (x + w - 14, y + 66)], fill=PAPER_RGB, width=3)
        self.pen.line([(x + 170, y + h - 50), (x + 220, y + h - 58),
                       (x + w - 14, y + h - 52)], fill=PAPER_RGB, width=3)
        marks = [
            ("BAHRAIN", "Iran's strike", 0.55, 0.42, (255, 176, 0), "start"),
            ("QESHM ISLAND", "drone 'downed'", 0.78, 0.58, RED_RGB, "end"),
            ("HORMUZ", "tankers attacked", 0.22, 0.74, (255, 176, 0), "start"),
        ]
        for name, note, fx, fy, colour, side in marks:
            cx, cy = x + w * fx, y + h * fy
            self.pen.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=colour,
                             outline=(255, 255, 255), width=2)
            if side == "end":
                self.pen.text((cx - 10, cy - 20), name, font=self.sans_b(15),
                              fill=(255, 255, 255), anchor="ra")
                self.pen.text((cx - 10, cy - 2), note, font=self.sans(13),
                              fill=(220, 228, 240), anchor="ra")
            else:
                self.pen.text((cx + 10, cy - 20), name, font=self.sans_b(15),
                              fill=(255, 255, 255))
                self.pen.text((cx + 10, cy - 2), note, font=self.sans(13),
                              fill=(220, 228, 240))
        self.pen.text((x + 14, y + h - 30), "PERSIAN GULF  ·  IRAN  ·  ARABIA",
                      font=self.sans(12), fill=(180, 195, 220))

    def barrage(self, x, y, w):
        """Two bars for the overnight strike on Ukraine: drones, missiles."""
        self.pen.text((x, y), "RUSSIA'S BIGGEST NOVEMBER BARRAGE",
                      font=self.sans_b(14), fill=self.grey)
        y += 22
        drone_w = int(w * 0.78)
        self.pen.rectangle([x, y, x + drone_w, y + 16], fill=(178, 34, 52))
        self.pen.rectangle([x + drone_w, y, x + w, y + 16], fill=SAND_RGB)
        self.pen.text((x + 6, y + 1), "404 DRONES", font=self.sans_b(12),
                      fill=(255, 255, 255))
        y += 22
        missile_w = int(w * 0.22)
        self.pen.rectangle([x, y, x + missile_w, y + 16], fill=self.navy)
        self.pen.rectangle([x + missile_w, y, x + w, y + 16], fill=SAND_RGB)
        self.pen.text((x + 6, y + 1), "111 MISSILES", font=self.sans_b(12),
                      fill=(255, 255, 255))
        return y + 16

    def badge(self, x, y, w):
        """A boxed note: the captured cartel boss was FBI most-wanted."""
        self.pen.rectangle([x, y, x + w, y + 60], outline=self.red, width=2)
        self.pen.text((x + 12, y + 8), "FBI 10 MOST WANTED",
                      font=self.sans_b(16), fill=self.red)
        self.pen.text((x + 12, y + 32), "Meza Flores, 62 — Beltran Leyva cartel",
                      font=self.sans(15), fill=self.ink)
        return y + 60

    def two_columns(self, y, left, right):
        """Two stories side by side; return the lower of their bottoms."""
        col = (SPAN - 36) // 2
        x2 = EDGE + col + 36
        end_left = self.tag(EDGE, y, left[0], 21)
        end_left = self.block(EDGE, end_left, left[1], self.serif_b(26),
                              col, 32)
        end_left = self.block(EDGE, end_left + 4, left[2], self.sans(18),
                              col, 24)
        end_right = self.tag(x2, y, right[0], 21)
        end_right = self.block(x2, end_right, right[1], self.serif_b(26),
                               col, 32)
        end_right = self.block(x2, end_right + 4, right[2], self.sans(18),
                               col, 24)
        return max(end_left, end_right), col, x2

    def build(self):
        self.masthead()
        # Lead story: the Gulf.
        y = self.tag(EDGE, 192, "GULF CRISIS", 22)
        y = self.block(EDGE, y, "Iran claims strikes on U.S. bases in Bahrain",
                       self.serif_b(40), 630, 48)
        lead_end = self.block(
            EDGE, y + 6,
            "Tehran says its Guards hit al-Riffa and Awali; Bahrain reports "
            "a fire at an industrial site and no injuries, while air "
            "defences stop other attacks and tanker strikes slow Hormuz oil.",
            self.sans(21), 630, 28)
        self.gulf(700, 192, 290, 230)
        lead_end = max(lead_end, 192 + 230)
        # Second row: Ukraine and Mexico.
        self.hline(lead_end + 12)
        row_end, col, x2 = self.two_columns(
            lead_end + 24,
            ("UKRAINE",
             "Russian missile hits Zelenskyy's hometown",
             "2 killed, 60 wounded in Kryvyi Rih; missiles land in Poland "
             "in the same barrage."),
            ("MEXICO",
             "Mexico captures \u201cEl Chapo Isidro\u201d",
             "FBI most-wanted cartel boss seized in Sinaloa; 11 dead in "
             "the violence that followed."))
        self.barrage(EDGE, row_end + 8, col)
        self.badge(x2, row_end + 8, col)
        row_end += 68
        # Third row: climate talks and markets.
        self.hline(row_end + 12)
        row_end, _, _ = self.two_columns(
            row_end + 24,
            ("CLIMATE",
             "COP31 in Antalya runs into overtime, no deal yet",
             "Talks pass their deadline; fossil fuels missing from the "
             "draft deal."),
            ("MARKETS",
             "AI sell-off drags U.S. stocks into correction",
             "Nasdaq erases its 2026 gains as chip shares slide."))
        # Fourth row: the World Court, full width.
        self.hline(row_end + 12)
        y = row_end + 24
        label = "WORLD COURT — "
        self.pen.text((EDGE, y), label, font=self.sans_b(24), fill=self.red)
        lx = EDGE + self.pen.textlength(label, font=self.sans_b(24))
        self.pen.text((lx, y), "Sanctions urged after Myanmar genocide ruling",
                      font=self.serif_b(24), fill=self.ink)
        y = self.block(
            EDGE, y + 32,
            "The Hague found Myanmar committed genocide against the "
            "Rohingya, 9–6 — the first such ruling against a State.",
            self.sans(18), SPAN, 24)
        # Also strip.
        self.hline(y + 12)
        y += 24
        also = "ALSO: "
        self.pen.text((EDGE, y), also, font=self.sans_b(18), fill=self.red)
        ax = EDGE + self.pen.textlength(also, font=self.sans_b(18))
        self.block(ax, y,
                   "Nigeria boat capsizes, 24 dead  ·  Denmark to expel "
                   "Russian envoy  ·  Nvidia halts H200 chips to China  ·  "
                   "Hormuz oil shipments down 15%",
                   self.sans(18), SIZE - EDGE - ax, 24)

    def save(self):
        path = os.path.join(ROOT, "entry.png")
        self.canvas.save(path, "PNG", optimize=True)
        print("wrote entry.png", self.canvas.size)


if __name__ == "__main__":
    page = FrontPage()
    page.build()
    page.save()
