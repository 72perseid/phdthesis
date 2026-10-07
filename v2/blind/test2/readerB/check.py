# -*- coding: utf-8 -*-
import json, re, collections

B = "/media/tugce/ProgramsVS/tez/v2/blind/test2/"
raw = open(B + "paper.txt", encoding="utf-8").read()
pages = raw.split("\f")


def norm(t, dehyph):
    if dehyph:
        t = re.sub(r"-\s*\n\s*", "", t)
    return re.sub(r"\s+", " ", t).strip()


# printed page number of each page chunk
pagetext = {}
for i, pg in enumerate(pages):
    nums = [l.strip() for l in pg.splitlines() if re.fullmatch(r"\s*\d{3}\s*", l)]
    if nums:
        pagetext[int(nums[-1])] = pg
print("pages found:", sorted(pagetext))

KEYS = ["n", "page", "group", "subject", "says", "value", "hedge", "negative", "who", "quote"]
GROUPS = "DOC STRUCT PEOPLE ADMIN WORK PLACE BUILT FIND MEASURE DATE INTERP LAB FIGURE DESCR HISTORY".split()
st = json.load(open(B + "readerB/statements.json", encoding="utf-8"))
bad = 0
for i, s in enumerate(st, 1):
    if list(s.keys()) != KEYS:
        print("KEYS", s.get("n")); bad += 1
    if s["n"] != i:
        print("NUM", s["n"]); bad += 1
    if s["group"] not in GROUPS:
        print("GROUP", s["n"], s["group"]); bad += 1
    if not isinstance(s["negative"], bool) or not isinstance(s["page"], int):
        print("TYPE", s["n"]); bad += 1
    if len(s["quote"]) > 200 or not s["quote"]:
        print("QLEN", s["n"], len(s["quote"])); bad += 1
    if "@" in json.dumps(s, ensure_ascii=False):
        print("EMAIL", s["n"]); bad += 1
    q = norm(s["quote"], False)
    pg = pagetext.get(s["page"], "")
    if not (q in norm(pg, True) or q in norm(pg, False)):
        where = "elsewhere" if (q in norm(raw, True) or q in norm(raw, False)) else "NOWHERE"
        print("QUOTE", s["n"], s["page"], where, repr(s["quote"])); bad += 1
pn = [s["page"] for s in st]
if pn != sorted(pn):
    print("page order not monotone"); bad += 1
print("problems:", bad)
print("total", len(st))
print("groups", dict(collections.Counter(s["group"] for s in st).most_common()))
print("pages", dict(sorted(collections.Counter(pn).items())))
print("hedged", sum(1 for s in st if s["hedge"]), "negative", sum(1 for s in st if s["negative"]))
print("unclear:")
for s in st:
    if "[unclear" in s["says"] or "[unclear" in s["hedge"]:
        print(" ", s["n"], s["page"], s["subject"], "|", s["value"])
