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

- Provenance first: `AN probe VIDEO` prints container tags; run `c2patool` if it is installed. A C2PA manifest naming a generator is decisive. A missing manifest proves nothing (re-uploads strip it). Camera make and model tags count against AI, weakly.
- SynthID (Google) can only be checked through Google's portal; Video Seal finds only Meta's mark. Say so instead of claiming a check you cannot run.
- Format hints, weak alone: Veo clips are 4, 6 or 8 s at 24 fps, 720p or 1080p. Many generators make 5 or 10 s clips; a long take with no cut is less likely to be generated.
- Frame checklist (sample 16-32 frames, plus pairs a few frames apart): text that warps or changes between frames; hands and fingers; objects that appear, vanish or merge; physics (liquids, cloth, contact, weight); texture that boils while the camera is still; faces or clothes that drift; background that morphs during a camera move; shadows or reflections that disagree with the light; skin and surfaces too smooth.
- Answer in bands: "strong signs of generation", "some signs", "no clear signs", with the top three timestamps and what each shows. Never say "this is AI" or "this is real" from tells alone.
- False positives: heavy compression, 2D or 3D animation, VFX, phone beautification, frame interpolation and screen recordings all produce some tells. Name the medium before scoring.
- Open detectors (UnivFD per frame, AIGVDet) lose a lot on generators they were not trained on; count their score as one weak signal.
- Breaking down an AI video for study: run the same notation steps and add the likely generator and clip length to the source notes.
