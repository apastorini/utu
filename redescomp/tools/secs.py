import pathlib
import re
import sys

p = pathlib.Path(sys.argv[1])
t = p.read_text(encoding="utf-8")
parts = re.split(r"(?m)^(#+ .*)$", t)
cur = "(inicio)"
tot = 0
for x in parts:
    if x.startswith("#"):
        cur = x
    else:
        tot += len(x)
        if len(x) > 400:
            print(len(x), cur[:72])
print("TOTAL", tot)