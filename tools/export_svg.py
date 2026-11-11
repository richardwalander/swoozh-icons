"""Export every component set (both styles) as SVG via the bridge into tools/export/raw.json.
Figma stalls for minutes after ~2 exportAsync calls in one script run, so each set is exported
in its own call (raw SVGs first, then the outlined/flattened font versions)."""
import json, subprocess, sys
D = "/Users/richard/Dev/swoozh-icons/"
raw_tpl = open(D + "tools/export_raw_tpl.js").read()
font_tpl = open(D + "tools/export_font_tpl.js").read()

def call(tpl, i):
    open(D + "tools/_exp.js", "w").write(tpl.replace("__START__", str(i)).replace("__END__", str(i + 1)))
    subprocess.run(["python3", "-I", D + "br.py", D + "tools/_exp.js", D + "tools/_exp.json", "--remove"], check=True, stdout=subprocess.DEVNULL)
    r = json.load(open(D + "tools/_exp.json"))
    if "data" not in r: print(i, r); sys.exit(1)
    return r["data"]["result"]

res, errs, i, total = [], [], 0, None
while total is None or i < total:
    a = call(raw_tpl, i); total = a["total"]
    b = call(font_tpl, i)
    rec = a["out"][0]; rec.update({k: v for k, v in b["out"][0].items() if k != "name"})
    res.append(rec); errs += b["errs"]
    i += 1
    if i % 100 == 0: print(i, total, len(errs), flush=True)
json.dump({"icons": res, "errs": errs}, open(D + "tools/export/raw.json", "w"))
print("done", len(res), "errs", len(errs)); print("\n".join(errs[:30]))
