---
title: Prop constants
slug: prop-constants
summary: Give every prop that is held or seen close a fixed description in bibles/props.json; the compiler pastes it wherever a card holds the prop, and qc checks its look.
tags: [design, props, bible, continuity]
last_checked: 2026-10-04
sources: ["Vincent LoBrutto, The Filmmaker's Guide to Production Design, 2002", "Field lesson 005, 2026-09-06: chained clips lose character identity and prop continuity"]
---

# Prop constants

## Rules

- A prop the story turns on, or one held in any shot, gets an entry in `bibles/props.json`: `name` (the word cards use in `holding`) and `description`.
- Description: material, size against a hand, shape, color, one wear detail. "a small dented tin matchbox with a hinged lid", not "a matchbox". 200 characters or fewer, one article, no emblems or text unless the story needs them.
- The compiler pastes the description verbatim wherever a card's `holding` names the prop, and stops if it is missing from the prompt. `qc rubric` shows it beside the prop check.
- Props are designed for the period and place in the location bible; a wrong-era object breaks the world faster than a wrong color.
- Hero prop: the one the scene turns on gets an insert (CU or ECU, no cast) and, if it recurs, a clean reference image in its `refs`.
- Keep held props few: one per hand, one per person per shot. Models merge or duplicate small objects passed between hands.
- When a prop changes hands, the giver's `holding_end` and the taker's next `holding` name the same prop; the diff checks it.

## Numbers

- Description 15-200 characters (schema). A prop seen only in a wide shot needs no entry.

## Vocabulary

- hero prop, practical (a prop that works or lights), set dressing, hand prop, insert.

## Pitfalls

- A one-word prop name leaves the model to invent its look each shot: the first render of the example drew a cardboard box where the story meant a tin one.
- "The same box as before" means nothing to a separate generation; paste the description.

## Verify

- `continuity diff` shows no PROP warning about a missing description; each compiled prompt holding the prop contains its description word for word.
