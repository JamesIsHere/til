"""Rebuild the README index from the posts on disk.

Reads every topic/slug.md, extracts the title from line 1 and the created
date from git history, and rewrites the section of README.md between the
index markers. Everything outside the markers is left untouched.

Usage:
    python build_index.py
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
README = ROOT / "README.md"
START = "<!-- index starts -->"
END = "<!-- index ends -->"
NON_POSTS = {"README.md", "FORMAT.md"}


def created_date(path):
    """First-commit date for a file, YYYY-MM-DD, or None if uncommitted."""
    out = subprocess.run(
        ["git", "log", "--follow", "--format=%ad", "--date=short", "--",
         str(path.relative_to(ROOT))],
        cwd=ROOT, capture_output=True, text=True,
    ).stdout.split()
    return out[-1] if out else None


def title_of(path):
    first = path.read_text(encoding="utf-8").splitlines()[0]
    return first.lstrip("#").strip()


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    posts = sorted(
        p for p in ROOT.glob("*/*.md")
        if not p.parent.name.startswith(".") and p.name not in NON_POSTS
    )

    by_topic = {}
    for p in posts:
        by_topic.setdefault(p.parent.name, []).append(p)

    lines = [f"{len(posts)} posts across {len(by_topic)} topics.", ""]
    for topic in sorted(by_topic):
        lines.append(f"## {topic}")
        lines.append("")
        entries = []
        for p in by_topic[topic]:
            date = created_date(p)
            entries.append((date or "9999-99-99", p))  # uncommitted sorts first
        entries.sort(reverse=True)
        for date, p in entries:
            rel = f"{p.parent.name}/{p.name}"
            suffix = f" - {date}" if not date.startswith("9999") else ""
            lines.append(f"* [{title_of(p)}]({rel}){suffix}")
        lines.append("")

    text = README.read_text(encoding="utf-8")
    if START not in text or END not in text:
        print(f"ERROR: README.md is missing {START} / {END} markers")
        return 1
    head, rest = text.split(START, 1)
    _, tail = rest.split(END, 1)
    README.write_text(
        head + START + "\n" + "\n".join(lines) + END + tail,
        encoding="utf-8", newline="\n",
    )
    print(f"index rebuilt: {len(posts)} posts, {len(by_topic)} topics")
    return 0


if __name__ == "__main__":
    sys.exit(main())
