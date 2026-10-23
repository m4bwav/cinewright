---
title: Pacing and average shot length
slug: pacing
summary: Set pace by average shot length per scene from the style and the scene's job, vary it across the film, and cut to the target length by dropping shots before trimming every shot.
tags: [edit, pacing, rhythm, asl, length]
last_checked: 2026-10-22
sources: ["David Bordwell, The Way Hollywood Tells It, 2006", "Ken Dancyger, The Technique of Film and Video Editing, 6th ed., 2019", "Walter Murch, In the Blink of an Eye, 2nd ed., 2001", "Joseph V. Mascelli, The Five C's of Cinematography, 1965"]
---

# Pacing and average shot length

## Rules

- Average shot length (ASL) = scene length / number of shots. Set a target ASL per scene from its job: quiet and tense scenes long, action and montage short. The style bible's period or director card may give one (cinewright-history).
- Vary pace across the film: a fast scene lands harder after a slow one. Equal ASL everywhere reads as monotone.
- Hold a shot as long as it gives new information or feeling, then cut. A shot's length is set by its content, not by the card's duration; trim a 6 s take to 3.5 s when the beat is done.
- Wider shots need longer to read than close-ups; give a wide 1-2 s more than a close-up of the same moment.
- Over target length: drop whole shots (the weakest beat) before shaving frames from every shot. Under target: hold reactions, never stretch action.
- Rhythm across cuts: cut on beats the scene sets (breaths, steps, line ends). Music cuts on the bar only when the scene is music-driven.
- Deciding where not to cut is most of the work. An overcut film is a tour guide who never stops pointing (after Murch).
- Cross-cutting: give the first shot of each line a little more time. Opposite travel predicts a meeting; cut toward it with shots that get closer and shorter each round (after Mascelli, *The Five C's*).

## Numbers

- ASL, approximate, from published studies (Bordwell 2006): 1930s-1950s Hollywood about 8-11 s; by 2000 typically 3-6 s; action sequences often 2 s or less. Unverified against a database this session.
- Generated cards are 3-8 s; a cut shot often lands at 2-5 s.
- Target length: the brief's `target_seconds`, within ±0.5 s for a short, ±2% for longer work.
- Murch's ballpark: about 25 cuts a minute for a convincing action sequence (ASL about 2.4 s), and 6 or fewer for American dialogue (10 s or more). Fewer cuts in a fight make the viewer watch it rather than take part.

## Pitfalls

- Using every rendered second because rendering was expensive: the most common reason a generated film drags.
- Cutting a slow scene fast to "keep energy" kills the contrast that makes the fast scenes work.
- A scattered rhythm makes the audience hold back; a coherent one lets them give in to the film.

## Verify

- `edit/cut.md` lists each shot's in, out and length, the scene ASL, and the total against `target_seconds`.
