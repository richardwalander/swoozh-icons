"""Export every component set (both styles) as SVG via the bridge into tools/export/raw.json."""
import json, subprocess, sys
D = "/Users/richard/Dev/swoozh-icons/"
tpl = open(D + "tools/export_svg_tpl.js").read()
step = int(sys.argv[1]) if len(sys.argv) > 1 else 100
res, errs, start, total = [], [], 0, None
while total is None or start < total:
    open(D + "tools/_exp.js", "w").write(tpl.replace("__START__", str(start)).replace("__END__", str(start + step)))
    subprocess.run(["python3", "-I", D + "br.py", D + "tools/_exp.js", D + "tools/_exp.json", "--remove"], check=True, stdout=subprocess.DEVNULL)
    r = json.load(open(D + "tools/_exp.json"))
    if "data" not in r: print(r); sys.exit(1)
    r = r["data"]["result"]; total = r["total"]; res += r["out"]; errs += r["errs"]
    start += step; print(start, total, len(errs), flush=True)
json.dump({"icons": res, "errs": errs}, open(D + "tools/export/raw.json", "w"))
print("done", len(res), "errs", len(errs)); print("\n".join(errs[:30]))
