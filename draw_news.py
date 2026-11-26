#!/usr/bin/env python3
"""Draw the 26 November 2026 world-news image (1024x1024 PNG).

Stories verified against Reuters / Japan Times / Qatar Tribune /
Economic Times reporting of 26 November 2026, read on the day.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
RED = (179, 32, 44)
BLUE = (31, 78, 121)
GREY = (110, 108, 100)
CARD = (255, 255, 255)
DARK = (24, 30, 38)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)

F_TITLE = font("DejaVuSans-Bold.ttf", 58)
F_DATE = font("DejaVuSans-Bold.ttf", 30)
F_KICK = font("DejaVuSans-Bold.ttf", 22)
F_HEAD = font("DejaVuSans-Bold.ttf", 34)
F_HEAD2 = font("DejaVuSans-Bold.ttf", 26)
F_BODY = font("DejaVuSans.ttf", 22)
F_CARD_H = font("DejaVuSans-Bold.ttf", 22)
F_CARD = font("DejaVuSans.ttf", 20)
F_TICK = font("DejaVuSans-Bold.ttf", 20)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def wrap(text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def para(text, fnt, x, y, max_w, fill=INK, leading=6):
    for line in wrap(text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + leading
    return y

def kicker(text, x, y, fill=RED):
    d.text((x, y), text, font=F_KICK, fill=fill)
    return y + 30

# ---- header ----
d.rectangle([0, 0, W, 112], fill=DARK)
d.text((36, 16), "THE WORLD IN ONE DAY", font=F_TITLE, fill=(247, 243, 234))
d.text((36, 76), "THURSDAY  26  NOVEMBER  2026", font=F_DATE, fill=(232, 180, 60))
d.rectangle([0, 112, W, 118], fill=RED)

# ---- lead: tariffs ----
y = 138
y = kicker("TARIFFS  —  ROUND TWO", 36, y)
y = para("Trump hits China, the EU and Japan with new tariffs",
         F_HEAD, 36, y, 952)
y = para("Washington cites factory overcapacity as the president doubles down, "
         "saying the levies are about power, not popularity — markets wobble "
         "as a second act of the tariff war opens.",
         F_BODY, 36, y + 4, 952)
d.line([36, 348, 988, 348], fill=GREY, width=2)

# ---- second row: two panels ----
y0 = 366
# left: Ukraine
d.rectangle([36, y0, 500, 560], outline=BLUE, width=3)
kicker("UKRAINE STRIKES BACK", 52, y0 + 14, fill=BLUE)
para("Kyiv says it hit a major Russian air base, damaging five planes, "
     "and two refineries in Samara. Poland asks NATO to shoot down "
     "Russian missiles over Ukraine.",
     F_BODY, 52, y0 + 52, 432)
# right: North Korea
d.rectangle([524, y0, 988, 560], outline=RED, width=3)
kicker("PYONGYANG", 540, y0 + 14, fill=RED)
para("Kim Jong Un calls for a wider deployment of tactical nuclear "
     "weapons and more production of nuclear material.",
     F_BODY, 540, y0 + 52, 432)

# ---- grid: six cards ----
cards = [
    ("EGYPT", "Fuel tanker fire on Cairo's ring road kills 30 and injures 15."),
    ("SPACE", "SpaceX wins US approval to launch data centers in orbit."),
    ("HONG KONG", "City remembers the 168 people killed in a housing-complex fire."),
    ("MUSIC", "Duran Duran guitarist Andy Taylor dies at 65."),
    ("SPACE", "Pakistan's first astronaut reaches orbit aboard China's Tiangong."),
    ("UNITED STATES", "A second judge blocks Trump's birthright-citizenship order."),
]
cw, ch, gx, gy = 304, 158, 24, 20
x0, y0 = 36, 584
for i, (tag, text) in enumerate(cards):
    cx = x0 + (i % 3) * (cw + gx)
    cy = y0 + (i // 3) * (ch + gy)
    d.rectangle([cx, cy, cx + cw, cy + ch], fill=CARD, outline=(200, 196, 186), width=2)
    d.text((cx + 14, cy + 12), tag, font=F_CARD_H, fill=RED)
    para(text, F_CARD, cx + 14, cy + 44, cw - 28)

# ---- ticker ----
d.rectangle([0, 928, W, H], fill=DARK)
para("SUDAN: RSF drone attacks kill at least 19 in Blue Nile  ·  "
     "US famine monitor halts reporting as funds run dry  ·  "
     "King tides batter the California coast on Thanksgiving  ·  "
     "Iran to execute two protesters at dawn",
     F_TICK, 36, 946, 952, fill=(247, 243, 234))

img.save("entry.png")
print("saved entry.png", img.size)
