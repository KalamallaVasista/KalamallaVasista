#!/usr/bin/env python3
"""Generate an analog + digital IST clock as an SVG.

Usage: python3 scripts/generate_clock.py assets/clock.svg
No third-party packages needed.
"""
import math
import sys
from datetime import datetime, timedelta, timezone

IST = timezone(timedelta(hours=5, minutes=30))
CX = CY = 200


def polar(r, deg):
    a = math.radians(deg - 90)
    return CX + r * math.cos(a), CY + r * math.sin(a)


def build(now):
    h, m, s = now.hour, now.minute, now.second
    hour_deg = (h % 12) * 30 + m * 0.5
    min_deg = m * 6 + s * 0.1
    sec_deg = s * 6

    ticks = []
    for i in range(60):
        major = i % 5 == 0
        x1, y1 = polar(160, i * 6)
        x2, y2 = polar(160 - (14 if major else 6), i * 6)
        color = "#58a6ff" if major else "#3b4a5c"
        width = 3 if major else 1.2
        ticks.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>'
        )

    nums = []
    for n in range(1, 13):
        x, y = polar(128, n * 30)
        nums.append(
            f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="middle" dominant-baseline="central" '
            f'font-size="22" font-weight="700" fill="#c9d1d9">{n}</text>'
        )

    h12 = h % 12 or 12
    ampm = "AM" if h < 12 else "PM"
    date_txt = now.strftime("%a · %d %b %Y")
    synced = now.strftime("synced %H:%M IST")

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 500" width="400" height="500" role="img" aria-label="Clock showing {h12}:{m:02d} {ampm} IST">
<defs>
  <radialGradient id="bezel" cx="50%" cy="35%" r="70%">
    <stop offset="0" stop-color="#3a4656"/><stop offset="1" stop-color="#0b0f14"/>
  </radialGradient>
  <radialGradient id="face" cx="50%" cy="40%" r="65%">
    <stop offset="0" stop-color="#121b27"/><stop offset="1" stop-color="#06090d"/>
  </radialGradient>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="2.5" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>
<style>
  text {{ font-family: "Fira Code", "SF Mono", Consolas, "DejaVu Sans Mono", monospace; }}
  .colon {{ animation: blink 1s steps(2, start) infinite; }}
  @keyframes blink {{ to {{ visibility: hidden; }} }}
</style>

<circle cx="{CX}" cy="{CY}" r="186" fill="url(#bezel)"/>
<circle cx="{CX}" cy="{CY}" r="176" fill="none" stroke="#58a6ff" stroke-opacity=".35" stroke-width="1.5"/>
<circle cx="{CX}" cy="{CY}" r="170" fill="url(#face)"/>

{''.join(ticks)}
{''.join(nums)}

<text x="{CX}" y="150" text-anchor="middle" font-size="12" letter-spacing="4" fill="#58a6ff">IST</text>
<text x="{CX}" y="262" text-anchor="middle" font-size="10" letter-spacing="2" fill="#6e7b8b">UTC+5:30</text>

<line x1="{CX}" y1="{CY+14}" x2="{CX}" y2="{CY-82}" stroke="#e6edf3" stroke-width="8" stroke-linecap="round" transform="rotate({hour_deg:.2f} {CX} {CY})"/>
<line x1="{CX}" y1="{CY+16}" x2="{CX}" y2="{CY-120}" stroke="#58a6ff" stroke-width="5" stroke-linecap="round" transform="rotate({min_deg:.2f} {CX} {CY})"/>
<g filter="url(#glow)">
  <g>
    <line x1="{CX}" y1="{CY+30}" x2="{CX}" y2="{CY-138}" stroke="#ff5a5f" stroke-width="2" stroke-linecap="round"/>
    <animateTransform attributeName="transform" type="rotate" from="{sec_deg} {CX} {CY}" to="{sec_deg + 360} {CX} {CY}" dur="60s" repeatCount="indefinite"/>
  </g>
</g>
<circle cx="{CX}" cy="{CY}" r="9" fill="#ff5a5f"/>
<circle cx="{CX}" cy="{CY}" r="3.5" fill="#06090d"/>

<rect x="85" y="398" width="230" height="58" rx="12" fill="#0b121a" stroke="#1f6feb" stroke-opacity=".5"/>
<text x="{CX}" y="436" text-anchor="middle" font-size="32" font-weight="700" fill="#3fb950" filter="url(#glow)">{h12:02d}<tspan class="colon">:</tspan>{m:02d}<tspan font-size="14" fill="#8b949e" dx="6">{ampm}</tspan></text>
<text x="{CX}" y="478" text-anchor="middle" font-size="13" fill="#8b949e">{date_txt}</text>
<text x="{CX}" y="494" text-anchor="middle" font-size="9" fill="#4b5563">{synced}</text>
</svg>
'''


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "assets/clock.svg"
    now = datetime.now(IST)
    with open(out, "w", encoding="utf-8") as f:
        f.write(build(now))
    print(f"Wrote {out} for {now:%Y-%m-%d %H:%M:%S} IST")


if __name__ == "__main__":
    main()
