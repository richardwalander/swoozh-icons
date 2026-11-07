"""Generate build.js: Figma Plugin API script that creates Style=Outline/Filled
component sets for the icons in icons.py, one wrapper frame per category page.
Usage: python3 -I build.py [category-substring ...]"""
import json, sys, re
sys.path.insert(0, "/Users/richard/Dev/swoozh-icons")
from icons import CATEGORIES, NEW

D = "/Users/richard/Dev/swoozh-icons/"
ST = 'stroke="#000" stroke-width="1.5" stroke-linecap="butt" stroke-linejoin="miter" stroke-miterlimit="10" fill="none"'


def close_all(d):
    subs = [s for s in re.split(r"(?=M)", d) if s.strip()]
    return "".join(s if s.rstrip().endswith("Z") else s + "Z" for s in subs)


def svg(paths):
    return '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">' + "".join(paths) + "</svg>"


SPECIAL = ("e", "g", "gf")


def outline(elems):
    """Plain SVG, or (svg, kinds) when the icon has erase/glyph parts that need boolean ops."""
    if not any(k in SPECIAL for k, _ in elems):
        p = []
        for k, d in elems:
            if k in ("o", "s", "cut"):
                p.append(f'<path d="{d}" {ST}/>')
            elif k in ("d", "f"):
                p.append(f'<path d="{d}" fill="#000"/>')
        return svg(p), None
    p, kinds = [], []
    for k, d in elems:
        if k in ("o", "s", "cut"):
            p.append(f'<path d="{d}" {ST}/>'); kinds.append("T")
        elif k in ("d", "f"):
            p.append(f'<path d="{d}" fill="#000"/>'); kinds.append("S")
        elif k == "e":
            p.append(f'<path d="{d}" fill="#000"/>'); kinds.append("CF")
        elif k == "g":
            p.append(f'<path d="{d}" {ST}/>'); kinds.append("TG")
        elif k == "gf":
            p.append(f'<path d="{d}" fill="#000"/>'); kinds.append("SG")
    return svg(p), kinds


def filled(elems):
    p, kinds = [], []
    for k, d in elems:
        if k == "s":
            p += [f'<path d="{close_all(d)}" fill="#000"/>', f'<path d="{d}" {ST}/>']
            kinds += ["S", "T"]
        elif k == "o":
            p.append(f'<path d="{d}" {ST}/>'); kinds.append("T")
        elif k == "f":
            p.append(f'<path d="{d}" fill="#000"/>'); kinds.append("S")
        elif k in ("cut", "k"):
            if k == "cut" and "Z" in d:
                p.append(f'<path d="{d}" fill="#000"/>'); kinds.append("CF")
            p.append(f'<path d="{d}" {ST}/>'); kinds.append("C")
        elif k in ("d", "e"):
            p.append(f'<path d="{d}" fill="#000"/>'); kinds.append("CF")
        elif k == "g":
            p.append(f'<path d="{d}" {ST}/>'); kinds.append("TG")
        elif k == "gf":
            p.append(f'<path d="{d}" fill="#000"/>'); kinds.append("SG")
    return svg(p), kinds


only_new = "--new" in sys.argv
want = [a for a in sys.argv[1:] if a != "--new"]
data = []
for cat, icons in CATEGORIES.items():
    if want and not any(w.lower() in cat.lower() for w in want):
        continue
    items = []
    for name, (elems, tags) in icons.items():
        if only_new and name not in NEW:
            continue
        fs, kinds = filled(elems)
        os_, ok = outline(elems)
        items.append({"name": name, "desc": tags, "o": os_, "ok": ok, "f": fs, "k": kinds})
    if not items:
        continue
    data.append({"page": cat, "title": {"➡️ Arrows": "Arrows components", "📱 UI": "UI components"}.get(cat, cat.split(" ", 1)[1]), "icons": items})

js = "const DATA = " + json.dumps(data, ensure_ascii=False) + ";\n" + open(D + "build_tpl.js").read()
open(D + "build.js", "w").write(js)
print("icons:", sum(len(c["icons"]) for c in data), "in", [c["title"] for c in data])
