---
title: Layered character passes for many-character takes
summary: Research (2026-10-25) on building a take with more people than a video model holds by adding a few characters per pass. Subject limits in the literature (no benchmark goes past 3), the ways to add people to an existing video, MiniMax H3's native masked inpaint through the Fun ControlNet patch, prior art, and what breaks. Test results are in the Test section.
tags: [research, crowds, battle, inpainting, masks, references, layered-passes, controlnet]
date: 2026-10-25
---

# Layered character passes for many-character takes

Question (the owner, 2026-10-25): free video models hold about 3-5 acting characters per take; past that they clone faces, merge limbs, drop people or swap sides. Does a take built in repeated passes, each adding 3-5 characters to the previous pass, beat one pass with everyone?

Related: builds on [2026-10-13-battle-crowd-compositing](2026-10-13-battle-crowd-compositing.md); see also [crowd-prompting](../../plugins/cinewright/skills/cinewright-genvideo/references/crowd-prompting.md), [crowd-multiplication](../../plugins/cinewright-craft/skills/cinewright-finish/references/crowd-multiplication.md).

## Answer from the sources

- Nobody measures past 3 subjects. OpenS2V-Eval caps each sample at three subject images "because current models can't handle more", and finds fidelity falls as references are added. MAGREF's test set allows at most 3 references; without its disentangling step it shows identity drift, blending and invented extra subjects. LumosX's test set has 50 three-subject videos and none larger. The 3-5 ceiling seen in practice is consistent with this, never measured.
- MiniMax H3 takes up to 9 reference images and states no subject limit. The ComfyUI tutorial says a 4-step turbo run "can barely apply references" and suggests about 25 steps when references matter.
- No paper or practitioner post was found that builds a crowd by layered character passes. VideoAnydoor says objects can be added iteratively but reports no drift analysis; InsertAnywhere inserts one object with matched local light.

## Ways to add people to an existing video

1. Masked inpainting (the route to test first). H3's `MiniMaxH3FunControlNetApply` takes an optional `mask` (1 = regenerate) and `source_video` besides the control video; with both, the masked source is encoded into the control hint, so the model sees what is already there and fills only the hole. The tutorial says unmasked areas stay unchanged and that the patch works with the reference-to-video model too. Exact pixel identity outside the mask is not documented, so composite the source back outside a feathered mask: then earlier characters never go through the VAE again.
2. Wan VACE (`WanVaceToVideo`, control masks plus one reference image) does the same for Wan; the official template composites the result back with `ImageCompositeMasked`. No Wan weights on the test machine.
3. Partial-denoise video-to-video. H3 documents partial denoise only for its latent-upscale refine (0.1-0.5 keeps composition). Low denoise cannot create new people, so it is not an add route.
4. Previous pass as a control video (Canny or depth of pass N into pass N+1). It holds the earlier figures' outlines but also the empty areas, which may resist newcomers. Tested below.
5. Cut-outs and compositing: SAM 3.1 video tracking is native in ComfyUI, MatAnyone 2 (non-commercial licence) and Wan-Alpha are not installed; installing weights needs the owner's yes.

## What breaks, as reported

- Every VAE round trip loses detail; chained continuations accumulate error (H3 docs; arXiv 2512.13604).
- Colour drift after re-encoding (anecdotal, LTX); fix by matching colour to the first pass.
- No measured per-pass loss for H3's VAE.

## Sources

- https://platform.minimax.io/docs/guides/local-deploy-h3.md
- https://docs.comfy.org/tutorials/video/minimax/minimax-h3
- https://docs.comfy.org/tutorials/video/minimax/minimax-h3-fun-controlnet.md
- https://docs.comfy.org/built-in-nodes/MiniMaxH3FunControlNetApply.md
- https://arxiv.org/html/2505.20292v4 (OpenS2V-Eval)
- https://arxiv.org/html/2505.23742v2 (MAGREF)
- https://arxiv.org/html/2504.02436v1 (SkyReels-A2)
- https://arxiv.org/pdf/2603.20192 (LumosX)
- https://huggingface.co/tencent/HunyuanCustom/blob/main/README.md
- https://docs.comfy.org/ja/built-in-nodes/conditioning/video-models/wan-vace-to-video.md
- https://comfy.org/es/workflows/video_wan_vace_inpainting-a1bb55d904c9/
- https://docs.ltx.io/open-source-model/advanced-workflows/in-outpainting
- https://docs.comfy.org/tutorials/utility/video-segment-sam3
- https://arxiv.org/html/2501.01427v4 (VideoAnydoor)
- https://arxiv.org/abs/2512.17504 (InsertAnywhere)
- https://arxiv.org/pdf/2512.13604
- Unverified: Phantom's 4-subject cap (secondhand tutorial), Kling O1's 7 elements (aggregator).

## Test (2026-10-25)

One shot, 10 spearmen in a line against 10 wild creatures charging from the right (the owner: no formation, they attack as efficiently as possible). MiniMax H3, 608x352, 73 frames, 4-step turbo LoRA, one seed for every take. Six single-figure reference sheets (three per side). People counted by eye on frames 1, 28 and 56; the full table, grids and run log are in the owner's private test folder.

| Take | Spearmen | Creatures | Notes |
|---|---|---|---|
| one prompt, no refs | 8 / 8 / 5 | 0 / 3 / 4 | every spearman one clone; creatures as mannequins |
| one prompt, 3 refs | 9 / 9 / 8 | 0 / 3 / 5 | creatures arrive late |
| one prompt, 5 refs | 9 / 9 / 8 (one rank) | 1 / 3 / 6 | most look variety |
| four masked passes, composited | 5 / 5 / 5 | 0 / 3 / 5 | pass 3 added nobody and repainted the front rank; newcomers cut off at the mask edge |
| pass 2 with pass 1's edges as control | 5 | 4-5 | the earlier people redrawn |
| blockout depth 0.6/0.4, no refs | 8 / 7 / 6 | 3 / 4 / 5 | clones, mannequins |
| blockout masks over that take | as above | as above | the masks did not line up with the drawn figures |
| blockout depth 0.6/0.4 + refs | 7 / 7 / 6 | 5 / 6 / 5 | two figures see-through late |
| **blockout depth 0.8/0.6 + refs** | **10 / 11 / 10** | **5 / 8 / 6** | two ranks; a few extra far figures late; creatures still man-height |

Time: a plain draft 34-40 s of GPU, a masked pass 53-74 s, the blockout 9-15 s of CPU.

**Verdict: layered passes do not work for this.** A region mask cannot add people behind people (the common case in a battle); anyone crossing the mask edge is cut off in the composite, and without the composite the model moves the earlier people; each pass adds fewer than asked. The masked add works for a narrow job: a few figures into empty space of an approved take, composited so the earlier people keep their own pixels. The route for more than about 5 acting people is the 3D blockout with its depth at 0.8 plus one or two reference sheets per side, in one render. Untested: a mask video that moves with the newcomers, taken from a blockout the render follows exactly (0.8 or more).

What changed: cinewright `cards validate` warns CAST-COUNT above 5 acting people (cast plus numbers before a people noun); crowd-prompting carries the route and the numbers; the private image-generation skill wires the inpaint inputs into its H3 driver; polywright `pw.py crowd` takes per-side looseness, kit, height and stagger (`--jitter-b`, `--kit-b`, `--scale-b`, `--stagger-b`).
