#!/usr/bin/env python3
"""Generate the profile banner PNG. Dark GitHub theme, brand-neutral, editable.
Re-run after changing NAME/TAGLINE to regenerate."""
from PIL import Image, ImageDraw, ImageFont
import math

NAME = "MICHAEL"
TAGLINE = "Privileged Access & Cloud Security Engineer"
DOMAINS = ["CyberArk / Idira", "Linux", "AWS", "Azure"]

W, H = 1280, 360
BG = (13, 17, 23)          # #0d1117
PANEL = (22, 27, 34)       # #161b22
INK = (230, 237, 243)      # #e6edf3
MUTED = (139, 148, 158)    # #8b949e
ACCENT = (88, 166, 255)    # #58a6ff
GREEN = (63, 185, 80)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# subtle grid of dots
for x in range(0, W, 32):
    for y in range(0, H, 32):
        d.point((x, y), fill=(28, 34, 42))

# accent bar on the left
d.rectangle([0, 0, 8, H], fill=ACCENT)

def font(sz, bold=True):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in paths:
        try:
            return ImageFont.truetype(p, sz)
        except OSError:
            continue
    return ImageFont.load_default()

# Name
d.text((56, 70), NAME, font=font(88, True), fill=INK)
# Tagline
d.text((60, 178), TAGLINE, font=font(30, False), fill=ACCENT)

# Domain chips
x = 60
y = 250
f = font(22, True)
for dom in DOMAINS:
    tw = d.textbbox((0, 0), dom, font=f)[2]
    pad = 18
    d.rounded_rectangle([x, y, x + tw + pad * 2, y + 44], radius=8,
                        fill=PANEL, outline=(48, 54, 61), width=1)
    d.text((x + pad, y + 9), dom, font=f, fill=MUTED)
    x += tw + pad * 2 + 14

# little "labs" mark, top right
mark = "11 hands-on labs"
fm = font(20, True)
tw = d.textbbox((0, 0), mark, font=fm)[2]
d.text((W - tw - 56, 80), mark, font=fm, fill=GREEN)

img.save("assets/banner.png")
print("wrote assets/banner.png", img.size)
