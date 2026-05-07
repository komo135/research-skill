"""lit_fetch.py — Batch fetch literature from arxiv and Semantic Scholar.

Per D-21 (`.rebuild/DECISIONS.md`): API source is arxiv + Semantic Scholar.
SSRN is not scrape-friendly; users provide manual SSRN URLs to extract metadata.

Output is appended to `<project>/literature/papers.md` in the format
defined by `assets/shared/papers.md.template`.

Usage:
    python scripts/lit_fetch.py --project-dir <path> --query "measurement reliability" --max-results 10
    python scripts/lit_fetch.py --project-dir <path> --arxiv-ids 2310.12345 2401.67890
    python scripts/lit_fetch.py --project-dir <path> --ssrn-url https://papers.ssrn.com/sol3/papers.cfm?abstract_id=...

Sources:
    - arxiv: arxiv.org Atom API (no key required)
      https://export.arxiv.org/api/query
    - Semantic Scholar: https://api.semanticscholar.org/graph/v1/paper/search
      (rate-limited without key; for batch, request a key)

Dependencies:
    Standard library only (urllib, xml.etree.ElementTree, json).
    Network access required.

Exit codes:
    0: papers fetched and appended
    1: network error / API error
    2: setup error (project_dir invalid, no query and no ids)
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class Paper:
    title: str
    authors: list[str]
    year: str
    venue: str
    url: str
    abstract: str
    citations: int | None = None
    source: str = "unknown"  # "arxiv" | "semantic_scholar" | "ssrn_manual"


# ---------------------------------------------------------------------------
# arxiv fetch
# ---------------------------------------------------------------------------

ARXIV_NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}


def fetch_arxiv_query(query: str, max_results: int) -> list[Paper]:
    """Search arxiv with a query string."""
    scoped = query
    params = urllib.parse.urlencode({
        "search_query": scoped,
        "start": "0",
        "max_results": str(max_results),
        "sortBy": "relevance",
        "sortOrder": "descending",
    })
    url = f"https://export.arxiv.org/api/query?{params}"
    return _fetch_arxiv_url(url)


def fetch_arxiv_by_ids(ids: list[str]) -> list[Paper]:
    """Fetch specific arxiv ids."""
    params = urllib.parse.urlencode({
        "id_list": ",".join(ids),
        "max_results": str(len(ids)),
    })
    url = f"https://export.arxiv.org/api/query?{params}"
    return _fetch_arxiv_url(url)


def _fetch_arxiv_url(url: str) -> list[Paper]:
    try:
        with urllib.request.urlopen(url, timeout=20) as resp:
            data = resp.read()
    except Exception as e:
        raise RuntimeError(f"arxiv fetch failed: {e}") from e

    root = ET.fromstring(data)
    papers = []
    for entry in root.findall("atom:entry", ARXIV_NS):
        title = (entry.findtext("atom:title", "", ARXIV_NS) or "").strip().replace("\n", " ")
        summary = (entry.findtext("atom:summary", "", ARXIV_NS) or "").strip().replace("\n", " ")
        published = (entry.findtext("atom:published", "", ARXIV_NS) or "")[:4]
        link = ""
        for a in entry.findall("atom:link", ARXIV_NS):
            if a.attrib.get("type") == "text/html" or a.attrib.get("rel") == "alternate":
                link = a.attrib.get("href", "")
                break
        if not link:
            link = entry.findtext("atom:id", "", ARXIV_NS) or ""

        authors = [
            (a.findtext("atom:name", "", ARXIV_NS) or "").strip()
            for a in entry.findall("atom:author", ARXIV_NS)
        ]
        papers.append(Paper(
            title=title,
            authors=[a for a in authors if a],
            year=published,
            venue="arXiv",
            url=link,
            abstract=summary,
            source="arxiv",
        ))
    return papers


# ---------------------------------------------------------------------------
# Semantic Scholar fetch
# ---------------------------------------------------------------------------


def fetch_semantic_scholar(query: str, max_results: int) -> list[Paper]:
    params = urllib.parse.urlencode({
        "query": query,
        "limit": str(max_results),
        "fields": "title,authors,year,venue,abstract,citationCount,url,externalIds",
    })
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?{params}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "research-skill/lit_fetch.py"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        raise RuntimeError(f"semantic scholar fetch failed: {e}") from e

    papers = []
    for item in data.get("data", []):
        authors = [a.get("name", "") for a in (item.get("authors") or [])]
        papers.append(Paper(
            title=(item.get("title") or "").strip(),
            authors=[a for a in authors if a],
            year=str(item.get("year") or ""),
            venue=item.get("venue") or "",
            url=item.get("url") or "",
            abstract=(item.get("abstract") or "").strip(),
            citations=item.get("citationCount"),
            source="semantic_scholar",
        ))
    return papers


# ---------------------------------------------------------------------------
# SSRN manual extraction
# ---------------------------------------------------------------------------


def fetch_ssrn_manual(url: str) -> Paper:
    """Fetch a single SSRN URL and extract minimal metadata via simple HTML scrape."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 research-skill"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        raise RuntimeError(f"ssrn fetch failed: {e}") from e

    # Look for <title>, meta tags
    import re
    title = ""
    title_m = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    if title_m:
        title = title_m.group(1).strip().replace("\n", " ")[:300]

    abstract = ""
    abs_m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html, re.IGNORECASE)
    if abs_m:
        abstract = abs_m.group(1).strip()[:1000]

    return Paper(
        title=title,
        authors=[],
        year="",
        venue="SSRN",
        url=url,
        abstract=abstract,
        citations=None,
        source="ssrn_manual",
    )


# ---------------------------------------------------------------------------
# Output formatting (papers.md)
# ---------------------------------------------------------------------------


def format_paper_md(p: Paper) -> str:
    """Format one paper as a markdown section per assets/shared/papers.md.template."""
    authors_str = ", ".join(p.authors) if p.authors else "<unknown>"
    year_str = p.year or "<year>"
    citations_str = str(p.citations) if p.citations is not None else "(unknown)"
    abstract_short = (p.abstract or "")[:600]
    return f"""## [{authors_str} ({year_str})] {p.title}

- **venue**: {p.venue}
- **citations**: {citations_str}
- **URL / DOI**: {p.url}
- **source**: {p.source}
- **main claim** (abstract excerpt): {abstract_short}{'...' if len(p.abstract) > 600 else ''}
- **method**:
  - model type: <REPLACE: math / classical ML / DL / RL / foundation>
  - data: <REPLACE: universe, period, frequency>
  - validation: <REPLACE: split, k-fold, holdout, replication design>
- **results**:
  - main metric: <REPLACE>
- **limitations**:
  - <REPLACE>
- **relation to this research**: <REPLACE: use / compare / differentiate from / refute>
"""


def append_papers(papers: list[Paper], project_dir: Path) -> None:
    lit_dir = project_dir / "literature"
    lit_dir.mkdir(parents=True, exist_ok=True)
    papers_md = lit_dir / "papers.md"

    existing = ""
    if papers_md.exists():
        existing = papers_md.read_text(encoding="utf-8").rstrip() + "\n\n"

    new_sections = "\n".join(format_paper_md(p) for p in papers)
    papers_md.write_text(existing + new_sections, encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--project-dir", required=True, type=Path)
    p.add_argument("--query", default=None, help="search query (used for arxiv + semantic scholar)")
    p.add_argument("--arxiv-ids", nargs="*", default=[], help="explicit arxiv IDs (e.g. 2310.12345)")
    p.add_argument("--ssrn-url", default=None, help="SSRN paper URL for manual scrape")
    p.add_argument("--max-results", type=int, default=10)
    p.add_argument("--source", choices=["arxiv", "semantic_scholar", "both"], default="both")
    args = p.parse_args()

    if not args.project_dir.exists():
        print(f"ERROR: project_dir not found: {args.project_dir}", file=sys.stderr)
        sys.exit(2)
    if not (args.query or args.arxiv_ids or args.ssrn_url):
        print("ERROR: provide at least one of --query, --arxiv-ids, --ssrn-url", file=sys.stderr)
        sys.exit(2)

    all_papers: list[Paper] = []

    try:
        if args.arxiv_ids:
            papers = fetch_arxiv_by_ids(args.arxiv_ids)
            print(f"arxiv (by IDs): {len(papers)} papers")
            all_papers.extend(papers)

        if args.query and args.source in ("arxiv", "both"):
            papers = fetch_arxiv_query(args.query, args.max_results)
            print(f"arxiv (query '{args.query}'): {len(papers)} papers")
            all_papers.extend(papers)

        if args.query and args.source in ("semantic_scholar", "both"):
            papers = fetch_semantic_scholar(args.query, args.max_results)
            print(f"semantic_scholar: {len(papers)} papers")
            all_papers.extend(papers)

        if args.ssrn_url:
            paper = fetch_ssrn_manual(args.ssrn_url)
            print(f"ssrn (manual): {paper.title[:80]}")
            all_papers.append(paper)
    except RuntimeError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    # Deduplicate by title (best-effort)
    seen_titles = set()
    unique = []
    for p in all_papers:
        key = p.title.lower().strip()
        if key not in seen_titles and key:
            seen_titles.add(key)
            unique.append(p)

    print(f"\nTotal unique papers: {len(unique)}")
    append_papers(unique, args.project_dir)
    print(f"Appended to {args.project_dir}/literature/papers.md")
    print()
    print("Each paper has <REPLACE> markers for: model type / data / validation / "
          "results / limitations / relation to this research. Fill these per the "
          "PR/FAQ scope.")


if __name__ == "__main__":
    main()
