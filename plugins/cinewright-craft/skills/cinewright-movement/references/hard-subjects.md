---
title: Hard subjects
slug: hard-subjects
summary: Animals, crowds, vehicles drawn by animals, hands and liquids break in video models; show them side-on, few and large, and give the mass one line in the background.
tags: [movement, animals, crowds, hands, vehicles, physics]
last_checked: 2026-10-04
sources: ["Field lesson 020, 2026-09-30: draw an animal-drawn vehicle from the side; from behind, the image model puts the animals behind it", "Field lesson 021, 2026-09-30: few animals, large in frame, fix the legs; a far column of animals cannot be drawn"]
---

# Hard subjects

## Rules

- Few and large: frame 1-5 animals or people of a group, each at least a third of the frame height. Detail scales with size in pixels; a far animal gets almost nothing and its legs break.
- Never ask for a far column, herd or crowd in the middle of a shot. Give the mass one line in the background ("a long line of riders lost in dust behind them"). `continuity diff` warns HARD-SUBJECT on crowd words in EWS and WS cards.
- Side-on or three-quarter: legs, wheels and harness read clearly from the side. From behind or head-on, order and depth get confused.
- Vehicles pulled by animals: a side view with the direction stated ("travels from frame left to frame right; the horses on its right, heads pointing right, pulling it by long shafts"). Write the shot's last beat as the same side view, and check every guide still for the order before using it.
- Name each animal or rider differently (a grey mare, a black gelding with a white blaze) so the model does not clone one.
- Hands: one hand action per shot, hands large in frame, fingers doing one simple thing. Passing an object between two hands is two cards or an insert.
- Liquids, smoke and cloth: one stream or one sheet, with a named source and direction ("water pours from the jug into the cup").
- Spins and flips: avoid in one shot; cut from the take-off to the landing.
- Local models: spend compute on resolution, not sampling steps, when animals or hands are the subject.

## Numbers

- Subject height at least 1/3 of the frame; 1-5 subjects; local resolution 1056-1344 px on the long side for animal shots (one local model, 2026-09; unverified on others).

## Vocabulary

- side-on, three-quarter, head-on, far group, background mass, guide still (first frame).

## Pitfalls

- Story directions ("toward the enemy", "in front of the wagon") are ambiguous from behind; use frame words from a side view.
- More steps or a longer prompt do not fix small legs.

## Verify

- No HARD-SUBJECT warning in `continuity diff`, or the card's `notes` say why the wide crowd is needed.
