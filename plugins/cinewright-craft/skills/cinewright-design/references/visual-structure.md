---
title: Visual structure plan
slug: visual-structure
summary: Block's plan: story intensity 0-100 per scene, one line of point of view, and per component a constant, a progression or peaks; cards graph and grade measure --plan check it.
tags: [design, visual-structure, intensity, contrast, affinity, block, story-graph]
last_checked: 2026-10-22
sources: ["Bruce Block, The Visual Story, 3rd ed., 2021, ch. 1-2, 9-10"]
---

# Visual structure plan

## Rules

- Every frame is built from seven components: space, line, shape, tone, colour, movement and rhythm. They work on the audience whether planned or not, so plan them (after Block, *The Visual Story*).
- Contrast in a component raises visual intensity; affinity (sameness) lowers it. This holds inside a shot, from shot to shot and from sequence to sequence.
- Draw the story graph first: `intensity` 0-100 on each scene in `bibles/scenes.json`. Exposition sits low, the conflict climbs with dips, one scene is the climax at the top, the resolution comes back down. A one-scene film gets `intensity` per card instead.
- Write the visual point of view in one line in `style.json` `visual_structure.point_of_view` ("a wary family: flat space, square shapes, cool colours").
- For each component pick one plan: a constant (never changes), a progression (`from`, `to`, steadily across the film) or `peaks` (contrast spikes at named scenes). Most stay constant; two or three change at most. Constants are a list in `constants`.
- Name the climax scene in `visual_structure.climax`. At the climax the changing components contrast hardest from shot to shot; the resolution returns to affinity.
- The first scene that uses a value teaches its meaning (a colour, an angle, a kind of space). Record it in `meanings` and keep it for the whole film. Any meaning can be taught; the stereotype is optional.
- Keep it simple enough to see on one viewing, and ask of each shot what can be taken out.
- Where it compiles: scene `space` (cinewright-shots space-types), scene `color` (entry color-script), card `line` and `attention` (cinewright-edit attention-continuum).

## Numbers

- Intensity 0-100. `cards graph` flags a span under 30 points (a monotone curve), a named climax below another scene, a peak in the first scene, and a last scene as intense as the climax.
- Changing components: 1-3. More reads as noise.

## Pitfalls

- Changing everything at once: nothing reads as the change.
- Intensity spread evenly across scenes: the film has no shape.
- A contrast spike with no story peak under it (`cards graph` flag PEAK).

## Verify

- `CINE cards graph <project>`: no flags, or each one answered in `design.md`.
- After the edit: `CINE_POST grade measure SHOTS --plan <project>` (cinewright-edit, cinewright-finish) shows each changing component following its plan.

Related: see also [color-script](color-script.md).
