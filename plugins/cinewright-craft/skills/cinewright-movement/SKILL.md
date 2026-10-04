---
name: cinewright-movement
description: "Movement director for AI video: weight, contact and follow-through, one movement phrase per shot, fights, stunts, and hard subjects (animals, crowds, hands, liquids). Use when an action looks floaty, melts, has broken legs, or needs choreography. Also 'refresh cinewright-movement'."
license: MIT
---

# cinewright-movement

Write every action so a video model renders it with weight and finishes it inside the shot: one phrase per card, a named contact and settle, fights as single exchanges, and hard subjects framed few, large and side-on. Outcome: card actions, start and end states rewritten, and a `continuity diff` with no movement warnings.

`CINE` means `python scripts/cine.py` run from the folder holding this file (run it, never read it). Knowledge: read [references/INDEX.md](references/INDEX.md) once, then `CINE kb show <slug> --section Rules`. Never read the whole folder.

## Step 0: freshness

Read `evergreen.json`. If `contradiction` is set or today is on or after `next_due`, say so in one line, do the task with the current content, then run `evergreen-refresh` if the evergreen plugin is installed. If `tests.failing` is non-empty, say so and run `evergreen-tune` after the task.

## Step 1: one phrase per card

Read each card's `action`. Split any card with two movement ideas; give each a `start_state` and an `end_state`, and counts for repeated moves (`kb show one-phrase-per-shot`).

## Step 2: weight

Rewrite each action as start, verb with speed, contact, settle, plus one thing the weight makes react (`kb show weight-and-contact`). Hits are sold by the reaction shot.

## Step 3: hard subjects

Animals, crowds, animal-drawn vehicles, hands at fine work, liquids, spins: 1-5 subjects, a third of the frame height or more, side-on, each named differently, the mass as one background line (`kb show hard-subjects`). Change the card's size and azimuth if the subject is too small or seen from behind.

## Step 4: fights and stunts

One exchange per card, fighters on fixed sides, take-off and landing in separate cards, a simple camera (`kb show fights-and-stunts`). Weapons go in `bibles/props.json`.

## Step 5: check

Run `CINE continuity diff <project>` and quote its last line. No ONE-ACTION, HARD-SUBJECT or POSITION findings may remain unless a card's `notes` say why. Hand the cards back to cinewright-shots or straight to cinewright-genvideo.

## Output

Each card's old and new action, any card split or reframed, and the diff's last line.

## While working: capture learnings

If the user corrects you, the same error happens twice, or a workaround turns up, add an entry to [LEARNINGS.md](LEARNINGS.md) now (check existing entries first). If it proves a rule here wrong, fix the rule, log it in [CHANGELOG.md](CHANGELOG.md), and set `contradiction` in `evergreen.json`.

## Maintenance

This skill is evergreen (tier `slow`; state in `evergreen.json`). Files: [RESEARCH.md](RESEARCH.md) (findings and search plan), [CHANGELOG.md](CHANGELOG.md), [LEARNINGS.md](LEARNINGS.md), [TESTS.md](TESTS.md) and `evals/evals.json`. How to maintain it, with or without the evergreen plugin: [MAINTENANCE.md](MAINTENANCE.md). Refresh with `evergreen-refresh`, test with `evergreen-test`, fix with `evergreen-tune`.
