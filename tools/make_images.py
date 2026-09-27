"""Generate the placeholder illustrations in images/ (original SVG artwork, free to use).

Run: python3 tools/make_images.py
"""
import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "images"


def svg(w, h, body, defs=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'preserveAspectRatio="xMidYMid slice">'
        f'<defs><filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14"/></filter>'
        f'<filter id="soft"><feGaussianBlur stdDeviation="3"/></filter>'
        f'<filter id="shadow" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#3a2219" flood-opacity=".28"/></filter>'
        f"{defs}</defs>{body}</svg>"
    )


def lin(id_, stops, x2=0, y2=1):
    s = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return f'<linearGradient id="{id_}" x1="0" y1="0" x2="{x2}" y2="{y2}">{s}</linearGradient>'


def shade(id_, c, dark):
    # horizontal shading for cylinders
    return lin(id_, [(0, dark), (0.35, c), (0.6, c), (1, dark)], x2=1, y2=0)


def bokeh(rng, w, h, n, colors, rmin=20, rmax=70, op=(0.15, 0.5)):
    out = []
    for _ in range(n):
        out.append(
            f'<circle cx="{rng.uniform(0, w):.0f}" cy="{rng.uniform(0, h):.0f}" r="{rng.uniform(rmin, rmax):.0f}" '
            f'fill="{rng.choice(colors)}" opacity="{rng.uniform(*op):.2f}"/>'
        )
    return f'<g filter="url(#blur)">{"".join(out)}</g>'


def leaf(x, y, size, angle, color="#6f8a5e"):
    return (
        f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{size:.1f}" ry="{size * 0.42:.1f}" fill="{color}" '
        f'transform="rotate({angle:.0f} {x:.1f} {y:.1f})"/>'
        f'<line x1="{x - size * 0.9 * math.cos(math.radians(angle)):.1f}" y1="{y - size * 0.9 * math.sin(math.radians(angle)):.1f}" '
        f'x2="{x + size * 0.9 * math.cos(math.radians(angle)):.1f}" y2="{y + size * 0.9 * math.sin(math.radians(angle)):.1f}" '
        f'stroke="#4f6843" stroke-width="{max(size * 0.05, 0.8):.1f}" opacity=".6"/>'
    )


def rose(x, y, r, base, dark, light):
    parts = [f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{base}"/>']
    # outer petals
    for i in range(7):
        a = i * 360 / 7
        px = x + r * 0.55 * math.cos(math.radians(a))
        py = y + r * 0.55 * math.sin(math.radians(a))
        parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r * 0.5:.1f}" fill="{base}" stroke="{dark}" stroke-width="{r * 0.04:.1f}" opacity=".95"/>')
    # spiral centre
    for k, (rr, col) in enumerate([(0.62, light), (0.45, base), (0.3, light), (0.16, dark)]):
        parts.append(f'<circle cx="{x + r * 0.05 * k:.1f}" cy="{y - r * 0.04 * k:.1f}" r="{r * rr:.1f}" fill="{col}" stroke="{dark}" stroke-width="{r * 0.035:.1f}" stroke-opacity=".6"/>')
    parts.append(f'<path d="M{x - r * .25:.1f} {y:.1f} q{r * .25:.1f} {-r * .35:.1f} {r * .5:.1f} 0" fill="none" stroke="{dark}" stroke-width="{r * 0.05:.1f}" opacity=".7"/>')
    return "".join(parts)


FLOWERS = {
    "blush": ("#f3c1c4", "#c9787f", "#fbe1e1"),
    "peach": ("#f5b99a", "#cf7a55", "#fbdcc8"),
    "coral": ("#ec8d73", "#b8543d", "#f7b8a4"),
    "cream": ("#f8ecdc", "#cdb38f", "#fffaf2"),
    "pink": ("#ea8fa5", "#b2506a", "#f7c3cf"),
    "white": ("#fbf8f3", "#d8cabb", "#ffffff"),
}


def cluster(rng, x, y, spread, n, palette, rmin, rmax):
    items = []
    for _ in range(n):
        items.append((x + rng.uniform(-spread, spread), y + rng.uniform(-spread * 0.45, spread * 0.45), rng.uniform(rmin, rmax), rng.choice(palette)))
    out = []
    for fx, fy, fr, _ in items:
        for _ in range(2):
            out.append(leaf(fx + rng.uniform(-fr, fr), fy + rng.uniform(-fr * 0.6, fr * 0.6), fr * 0.9, rng.uniform(0, 360)))
    for fx, fy, fr, name in sorted(items, key=lambda t: t[1]):
        out.append(rose(fx, fy, fr, *FLOWERS[name]))
    return "".join(out)


def stand(cx, y, w, color="#efe9e4", dark="#b9aea6"):
    return (
        f'<rect x="{cx - w * 0.07:.0f}" y="{y:.0f}" width="{w * 0.14:.0f}" height="{w * 0.28:.0f}" fill="{dark}"/>'
        f'<ellipse cx="{cx:.0f}" cy="{y + w * 0.28:.0f}" rx="{w * 0.28:.0f}" ry="{w * 0.05:.0f}" fill="{dark}"/>'
        f'<ellipse cx="{cx:.0f}" cy="{y:.0f}" rx="{w * 0.6:.0f}" ry="{w * 0.07:.0f}" fill="{color}"/>'
        f'<ellipse cx="{cx:.0f}" cy="{y + w * 0.02:.0f}" rx="{w * 0.6:.0f}" ry="{w * 0.06:.0f}" fill="none" stroke="{dark}" stroke-width="2"/>'
    )


def tier(cx, bottom, w, h, grad, top):
    x = cx - w / 2
    ry = w * 0.09
    return (
        f'<rect x="{x:.1f}" y="{bottom - h:.1f}" width="{w:.1f}" height="{h:.1f}" fill="url(#{grad})"/>'
        f'<ellipse cx="{cx:.1f}" cy="{bottom:.1f}" rx="{w / 2:.1f}" ry="{ry:.1f}" fill="url(#{grad})"/>'
        f'<ellipse cx="{cx:.1f}" cy="{bottom - h:.1f}" rx="{w / 2:.1f}" ry="{ry:.1f}" fill="{top}"/>'
    )


def drip(cx, top, w, color, rng, length=0.35, h=100):
    x0 = cx - w / 2
    ry = w * 0.09
    d = f"M{x0:.1f} {top:.1f} "
    steps = 12
    for i in range(steps + 1):
        x = x0 + w * i / steps
        y = top + ry * math.sin(math.pi * i / steps) + rng.uniform(4, h * length)
        d += f"L{x:.1f} {y:.1f} "
    d += f"L{x0 + w:.1f} {top:.1f} Z"
    return f'<path d="{d}" fill="{color}" stroke="{color}" stroke-width="{w * 0.03:.1f}" stroke-linejoin="round"/><ellipse cx="{cx:.1f}" cy="{top:.1f}" rx="{w / 2:.1f}" ry="{ry:.1f}" fill="{color}"/>'


def sprinkles(rng, x, y, w, h, n, colors=("#f06a8a", "#5bb7e5", "#f7c948", "#7fd18b", "#b58be0", "#ff9a5c")):
    out = []
    for _ in range(n):
        px, py = rng.uniform(x, x + w), rng.uniform(y, y + h)
        out.append(f'<rect x="{px:.1f}" y="{py:.1f}" width="{w * 0.028:.1f}" height="{w * 0.008:.1f}" rx="{w * 0.004:.1f}" fill="{rng.choice(colors)}" transform="rotate({rng.uniform(0, 180):.0f} {px:.1f} {py:.1f})"/>')
    return "".join(out)


def candles(cx, top, n, spacing, colors=("#f4a6b8", "#8fd0e8", "#f7d06a", "#b9e2a0")):
    out = []
    for i in range(n):
        x = cx + (i - (n - 1) / 2) * spacing
        c = colors[i % len(colors)]
        out.append(
            f'<rect x="{x - 4:.1f}" y="{top - 70:.1f}" width="8" height="70" rx="3" fill="{c}"/>'
            f'<ellipse cx="{x:.1f}" cy="{top - 84:.1f}" rx="10" ry="16" fill="#ffd27a" opacity=".45" filter="url(#soft)"/>'
            f'<path d="M{x:.1f} {top - 96:.1f} q7 12 0 20 q-7 -8 0 -20z" fill="#ffb347"/>'
        )
    return "".join(out)


def table(w, h, y, color, edge):
    return f'<rect x="0" y="{y}" width="{w}" height="{h - y}" fill="{color}"/><rect x="0" y="{y}" width="{w}" height="6" fill="{edge}" opacity=".6"/>'


# ---------- scenes ----------

def wedding_cake(rng, cx, base, scale, flowers=("peach", "coral", "blush", "cream"), grad="cakeW", drip_color=None):
    s = scale
    out = [stand(cx, base, 300 * s)]
    tiers = [(300 * s, 150 * s), (220 * s, 130 * s), (150 * s, 110 * s)]
    y = base - 4 * s
    tops = []
    for w, h in tiers:
        out.append(tier(cx, y, w, h, grad, "#fffaf4"))
        if drip_color:
            out.append(drip(cx, y - h, w, drip_color, rng, 0.35, h))
        tops.append((y - h, w))
        y -= h
    # cascading flowers
    out.append(cluster(rng, cx + 70 * s, tops[2][0] - 10 * s, 60 * s, 7, flowers, 16 * s, 30 * s))
    out.append(cluster(rng, cx + 95 * s, tops[1][0] + 30 * s, 45 * s, 5, flowers, 14 * s, 26 * s))
    out.append(cluster(rng, cx - 110 * s, tops[0][0] + 60 * s, 45 * s, 5, flowers, 14 * s, 24 * s))
    out.append(cluster(rng, cx + 20 * s, base - 30 * s, 110 * s, 6, flowers, 12 * s, 22 * s))
    return f'<g filter="url(#shadow)">{"".join(out)}</g>'


CAKE_DEFS = (
    shade("cakeW", "#fdf7ef", "#e2d3c3")
    + shade("cakeP", "#fbe3e4", "#e5b9bd")
    + shade("cakeB", "#d5eef7", "#9ccbdd")
    + shade("cakeC", "#6d3f2a", "#3d2014")
    + shade("cakeS", "#fffaf2", "#e6d6c4")
)


def hero():
    rng = random.Random(1)
    w, h = 1600, 700
    bg = lin("bgH", [(0, "#2b1c15"), (0.55, "#5a3c2b"), (1, "#8a6450")], x2=1, y2=0.3)
    body = [f'<rect width="{w}" height="{h}" fill="url(#bgH)"/>']
    body.append(bokeh(rng, w, h, 40, ["#f6c89b", "#ffe2b8", "#f0a988", "#fff1d6"], 15, 60, (0.2, 0.55)))
    body.append(cluster(rng, 330, 650, 260, 9, ["pink", "blush", "peach"], 22, 40))
    body.append(table(w, h, 640, "#eadfd6", "#fff"))
    body.append(wedding_cake(rng, 1150, 600, 0.95))
    body.append(cluster(rng, 1480, 660, 120, 6, ["blush", "peach", "cream"], 20, 34))
    return svg(w, h, "".join(body), bg + CAKE_DEFS)


def card_scene(kind, seed):
    rng = random.Random(seed)
    w = h = 800
    if kind == "classic":
        bg = lin("bg", [(0, "#f2ebe5"), (1, "#d9c9bc")])
        scene = wedding_cake(rng, 400, 640, 1.2, ("cream", "blush", "peach"))
        extra = bokeh(rng, w, h, 18, ["#ffffff", "#f5e3d6"], 20, 60, (0.3, 0.6))
        tbl = table(w, h, 690, "#e8ddd3", "#fff")
    elif kind == "birthday":
        bg = lin("bg", [(0, "#fbf4ee"), (1, "#f0dcd0")])
        extra = bokeh(rng, w, h, 18, ["#ffffff", "#fde1cf"], 20, 60, (0.3, 0.6))
        tbl = table(w, h, 690, "#f4e8de", "#fff")
        parts = [stand(400, 640, 420), tier(400, 636, 420, 270, "cakeS", "#fffdf8")]
        parts.append(sprinkles(rng, 190, 370, 420, 260, 170))
        parts.append(sprinkles(rng, 230, 345, 340, 40, 50))
        parts.append(candles(400, 372, 6, 42))
        scene = f'<g filter="url(#shadow)">{"".join(parts)}</g>'
    elif kind == "floral":
        bg = lin("bg", [(0, "#f6ece8"), (1, "#e6cdc6")])
        extra = bokeh(rng, w, h, 18, ["#ffffff", "#f8d7da"], 20, 60, (0.3, 0.6))
        tbl = table(w, h, 690, "#efe2dc", "#fff")
        scene = wedding_cake(rng, 400, 640, 1.2, ("pink", "blush", "white"), grad="cakeP")
    else:  # statement
        bg = lin("bg", [(0, "#3a241a"), (1, "#1f130d")])
        extra = bokeh(rng, w, h, 22, ["#f3b77a", "#ffdca8"], 15, 45, (0.25, 0.6))
        tbl = table(w, h, 690, "#4a3024", "#6b4636")
        parts = [stand(400, 640, 400, "#d9cfc6", "#8e7f74"), tier(400, 636, 380, 300, "cakeC", "#7a4a33")]
        parts.append(drip(400, 336, 380, "#3b1f12", rng, 0.4, 300))
        for i in range(9):
            x = 400 + (i - 4) * 38 + rng.uniform(-6, 6)
            col = rng.choice(["#c0392b", "#e8b04a", "#f2d7c4", "#7b3b2a"])
            parts.append(f'<circle cx="{x:.0f}" cy="{322 + rng.uniform(-14, 6):.0f}" r="{rng.uniform(18, 26):.0f}" fill="{col}" stroke="#00000022" stroke-width="3"/>')
        for i in range(10):
            x = 230 + i * 38
            parts.append(f'<circle cx="{x:.0f}" cy="{640 + rng.uniform(-8, 4):.0f}" r="{rng.uniform(12, 18):.0f}" fill="#d98a3a" stroke="#8a4f1c" stroke-width="2"/>')
        scene = f'<g filter="url(#shadow)">{"".join(parts)}</g>'
    return svg(w, h, f'<rect width="{w}" height="{h}" fill="url(#bg)"/>' + extra + tbl + scene, bg + CAKE_DEFS)


def cupcakes(seed, cookies=False):
    rng = random.Random(seed)
    w, h = 1000, 800
    bg = lin("bg", [(0, "#faf1ea"), (1, "#ead6c8")])
    body = [f'<rect width="{w}" height="{h}" fill="url(#bg)"/>', bokeh(rng, w, h, 16, ["#ffffff", "#fde4d3"], 20, 60, (0.3, 0.6)), table(w, h, 560, "#f0e3d8", "#fff")]
    if cookies:
        for row in range(3):
            for col in range(5):
                x = 130 + col * 185 + (row % 2) * 90 + rng.uniform(-10, 10)
                y = 230 + row * 200 + rng.uniform(-10, 10)
                body.append(f'<g filter="url(#shadow)"><circle cx="{x:.0f}" cy="{y:.0f}" r="88" fill="#e3b77e"/><circle cx="{x:.0f}" cy="{y:.0f}" r="74" fill="{rng.choice(["#fdf7f2", "#f7cfd6", "#fbe3c9"])}"/>')
                for _ in range(5):
                    a = rng.uniform(0, 6.28)
                    body.append(f'<circle cx="{x + 42 * math.cos(a):.0f}" cy="{y + 42 * math.sin(a):.0f}" r="15" fill="{rng.choice(["#ef9fb2", "#f5c16c", "#ffffff"])}"/>')
                body.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="14" fill="#f2b84b"/></g>')
    else:
        for i, (x, y, s) in enumerate([(210, 560, 1), (500, 540, 1.1), (790, 560, 1), (350, 720, 1.05), (650, 720, 1.05)]):
            frost = rng.choice(["#fff8f0", "#fbe2e4", "#fde9d4"])
            part = [f'<path d="M{x - 95 * s:.0f} {y - 110 * s:.0f} L{x + 95 * s:.0f} {y - 110 * s:.0f} L{x + 70 * s:.0f} {y:.0f} L{x - 70 * s:.0f} {y:.0f} Z" fill="#c9905e"/>']
            for k in range(8):
                xx = x - 80 * s + k * 23 * s
                part.append(f'<line x1="{xx:.0f}" y1="{y - 110 * s:.0f}" x2="{xx + (x - xx) * 0.25:.0f}" y2="{y:.0f}" stroke="#a8713f" stroke-width="3"/>')
            for layer, (rw, dy) in enumerate([(110, 125), (88, 170), (62, 208), (34, 238)]):
                part.append(f'<ellipse cx="{x:.0f}" cy="{y - dy * s:.0f}" rx="{rw * s:.0f}" ry="{36 * s:.0f}" fill="{frost}" stroke="#e5d3c2" stroke-width="3"/>')
            part.append(sprinkles(rng, x - 80 * s, y - 250 * s, 160 * s, 120 * s, 20))
            body.append(f'<g filter="url(#shadow)">{"".join(part)}</g>')
    return svg(w, h, "".join(body), bg)


def baby_cake(seed):
    rng = random.Random(seed)
    w, h = 1000, 800
    bg = lin("bg", [(0, "#fbf6f1"), (1, "#eadfd5")])
    parts = [stand(500, 640, 440), tier(500, 636, 440, 300, "cakeB", "#e8f6fb")]
    for i in range(14):
        x = 300 + i * 30
        parts.append(f'<circle cx="{x:.0f}" cy="{600 + rng.uniform(-6, 6):.0f}" r="14" fill="#fff" opacity=".9"/>')
    for _ in range(12):
        parts.append(rose(rng.uniform(310, 690), rng.uniform(380, 590), rng.uniform(9, 14), *FLOWERS[rng.choice(["white", "pink", "cream"])]))
    parts.append(cluster(rng, 560, 330, 60, 4, ["white", "blush"], 18, 26))
    body = [f'<rect width="{w}" height="{h}" fill="url(#bg)"/>', bokeh(rng, w, h, 16, ["#ffffff", "#dff1f8"], 20, 60, (0.3, 0.6)), table(w, h, 690, "#efe6de", "#fff"), f'<g filter="url(#shadow)">{"".join(parts)}</g>']
    return svg(w, h, "".join(body), bg + CAKE_DEFS)


def gold_cake(seed):
    rng = random.Random(seed)
    w, h = 1000, 800
    bg = lin("bg", [(0, "#f8f1ea"), (1, "#e3d2c4")])
    parts = [stand(500, 650, 400), tier(500, 646, 360, 330, "cakeS", "#fffaf3"), drip(500, 316, 360, "#d7a94f", rng, 0.35, 330)]
    for i in range(6):
        x = 400 + i * 40
        parts.append(f'<circle cx="{x:.0f}" cy="{300 + rng.uniform(-10, 6):.0f}" r="22" fill="{rng.choice(["#f4c7cf", "#e8b04a", "#fbe6d0", "#6b3a26"])}" stroke="#00000018" stroke-width="3"/>')
    body = [f'<rect width="{w}" height="{h}" fill="url(#bg)"/>', bokeh(rng, w, h, 16, ["#ffffff", "#f7dcb4"], 20, 60, (0.3, 0.6)), table(w, h, 700, "#efe4da", "#fff"), f'<g filter="url(#shadow)">{"".join(parts)}</g>']
    return svg(w, h, "".join(body), bg + CAKE_DEFS)


def tall_portfolio():
    rng = random.Random(21)
    w, h = 900, 1000
    bg = lin("bg", [(0, "#f7ede8"), (1, "#e6d0c8")])
    body = [f'<rect width="{w}" height="{h}" fill="url(#bg)"/>', bokeh(rng, w, h, 20, ["#ffffff", "#f8d5da"], 20, 70, (0.3, 0.6)), table(w, h, 880, "#efe3dd", "#fff")]
    body.append(wedding_cake(rng, 450, 830, 1.1, ("pink", "blush", "white", "cream"), drip_color="#fbf3ec"))
    return svg(w, h, "".join(body), bg + CAKE_DEFS)


def sprinkle_portfolio():
    rng = random.Random(33)
    w, h = 1000, 800
    bg = lin("bg", [(0, "#fbe9ea"), (1, "#f0c9ce")])
    parts = [stand(500, 650, 420), tier(500, 646, 400, 320, "cakeS", "#fffdf8"), sprinkles(rng, 300, 330, 400, 320, 200), sprinkles(rng, 330, 300, 340, 40, 60), candles(500, 330, 1, 0)]
    body = [f'<rect width="{w}" height="{h}" fill="url(#bg)"/>', bokeh(rng, w, h, 16, ["#ffffff", "#fcd4dc"], 20, 60, (0.3, 0.6)), table(w, h, 700, "#f6e2e2", "#fff"), f'<g filter="url(#shadow)">{"".join(parts)}</g>']
    return svg(w, h, "".join(body), bg + CAKE_DEFS)


def dark_band(name, seed, cake_x, colors, warm=("#f6c89b", "#ffe2b8", "#f0a988")):
    rng = random.Random(seed)
    w, h = 1600, 460
    bg = lin("bgD", colors, x2=1, y2=0.2)
    body = [f'<rect width="{w}" height="{h}" fill="url(#bgD)"/>', bokeh(rng, w, h, 34, list(warm), 15, 60, (0.2, 0.5))]
    body.append(table(w, h, 420, "#3d2a21", "#6d5041"))
    body.append(wedding_cake(rng, cake_x, 400, 0.68, ("white", "cream", "blush")))
    body.append(cluster(rng, cake_x + 200, 440, 110, 6, ["cream", "blush", "peach"], 18, 30))
    if name == "reputation":
        # gold topper script
        body.append(f'<text x="{cake_x + 20}" y="70" font-family="Brush Script MT, cursive" font-size="70" fill="#d9ad5b" text-anchor="middle" transform="rotate(-8 {cake_x} 70)">Mama\'s</text>')
        body.append(f'<line x1="{cake_x - 20}" y1="85" x2="{cake_x - 15}" y2="140" stroke="#d9ad5b" stroke-width="3"/><line x1="{cake_x + 45}" y1="78" x2="{cake_x + 40}" y2="140" stroke="#d9ad5b" stroke-width="4"/>')
    return svg(w, h, "".join(body), bg + CAKE_DEFS)


def floral_band(seed, colors):
    rng = random.Random(seed)
    w, h = 1600, 600
    bg = lin("bgF", colors, x2=1, y2=0.2)
    body = [f'<rect width="{w}" height="{h}" fill="url(#bgF)"/>', bokeh(rng, w, h, 30, ["#f9d7cf", "#ffe9df", "#e8a99a"], 20, 70, (0.25, 0.55))]
    body.append(f'<g filter="url(#soft)">{cluster(rng, 1350, 380, 280, 16, ["blush", "pink", "peach", "cream"], 28, 50)}</g>')
    body.append(cluster(rng, 150, 520, 200, 8, ["blush", "peach", "cream"], 22, 38))
    return svg(w, h, "".join(body), bg)


def main():
    OUT.mkdir(exist_ok=True)
    files = {
        "hero.svg": hero(),
        "cake-classic-wedding.svg": card_scene("classic", 2),
        "cake-birthday.svg": card_scene("birthday", 3),
        "cake-floral.svg": card_scene("floral", 4),
        "cake-statement.svg": card_scene("statement", 5),
        "reputation.svg": dark_band("reputation", 6, 1150, [(0, "#1d130e"), (0.6, "#3b281d"), (1, "#6b4c3a")]),
        "portfolio-1.svg": tall_portfolio(),
        "portfolio-2.svg": cupcakes(7),
        "portfolio-3.svg": baby_cake(8),
        "portfolio-4.svg": gold_cake(9),
        "portfolio-5.svg": cupcakes(10, cookies=True),
        "portfolio-6.svg": sprinkle_portfolio(),
        "testimonials.svg": floral_band(11, [(0, "#3a261c"), (0.5, "#7b5a48"), (1, "#d9b1a4")]),
        "cta.svg": floral_band(12, [(0, "#4b3228"), (0.5, "#8d6a59"), (1, "#e6c1b5")]),
    }
    for name, content in files.items():
        (OUT / name).write_text(content)
    print(f"wrote {len(files)} files to {OUT}")


if __name__ == "__main__":
    main()
