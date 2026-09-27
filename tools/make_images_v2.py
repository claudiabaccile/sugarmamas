"""Generate the placeholder illustrations for v2/images (original SVG artwork, free to use).

Run: python3 tools/make_images_v2.py
"""
import math
import random
from pathlib import Path

from make_images import (CAKE_DEFS, FLOWERS, bokeh, candles, cluster, drip, leaf, lin, rose,
                         sprinkles, stand, svg, table, tier, wedding_cake)

OUT = Path(__file__).resolve().parent.parent / "v2" / "images"

ICING = ["#f7a8c4", "#fbd3e0", "#bfe6d9", "#fff6ec", "#f9d27a", "#c9b6f0"]


def cookie(rng, x, y, r, shape="round", icing=None, deco="dots", text=None):
    icing = icing or rng.choice(ICING)
    base = "#e2b27a"
    if shape == "heart":
        def heart(s):
            return (f"M{x:.1f} {y + s * 0.9:.1f} C{x - s * 1.6:.1f} {y - s * 0.1:.1f} {x - s * 0.9:.1f} {y - s * 1.3:.1f} {x:.1f} {y - s * 0.5:.1f} "
                    f"C{x + s * 0.9:.1f} {y - s * 1.3:.1f} {x + s * 1.6:.1f} {y - s * 0.1:.1f} {x:.1f} {y + s * 0.9:.1f} Z")
        out = f'<path d="{heart(r)}" fill="{base}"/><path d="{heart(r * 0.84)}" fill="{icing}"/>'
    elif shape == "plaque":
        out = (f'<rect x="{x - r * 1.3:.1f}" y="{y - r * 0.85:.1f}" width="{r * 2.6:.1f}" height="{r * 1.7:.1f}" rx="{r * 0.45:.1f}" fill="{base}"/>'
               f'<rect x="{x - r * 1.15:.1f}" y="{y - r * 0.7:.1f}" width="{r * 2.3:.1f}" height="{r * 1.4:.1f}" rx="{r * 0.35:.1f}" fill="{icing}"/>')
    elif shape == "flower":
        petals = "".join(f'<circle cx="{x + r * 0.55 * math.cos(a):.1f}" cy="{y + r * 0.55 * math.sin(a):.1f}" r="{r * 0.5:.1f}" fill="{base}"/>' for a in [i * math.pi / 3 for i in range(6)])
        petals2 = "".join(f'<circle cx="{x + r * 0.55 * math.cos(a):.1f}" cy="{y + r * 0.55 * math.sin(a):.1f}" r="{r * 0.4:.1f}" fill="{icing}"/>' for a in [i * math.pi / 3 for i in range(6)])
        out = petals + petals2 + f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r * 0.35:.1f}" fill="#f9d27a"/>'
    else:
        out = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{base}"/><circle cx="{x:.1f}" cy="{y:.1f}" r="{r * 0.84:.1f}" fill="{icing}"/>'
    if deco == "dots":
        for i in range(10):
            a = i * math.pi / 5
            out += f'<circle cx="{x + r * 0.62 * math.cos(a):.1f}" cy="{y + r * 0.62 * math.sin(a):.1f}" r="{r * 0.06:.1f}" fill="#fff"/>'
    elif deco == "rose":
        out += rose(x, y, r * 0.35, *FLOWERS[rng.choice(["pink", "blush", "peach"])])
        out += leaf(x + r * 0.4, y + r * 0.25, r * 0.2, 30)
    elif deco == "swirl":
        out += f'<path d="M{x - r * .4:.1f} {y:.1f} q{r * .2:.1f} {-r * .4:.1f} {r * .4:.1f} 0 t{r * .4:.1f} 0" fill="none" stroke="#fff" stroke-width="{r * .08:.1f}" stroke-linecap="round"/>'
    if text:
        out += (f'<text x="{x:.1f}" y="{y + r * 0.12:.1f}" text-anchor="middle" font-family="Brush Script MT, cursive" '
                f'font-size="{r * min(0.5, 3.4 / max(len(text), 1)):.1f}" fill="#b04a72">{text}</text>')
    return f'<g filter="url(#shadow)">{out}</g>'


def macaron(x, y, r, color, filling="#fff6ec"):
    return (f'<g filter="url(#shadow)"><ellipse cx="{x}" cy="{y + r * 0.35:.1f}" rx="{r:.1f}" ry="{r * 0.45:.1f}" fill="{color}"/>'
            f'<rect x="{x - r * 0.92:.1f}" y="{y - r * 0.05:.1f}" width="{r * 1.84:.1f}" height="{r * 0.28:.1f}" rx="{r * 0.1:.1f}" fill="{filling}"/>'
            f'<ellipse cx="{x}" cy="{y - r * 0.2:.1f}" rx="{r:.1f}" ry="{r * 0.5:.1f}" fill="{color}"/>'
            f'<ellipse cx="{x - r * 0.3:.1f}" cy="{y - r * 0.4:.1f}" rx="{r * 0.35:.1f}" ry="{r * 0.12:.1f}" fill="#fff" opacity=".35"/></g>')


def cupcake(rng, x, y, s, frost):
    part = [f'<path d="M{x - 80 * s:.0f} {y - 95 * s:.0f} L{x + 80 * s:.0f} {y - 95 * s:.0f} L{x + 60 * s:.0f} {y:.0f} L{x - 60 * s:.0f} {y:.0f} Z" fill="#f4a6c0"/>']
    for k in range(7):
        xx = x - 68 * s + k * 23 * s
        part.append(f'<line x1="{xx:.0f}" y1="{y - 95 * s:.0f}" x2="{xx + (x - xx) * 0.25:.0f}" y2="{y:.0f}" stroke="#e58aab" stroke-width="3"/>')
    for rw, dy in [(92, 108), (72, 148), (50, 180), (26, 204)]:
        part.append(f'<ellipse cx="{x:.0f}" cy="{y - dy * s:.0f}" rx="{rw * s:.0f}" ry="{30 * s:.0f}" fill="{frost}" stroke="#00000012" stroke-width="3"/>')
    part.append(sprinkles(rng, x - 70 * s, y - 215 * s, 140 * s, 100 * s, 16))
    part.append(f'<circle cx="{x:.0f}" cy="{y - 232 * s:.0f}" r="{14 * s:.0f}" fill="#d6304f"/>')
    return f'<g filter="url(#shadow)">{"".join(part)}</g>'


def scene(w, h, bg_stops, body, seed, bokeh_cols=("#ffffff", "#ffd9e6"), tbl=None):
    rng = random.Random(seed)
    parts = [f'<rect width="{w}" height="{h}" fill="url(#bg)"/>', bokeh(rng, w, h, 14, list(bokeh_cols), 20, 60, (0.3, 0.6))]
    if tbl:
        parts.append(table(w, h, *tbl))
    parts.append(body)
    return svg(w, h, "".join(parts), lin("bg", bg_stops) + CAKE_DEFS)


def cookie_spread(seed, w, h, n_cols, n_rows, r, texts=("Happy Birthday", "Congrats!", "Love")):
    rng = random.Random(seed)
    out = []
    shapes = ["round", "heart", "flower", "round", "plaque"]
    decos = ["dots", "rose", "swirl"]
    ti = 0
    for row in range(n_rows):
        for col in range(n_cols):
            x = (col + 0.5 + (row % 2) * 0.25) * w / n_cols + rng.uniform(-10, 10)
            y = (row + 0.55) * h / n_rows + rng.uniform(-10, 10)
            sh = rng.choice(shapes)
            text = None
            if sh == "plaque":
                text = texts[ti % len(texts)]
                ti += 1
            out.append(cookie(rng, x, y, r * rng.uniform(0.9, 1.05), sh, deco=None if text else rng.choice(decos), text=text))
    return "".join(out)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rng = random.Random(1)
    pinkbg = [(0, "#fff1f5"), (1, "#fbd1df")]
    creambg = [(0, "#fff8f1"), (1, "#f6e3d4")]
    mintbg = [(0, "#f2fbf8"), (1, "#cfeee3")]

    files = {}
    # hero: cake + cookies on the right side, pink backdrop
    body = wedding_cake(random.Random(2), 1080, 620, 1.0, ("pink", "blush", "white", "peach"), grad="cakeP")
    body += "".join(cookie(rng, x, y, r, sh, deco=d) for x, y, r, sh, d in [
        (760, 650, 60, "heart", "dots"), (880, 690, 55, "round", "rose"), (1330, 660, 62, "flower", None), (1440, 700, 55, "round", "swirl")])
    body += macaron(620, 690, 42, "#bfe6d9") + macaron(540, 700, 40, "#f7a8c4")
    files["hero.svg"] = scene(1600, 800, [(0, "#ffe3ec"), (1, "#f6b3c9")], body, 3, ("#ffffff", "#ffd0df"), (720, "#fff4f7", "#fff"))

    # categories
    files["cat-cakes.svg"] = scene(800, 800, pinkbg, wedding_cake(random.Random(4), 400, 650, 1.1, ("pink", "blush", "white")), 4, tbl=(700, "#fde8ef", "#fff"))
    files["cat-cookies.svg"] = scene(800, 800, creambg, cookie_spread(5, 800, 800, 3, 3, 95), 5)
    files["cat-cupcakes.svg"] = scene(800, 800, mintbg, cupcake(rng, 170, 620, 0.95, "#fff6ec") + cupcake(rng, 630, 620, 0.95, "#f7a8c4") + cupcake(rng, 400, 680, 1.1, "#fbd3e0"), 6, ("#ffffff", "#d9f3ea"))
    mac = "".join(macaron(160 + c * 160, 200 + r * 150, 62, ICING[(r * 4 + c) % len(ICING)]) for r in range(4) for c in range(4))
    files["cat-macarons.svg"] = scene(800, 800, pinkbg, mac, 7)

    # products
    def cake_card(seed, kind):
        r = random.Random(seed)
        if kind == "birthday":
            b = stand(400, 640, 420) + tier(400, 636, 420, 270, "cakeS", "#fffdf8") + sprinkles(r, 190, 370, 420, 260, 170) + candles(400, 372, 5, 46)
            return scene(800, 800, pinkbg, f'<g filter="url(#shadow)">{b}</g>', seed, tbl=(690, "#fde8ef", "#fff"))
        if kind == "drip":
            b = stand(400, 650, 400) + tier(400, 646, 360, 320, "cakeP", "#fbe3e4") + drip(400, 326, 360, "#f28cb1", r, 0.35, 320)
            b += "".join(macaron(300 + i * 50, 300, 22, ICING[i % 6]) for i in range(5))
            return scene(800, 800, mintbg, f'<g filter="url(#shadow)">{b}</g>', seed, ("#ffffff", "#d9f3ea"), (700, "#e8f7f1", "#fff"))
        if kind == "floral":
            return scene(800, 800, creambg, wedding_cake(r, 400, 650, 1.1, ("peach", "coral", "cream")), seed, tbl=(700, "#f6ebe2", "#fff"))
        if kind == "wedding":
            return scene(900, 1100, creambg, wedding_cake(r, 450, 950, 1.5, ("white", "cream", "blush")), seed, tbl=(1000, "#f6ebe2", "#fff"))
    files["p-birthday.svg"] = cake_card(8, "birthday")
    files["p-drip.svg"] = cake_card(9, "drip")
    files["p-floral.svg"] = cake_card(10, "floral")
    files["wedding.svg"] = cake_card(11, "wedding")
    files["p-cookie-box.svg"] = scene(800, 800, creambg,
        '<rect x="90" y="120" width="620" height="560" rx="18" fill="#fff" filter="url(#shadow)"/><rect x="110" y="140" width="580" height="520" rx="12" fill="#fde8ef"/>'
        + cookie_spread(12, 580, 520, 3, 3, 72).replace('<g filter="url(#shadow)">', '<g filter="url(#shadow)" transform="translate(110 140)">'), 12)
    files["p-cupcakes.svg"] = scene(800, 800, pinkbg, "".join(cupcake(rng, x, y, 0.8, f) for x, y, f in [(200, 420, "#fff6ec"), (400, 420, "#bfe6d9"), (600, 420, "#fbd3e0"), (300, 680, "#f9d27a"), (500, 680, "#fff6ec")]), 13)
    files["p-macarons.svg"] = scene(800, 800, mintbg,
        '<rect x="80" y="260" width="640" height="300" rx="20" fill="#fff" filter="url(#shadow)"/>'
        + "".join(macaron(150 + i * 83, 410, 44, ICING[i % 6]) for i in range(7)), 14, ("#ffffff", "#d9f3ea"))
    files["cookies-feature.svg"] = scene(1200, 900, [(0, "#fff6ef"), (1, "#f9dbe5")], cookie_spread(15, 1200, 900, 4, 3, 105, ("Happy Birthday", "Oh Baby!", "Thank You", "XO")), 15)
    files["consult.svg"] = scene(1200, 900, creambg,
        "".join(f'<g filter="url(#shadow)"><ellipse cx="{x}" cy="{y}" rx="120" ry="38" fill="#fff"/><ellipse cx="{x}" cy="{y - 6}" rx="100" ry="28" fill="#f3ece6"/>'
                f'<path d="M{x - 70} {y - 10} l70 -80 l70 80 z" fill="{c}"/><path d="M{x - 70} {y - 10} l70 -80 l70 80 z" fill="none" stroke="#fff" stroke-width="3"/>'
                f'<rect x="{x - 70}" y="{y - 40}" width="140" height="12" fill="#fff" opacity=".9"/></g>'
                for x, y, c in [(300, 380, "#f6d8b8"), (600, 330, "#6d3f2a"), (900, 380, "#fbd3e0"), (450, 640, "#fff4d6"), (750, 640, "#e8475f")]), 16)
    for name, content in files.items():
        (OUT / name).write_text(content)
    print(f"wrote {len(files)} files to {OUT}")


if __name__ == "__main__":
    main()
