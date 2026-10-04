---
title: Coverage
slug: coverage
summary: Which shots a scene needs (master, matched singles, an insert), the default set for a two-person scene, and why AI coverage is a cut plan, not a pile of takes.
tags: [shots, coverage, master, reverse, insert, dialogue]
last_checked: 2026-10-04
sources: ["Daniel Arijon, Grammar of the Film Language, 1976", "Steven D. Katz, Film Directing Shot by Shot, 1991", "David Bordwell, The Way Hollywood Tells It, 2006"]
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

- An OTS shot asks the model to draw a second person from behind; that shoulder drifts in hair and wardrobe. Use clean singles unless the second person has reference images.

## Verify

- `cards list` shows a master or establishing shot before the first single of each scene, and one insert or reaction per scene.
- Singles in a pair share size and lens (`continuity diff` checks the 30-degree rule, not this).
