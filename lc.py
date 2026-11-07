import json, sys, collections
sys.path.insert(0, "/Users/richard/Dev/swoozh-icons")
from icons import CATEGORIES
from convert_names import ARROWS, UI
have = set(ARROWS) | set(UI) | {k for v in CATEGORIES.values() for k in v}
d = json.load(open("lucide_cats.json"))
inv = collections.defaultdict(list)
for icon, cats in d.items():
    for c in cats: inv[c].append(icon)
print(len(d), "icons;", {k: len(v) for k, v in sorted(inv.items())})
skip = ("gaming", "science", "animals", "sports", "text", "development", "medical", "layout", "arrows", "design", "math", "shapes")
for k, v in sorted(inv.items()):
    if k in skip: continue
    print(f"\n## {k}: " + " ".join(x for x in v if x not in have))
