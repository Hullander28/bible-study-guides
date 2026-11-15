"""Compile src/<id>.txt study guides into data/<id>.json, validate, and update books.js + sw.js.
Format: header 'key: value' lines (name, tagline, author, date, audience, setting, purpose, structure, plan),
then sections '## outline|themes|verses|christ|xrefs|reflect|chapters'.
outline: '* Part title | range | start | end' then '- item | range'
themes/verses/christ/xrefs: '- a | b'; reflect: '- prompt'
chapters: '@ Title' / summary lines / '? question' / '> ref | ref'
"""
import json, re, sys, os, glob
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

def smart(s):
    s = re.sub(r"(\d)-(\d)", "\\1\u2013\\2", s)
    s = re.sub(r'(^|[\s(\[\u2014/])"', "\\1\u201c", s)
    s = s.replace('"', "\u201d")
    s = re.sub(r"(^|[\s(\[\u2014\u201c])'", "\\1\u2018", s)
    s = s.replace("'", "\u2019")
    s = s.replace(" -- ", ", ").replace("--", "\u2014")
    return s.strip()

def books():
    src = open(os.path.join(ROOT, "js/books.js")).read()
    return [(m[0], m[1], int(m[2])) for m in re.findall(r'\["([a-z0-9-]+)","([^"]+)",(\d+)', src)]

def parse(path, bid, name, nch):
    g = {"id": bid, "name": name, "chapters": nch, "overview": {}, "outline": [], "themes": [], "keyVerses": [],
         "christInBook": [], "crossReferences": [], "reflection": [], "chapterList": []}
    sec = None; cur = None
    for raw in open(path, encoding="utf-8"):
        line = raw.strip()
        if not line or line.startswith("//"): continue
        if line.startswith("## "): sec = line[3:].strip(); continue
        if sec is None:
            k, v = line.split(":", 1); k = k.strip(); v = smart(v)
            if k in ("tagline",): g["tagline"] = v
            elif k == "plan": g["readingPlan"] = v
            elif k == "name": pass
            else: g["overview"][k] = v
            continue
        if sec == "outline":
            if line.startswith("*"):
                p = [x.strip() for x in line[1:].split("|")]
                g["outline"].append({"title": smart(p[0]), "range": smart(p[1]), "start": int(p[2]), "end": int(p[3]), "items": []})
            else:
                p = [x.strip() for x in line[1:].split("|")]
                g["outline"][-1]["items"].append({"title": smart(p[0]), "range": smart(p[1])})
        elif sec in ("themes", "verses", "christ", "xrefs"):
            a, b = [x.strip() for x in line[1:].split("|", 1)]
            key = {"themes": ("themes", "title", "text"), "verses": ("keyVerses", "ref", "quote"),
                   "christ": ("christInBook", "ref", "text"), "xrefs": ("crossReferences", "ref", "note")}[sec]
            g[key[0]].append({key[1]: smart(a), key[2]: smart(b)})
        elif sec == "reflect":
            g["reflection"].append(smart(line[1:]))
        elif sec == "chapters":
            if line.startswith("@"):
                cur = {"n": len(g["chapterList"]) + 1, "title": smart(line[1:]), "summary": "", "questions": [], "crossRefs": []}
                g["chapterList"].append(cur)
            elif line.startswith("?"): cur["questions"].append(smart(line[1:]))
            elif line.startswith(">"): cur["crossRefs"] += [smart(x) for x in line[1:].split("|") if x.strip()]
            else: cur["summary"] = (cur["summary"] + " " + smart(line)).strip()
    if "readingPlan" not in g:
        g["readingPlan"] = (f"{nch} chapter{'s' if nch > 1 else ''}: " + (f"one chapter a day takes {nch} days; two a day takes about {-(-nch//2)} days. " if nch > 2 else "a short book you can read in one sitting, then work through the questions over a few days. ") +
                            "For each chapter, read it on ESV.org, then come back here for the summary, questions, and your notes.")
    return g

def validate(g, nch):
    errs = []
    for k in ("author", "date", "audience", "setting", "purpose"):
        if not g["overview"].get(k): errs.append("missing overview." + k)
    if not g.get("tagline"): errs.append("missing tagline")
    for k, mn in (("outline", 2), ("themes", 4), ("keyVerses", 3), ("christInBook", 2), ("crossReferences", 3), ("reflection", 5)):
        if len(g[k]) < mn: errs.append(f"{k} has {len(g[k])} < {mn}")
    if len(g["chapterList"]) != nch: errs.append(f"chapters {len(g['chapterList'])} != {nch}")
    for c in g["chapterList"]:
        if len(c["summary"]) < 80: errs.append(f"ch{c['n']} short summary")
        if not 3 <= len(c["questions"]) <= 4: errs.append(f"ch{c['n']} has {len(c['questions'])} questions")
        if not c["crossRefs"]: errs.append(f"ch{c['n']} no crossRefs")
    for v in g["keyVerses"]:
        if len(v["quote"]) > 260: errs.append("long quote " + v["ref"])
    return errs

def main():
    bl = books(); ready = {"genesis"}; bad = False
    for bid, name, nch in bl:
        p = os.path.join(ROOT, "src", bid + ".txt")
        if not os.path.exists(p): continue
        g = parse(p, bid, name, nch); errs = validate(g, nch)
        if errs: print("FAIL", bid, errs[:8]); bad = True; continue
        json.dump(g, open(os.path.join(ROOT, "data", bid + ".json"), "w"), ensure_ascii=False, indent=1)
        ready.add(bid)
    # re-validate every json in data/
    for f in glob.glob(os.path.join(ROOT, "data", "*.json")):
        json.load(open(f))
    # books.js ready flags
    js = open(os.path.join(ROOT, "js/books.js")).read()
    def rep(m):
        return f'["{m[1]}","{m[2]}",{m[3]}' + (',true]' if m[1] in ready else ']')
    js = re.sub(r'\["([a-z0-9-]+)","([^"]+)",(\d+)(?:,true)?\]', rep, js)
    open(os.path.join(ROOT, "js/books.js"), "w").write(js)
    # sw.js cache list + version
    sw = open(os.path.join(ROOT, "sw.js")).read()
    core = ["./", "index.html", "css/style.css", "js/books.js", "js/app.js", "manifest.webmanifest", "icons/icon-192.png"] + [f"data/{b}.json" for b, _, _ in bl if b in ready]
    sw = re.sub(r"const CORE = \[.*?\];", "const CORE = " + json.dumps(core) + ";", sw, flags=re.S)
    v = int(re.search(r'bsg-v(\d+)', sw)[1]) + 1
    sw = re.sub(r'bsg-v\d+', f"bsg-v{v}", sw)
    open(os.path.join(ROOT, "sw.js"), "w").write(sw)
    print(f"ready {len(ready)}/66; sw cache bsg-v{v}; chapters ready:", sum(n for b, _, n in bl if b in ready))
    print("missing:", [b for b, _, _ in bl if b not in ready])
    sys.exit(1 if bad else 0)
main()
