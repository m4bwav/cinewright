---
title: Shared sources copied into skills with a hash header
kind: decision
status: active
date: 2026-10-03
verified: 2026-10-03
stale_after: 2027-04-01
tags: [build, lint, drift, shared]
entities: [cine.py, needs.json]
summary: "Read before editing shared/ or a skill's references, scripts or schemas: how build copies them and how lint catches drift"
---

# Shared sources copied into skills with a hash header

## Context

Each skill must work alone (a claude.ai ZIP holds one skill folder), yet vocabulary, the runtime library and the schemas should have one source.

## Decision

They live once in `shared/` and `cine.py build` copies them into each skill, driven by the skill's `needs.json` (`vocab`, `lib`, `schemas`). A copy is marked by file type:

- Markdown: `<!-- copied from shared/vocab/<file> sha256:<hash>; edit the source -->` on the line after the frontmatter, so the frontmatter stays on line 1 for parsers and Obsidian.
- Python: `# copied from shared/lib/cine.py sha256:<hash>; edit the source` after the shebang.
- JSON: a `"$comment"` key first; `load_schema` drops it before validating.

`cine.py kb lint` renders every planned copy in memory from the current source and compares it byte for byte with the file on disk. A hand edit, a source edit without a rebuild, or a file with a copy header that `needs.json` no longer lists all fail lint. The maintainer CLI (`scripts/cine.py`) imports `shared/lib/cine.py` and adds `kb lint`, `budget`, `zip` and `build`, so the shipped copy carries no maintainer commands. Copies are committed, so a git install needs no build.

## Reasons

Byte comparison catches hand edits that keep the header; the hash in the header is for people. Rejected: symlinks (the Claude directory refuses them); one library per plugin (a one-skill ZIP would lose it); hashing only the header.

Related: builds on [../plans/PLAN.md](../plans/PLAN.md)
