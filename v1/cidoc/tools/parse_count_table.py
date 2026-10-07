#!/usr/bin/env python3
"""Read a printed cross table of counts (rows = types, columns = attributions)
from `pdftotext -layout` output and check it against its own totals.

Numbers are assigned to columns by the position of their last digit, using the
totals row as the ruler.  Row and column sums must equal the printed totals,
otherwise the table is not accepted.
"""
import re
import sys


def parse(lines, columns, total_label="TOPLAM"):
    rows = []
    for line in lines:
        m = re.match(r"^\s(\S.*?)\s{2,}(\d.*)$", line.rstrip())
        if m:
            label = m.group(1).strip()
            cells = [(n.end() + m.start(2), int(n.group())) for n in re.finditer(r"\d+", m.group(2))]
            rows.append((label, cells))
    total = next(r for r in rows if r[0] == total_label)
    anchors = [pos for pos, _ in total[1]]
    assert len(anchors) == len(columns) + 1, (len(anchors), len(columns))
    table, problems = {}, []
    for label, cells in rows:
        values = {}
        for pos, n in cells:
            i = min(range(len(anchors)), key=lambda k: abs(anchors[k] - pos))
            name = (columns + ["Toplam"])[i]
            if name in values:
                problems.append(f"{label}: two numbers fall in column {name}")
            values[name] = n
        printed = values.pop("Toplam", None)
        if sum(values.values()) != printed:
            problems.append(f"{label}: cells sum to {sum(values.values())}, printed total {printed}")
        table[label] = values
    totals = table.pop(total_label)
    for c in columns:
        s = sum(v.get(c, 0) for v in table.values())
        if s != totals.get(c, 0):
            problems.append(f"column {c}: cells sum to {s}, printed total {totals.get(c, 0)}")
    return table, totals, problems


if __name__ == "__main__":
    text = open(sys.argv[1], encoding="utf-8").read().split("\f")
    page = next(p for p in text if "Tablo 2:" in p)
    cols = ["belirsiz", "doğal", "Epipaleolitik?", "Neo-ÜP?", "Neolitik?", "Neolitik", "OP", "OP-ÜP?", "OP?", "ÜP",
            "ÜP-Epi?", "ÜP?"]
    body = page.split("Toplam", 1)[1].splitlines()
    table, totals, problems = parse(body, cols)
    for k, v in table.items():
        print(f"{k:24s} {v}")
    print("totals", totals)
    print("problems:", problems or "none")
