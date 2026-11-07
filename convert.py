import json, sys
sys.path.insert(0, "/Users/richard/Dev/swoozh-icons")
from convert_names import ARROWS, UI
D = "/Users/richard/Dev/swoozh-icons/"
jobs = [{"page": "0:1", "src": "Arrows", "title": "Arrows components", "names": ARROWS},
        {"page": "2915:883", "src": "UI", "title": "UI components", "names": UI}]
want = sys.argv[1:]
jobs = [j for j in jobs if not want or any(w.lower() in j["title"].lower() for w in want)]
open(D + "convert.js", "w").write("const JOBS = " + json.dumps(jobs) + ";\n" + open(D + "convert_tpl.js").read())
print([j["title"] for j in jobs])
