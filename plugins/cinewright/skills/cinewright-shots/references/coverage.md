---
title: Coverage
slug: coverage
summary: Which shots a scene needs (master, matched singles, an insert), the classical card order, the close-up budget, and why AI coverage is a cut plan, not a pile of takes.
tags: [shots, coverage, master, reverse, insert, dialogue, decoupage]
last_checked: 2026-11-09
sources: ["Daniel Arijon, Grammar of the Film Language, 1976", "Steven D. Katz, Film Directing Shot by Shot, 1991", "David Bordwell, The Way Hollywood Tells It, 2006", "Joseph V. Mascelli, The Five C's of Cinematography, 1965", "Eric Sherman, Directing the Film, 1976", "Bordwell, Staiger, Thompson, The Classical Hollywood Cinema, 1985, ch. 5", "David Bordwell, The Labyrinth of Linkages, 2023"]
---

# Coverage

## Rules

- Coverage is the cut plan: every AI take costs a generation, so plan only the shots the cut uses, plus one escape shot (an insert or silent reaction) per scene to cut to over bad frames.
- Two people talking: master (WS two-shot, azimuth 90), one single each at azimuth 45 and 135 with the same size, lens and height, one insert of the prop the scene turns on. Each person keeps the frame side the master gave them.
- Classical order: wide, then two-shot or straight to reverses (`decoupage: stepped` or `direct`), singles, end the scene close. Re-establish with a wide after anyone moves or enters. Repeat setups exactly (same angle and distance each return); reverses share a scale (Bordwell 1985, pp. 70-71).
- Open a new place wide unless the style bible says otherwise. Tighten as tension rises; go wide at the release.
- Close-up budget: save the scene's tightest size for its peak beat and leave it unused before then; a big head lands only after a far shot (Sherman ch. 5).
- Private beats (confession, grief, alone) play in a held wide; plan the CU too, cut the wide first (Sherman ch. 5).
- Every OTS card gets a sibling clean single of the same face from the same side (Sherman ch. 5).
- Singles share = single cards over all actor cards. A high share reads choppy (Insomnia: 24 of 34). Resolve singles into a shared frame on a narrative beat (Labyrinth pp. 15-17). Warn only.
- One designed shot beats three: a face and the thing it reacts to can be one card with a focus pull (Labyrinth p. 17).
- Plan the listener's single, not only the speaker's. Keep a character the audience must not read at FS or wider (Katz), unless `intro: cu` (staging-moves).
- Vary the pattern between scenes: progressive, contrasting or repetitious; every change a full size step with an angle change (Mascelli).
- Protection: a reaction bank per principal (CU looking left and right, neutral). A risky card gets a cheaper static card with `role: protection`, `protects: <id>`, rendered after two failures (Mascelli).
- Push only on the character who holds the secret (MS2 6.5). For grief or shock the wide can come last (MS2 8.5). A hidden cut needs the same subject size both sides (MS3 11.8). One camera support per exchange (Bowen ch. 5). Book rules, unverified.

## Numbers

| Shot | Typical length | Notes |
|---|---|---|
| master | 6-8 s | holds the whole action once |
| single | 3-5 s | one line or one reaction |
| insert | 3 s | the shortest a model finishes; trim in the edit |

- 2000s features average 3-6 s per shot (Bordwell 2006); trim heads and tails to reach it.

## Vocabulary

- master: the whole scene in one wide. two-shot: two people. single (clean): one person alone. dirty single (OTS): a slice of the other in the foreground.
- reverse: the matching shot from the other side. insert: a close detail. cutaway: outside the action. reaction: a listener's face.

## Pitfalls

- An OTS asks the model to draw a second person from behind, and that shoulder drifts. Use clean singles unless the near person has references; then set `view: three-quarter-back` ("seen from behind at a three-quarter rear angle, only the cheek line showing") so it does not read as a two-shot (`ots-wrong`).

## Verify

- `cards list`: a master before the first single of each scene, one insert or reaction per scene, at least two size patterns across scenes.
- Singles in a pair share size and lens (`continuity diff` checks the 30-degree rule, not this).
