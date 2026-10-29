"""Gera assets/stats.svg com dados da API do GitHub (roda na Action stats.yml).

Localmente funciona sem token (limite de 60 req/h); na Action usa o GITHUB_TOKEN.
"""

import json
import os
import urllib.request
from datetime import date
from pathlib import Path

USER = os.environ.get("GH_USER", "nickezinho")
TOKEN = os.environ.get("GITHUB_TOKEN")
OUT = Path(__file__).parent / "assets" / "stats.svg"

MONO = "'JetBrains Mono','Fira Code',Consolas,'Courier New',monospace"
SANS = "'Segoe UI',Ubuntu,'Helvetica Neue',Arial,sans-serif"
PALETTE = ["#a78bfa", "#67e8f9", "#f472b6", "#ffe66d", "#4ade80", "#3a86ff"]


def api(path):
    req = urllib.request.Request(f"https://api.github.com{path}", headers={"Accept": "application/vnd.github+json"})
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def collect():
    user = api(f"/users/{USER}")
    repos = [r for r in api(f"/users/{USER}/repos?per_page=100&type=owner") if not r["fork"]]
    langs = {}
    for r in repos:
        for name, size in api(f"/repos/{r['full_name']}/languages").items():
            langs[name] = langs.get(name, 0) + size
    year = date.today().year
    commits = api(f"/search/commits?q=author:{USER}+committer-date:>={year}-01-01&per_page=1")["total_count"]
    prs = api(f"/search/issues?q=author:{USER}+type:pr&per_page=1")["total_count"]
    return {
        "repos": len(repos),
        "stars": sum(r["stargazers_count"] for r in repos),
        "followers": user["followers"],
        "commits": commits,
        "prs": prs,
        "year": year,
        "langs": sorted(langs.items(), key=lambda kv: -kv[1])[:6],
    }


def render(s):
    W, H = 900, 230
    rows = [
        (f"commits in {s['year']}", s["commits"]),
        ("public repos", s["repos"]),
        ("pull requests", s["prs"]),
        ("stars earned", s["stars"]),
        ("followers", s["followers"]),
    ]
    stats = "".join(
        f'<g class="in" style="animation-delay:{0.2 + i * 0.12:.2f}s">'
        f'<text x="40" y="{92 + i * 28}" font-family="{MONO}" font-size="14" fill="#8b93b8">{label}</text>'
        f'<text x="360" y="{92 + i * 28}" font-family="{MONO}" font-size="15" font-weight="700" fill="#e2e8ff" text-anchor="end">{value}</text>'
        f'<line x1="40" x2="360" y1="{101 + i * 28}" y2="{101 + i * 28}" stroke="#fff" stroke-opacity=".06"/></g>'
        for i, (label, value) in enumerate(rows)
    )

    total = sum(v for _, v in s["langs"]) or 1
    bar_x, bar_w = 430, 430
    segs, legend, x = [], [], bar_x
    for i, (name, size) in enumerate(s["langs"]):
        w = bar_w * size / total
        color = PALETTE[i % len(PALETTE)]
        segs.append(f'<rect x="{x:.1f}" y="78" width="{w:.1f}" height="12" fill="{color}"/>')
        x += w
        lx, ly = bar_x + (i % 2) * 215, 128 + (i // 2) * 30
        legend.append(
            f'<g class="in" style="animation-delay:{0.5 + i * 0.1:.2f}s"><circle cx="{lx + 6}" cy="{ly - 5}" r="5" fill="{color}"/>'
            f'<text x="{lx + 20}" y="{ly}" font-family="{SANS}" font-size="15" fill="#e2e8ff">{name} '
            f'<tspan fill="#8b93b8" font-family="{MONO}" font-size="13">{100 * size / total:.1f}%</tspan></text></g>'
        )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="GitHub stats for {USER}">
<defs>
  <linearGradient id="sbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0d1117"/><stop offset="1" stop-color="#111733"/></linearGradient>
  <linearGradient id="sedge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7c3aed"/><stop offset="1" stop-color="#06b6d4"/></linearGradient>
  <clipPath id="barclip"><rect x="{bar_x}" y="78" width="{bar_w}" height="12" rx="6"/></clipPath>
</defs>
<style>
  .in {{ animation:in .7s ease-out both; }}
  @keyframes in {{ from {{ opacity:0; transform:translateY(6px) }} to {{ opacity:1; transform:none }} }}
  .grow {{ transform-box:fill-box; transform-origin:0 50%; animation:grow 1.4s cubic-bezier(.2,.8,.2,1) .3s both; }}
  @keyframes grow {{ from {{ transform:scaleX(0) }} to {{ transform:scaleX(1) }} }}
  @media (prefers-reduced-motion: reduce) {{ * {{ animation:none !important; }} }}
</style>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="url(#sbg)" stroke="url(#sedge)" stroke-opacity=".7" stroke-width="1.5"/>
<text x="40" y="50" font-family="{MONO}" font-size="12" fill="#8b93b8" letter-spacing="3">STATS</text>
<text x="{bar_x}" y="50" font-family="{MONO}" font-size="12" fill="#8b93b8" letter-spacing="3">MOST USED LANGUAGES</text>
{stats}
<g clip-path="url(#barclip)"><g class="grow">{"".join(segs)}</g></g>
{"".join(legend)}
<text x="{W - 24}" y="{H - 14}" font-family="{MONO}" font-size="10" fill="#8b93b8" opacity=".6" text-anchor="end">updated {date.today().isoformat()}</text>
</svg>
"""
    OUT.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    data = collect()
    render(data)
    print(json.dumps(data))
