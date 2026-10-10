---
title: Shot matching
slug: shot-matching
summary: Match every shot of a scene to one hero frame with a per-shot LUT (cine_post grade match), then one look LUT and grain for the whole film; a look LUT alone never fixes mismatched shots.
tags: [finish, grade, color, lut, matching]
last_checked: 2026-10-09
sources: ["invideo, colour grading workflow for AI-generated video, 2026-07-27", "Houbre, How to color match AI video clips, HackerNoon, 2026-07-30", "Reinhard et al., Color transfer between images, 2001", "local tests on H3 footage, 2026-10-09"]
---

# Shot matching

## Rules

- Order: match, then look, then texture. Each shot is first matched to the scene's hero frame, then the film's one look LUT goes on every shot, then grain.
- Pick the hero frame per scene: the establishing wide, rendered and approved first. Match the scene's closer angles to it, never to a frame from another scene: matching averages the whole picture, so a hero with a big blue sky pulls an interior cool.
- Run `CINE_POST grade match SHOTS --ref hero.png --cube-dir grade/ --apply graded/`. It writes one 17-point `.cube` per shot (ffmpeg, Resolve and Premiere read it) and `grade.json` with the gains. Strength 0.7 by default; 1.0 copies the hero's balance fully and can look forced.
- Light that falls across the story (day into night, a darkening mood): give each scene a mean luma target with `--luma` and record the targets in `finish/grade.md`.
- The look LUT (`--look`) is the film's one creative grade, made once in a grading tool or exported from the hero; apply it at 60 to 80% intensity when building it. Grain last (`--grain 4` to `8`).
- Stats are pooled over the whole shot, so the correction is one fixed transform and does not flicker. Brightness pulsing inside a shot is a separate fix (deflicker); texture shimmer and identity drift are not grading problems: re-render.
- Grade a mezzanine copy; keep the ungraded renders.

## Numbers

- Strength 0.5 to 0.8; per-channel gain is clamped to 0.4 to 2.5 so a near-flat shot cannot blow up its noise.
- Luma targets are 0 to 255 full range (Rec.709 weights), not the 16 to 235 video range scopes show.

## Vocabulary

- shot match, hero frame, look LUT, .cube, mezzanine, luma, grain.

## Pitfalls

- One look LUT on unmatched shots: two different looks with the same tint on top.
- Matching across scenes, or to a frame with very different content.
- Grading the compressed delivery file instead of the mezzanine.

## Verify

- `CINE_POST grade measure` before and after: the scene's shots sit within a few luma points of their target and of each other; a contact sheet of the graded middles reads as one film.
