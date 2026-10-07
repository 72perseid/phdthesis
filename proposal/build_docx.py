#!/usr/bin/env python3
"""
build_docx.py - proposal.md to proposal.docx, without pandoc.

  python3 build_docx.py

Turns the markdown into one HTML file with the figure inside it,
then lets LibreOffice write the Word file. Knows only the markdown
that proposal.md uses: headings, paragraphs, tables, numbered lists,
bold, code and one kind of image line.
"""

from __future__ import annotations

import base64
import html
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).parent

CSS = """
body { font-family: 'Liberation Serif', 'Times New Roman', serif; font-size: 11pt; line-height: 1.25; }
h1 { font-size: 16pt; } h2 { font-size: 13pt; margin-top: 14pt; }
table { border-collapse: collapse; width: 100%; font-size: 9.5pt; }
th, td { border: 1px solid #000; padding: 2pt 4pt; vertical-align: top; }
th { background: #e6e6e6; }
code { font-family: 'Liberation Mono', monospace; font-size: 9.5pt; }
p.caption { font-size: 9.5pt; font-style: italic; }
"""


def inline(text: str) -> str:
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    return text


def cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def convert(md: str) -> str:
    out: list[str] = []
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
        elif m := re.match(r"(#+) (.*)", line):
            n = len(m.group(1))
            out.append(f"<h{n}>{inline(m.group(2))}</h{n}>")
            i += 1
        elif m := re.match(r"!\[(.*)\]\((.*)\)$", line):
            data = base64.b64encode((HERE / m.group(2)).read_bytes()).decode()
            out.append(f'<p><img src="data:image/png;base64,{data}" width="620"></p>')
            out.append(f'<p class="caption">{inline(m.group(1))}</p>')
            i += 1
        elif line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(cells(lines[i]))
                i += 1
            out.append('<table border="1" cellpadding="3" cellspacing="0">')
            out.append("<tr>" + "".join(f"<th>{inline(c)}</th>" for c in rows[0]) + "</tr>")
            for row in rows[2:]:   # rows[1] is the line of dashes
                out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in row) + "</tr>")
            out.append("</table>")
        elif re.match(r"\d+\. ", line):
            out.append("<ol>")
            while i < len(lines) and re.match(r"\d+\. ", lines[i]):
                out.append("<li>" + inline(re.sub(r"^\d+\. ", "", lines[i])) + "</li>")
                i += 1
            out.append("</ol>")
        else:
            para = []
            while i < len(lines) and lines[i].strip() and not re.match(r"#|\||!\[|\d+\. ", lines[i]):
                para.append(inline(lines[i]))
                i += 1
            out.append("<p>" + "<br>".join(para) + "</p>")
    return (f'<!DOCTYPE html><html lang="tr"><head><meta charset="utf-8"><style>{CSS}</style></head>'
            f'<body>{"".join(out)}</body></html>')


def main() -> None:
    page = HERE / "proposal.html"
    page.write_text(convert((HERE / "proposal.md").read_text(encoding="utf-8")), encoding="utf-8")
    subprocess.run(["soffice", "--headless", "--convert-to", "docx:MS Word 2007 XML",
                    "--outdir", str(HERE), str(page)], check=True)
    docx = HERE / "proposal.docx"
    # LibreOffice exits with 0 even when it wrote nothing, for example while the file is open
    if not docx.exists() or docx.stat().st_mtime < page.stat().st_mtime:
        raise SystemExit("proposal.docx was NOT updated. Close the file in Word or LibreOffice and run again.")
    print("written:", docx)


if __name__ == "__main__":
    main()
