---
title: Shot sizes
slug: shot-sizes
summary: The eight shot-size tokens cards use (EWS to ECU), what each frames, the order used for size steps, and the prompt words each compiles to.
tags: [vocab, camera, framing, shots]
last_checked: 2026-10-03
sources: ["Joseph V. Mascelli, The Five C's of Cinematography, 1965", "Daniel Arijon, Grammar of the Film Language, 1976", "https://en.wikipedia.org/wiki/Shot_(filmmaking)"]
---

# Shot sizes

## Vocabulary

Ordered widest to tightest. A size step is the distance between two tokens in this list.

| Token | Name | Frames | Prompt words |
|---|---|---|---|
| `EWS` | extreme wide shot | place first, people tiny or absent | extreme wide shot |
| `WS` | wide shot | whole set, people full figure with room | wide shot |
| `FS` | full shot | one person head to feet, little headroom | full shot |
| `MWS` | medium wide (cowboy) | mid-thigh up | medium wide shot |
| `MS` | medium shot | waist up | medium shot |
| `MCU` | medium close-up | chest up | medium close-up |
| `CU` | close-up | face, top of shoulders | close-up |
| `ECU` | extreme close-up | eyes, a hand, an object detail | extreme close-up |

## Rules

- A card has exactly one size. A move that changes size (dolly in) is recorded as the starting size plus the move.
- Cut between two shots of the same subject with at least two size steps, or a 30-degree change of angle (see the thirty-degree rule entry).
- Inserts of props are `CU` or `ECU` with no cast on screen.

## Pitfalls

- "Medium" alone is read by video models as anything from `MWS` to `MCU`. Compile the full prompt words above.
