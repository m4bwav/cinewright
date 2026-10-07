---
title: Curate commands live in the maintainer CLI; scrub's private names live outside the repo
kind: decision
status: accepted
date: 2026-10-06
verified: 2026-10-06
stale_after: 2027-04-06
tags: [curate, cli, scrub, budget, public-repo]
summary: "Read before changing cinewright-curate, `cine.py kb due|new|verify|retire` or `cine.py scrub`: why they are maintainer-only, how retire treats cards versus entries, and where the private-names list is kept"
---

# Curate commands in the maintainer CLI; scrub names outside the repo

## Context

S7 builds cinewright-curate (PLAN section 2, dev slice). It needs commands to add, re-verify and retire knowledge entries. The shipped runtime (`shared/lib/cine.py`) is copied into every skill, and genvideo's folder is already yellow (167 KB) on the unanswered runtime budget row. The public scrub needs a list of the maintainer's private project names, which must not ship.

## Decision

- `kb due`, `kb new`, `kb verify` and `kb retire` live in `scripts/cine.py`, the maintainer CLI, not the shipped runtime. Curate works in a repository checkout and ships no script copy, so no skill folder grows.
- `kb due` uses each skill's `interval_days` from `evergreen.json` (14 days for genvideo's model cards). Shared-vocab entries are listed once, by their source.
- `kb verify` requires `--source` (the page read this session), stamps `last_checked`, adds new sources and a dated Notes line; a shared-vocab slug edits the source and rebuilds the copies.
- `kb retire`: a model card keeps its file and gets `status: shut-down` (default) or `deprecated` plus a dated note, because old shot lists still name the model and `compile` already warns on those statuses. Any other entry is deleted, the index rebuilt and a `C-` entry written, and this is refused while another file names the slug. A shared-vocab slug is refused with the steps (needs.json, source, build).
- `cine.py scrub` scans every tracked file (including `ai-docs/`) for drive and home paths, LAN addresses, hostnames, GPU names and emails, plus the names in `--names FILE`. The names file is the vault sidecar's `scrub-names.txt`, never the repository (the list would itself leak the names).

## Reasons

The dev plugin is for maintainers in a checkout, so its tools belong with the other maintainer commands (build, budget, zip); the shipped runtime stays the same size. A retire that keeps cards matches what compile already does. A names list must stay private to be useful.

## Rejected

- Commands in the shipped runtime: would grow all 13 skill folders for a maintainer-only job.
- Deleting a retired model card: breaks `compile` on old projects with no warning.
- A names list in the repo with hashed names: still reveals the count and invites guessing; a private file is simpler.

Related: builds on [2026-10-04-proposed-runtime-budget-row.md](2026-10-04-proposed-runtime-budget-row.md); see also [2026-10-03-field-lessons-cited-without-the-private-source-s-name.md](2026-10-03-field-lessons-cited-without-the-private-source-s-name.md)
