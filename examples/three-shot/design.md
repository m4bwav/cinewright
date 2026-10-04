# Design notes: The Last Match

Written with cinewright-design and cinewright-movement. Bibles hold the strings; this file holds the reasons.

## Color script

Palette (`bibles/style.json`): storm blue, brass, amber.

| Scene | Dominant | Accent | Why |
|---|---|---|---|
| 1 | storm blue (window light, `sun` in the scene bible) | amber (the match, later the flame) | cold and dark until trust is given; the warm accent sits in the hand that passes it |

Costume colors split the two people: Maren in navy, Tomas in yellow. Their silhouettes differ too (a braid and a close sweater against a mop of curls and a coat far too big).

## Costumes

One scene, so no arc: each character keeps the `default` wardrobe. If a later scene follows the relit lamp, Tomas's coat gets a stage-two string ("rain-soaked") keyed by that scene id.

## Props

`bibles/props.json` describes the tin matchbox and the match. The S2 render drew a cardboard box where the story meant tin; the compiler now pastes the description wherever a card holds the box.

## References

Turnaround prompt, Maren (one image, then crop to front, three-quarter and back into `refs/maren-front.png`, `refs/maren-3q.png`, `refs/maren-back.png`):

> Character turnaround sheet: the same person shown three times side by side, front, three-quarter, back. A lean woman in her sixties with deep-set grey eyes, silver hair in a single braid and a thin white scar through her left eyebrow, wearing a navy wool fisherman's sweater with a frayed collar. Flat even light, plain mid-grey backdrop.

Clean-up checklist before any reference goes into a shot: the scar is through her own LEFT eyebrow (the S2 take put it above the right); no pendant, badge or logo on the sweater; no text. Inspect at full size. Tomas's sheet uses the same frame with his strings.

## Movement

- 1A: a hand action (opening the box) inside a wide shot is a hard subject. Kept, because the shot's job is the room; the action is one phrase with contact ("thumbs ... open with a click") and a settle ("holding it still"). If the box drifts again, re-plan with an insert of the box (repair ladder rung 6).
- 1B: one slow phrase, the arm stretching out; the match steady is the settle.
- 1C: the handover is split across 1B and 1C, so no shot passes an object between two hands on screen; the fist pulled to the chest is the settle and matches `end_state`.
