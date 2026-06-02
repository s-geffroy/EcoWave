#!/usr/bin/env python3
"""Validate a BibTeX file: resolve every DOI, sanity-check ISBNs and URLs.

Usage:
    python3 validate_bib.py references.bib [--strict]

The script parses the .bib file with a deliberately small, regex-based
parser to avoid pulling in heavy dependencies. It then issues HEAD requests
to https://doi.org/<doi> for every entry that has a doi field, validates
ISBN-10 / ISBN-13 checksums, and tries a HEAD on every url field.

Exit code:
    0  if every entry passes
    1  if any entry fails (in --strict mode) or any DOI cannot be resolved
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from typing import Optional

import requests


ENTRY_RE = re.compile(r"@(\w+)\s*\{\s*([^,]+)\s*,(.*?)\n\}", re.DOTALL)
FIELD_RE = re.compile(r"(\w+)\s*=\s*[\{\"]+(.*?)[\}\"]+\s*,?\s*$", re.MULTILINE | re.DOTALL)


@dataclass
class Entry:
    kind: str
    key: str
    fields: dict[str, str] = field(default_factory=dict)


def parse_bib(text: str) -> list[Entry]:
    entries: list[Entry] = []
    for m in ENTRY_RE.finditer(text):
        kind = m.group(1).lower()
        key = m.group(2).strip()
        body = m.group(3)
        fields: dict[str, str] = {}
        for fm in FIELD_RE.finditer(body):
            name = fm.group(1).lower()
            value = re.sub(r"\s+", " ", fm.group(2)).strip().rstrip("},")
            fields[name] = value
        entries.append(Entry(kind=kind, key=key, fields=fields))
    return entries


def check_isbn(isbn: str) -> bool:
    digits = re.sub(r"[-\s]", "", isbn)
    if len(digits) == 10:
        if not re.fullmatch(r"\d{9}[\dXx]", digits):
            return False
        total = sum((10 - i) * (10 if d in "Xx" else int(d)) for i, d in enumerate(digits))
        return total % 11 == 0
    if len(digits) == 13:
        if not digits.isdigit():
            return False
        total = sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(digits))
        return total % 10 == 0
    return False


# Some publishers (JSTOR, APS, AEA, Wiley, Cell Press, Elsevier) block
# bare HEAD requests. The strategy below mimics a real browser well enough
# to get a redirect chain to the publisher landing page, which is what we
# really want to verify.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}


def _http_check(url: str, timeout: float) -> tuple[bool, Optional[int]]:
    """Try HEAD first; fall back to a streaming GET if the server returns 4xx/5xx.

    Streaming GET reads only the headers and closes the connection, so the
    cost is identical to a real HEAD that the server happens to like.
    """
    try:
        r = requests.head(url, headers=HEADERS, allow_redirects=True, timeout=timeout)
        if r.status_code < 400:
            return True, r.status_code
    except requests.RequestException:
        r = None

    try:
        with requests.get(url, headers=HEADERS, allow_redirects=True,
                          timeout=timeout, stream=True) as g:
            return g.status_code < 400, g.status_code
    except requests.RequestException:
        return False, r.status_code if r is not None else None


def check_doi(doi: str, timeout: float = 12.0) -> tuple[bool, Optional[int]]:
    """Validate a DOI through the CrossRef API.

    `doi.org` redirects to publisher landing pages, most of which block
    scrapers (JSTOR, APS, Wiley, Elsevier, ...). CrossRef is the official
    DOI registrar and always returns 200 for a registered DOI, no auth
    required. A 404 from CrossRef means the DOI is not registered, i.e.
    almost certainly malformed or typo'd.
    """
    api = f"https://api.crossref.org/works/{doi.strip()}"
    try:
        r = requests.get(api, headers={"User-Agent": HEADERS["User-Agent"]},
                         timeout=timeout)
        return r.status_code == 200, r.status_code
    except requests.RequestException:
        # CrossRef unreachable: fall back to doi.org redirect chain.
        return _http_check(f"https://doi.org/{doi.strip()}", timeout)


def check_url(url: str, timeout: float = 12.0) -> tuple[bool, Optional[int]]:
    return _http_check(url.strip(), timeout)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a BibTeX file.")
    parser.add_argument("bibfile")
    parser.add_argument("--strict", action="store_true",
                        help="exit 1 if any entry has any failure")
    parser.add_argument("--no-network", action="store_true",
                        help="skip DOI and URL HEAD requests")
    args = parser.parse_args()

    with open(args.bibfile, encoding="utf-8") as f:
        text = f.read()

    entries = parse_bib(text)
    print(f"Parsed {len(entries)} entries from {args.bibfile}.")

    failures: list[str] = []
    for e in entries:
        problems: list[str] = []
        doi = e.fields.get("doi")
        isbn = e.fields.get("isbn")
        url = e.fields.get("url")

        if doi and not args.no_network:
            ok, status = check_doi(doi)
            if not ok:
                problems.append(f"DOI {doi} -> {status}")
        if isbn and not check_isbn(isbn):
            problems.append(f"ISBN checksum invalid: {isbn}")
        if url and not args.no_network:
            ok, status = check_url(url)
            if not ok:
                problems.append(f"URL {url} -> {status}")

        if problems:
            failures.append(f"  - {e.key}: {'; '.join(problems)}")

    if failures:
        print(f"\n{len(failures)} entries with problems:")
        for line in failures:
            print(line)
    else:
        print("\nAll entries pass.")

    return 1 if (failures and args.strict) else 0


if __name__ == "__main__":
    sys.exit(main())
