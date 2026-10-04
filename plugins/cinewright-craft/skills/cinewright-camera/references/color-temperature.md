---
title: Color temperature
slug: color-temperature
summary: Name each light's color by its source and kelvin word (candle, tungsten, daylight, shade, blue hour), keep one white balance per scene, and use warm against cool as the main contrast.
tags: [lighting, color-temperature, kelvin, white-balance, golden-hour, blue-hour]
last_checked: 2026-10-04
sources: ["https://en.wikipedia.org/wiki/Color_temperature", "Blain Brown, Motion Picture and Video Lighting, 3rd ed., 2018", "Bruce Block, The Visual Story, 2nd ed., 2008"]
---

# Color temperature

## Rules

- Name each source by what it is and its color: "warm tungsten lamp", "deep orange candlelight", "cool blue daylight from the window". Source words carry color better than kelvin numbers. (Practice observation; models vary.)
- One white balance per scene: decide what reads as white (usually the key source) and keep it for every card. A scene lit by tungsten at a tungsten balance looks neutral; the same light at a daylight balance looks orange.
- Warm against cool is the strongest color contrast a prompt carries: warm practicals inside, cool light outside, or the reverse. It also feeds the color script (cinewright-design, color-script).
- Golden hour (low warm sun, long shadows) and blue hour (after sunset, deep blue sky, lamps lit) are time-of-day facts: put them in the scene bible's `sun` and `time_of_day`, never only in one card.
- Fire, candles and screens flicker; say "flickering" once in the scene's source, not per card.
- The grade can shift balance later (cinewright-finish); the prompt sets the light's color, the grade sets the film's.

## Numbers

- Candle about 1,850-1,900 K; tungsten 3,200 K; daylight 5,500-5,600 K; overcast and shade 6,500-7,500 K (lighting-terms vocab).

## Pitfalls

- A kelvin number alone ("3200K light") may print as text or be ignored; pair it with the source word.
- Mixing color words between cards of one scene shifts the color of everything, like changing the look string.

## Verify

- The scene's `sun` names the source color; cards agree with it; warm and cool roles match the color script.
