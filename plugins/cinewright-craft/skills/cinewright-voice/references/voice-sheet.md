---
title: Voice sheet
slug: voice-sheet
summary: The casting fields that pin a character's voice (age, gender, pitch, pace, timbre, accent, energy, attitude, quirks), the short prompt string, and the pronunciation list.
tags: [voice, casting, character, sheet]
last_checked: 2026-10-07
sources: ["https://gdcvault.com/play/1012430/Character-Voices-Conceptualization-Casting-Recording", "https://gdcvault.com/play/1023353/Anatomy-of-Great-Voice-Over", "https://cmosshoptalk.com/2019/10/15/preparing-an-audiobook-for-a-narrator-who-isnt-you/"]
---

# Voice sheet

## Rules

- One sheet per speaking character, written before any audio. Animation, game and audiobook casting all start here: most voice problems are made before recording (GDC 2010).
- Fill every required field with one or two plain words; a field left vague is where the voice drifts.
- Pick a reference point for people (a known voice it sits near) in `reference_point`; never put a real person's name in a design prompt or a video prompt.
- Contrast the cast: two characters who share a scene differ on at least two of pitch, pace, timbre, accent.
- The short `voice` string in characters.json is three to six words from the sheet ("low, dry, unhurried"). It goes verbatim into every prompt; change it only before the first render.
- Names and invented words go in characters.json `pronounce` (word to respelling); every engine reads the same respelling.

## Vocabulary

| field | words to choose from |
|---|---|
| age | child, teen, twenties, thirties, middle-aged, sixties, elderly |
| pitch | very low, low, mid, high; steady or wide-ranging |
| pace | slow, unhurried, measured, brisk, rapid; words a minute if known |
| timbre | warm, dry, bright, dark, gravelly, breathy, nasal, smooth, raspy, thin, full |
| resonance | chest, mouth, head |
| accent | region and class, light or strong |
| energy | contained, calm, alert, intense, weary |
| attitude | warm, mocking, guarded, kind, cold, wry |
| quirks | one habit at most: a clipped ending, a laugh before answers |

## Pitfalls

- Adjectives that only describe emotion ("angry voice"): emotion changes per line; the sheet describes the person.
- A different voice string per shot: the video model reinvents the voice each time.
