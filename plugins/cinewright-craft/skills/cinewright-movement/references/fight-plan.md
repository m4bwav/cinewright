---
title: Fight plan
slug: fight-plan
summary: Choreograph a fight before its cards: question and ending first, phrases with who is ahead and why, exchanges operator first with weapons, wounds and sides tracked, then check the cards.
tags: [movement, fights, choreography, notation, fight-plan, rhythm]
last_checked: 2026-10-15
sources: ["David McCormick (Fight Directors Canada), Recording Choreography, Academie Duello, 2015: https://web.archive.org/web/20150311201049/http://www.academieduello.com:80/news-blog/recording-choreography/", "McCormick, Plot in Choreography, 2013: https://web.archive.org/web/20131023003111/http://www.academieduello.com/news-blog/plot-in-choreography/", "McCormick, Fight Choreography: Action Logic, 2012: https://web.archive.org/web/20160815083821/http://www.academieduello.com/news-blog/fight-choreography-action-logic/", "David Bordwell, Planet Hong Kong, 2000, ch. 8 (pause, burst, pause)", "Baby Driver editors, Art of the Cut: https://www.provideocoalition.com/aotc-baby-driver/", "ai-docs/research/2026-10-15-fight-planning.md"]
---

# Fight plan

## Rules

- Any fight longer than one exchange gets a plan before its cards: `fights/<id>.json` (schema `scripts/schemas/fight-plan.schema.json`). Run `python scripts/cine_fight.py check fights/<id>.json`, write the cards, then `check ... --project .` until no errors remain.
- Write the question and the ending first and plan back from the ending. The question is what the audience waits to learn, not who wins: "can he still take his revenge?", "will she spare him?".
- Split the fight into phrases of 2 to 6 exchanges with a pause between them (pause, burst, pause). Each phrase names who is `ahead` at its end and `why`, in visible terms: courage, a cheat, terrain, a wound. Lines and looks go in the pauses, never mid-exchange.
- The side that wins must almost lose. `check` warns ONE-SIDED when one fighter leads every phrase.
- Write each exchange operator first: who acts (`lead`), the move with its weapon (`with`) and its target in body words ("thrusts at his left shoulder"), the other's `answer`, the `result`. Never fencing parry numbers or target codes: no video model knows "parry 4".
- Record every change after an exchange: a prop drawn, dropped or taken (`right`, `left`, `carried`), a new `mark` (wound, blood), `posture`, and `side` when they cross on screen. A prop is in one place: taking it from the other's belt removes it there.
- Copy every mark verbatim into the start_state, action or a beat of each later card of that fighter; the model forgets wounds between generations. A mark the beat touches goes in that beat. Clean reference sheets keep identity (entry wounds-and-healing).
- One exchange per card, two at most; a card no shorter than its exchanges. Pause cards carry dialogue.
- Music: set `bpm`; cut cards and land the big impacts on beats, not every contact. Timing lives at the cuts. Inside a fight card, give the card `beats` (each hit and its reaction on its own range of about 0.8 s, times on the rendered clip) for models that take timecodes: they set order and rhythm, not frames (genvideo L-016). Keep `action` as a one-sentence summary for the others.
- `cine_fight.py sheet` writes the grid (a column per fighter, an arrow from the operator) and a CSV; a step chart of `ahead_score` over `time_s` (chartwright) shows the turns at a glance. Sheets and charts are for people reviewing the arc; never paste them into prompts.

## Numbers

- Exchange 1-2.5 s; phrase 2-6 exchanges; pause 1 s, 3-7 s with lines. About 20 exchanges and 9 phrases make a 70 s duel with dialogue.
- At least three phrases; `margin` 1 edge, 2 clear, 3 nearly beaten.

## Vocabulary

- operator, exchange, phrase, pause, burst, ahead, margin, story decision, arrow of intention, cadence.

## Pitfalls

- A per-second spreadsheet of cause and effect: a video model cannot hit a timestamp inside a clip, and the extra prose leaks into prompts.
- A plan with no `with` fields cannot catch a weapon used after it was dropped.
- A flat ahead line is a fight with no story; a line that swings every exchange is noise. Turn it at phrase ends.

## Verify

- `cine_fight.py check fights/<id>.json --project .` ends with 0 errors; MARK warnings are fixed or explained in the card's notes.

Related: builds on [fights-and-stunts](fights-and-stunts.md); see also [fight-from-a-book](fight-from-a-book.md), [fight-previs](fight-previs.md).
