---
title: Logline and beats
slug: logline-and-beats
summary: The one-sentence logline form, act proportions, how many beats a film of a given length holds, and the beat sentence each shot card carries.
tags: [script, logline, beats, structure, acts]
last_checked: 2026-11-09
sources: ["Blake Snyder, Save the Cat!, 2005", "Syd Field, Screenplay, rev. ed. 2005", "John Truby, The Anatomy of Story, 2007", "Michael Rabiger and Mick Hurbis-Cherrier, Directing: Film Techniques and Aesthetics, 6th ed., 2020", "David Mamet, On Directing Film, 1991", "David Bordwell, Poetics of Cinema, 2008, ch. 3", "David Bordwell, Narration in the Fiction Film, 1985, ch. 9"]
---

# Logline and beats

## Rules

- Logline: one sentence, 35 words or fewer, in the form: when/where + a specific protagonist + wants a concrete goal + against a specific obstacle + what is at stake. No names needed; a defining adjective beats a name.
- Write the logline first; if it will not fit one sentence, the film has two stories. Cut one.
- Open on a concrete event that happens on screen (why now), not on a place or on someone getting an idea (Mamet p. 81).
- Cap each scene objective: a visible end state that is won or flatly refused ("get the grade changed", not "win respect"). Write `ends_when:` per scene, the card where it resolves; later cards go to the next scene or are cut (Mamet p. 35, p. 41).
- Beat names sit one level below the objective and never restate it or repeat each other: "to impress" under "win respect" is a repeat (Mamet p. 35).
- A beat is one change the audience sees: a want shown, a choice made, a reversal, a reveal. Write each as a present-tense sentence with an active verb. "She hesitates" is a beat; "tension builds" is not.
- Every beat must be something a camera can show. Cut unfilmable lines: traits, backstory, "thirty hours later" (Mamet).
- Parts (Thompson, in Bordwell ch. 3): setup, complicating action, development, climax; each boundary is a change of goal, not a page count. A short may keep three. Climax no longer than setup (warn only).
- The midpoint is a knowledge flip: after it someone knows the key fact the other does not (`knows:` on the beat).
- Every fact the ending depends on is shown at least three times by different carriers (line, action, prop, another's comment); a prop the climax uses appears early and casually (Bordwell, Narration ch. 9).
- Pair every inner need in the brief with a visible task (`need:` and `visible task:`): a stammer is the outward form of feeling unworthy (Rabiger ch. 4).
- One objective per person per card; a second objective is a new card (Rabiger ch. 17).
- For each line of dialogue, ask whether a look or a task can carry it. A scene of dialogue singles with no action verb in any card is a warning sign (Rabiger ch. 8).
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
