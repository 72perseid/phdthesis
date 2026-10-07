#!/usr/bin/env python3
"""
split_papers.py - Split a proceedings-style PDF (e.g. "Kazi Sonuclari Toplantisi")
into one PDF per paper, where each paper describes a single excavation.

Three ways to find where each paper starts:

  auto     (default) Detect title pages from font size: a page whose top region
           contains text set in (almost) the largest font of the whole document
           is treated as the first page of a new paper.  Tunable with
           --title-ratio, --top-frac, --min-pages and --start-regex.
  outline  Use the PDF bookmarks (top-level outline entries).
  ranges   Use a CSV file you wrote (or an edited manifest from --dry-run):
           start,end,title

Typical workflow:
  1. python split_papers.py volume.pdf --dry-run          # look at detected splits
  2. adjust flags, or edit the printed manifest.csv by hand
  3. python split_papers.py volume.pdf -o out/            # write the PDFs
     (or:  --mode ranges --ranges manifest.csv)

Requires poppler-utils (pdftohtml, pdfseparate, pdfunite).  Uses pypdf when it
is installed (faster, single dependency); falls back to poppler otherwise.
"""

from __future__ import annotations

import argparse
import csv
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

try:
    import pypdf  # type: ignore
except ImportError:  # pragma: no cover
    pypdf = None


# ----------------------------------------------------------------------------
# Data structures
# ----------------------------------------------------------------------------

@dataclass
class Line:
    page: int          # 1-based page number
    top: float         # y position from page top (pdftohtml units)
    left: float
    size: float        # font size
    text: str


@dataclass
class Page:
    number: int
    height: float
    width: float
    lines: list[Line] = field(default_factory=list)


@dataclass
class Paper:
    index: int
    start: int         # 1-based, inclusive
    end: int           # 1-based, inclusive
    title: str
    filename: str = ""

    @property
    def n_pages(self) -> int:
        return self.end - self.start + 1


# ----------------------------------------------------------------------------
# Text + font extraction via pdftohtml -xml
# ----------------------------------------------------------------------------

_FONTSPEC_RE = re.compile(r'<fontspec id="(\d+)" size="([\d.]+)"')
_PAGE_RE = re.compile(r'<page number="(\d+)"[^>]*height="([\d.]+)" width="([\d.]+)"')
_TEXT_RE = re.compile(
    r'<text top="([\d.-]+)" left="([\d.-]+)" width="[\d.-]+" height="[\d.-]+" font="(\d+)">(.*?)</text>',
    re.S,
)
_TAG_RE = re.compile(r"<[^>]+>")


def _need(tool: str) -> str:
    path = shutil.which(tool)
    if not path:
        sys.exit(f"error: '{tool}' not found. Install poppler-utils (apt install poppler-utils).")
    return path


def extract_pages(pdf: Path, first: Optional[int] = None, last: Optional[int] = None) -> list[Page]:
    """Run pdftohtml -xml and parse it into Page/Line objects (regex based, tolerant)."""
    _need("pdftohtml")
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp) / "doc"
        cmd = ["pdftohtml", "-xml", "-i", "-q", "-hidden"]
        if first:
            cmd += ["-f", str(first)]
        if last:
            cmd += ["-l", str(last)]
        cmd += [str(pdf), str(base)]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        xml = (base.with_suffix(".xml")).read_text(encoding="utf-8", errors="replace")

    pages: list[Page] = []
    fonts: dict[str, float] = {}
    current: Optional[Page] = None

    # Walk the XML sequentially so that fontspec ids (which are global but
    # declared lazily per page) are known before the text that uses them.
    token_re = re.compile(r"<page [^>]*>|<fontspec [^>]*/>|<text [^>]*>.*?</text>", re.S)
    for m in token_re.finditer(xml):
        tok = m.group(0)
        if tok.startswith("<page"):
            pm = _PAGE_RE.match(tok)
            if pm:
                current = Page(int(pm.group(1)), float(pm.group(2)), float(pm.group(3)))
                pages.append(current)
        elif tok.startswith("<fontspec"):
            fm = _FONTSPEC_RE.match(tok)
            if fm:
                fonts[fm.group(1)] = float(fm.group(2))
        else:
            tm = _TEXT_RE.match(tok)
            if not tm or current is None:
                continue
            raw = html.unescape(_TAG_RE.sub("", tm.group(4)))
            text = re.sub(r"\s+", " ", raw).strip()
            if not text:
                continue
            current.lines.append(
                Line(current.number, float(tm.group(1)), float(tm.group(2)),
                     fonts.get(tm.group(3), 0.0), text)
            )
    return pages


# ----------------------------------------------------------------------------
# Heuristic detection of paper start pages
# ----------------------------------------------------------------------------

def _is_wordy(text: str, min_letters: int = 4) -> bool:
    return sum(ch.isalpha() for ch in text) >= min_letters


def body_font_size(pages: list[Page]) -> float:
    """Most common font size weighted by number of characters (= body text)."""
    weight: Counter = Counter()
    for p in pages:
        for ln in p.lines:
            weight[ln.size] += len(ln.text)
    return weight.most_common(1)[0][0] if weight else 10.0


def typical_title_size(pages: list[Page], skip_pages: set[int], body: float, top_frac: float) -> float:
    """Font size that paper titles are typically set in.

    For every page, take the largest 'wordy' font in the top region if it is
    clearly bigger than the body text; the most common such size across pages
    is the title size.  This is robust against a cover page whose title is set
    in a much larger font than the papers themselves.
    """
    per_page: Counter = Counter()
    for p in pages:
        if p.number in skip_pages:
            continue
        sizes = [ln.size for ln in p.lines
                 if _is_wordy(ln.text) and ln.top <= top_frac * p.height and ln.size >= body * 1.2]
        if sizes:
            per_page[max(sizes)] += 1
    if per_page:
        # Section headings inside papers are often more frequent than paper
        # titles, so do not take the plain mode: take the LARGEST size that
        # recurs on a reasonable number of pages (cover pages occur only once).
        n_pages = max(1, len(pages) - len(skip_pages))
        min_count = max(3, round(0.01 * n_pages))
        recurring = [size for size, cnt in per_page.items() if cnt >= min_count]
        if recurring:
            return max(recurring)
        return per_page.most_common(1)[0][0]
    sizes = [ln.size for p in pages if p.number not in skip_pages
             for ln in p.lines if _is_wordy(ln.text)]
    return max(sizes) if sizes else 0.0


def merge_title_lines(lines: list[Line]) -> str:
    """Join title fragments that sit on the same visual line, then across lines."""
    rows: dict[int, list[Line]] = defaultdict(list)
    for ln in lines:
        rows[int(round(ln.top / 4))].append(ln)  # 4-unit tolerance for same baseline
    out = []
    for key in sorted(rows):
        out.append(" ".join(l.text for l in sorted(rows[key], key=lambda l: l.left)))
    return " ".join(out).strip()


def detect_starts(
    pages: list[Page],
    title_ratio: float,
    top_frac: float,
    min_pages: int,
    start_regex: Optional[str],
    skip_first: int,
    min_size: Optional[float],
) -> list[tuple[int, str]]:
    """Return [(start_page, title), ...]."""
    skip = {p.number for p in pages[:skip_first]}
    body = body_font_size(pages)
    tsize = typical_title_size(pages, skip, body, top_frac)
    threshold = min_size if min_size else max(title_ratio * tsize, body * 1.15)
    print(f"body font {body:g}pt, typical title font {tsize:g}pt, threshold {threshold:.1f}pt", file=sys.stderr)
    rx = re.compile(start_regex, re.I) if start_regex else None

    starts: list[tuple[int, str]] = []
    for p in pages:
        if p.number in skip:
            continue
        cand = [ln for ln in p.lines
                if ln.size >= threshold and ln.top <= top_frac * p.height and _is_wordy(ln.text)]
        if not cand:
            continue
        title = merge_title_lines(cand)
        if rx:
            top_text = " ".join(ln.text for ln in p.lines if ln.top <= top_frac * p.height)
            if not rx.search(title) and not rx.search(top_text):
                continue
        if starts and p.number - starts[-1][0] < min_pages:
            continue  # too close to the previous start: probably a subtitle/section
        starts.append((p.number, title))
    return starts


# ----------------------------------------------------------------------------
# Other split sources
# ----------------------------------------------------------------------------

def starts_from_outline(pdf: Path) -> list[tuple[int, str]]:
    if pypdf is None:
        sys.exit("error: --mode outline needs pypdf (pip install pypdf).")
    reader = pypdf.PdfReader(str(pdf))
    starts = []
    for entry in reader.outline:
        if isinstance(entry, list):
            continue  # nested children: we only split on top level
        try:
            page = reader.get_destination_page_number(entry) + 1
        except Exception:
            continue
        starts.append((page, str(entry.title)))
    starts.sort()
    return starts


def papers_from_ranges(path: Path) -> list[Paper]:
    papers: list[Paper] = []
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.reader(fh):
            if not row or row[0].strip().startswith("#"):
                continue
            cells = [c.strip() for c in row]
            if cells[0].lower() in {"index", "start"}:
                continue  # header line
            # accept either "start,end,title" or the manifest "index,start,end,pages,title,filename"
            if len(cells) >= 5 and cells[0].isdigit() and cells[1].isdigit() and cells[2].isdigit():
                start, end, title = int(cells[1]), int(cells[2]), cells[4]
            else:
                start, end = int(cells[0]), int(cells[1])
                title = cells[2] if len(cells) > 2 else f"pages_{start}-{end}"
            papers.append(Paper(len(papers) + 1, start, end, title))
    return papers


# ----------------------------------------------------------------------------
# Naming
# ----------------------------------------------------------------------------

_TR_MAP = str.maketrans({
    "ı": "i", "İ": "I", "ş": "s", "Ş": "S", "ğ": "g", "Ğ": "G",
    "ç": "c", "Ç": "C", "ö": "o", "Ö": "O", "ü": "u", "Ü": "U",
})


def slugify(text: str, max_len: int = 80) -> str:
    text = text.translate(_TR_MAP)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_")
    if len(text) > max_len:
        text = text[:max_len].rsplit("_", 1)[0]
    return text or "untitled"


def build_papers(starts: list[tuple[int, str]], n_pages: int, keep_front: bool) -> list[Paper]:
    papers: list[Paper] = []
    # Collapse entries that point at the same page (e.g. two bookmarks on one
    # page) and make sure the list is in page order.
    merged: list[tuple[int, str]] = []
    for page, title in sorted(starts, key=lambda s: s[0]):
        if merged and merged[-1][0] == page:
            merged[-1] = (page, f"{merged[-1][1]} / {title}")
        else:
            merged.append((page, title))
    starts = merged
    if not starts:
        return papers
    if keep_front and starts[0][0] > 1:
        papers.append(Paper(0, 1, starts[0][0] - 1, "front matter"))
    for i, (start, title) in enumerate(starts):
        end = starts[i + 1][0] - 1 if i + 1 < len(starts) else n_pages
        papers.append(Paper(i + 1, start, end, title))
    return papers


def assign_filenames(papers: list[Paper]) -> None:
    width = max(2, len(str(len(papers))))
    seen: Counter = Counter()
    for p in papers:
        slug = slugify(p.title)
        seen[slug] += 1
        if seen[slug] > 1:
            slug = f"{slug}_{seen[slug]}"
        p.filename = f"{p.index:0{width}d}_{slug}.pdf"


# ----------------------------------------------------------------------------
# Writing the PDFs
# ----------------------------------------------------------------------------

def write_with_pypdf(pdf: Path, papers: list[Paper], outdir: Path) -> None:
    reader = pypdf.PdfReader(str(pdf))
    for p in papers:
        writer = pypdf.PdfWriter()
        for i in range(p.start - 1, p.end):
            writer.add_page(reader.pages[i])
        writer.add_metadata({"/Title": p.title})
        with open(outdir / p.filename, "wb") as fh:
            writer.write(fh)


def write_with_poppler(pdf: Path, papers: list[Paper], outdir: Path) -> None:
    _need("pdfseparate"); _need("pdfunite")
    with tempfile.TemporaryDirectory() as tmp:
        for p in papers:
            subprocess.run(["pdfseparate", "-f", str(p.start), "-l", str(p.end),
                            str(pdf), f"{tmp}/p-%d.pdf"], check=True, stderr=subprocess.DEVNULL)
            parts = [f"{tmp}/p-{i}.pdf" for i in range(p.start, p.end + 1)]
            if len(parts) == 1:
                shutil.copy(parts[0], outdir / p.filename)
            else:
                subprocess.run(["pdfunite", *parts, str(outdir / p.filename)], check=True,
                               stderr=subprocess.DEVNULL)
            for part in parts:
                os.remove(part)


def write_manifest(papers: list[Paper], path: Path) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["index", "start", "end", "pages", "title", "filename"])
        for p in papers:
            w.writerow([p.index, p.start, p.end, p.n_pages, p.title, p.filename])


def print_table(papers: list[Paper]) -> None:
    print(f"{'#':>3}  {'pages':>9}  {'n':>3}  title")
    for p in papers:
        title = p.title if len(p.title) <= 90 else p.title[:87] + "..."
        print(f"{p.index:>3}  {p.start:>4}-{p.end:<4}  {p.n_pages:>3}  {title}")


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------

def page_count(pdf: Path) -> int:
    if pypdf is not None:
        return len(pypdf.PdfReader(str(pdf)).pages)
    out = subprocess.run([_need("pdfinfo"), str(pdf)], capture_output=True, text=True).stdout
    m = re.search(r"^Pages:\s+(\d+)", out, re.M)
    return int(m.group(1)) if m else 0


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf", type=Path, help="input PDF (proceedings volume)")
    ap.add_argument("-o", "--outdir", type=Path, help="output folder (default: <pdf name>_split/)")
    ap.add_argument("--mode", choices=["auto", "outline", "ranges"], default="auto")
    ap.add_argument("--ranges", type=Path, help="CSV with start,end,title (for --mode ranges)")
    ap.add_argument("--dry-run", action="store_true", help="only print the detected papers")
    ap.add_argument("--manifest", type=Path, help="where to write manifest.csv (default: outdir/manifest.csv)")
    ap.add_argument("--no-front", action="store_true", help="drop pages before the first paper")
    # auto-mode tuning
    ap.add_argument("--title-ratio", type=float, default=0.95,
                    help="a line counts as a title if its font size >= ratio * typical title font size "
                         "(the most common large font at the top of pages; default 0.95)")
    ap.add_argument("--min-size", type=float, help="absolute title font size threshold; overrides --title-ratio")
    ap.add_argument("--top-frac", type=float, default=0.45,
                    help="title must be within this fraction of the page height from the top (default 0.45)")
    ap.add_argument("--min-pages", type=int, default=2,
                    help="a new paper cannot start fewer than this many pages after the previous one (default 2)")
    ap.add_argument("--start-regex", help="only accept a title page if this regex matches its title/top text, "
                                          "e.g. 'KAZI|KAZISI|EXCAVATION'")
    ap.add_argument("--skip-first", type=int, default=0,
                    help="ignore the first N pages (cover, table of contents) when detecting titles")
    args = ap.parse_args(argv)

    pdf: Path = args.pdf
    if not pdf.is_file():
        sys.exit(f"error: {pdf} not found")
    n_pages = page_count(pdf)
    outdir: Path = args.outdir or pdf.with_name(pdf.stem + "_split")

    if args.mode == "ranges":
        if not args.ranges:
            sys.exit("error: --mode ranges needs --ranges FILE")
        papers = papers_from_ranges(args.ranges)
    else:
        if args.mode == "outline":
            starts = starts_from_outline(pdf)
        else:
            pages = extract_pages(pdf)
            starts = detect_starts(pages, args.title_ratio, args.top_frac, args.min_pages,
                                   args.start_regex, args.skip_first, args.min_size)
        papers = build_papers(starts, n_pages, keep_front=not args.no_front)

    if not papers:
        sys.exit("no papers detected. Try a lower --title-ratio, a larger --top-frac, "
                 "or --mode ranges with a hand-written CSV.")
    for p in papers:
        if not (1 <= p.start <= p.end <= n_pages):
            sys.exit(f"error: paper {p.index} has an invalid page range {p.start}-{p.end} (document has {n_pages} pages)")
    assign_filenames(papers)

    print(f"{pdf.name}: {n_pages} pages -> {len(papers)} file(s)")
    print_table(papers)

    if args.dry_run:
        if args.manifest:
            write_manifest(papers, args.manifest)
            print(f"\nmanifest written to {args.manifest} (edit it and re-run with --mode ranges --ranges {args.manifest})")
        return 0

    outdir.mkdir(parents=True, exist_ok=True)
    if pypdf is not None:
        write_with_pypdf(pdf, papers, outdir)
    else:
        write_with_poppler(pdf, papers, outdir)
    manifest = args.manifest or outdir / "manifest.csv"
    write_manifest(papers, manifest)
    print(f"\nwrote {len(papers)} PDF(s) to {outdir}/ and {manifest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
