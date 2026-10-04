---
title: Render media stays in the local render folder; text goes to the vault sidecar
kind: decision
status: active
date: 2026-10-03
verified: 2026-10-03
stale_after: 2027-04-01
tags: [renders, privacy, vault, sidecar]
summary: "Read before saving clips, contact sheets or verdicts from a real render: what goes where and why media stays out of the vault"
---

# Render media stays in the local render folder; text goes to the vault sidecar

## Context

The S2 prompt keeps clips, sheets and verdicts out of the repo and in the vault sidecar. The vault is a git repository with a GitHub remote, and its whole `.git` folder is 4.2 MB. One 14 s clip at 864x480 is several megabytes, and every reroll adds another.

## Decision

Clips, contact sheets and last frames stay in the local renderer's output folder, outside every repository. The vault sidecar (`projects/cinewright/private/`) gets the text only: take records, filled rubrics, the compiled prompt and a note that names the media folder and the verdicts. The repo gets the lesson only, as a LEARNINGS entry.

## Reasons

The text is the record a later session needs, while the media can be regenerated from prompt, seed and settings. Committing media would grow the vault repository with every reroll. Rejected: Git LFS in the vault (a new dependency for a notes repo).

Related: see also [2026-10-03-field-lessons-cited-without-the-private-source-s-name.md](2026-10-03-field-lessons-cited-without-the-private-source-s-name.md)
