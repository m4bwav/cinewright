---
title: Fight planning documents, AI fight practice and 3D previs
summary: Research (2026-10-15) on what fight choreographers write down, how people make AI fight video work in 2025-2026, and how 3D and motion capture could drive it; Gemini's three document claims checked; what cinewright adopted (fight plan, cine_fight.py) and what it rejected.
tags: [research, fights, choreography, notation, previs, stuntvis, reference-video, scail, adaptation]
date: 2026-10-15
---

# Fight planning documents, AI fight practice and 3D previs

Question (the user): improve the depth of cinewright's fight choreography and the documents it makes. Gemini named three document types (written combat notation, "reversal of fortune graphs", "timeline moments"). Check them, find how people improve AI fight scenes and plan them, research 3D modelling for fights, connect other plugins where it helps, and keep anything that would confuse agents or generators out. Test run: a duel from a novel.

Method: three web research passes (choreography documents; AI fight practice from forums, model docs and makers; 3D and motion capture), each claim labelled tested, vendor, paper or inference. Full notes with every link stay in the private sidecar (they name the maintainer's hardware); this note keeps the findings and sources that shipped entries cite.

## Gemini's three claims

| Claim | Verdict | What is real |
|---|---|---|
| Written combat notation: a narrative plan "operator first", a tabular plan with a column per fighter and an arrow between | Verified, wording inflated | David McCormick (FDC-certified), "Recording Choreography", Academie Duello, 2015 ([archive](https://web.archive.org/web/20150311201049/http://www.academieduello.com:80/news-blog/recording-choreography/)). Narrative: `1: I. cut L arm, W. parry 3`. Tabular: `Move | Inigo | vs | Wesley | Notes` with an arrow of intention, "the most popular format in Fight Directors Canada". Gemini's example row is invented. Other systems: five cut targets and +/- diagrams (Weapons of Choice textbook), a notation chapter in Hobbs, *Fight Direction for Stage and Screen* (1995, not read). |
| Reversal of fortune graphs | Not found as a document; real as a practice | Fights are split into phrases separated by pauses, each with a "story decision" (the villain turns the tables by cheating); plan from the end; ask an emotional question, not who wins; "the good guys must almost lose" (McCormick, [Plot in Choreography](https://web.archive.org/web/20131023003111/http://www.academieduello.com/news-blog/plot-in-choreography/), [Action Logic](https://web.archive.org/web/20160815083821/http://www.academieduello.com/news-blog/fight-choreography-action-logic/)). Pro wrestling's shine, heat, hope spot, comeback, finish is the same idea. All written as text. |
| Timeline moments spreadsheets; a "Crossbow" channel | Not found | Real equivalents: animatics cut to the song with stunts timed to it (Baby Driver, [Art of the Cut](https://www.provideocoalition.com/aotc-baby-driver/)); animation bar sheets (12 frames a beat at 24 fps is 120 BPM); stuntvis edits ([VFX Voice 2018](https://vfxvoice.com/?p=3123357)); counted move sequences. FDC advice: do not put every contact on the beat. |

Rhythm: David Bordwell's pause, burst, pause for Hong Kong action (*Planet Hong Kong*, 2000). Jackie Chan via Tony Zhou ([Every Frame a Painting, 2014](https://www.youtube.com/watch?v=Z1PCtIaM_GQ)): action and reaction in one frame, two good hits cut together read as one great hit, start at a disadvantage.

Novel to film: inner tactics become lines or visible changes (The Princess Bride); a world's combat rule becomes the visible style (Dune's shield, [Villeneuve](https://abs-cbn.com/entertainment/10/25/21/dune-combat-inspired-by-ph-martial-art-says-director)); cheats that make a fight one-sided are cut (Feyd's poison in Dune: Part Two); dialogue that slows a fight is cut and each half gets its own intent (Witcher Blaviken, [Hissrich](https://comicbook.com/gaming/2020/01/13/netflix-witcher-geralt-renfri-fight-blaviken-breakdown-lauren-hissrich-interview)).

## How people make AI fights work (2025-2026)

- Hosted models: plan in images, render multi-shot. A 4x4 storyboard grid (shot size, camera arrow, rhythm tag per cell) given to Seedance 2.0 gave about four times the cuts of a prose prompt (Atlas Cloud, 2026-06-12, one vendor A/B). The same recipe ships as an agent skill, `muapi-ai-fight-scene` (SamurAIGPT/Generative-Media-Skills, MIT): never two wides in a row, every impact on a CU or ECU. Kling 3.0 multi-shot: define each subject once, never switch to pronouns.
- The most cited AI fight (a Seedance celebrity rooftop fight, Feb 2026) is disputed: its maker says text only; critics found the same choreography as stunt performers' green-screen footage on the vendor's own site.
- Local MiniMax H3 (r/StableDiffusion, Aug-Sep 2026, tested by users): punches "never really land" in plain prompts; one user got them to land with every hit and reaction on its own timecode, 50 steps and one action LoRA ([thread](https://www.reddit.com/r/StableDiffusion/comments/1vsjezd/)); turbo LoRAs changed the moves themselves; distant fighters smear (the H3 team calls it a model-level issue); a 12 s reference fight was not followed, 6 s pieces were ([thread](https://www.reddit.com/r/StableDiffusion/comments/1vnzx6w/)); a face swap into a fight put one face on both fighters, fixed by per-shot timestamps naming who is where and 5-10 s swaps ([thread](https://www.reddit.com/r/StableDiffusion/comments/1w8p67n/)).
- Reroll budgets reported: 3 to 8 per fight shot; makers often cut the best seconds of several takes together.
- Planning documents makers use: intent, action, reaction triplets (a 15-20 s duel is 6-9 shots, [Hackernoon](https://hackernoon.com/how-to-cover-a-fight-scene-in-ai-generated-video-so-the-audience-can-follow-it)); an end-state contract per shot whose accepted last frame seeds the next (cinewright already does this with start and end states); one sheet per fighter per state, one per prop.
- No ComfyUI node for fight choreography exists.

## 3D, motion capture and pose control

- SCAIL and SCAIL-2 (zai-org, Wan 2.1 base, open, native in ComfyUI): driven by a 3D skeleton drawn as coloured cylinders, one colour per person, which keeps occlusion between two bodies; the paper names fighting as a target case; a Blender rig renders its pose directly ([issue #30](https://github.com/zai-org/SCAIL/issues/30)). Wan-Animate-2 (2026-08) claims multi-person driving. None tested on fights.
- Motion sources an agent can use: Mixamo (royalty-free in films, no redistribution, no API: a one-time manual download), CMU BVH, free fight packs; Cascadeur (free tier non-commercial, no headless mode); NVIDIA Kimodo (text plus keyframe and contact constraints, single person, commercial-use weights). Two-person interaction models are research-only licences.
- Video to motion: GVHMR (about 8 GB) via ComfyUI-MotionCapture; person tracking swaps fighters at contact; no benchmark for fast strikes.
- Weapons have no skeleton. A 1 m blade at full-shot distance is about 11 px wide at 832 px in depth (about 1.4 latent cells): likely lost. Ideas, all untested: thicker blades in control passes only, a weapon mask pass, a pinned impact still.
- PrevizWhiz (Autodesk Research, CHI 2026, [arXiv](https://arxiv.org/html/2602.03838v1)): rough 3D plus skeleton or depth into Wan Fun Control or VACE; 7 of 10 users preferred the mode that follows the blocking.

## What cinewright adopted

- A fight plan file per fight (`shared/schemas/fight-plan.schema.json`): question and ending first, phrases with `ahead`, `margin`, `why` and the pause, exchanges operator first with `with`, target in body words, answer, result, and changes (hands, worn props, marks, posture, side). This is McCormick's tabular plan plus his story decisions, made checkable.
- `cine_fight.py` (shipped only in cinewright-movement): `check` replays the fight (weapon used after it left the hand, phrase length and order, one-sided fights) and holds cards to it (held props, sides, marks copied verbatim, exchanges per card, length, cut order); `sheet` writes the grid and a CSV of the ahead score over time.
- The "reversal graph" became a derived view, not a document: a step chart of the CSV, drawn by chartwright for people reviewing the arc. Nothing from it goes into prompts.
- Entries fight-plan, fight-from-a-book, fight-previs; two lines in fights-and-stunts.

## What cinewright rejected, and why

- Parry numbers and target codes: no video model knows them; plain body words only.
- Per-second spreadsheets with cause and effect prose: a model cannot hit a timestamp inside one generation; timing lives at card cuts, and the extra prose leaks into prompts.
- Safety columns: no performers to protect.
- Coloured multi-series graphs: one score per phrase does the job.
- Shipping 3D routes as rules before a single local test: fight-previs marks the 3D route untested and names the first test.

## Plugin links

- readwright: reads only the fight sections of a book and gives line numbers for each exchange's `src`.
- chartwright: `cw.py build --chart step --target vega-lite --data <id>.csv --x time_s --y ahead_score`, then `cw.py render` to PNG (tested 2026-10-15).
- polywright: proposed `pw.py duel`, a two-fighter Blender staging that renders depth (weapons included), per-fighter and weapon masks, COCO and SCAIL-style pose from the bones, clay and a contact-gap report from a fight plan plus animation clips. About 650 lines for v0. Not built: the first H3 depth test with swords decides whether it is worth it.

## Open tests (in order)

1. H3 with Fun ControlNet Union on a depth video of two fighters with swords, normal against thickened blades; does the blade survive and the hit land on the planned frame.
2. H3 fight card: every hit on its own timecode, 30-50 steps, no speed LoRA, against the same card in plain prose; same seed, scored with `qc judge`.
3. A 3-4 panel storyboard reference against prose on one H3 fight card.
4. SCAIL-2 at 16 GB with a two-person Blender rig render of one throw.
5. A self-recorded 5 s exchange through H3 reference video against Wan Animate.

Related: builds on [2026-10-14-violence-healing-flight](2026-10-14-violence-healing-flight.md), [2026-10-13-battle-crowd-compositing](2026-10-13-battle-crowd-compositing.md).
