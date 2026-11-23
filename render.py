#!/usr/bin/env python3
"""Build-time renderer for the news-image-20261123 entry.

Draws a one-page broadsheet that sums up Monday 23 November 2026:
COP31 collapses in Antalya as the lead, three more stories below, and
an "also today" strip. Everything is procedural Pillow drawing -- no
photographs, no network, no clock, no randomness -- so rendering twice
produces a byte-identical PNG.

Run:  python3 render.py        # writes entry.png next to this file
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (245, 239, 224)      # warm cream page
INK = (27, 27, 27)           # near-black ink
TEAL = (12, 59, 57)          # header band
TEAL_MID = (20, 99, 92)      # globe
TEAL_DARK = (9, 43, 41)      # globe shading
RED = (179, 39, 30)          # accent / crack / stamp
ORANGE = (224, 123, 42)      # flame
YELLOW = (242, 194, 48)      # flame core
GOLD = (201, 162, 39)        # rules and "also" label
PANEL = (233, 225, 203)      # pictogram panels
BODY = (58, 55, 46)          # body text
MUTED = (185, 178, 160)      # footer text on ink
CREAM = (245, 239, 224)
GREY = (120, 116, 104)       # smoke
HULL = (31, 42, 46)          # ship hulls
WOOD = (107, 68, 35)         # gavel

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines fitting max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def spaced(draw, xy, text, fnt, fill, tracking=3):
    """Draw text with extra space between letters (small-caps feel)."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking
    return x


def flame(draw, cx, base_y, w, h):
    """Layered teardrop flame rising from (cx, base_y)."""
    draw.polygon(
        [(cx - w / 2, base_y), (cx - w * 0.28, base_y - h * 0.62),
         (cx, base_y - h), (cx + w * 0.28, base_y - h * 0.62),
         (cx + w / 2, base_y)],
        fill=ORANGE,
    )
    draw.polygon(
        [(cx - w * 0.26, base_y), (cx - w * 0.12, base_y - h * 0.55),
         (cx, base_y - h * 0.78), (cx + w * 0.12, base_y - h * 0.55),
         (cx + w * 0.26, base_y)],
        fill=YELLOW,
    )


def smoke(draw, cx, top_y):
    for dx, dy, r in ((-24, 0, 12), (0, -12, 14), (24, -22, 10)):
        draw.ellipse([cx + dx - r, top_y + dy - r,
                       cx + dx + r, top_y + dy + r], fill=GREY)


def draw_tanker(draw, ox, oy):
    """Oil tanker with a burning deck container, on waves."""
    draw.polygon([(ox + 8, oy + 96), (ox + 296, oy + 96),
                  (ox + 272, oy + 132), (ox + 30, oy + 132)], fill=HULL)
    draw.rectangle([ox + 40, oy + 62, ox + 96, oy + 96], fill=TEAL_MID)
    draw.rectangle([ox + 104, oy + 62, ox + 160, oy + 96], fill=RED)
    draw.rectangle([ox + 168, oy + 62, ox + 224, oy + 96], fill=GOLD)
    draw.rectangle([ox + 238, oy + 44, ox + 268, oy + 96], fill=CREAM)
    flame(draw, ox + 132, oy + 62, 44, 52)
    smoke(draw, ox + 132, oy + 30)
    for k in range(4):
        x0 = ox + 10 + k * 76
        draw.arc([x0, oy + 136, x0 + 46, oy + 148], 180, 360,
                 fill=TEAL_MID, width=4)


def draw_ship(draw, ox, oy):
    """Cargo ship ablaze, drifting with smoke."""
    draw.polygon([(ox + 16, oy + 100), (ox + 288, oy + 100),
                  (ox + 262, oy + 134), (ox + 40, oy + 134)], fill=HULL)
    draw.rectangle([ox + 52, oy + 66, ox + 118, oy + 100], fill=TEAL_MID)
    draw.rectangle([ox + 126, oy + 66, ox + 192, oy + 100], fill=GOLD)
    draw.rectangle([ox + 210, oy + 40, ox + 244, oy + 100], fill=CREAM)
    draw.rectangle([ox + 250, oy + 22, ox + 256, oy + 100], fill=INK)
    flame(draw, ox + 85, oy + 66, 46, 56)
    smoke(draw, ox + 85, oy + 30)
    for k in range(4):
        x0 = ox + 14 + k * 74
        draw.arc([x0, oy + 138, x0 + 44, oy + 150], 180, 360,
                 fill=TEAL_MID, width=4)


def draw_factory(draw, ox, oy):
    """Factory with sawtooth roof, chimney smoke and a fire window."""
    draw.rectangle([ox + 30, oy + 78, ox + 240, oy + 138], fill=HULL)
    draw.polygon([(ox + 30, oy + 78), (ox + 30, oy + 52),
                  (ox + 82, oy + 78), (ox + 134, oy + 52),
                  (ox + 186, oy + 78), (ox + 240, oy + 52),
                  (ox + 240, oy + 78)], fill=TEAL_MID)
    draw.rectangle([ox + 252, oy + 30, ox + 276, oy + 138], fill=INK)
    smoke(draw, ox + 264, oy + 34)
    draw.rectangle([ox + 52, oy + 100, ox + 88, oy + 138], fill=ORANGE)
    flame(draw, ox + 70, oy + 100, 26, 34)
    draw.rectangle([ox + 120, oy + 100, ox + 150, oy + 122], fill=CREAM)
    draw.rectangle([ox + 170, oy + 100, ox + 200, oy + 122], fill=CREAM)


def draw_globe(base):
    """Cracked globe with a gavel and a NO DEAL stamp, right of hero."""
    cx, cy, r = 806, 332, 128
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=TEAL_MID + (255,))
    # latitude / longitude guides
    d.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2],
              outline=TEAL_DARK + (255,), width=4)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r],
              outline=TEAL_DARK + (255,), width=4)
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=TEAL_DARK + (255,), width=10)
    # cream landmasses, clipped to the disc
    land = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(land)
    ld.ellipse([cx - 96, cy - 96, cx - 18, cy - 34], fill=CREAM + (255,))
    ld.ellipse([cx - 52, cy - 62, cx + 12, cy - 6], fill=CREAM + (255,))
    ld.ellipse([cx + 8, cy + 6, cx + 92, cy + 66], fill=CREAM + (255,))
    ld.ellipse([cx - 92, cy + 28, cx - 30, cy + 92], fill=CREAM + (255,))
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    land = Image.composite(land, Image.new("RGBA", (W, H), (0, 0, 0, 0)), mask)
    layer = Image.alpha_composite(layer, land)
    d = ImageDraw.Draw(layer)
    # jagged crack across the disc
    crack = [(cx - 88, cy - 118), (cx - 46, cy - 74), (cx - 70, cy - 30),
             (cx - 18, cy + 14), (cx - 44, cy + 58), (cx + 6, cy + 104),
             (cx + 40, cy + 128)]
    d.line(crack, fill=RED + (255,), width=9, joint="curve")
    d.line([(cx - 46, cy - 74), (cx - 6, cy - 92)], fill=RED + (255,), width=6)
    d.line([(cx - 18, cy + 14), (cx + 26, cy - 6)], fill=RED + (255,), width=6)
    base.alpha_composite(layer)
    # gavel, drawn flat then rotated
    g = Image.new("RGBA", (150, 105), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    gd.rounded_rectangle([16, 12, 124, 50], radius=9, fill=WOOD + (255,))
    gd.rectangle([16, 26, 124, 35], fill=(60, 36, 16, 255))
    gd.rectangle([64, 50, 84, 98], fill=(140, 92, 48, 255))
    g = g.rotate(-28, expand=True, resample=Image.BICUBIC)
    base.alpha_composite(g, (cx + 8, cy - r - 52))
    # NO DEAL stamp
    s = Image.new("RGBA", (220, 80), (0, 0, 0, 0))
    sd = ImageDraw.Draw(s)
    sd.rounded_rectangle([4, 4, 216, 76], radius=8, outline=RED + (255,), width=5)
    sd.text((110, 40), "NO DEAL", font=SANS_B(38), fill=RED + (255,), anchor="mm")
    s = s.rotate(-11, expand=True, resample=Image.BICUBIC)
    base.alpha_composite(s, (cx - 26, cy + r - 40))


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- header band -------------------------------------------------
    draw.rectangle([0, 0, W, 118], fill=TEAL)
    draw.rectangle([0, 118, W, 124], fill=GOLD)
    spaced(draw, (48, 32), "ONE DAY · ONE IMAGE", SANS_B(27), CREAM)
    date = "MONDAY 23 NOVEMBER 2026"
    draw.text((976, 32), date, font=SANS_B(27), fill=CREAM, anchor="ra")
    spaced(draw, (48, 76), "WORLD NEWS IN ONE PAGE", SANS_B(16), GOLD)
    draw.text((976, 76), "ANTALYA · TURKEY", font=SANS_B(16),
              fill=GOLD, anchor="ra")

    # ---- hero: COP31 collapses ---------------------------------------
    spaced(draw, (48, 152), "CLIMATE SUMMIT — ANTALYA, TURKEY",
           SANS_B(23), RED)
    draw.text((46, 182), "COP31", font=SERIF_B(90), fill=INK)
    draw.text((46, 282), "COLLAPSES", font=SERIF_B(90), fill=INK)
    sub = ("No deal after two weeks of talks. The longest climate "
           "summit ever ends with no agreement — and no mention "
           "of fossil fuels.")
    y = 396
    for line in wrap(draw, sub, SANS(24), 560):
        draw.text((48, y), line, font=SANS(24), fill=BODY)
        y += 32
    chips = ["194 NATIONS", "2 WEEKS OF TALKS", "LONGEST COP EVER"]
    cx = 48
    for chip in chips:
        tw = draw.textlength(chip, font=SANS_B(18))
        draw.rounded_rectangle([cx, 506, cx + tw + 28, 540], radius=17,
                               outline=TEAL, width=2)
        draw.text((cx + 14, 523), chip, font=SANS_B(18), fill=TEAL, anchor="lm")
        cx += tw + 44

    img = img.convert("RGBA")
    draw_globe(img)
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)

    # ---- divider ------------------------------------------------------
    draw.line([(48, 566), (976, 566)], fill=INK, width=2)
    label = "THE REST OF THE DAY"
    lw = draw.textlength(label, font=SANS_B(20))
    draw.rectangle([512 - lw / 2 - 16, 552, 512 + lw / 2 + 16, 580], fill=PAPER)
    spaced(draw, (512 - lw / 2 - 10, 556), label, SANS_B(20), INK)

    # ---- three story tiles --------------------------------------------
    tiles = [
        ("WAR AT SEA", draw_tanker,
         "Iran strike wounds two in Bahrain; tankers hit in the "
         "Strait of Hormuz."),
        ("SHIP ABLAZE", draw_ship,
         "Russian cargo ship still burning off Finland after a "
         "drone strike; crew evacuated."),
        ("FACTORY FIRE", draw_factory,
         "Seven dead and 50 missing after a blaze at a candy "
         "factory in Indonesia."),
    ]
    for i, (title, pic, body) in enumerate(tiles):
        x0 = 48 + i * 312
        draw.rounded_rectangle([x0, 592, x0 + 304, 742], radius=10, fill=PANEL)
        pic(draw, x0, 592)
        draw.text((x0, 758), title, font=SANS_B(25), fill=INK)
        y = 792
        for line in wrap(draw, body, SANS(19), 304):
            draw.text((x0, y), line, font=SANS(19), fill=BODY)
            y += 26

    # ---- bottom band ---------------------------------------------------
    draw.rectangle([0, 892, W, H], fill=INK)
    spaced(draw, (48, 910), "ALSO TODAY", SANS_B(21), GOLD)
    also = ("Democrats clinch the biggest US House majority since 1992 · "
            "14 missing after a Russian drone hits a building near Kyiv · "
            "Verstappen wins the Las Vegas Grand Prix")
    y = 942
    for line in wrap(draw, also, SANS(20), 928):
        draw.text((48, y), line, font=SANS(20), fill=CREAM)
        y += 27
    draw.text((48, 996), "Sources: CNN · Reuters · Le Monde · AFP — "
              "Monday 23 November 2026 · Drawn in code; no photograph",
              font=SANS(15), fill=MUTED)
    return img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    build().save(out, format="PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
