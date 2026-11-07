import json, base64, sys
D = "/Users/richard/Dev/swoozh-icons/"
r = json.load(open(D + "exp4.json"))["data"]["result"]
for k, v in r.items():
    if k == "detail":
        print(json.dumps(v, indent=1))
        continue
    name = "page_" + "".join(c for c in k if c.isalnum()) + ".png"
    open(D + name, "wb").write(base64.b64decode(v))
    print(D + name)
