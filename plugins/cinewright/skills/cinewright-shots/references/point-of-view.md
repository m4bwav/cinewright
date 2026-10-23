---
title: Point of view and the card's role
slug: point-of-view
summary: Whose scene each card serves (pov), the four questions to answer before tokens, how POV shots are set up, and the card's job in the edit (role).
tags: [shots, point-of-view, pov, role, identification]
last_checked: 2026-10-22
sources: ["Steven D. Katz, Film Directing Shot by Shot, 1991", "Joseph V. Mascelli, The Five C's of Cinematography, 1965"]
---

# Point of view and the card's role

## Rules

- Every scene belongs to one character: the one who leads the audience in, by being first on screen or first to look. Set `pov` to that id on their cards, and `objective` on cards that serve nobody (an establishing wide, a neutral insert).
- Shoot the owner's singles close to their sight line, a few degrees outside it, and always from the same angle. The other person's singles stay at the matched 45 and 135. The closer the camera sits to a sight line, the more the audience takes that person's side (after Katz, *Shot by Shot*).
- Before choosing tokens, answer four questions per card: whose view is this (camera position), how close do we feel (size), how do we relate to them (angle), and do we cut or move (comparing two views, or staying with one).
- A POV shot (`framing: pov`) shows what someone sees. It comes right after a card of that person looking off screen. People inside a POV shot look just past the lens, never into it.
- Never pan a POV shot round onto the person whose view it is (after Mascelli, *The Five C's*).
- Set `role` for the card's job in the edit: `establishing`, `master`, `coverage`, `reaction`, `cut-in` (a part of what a wider card showed), `cut-away` (something outside the main action), or `protection` (entry coverage).
- Not every big line needs a close-up. Holding the close-up back makes the next one land.

## Pitfalls

- With no owner, coverage drifts into neutral singles for everyone, and the scene belongs to nobody.

## Verify

- `continuity diff` POV: an unknown pov id (error), or a POV shot with no card of its owner looking off screen before it (warning).
