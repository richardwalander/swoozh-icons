"""Figma bridge RPC helper (SwoozhIcons).
Usage: python3 -I br.py script.js [out.json] [--remove]"""
import json, sys, urllib.request

FILE_KEY = "unsaved-mwbu6w4c-q8br717u"


def rpc(tool, params=None, node_ids=None, timeout=600):
    body = json.dumps({"tool": tool, "nodeIds": node_ids or [], "params": params or {}, "fileKey": FILE_KEY}).encode()
    req = urllib.request.Request("http://127.0.0.1:1994/rpc", body, {"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=timeout))


def script(code, allow_remove=False):
    return rpc("run_script", {"code": code, "allowRemove": allow_remove})


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    r = script(open(args[0]).read(), "--remove" in sys.argv)
    s = json.dumps(r, indent=1)
    if len(args) > 1:
        open(args[1], "w").write(s)
    print(s[:6000])
