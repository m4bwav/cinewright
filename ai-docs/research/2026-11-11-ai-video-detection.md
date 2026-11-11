# AI video detection: research for `aidetect`

Accessed 2026-11-11. Each claim cites a URL. **[UNVERIFIED]** means I did not confirm it against a primary source in this pass. It comes from memory or from secondary coverage only. Check those claims before relying on them.

## 1. Provenance

### C2PA content credentials

| Item | Finding | Source |
|---|---|---|
| Sora | OpenAI says every Sora video carries visible and invisible signals and C2PA metadata | https://openai.com/index/launching-sora-responsibly/ , https://openai.com/index/creating-with-sora-safely |
| Sora (field test) | A hobbyist test found no C2PA in downloads that carry the visible watermark. It found C2PA only in Pro downloads with no watermark. Treat as contested. | https://www.lesswrong.com/posts/kSvrmiyyN7CDyh3NN/openai-does-not-appear-to-be-applying-watermarks-honestly |
| Sora product | Secondary reporting says the Sora product closed on 2026-04-26 **[UNVERIFIED on openai.com]** | (search summary of openai.com/index/creating-with-sora-safely) |
| Fragility | C2PA lives in the file container. Social uploads and re-encodes strip it. | https://nofilmschool.com/sora-2-watermarks |
| Veo, Runway, Firefly, Kling | Adobe Firefly attaches Content Credentials. Veo carries SynthID and probably C2PA. Runway and Kling: **[UNVERIFIED]**. |  |
| Reading tools | `c2patool <file>` (Rust CLI) and `c2pa-python` read manifests from MP4/MOV. **[UNVERIFIED in this pass]**: repos github.com/contentauth/c2patool and github.com/contentauth/c2pa-python |  |

**Rule:** a valid manifest that names a generator is strong evidence of AI. A missing manifest is **no evidence** either way.

### Invisible watermarks

| System | Status | Source |
|---|---|---|
| Google SynthID Detector | Portal announced at I/O on 2025-05-20 (upload media, check for SynthID). Video detection came later. Public access dates in secondary sources disagree (Oct 2026). A partner Content Detection API is in preview. There is no public bulk API. | https://blog.google/technology/ai/google-synthid-ai-content-detector/ , https://infoq.com/news/2026/05/google-synthid-content-detection |
| Meta Video Seal | Open source under the MIT licence: models, training and inference code. ChunkySeal and PixelSeal added in Dec 2025. Detects only Meta-seal marks, which are rare in the wild. | https://github.com/facebookresearch/videoseal , https://facebookresearch.github.io/meta-seal |

Practical upshot: a local script cannot detect SynthID. Use the portal by hand for suspected Google output.

### Metadata and format tells (weak, easily removed)

| Generator | Typical output | Source |
|---|---|---|
| Veo 3 / 3 Fast | 4, 6 or 8 s; 720p or 1080p; 24 fps | https://cloud.google.com/vertex-ai/generative-ai/docs/models/veo/3-0-fast-generate-001 |
| Kling | 5 s or 10 s clips | **[UNVERIFIED]** |
| Hailuo/MiniMax | about 6 s or 10 s, 768p or 1080p | **[UNVERIFIED]** |
| Wan 2.x | 81 frames at 16 fps (about 5 s), 480p/720p | **[UNVERIFIED]** |
| LTX | frame counts of the form 8n+1, often 24/25 fps | **[UNVERIFIED]** |
| Runway Gen-4 | 5 s or 10 s | **[UNVERIFIED]** |

ffprobe checks: `format_tags` (encoder, e.g. `Lavf`, `Google`), `handler_name`, missing camera make/model/GPS, missing `creation_time`, no audio track (or synthetic audio). These checks only lean one way: phone footage normally carries make and model atoms (**[UNVERIFIED]** per device), and their absence is weak evidence.

## 2. Visual tells and how to measure them

Most of these rows are engineering proposals. They are not validated in the literature, and the weights below are guesses to calibrate.

| Tell | Automatic measurement | Deps |
|---|---|---|
| Gibberish or warping text | Run OCR on keyframes and track the edit distance of the same region across frames. AI text mutates. | tesseract/easyocr (optional) |
| Hands and fingers | Count fingers with a hand-pose model. Flag counts other than 5 and jitter in the keypoints. | mediapipe (optional) |
| Object permanence | Track objects with a detector and tracker. Flag tracks born or killed mid-frame with no occlusion or edge exit. | YOLO (optional) |
| Temporal flicker / texture boiling | Warp frame t to t+1 with optical flow (`cv2.calcOpticalFlowFarneback`). The residual energy in static or textured regions is high for AI. | opencv |
| Background morphing during camera moves | Fit a homography (ORB + RANSAC) between frames. A low inlier ratio when global motion is large signals morphing. | opencv |
| Too-smooth or floaty motion | Take the second derivative of mean flow magnitude. Very low jerk combined with a lack of camera shake is suspicious. | opencv |
| Identity drift | Compute the cosine distance of face embeddings over time against the first frame. | insightface (optional) |
| Over-smooth skin | Measure Laplacian variance in face boxes relative to the whole frame. | opencv |
| Lighting/shadow mismatch | Hard to automate. Leave it to a VLM or reviewer. | none |
| Physics violations | Leave to a VLM or reviewer (liquids, collisions, gravity). Physics-IQ-style tests show models fail at this **[UNVERIFIED]**. | none |
| Frequency artefacts | Compute the azimuthal average of the 2D FFT on the luma channel. Look for periodic peaks and high-frequency roll-off from upsampling. | numpy |

AIGVDet backs the use of optical flow: it pairs a spatial detector with a RAFT optical-flow ResNet50 detector, which shows that flow carries the signal. Source: https://arxiv.org/abs/2403.16638

### Reviewer / VLM checklist (apply to 8-16 sampled frames plus a 1 fps contact sheet)

1. Read every sign and label. Does the text stay the same between frames?
2. Count the fingers. Check where each hand meets the object it holds.
3. Does any object appear, vanish, merge or change count?
4. Do faces, clothes and accessories stay the same throughout the shot?
5. Do shadows agree with the light sources? Do reflections match?
6. Do the background buildings and lines keep their geometry while the camera moves?
7. Is the motion physically plausible (weight, contact, liquid, hair)?
8. Is the skin poreless and waxy? Is everything too perfectly lit?
9. Are there signs of real capture (sensor noise, rolling shutter, focus hunting, lens dirt)?

Answer each item as `seen / not seen / can't tell`. Never output a bare "AI" verdict.

## 3. Research detectors and benchmarks

| Work | What it is | Weights | Source |
|---|---|---|---|
| GenVideo + DeMamba | Million-scale dataset. Trains on 10 generators and tests on 10 others. DeMamba is a detail module for detecting generated video. | Code + data on GitHub **[weights UNVERIFIED]** | https://arxiv.org/abs/2405.19707 , https://github.com/chenhaoxing/DeMamba |
| GenVidBench | Up to 6.78M videos in v3 (v1 had 143k). Cross-source/cross-generator splits. Benchmarks VideoSwin, UniformerV2 and DeMamba. | Dataset | https://arxiv.org/abs/2501.11340 , https://genvidbench.github.io/ |
| AIGVDet | Two ResNet50 branches (spatial + RAFT flow), 11 generators | Repo stated in the paper; probably runs on 16 GB | https://arxiv.org/abs/2403.16638 , https://github.com/multimediaFor/AIGVDet |
| UnivFD | Linear probe on CLIP ViT-L/14 features. Image-level, frame-wise. Easily fits in 16 GB. | Yes | https://github.com/Yuheng-Li/UniversalFakeDetect (CVPR 2023) |
| SynthForensics (2026) | Detectors lose about 29 AUC points on fully synthetic video. Some score below chance. Heavy compression costs more than 30 points. | Benchmark | https://arxiv.org/abs/2602.04939 |
| DIRE-for-video, VidGuard | **[UNVERIFIED in this pass]** |  |

### Commercial tools

The "Fit for Purpose?" study (Oct 2025) found that academic and government detectors scored a best AUC below 0.75 on real political deepfakes. Paid tools did better, but all of them generalized poorly. Source: https://arxiv.org/abs/2510.16556. I did not verify per-vendor numbers for Hive, Reality Defender, Sensity or TrueMedia. TrueMedia.org reportedly shut down in early 2025 **[UNVERIFIED]**. Vendor accuracy claims are marketing until third parties test them.

Takeaway: no detector generalizes reliably to generators it has not seen. A learned score is one signal, never a verdict.

## 4. Model-specific tells

I found no primary documentation for model-specific tells in Veo 3, Sora 2, Kling 2.x, Hailuo, Wan 2.x, Runway Gen-4, Seedance or LTX-2. Everything in this section is **[UNVERIFIED]**. The only usable fingerprints are the format ones in section 1: duration, fps and frame count. Our own cinewright renders (Wan, LTX, MiniMax H3 on the local box) can serve as labelled positives to learn them empirically.

## 5. False-positive sources

| Source | Why it fools signals | Mitigation |
|---|---|---|
| Heavy compression / re-uploads | Destroys noise and high frequencies and adds blocking. The 2025 study shows that JPEG compression and enhancement reduce detector performance. | Lower confidence when bitrate per pixel is low. Source: https://arxiv.org/abs/2507.21905 |
| Animation, CGI, games | No sensor noise, perfectly smooth motion, clean text | Detect "non-photographic" content and report it as out of scope |
| VFX composites, stabilization | Homography breaks, warped backgrounds | Treat warp signals as weak |
| Phone beautification, portrait mode, frame interpolation (60/120 fps) | Smooth skin, depth blur, interpolation flicker | Down-weight skin and smoothness signals |
| Screen recordings, slideshows, timelapse | Odd fps and missing metadata | Metadata signals carry low weight |

## 6. Scoring design

Each signal outputs a value in [0,1] and a reliability factor in [0,1] (lowered by compression, short duration or no faces). Combine the signals as a weighted log-odds sum with a prior of 0.

| Signal | Weight (start, to calibrate) |
|---|---|
| C2PA manifest naming an AI generator | decisive (report alone, score ≥0.95) |
| Visible watermark (Sora/Veo/Kling logo found by template match) | strong (+3) |
| Learned detector (UnivFD/AIGVDet, optional) | +1.5 |
| Flow-warp residual (boiling) | +1.0 |
| Homography inlier collapse during camera motion | +1.0 |
| OCR instability | +1.0 (only when text is present) |
| Identity drift | +0.8 (only when faces are present) |
| Frequency peaks | +0.5 |
| Format fingerprint (duration/fps/res matches a known generator, no camera atoms) | +0.5 |
| Camera make/model atoms present | -0.7 |

Confidence language. Never say "is AI" or "is real". Report the score band together with the top three pieces of evidence and their frame timestamps.

- ≥0.9 with provenance: "Content credentials state this was generated by X."
- 0.75-0.9: "Several independent signs consistent with AI generation."
- 0.4-0.75: "Inconclusive; some signs present."
- <0.4: "No strong signs found. This does not show the video is authentic."

Always add the caveats: compression level, out-of-scope content (animation), and that detectors miss unseen generators.

## 7. Minimal v1 (ffmpeg + opencv + numpy only)

1. `ffprobe -show_format -show_streams -of json`. Record duration, fps, resolution, frame count, encoder and handler tags, audio presence and camera atoms. Then match against the format table.
2. If `c2patool` is on PATH, run it. Otherwise skip that check.
3. Sample N=32 frames evenly, plus pairs of consecutive frames at each sample.
4. Per pair, compute the Farneback flow-warp residual (median over low-gradient and textured masks) and the ORB+RANSAC homography inlier ratio, weighted by global motion magnitude.
5. Per frame, compute the FFT radial profile peakiness and the Laplacian-variance ratio.
6. Estimate compression from bits per pixel per frame. It sets the reliability factor.
7. Combine the scores as in section 6. Write `report.json` plus `evidence/` holding the top-k frames by signal with flow and residual heat-map overlays, and a 4x4 contact sheet for a VLM or reviewer using the checklist in section 2.
8. Calibrate thresholds on our own renders as positives and phone footage as negatives before trusting any number.
