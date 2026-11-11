# Film analysis pipeline and Gemini video: research (2026-11-11)

Goal: turn a video (local file or YouTube URL) into a written film notation (shots, scenes, camera moves, blocking on a floor plan, set size in character heights, costumes, props, light, edit rhythm, audio layers) good enough to rebuild the set as a game level. Benchmark: a 2D Madness Combat fan film, where an earlier attempt made the first room about 2.5x too wide because nobody measured it.

All sources were accessed on 2026-11-11. **[V]** = checked against a primary page this session. **[U]** = from prior knowledge, not re-checked today; confirm before relying on it.

## 1. Shot and scene detection

| Tool | Status | Notes |
|---|---|---|
| PySceneDetect | **[V]** 0.7.3 (2026-11-08) is listed in the changelog. The download page still shows 0.7.2 (2026-10-11). | Five detectors: Content, Adaptive, Threshold, Histogram and Hash. 0.7.2 changed the Histogram and Hash defaults. The `scenedetect-core` package is discontinued: install `scenedetect` or `scenedetect-headless`. https://scenedetect.com/changelog/ , https://scenedetect.com/download/ , https://www.scenedetect.com/docs/0.7/api.html |
| ffmpeg `select='gt(scene,0.3)'` + `showinfo` | **[U]** | Needs no install. Gives one score per frame. Good for a first pass and for tuning the threshold. https://ffmpeg.org/ffmpeg-filters.html#select_002c-aselect |
| TransNetV2 | **[U]** | A CNN shot detector with PyTorch and TF weights. It handles dissolves better than threshold methods. https://github.com/soCzech/TransNetV2 |
| AutoShot | **[U]** | A NAS-searched successor that reports gains over TransNetV2 on short-form video. https://github.com/wentaozhu/AutoShot |

Animation notes **[U]**: flat cel colour gives low HSV variance inside a shot, so ContentDetector works well on hard cuts. Its false positives come from muzzle flashes, white impact frames and blood splashes, all common in Madness. Mitigations: set AdaptiveDetector `min_scene_len` to at least 8 frames, and check each candidate cut with a second signal, such as a histogram distance taken before and after the flash frame. I found no published benchmark on 2D animation.

## 2. Camera motion classification

- Classic route **[U]**: track features with `cv2.goodFeaturesToTrack` + `calcOpticalFlowPyrLK`, or ORB matches, and fit a homography or affine with `cv2.findHomography(RANSAC)` for each frame pair. Then decompose the fit: mean translation means pan or tilt, scale above 1 means zoom in, and rotation means roll. Dolly versus zoom: a dolly shows parallax (flow residual differs by depth layer), a zoom does not. In side-on 2D animation most "camera" motion is a pure 2D pan or zoom of the background plate, so the homography fit is almost exact. That is good news for this benchmark.
- CameraBench (2025) **[U]**: a taxonomy and dataset of camera primitives (pan, tilt, roll, dolly, truck, pedestal, zoom, orbit, static, shaky) with a VLM benchmark. Its taxonomy is worth copying for the notation vocabulary. https://linzhiqiu.github.io/papers/camerabench/
- I found no maintained pip tool that labels pan, tilt and zoom directly. **[U]** Write the roughly 100 lines in opencv instead.

## 3. Depth and room metrology

| Model | Output | Notes |
|---|---|---|
| Depth Anything V2 | relative (metric fine-tunes exist) | **[U]** https://github.com/DepthAnything/Depth-Anything-V2 |
| Depth Anything 3 (ByteDance Seed, Nov 2025) | any-view geometry; DA3METRIC-LARGE is 0.35B, Apache-2.0 | **[V]** Metric depth = focal_px * net_output / 300, so it needs a focal length. ETH3D delta1 0.917. https://huggingface.co/APaul1/DA3METRIC-LARGE , https://arxiv.org/pdf/2511.10647v1 (the model card is a mirror, not the official org; **[U]** the official repo is ByteDance-Seed/Depth-Anything-3) |
| MoGe-2 | metric point map from one image | **[V]** https://arxiv.org/html/2507.02546v1 |
| Depth Pro (Apple) | metric depth plus focal | **[V]** The MoGe-2 paper says it is sharp but weaker in geometric accuracy (same URL) |
| UniDepth, VGGT | metric (UniDepth), multi-view feed-forward recon (VGGT) | **[U]** |

On cartoons: **[V]** I found no benchmark of any of these on cartoons or 2D animation. **[U]** Side-on cel rooms are orthographic-ish flat paintings, so metric depth models will guess a plausible but invented depth. Do not trust their scale.

Recommended route (classic, no deep model): measure in character heights.
1. Character height in pixels: take the standing bbox height of a Madness grunt in the same shot. Use the median over frames where the figure stands upright, so pose keypoints are not needed.
2. For a flat side-on room, the floor line and walls lie on roughly the same plane as the characters. Room width = wall-to-wall px / character px, measured in a frame where the character stands at the depth of the walls.
3. If the camera pans, stitch a panorama first: chain the homographies from section 2 into one background plate with the characters masked out, then measure on the plate. This is what the 2.5x error needed: the width came from one frame or a guess and was never stitched and measured.
4. For rooms in true perspective, use Criminisi single-view metrology: with a vanishing line plus a vertical vanishing point, ratios of heights on the ground plane are exact, and a known height (the character) fixes the scale. Criminisi, Reid, Zisserman, "Single View Metrology", IJCV 2000. https://www.robots.ox.ac.uk/~vgg/publications/2000/Criminisi00/ **[U]**
5. Use DA3 or MoGe-2 only as a cross-check on live-action input.

## 4. Pose and choreography

- rtmlib: runs RTMPose / RTMO / DWPose through onnxruntime with no torch or mmcv. That is the lightest fit for this machine. **[U]** https://github.com/Tau-J/rtmlib
- MediaPipe Pose Landmarker **[U]**: CPU, 33 landmarks. https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker
- ViTPose **[U]**: higher accuracy, needs torch. 4D-Humans (HMR2) and GVHMR **[U]** give SMPL meshes and world trajectories. They are overkill and fail on non-human proportions.
- On cartoons **[U]**: human-trained detectors often miss Madness grunts, which have no face features, a round head and stick limbs. Expect partial keypoints at best. For blocking (where each figure stands on the floor plan), a person or blob bbox plus colour segmentation (grunt grey, agent black suits) is more reliable than skeletons. Treat keypoints as a bonus.

## 5. Audio

- Dialogue with timestamps **[U]**: faster-whisper (CTranslate2, about 4x faster than openai-whisper, word timestamps) https://github.com/SYSTRAN/faster-whisper ; WhisperX adds forced alignment and diarization https://github.com/m-bain/whisperX . Madness films have little dialogue, so this step is optional.
- Stems **[U]**: Demucs v4 htdemucs https://github.com/facebookresearch/demucs ; BS-RoFormer / Mel-RoFormer, which top the MVSEP charts, through python-audio-separator https://github.com/nomadkaraoke/python-audio-separator
- Sound events **[U]**: PANNs (AudioSet 527 classes, frame-level) https://github.com/qiuqiangkong/audioset_tagging_cnn ; BEATs (Microsoft); CLAP (LAION, zero-shot text labels such as "gunshot", "punch") https://github.com/LAION-AI/CLAP
- ffmpeg alone gives onsets, loudness (ebur128) and silence (silencedetect), which is enough for edit-rhythm versus music-hit analysis.

## 6. Gemini video understanding

Source: https://aistudio.google.com/docs/video-understanding (formerly ai.google.dev/gemini-api/docs/video-understanding) **[V]**

| Item | Value |
|---|---|
| Models | All Gemini models take video. Static 1 fps is the default. "Agentic processing" is on Gemini 4 Carbon, Gemini 4 Argon, 3.8 Flash, 3.6 Flash and 3.5 Flash Lite. |
| YouTube URL | Preview and no charge for the URL fetch. **Public videos only** (no private or unlisted). Free tier: 8 h of YouTube per day. Paid tier: no length limit. Up to 10 videos per request on 2.5+ (1 before 2.5). |
| Files API | 20 GB per file on paid, 2 GB on free. Inline only for requests under 20 MB (the page also shows 100 MB, an inconsistency). |
| Sampling | Default 1 fps. Custom `fps` in the `processing` object (static mode). Clipping with `start_offset` / `end_offset` as strings in seconds ("10.5s"). |
| Tokens | 258 tokens per frame by default, 66 with `media_resolution` low. About 300 tok/s video+audio at default, about 100 tok/s at low. Audio is 32 tok/s (1 kbps mono). |
| Length | On 1M-context models: about 1 h at default resolution, about 3 h at low. |
| Timestamps | `MM:SS` in prompts and answers. |

Pricing per 1M input tokens, Standard paid tier (https://aistudio.google.com/docs/pricing) **[V]**:

| Model id | Input | Output | Free tier |
|---|---|---|---|
| gemini-3.8-flash | $0.75 (to 2026-12-31), then $1.50 | $3.75, then $7.50 | yes |
| gemini-3.6-flash | same as 3.8 | same | yes |
| gemini-3.5-flash-lite | $0.30 | $2.50 | yes |
| gemini-3.1-flash-lite | $0.25 | $1.50 | yes |
| gemini-3.1-pro-preview | $2.00 (≤200k), $4.00 | $12 / $18 | **no** |
| gemini-2.5-flash-lite | $0.10 | $0.40 | yes |
| gemini-2.5-pro / 2.5-flash | deprecated; from 2026-12-01 routed to 3.8-flash and 3.5-flash-lite | | |

The pricing page was truncated at 100k characters. Gemini 4 Carbon and Argon prices were not read **[U]**. Free-tier data is used to improve Google products, except on 3.1 Pro, which has no free tier.

Worked cost: a 3-minute film at default resolution is about 180 s x 300 tok = 54k tokens, about $0.04 on 3.8-flash. At 5 fps for action, the frames cost about 5x that. Free tier first.

Compared with other providers:
- Claude **[V]**: images only, no video input. Up to 600 images per API request (100 on 200k-context models), 20 per turn on claude.ai, 8000x8000 px max, with a lower per-image limit above 20 images. The request limit is 128 MB. https://platform.claude.com/docs/en/build-with-claude/vision . So frames must be sampled by ffmpeg, and audio is not taken.
- OpenAI **[U, not verified]**: the API takes images (frames). I could not confirm native video-file input for GPT models in 2026. Audio is a separate path.
- What only Gemini gives: native video with the synced audio track in one request, a YouTube URL with no download, MM:SS-grounded answers, custom fps and clipping, and hour-scale context.

YouTube terms **[U]**: the docs only say that public videos are allowed. They also link to the Gemini API Additional Terms (https://ai.google.dev/gemini-api/terms) and the YouTube Terms of Service (https://www.youtube.com/t/terms). Downloading with yt-dlp for local analysis is a separate act that YouTube's ToS forbids without permission. Passing the URL to Gemini avoids downloading. Analysing a fan film for notation is fine in practice, but rebuilding someone's set as a published level needs the creator's permission.

## 7. Film breakdown work and notation standards

- MovieNet (ECCV 2020) **[U]**: 1,100 movies, shot-type labels (scale: ECS/FS/MS/CS/LS; movement: static/motion/push/pull) and scene boundaries. https://movienet.github.io/
- MovieShots / shot-type classification (Rao et al. 2020) **[U]**: the source of the scale and movement label set.
- CameraBench (2025) **[U]**: the camera-motion taxonomy, see section 2.
- Notation worth copying **[U]**: the industry shot list (shot #, size, angle, move, lens, subject, action, duration), the AD/continuity "lined script", and EDL / OpenTimelineIO (https://opentimeline.io/) for the cut list. OTIO is a stable machine format for shots plus timecodes and is importable into editors.

## Recommended local pipeline (Windows, RTX 5060 Ti 16 GB)

1. **Already installed** (ffmpeg, opencv, numpy): ffmpeg scene scores, silencedetect, ebur128, frame dumps; opencv homography for camera moves and panorama stitching; bbox-based character-height metrology. 0 VRAM. This step alone fixes the room-width bug.
2. `pip install scenedetect` (CPU): AdaptiveDetector shot list, then OTIO export.
3. `google-genai` + GEMINI_API_KEY: one pass per film at 1-2 fps for semantic notation (costumes, props, light, actions with MM:SS), cross-checked against the local cut list.
4. `pip install rtmlib onnxruntime-gpu`: pose for blocking, under 2 GB VRAM. **[U]**
5. `pip install faster-whisper` plus audio-separator (Demucs or RoFormer): 2-6 GB VRAM. **[U]** torch is needed for Demucs.
6. Optional torch stack (cu128 build for Blackwell **[U]**): TransNetV2, DA3 / MoGe-2 (about 2-6 GB), PANNs/CLAP. Only if steps 1-5 leave gaps.

Ranked: try first
1. Measured room scale: stitch the background, then measure walls in character heights (opencv). Directly fixes the benchmark failure.
2. PySceneDetect AdaptiveDetector with the flash-frame guard.
3. Gemini 3.8-flash YouTube-URL pass for the descriptive notation (free tier).
4. Homography-based pan/tilt/zoom labels in the CameraBench vocabulary.
5. rtmlib pose plus colour segmentation for blocking positions.
6. faster-whisper, stems and PANNs/CLAP for the audio layers.
7. Monocular depth (DA3 / MoGe-2): last, for live-action only; not trusted on cel art.
