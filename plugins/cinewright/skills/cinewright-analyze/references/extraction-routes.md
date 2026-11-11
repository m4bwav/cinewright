---
title: Extraction routes
slug: extraction-routes
summary: Which tool extracts what from a video: ffmpeg or PySceneDetect for cuts, frames plus a vision model for content, Gemini for video with audio and YouTube links, Whisper for dialogue.
tags: [analysis, gemini, extraction, audio, tools]
last_checked: 2026-11-11
sources: ["https://aistudio.google.com/docs/video-understanding", "https://aistudio.google.com/docs/pricing", "https://ai.google.dev/gemini-api/terms", "https://scenedetect.com/changelog/", "https://docs.claude.com/en/docs/build-with-claude/vision"]
---

# Extraction routes

## Rules

- Cuts and timecodes: local first (`AN shots`; PySceneDetect 0.7 adds adaptive and histogram detectors). Never let a model invent timecodes the shot list can measure.
- Content (who, what, props, text): sampled frames read by a vision model. Claude takes images only, no audio, up to 600 images a request; send frames, not the video.
- Gemini is the one route that takes the video with its synced audio, and public YouTube URLs without downloading (up to 10 per request). It samples 1 frame per second by default (a custom fps and clip start and end can be set); about 300 tokens a second with audio, 258 per frame (66 at low resolution), so about an hour per 1M-token request. Answers cite MM:SS. Use it to draft per-shot descriptions and dialogue for long films; check its timecodes against `AN shots` and never take sizes from it.
- Gemini model ids and prices change monthly: read the pricing page before a run and record the model id in the notation. A short film costs cents; stop and ask before any run over a few dollars.
- Dialogue with timestamps: faster-whisper or WhisperX locally. Music and effects stems: Demucs or BS-RoFormer. Sound events: CLAP or PANNs tags.
- Pose and blocking: rtmlib (RTMPose on onnxruntime) on live action; on cartoons pose models are unreliable, so mark positions by hand on the floor plan.
- Terms: the source film's art, logos and characters never enter a repo or a rebuild; keep downloads in a work folder and record only measurements and descriptions.
