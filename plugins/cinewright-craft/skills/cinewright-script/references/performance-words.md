---
title: Performance words
slug: performance-words
summary: Write a performance as an objective, a playable verb aimed at a person, a physical task and a posture, never emotion adjectives; the card perform fields and what compile says.
tags: [script, performance, acting, prompts, voice]
last_checked: 2026-11-09
sources: ["Judith Weston, Directing Actors, 25th anniversary ed., 2021", "Michael Rabiger and Mick Hurbis-Cherrier, Directing: Film Techniques and Aesthetics, 6th ed., 2020"]
---

# Performance words

## Rules

- Each person in a two-person card has an objective: what they want from the other, as verb plus person plus effect ("make him admit he took the money"). It stays in the card for the reviewer; the model gets only its outward signs (Weston ch. 4 "Obstacle"; Rabiger ch. 20).
- Name an obstacle: what makes the objective hard (who they are to each other, a shame, a stuck lid). Competing objectives give both people one (Weston ch. 4 "Obstacle").
- The beat is one transitive verb aimed at the other person: accuses him, begs her, mocks him, coaxes her. Not angry, desperate, sarcastic. A verb gives the gaze and the gesture a target; an emotion word gives a face pulled on demand (Weston ch. 1 "Verbs"). Table: `kb show performance-verbs`.
- Prefer a bold verb to a weak one. Avoid become, feel, seem, react, ignore, defend (Weston ch. 1 "Verbs").
- Give the hands a physical task with a prop, ideally one that resists: pours tea, folds a shirt, works a stuck drawer. Busy hands show the state, and models render real motion better than a held face (Weston ch. 1 "Physical Tasks").
- A hidden feeling plays behind a task: "tries to look casual while tying the suitcase" raises more tension than the feeling shown (Rabiger ch. 17; ch. 8).
- One posture or gait from the character's past or the scene's pressure: head low, shoulders braced, fingers at a tight collar (Weston ch. 4 "The Physical Is Emotional"). Repeat it on every card of the scene, or the manner drifts between generations.
- One objective and one verb per person per card. A change of verb is a new beat; give it its own card or its own beat range (Rabiger ch. 17).
- The event happens inside the shot: start before she gives in, and let the turn play on screen (Weston ch. 5). One turn fits one 5-10 s generation.
- A move marks the end of a beat: a head turn, a step away, sitting down. Tie each move to a beat change, not to a line (Weston ch. 7).
- A reaction card names what lands on the listener, not the reaction: "as he says it, she stops folding the shirt", not "she looks shocked" (Weston ch. 1 ex. 5, ch. 3).
- Each generation has no memory of the last: state where the person comes from in `enters_from` ("still out of breath from running"), compiled as "Name is ..." (Rabiger ch. 29).
- Close shots stay contained: small purposeful gestures, steady gaze, no pacing or arm waving (Rabiger ch. 20).

## Numbers

- Per person per card: one objective, one verb, at most one task, one posture. Compile adds at most four short sentences per person.

## Vocabulary

- objective, obstacle, playable verb, physical task, adjustment, subtext, mask (the feeling hidden and the cover behaviour), result word (an emotion or judgement word played as an outcome).

## Pitfalls

- "Frightened but determined": two adjectives at once. Write two verbs in order over the beat, or a line said against a contrary action ("says sorry while glaring") (Weston ch. 1 ex. 9).
- Dial words ("a bit more, but not too much") give a model nothing to do (Weston ch. 1).
- Judgement labels (villain, creep, crazy) pull a caricature. Say what the person does to whom (Weston ch. 1 ex. 7).
- Two-person interaction is weak in current models. A single with the partner off screen and a physical task may beat a two-shot that says "she accuses him".
- Video models were trained on captions full of result words. A short face clause after the verb and task ("jaw clenched", "a small smile", "subtle expression") may still be needed. Untested: A/B verb-only against verb plus one face clause on the same seed.

## Verify

- Every two-person card has `perform.objective` and `perform.verb` for the person the shot favours.
- No performance text is only emotion adjectives: `continuity diff` RESULT warns when a `perform` verb or body holds only result words and no task.

## Notes

- 2026-11-09: card field `cast[].perform` added (objective, obstacle, subtext stay in the card; verb, task, body, masks, enters_from compile). Whether verbs beat adjectives on any model is untested.
