---
title: Logline and beats
slug: logline-and-beats
summary: The one-sentence logline and its tests, the bookend pair, want against need, act proportions, how many beats a film of a given length holds, and the beat sentence each shot card carries.
tags: [script, logline, beats, structure, acts]
last_checked: 2026-11-20
sources: ["Blake Snyder, Save the Cat!, 2005", "Jessica Brody, Save the Cat! Writes a Novel, 2018 (book rule, unverified)", "Syd Field, Screenplay, rev. ed. 2005", "John Truby, The Anatomy of Story, 2007", "Robert McKee, Story, 1997", "Michael Rabiger and Mick Hurbis-Cherrier, Directing, 6th ed., 2020", "David Mamet, On Directing Film, 1991", "David Bordwell, Poetics of Cinema, 2008, ch. 3", "David Bordwell, Narration in the Fiction Film, 1985, ch. 9", "Sheila Curran Bernard, Documentary Storytelling, 5th ed., ch. 2, 5 (book rule, unverified)"]
---

# Logline and beats

## Rules

- Logline: one sentence of about 35 words at most (house rule): protagonist, concrete goal, obstacle, stakes. Snyder's tests (ch. 1, 3): irony, an implied time frame, an adjective each for hero and opponent, a primal goal whose removal collapses the stakes.
- A logline that will not fit one sentence means two stories: cut one.
- Bookend pair (Snyder ch. 4): first and last shots planned as opposites on one visible axis (who is beside the hero, where they stand, what they hold). `brief.md` names `opening image:`, `final image:`, `axis:`. It survives at 45 s.
- `want:` concrete (object, place, person, result) with a shot where it is reached; `need:` the inner lesson, not the want, shown by a `visible task:` (Brody ch. 1; Rabiger ch. 4). Flat arc or ad: `need: none`.
- Name the train in `brief.md`: the main line of action that pulls the film to its end. Start it in the opening beats (the point of attack); backstory comes after it moves, in small pieces.
- Open on a concrete event that happens on screen (why now), not on a place or on someone getting an idea (Mamet p. 81). The inciting incident is on screen, never only in backstory or narration (McKee ch. 12).
- Cap each scene objective: a visible end state that is won or flatly refused ("get the grade changed", not "win respect"). Write `ends_when:` per scene, the card where it resolves; later cards go to the next scene or are cut (Mamet p. 35, p. 41).
- Beat names sit below the objective, never restating it or each other ("to impress" under "win respect") (Mamet p. 35).
- A beat is one change the audience sees: a want shown, a choice made, a reversal, a reveal. Write each as a present-tense sentence with an active verb. "She hesitates" is a beat; "tension builds" is not.
- Every beat is something a camera can show. Cut unfilmable lines: traits, backstory, "thirty hours later" (Mamet).
- Parts (Thompson, in Bordwell ch. 3): setup, complicating action, development, climax; each boundary is a change of goal, not a page count. A short may keep three. Climax no longer than setup (warn only).
- Midpoint (2 min and up): a false high or low that raises the stakes, mirrored by an all-is-lost beat of opposite charge (Snyder ch. 4); a knowledge flip (`knows:`) is one way to build it (house rule). Positions and tests: `kb show beat-positions-and-tests`.
- Every fact the ending depends on is shown at least three times by different carriers (line, action, prop, another's comment); a prop the climax uses appears early and casually (Bordwell, Narration ch. 9).
- One objective per person per card; a second objective is a new card (Rabiger ch. 17).
- Write the beats silent first, then add only the lines a look or a task cannot carry (McKee ch. 23; Truby ch. 10). A scene of dialogue singles with no action verb in any card is a warning sign (Rabiger ch. 8).
- Each shot card's `beat` field names the beat it serves. A beat with no card is unshot; a card with no beat is cuttable.

## Numbers

| Film length | Beats | Turns |
|---|---|---|
| 10-20 s | 2-3 | 1 |
| 30-60 s | 3-6 | 1 |
| 2-5 min | 8-15 | 2-3 |
| feature | 15 (Save the Cat), 22 steps (Truby) | many |

- Act proportions in a feature: about 25 / 50 / 25 percent (Field). One screenplay page runs about one minute.

## Vocabulary

- logline, premise, protagonist, goal (want), need, obstacle, stakes, inciting incident, midpoint, climax, resolution, beat sheet.

## Pitfalls

- A theme logline ("a story about loss") has no goal or obstacle. Mood beats ("a quiet moment") give the model nothing to act.

## Verify

- `brief.md` holds a one-sentence logline and a numbered beat list; every beat is named by at least one card's `beat` (`cards list`).
- Warn only, by eye (no script reads briefs): BOOKEND (both images named, opposite on the axis), WANT-NEED (both filled, different), WANT-CONCRETE (no abstract want: happiness, respect).
