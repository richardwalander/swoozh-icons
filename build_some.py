import re, sys
D = "/Users/richard/Dev/swoozh-icons/"
s = open(D + "build.py").read()
names = sys.argv[1:]
s = s.replace("if only_new and name not in NEW:", f"if name not in {names!r}:")
s = s.replace('only_new = "--new" in sys.argv', 'sys.argv = sys.argv[:1]; only_new = False')
exec(compile(s, "build.py", "exec"))
