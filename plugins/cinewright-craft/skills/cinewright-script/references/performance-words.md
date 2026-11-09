---
title: Performance words
slug: performance-words
summary: Write a performance as an objective, a playable verb aimed at a person, a physical task and a posture, never emotion adjectives; the card perform fields and what compile says.
tags: [script, performance, acting, prompts, voice]
last_checked: 2026-11-09
sources: ["Judith Weston, Directing Actors, 25th anniversary ed., 2021", "Michael Rabiger and Mick Hurbis-Cherrier, Directing: Film Techniques and Aesthetics, 6th ed., 2020", "Judy Kerr DeKoven, Changing Direction, 2006", "Nicholas T. Proferes, Film Directing Fundamentals, 4th ed., ch. 2, 10", "David Mamet, On Directing Film, 1991"]
---

# Performance words

## Rules

- Each person in a two-person card has an objective: what they want from the other, as verb plus person plus effect ("make him admit he took the money"). It stays in the card; the model gets only its outward signs (Weston ch. 4; Rabiger ch. 20).
- Name an obstacle: what makes the objective hard (who they are to each other, a shame, a stuck lid) (Weston ch. 4).
- Chain it: verb, in order to the scene need, in order to a life need. The life need never changes in the film; the scene need holds from a scene's first card to its last (DeKoven ch. 3). Reviewer check only.
- The beat is one transitive verb aimed at the other person: accuses him, begs her, mocks him, coaxes her. Not angry, desperate, sarcastic: a verb gives gaze and gesture a target (Weston ch. 1). Table: `kb show performance-verbs`.
- Prefer a bold verb. Never be, look, become, feel, seem, react, ignore, defend: "be funny" is amuse (Weston ch. 1; DeKoven p. 31).
- The verb must be playable in silence: challenge, impress, amuse pass; say, tell, explain, ask fail. Most clips are silent (DeKoven p. 31).
- Give the hands a physical task with a prop, ideally one that resists: pours tea, works a stuck drawer. Models render real motion better than a held face (Weston ch. 1). The task is the activity, the verb the action; the verb may aim at the prop (she accuses his shirt as she irons it) (Proferes ch. 2; DeKoven p. 112).
- A hidden feeling plays behind a task: "tries to look casual while tying the suitcase" beats the feeling shown (Rabiger ch. 17).
- One posture or gait from the character's past or the scene's pressure: head low, shoulders braced (Weston ch. 4). Repeat it on every card of the scene, or the manner drifts.
- One objective and one verb per person per card. A change of verb is a new beat (Rabiger ch. 17).
- The event happens inside the shot: start before she gives in, and let the turn play on screen (Weston ch. 5). One turn fits one 5-10 s generation.
- A move marks the end of a beat: a head turn, a step away, sitting down. Tie each move to a beat change, not to a line (Weston ch. 7).
- A reaction card names what lands on the listener, not the reaction: "as he says it, she stops folding the shirt", not "she looks shocked" (Weston ch. 1 ex. 5, ch. 3).
- Each generation has no memory of the last: state where the person comes from in `enters_from` ("still out of breath from running"), compiled as "Name is ..." (Rabiger ch. 29).
- Close shots stay contained: small gestures, steady gaze, no pacing (Rabiger ch. 20).
- Restraint card: the biggest moment gets the smallest act ("takes a beat, then nods once"), and the next card shows what it causes (Mamet).
- When a verb fails, put a fact in the subtext, not an attitude: "he slept with your best friend", not "can't be trusted" (Proferes ch. 10).

## Numbers

- Per person per card: one objective, one verb, at most one task, one posture. Compile adds at most four short sentences per person.

## Vocabulary

- objective, obstacle, playable verb, physical task, adjustment, subtext, mask (the feeling hidden and the cover behaviour), result word (an emotion or judgement word played as an outcome).

## Pitfalls

- "Frightened but determined": two adjectives. Write two verbs in order, or a line against a contrary action (Weston ch. 1 ex. 9).
- Dial words ("a bit more, but not too much") give a model nothing to do (Weston ch. 1).
- Judgement labels (villain, creep, crazy) pull a caricature. Say what the person does to whom (Weston ch. 1 ex. 7).
- Two-person interaction is weak in current models. A single with the partner off screen and a physical task may beat a two-shot that says "she accuses him".
- Models were trained on captions full of result words; a short face clause after the verb and task may still be needed. Untested: A/B on one seed.

## Verify

- Every two-person card has `perform.objective` and `perform.verb` for the person the shot favours.
- No performance text is only emotion adjectives: `continuity diff` RESULT warns when a `perform` verb or body holds only result words and no task.
