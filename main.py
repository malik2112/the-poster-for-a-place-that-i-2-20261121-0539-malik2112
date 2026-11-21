#!/usr/bin/env python3
"""The Poster for a Place That Isn't There — VELMARIS.

Deterministic PIL travel poster (1024x1024 PNG) for an invented coastal
city: a spiral tower on a rocky island, terraced whitewashed houses,
a calm bay at dusk. The only text in the picture is the place name.
No network; fixed-seed pseudo-random detail only.
"""
import os
import random
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "/output/entry.png"
rng = random.Random(20261121)

# ---------- fonts ----------
FONT_DIRS = ["/usr/share/fonts/truetype/liberation", "/usr/share/fonts/truetype/dejavu"]

def font(names, size):
    for d in FONT_DIRS:
        for n in names:
            p = os.path.join(d, n)
            if os.path.exists(p):
                return ImageFont.truetype(p, size)
    return ImageFont.load_default()

SERIF_B = lambda s: font(["LiberationSerif-Bold.ttf", "DejaVuSerif-Bold.ttf"], s)

# ---------- palette ----------
PAPER   = (244, 236, 214)
INK     = (24, 34, 54)
NAVY    = (18, 38, 66)
TEAL_D  = (23, 84, 96)
TEAL    = (38, 128, 138)
TEAL_L  = (96, 176, 168)
CORAL   = (232, 118, 84)
GOLD    = (240, 192, 96)
CREAM   = (250, 244, 224)
ROOF    = (196, 84, 60)
ROCK    = (58, 64, 84)
ROCK_L  = (96, 104, 126)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# poster field (inside the paper margin)
X0, Y0, X1, Y1 = 36, 36, W - 36, H - 36
HOR = 620          # horizon line
BAND = 872         # top of the name band

# ---------- sky: flat dusk bands ----------
sky_stops = [
    (0.00, (26, 44, 86)),
    (0.30, (44, 92, 128)),
    (0.55, (92, 150, 152)),
    (0.75, (226, 150, 104)),
    (1.00, (246, 196, 118)),
]
def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))

def sky_color(t):
    for i in range(len(sky_stops) - 1):
        t0, c0 = sky_stops[i]
        t1, c1 = sky_stops[i + 1]
        if t0 <= t <= t1:
            return lerp(c0, c1, (t - t0) / (t1 - t0))
    return sky_stops[-1][1]

for y in range(Y0, HOR):
    t = (y - Y0) / (HOR - Y0)
    d.line([(X0, y), (X1, y)], fill=sky_color(t))

# ---------- stars in the upper sky ----------
for _ in range(90):
    x = rng.randint(X0 + 8, X1 - 8)
    y = rng.randint(Y0 + 8, Y0 + 240)
    r = rng.choice([1, 1, 2])
    d.ellipse([x - r, y - r, x + r, y + r], fill=(232, 238, 250))

# ---------- the twin moons of Velmaris (its signature sky) ----------
mx, my, mr = 822, 128, 34
d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(246, 240, 218))
sky_at_moon = sky_color((my - Y0) / (HOR - Y0))
d.ellipse([mx - mr + 18, my - mr - 4, mx + mr + 12, my + mr - 6], fill=sky_at_moon)
mx2, my2, mr2 = 884, 176, 18
d.ellipse([mx2 - mr2, my2 - mr2, mx2 + mr2, my2 + mr2], fill=(246, 240, 218))

# ---------- flat poster clouds (row of puffs on a flat base) ----------
def cloud(cx, cy, cw):
    base = cy + 14
    for dx, r in [(-0.32, 0.20), (-0.10, 0.28), (0.14, 0.24), (0.34, 0.17)]:
        px = cx + int(dx * cw)
        pr = int(r * cw)
        d.ellipse([px - pr, base - 2 * pr, px + pr, base], fill=(232, 220, 200))
    d.rectangle([cx - cw // 2, base - 6, cx + cw // 2, base], fill=(232, 220, 200))

cloud(210, 150, 170)
cloud(520, 108, 130)
cloud(330, 252, 105)

# ---------- birds ----------
for bx, by, bs in [(250, 320, 14), (300, 348, 11), (620, 300, 12)]:
    d.arc([bx - bs, by - bs // 2, bx, by + bs // 2], start=200, end=330, fill=INK, width=2)
    d.arc([bx, by - bs // 2, bx + bs, by + bs // 2], start=210, end=340, fill=INK, width=2)

# ---------- sun, low over the bay ----------
sx, sy, sr = 400, HOR - 88, 118
d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(252, 222, 150))
d.ellipse([sx - sr + 14, sy - sr + 14, sx + sr - 14, sy + sr - 14], fill=(250, 205, 118))

# ---------- distant mountains ----------
ridge = [(X0, HOR), (150, 520), (300, 566), (470, 512), (640, 560), (820, 516), (X1, 556), (X1, HOR)]
d.polygon(ridge, fill=(74, 92, 132))
ridge2 = [(X0, HOR), (220, 560), (420, 588), (700, 556), (X1, 584), (X1, HOR)]
d.polygon(ridge2, fill=(52, 74, 112))

# ---------- sea ----------
for y in range(HOR, BAND):
    t = (y - HOR) / (BAND - HOR)
    d.line([(X0, y), (X1, y)], fill=lerp(TEAL, TEAL_D, t))

# sun path on the water (broken, widening dashes)
for i in range(13):
    yy = HOR + 16 + i * 17
    half = 20 + i * 6
    jitter = rng.randint(-20, 20)
    seg = rng.randint(18, 30)
    d.line([(sx - half + jitter, yy), (sx - half + jitter + seg, yy)], fill=(246, 205, 130), width=3)
    d.line([(sx + half + jitter - seg, yy), (sx + half + jitter, yy)], fill=(246, 205, 130), width=3)
    if i % 2 == 0:
        d.line([(sx - 12 + jitter, yy), (sx + 12 + jitter, yy)], fill=(250, 220, 160), width=3)
# gentle wave dashes
for _ in range(60):
    x = rng.randint(X0 + 20, X1 - 60)
    y = rng.randint(HOR + 16, BAND - 20)
    d.line([(x, y), (x + rng.randint(14, 34), y)], fill=TEAL_L, width=2)

# sailboats
def boat(bx, by, s, sail):
    d.polygon([(bx - 26 * s, by), (bx + 26 * s, by), (bx + 16 * s, by + 10 * s), (bx - 16 * s, by + 10 * s)], fill=INK)
    d.line([(bx, by), (bx, by - 44 * s)], fill=INK, width=2)
    d.polygon([(bx + 2, by - 42 * s), (bx + 2, by - 4), (bx + 24 * s, by - 4)], fill=sail)
    d.polygon([(bx - 2, by - 36 * s), (bx - 2, by - 4), (bx - 18 * s, by - 4)], fill=sail)
    d.line([(bx - 20 * s, by + 16 * s), (bx + 20 * s, by + 16 * s)], fill=TEAL_L, width=2)

boat(470, 668, 0.62, CREAM)
boat(540, 780, 0.7, (244, 224, 178))
boat(880, 730, 0.85, CREAM)

# ---------- island + spiral tower (the Needle of Velmaris) ----------
ix, iy = 700, HOR + 46
d.polygon([(ix - 150, iy + 60), (ix - 90, iy - 26), (ix + 30, iy - 44), (ix + 130, iy - 10), (ix + 170, iy + 60)], fill=ROCK)
d.polygon([(ix - 90, iy - 26), (ix + 30, iy - 44), (ix + 70, iy + 6), (ix - 30, iy + 16)], fill=ROCK_L)
# tower body (tapered)
tx, tbase, ttop = ix + 6, iy - 30, iy - 330
d.polygon([(tx - 34, tbase), (tx + 34, tbase), (tx + 18, ttop), (tx - 18, ttop)], fill=CREAM)
# spiral stripe
for i in range(7):
    yy = tbase - 26 - i * 40
    wdt = 34 - i * 2
    d.line([(tx - wdt, yy), (tx + wdt, yy - 22)], fill=CORAL, width=9)
# lantern room
d.rectangle([tx - 24, ttop - 44, tx + 24, ttop], fill=INK)
d.rectangle([tx - 16, ttop - 36, tx + 16, ttop - 8], fill=GOLD)
d.polygon([(tx - 30, ttop - 44), (tx + 30, ttop - 44), (tx, ttop - 76)], fill=ROOF)
# flag (no text)
d.line([(tx, ttop - 76), (tx, ttop - 104)], fill=INK, width=3)
d.polygon([(tx, ttop - 104), (tx + 34, ttop - 96), (tx, ttop - 88)], fill=CORAL)
# lantern glow + light beam sweeping the bay
beam = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bd = ImageDraw.Draw(beam)
bd.polygon([(tx - 10, ttop - 24), (tx - 330, ttop + 130), (tx - 330, ttop + 196)], fill=(250, 220, 140, 52))
bd.ellipse([tx - 46, ttop - 70, tx + 46, ttop + 22], fill=(250, 220, 140, 70))
img.paste(Image.alpha_composite(img.convert("RGBA"), beam).convert("RGB"), (0, 0))
d = ImageDraw.Draw(img)
# lit windows on the tower
for wy in (tbase - 70, tbase - 150, tbase - 230):
    d.rectangle([tx - 5, wy - 8, tx + 5, wy + 8], fill=GOLD)

# ---------- terraced houses on the left cliff ----------
d.polygon([(X0, BAND), (X0, 640), (300, 690), (380, BAND)], fill=(44, 58, 84))
houses = [
    (70, 664, 54, 36), (140, 656, 48, 32), (204, 668, 58, 38), (276, 676, 46, 32),
    (86, 714, 50, 34), (152, 722, 56, 36), (224, 716, 48, 32), (288, 726, 52, 34),
    (100, 766, 54, 36), (170, 774, 48, 32), (234, 768, 56, 38),
    (118, 818, 50, 34), (184, 824, 54, 36),
]
for hx, hy, hw, hh in houses:
    d.rectangle([hx, hy, hx + hw, hy + hh], fill=CREAM)
    d.polygon([(hx - 4, hy), (hx + hw + 4, hy), (hx + hw // 2, hy - 16)], fill=ROOF)
    d.rectangle([hx + 9, hy + 10, hx + 17, hy + 21], fill=GOLD)
    d.rectangle([hx + hw - 17, hy + 10, hx + hw - 9, hy + 21], fill=GOLD)
    d.rectangle([hx + hw // 2 - 4, hy + hh - 14, hx + hw // 2 + 4, hy + hh], fill=INK)
# promenade lamps along the shore
for lx in (420, 500, 580):
    d.line([(lx, BAND - 6), (lx, BAND - 44)], fill=INK, width=3)
    d.ellipse([lx - 6, BAND - 56, lx + 6, BAND - 44], fill=GOLD)
    d.line([(lx - 14, BAND - 2), (lx + 14, BAND - 2)], fill=(246, 205, 130), width=2)

# ---------- name band: the only text ----------
d.rectangle([X0, BAND, X1, Y1], fill=NAVY)
d.line([(X0 + 40, BAND + 22), (X1 - 40, BAND + 22)], fill=GOLD, width=2)
name = "VELMARIS"
f = SERIF_B(72)
# letter-spaced, centred
spacing = 30
widths = [d.textlength(ch, font=f) for ch in name]
total = sum(widths) + spacing * (len(name) - 1)
x = (W - total) / 2
for ch, wch in zip(name, widths):
    d.text((x, BAND + 34), ch, font=f, fill=CREAM)
    x += wch + spacing

# ---------- print grain (deterministic) ----------
grain = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(grain)
for _ in range(2600):
    x = rng.randint(0, W - 1)
    y = rng.randint(0, H - 1)
    a = rng.randint(4, 13)
    gd.point((x, y), fill=(30, 26, 20, a) if rng.random() < 0.5 else (255, 250, 235, a))
img = Image.alpha_composite(img.convert("RGBA"), grain).convert("RGB")
d = ImageDraw.Draw(img)

# ---------- frame ----------
d.rectangle([X0, Y0, X1, Y1], outline=INK, width=3)
d.rectangle([18, 18, W - 18, H - 18], outline=INK, width=1)

os.makedirs("/output", exist_ok=True)
img.save(OUT, "PNG", optimize=True)
print(f"wrote {OUT}: {os.path.getsize(OUT)} bytes, {img.size}")
