#!/usr/bin/env python3
"""Check primer links, Markdown structure, and GFM table column counts."""

from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def prose_lines(path):
    """Yield non-code lines; also catch an unclosed fenced code block."""
    fence = None
    for number, line in enumerate(path.read_text().splitlines(), 1):
        match = FENCE.match(line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            yield number, ""  # A code fence breaks a table or prose block.
        elif fence is None:
            yield number, line
    if fence:
        raise ValueError(f"{path}: unclosed code fence")


def heading_ids(path):
    """GitHub-style slugs for the plain/inline-code headings used here."""
    slugs = set()
    counts = {}
    for _, line in prose_lines(path):
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        slug = re.sub(r"[^\w\- ]", "", match.group(1).lower()).replace(" ", "-")
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        slugs.add(f"{slug}-{count}" if count else slug)
    return slugs


def main():
    repo = ROOT.parent
    entrypoints = [repo / "README.md", repo / "verilong/README.md",
                   repo / "verilong/cpu/README.md", repo / "verilong/cpu/intro.md"]
    files = sorted(ROOT.rglob("*.md")) + entrypoints
    failures = []
    links = 0
    for path in files:
        details = 0
        table_columns = None
        try:
            for number, line in prose_lines(path):
                details += line.count("<details>") - line.count("</details>")
                if details < 0:
                    failures.append(f"{path}:{number}: unmatched </details>")
                if path.is_relative_to(ROOT) and line.startswith("|"):
                    columns = len(re.split(r"(?<!\\)\|", line)) - 2
                    if table_columns is not None and columns != table_columns:
                        failures.append(f"{path}:{number}: {columns} table columns; expected {table_columns}")
                    table_columns = columns
                else:
                    table_columns = None
                for target in LINK.findall(line):
                    parsed = urlsplit(target)
                    if parsed.scheme or parsed.netloc:
                        continue
                    links += 1
                    destination = (path.parent / unquote(parsed.path)).resolve()
                    if not destination.exists():
                        failures.append(f"{path}:{number}: missing {target}")
                    elif destination.is_file() and destination.stat().st_size == 0:
                        failures.append(f"{path}:{number}: empty {target}")
                    elif parsed.fragment and destination.suffix == ".md":
                        if unquote(parsed.fragment) not in heading_ids(destination):
                            failures.append(f"{path}:{number}: missing heading in {target}")
            if details:
                failures.append(f"{path}: unclosed answer panel")
        except ValueError as error:
            failures.append(str(error))
    if failures:
        raise SystemExit("\n".join(failures))
    print(f"PASS: {len(files)} Markdown files, {links} local links; fences, panels, tables, and linked headings")


if __name__ == "__main__":
    main()
