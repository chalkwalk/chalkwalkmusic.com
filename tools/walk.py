#!/usr/bin/env python3
"""Generate the chalk "walk" line: the Euclidean rhythm E(5,16) as an SVG, and
write it into site/index.html between the <!--walk:wide--> and <!--walk:narrow-->
markers. Two drawings of the same 16 steps: a wide one for desktop and a
compressed one for phones (same stroke and dot sizes in SVG units, so they stay
legible when scaled down to a phone's width).

    python3 tools/walk.py        # rewrites site/index.html in place
"""
import math
import pathlib
import random
import re

HITS, STEPS = 5, 16
PATTERN = [1 if (i * HITS) % STEPS < HITS else 0 for i in range(STEPS)]


def walk(width, name, seed=5):
    rnd = random.Random(seed)
    y0, n = 44, 80
    pts = []
    for i in range(n + 1):
        x = 8 + i * (width - 16) / n
        pts.append((x, y0 + 2.6 * math.sin(i / 9.0) + rnd.uniform(-0.9, 0.9)))
    d = "M%.1f %.1f" % pts[0]
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        d += " Q%.1f %.1f %.1f %.1f" % (xa, ya, (xa + xb) / 2, (ya + yb) / 2)
    d += " L%.1f %.1f" % pts[-1]
    seg = (width - 16) / n

    def y_at(x):
        i = min(int((x - 8) / seg), n - 1)
        (xa, ya), (xb, yb) = pts[i], pts[i + 1]
        return ya + (yb - ya) * (x - xa) / (xb - xa)

    step = (width - 16) / STEPS
    marks = []
    for i, hit in enumerate(PATTERN):
        x = 8 + step * (i + 0.5)
        y = y_at(x)
        delay = 0.15 + 1.45 * (x / width)
        if hit:
            r = 15 + rnd.uniform(-0.8, 0.8)
            marks.append(f'<circle class="hit" style="animation-delay:{delay:.2f}s" '
                         f'cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}"/>')
        else:
            a = rnd.uniform(-0.1, 0.1)
            marks.append(f'<line class="tick" style="animation-delay:{delay:.2f}s" '
                         f'x1="{x + a * 12:.1f}" y1="{y - 12:.1f}" '
                         f'x2="{x - a * 12:.1f}" y2="{y + 12:.1f}"/>')
    fid = f"chalk-{name}"
    body = "\n        ".join(marks)
    return f'''<svg class="walk walk-{name}" viewBox="0 0 {width} 88" width="{width}" height="88" aria-hidden="true" focusable="false">
      <defs>
        <filter id="{fid}" x="-2%" y="-40%" width="104%" height="180%">
          <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="7" result="noise"/>
          <feDisplacementMap in="SourceGraphic" in2="noise" scale="4" result="rough"/>
          <feColorMatrix in="noise" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -2.6 2.05" result="grain"/>
          <feComposite in="rough" in2="grain" operator="in"/>
        </filter>
      </defs>
      <g filter="url(#{fid})">
        <path class="line" pathLength="1" d="{d}"/>
        {body}
      </g>
    </svg>'''


def main():
    page = pathlib.Path(__file__).resolve().parent.parent / "site" / "index.html"
    s = page.read_text()
    for name, width in (("wide", 1600), ("narrow", 760)):
        pat = re.compile(rf"(<!--walk:{name}-->).*?(<!--/walk:{name}-->)", re.S)
        if not pat.search(s):
            raise SystemExit(f"marker <!--walk:{name}--> not found in {page}")
        s = pat.sub(lambda m: m.group(1) + "\n    " + walk(width, name) + "\n    " + m.group(2), s)
    page.write_text(s)


if __name__ == "__main__":
    main()
