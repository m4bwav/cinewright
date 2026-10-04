---
title: Dialogue for generated voices
slug: dialogue-for-generated-voices
summary: How many words fit a shot, one speaker per shot, lines a voice model says cleanly, voice strings in the bible, and the DIALOGUE check in the continuity diff.
tags: [script, dialogue, voice, lip-sync, speech]
last_checked: 2026-10-04
sources: ["Christopher Riley, The Hollywood Standard, 3rd ed., 2021", "https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1", "https://kling.ai/quickstart/klingai-video-3-model-user-guide"]
---

# Dialogue for generated voices

## Rules

- Fit the line to the shot: words at most 2.5 per second of shot, after half a second of lead-in. `continuity diff` warns DIALOGUE when a card holds more.
- One speaker per shot. Lines from two people in one clip often come out in the wrong mouth; cut to the listener for the answer.
- Short lines: one sentence, 12 words or fewer. Subtext over explanation: a line says what the person wants, not what they feel.
- Write words the voice says cleanly: spell numbers and abbreviations as spoken ("twelve", "doctor"), avoid rare names and words that look alike in spelling, no stage directions inside the quotes.
- Give each speaking character a `voice` string in the character bible (age, pitch, pace, texture: "low, dry, unhurried"); genvideo compiles it into every line on models that take it.
- Delivery notes go in the card's dialogue `tone`, one or two words ("quietly", "breathless"). They become the parenthetical.
- Off-screen lines and voice over: put them in the card's `sound` as a voice description, or lay a recorded line in the mix; models lip-sync whoever is on screen.
- Silence is a line. A beat that turns on a look needs no dialogue.

## Numbers

- 2.5 words a second is about 150 words a minute, a clear conversational pace. Generated voices rush lines that are too long and pad short ones (field observation, unverified per model).
- 4 s shot: up to 8 words. 6 s: up to 13. 8 s: up to 18.

## Pitfalls

- Long lines push the model to speed up speech or cut it off at the clip end.
- Overlapping speech and shouting matches come out garbled; stage them as alternating singles.

## Verify

- `continuity diff` shows no DIALOGUE warning; every speaker has a `voice` in the bible.
