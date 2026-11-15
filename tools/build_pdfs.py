"""Render pdf/<id>.pdf printable study guides from data/<id>.json (uses Playwright + Chrome)."""
import json, os, re, html, sys
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = lambda s: html.escape(str(s))
ATTR = ("Scripture quotations are from the ESV® Bible (The Holy Bible, English Standard Version®), © 2001 by Crossway, "
        "a publishing ministry of Good News Publishers. Used by permission. All rights reserved.")
CSS = """
@page{size:Letter;margin:0.7in 0.75in 0.8in}
body{font:10.5pt/1.5 Georgia,'Times New Roman',serif;color:#1d1712}
h1{font-size:30pt;margin:0 0 4pt;color:#5a3412}h2{font-size:15pt;color:#5a3412;border-bottom:1.5pt solid #b5793a;padding-bottom:3pt;margin:20pt 0 8pt;break-after:avoid}
h3{font-size:12pt;margin:12pt 0 4pt;break-after:avoid;color:#2b2118}
.cover{height:8.6in;display:flex;flex-direction:column;justify-content:center;border-left:6pt solid #b5793a;padding-left:22pt;break-after:page}
.cover .kicker{font:600 10pt Helvetica,Arial,sans-serif;letter-spacing:.15em;text-transform:uppercase;color:#8a5a2a}
.cover .tag{font-size:15pt;font-style:italic;color:#4a3b2e;margin:8pt 0 18pt}
.cover .meta{font:10pt Helvetica,Arial,sans-serif;color:#6f6254}
dl dt{font:700 9pt Helvetica,Arial,sans-serif;text-transform:uppercase;letter-spacing:.06em;color:#8a5a2a;margin-top:8pt}dl dd{margin:1pt 0 0}
.part{border-left:2.5pt solid #b5793a;padding-left:10pt;margin:8pt 0;break-inside:avoid}.part ul{margin:3pt 0;padding-left:16pt}
.rng{color:#6f6254;font-size:9pt}
blockquote{margin:6pt 0;padding:5pt 10pt;border-left:3pt solid #b5793a;background:#f6efe4;break-inside:avoid}
blockquote cite{display:block;font:9pt Helvetica,Arial,sans-serif;color:#6f6254;font-style:normal;margin-top:2pt}
.theme{margin:6pt 0;break-inside:avoid}.theme b{color:#5a3412}
ul.r li,ol li{margin:3pt 0}
.ch{break-inside:avoid;border-top:.6pt solid #d9cbb5;padding-top:6pt;margin-top:10pt}
.ch h3{margin-top:0}.ch .n{display:inline-block;min-width:22pt;color:#fff;background:#7a4b1e;border-radius:4pt;text-align:center;font:700 9pt Helvetica,Arial,sans-serif;padding:2pt 4pt;margin-right:6pt}
.ch .x{font:9pt Helvetica,Arial,sans-serif;color:#6f6254}
.lines{border-bottom:.5pt solid #cdbfa8;height:16pt}
.attr{font:8pt Helvetica,Arial,sans-serif;color:#6f6254;margin-top:18pt;border-top:.5pt solid #cdbfa8;padding-top:6pt}
.newpage{break-before:page}
"""
def guide_html(g):
    o = g["overview"]; n = g["chapters"]
    h = [f"<!doctype html><html><head><meta charset='utf-8'><title>{E(g['name'])}: Bible Study Guide (ESV)</title><style>{CSS}</style></head><body>"]
    h.append(f"<section class='cover'><div class='kicker'>Bible Study Guide · ESV</div><h1>{E(g['name'])}</h1><div class='tag'>{E(g['tagline'])}</div>"
             f"<div class='meta'>{n} chapter{'s' if n > 1 else ''} · Overview, outline, themes, key verses, Christ connections, and chapter-by-chapter discussion questions</div>"
             f"<div class='attr' style='margin-top:40pt'>{E(ATTR)}</div></section>")
    h.append("<h2>Overview</h2><dl>" + "".join(f"<dt>{k.title()}</dt><dd>{E(o[k])}</dd>" for k in ["author", "date", "audience", "setting", "purpose", "structure"] if o.get(k)) + "</dl>")
    if g.get("readingPlan"): h.append(f"<h3>Reading plan</h3><p>{E(g['readingPlan'])}</p>")
    h.append("<h2>Outline</h2>" + "".join(f"<div class='part'><b>{E(p['title'])}</b> <span class='rng'>({E(p['range'])})</span><ul>" + "".join(f"<li>{E(i['title'])} <span class='rng'>({E(i['range'])})</span></li>" for i in p["items"]) + "</ul></div>" for p in g["outline"]))
    h.append("<h2>Key Themes</h2>" + "".join(f"<div class='theme'><b>{E(t['title'])}.</b> {E(t['text'])}</div>" for t in g["themes"]))
    h.append("<h2>Key Verses</h2>" + "".join(f"<blockquote>“{E(v['quote'])}”<cite>{E(v['ref'])} (ESV)</cite></blockquote>" for v in g["keyVerses"]))
    h.append(f"<h2>Christ in {E(g['name'])}</h2><ul class='r'>" + "".join(f"<li><b>{E(x['ref'])}</b>: {E(x['text'])}</li>" for x in g["christInBook"]) + "</ul>")
    h.append("<h2>Cross-References</h2><ul class='r'>" + "".join(f"<li><b>{E(x['ref'])}</b>: {E(x['note'])}</li>" for x in g["crossReferences"]) + "</ul>")
    h.append("<h2 class='newpage'>Chapter by Chapter</h2>")
    for c in g["chapterList"]:
        h.append(f"<div class='ch'><h3><span class='n'>{c['n']}</span>{E(c['title'])}</h3><p>{E(c['summary'])}</p><ol>" + "".join(f"<li>{E(q)}</li>" for q in c["questions"]) + "</ol>"
                 f"<div class='x'>Cross-references: {E('; '.join(c['crossRefs']))}</div></div>")
    h.append("<h2 class='newpage'>Reflection &amp; Application</h2><ol>" + "".join(f"<li>{E(r)}</li>" for r in g["reflection"]) + "</ol>")
    h.append("<h3>My notes</h3>" + "<div class='lines'></div>" * 14)
    h.append(f"<div class='attr'>{E(ATTR)} Study notes, summaries, and questions are original to the Bible Study Guides app (hullander28.github.io/bible-study-guides). Read the full text at esv.org.</div></body></html>")
    return "".join(h)

def main(ids):
    os.makedirs(os.path.join(ROOT, "pdf"), exist_ok=True)
    src = open(os.path.join(ROOT, "js/books.js")).read()
    all_ids = re.findall(r'\["([a-z0-9-]+)","', src)
    ids = ids or all_ids
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = b.new_page()
        for bid in ids:
            g = json.load(open(os.path.join(ROOT, f"data/{bid}.json")))
            pg.set_content(guide_html(g), wait_until="load")
            foot = (f"<div style='font:7.5pt Helvetica,Arial,sans-serif;color:#7a6a58;width:100%;padding:0 0.75in;display:flex;justify-content:space-between'>"
                    f"<span>{E(g['name'])} · Bible Study Guide</span><span>ESV® © Crossway. Used by permission.</span><span class='pageNumber'></span></div>")
            pg.pdf(path=os.path.join(ROOT, f"pdf/{bid}.pdf"), format="Letter", print_background=True, display_header_footer=True,
                   header_template="<span></span>", footer_template=foot, margin={"top": "0.7in", "bottom": "0.8in", "left": "0.75in", "right": "0.75in"})
            print(bid, os.path.getsize(os.path.join(ROOT, f"pdf/{bid}.pdf")) // 1024, "KB")
        b.close()

if __name__ == "__main__":
    main(sys.argv[1:])
