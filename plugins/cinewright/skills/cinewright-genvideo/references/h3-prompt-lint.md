---
title: H3 prompt lint (known misreads)
slug: h3-prompt-lint
summary: What cine.py compile's H3 lint warns about before GPU time (short clips, late or short cuts, fast speech, quoted lines, no soundscape, filler). IV Studio thresholds, unmeasured.
tags: [minimax, h3, prompt-lint, compile, untested]
last_checked: 2026-11-09
sources: ["r/StableDiffusion 1xqfux1, IV Studio lint.js (MIT, hollisorg/iv-studio), 2026-11", "MiniMax H3 prompt guide"]
---

# H3 prompt lint (known misreads)

`cine.py compile` lints every H3 prompt and prints `lint h3-...` warnings, never blockers. Rules adapted from IV Studio `lint.js` (MIT) and MiniMax's H3 guide; thresholds are theirs, unmeasured here. Hand-written prompts: the checklist in [h3-long-takes](h3-long-takes.md).

## Rules

- `h3-short`: under 124 frames (5.17 s), H3's trained floor; motion runs weak.
- `h3-cut-late`: a cut within 0.5 s of the end is dropped. `h3-shot-short`: a shot under 1.5 s often does not register. `h3-many-shots`: more than about one shot per 3 s. `h3-cut-order`: shot times must increase.
- `h3-speech-long`: more than 2.5 words a second inside `<d>`. `h3-quoted-line`: a line in quotes instead of `<d>`; H3 invents words.
- `h3-no-soundscape` (flat sound bed), `h3-silent` (`N/A` asks for silence), `h3-no-description`, `h3-blank` (`___` left in), `h3-filler` (quality tokens).

## Notes

- Not linted yet (IV Studio has them): a last frame attached but not placed is ignored; references attached but never named; face words fighting a character LoRA; several camera moves in one shot.
- GPU A/B of raw against lint-fixed prompts is planned (technique-harvest posts/1xqfux1.md); adopt a rule as proven only where the fixed prompt wins on 3 of 5 cards.
