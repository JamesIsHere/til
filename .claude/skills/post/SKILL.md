---
name: post
description: Write and publish a TIL post - draft from the user's raw material, validate against FORMAT.md, commit, push. Use whenever the user wants to capture something they learned as a post.
---

# Publish a TIL post

Turn raw material (a story, a pasted error, a rough explanation) into a
published post. The contract lives in FORMAT.md at the repo root — read it
before drafting if it is not already in context.

## Steps

1. Draft. From the user's material, produce:
   - Topic: pick an existing topic folder if one fits (`ls` the repo root);
     otherwise propose a new lowercase kebab-case topic.
   - Filename: kebab-case slug derived from the title.
   - Title: problem-phrased — what the user was trying to do.
   - First paragraph: must stand alone as a summary of the situation.
   - Body: freeform, headings start at ##, real commands and output
     preferred over prose descriptions. No emojis. Never write dates into
     the file.
2. Show the user the full draft and proposed path (`topic/slug.md`).
   Wait for approval or edits. Do not write the file before approval.
3. Write the file, then validate:

       python validate_post.py topic/slug.md

   Fix any FAIL and re-run until OK. Never skip or weaken the validator.
4. Commit just that file — one post per commit, so git history dates stay
   per-post. Commit message: the post title.
5. Push. Confirm the push was accepted (`main -> main` in the output) and
   give the user the public URL:
   `https://github.com/JamesIsHere/til/blob/main/topic/slug.md`

## Rules

- One post per invocation. If the user's material contains two learnings,
  say so and split into two runs.
- The user's voice wins: keep their phrasing where it works; tighten,
  don't rewrite.
- If validation and the user's approved draft conflict (e.g. they approved
  an emoji), surface the conflict instead of silently changing the draft.
