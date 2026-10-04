# Worked example: three shots

One one-line idea taken through the cinewright pipeline to compiled prompts, using each pre-production skill once. Every command runs from the repository root; inside an installed skill, use that skill's `scripts/cine.py` instead. The S2 session rendered this example once on a local model; the media stays out of the repository.

## 1. Idea to brief and script (cinewright-script)

- [brief.md](brief.md): logline, length, format, three beats, and the scene turn (trust, minus to plus, in 1B).
- [script.md](script.md): the screenplay. Its slugline is the scene bible's `heading`, and its one line of dialogue is on card 1B word for word (8 words in a 4 s shot: under the 2.5-words-a-second limit).

## 2. Bibles and design (cinewright-continuity, cinewright-design)

- [bibles/style.json](bibles/style.json): 16:9, 720p, 24 fps, the look string and the palette.
- [bibles/characters.json](bibles/characters.json): one identity string each for Maren and Tomas, wardrobe.
- [bibles/props.json](bibles/props.json): fixed descriptions for the tin matchbox and the match. The S2 render drew a cardboard box; the compiler now pastes "a small dented tin matchbox with a hinged lid, ..." wherever a card holds it.
- [bibles/locations.json](bibles/locations.json), [bibles/scenes.json](bibles/scenes.json): the lamp room; scene 1 with the axis between Maren (frame-left) and Tomas (frame-right), camera side A, night, storm light.
- [design.md](design.md): color script, why the costumes differ, the turnaround prompt and clean-up checklist (scar through her own left eyebrow), and the movement notes.

## 3. Shot list (cinewright-shots, cinewright-movement)

Coverage for two people and one turn: a master, matched singles at azimuth 45 and 135 (MCU, 50mm). The actions were rewritten with a contact and a settle; the handover is split across 1B and 1C so no shot passes an object between hands.

```
$ python scripts/cine.py cards list examples/three-shot
| # | Slate | Size | Angle | Az | Move | Lens | Cast | Action | s |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1A | WS | eye-level | 90 | static | 24 | Maren, Tomas | Maren thumbs the tin matchbox open with a click and pinches out a single match, holding it still between finger and thumb. | 6 |
| 2 | 1B | MCU | eye-level | 45 | dolly-in | 50 | Maren | Maren slowly stretches her arm out toward Tomas, off screen, the match steady in her fingers. | 4 |
| 3 | 1C | MCU | eye-level | 135 | static | 50 | Tomas | Tomas takes the match from a hand entering frame left and closes his fist tight around it, pulling it to his chest. | 4 |
shot list: 3 shots, 1 scene(s), 14s
$ python scripts/cine.py cards validate examples/three-shot
cards validate: 3 cards, 0 errors
```

## 4. Continuity diff: clean, then a planted error

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

## 5. Compiled prompts

```
$ python scripts/cine.py compile examples/three-shot --model veo --out examples/three-shot/compiled/veo
$ python scripts/cine.py compile examples/three-shot --model veo --sequence --out examples/three-shot/compiled/veo-sequence
$ python scripts/cine.py compile examples/three-shot --model minimax-h3 --sequence --resolution 480p --out examples/three-shot/compiled/minimax-h3-sequence
```

- [compiled/veo/](compiled/veo/): one prompt and one settings file per card. 1A runs 6 s, 1B and 1C 4 s each.
- [compiled/veo-sequence/](compiled/veo-sequence/): 1B and 1C in one 8 s generation with `[00:00-00:04]` and `[00:04-00:08]` blocks.
- [compiled/minimax-h3-sequence/](compiled/minimax-h3-sequence/): all three shots in one 14.4 s local generation, as rendered in S2. It is 377 words against H3's 300-word guide (the S2 take at 336 words rendered well); the compiler warns, and the words cut first would be action or context, never identity or prop strings.

Each prompt holds its cast's identity strings and the held prop's description word for word, the fixed eyeline phrases, and the same look string.

## 6. Export for a local long-render pipeline

`python scripts/cine.py cards export examples/three-shot --film-json` prints the shot list as a `film.json` (name, target seconds, size, seeds, lengths in frames).
