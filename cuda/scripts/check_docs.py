"""Check local guide links, code fences, and nonempty diagram assets.

Run from cuda/: python3 scripts/check_docs.py
No third-party packages required. Remote URLs are not fetched by this check.
"""
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def main():
    failures = []
    files = sorted(ROOT.rglob("*.md")) + [ROOT.parent / "README.md"]
    links = 0
    for path in files:
        contents = path.read_text()
        fence = None
        prose = []
        for number, line in enumerate(contents.splitlines(), 1):
            marker = re.match(r"^\s*(`{3,}|~{3,})", line)
            if marker:
                current = marker.group(1)
                if fence is None:
                    fence = current
                elif current[0] == fence[0] and len(current) >= len(fence):
                    fence = None
                continue
            if fence is None:
                prose.append((number, line))
        if fence:
            failures.append(f"{path}: unclosed code fence")
        for number, line in prose:
            for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", line):
                parsed = urlsplit(target)
                if parsed.scheme or target.startswith("#"):
                    continue
                links += 1
                resolved = (path.parent / unquote(parsed.path)).resolve()
                if not resolved.exists():
                    failures.append(f"{path}:{number}: missing {target}")
                elif resolved.is_file() and resolved.stat().st_size == 0:
                    failures.append(f"{path}:{number}: empty {target}")
    if failures:
        raise SystemExit("\n".join(failures))
    print(f"PASS: {len(files)} Markdown files, {links} local links, closed code fences")


if __name__ == "__main__":
    main()
