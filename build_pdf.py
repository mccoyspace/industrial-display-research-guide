#!/usr/bin/env python3
"""Build the combined single-layout PDF from the guide + companion research.

Usage:
    python3 build_pdf.py          # or: make pdf

Requires: pip install weasyprint markdown
macOS:    brew install pango     (WeasyPrint's rendering backend)

Layout notes: cover + linked TOC with page numbers, Part I (main guide),
Part II (panel-PC companion report). Fonts prefer Liberation/DejaVu (Linux)
and fall back to Helvetica Neue/Georgia/Menlo on macOS. For output identical
to the Linux build, install the Liberation fonts.
"""
import re
from pathlib import Path

import markdown
from weasyprint import HTML

BASE = Path(__file__).resolve().parent
GUIDE = BASE / "contemporary-artists-guide-to-industrial-displays.md"
COMPANION = BASE / "panel-pc-buying-guide.md"
OUT = BASE / "contemporary-artists-guide-to-industrial-displays.pdf"

MD_EXT = ["tables", "fenced_code", "toc", "sane_lists"]


def md_to_html(path, id_prefix=""):
    text = path.read_text(encoding="utf-8")
    # glyph safety for bundled fonts
    text = text.replace("⭐", "★")  # star emoji -> black star
    html = markdown.markdown(text, extensions=MD_EXT)
    if id_prefix:
        html = re.sub(r'id="', f'id="{id_prefix}', html)
    return html


def extract_toc(html, levels=("h2",)):
    entries = []
    for m in re.finditer(r'<(h[12]) id="([^"]+)">(.*?)</\1>', html):
        tag, hid, txt = m.groups()
        if tag in levels:
            txt = re.sub(r"<[^>]+>", "", txt)
            entries.append((hid, txt))
    return entries


guide_html = md_to_html(GUIDE)
comp_html = md_to_html(COMPANION, id_prefix="p2-")

# Drop each source doc's own h1 (part dividers are supplied below)
guide_html = re.sub(r"<h1[^>]*>.*?</h1>", "", guide_html, count=1)
comp_html = re.sub(r"<h1[^>]*>.*?</h1>", "", comp_html, count=1)

toc1 = extract_toc(guide_html)
toc2 = extract_toc(comp_html)


def toc_block(entries, part_label):
    items = "\n".join(f'<li><a href="#{hid}">{txt}</a></li>' for hid, txt in entries)
    return f'<div class="toc-part">{part_label}</div><ul class="toc">{items}</ul>'


SANS = '"Liberation Sans", "Helvetica Neue", Arial, sans-serif'
SERIF = '"Liberation Serif", Georgia, "Times New Roman", serif'
MONO = '"DejaVu Sans Mono", Menlo, "Liberation Mono", monospace'

CSS = f"""
@page {{
  size: letter;
  margin: 20mm 16mm 18mm 16mm;
  @bottom-left {{ content: "The Contemporary Artist\\2019s Guide to Industrial Displays"; font-family: {SANS}; font-size: 7pt; color: #8a8a8a; }}
  @bottom-right {{ content: counter(page) " / " counter(pages); font-family: {SANS}; font-size: 7.5pt; color: #8a8a8a; }}
}}
@page cover {{ margin: 0; @bottom-left {{ content: none }} @bottom-right {{ content: none }} }}
@page divider {{ @bottom-left {{ content: none }} }}

html {{ font-size: 9.5pt; }}
body {{ font-family: {SERIF}; color: #1c1c1e; line-height: 1.45; }}

/* ---------- cover ---------- */
.cover {{ page: cover; height: 279mm; background: #14141f; color: #f4f2ec; position: relative; }}
.cover .band {{ position: absolute; top: 0; left: 0; width: 9mm; height: 279mm; background: #e4572e; }}
.cover .inner {{ position: absolute; top: 58mm; left: 26mm; right: 22mm; }}
.cover h1 {{ font-family: {SANS}; font-size: 27pt; line-height: 1.15; font-weight: bold; margin: 0 0 8mm 0; letter-spacing: -0.3pt; color: #f4f2ec !important; }}
.cover .sub {{ font-family: {SANS}; font-size: 11.5pt; color: #d8d4c8; line-height: 1.5; margin-bottom: 14mm; }}
.cover .meta {{ font-family: {SANS}; font-size: 9pt; color: #9c98a8; line-height: 1.8; border-top: 0.4pt solid #4a4a5e; padding-top: 5mm; }}
.cover .meta b {{ color: #d8d4c8; }}
.cover .kicker {{ font-family: {SANS}; font-size: 8.5pt; letter-spacing: 2.5pt; text-transform: uppercase; color: #e4572e; margin-bottom: 10mm; }}

/* ---------- TOC ---------- */
.toc-page {{ page-break-before: always; }}
.toc-title {{ font-family: {SANS}; font-size: 16pt; font-weight: bold; color: #14141f; border-bottom: 2pt solid #e4572e; padding-bottom: 2mm; margin-bottom: 6mm; }}
.toc-part {{ font-family: {SANS}; font-size: 9pt; font-weight: bold; letter-spacing: 1.5pt; text-transform: uppercase; color: #e4572e; margin: 5mm 0 2mm 0; }}
ul.toc {{ list-style: none; margin: 0; padding: 0; }}
ul.toc li {{ font-family: {SANS}; font-size: 9pt; margin: 0 0 1.6mm 0; }}
ul.toc a {{ text-decoration: none; color: #1c1c1e; }}
ul.toc a::after {{ content: leader(". ") target-counter(attr(href), page); color: #8a8a8a; }}

/* ---------- part dividers ---------- */
.divider {{ page: divider; page-break-before: always; padding-top: 90mm; }}
.divider .num {{ font-family: {SANS}; font-size: 10pt; letter-spacing: 3pt; text-transform: uppercase; color: #e4572e; margin-bottom: 4mm; }}
.divider h1 {{ font-family: {SANS}; font-size: 21pt; color: #14141f; margin: 0 0 4mm 0; border: none; }}
.divider p {{ font-family: {SANS}; font-size: 9.5pt; color: #666; max-width: 120mm; }}

/* ---------- headings ---------- */
h1, h2, h3, h4 {{ font-family: {SANS}; color: #14141f; }}
h2 {{ page-break-before: always; font-size: 15pt; border-bottom: 1.6pt solid #e4572e; padding-bottom: 1.5mm; margin: 0 0 4mm 0; }}
h3 {{ font-size: 11pt; margin: 6mm 0 2mm 0; page-break-after: avoid; }}
h4 {{ font-size: 9.5pt; margin: 4mm 0 1.5mm 0; page-break-after: avoid; }}
h2 + p, h3 + p {{ page-break-before: avoid; }}

p {{ margin: 0 0 2.4mm 0; }}
strong {{ color: #14141f; }}
hr {{ display: none; }}
a {{ color: #b23a1c; text-decoration: none; }}

/* ---------- blockquote ---------- */
blockquote {{ margin: 3mm 0; padding: 2.5mm 5mm; border-left: 2.5pt solid #e4572e; background: #faf6f1; font-style: italic; page-break-inside: avoid; }}
blockquote p {{ margin: 0; }}

/* ---------- code ---------- */
code {{ font-family: {MONO}; font-size: 7.6pt; background: #f1efe9; padding: 0.2mm 1mm; border-radius: 1pt; }}
pre {{ background: #f1efe9; border: 0.4pt solid #ddd8cc; border-radius: 2pt; padding: 3mm; font-size: 7.4pt; line-height: 1.4; white-space: pre-wrap; page-break-inside: avoid; margin: 2.5mm 0; }}
pre code {{ background: none; padding: 0; }}

/* ---------- tables ---------- */
table {{ width: 100%; border-collapse: collapse; margin: 2.5mm 0 3.5mm 0; font-family: {SANS}; font-size: 7.4pt; line-height: 1.32; }}
th {{ background: #14141f; color: #f4f2ec; text-align: left; padding: 1.4mm 1.8mm; font-size: 7.2pt; }}
td {{ padding: 1.3mm 1.8mm; border-bottom: 0.35pt solid #d8d4c8; vertical-align: top; }}
tr:nth-child(even) td {{ background: #f7f5ef; }}
table code {{ font-size: 6.8pt; }}
tr {{ page-break-inside: avoid; }}
thead {{ display: table-header-group; }}

/* ---------- lists ---------- */
ul, ol {{ margin: 1mm 0 2.5mm 0; padding-left: 5.5mm; }}
li {{ margin-bottom: 1mm; }}

em {{ color: #333; }}
"""

cover = """
<div class="cover">
  <div class="band"></div>
  <div class="inner">
    <div class="kicker">McCoySpace &middot; Studio Technical Reference</div>
    <h1>The Contemporary Artist&rsquo;s Guide<br/>to Industrial Displays</h1>
    <div class="sub">Selecting, modifying, and maintaining commercial and industrial
    displays for long-lived media artworks &mdash; touch monitors, panel PCs, Android
    signage, and semi-barebone systems, under Android and Ubuntu/Linux.</div>
    <div class="meta">
      Prepared for the studio of <b>Jennifer and Kevin McCoy</b><br/>
      July 2026 &middot; Research base: five parallel investigation streams, 200+ sources,
      verified on load-bearing claims<br/>
      Part I &mdash; The Guide &nbsp;&nbsp;|&nbsp;&nbsp; Part II &mdash; Companion Research: Industrial Panel PCs
    </div>
  </div>
</div>
"""

toc_page = f"""
<div class="toc-page">
  <div class="toc-title">Contents</div>
  {toc_block(toc1, "Part I — The Guide")}
  {toc_block(toc2, "Part II — Companion Research: Industrial Panel PCs")}
</div>
"""

div1 = """
<div class="divider">
  <div class="num">Part I</div>
  <h1>The Contemporary Artist&rsquo;s Guide to Industrial Displays</h1>
  <p>The full guide: product classes, buying strategy, shortlists, SoCs and mainboards,
  panels and touch components, scoring, studio configurations, risks, and final
  recommendations, with appendices.</p>
</div>
"""

div2 = """
<div class="divider">
  <div class="num">Part II</div>
  <h1>Companion Research: Industrial Panel PCs</h1>
  <p>The unabridged panel-PC research report &mdash; vendor-by-vendor x86 and ARM findings,
  OPS/SDM modular architectures, lifecycle and warranty comparison, and real-world
  Linux evidence, with per-claim evidence labels.</p>
</div>
"""

doc = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body>
{cover}
{toc_page}
{div1}
{guide_html}
{div2}
{comp_html}
</body></html>"""

HTML(string=doc).write_pdf(str(OUT))
print("written:", OUT)
