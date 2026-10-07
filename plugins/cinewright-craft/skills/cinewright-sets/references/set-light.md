---
title: Set light
slug: set-light
summary: Write each set's light once per time of day as a named source, a color temperature and a key side tied to the plan's compass, and paste the same words into every plate and shot.
tags: [sets, light, time-of-day, continuity, color-temperature]
last_checked: 2026-10-07
sources: ["https://hackernoon.com/every-ai-generated-shot-invents-its-own-light-heres-how-to-keep-lighting-consistent", "https://apps.apple.com/us/app/sun-seeker-3d-augmented-reality-viewer/id330247123", "Blain Brown, Motion Picture and Video Lighting, 3rd edition, 2018"]
---

# Set light

## Rules

- Every generated shot invents its own light unless the words fix it. Write one light line per set and time of day in `sets/<id>.md`: the source (late-morning sun through the south windows, two brass practicals), a color temperature, and where the key falls in the plan (from the south wall).
- Turn the plan's compass into screen words per wall plate: facing north, a south key is behind the camera; facing east, it falls from frame right. Write the screen side in each wall plate's prompt.
- Paste the light line verbatim into every plate at that time of day, and into the style or scene light of the shots. Never reword it for variety.
- Exteriors: get the sun's direction for the time of day and the place's orientation (a sun-path app or table). A north facade in a northern-hemisphere summer morning has no direct sun on it.
- Make the widest plate first and match closer plates to its light.

## Numbers

- Daylight about 5600K, tungsten practicals about 3200K, overcast 6500-7500K, golden hour 3500-4000K (cinewright-camera, entry color-temperature).

## Pitfalls

- "Natural light" alone: each plate picks a different sun.
- A window wall plate with the sun behind the windows and a reverse also lit from the windows: on the reverse the windows are behind the camera, so the light comes from behind it.

## Verify

- Every plate of one time of day carries the same light line, and the bright side of each plate matches the plan.
