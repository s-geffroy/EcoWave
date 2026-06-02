#!/usr/bin/env python3
"""Cross-check \\cite{} keys in a LaTeX project against entries in a .bib file.

Usage:
    python3 check_bib_consistency.py cycles_refuted.tex references.bib

The script reads the main .tex file and every file referenced through
\\input{...}, harvests all \\cite{...} / \\citet{...} / \\citep{...} keys,
parses the .bib file for entry keys, and reports:
    (a) cite keys with no matching .bib entry  -> citation orphans
    (b) .bib entries that are never cited      -> bibliography orphans

Exit code is 1 if any cite-orphan is found, 0 otherwise. Bibliography
orphans are reported but do not by themselves trigger a non-zero exit
code (a project may legitimately keep auxiliary entries).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


CITE_RE = re.compile(r"\\cite[a-z]*\*?(?:\[[^\]]*\])?\s*\{([^}]+)\}")
INPUT_RE = re.compile(r"\\input\s*\{([^}]+)\}")
BIB_KEY_RE = re.compile(r"@\w+\s*\{\s*([^,\s]+)")


def gather_tex_files(root: Path) -> list[Path]:
    seen: set[Path] = set()
    queue: list[Path] = [root]
    while queue:
        p = queue.pop()
        if p in seen or not p.exists():
            continue
        seen.add(p)
        text = p.read_text(encoding="utf-8")
        for m in INPUT_RE.finditer(text):
            target = m.group(1).strip()
            if not target.endswith(".tex"):
                target += ".tex"
            queue.append(p.parent / target)
    return sorted(seen)


def gather_cite_keys(files: list[Path]) -> set[str]:
    keys: set[str] = set()
    for p in files:
        for m in CITE_RE.finditer(p.read_text(encoding="utf-8")):
            for k in m.group(1).split(","):
                k = k.strip()
                if k:
                    keys.add(k)
    return keys


def gather_bib_keys(bib: Path) -> set[str]:
    return {m.group(1).strip() for m in BIB_KEY_RE.finditer(bib.read_text(encoding="utf-8"))}


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: check_bib_consistency.py <main.tex> <references.bib>", file=sys.stderr)
        return 2
    main_tex = Path(sys.argv[1]).resolve()
    bib = Path(sys.argv[2]).resolve()

    tex_files = gather_tex_files(main_tex)
    cite_keys = gather_cite_keys(tex_files)
    bib_keys = gather_bib_keys(bib)

    orphans_cite = sorted(cite_keys - bib_keys)
    orphans_bib = sorted(bib_keys - cite_keys)

    print(f"Scanned {len(tex_files)} .tex files; found {len(cite_keys)} cite keys.")
    print(f"Parsed {len(bib_keys)} entries from {bib.name}.")

    if orphans_cite:
        print(f"\n{len(orphans_cite)} citation orphan(s) (cited but no .bib entry):")
        for k in orphans_cite:
            print(f"  - {k}")
    else:
        print("\nNo citation orphans.")

    if orphans_bib:
        print(f"\n{len(orphans_bib)} bibliography orphan(s) (in .bib but not cited):")
        for k in orphans_bib:
            print(f"  - {k}")

    return 1 if orphans_cite else 0


if __name__ == "__main__":
    sys.exit(main())
