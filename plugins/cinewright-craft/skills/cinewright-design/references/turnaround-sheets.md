---
title: Turnaround sheets
slug: turnaround-sheets
summary: Make each recurring character one turnaround sheet in a single image (front, three-quarter, back), then crop the views into separate reference files.
tags: [design, character, turnaround, references, identity]
last_checked: 2026-10-04
sources: ["Field lesson 017, 2026-09-29: turnaround sheets hold one identity across views; costume sheets invent symbols", "Tom Bancroft, Creating Characters with Personality, 2006"]
---

# Turnaround sheets

## Rules

- Generate each recurring character as one image holding three views side by side: front, three-quarter, back. An image model keeps one face, hair and costume inside a single image far better than across separate generations.
- Prompt the sheet as "character turnaround sheet: the same person shown three times side by side, front, three-quarter, back", then the identity string and the scene's wardrobe, word for word from the bibles.
- Flat, even, neutral light on a plain mid-grey backdrop; no shadows across the face, no props unless the prop is part of the character.
- Crop each view into its own reference file. A whole sheet passed as one reference leaves each view only a few pixels at the size models resize references to.
- Name the crops `<character>-front.png`, `<character>-3q.png`, `<character>-back.png` in `refs/` and list them in the character bible's `refs`. The compiler passes them in that order.
- One sheet per costume. A costume change by scene (costume arc) needs a new sheet for that scene's look.
- Check every sheet at full size before use: same face in all views, the side of every mark (scar, part, mole) correct as the character's own left or right, nothing the text did not ask for.

## Numbers

- Three views is the default; add a profile only if a shot is side-on.
- Generate 2-3 seeds per sheet and keep the one whose three views agree best.

## Vocabulary

- turnaround, model sheet, view (front, three-quarter, profile, back), crop, reference image.

## Pitfalls

- Strong period or genre costumes pull in symbols the text did not ask for (crosses, crests, insignia), even with "no symbols" in the prompt. Describe the plain surface instead and inspect the sheet; clean it if needed (entry clean-references).
- A sheet made under dramatic light bakes that light into every shot that uses it.

## Verify

- Every character with more than one shot has `refs` in the bible pointing at cropped views, and the files exist.
