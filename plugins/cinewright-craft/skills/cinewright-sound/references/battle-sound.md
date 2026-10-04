---
title: Battle sound
slug: battle-sound
summary: Carry a battle's scale with sound: near, mid and far layers, weapons only in the near layer, perspective that follows shot size, silence at the turn; sound implies the unrendered army.
tags: [sound, battle, crowds, perspective, weapons]
last_checked: 2026-10-04
sources: ["David Sonnenschein, Sound Design, 2001", "Michel Chion, Audio-Vision: Sound on Screen, 2nd ed., 2019"]
---

# Battle sound

## Rules

- Three distance layers, always present: near (the hero's fight: each weapon hit, breath, armor, footfalls, all in sync), mid (groups fighting: clashes and shouts, loosely synced), far (the mass: a roar, drums, horns, rolling impacts, never in sync with anything).
- The far layer is the army: an acousmatic mass behind a close fight implies thousands where the render shows five (Chion's terms, entry chion-terms). cinewright-edit, entry cutting-a-battle, cuts to close fights with the mass heard.
- Perspective follows the shot: in a wide, mid and far layers lead and near hits are small; in a close-up, near leads and the mass drops and loses its highs.
- Weapons: one distinct sound per side's weapon type (heavy blades vs spears; rifles vs cannon) so the ear tells the sides apart, matched to the picture's screen direction (side A pans left to right).
- Each phase has its own bed (approach: drums and distant movement; clash: full layers; turn: drop to near and silence; rout: thinning far layer; aftermath: wind, single voices).
- Silence or near-silence at the turn (a muffled, ringing interval of 1-3 s) lands harder than the loudest moment.
- Loudness: battles drive true peaks; keep short-term loudness peaks inside the delivery's limits with a limiter on the effects stem, not by turning dialogue down (entry mix-and-loudness).

## Numbers

- Layers: near, mid, far. Turn silence: 1-3 s. Pan the sides consistently, for example side A 30% left of center when off-screen.

## Pitfalls

- One loud constant bed for the whole battle: fatigue within a minute and no sense of phases.
- Generic crowd walla in a war: needs shouts, effort and impacts, not murmur.

## Verify

- `sound/plan.md` names the three layers per battle shot and the bed per phase; `CINE qc loud` passes on the battle scene's mix.
