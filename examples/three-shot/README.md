# Worked example: three shots

One one-line idea taken through the cinewright pipeline to compiled Veo 3.1 prompts. Nothing is rendered. Every command runs from the repository root; inside an installed skill, use that skill's `scripts/cine.py` instead.

## 1. Idea to brief

[brief.md](brief.md): logline, length, format, three beats.

## 2. Bibles, then cards

- [bibles/style.json](bibles/style.json): 16:9, 720p, 24 fps and the look string.
- [bibles/characters.json](bibles/characters.json): one identity string each for Maren and Tomas, wardrobe.
- [bibles/locations.json](bibles/locations.json): the lamp room.
- [bibles/scenes.json](bibles/scenes.json): scene 1, axis between Maren (frame-left) and Tomas (frame-right), camera side A, night, storm light.
- [cards/](cards/): 1A wide two-shot (azimuth 90), 1B Maren's MCU (45), 1C Tomas's MCU reverse (135). Each new card started as `python scripts/cine.py cards new examples/three-shot --id 1B --scene 1 --cast maren`.

```
$ python scripts/cine.py cards validate examples/three-shot
cards validate: 3 cards, 0 errors
```

## 3. Continuity diff: clean, then a planted error

```
$ python scripts/cine.py continuity diff examples/three-shot
continuity diff: 3 cards, 0 errors, 0 warnings
```

[planted/1C.json](planted/1C.json) is 1C with the camera moved to side B, across the line, for no on-screen reason:

```
$ python scripts/cine.py continuity diff examples/three-shot --with examples/three-shot/planted/1C.json
ERROR 1C AXIS: camera is on side B of the 1 axis (between Maren and Tomas, across the lens): it crosses the line, so every left and right flips. Move it to side A, or set crosses_axis with a cross_reason (a neutral shot or a move seen on screen).
ERROR 1C EYELINE: Tomas looks frame-left at Maren; from side B the eyeline must be frame-right
continuity diff: 3 cards, 2 errors, 0 warnings
```

The diff names the cause (AXIS) and the symptom a viewer would see (Tomas looking away from Maren).

## 4. Compiled Veo prompts

```
$ python scripts/cine.py compile examples/three-shot --model veo --out examples/three-shot/compiled/veo
$ python scripts/cine.py compile examples/three-shot --model veo --sequence --out examples/three-shot/compiled/veo-sequence
```

- [compiled/veo/](compiled/veo/): one prompt and one settings file per card. 1A runs 6 s, 1B and 1C 4 s each.
- [compiled/veo-sequence/](compiled/veo-sequence/): 1B and 1C in one 8 s generation with `[00:00-00:04]` and `[00:04-00:08]` blocks, so the cut between them happens inside one render.

Each prompt holds its cast's identity strings word for word, the fixed eyeline phrases, and the same look string.

## 5. Export for a local long-render pipeline

`python scripts/cine.py cards export examples/three-shot --film-json` prints the shot list as a `film.json` (name, target seconds, size, seeds, lengths in frames).
