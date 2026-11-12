"""Generate stroke-based SVGs (icons/stroke/*.svg) whose line thickness is the root stroke-width attribute.
Source: icons.py geometry (strokes, dots, erase masks); icons that only exist in Figma fall back to the raw export.
Usage: python3 -I tools/gen_stroke.py"""
import json, os, re, sys
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
sys.path.insert(0, D)
from icons import CATEGORIES, MITER

ROOT = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-miterlimit="10">'
FILL = 'fill="currentColor" stroke="none"'

def icon_svg(name, elems):
    solids, cuts, tops = [], [], []
    for k, d in elems:
        if k in ("o", "s", "cut"): solids.append(f'<path d="{d}"/>')
        elif k in ("d", "f"): solids.append(f'<path d="{d}" {FILL}/>')
        elif k == "e": cuts.append(f'<path d="{d}" fill="#000" stroke="none"/>')
        elif k == "g": tops.append(f'<path d="{d}"/>')
        elif k == "gf": tops.append(f'<path d="{d}" {FILL}/>')
        elif k == "k": pass  # filled-style only
        else: raise ValueError(k)
    if cuts:
        mid = "m-" + name
        body = (f'<mask id="{mid}" maskUnits="userSpaceOnUse" x="0" y="0" width="24" height="24">'
                f'<rect width="24" height="24" fill="#fff" stroke="none"/>{"".join(cuts)}</mask>'
                f'<g mask="url(#{mid})">{"".join(solids)}</g>{"".join(tops)}')
    else:
        body = "".join(solids + tops)
    root = ROOT.replace('stroke-miterlimit="10"', f'stroke-miterlimit="{MITER[name]}"') if name in MITER else ROOT
    return root + body + "</svg>"

def from_raw(svg):
    b = re.sub(r'^.*?<svg[^>]*>', '', svg, flags=re.S).rsplit("</svg>", 1)[0].strip()
    b = re.sub(r'<[^>]*stroke="black"[^>]*>', lambda m: m.group(0) if 'stroke-width' in m.group(0) else m.group(0).replace('stroke="black"', 'stroke="black" stroke-width="1"'), b)
    b = b.replace('stroke="black"', '').replace('stroke-width="1.5"', '').replace('fill="black"', FILL)
    b = re.sub(r'<rect[^>]*fill="white"[^>]*/>', '', b)  # Lucide-era eraser rect (rotate-cw)
    # mask shapes must not inherit the root stroke (they only define the inside-stroke clip region)
    b = re.sub(r'(<mask[^>]*>)(.*?)(</mask>)', lambda m: m.group(1) + re.sub(r'<(path|circle|rect|ellipse)\b', r'<\1 stroke="none"', m.group(2)) + m.group(3), b, flags=re.S)
    return ROOT + re.sub(r'\s+', ' ', b).replace(' />', '/>') + "</svg>"

os.makedirs(D + "icons/stroke", exist_ok=True)
for f in os.listdir(D + "icons/stroke"): os.remove(D + "icons/stroke/" + f)
raw = {i["name"]: i for i in json.load(open(D + "tools/export/raw.json"))["icons"]}
py = {n: e for cat in CATEGORIES.values() for n, (e, _) in cat.items()}
names = sorted(os.listdir(D + "icons/outline"))
n_py = n_raw = 0
for fn in names:
    name = fn[:-4]
    if name in py: svg = icon_svg(name, py[name]); n_py += 1
    else: svg = from_raw(raw[name]["outline"]); n_raw += 1
    open(D + "icons/stroke/" + fn, "w").write(svg)
print(f"stroke svgs: {n_py} from icons.py, {n_raw} from Figma raw")
