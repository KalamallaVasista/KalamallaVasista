#!/usr/bin/env python3
"""Generates assets/terminal-about.svg (the green terminal card in the README).

Edit the BLOCKS below, then run:
    python3 scripts/generate_card.py
and commit the updated assets/terminal-about.svg. No third-party packages needed.
"""
from html import escape
from pathlib import Path

HEADER = ".github/workflows/vasista_readme.yml"
FILES = ["about_me.txt", "projects.sh", "certs.yml"]

BLOCKS = [
    ("cat about_me.txt", "# ABOUT ME", [
        ("Data and Databases", "MySQL · SQL · dbt · Data Modeling"),
        ("BI and Visualization", "Power BI · DAX · What-If Analysis · KPI Dashboards"),
        ("Programming", "Python · C"),
        ("Tools and Workflow", "Git · GitHub · VS Code · Google Colab"),
        ("Analytics Focus", "Fraud Monitoring · Churn Risk · Revenue Recovery"),
        ("Education and Training", "B.Tech CSE (AI/ML) · ExcelR Data Analyst Course"),
    ]),
    ("cat projects.sh", "# PROJECTS", [
        ("B2B-Fraud-Risk-Engine", "MySQL · dbt · Power BI · What-If risk threshold (DAX)"),
        ("Revenue-Recovery-Engine", "SQL · dbt · Power BI · daily Risk Roster"),
    ]),
    ("cat certs.yml", "# CERTIFICATIONS", [
        ("Power BI Fundamentals", "Corporate Finance Institute (CFI)"),
        ("BI Essentials", "IBM"),
        ("Machine Learning with Python", "IBM"),
    ]),
]

W = 900
out, t = [], 0.30


def ln(delay, inner):
    out.append(f'<g class="ln" style="animation-delay:{delay:.2f}s">{inner}</g>')


ln(t, f'<text x="40" y="52" font-size="18" font-weight="700" fill="#79c0ff">{escape(HEADER)}</text>')
line_y = 72
y = 112
t += 0.40
ln(t, f'<text x="40" y="{y}" font-size="18"><tspan fill="#3fb950">$</tspan><tspan fill="#e6edf3"> ls</tspan></text>')
y += 36
t += 0.50
xs = [40, 290, 470]
ln(t, "".join(f'<text x="{x}" y="{y}" font-size="17" fill="#79c0ff">{escape(n)}</text>' for x, n in zip(xs, FILES)))
y += 44
for cmd, comment, sections in BLOCKS:
    t += 0.50
    ln(t, f'<text x="40" y="{y}" font-size="18"><tspan fill="#3fb950">$</tspan><tspan fill="#e6edf3"> {escape(cmd)}</tspan></text>')
    y += 36
    t += 0.50
    ln(t, f'<text x="40" y="{y}" font-size="13" fill="#6e7b8b">{escape(comment)}</text>')
    y += 30
    for title, items in sections:
        t += 0.40
        ln(t, f'<text x="40" y="{y}" font-size="17" font-weight="700" fill="#4ac26b">{escape(title)}</text>'
              f'<text x="40" y="{y+25}" font-size="17" fill="#e0896b">{escape(items)}</text>')
        y += 66
    y -= 66 - 25          # y now at last item line
    y += 47               # gap before next command
prompt_y = y - 47 + 49
t += 0.40
out.append(f'<g class="ln" style="animation-delay:{t:.2f}s"><text x="40" y="{prompt_y}" font-size="18" fill="#3fb950">$</text>'
           f'<rect class="cur" x="62" y="{prompt_y-16}" width="11" height="20" fill="#3fb950"/></g>')
H = prompt_y + 32

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Terminal: about me, projects and certifications">
<style>
text{{font-family:'Fira Code','SF Mono',Consolas,'DejaVu Sans Mono',monospace}}
.ln{{opacity:0;animation:show .5s ease-out forwards}}
@keyframes show{{from{{opacity:0;transform:translateX(-6px)}}to{{opacity:1;transform:none}}}}
.cur{{animation:blink 1s steps(2,start) infinite}}
@keyframes blink{{to{{visibility:hidden}}}}
</style>
<rect x="3" y="3" width="{W-6}" height="{H-6}" rx="14" fill="#0a1a12" stroke="#2ea043" stroke-width="2"/>
{out[0]}<line x1="40" y1="{line_y}" x2="{W-40}" y2="{line_y}" stroke="#2ea043" stroke-width="1.5"/>{''.join(out[1:])}
</svg>
'''
Path("assets").mkdir(exist_ok=True)
Path("assets/terminal-about.svg").write_text(svg, encoding="utf-8")
print(f"wrote assets/terminal-about.svg ({W}x{H})")
