---
title: Coverage
slug: coverage
summary: Which shots a scene needs (master, matched singles, an insert), the default set for a two-person scene, and why AI coverage is a cut plan, not a pile of takes.
tags: [shots, coverage, master, reverse, insert, dialogue]
last_checked: 2026-10-22
sources: ["Daniel Arijon, Grammar of the Film Language, 1976", "Steven D. Katz, Film Directing Shot by Shot, 1991", "David Bordwell, The Way Hollywood Tells It, 2006", "Joseph V. Mascelli, The Five C's of Cinematography, 1965"]
---

# Coverage

## Rules

- Coverage is the cut plan. A film crew shoots extra angles and chooses in the edit; every AI take costs a generation, so plan only the shots the cut uses, plus one escape shot per scene.
- Default for two people talking: a master (WS two-shot, azimuth 90), then one single each at azimuth 45 and 135 with the same size, lens and camera height, then one insert of the prop the scene turns on. Cut order: master, singles, insert at the turn.
- Matched singles: same size (MCU), same lens (50mm), mirrored azimuth, each person on the side of frame the master gave them. A mismatch makes one person look bigger or farther away.
- Every scene gets one escape shot: an insert or a reaction with no dialogue. When a take has bad frames, cut to it (repair ladder rung 7).
- Open each new place with a wide shot that shows where everyone stands, unless the style bible says otherwise. The master is what the singles are checked against.
- Tighten as tension rises (wide, medium, close) and go wide again at the release.
- The reaction carries the feeling: plan the listener's single, not only the speaker's.
- Shot size is emotional distance. Keep a character the audience must not read (an antagonist, a mystery) at FS or wider for the whole scene (after Katz, *Shot by Shot*).
- Vary the pattern between scenes: progressive (step in), contrasting (WS against CU, high against low) or repetitious (a row of matched reaction CUs). Never run WS, MS, CU by rote in every scene. Each change is definite: a full size step with an angle change, never a half step (after Mascelli, *The Five C's*).
- Protection: per film, render a reaction bank for each principal, one CU looking frame-left and one frame-right, neutral face, plain receding background, same wardrobe. Per risky card (a dutch, a long move, a complex cross), plan one cheaper static card with `role: protection` and `protects: <id>`, rendered only if the risky card fails twice (after Mascelli).
- Push only on the character who holds the secret; matched pushes on both bind them. (MS2 6.5, 5.4) Book rule, unverified.
- For intense grief or shock, the establishing wide can come last. (MS2 8.5) Book rule, unverified.
- A hidden cut inside a render needs the subject the same size on both sides. (MS3 11.8) Book rule, unverified.
- One camera support per scene: never mix locked-off and handheld inside one exchange. (Bowen ch. 5) Book rule, unverified.

## Numbers

| Shot | Typical length | Notes |
|---|---|---|
| master | 6-8 s | holds the whole action once |
| single | 3-5 s | one line or one reaction |
| insert | 3 s | the shortest a model finishes; trim in the edit |

- 2000s Hollywood features average 3-6 s per shot (Bordwell 2006). Generated shots run at least 3 s, so trim heads and tails in the edit to reach a modern pace.

## Vocabulary

- master: the whole scene in one wide shot. two-shot: two people in one frame.
- single (clean single): one person, nobody else in frame. dirty single (OTS): over the shoulder, a slice of the other person in the foreground.
- reverse: the matching shot from the other person's side. insert: a close detail, usually a prop. cutaway: something outside the action. reaction: a listener's face.

## Pitfalls

- An OTS shot asks the model to draw a second person from behind; that shoulder drifts in hair and wardrobe. Use clean singles unless the second person has reference images. When you do shoot one, set `view: three-quarter-back` on the near person: it compiles to "seen from behind at a three-quarter rear angle, only the cheek line showing", so their nose and eye stay hidden and the shot does not read as a two-shot (`ots-wrong`; after Mascelli).

## Verify

- `cards list` shows a master or establishing shot before the first single of each scene, and one insert or reaction per scene.
- Singles in a pair share size and lens (`continuity diff` checks the 30-degree rule, not this).
- `cards list` shows at least two different size patterns across the scenes.
