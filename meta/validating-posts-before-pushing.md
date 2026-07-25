# Validating posts against a format contract before pushing

Every post in this repo has its metadata derived from structure — folder name becomes topic, filename becomes slug, line 1 becomes title, first paragraph becomes summary, git history supplies the dates. That only works if every file honors the contract, so a small script checks each post mechanically before it ships.

The contract itself lives in [FORMAT.md](../FORMAT.md). The check is:

```
python validate_post.py meta/validating-posts-before-pushing.md
```

It verifies the path shape (lowercase kebab-case topic and slug), a single problem-phrased `# Title` on line 1, a first paragraph that can stand alone as a summary, body headings starting at `##`, no frontmatter, and no emojis.

Example only — the output below is invented to show the failure format; `git/two-h1s.md` does not exist and nothing in this repo is failing:

```
FAIL git/two-h1s.md
  - line 5: second H1 -> body headings start at ##

0/1 posts pass
```

Run with no arguments it validates every post in the repo, which is exactly the shape a CI job wants: the same script will later run on push via GitHub Actions, turning a local habit into an enforced gate.
