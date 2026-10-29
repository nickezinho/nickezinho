"""Gera os SVGs animados do README do perfil (header.svg e terminal.svg).

Rode `python generate.py` e faça commit da pasta assets/ junto com o README.
Tudo é SVG puro (CSS + SMIL), porque o GitHub não executa JavaScript.
"""

import math
import random
from pathlib import Path

OUT = Path(__file__).parent / "assets"
OUT.mkdir(exist_ok=True)
random.seed(7)

MONO = "'JetBrains Mono','Fira Code',Consolas,'Courier New',monospace"
SANS = "'Segoe UI',Ubuntu,'Helvetica Neue',Arial,sans-serif"


def typing(x, y, text, begin, char_dur, size, fill, clip_id, char_w=None, extra=""):
    """Texto que aparece letra por letra (clip discreto) + retorna o fim da animação."""
    char_w = char_w or size * 0.6
    width = len(text) * char_w
    steps = len(text)
    widths = ";".join(f"{i * char_w:.1f}" for i in range(steps + 1))
    dur = steps * char_dur
    svg = f"""
  <clipPath id="{clip_id}"><rect x="{x}" y="{y - size}" height="{size * 1.5}" width="0">
    <animate attributeName="width" values="{widths}" calcMode="discrete" begin="{begin}s" dur="{dur:.2f}s" fill="freeze"/>
  </rect></clipPath>
  <text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" fill="{fill}" textLength="{width:.1f}"
        lengthAdjust="spacingAndGlyphs" clip-path="url(#{clip_id})" xml:space="preserve" {extra}>{text}</text>"""
    return svg, begin + dur, width


# ---------------------------------------------------------------- header.svg
LYRICS = [
    "i'm samuel, a cs student",
    "software engineering &amp; ai",
    "building practical, scalable stuff",
    "where ai meets real business",
    "open to swe internships in SP",
    "everything in its right place",
]


def header():
    """Player de música: o "álbum" é o perfil e a letra é a bio."""
    W, H = 1200, 420
    LINE_S = 2.6  # segundos que cada linha da letra fica destacada
    cycle = LINE_S * len(LYRICS)

    stars = []
    for _ in range(60):
        x, y = random.uniform(0, W), random.uniform(0, H)
        d, delay = random.uniform(2, 6), random.uniform(0, 6)
        stars.append(
            f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.choice([0.6, 0.8, 1, 1.2])}" class="star" '
            f'style="animation-duration:{d:.1f}s;animation-delay:-{delay:.1f}s"/>'
        )

    # sulcos do vinil
    grooves = "".join(
        f'<circle cx="0" cy="0" r="{r}" fill="none" stroke="#ffffff" stroke-opacity="{0.05 + (r % 3) * 0.02:.2f}"/>'
        for r in range(40, 148, 6)
    )

    # mini equalizador do "NOW PLAYING"
    mini = "".join(
        f'<rect x="{480 + i * 6}" y="76" width="4" height="16" rx="1.5" class="mini" '
        f'style="animation-duration:{random.uniform(0.5, 0.9):.2f}s;animation-delay:-{random.uniform(0, 1):.2f}s"/>'
        for i in range(4)
    )

    lyrics = "".join(
        f'<text x="862" y="{132 + i * 38}" class="lyr" style="animation-delay:{i * LINE_S - cycle:.1f}s">{line}</text>'
        for i, line in enumerate(LYRICS)
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Now playing: Software Engineer, by Samuel — album OK Computer Science">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#2a1458"/><stop offset=".45" stop-color="#0d0f24"/><stop offset="1" stop-color="#05060d"/>
  </linearGradient>
  <radialGradient id="glow" cx=".18" cy=".5" r=".45">
    <stop offset="0" stop-color="#7c3aed" stop-opacity=".55"/><stop offset="1" stop-color="#7c3aed" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="cover" cx=".3" cy=".25" r="1">
    <stop offset="0" stop-color="#a78bfa"/><stop offset=".45" stop-color="#4c1d95"/><stop offset="1" stop-color="#0b1026"/>
  </radialGradient>
  <linearGradient id="planet" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#67e8f9"/><stop offset="1" stop-color="#3a86ff"/>
  </linearGradient>
  <linearGradient id="prog" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#a78bfa"/><stop offset="1" stop-color="#67e8f9"/>
  </linearGradient>
  <radialGradient id="label" cx=".5" cy=".5" r=".5">
    <stop offset="0" stop-color="#67e8f9"/><stop offset="1" stop-color="#7c3aed"/>
  </radialGradient>
  <clipPath id="coverclip"><rect x="40" y="50" width="320" height="320" rx="14"/></clipPath>
  <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="14" stdDeviation="16" flood-color="#000" flood-opacity=".55"/></filter>
</defs>
<style>
  .star {{ fill:#fff; animation-name:tw; animation-iteration-count:infinite; animation-timing-function:ease-in-out; }}
  @keyframes tw {{ 0%,100% {{ opacity:.1 }} 50% {{ opacity:.7 }} }}
  .spin {{ animation:spin 6s linear infinite; }}
  .orbit {{ transform-origin:200px 210px; animation:spin 14s linear infinite; }}
  @keyframes spin {{ to {{ transform:rotate(360deg) }} }}
  .vinyl {{ animation:slide 1.4s cubic-bezier(.2,.8,.2,1) .3s both; }}
  @keyframes slide {{ from {{ transform:translateX(-90px) }} to {{ transform:none }} }}
  .mini {{ fill:#4ade80; transform-box:fill-box; transform-origin:50% 100%; animation-name:eq;
           animation-iteration-count:infinite; animation-direction:alternate; animation-timing-function:ease-in-out; }}
  @keyframes eq {{ from {{ transform:scaleY(.2) }} to {{ transform:scaleY(1) }} }}
  .fill {{ transform-box:fill-box; transform-origin:0 50%; animation:fill 60s linear infinite; }}
  @keyframes fill {{ from {{ transform:scaleX(.18) }} to {{ transform:scaleX(1) }} }}
  .knob {{ animation:knob 60s linear infinite; }}
  @keyframes knob {{ from {{ transform:translateX(0) }} to {{ transform:translateX(268px) }} }}
  .lyr {{ font-family:{SANS}; font-size:17px; font-weight:700; fill:#fff; opacity:.28;
          animation:lyr {cycle:.1f}s ease-in-out infinite; }}
  @keyframes lyr {{ 0%,{100 / len(LYRICS) - 2:.1f}% {{ opacity:1 }} {100 / len(LYRICS):.1f}%,97% {{ opacity:.28 }} 100% {{ opacity:1 }} }}
  .in {{ animation:in .9s ease-out both; }}
  @keyframes in {{ from {{ opacity:0; transform:translateY(8px) }} to {{ opacity:1; transform:none }} }}
  @media (prefers-reduced-motion: reduce) {{ * {{ animation:none !important; }} .lyr {{ opacity:1 }} }}
</style>

<rect width="{W}" height="{H}" rx="18" fill="url(#bg)"/>
<rect width="{W}" height="{H}" rx="18" fill="url(#glow)"/>
<g>{"".join(stars)}</g>

<!-- vinil saindo da capa -->
<g class="vinyl">
  <g transform="translate(300 210)">
    <circle r="150" fill="#08080c"/>
    {grooves}
    <g class="spin">
      <circle r="40" fill="url(#label)"/>
      <rect x="-2" y="-34" width="4" height="12" rx="2" fill="#0b1026" opacity=".6"/>
      <circle r="5" fill="#08080c"/>
    </g>
  </g>
</g>

<!-- capa do álbum -->
<g filter="url(#shadow)">
  <rect x="40" y="50" width="320" height="320" rx="14" fill="url(#cover)"/>
</g>
<g clip-path="url(#coverclip)">
  <circle cx="200" cy="210" r="70" fill="none" stroke="#fff" stroke-opacity=".18"/>
  <circle cx="200" cy="210" r="110" fill="none" stroke="#fff" stroke-opacity=".12" stroke-dasharray="2 6"/>
  <circle cx="200" cy="210" r="150" fill="none" stroke="#fff" stroke-opacity=".08"/>
  <circle cx="200" cy="210" r="34" fill="url(#planet)"/>
  <ellipse cx="200" cy="210" rx="58" ry="12" fill="none" stroke="#e2e8ff" stroke-opacity=".7" stroke-width="2" transform="rotate(-18 200 210)"/>
  <g class="orbit"><circle cx="310" cy="210" r="6" fill="#ffe66d"/></g>
  <g class="orbit" style="animation-duration:22s;animation-direction:reverse"><circle cx="200" cy="140" r="3.5" fill="#f472b6"/></g>
  <text x="62" y="84" font-family="{MONO}" font-size="12" fill="#e2e8ff" opacity=".75" letter-spacing="3">OK COMPUTER SCIENCE</text>
  <text x="338" y="352" font-family="{MONO}" font-size="11" fill="#e2e8ff" opacity=".6" text-anchor="end">℗ 2026 · nickezinho</text>
</g>

<!-- info da faixa -->
<g class="in" style="animation-delay:.5s">
  {mini}
  <text x="512" y="91" font-family="{MONO}" font-size="13" fill="#4ade80" letter-spacing="3">NOW PLAYING</text>
  <text x="480" y="150" font-family="{SANS}" font-size="40" font-weight="800" fill="#fff">Software Engineer</text>
  <text x="480" y="184" font-family="{SANS}" font-size="20" fill="#c4b5fd">(Internship Edition)</text>
  <text x="480" y="222" font-family="{SANS}" font-size="17" fill="#e2e8ff">Samuel <tspan fill="#8b93b8">·  OK Computer Science  ·  São Paulo</tspan></text>
</g>

<g class="in" style="animation-delay:.8s">
  <rect x="480" y="268" width="290" height="5" rx="2.5" fill="#fff" fill-opacity=".15"/>
  <rect x="480" y="268" width="290" height="5" rx="2.5" fill="url(#prog)" class="fill"/>
  <g class="knob"><circle cx="502" cy="270.5" r="7" fill="#fff"/></g>
  <text x="480" y="298" font-family="{MONO}" font-size="12" fill="#8b93b8">0:42</text>
  <text x="770" y="298" font-family="{MONO}" font-size="12" fill="#8b93b8" text-anchor="end">4:20</text>

  <g fill="none" stroke="#c9d1ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <!-- shuffle -->
    <path d="M512 336 h8 l14 18 h8 M512 354 h8 l14 -18 h8 M538 332 l4 4 -4 4 M538 350 l4 4 -4 4" stroke="#4ade80"/>
    <!-- prev -->
    <path d="M582 335 v20" /><path d="M600 335 l-14 10 14 10 z" fill="#c9d1ff"/>
  </g>
  <circle cx="625" cy="345" r="24" fill="#fff"/>
  <g fill="#0b1026"><rect x="617" y="335" width="5" height="20" rx="1.5"/><rect x="628" y="335" width="5" height="20" rx="1.5"/></g>
  <g fill="none" stroke="#c9d1ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <!-- next -->
    <path d="M668 335 v20"/><path d="M650 335 l14 10 -14 10 z" fill="#c9d1ff"/>
    <!-- repeat -->
    <path d="M708 343 v-4 a4 4 0 0 1 4 -4 h22 M730 331 l4 4 -4 4 M738 347 v4 a4 4 0 0 1 -4 4 h-22 M716 359 l-4 -4 4 -4"/>
  </g>
</g>

<!-- letra -->
<g class="in" style="animation-delay:1.1s">
  <rect x="832" y="50" width="328" height="320" rx="14" fill="#fff" fill-opacity=".05" stroke="#fff" stroke-opacity=".08"/>
  <text x="862" y="88" font-family="{MONO}" font-size="12" fill="#8b93b8" letter-spacing="3">LYRICS</text>
  {lyrics}
</g>
</svg>
"""
    (OUT / "header.svg").write_text(svg, encoding="utf-8")


# -------------------------------------------------------------- terminal.svg
def terminal():
    W, H = 900, 430
    size = 16
    cw = size * 0.6
    x0, y = 32, 92
    lh = 27
    t = 0.6
    body = []
    n = 0

    prompt_w = len("samuel@sp:~$ ") * cw

    def cmd(text):
        nonlocal y, t, n
        n += 1
        body.append(
            f'<text x="{x0}" y="{y}" font-family="{MONO}" font-size="{size}" class="show" style="animation-delay:{t:.2f}s">'
            f'<tspan fill="#a78bfa">samuel</tspan><tspan fill="#8b93b8">@</tspan><tspan fill="#67e8f9">sp</tspan>'
            f'<tspan fill="#8b93b8">:~$</tspan></text>'
        )
        svg, end, _ = typing(x0 + prompt_w, y, text, t + 0.25, 0.06, size, "#e6edf3", f"c{n}")
        body.append(svg)
        t = end + 0.25
        y += lh

    def out(markup, plain_len=None):
        nonlocal y, t
        body.append(
            f'<text x="{x0}" y="{y}" font-family="{MONO}" font-size="{size}" fill="#c9d1d9" class="show" '
            f'style="animation-delay:{t:.2f}s" xml:space="preserve">{markup}</text>'
        )
        t += 0.18
        y += lh

    cmd("whoami")
    out('<tspan fill="#4ade80">→</tspan> Samuel · CS student · Software Engineering &amp; AI')
    out('<tspan fill="#4ade80">→</tspan> building practical stuff where AI meets real business')
    y += 6
    cmd("cat stack.txt")
    out('<tspan fill="#ffd43b">python</tspan>  <tspan fill="#f89820">java</tspan>  '
        '<tspan fill="#f7df1e">javascript</tspan>  <tspan fill="#67e8f9">apis</tspan>  <tspan fill="#f472b6">automation</tspan>')
    y += 6
    cmd("ls ./projects")
    out('<tspan fill="#60a5fa">triage-AI/</tspan>   <tspan fill="#60a5fa">company-goals/</tspan>   <tspan fill="#60a5fa">whatsapp-automation/</tspan>')
    y += 6
    cmd("cat fun_facts.txt")
    out('🎧 radiohead 🔛🔝    📺 hunter x hunter    🏀 basketball')
    y += 6
    # prompt final com cursor piscando
    body.append(
        f'<text x="{x0}" y="{y}" font-family="{MONO}" font-size="{size}" class="show" style="animation-delay:{t:.2f}s">'
        f'<tspan fill="#a78bfa">samuel</tspan><tspan fill="#8b93b8">@</tspan><tspan fill="#67e8f9">sp</tspan>'
        f'<tspan fill="#8b93b8">:~$</tspan></text>'
        f'<rect x="{x0 + prompt_w:.1f}" y="{y - size + 2}" width="{cw:.1f}" height="{size + 2}" fill="#67e8f9" '
        f'class="show cur" style="animation-delay:{t:.2f}s, {t:.2f}s"/>'
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Terminal: whoami, stack, projects, fun facts">
<defs>
  <linearGradient id="tbg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#0d1117"/><stop offset="1" stop-color="#111733"/>
  </linearGradient>
  <linearGradient id="edge" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#7c3aed"/><stop offset="1" stop-color="#06b6d4"/>
  </linearGradient>
</defs>
<style>
  .show {{ opacity:0; animation:sh .01s linear forwards; }}
  @keyframes sh {{ to {{ opacity:1 }} }}
  .cur {{ animation:sh .01s linear forwards, bl 1s steps(1) infinite; }}
  @keyframes bl {{ 50% {{ opacity:0 }} }}
  @media (prefers-reduced-motion: reduce) {{ .show,.cur {{ animation:none; opacity:1 }} }}
</style>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="url(#tbg)" stroke="url(#edge)" stroke-opacity=".7" stroke-width="1.5"/>
<path d="M1 15 a14 14 0 0 1 14 -14 h{W - 32} a14 14 0 0 1 14 14 v27 h-{W - 4} z" fill="#161b2e"/>
<circle cx="26" cy="22" r="6.5" fill="#ff5f57"/><circle cx="48" cy="22" r="6.5" fill="#febc2e"/><circle cx="70" cy="22" r="6.5" fill="#28c840"/>
<text x="{W / 2}" y="27" text-anchor="middle" font-family="{MONO}" font-size="13" fill="#8b93b8">samuel@sao-paulo: ~ — zsh</text>
{"".join(body)}
</svg>
"""
    (OUT / "terminal.svg").write_text(svg, encoding="utf-8")


header()
terminal()
print("ok ->", OUT)
