---
title: The compile rule
slug: compile-rule
summary: How a shot card and the bibles become one model's prompt: what goes in, in what order, what is pasted verbatim, and how durations and limits are handled.
tags: [compile, prompts, shot-card, models]
last_checked: 2026-10-04
sources: ["https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1", "https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/video-gen-prompt-guide"]
---

# The compile rule

## Rules

- A card is generator-neutral. The model card's Compile block decides order, dialogue and audio syntax, durations, sizes and limits. `cine.py compile` applies it; never hand-write a prompt for a card that exists.
- Pasted verbatim, never paraphrased: identity strings, wardrobe for the scene, prop descriptions from `bibles/props.json`, location description, the look string, screen-direction and eyeline phrases. The compiler stops if an identity string or a held prop's description is not in the output word for word.
- One shot size, one angle, one move, one action per prompt. Moves get a speed ("slow").
- Durations snap up to the nearest length the model offers; trim the extra in the edit. Some settings force a length (refs, high resolutions): the settings file shows the result.
- Over the word guide: shorten the action or the location, never the identity string.
- Several cards of one scene that fit one generation: `--sequence` writes the people, place, sun and look once, then one timestamp block per card.
- The settings file holds the model's parameters (duration, aspect, resolution, seed, refs, negative terms). Keep it with the prompt; a take record points to both.

## Pitfalls

- A style bible format the model does not offer stops the compile. Change the bible, or pick another model.
- A model card past its `last_checked` plus the skill's interval may be wrong: re-check its volatile claims first.

## Notes

- 2026-10-03: nine model cards. Models without sound drop dialogue and sound with a warning; local models get frame counts and sizes on their grid.
