---
title: Identity strings and bibles
slug: identity-strings
summary: How to write the one verbatim identity string per character, wardrobe and prop strings, and location descriptions that hold across separately generated shots.
tags: [continuity, bibles, identity, wardrobe, props]
last_checked: 2026-10-03
sources: ["Pat P. Miller, Script Supervising and Film Continuity, 3rd ed., 1999", "https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1"]
---

# Identity strings and bibles

## Rules

- One identity string per character: age, build, face, hair, one distinctive mark. No clothes, no mood, no action. It is pasted word for word into every card and prompt; never paraphrased, never shortened.
- Wardrobe is a separate string per scene (`wardrobe.default`, overrides keyed by scene id). A costume change is a new scene key, never an edit inside a card.
- Define each story prop once as a constant string ("a dented tin matchbox"); reuse the same words in every shot. A later shot that shows it again adds "the same size and shape".
- Describe what is there, with absences written inside the description ("flat-topped towers and no domes"). Negative-only lines lose against what the scene suggests.
- Two characters or groups in one shot: add a contrast sentence (who wears what) or their looks bleed into each other.
- Recurring characters get reference images (a turnaround or a clean portrait) before the first render, when the model takes refs.

## Numbers

- Identity string: 15-40 words. Shorter gives the model room to invent; longer crowds out action.

## Pitfalls

- Generic features ("a man with brown hair") give a new person in every clip. Pick one mark a viewer would notice: a scar, a gap tooth, a white streak.
- Incidental attachments (ropes, straps, lanyards) are drawn differently every time. Leave them out unless the story needs them.
- A first frame carries composition into the next clip, not identity. The identity string and refs carry identity.

## Verify

- `continuity diff` reports IDENTITY or WARDROBE when a card's copy differs from the bible by one character.

## Notes

- 2026-10-03: the prop-constant, absence-inside-description, contrast-sentence and first-frame rules generalise field lessons 005 and 013 from the maintainer's local renders (see LEARNINGS).
