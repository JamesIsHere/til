# Post Format Contract

Every post in this repo follows one contract. The file's path and structure
ARE the metadata — nothing is duplicated into frontmatter, and nothing here
is decorative. Derived fields (title, summary, dates, index entries) are
extracted mechanically, so breaking the contract breaks the machinery.

## The contract

| Element         | Rule                                              | Derives                |
| :-------------- | :------------------------------------------------ | :--------------------- |
| Folder          | one lowercase topic, e.g. `git/`, `python/`       | topic                  |
| Filename        | kebab-case slug + `.md`, e.g. `fix-detached-head.md` | slug, URL           |
| Line 1          | `# Title`, phrased as the problem or task         | title                  |
| First paragraph | stands alone as context — readable with no body   | summary                |
| Rest of file    | freeform: code blocks, output, links, headings    | body                   |
| Git history     | first commit = created, last commit = updated     | dates                  |

## Rules

1. One post per file. One commit per post when possible — commit dates
   drive created/updated, so batching posts into one commit merges their
   timestamps.
2. Never write dates into the file. Git history is the single source of
   truth for time.
3. The first paragraph must survive being lifted out alone (it becomes the
   summary in the index). If it starts with "So then I..." it fails.
4. Headings inside the body start at `##`. Line 1 owns the only `#`.
5. Title is problem-phrased: "Using pysqlite3 on macOS", "Running different
   steps on a schedule" — what you were trying to do, not a clever caption.
6. No emojis. Plain-text markers only (`->`, `[!]`, `OK`).
7. Length is whatever the problem needs. Reference corpus runs roughly
   130-400 words; there is no cap and no floor.
8. New topic folders are cheap — create one when a post doesn't fit an
   existing topic. Don't force-fit.

## Reference

Modeled on [simonw/til](https://github.com/simonw/til). The extraction
mapping (file -> title/summary/dates/index) is fixed so that later layers
(README index generator, search database, site) can be added without
touching any post.
