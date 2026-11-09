---
title: Pacing and average shot length
slug: pacing
summary: Set pace by average shot length per scene from the style and the scene's job, vary it across the film, and cut to the target length by dropping shots before trimming every shot.
tags: [edit, pacing, rhythm, asl, length]
last_checked: 2026-11-09
sources: ["Bruce Block, The Visual Story, 3rd ed., 2021, ch. 8 (Rhythm)", "David Bordwell, The Way Hollywood Tells It, 2006", "Ken Dancyger, The Technique of Film and Video Editing, 6th ed., 2019", "Walter Murch, In the Blink of an Eye, 2nd ed., 2001", "Joseph V. Mascelli, The Five C's of Cinematography, 1965", "David Bordwell, A Labyrinth of Linkages, 2013", "David Mamet, On Directing Film, 1991", "Eric Sherman, Directing the Film, 1976"]
---

# Pacing and average shot length

## Rules

- Average shot length (ASL) = scene length / number of shots. Set a target ASL per scene from its job: quiet and tense scenes long, action and montage short. The style bible's period or director card may give one (cinewright-history).
- Vary pace across the film: a fast scene lands harder after a slow one. Equal ASL everywhere reads as monotone.
- Hold a shot as long as it gives new information or feeling, then cut. A shot's length is set by its content, not by the card's duration; trim a 6 s take to 3.5 s when the beat is done.
- A wide needs 1-2 s more to read than a close-up of the same moment.
- Over target length: drop whole shots (the weakest beat) before shaving frames from every shot. Under target: hold reactions, never stretch action.
- Rhythm across cuts: cut on beats the scene sets (breaths, steps, line ends); on the bar only when music drives the scene. Deciding where not to cut is most of the work (after Murch).
- Late in, early out: trim each scene's head to its first essential beat and its tail to `ends_when`. Cards before beat 1 or after `ends_when` are trim candidates (Mamet p. 31; Ashby in Sherman p. 250).
- Dialogue tempo rises and falls: slower open, faster middle, slower wind-down. Shot lengths and line gaps follow it (Bordwell, *Film Art* p. 281).
- Accelerating run for a climax: each shot loses a fixed number of frames (Hitchcock: 20 frames down to 8, 2 a step), then one or two equal punctuation shots, then a long held wide as a pause (*Film Art* p. 224). Cut it from one or two long takes.
- One movement of one character in three or more cards reads choppy (Insomnia: five shots to leave a plane). Prefer one tracking or panning card; one designed shot with a focus pull beats a face plus its object (*Labyrinth* pp. 15-17).
- No filler cards: drop extra establishing aerials and people entering or leaving buildings once the scene has its establishing card (*Labyrinth* p. 16).
- The edit room cannot add interest. A weak beat in the assembly is marked `REPLAN` (a new shot pair in the plan), not given a longer hold or music (Mamet, conclusion).
- A cut's beat is as strong as the visual contrast between its two shots. Quiet stretches cut between similar shots; intense ones between shots that differ in size, space, tone, colour or movement (after Block, *The Visual Story*).
- Alternate continuous events (one long take, or one multi-shot generation) with fragmented ones (coverage): each makes the other stronger, and an overcut film gains from one long take.
- Pick the film's flow-line and write it in `visual_structure.flow`: `peaks` (big rises and drops), `staccato` (short sharp beats, comedy) or `undulating` (slow swells).
- Cross-cutting: the first shot of each line gets a little more time; toward a meeting, shots get closer and shorter each round (after Mascelli). Strands and clocks: entry time-and-order.

## Numbers

- ASL (Bordwell 2006, approximate): 1930s-1950s Hollywood 8-11 s; by 2000 3-6 s; action 2 s or less.
- Intensified vs brooding pair: Nolan's *Insomnia* about 1.9 s ASL against the 1997 Norwegian original's 5.4 s (*Labyrinth* pp. 12, 17).
- Head over about 3 s before the first turn, or tail over 2 s after the last: warn only, untested (after Sherman p. 250).
- Generated cards are 3-8 s; a cut shot often lands at 2-5 s.
- Target length: the brief's `target_seconds`, within ±0.5 s for a short, ±2% for longer work.
- Murch's ballpark: about 25 cuts a minute for a convincing action sequence (ASL about 2.4 s), and 6 or fewer for American dialogue (10 s or more). Fewer cuts in a fight make the viewer watch it rather than take part.

## Pitfalls

- Using every rendered second because it was expensive: the commonest reason a generated film drags.
- Cutting a slow scene fast to "keep energy" kills the contrast that makes the fast scenes work.

## Verify

- `edit/cut.md` lists each shot's in, out and length, the scene ASL, and the total against `target_seconds`.
