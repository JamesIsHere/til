"""Validate TIL posts against the contract in FORMAT.md.

Usage:
    python validate_post.py                 # validate every post in the repo
    python validate_post.py git/foo.md ...  # validate specific files

Exit code 0 = all posts pass, 1 = at least one violation.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
NON_POSTS = {"README.md", "FORMAT.md"}

TOPIC_RE = re.compile(r"^[a-z0-9-]+$")
SLUG_RE = re.compile(r"^[a-z0-9-]+\.md$")

EMOJI_RANGES = [
    (0x1F300, 0x1FAFF),  # pictographs, emoticons, symbols
    (0x1F1E6, 0x1F1FF),  # regional indicators (flags)
    (0x2600, 0x27BF),    # misc symbols + dingbats
    (0xFE0F, 0xFE0F),    # variation selector (emoji presentation)
]


def find_emoji(text):
    for ch in text:
        cp = ord(ch)
        for lo, hi in EMOJI_RANGES:
            if lo <= cp <= hi:
                return ch
    return None


def first_paragraph(lines):
    """Return the first paragraph after the title, or None."""
    para = []
    for line in lines[1:]:
        if not line.strip():
            if para:
                break
            continue
        para.append(line.strip())
    return " ".join(para) if para else None


def validate(path):
    errors = []
    topic, name = path.parent.name, path.name

    if not TOPIC_RE.match(topic):
        errors.append(f"topic folder '{topic}' must be lowercase kebab-case")
    if not SLUG_RE.match(name):
        errors.append(f"filename '{name}' must be lowercase kebab-case .md")

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    if not lines:
        return ["file is empty"]
    if lines[0].startswith("---"):
        errors.append("no frontmatter: path and git history are the metadata")
    if not re.match(r"^# \S", lines[0]):
        errors.append("line 1 must be '# Title'")

    # Only line 1 may be an H1; track code fences so shell comments don't trip it.
    in_fence = False
    for i, line in enumerate(lines[1:], start=2):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        elif not in_fence and re.match(r"^# ", line):
            errors.append(f"line {i}: second H1 — body headings start at ##")

    para = first_paragraph(lines)
    if para is None:
        errors.append("no first paragraph after the title")
    elif re.match(r"^(#|```|[-*>|]|\d+\.)", para):
        errors.append("first paragraph must be prose (it becomes the summary), "
                      "not a heading, list, quote, table, or code block")
    elif len(para) < 40:
        errors.append("first paragraph too short to stand alone as a summary")

    emoji = find_emoji(text)
    if emoji:
        errors.append(f"contains emoji U+{ord(emoji):04X} — plain-text markers only")

    return errors


def main(argv):
    # Windows consoles default to cp1252, which can't print em-dashes or emoji.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if argv:
        posts = [Path(a).resolve() for a in argv]
    else:
        posts = sorted(
            p for p in ROOT.glob("*/*.md")
            if not p.parent.name.startswith(".") and p.name not in NON_POSTS
        )
    if not posts:
        print("no posts found")
        return 0

    failed = 0
    for post in posts:
        errors = validate(post)
        rel = post.relative_to(ROOT) if post.is_relative_to(ROOT) else post
        if errors:
            failed += 1
            print(f"FAIL {rel}")
            for e in errors:
                print(f"  - {e}")
        else:
            print(f"OK   {rel}")
    print(f"\n{len(posts) - failed}/{len(posts)} posts pass")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
