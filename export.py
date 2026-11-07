"""Export page wrappers (or single icon sets with --sets) to previews/. Usage: python3 -I export.py "Page title" ... [--sets name ...]"""
import json, sys, base64, subprocess
D = "/Users/richard/Dev/swoozh-icons/"
args = sys.argv[1:]
sets = "--sets" in args
names = [a for a in args if a != "--sets"]
if sets:
    js = ("await figma.loadAllPagesAsync(); const out = {}; for (const nm of " + json.dumps(names) + ") { const s = figma.root.findOne(n => n.type === 'COMPONENT_SET' && n.name === nm);"
          " if (s) out[nm] = figma.base64Encode(await s.exportAsync({format: 'PNG', constraint: {type: 'SCALE', value: 5}})); } return out;")
else:
    js = ("await figma.loadAllPagesAsync(); const out = {}; const want = " + json.dumps(names) + ";"
          " for (const p of figma.root.children) for (const c of p.children) if (want.includes(c.name) && c.type === 'FRAME')"
          " out[c.name] = figma.base64Encode(await c.exportAsync({format: 'PNG', constraint: {type: 'SCALE', value: 3}})); return out;")
open(D + "tools/_export.js", "w").write(js)
subprocess.run(["python3", "-I", D + "br.py", D + "tools/_export.js", D + "tools/_export.json"], check=True, stdout=subprocess.DEVNULL)
r = json.load(open(D + "tools/_export.json"))
res = r.get("data", {}).get("result")
if not res:
    print(r); sys.exit(1)
for k, v in res.items():
    f = D + "previews/" + ("set_" if sets else "page_") + "".join(c for c in k if c.isalnum()) + ".png"
    open(f, "wb").write(base64.b64decode(v)); print(f)
