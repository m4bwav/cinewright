---
title: Dialogue for generated voices
slug: dialogue-for-generated-voices
summary: How many words fit a shot, one speaker per shot, off-screen lines, names a voice model mispronounces, voice strings in the bible, and the dialogue checks in the continuity diff.
tags: [script, dialogue, voice, lip-sync, speech]
last_checked: 2026-11-09
sources: ["Christopher Riley, The Hollywood Standard, 3rd ed., 2021", "https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md", "library film test, 2026-10-07 (maintainer render)", "https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1", "https://kling.ai/quickstart/klingai-video-3-model-user-guide", "Judith Weston, Directing Actors, 25th anniversary ed., 2021", "Michael Rabiger and Mick Hurbis-Cherrier, Directing: Film Techniques and Aesthetics, 6th ed., 2020"]
---

# Dialogue for generated voices

## Rules

- Fit the line to the shot: at most 2.5 words per second after half a second of lead-in (DIALOGUE).
- One speaker per shot, and that speaker in the card's cast. Models lip-sync a face they can see: two speakers swap mouths, and an off-screen speaker's line goes to whoever is in frame (SPEAKERS, OFFSCREEN). Cut to the listener for the answer.
- A line that must stay off screen: keep the speaker out of the cast; `compile` uses the model's voiceover syntax if its card has one (H3: `says in an off-screen voiceover`, visible lips closed), else leaves the line out for the mix.
- Short lines: one sentence, 12 words or fewer, subtext over explanation.
- Words a voice says cleanly: numbers and abbreviations spelled as spoken, no stage directions inside the quotes.
- A rare name that must be said: a respelling in characters.json `pronounce`, taken from the source the owner trusts (audiobook, author), never guessed. It replaces the name inside spoken lines only (PRONOUNCE).
- Each speaker gets a `voice` string in the bible ("low, dry, unhurried"); a voice that must match across shots gets a locked reference (cinewright-voice, entry voice-sheet).
- `tone` follows "says": an adverb or phrase ("under his breath"), never a verb (TONE).
- Silence is a line.
- Each line tries to get something from the listener. Put that verb in the line's `intent` ("pleading with her to stay"); engines that take free-text direction get it in place of an emotion tag (Rabiger ch. 8; Weston ch. 1). Verbs: `kb show performance-verbs`.
- One subtext sentence per scene says what the talk is really about. Voice and face direction come from it, not from the surface words (Rabiger ch. 7, ch. 17).
- No capitals or italics to force stress: that is a line reading. Give the subtext and let the engine place the stress (Weston ch. 1). Untested on TTS.
- Script parentheticals (wryly, voice shaking) are clues: turn them into a verb and a task before compile (Weston ch. 1 ex. 12).

## Numbers

- 2.5 words a second is about 150 a minute. 4 s: up to 8 words; 6 s: 13; 8 s: 18.

## Pitfalls

- Long lines get rushed or cut off at the clip end.
- Overlapping speech comes out garbled; stage alternating singles.
- Respelling is unverified on every model: test it in one short render. If "ka-SEE-uh" is read letter by letter, try "Kasseeuh".

## Verify

- `continuity diff`: every warning in capitals above is fixed or a deliberate choice.
- QC: listen for who says each line (`dialogue-wrong`) and how names sound (`name-misread`).
