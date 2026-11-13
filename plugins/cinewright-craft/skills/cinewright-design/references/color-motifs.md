---
title: Color motifs
slug: color-motifs
summary: A colour carried across the story: arc per character, faction colour, a held-back colour, colour entering with the turn, show before remove; visual_structure.motifs and cards graph check it.
tags: [design, color, motif, color-script]
last_checked: 2026-11-13
sources: ["Patti Bellantoni, If It's Purple, Someone's Gonna Die, 2005, pp. 16-21, 28-29, 96-97, 105-106, 123-125"]
---

# Color motifs

## Rules

- Book rule, unverified, culture-bound: these devices come from one teacher's reading of finished Western films. Use them as questions to check a plan against.
- List each motif in `style.json` `visual_structure.motifs`: `hue` (the plain word used in rows and wardrobe), `carrier`, `owner` (character or faction), `enters` (scene id), and `reserved_until` when it is held back.
- Character arc: does the character keep one hue family and move its lightness, saturation or warmth at named beats? A resolution can be the same hue turning warm.
- Faction colour: does each side own one colour, carried by props, vehicles and set dressing as well as wardrobe? Changing sides means changing colour.
- Held-back colour: is one hue banned until its scene so it lands? Locations and props break the ban unless someone checks.
- Entering colour: does the motif first appear in a turn, or with the character who causes it? A spreading colour moves into other people's wardrobe as an influence grows; a leaving colour shows a change.
- Show before remove: before the story drains or covers a colour, is there a card where it is seen close and long?
- Give the motif's carrier a card of its own, close, before it has to mean anything.

## Pitfalls

- A held-back hue word hiding in a location or wardrobe string renders early; the model does not know it is reserved.
- A film-wide look that pulls saturation can move a motif into another variant.

## Verify

- `CINE cards graph <project>` shows no MOTIF flag (a motif with no enters scene that has cards) and no RESERVED flag (the held-back word in an earlier scene's row, cards or cast wardrobe).
- On a contact sheet in story order, the motif's entrance is findable from colour alone.

Related: builds on [color-script](color-script.md); see also [color-associations](color-associations.md), [costume-arc](costume-arc.md).
