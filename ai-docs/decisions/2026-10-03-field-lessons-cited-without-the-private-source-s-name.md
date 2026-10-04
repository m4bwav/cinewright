---
title: Field lessons cited without the private source's name
kind: decision
status: active
date: 2026-10-03
verified: 2026-10-03
stale_after: 2027-04-01
tags: [citations, public-hygiene, learnings]
summary: "Read before citing lessons from private projects in shipped files: the 'field lesson NNN' form and why"
---

# Field lessons cited without the private source's name

## Context

The S1 prompt asked for the four render lessons behind cinewright-continuity to be cited by ID and title. Two rules collide with writing them as `L-005` next to the source's name: AGENTS.md bans naming the maintainer's private projects in shipped files, and the evergreen link lint requires every `L-nnn` in a unit to be a heading in that unit (a foreign ID must be qualified with its unit's name, which would name the private project).

## Decision

Shipped files write "field lesson 005" with the lesson's title, generalised with no private context. The continuity skill holds its own entries L-001 to L-004, one per imported lesson, whose Trigger line quotes the original title and date. The mapping to the source and its lesson IDs is in the vault's private sidecar for cinewright.

## Reasons

Keeps the trail back to the evidence without leaking the source. Rejected: the qualified form `<unit>:L-005` (names the private unit); dropping the numbers (loses the trail).

Related: see also [../plans/PLAN.md](../plans/PLAN.md)
