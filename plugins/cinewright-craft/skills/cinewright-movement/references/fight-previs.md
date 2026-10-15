---
title: Fight previs
slug: fight-previs
summary: Pick a route per fight card, cheapest first: prose plus a contact still, an animatic, a performer's reference video, a 3D blockout (untested); keep each fighter's face apart.
tags: [movement, fights, previs, stuntvis, reference-video, pose, 3d]
last_checked: 2026-10-15
sources: ["Ian Failes, Stuntvis Amps Up the Action, VFX Voice, Fall 2018: https://vfxvoice.com/?p=3123357", "r/StableDiffusion H3 fight threads, Aug-Sep 2026: https://www.reddit.com/r/StableDiffusion/comments/1vsjezd/ , https://www.reddit.com/r/StableDiffusion/comments/1vnzx6w/ , https://www.reddit.com/r/StableDiffusion/comments/1w8p67n/", "SCAIL (zai-org), paper and Blender rig issue: https://github.com/zai-org/SCAIL , https://github.com/zai-org/SCAIL/issues/30", "PrevizWhiz, CHI 2026: https://arxiv.org/html/2602.03838v1", "ai-docs/research/2026-10-15-fight-planning.md"]
---

# Fight previs

## Rules

- Stunt teams rehearse a fight on video and cut it before the shoot (stuntvis). The AI version: an animatic of the fight from one still per card, timed to the cards (cine_post `animatic`, entry animatic), reviewed before any video render.
- Default route for a card: the prose exchange, fighters large in frame (head to thigh), and a pinned still of the contact moment when contact must land (entry fights-and-stunts). Distant fighters smear in fast motion on every model; the H3 team confirms it.
- On models that take shot timecodes in the prompt (MiniMax H3), name each hit and its reaction on its own timecode. Forum tests got punches to land this way at 30-50 steps; speed and turbo LoRAs changed the choreography itself.
- Hard beats (a throw, a grapple, contact that must read): record a performer doing the exchange at moderate speed with a locked camera at the card's angle, and drive the model with it (H3 reference video, Wan Animate). It carries timing and camera better than contact, so still pin the contact still. One reference per card, 5-6 s; a 12 s reference was not followed.
- Two fighters in one reference pass: mask one person per pass, or film both performers. Pose extraction breaks where limbs overlap or leave the frame.
- 3D blockout for grapples and falls (untested for fights): animation clips (Mixamo, CMU, Cascadeur) on proxy figures in Blender, rendered from the card's camera as depth plus a per-person skeleton for SCAIL-style pose models. Weapons have no skeleton: keep them in the depth pass, drawn thicker than life in the control passes only.
- Faces swap between fighters: a separate sheet per fighter, an asymmetric mark each (one glove, the scar side), and in the prompt name each by screen side ("the man on the right") when they look alike.

## Numbers

- Budget 3-8 renders per fight card; the best seconds of several takes are often cut together.
- Reference video 5-6 s per card; steps 30-50 on H3 fight cards, no speed LoRA.

## Pitfalls

- A storyboard grid as one reference for a whole fight works on hosted multi-shot models (vendor tests); on local models it is untested. Test one card before boarding a fight.
- A 1 m blade at full-shot distance is a few pixels in a depth or pose pass and is lost.

Related: builds on [fight-plan](fight-plan.md); see also [crowd-blockout](crowd-blockout.md), [fights-and-stunts](fights-and-stunts.md).
