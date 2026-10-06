---
title: Sound layers and stems
slug: sound-layers
summary: Build every scene from the same six layers (dialogue, foley, hard effects, ambience, room tone, music), keep them on separate tracks, and deliver dialogue, music and effects stems beside the mix.
tags: [sound, layers, stems, foley, ambience, dme]
last_checked: 2026-10-04
sources: ["David Sonnenschein, Sound Design, 2001", "Tomlinson Holman, Sound for Film and Television, 3rd ed., 2010"]
---

# Sound layers and stems

## Rules

- Six layers, one or more tracks each, in this priority for the mix: dialogue, hard effects (sounds tied to a visible event: a door, a match strike), foley (body sounds re-performed: steps, cloth, hand on an object), ambience (the place: rain, wind, a crowd), room tone (the quiet of the room), music.
- Dialogue is the anchor: everything else is set against it, and it stays intelligible over every other layer.
- Every visible contact gets a sound: a hand on a prop, a step, a door. Missing foley is what makes generated video feel weightless.
- Ambience and room tone run under the whole scene, across every cut, so changes in generated noise floors never show.
- Silence is a layer too: drop ambience before a turn and the cut lands harder (Chion's terms, entry chion-terms).
- Write the plan in `sound/plan.md`: per shot, the layers present and what each sound is. Effects that sell the story (the match lighting) are named in the shot card's `sound` field too.
- Stems: deliver D (dialogue), M (music) and E (effects, with foley and ambience) as separate files, each the length of the cut, which sum to the full mix. A dubbed or re-edited version needs them.

## Numbers

- Sample rate 48 kHz, 24-bit for production and delivery of film and video sound (Holman 2010). Stems sum to the mix within 0.5 dB.

## Vocabulary

- D/M/E stems, M&E (music and effects, no dialogue), hard effect, foley, ambience (atmos, BG), room tone, walla (crowd murmur without words), sweetener.

## Pitfalls

- Putting music on every second: it flattens the scene and covers dialogue; leave room.
- Using a model's audio as the only layer: it changes texture at every generation seam (entry generated-audio).

## Verify

- `sound/plan.md` lists the six layers per scene; the mix project has them on separate tracks; stems exist beside the mix.
