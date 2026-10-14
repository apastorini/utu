import os
base = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(base, "raw_text")
dst = os.path.join(base, "clean_text")
os.makedirs(dst, exist_ok=True)

# Map low control codes (artifacts of subset-font encoding) to readable chars
MAP = {
    "\x00": "(", "\x01": ")",
    "\x02": "(", "\x03": ")",
    "\x04": "(", "\x05": ")",
    "\x06": "(", "\x07": ")",
    "\x08": "{", "\x09": "}",   # careful: \x09 is tab; but appears as brace
    "\x0b": "{", "\x0c": "}",
    "\x0e": "(", "\x0f": ")",
    "\x10": "(", "\x11": ")",
    "\x12": "(", "\x13": ")",
    "\x14": "(", "\x15": ")",
    "\x16": "(", "\x17": ")",
    "\x18": "{", "\x19": "}",
    "\x1a": "{", "\x1b": "}",
    "\x1c": "(", "\x1d": ")",
    "\x1e": "(", "\x1f": ")",
}

def clean(t):
    return "".join(MAP.get(c, c) for c in t)

for f in sorted(os.listdir(src)):
    if not f.endswith(".txt"):
        continue
    t = open(os.path.join(src, f), encoding="utf-8", errors="replace").read()
    c = clean(t)
    open(os.path.join(dst, f), "w", encoding="utf-8").write(c)
    print("cleaned", f)
