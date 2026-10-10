import pathlib
import sys

p = pathlib.Path(sys.argv[1])
ls = p.read_text(encoding="utf-8").splitlines()
n = int(sys.argv[2]) if len(sys.argv) > 2 else 0
for i, l in enumerate(ls, 1):
    if l.strip().startswith("```"):
        nxt = ls[i].strip()[:55] if i < len(ls) else ""
        prv = ls[i - 2].strip()[:40] if i >= 2 else ""
        print(f"{i:5d} | {prv:42s} >>> {nxt}")