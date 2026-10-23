---
title: Light sources in frame
slug: light-sources
summary: Carry a visible practical onto the face, no face against a window, open shade outdoors, backlit rain and haze (light.atmosphere), flickering fire, moonlight, magic hour.
tags: [lighting, practical, window, exterior, atmosphere, rain, fire, moonlight]
last_checked: 2026-10-22
sources: ["Blain Brown, Cinematography: Theory and Practice, 3rd ed., 2016, Lighting Basics and Technical Issues", "Mike Goodridge, FilmCraft: Cinematography, 2012 (Deschanel, Lachman, Zsigmond interviews)"]
---

# Light sources in frame

## Rules

- Carry the practical: a lamp, candle, screen or fire in frame lights the face from its own direction, colour and hardness. Write it in `light.motivation` with a side ("the warm table lamp at frame left lights her face from the left"), and call the practical "glowing", never blown out (after Brown, *Cinematography*). Show the source in the wide first; the close shots then believe it.
- Never stage a face against a bright window. Put the window beside the face and the room behind it. Window light is soft because it is sky and bounce, not sun.
- Hard sun outdoors: move the people into open shade ("in the shade of the building, soft skylight, the bright street behind her"), or turn their backs to the sun and let it rim them.
- Rain, snow, smoke, haze, fog, dust and steam show only with light behind them. Set card `light.atmosphere`; compile writes "the rain is backlit, lit from behind so it shows". Front-lit, they vanish.
- Firelight is several flickering sources with shadows that jump, never one steady glow. Compile adds "the firelight flickers and the shadows jump" when `light.motivation` names fire, flames, a torch or a brazier. Lightning flashes from more than one direction.
- Two worlds can carry two colour temperatures (a cool house, a warm outside), and mixed practicals (tungsten, sodium, fluorescent) give a place its colour (after Lachman in *FilmCraft*).
- One room over a long scene: let the light change with time (late sun, dusk, then lamps and candles) and split the scene by light state, each with its own `sun` string (after Deschanel in *FilmCraft*).
- People walking in and out of pools of hard light add depth (after Zsigmond in *FilmCraft*).

## Numbers

- Table lamps and candles: about 2800 K and below, warm. Moonlight: blue by convention, from half to double blue correction; a touch of lavender keeps skin alive.
- Magic hour lasts about 20 to 30 minutes. A long scene "at golden hour" needs the grade to hold it.

## Pitfalls

- A lamp in frame and a key from the other side: `source-mismatch` in review.
- Rain or haze named in the action but no `light.atmosphere`: the model draws it front-lit or not at all (`atmos-unlit`).

## Verify

- Every card with a visible source names it in `light.motivation` with a side; every airborne effect has `light.atmosphere`.

Related: see also [lighting-setups](lighting-setups.md), [color-temperature](color-temperature.md).
