---
title: MiniMax H3 reference mode syntax
slug: h3-reference-mode
summary: H3 Ref2VA prompt format from the official ref guide: six sections, Subject/Picture/Video/Audio labels, task prefix, retention markers, (Sx) speakers, one source line per element.
tags: [minimax, h3, ref2va, references, syntax, untested]
last_checked: 2026-11-11
sources: ["https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_ref_en.md", "r/StableDiffusion 1vhloyz, PSA: H3 has two prompting guides, 2026-07", "r/comfyui 1ul9iei, previs vs storyboard vs still as reference, 2026-06"]
volatile_claims: ["section names and markers of the ref guide"]
---

# MiniMax H3 reference mode syntax

Read with [minimax-h3](minimax-h3.md). The base guide covers first/last frame; Ref2VA (images, videos, audio as references) has its own guide with a stricter format. Not yet A/B-tested here against the compiler's plain `<Picture N>` tags.

## Rules

- Six sections, in order: `subject_definitions`, `summary`, `retention_analysis`, `detailed_description`, `overall_soundscape`, `non_diegetic_music`. All in English except dialogue inside `<d>` and text visible in the scene.
- Labels: `<Subject N>` reusable visible content (a person, a set, a prop, an action); `<Picture N>` only when the image is itself a frame (first, key, last) or a storyboard anchor; `<Video N>` a whole-video source (edit, continuation, cut structure); `<Audio N>` a copied or referenced sound. A picture that only defines a character is cited inside that `<Subject N>` line, with no line of its own.
- `summary` opens with a task prefix, joined with ` + `: `keyframe completion`, `reference generation`, `video editing`, `video continuation`, `audio reuse`, `audio reference`. A video that gives only camera or rhythm is `reference generation`, not editing.
- `retention_analysis`: one line per label, `<Subject 1> (appears in [Shot 1]): fully_preserved - ...`. Visual markers `fully_preserved`, `partially_preserved`, `attribute_transfer`, `weak_reference`; audio markers `fully_copy`, `partially_copy`, `reference`, `weak_reference`. No `(Sx)` here.
- Speakers: `<Subject 2> (S1) ... says, <d>[English] ...</d>`; ids by order of speech in the target video, reused everywhere; `<Audio 1> is the voice-timbre reference for <Subject 1> (S1).`
- Cuts and speech across them: `[Shot N]` as in the base guide, `<scenetrans>` for dialogue crossing a cut, `<cutoff>` for speech cut off by the end.
- One source line per element when a control or previs video and stills are both given: "motion and camera from <Video 1>; characters and set from <Subject 1>, <Subject 2>" (1ul9iei). It separates how it moves from what it looks like.

## Pitfalls

- A reference video's own sound does not become an `<Audio N>` unless it is reused or referenced.
- `<Video N>` and `<Audio N>` count separately; the same file can be `<Video 1>` and `<Audio 2>`.

## Verify

- Same seed, same refs: compiler prompt vs a hand-written six-section prompt; compare identity hold and set hold on three frames.
