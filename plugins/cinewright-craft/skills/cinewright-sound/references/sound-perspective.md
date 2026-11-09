---
title: Sound perspective
slug: sound-perspective
summary: Distance by level and reverb, dialogue held level across shot sizes, phone and radio futz, source music in the next room, and sync held unless marked.
tags: [sound, perspective, reverb, futz, diegetic, sync]
last_checked: 2026-11-09
sources: ["David Bordwell and Kristin Thompson, Film Art: An Introduction, 12th ed., 2019, ch. 7"]
---

# Sound perspective

## Rules

- Distance is heard as level and as the ratio of direct to reflected sound: a far source is quieter and more reverberant, a big empty space echoes where a small room does not (*Film Art* p. 294). Card fields `sound_space: dry | room | hall | exterior` and `distance: near | mid | far`.
- Dialogue level and clarity hold steady when the cut goes from long shot to close-up, and an overlapped line keeps its perspective over the listener. The distance rule applies to effects and source music, not to dialogue (p. 294).
- Phone or radio voice is band-limited, coarser and dry of ambience (futzed); the on-screen speaker stays clear with room tone (pp. 271-272, 295). Mark the line `voice_treatment: phone | radio | speaker`.
- Source music heard from the next room gets less level and a reverb send when the cut moves to listeners there (p. 294).
- A non-diegetic effects layer (a pulse, a stinger no one in the scene hears) is optional and named as such in the cue sheet, so it is not mixed as a room sound.
- Sound out of sync with its picture is an error (`ASYNC`) unless the card says `async: intended` (p. 296); tolerances are in audio-qc.

## Numbers

- Phone band-pass about 300-3400 Hz (the standard telephone band). Next-room music -6 to -10 dB plus reverb: an assumption, set by ear.

## Verify

- A far card in the same space as a near one has lower level or more reverb on effects; dialogue level does not jump at the cut.

Related: see also [sound-layers](sound-layers.md), [audio-qc](audio-qc.md).
