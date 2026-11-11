---
title: AI-made video tells
slug: ai-video-tells
summary: How to judge whether a video is AI-generated: provenance first, then a frame checklist (text, hands, permanence, physics, boiling, identity drift, light), answered in confidence bands with timestamps.
tags: [analysis, ai-detection, provenance, qc]
last_checked: 2026-11-11
sources: ["https://c2pa.org/specifications/", "https://blog.google/technology/ai/google-synthid-ai-content-detector/", "https://github.com/facebookresearch/videoseal", "https://github.com/multimediaFor/AIGVDet", "https://cloud.google.com/vertex-ai/generative-ai/docs/models/veo/3-0-fast-generate-001", "cinewright ai-docs/research/2026-11-11-ai-video-detection.md"]
---

# AI-made video tells

## Rules

- Run `AN aidetect VIDEO --out DIR` first: it reads tags (ComfyUI workflow, generator names, phone make and model), runs c2patool when installed, samples 32 frame pairs, scores and writes report.json plus a 4x4 contact sheet for the checklist below. Its score is one input to the bands, not the answer.
- Calibration 2026-11-11 (21 generated clips: 16 of our MiniMax H3 and LTX renders, 5 Sora; 3 phone clips plus re-encodes): metadata decided almost everything. A ComfyUI `prompt` tag naming the model was on 13 of 16 of our renders; Pixel clips carry `com.android.model`. Of the picture signals only the high-frequency share of the luma spectrum (hf_ratio at 480 px wide) separated them: Sora 0.002-0.005, ours 0.008-0.045 (median about 0.014), phone 0.020-0.035, and a phone clip re-encoded small at CRF 35 fell to 0.018. Scored band: 0.020 camera-like to 0.008 generator-like. Flow-warp residual, homography inliers and motion jerk overlapped and are reported raw, not scored. With tags stripped our renders score about 0.5 (inconclusive): expect that, do not tune it away on three phone clips.
- Provenance first: `AN probe VIDEO` prints container tags; run `c2patool` if it is installed. A C2PA manifest naming a generator is decisive. A missing manifest proves nothing (re-uploads strip it). Camera make and model tags count against AI, weakly.
- SynthID (Google) can only be checked through Google's portal; Video Seal finds only Meta's mark. Say so instead of claiming a check you cannot run.
- Format hints, weak alone: Veo clips are 4, 6 or 8 s at 24 fps, 720p or 1080p. Many generators make 5 or 10 s clips; a long take with no cut is less likely to be generated.
- Frame checklist (sample 16-32 frames, plus pairs a few frames apart): text that warps or changes between frames; hands and fingers; objects that appear, vanish or merge; physics (liquids, cloth, contact, weight); texture that boils while the camera is still; faces or clothes that drift; background that morphs during a camera move; shadows or reflections that disagree with the light; skin and surfaces too smooth.
- Answer in bands: "strong signs of generation", "some signs", "no clear signs", with the top three timestamps and what each shows. Never say "this is AI" or "this is real" from tells alone.
- False positives: heavy compression, 2D or 3D animation, VFX, phone beautification, frame interpolation and screen recordings all produce some tells. Name the medium before scoring.
- Open detectors (UnivFD per frame, AIGVDet) lose a lot on generators they were not trained on; count their score as one weak signal.
- Breaking down an AI video for study: run the same notation steps and add the likely generator and clip length to the source notes.
