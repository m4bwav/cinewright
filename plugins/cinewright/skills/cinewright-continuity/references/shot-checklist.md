---
title: Per-shot continuity checklist
slug: shot-checklist
summary: The script supervisor's per-shot checks, each diff code with its usual fix, and the checks a person still makes by eye.
tags: [continuity, checklist, diff, script-supervisor]
last_checked: 2026-10-22
sources: ["Pat P. Miller, Script Supervising and Film Continuity, 3rd ed., 1999", "Avril Rowlands, The Continuity Supervisor, 4th ed., 2000"]
---

# Per-shot continuity checklist

## Vocabulary

Diff codes, what each means and the usual fix:

| Code | Means | Fix |
|---|---|---|
| AXIS | camera on side B without a reason | move to side A, or set crosses_axis with an on-screen reason |
| DIRECTION | travel flipped against the scene | use the scene's travel phrase |
| EYELINE | looking the wrong way for the camera side | flip the eyeline, or check positions in scenes.json |
| POSITION | two people swapped frame sides | restore the scene's positions |
| IDENTITY | identity text differs from the bible | paste the bible string again (`cards new` does it) |
| WARDROBE | clothes differ from the bible for this scene | paste the bible string, or add a scene key to the bible |
| PROP | prop in hand differs from the previous shot's end, or has no description in props.json | fix `holding` or `holding_end`; add the prop to props.json |
| 30-DEGREE | jump cut on the same subject | 30+ degrees or 2+ size steps, or cut away |
| TIME, SUN | time of day or sun differs from the scene | use the scene's values |
| ONE-ACTION | the action reads as two actions | split the card |
| DIALOGUE | more words than 2.5 a second fits (warning) | cut the line, or lengthen the shot (cinewright-script) |
| HARD-SUBJECT | crowd or herd words in an EWS or WS (warning) | 1-5 subjects, large and side-on (cinewright-movement) |
| EXIT-ENTRY | enters on the side the last card's exit left by | enter on the other side, or set a cross_reason |
| LOOK-TRACK | a watcher's head turns with the travel, not against it (warning) | swap `eyeline` and `eyeline_end` |
| MIDDLE-SWAP | the middle of a group jumps frame sides (warning) | a two-shot and a single (shots, group-staging) |
| ESTABLISH | a cut-in or insert shows what no earlier card showed (warning) | plant it in a wider card first, or keep it if the mystery is the point |
| POV | unknown `pov`, or a POV shot with no look before it | fix the id; put the looker's card first |
| ROLE | a protection card without a real `protects` | name the card it stands in for |
| AXIS (warning) | `cross_reason` opens with no legal method | start it with a token (axis-and-screen-direction) |

## Rules

- Each card records the start and end state; the next card's start state is the previous take's observed end state, written after the render.
- Props in hand, hand used, glass levels, cigarette length, wet or dry: record in `start_state` or `end_state` when the story touches them.
- A card's positions are checked against the block as it stands after the previous card: the scene's `axis.positions`, moved by every `position_end` before it. A `role: protection` card is checked but never becomes the state the next card starts from.

## Verify

By eye, on the rendered take (the diff cannot see pixels): the face matches the reference, the hands hold the same thing, the light comes from the same side, nothing extra appeared (a sixth finger, a second lamp).
