---
title: S2 model verification from vendor docs
kind: research
status: active
date: 2026-10-03
verified: 2026-10-03
stale_after: 2026-10-17
tags: [models, genvideo, veo, omni, kling, seedance, runway, luma, h3, wan, ltx2]
summary: "Read before editing a genvideo model card: what each vendor's own docs said on 2026-10-03, with sources, conflicts and what stayed unverified"
---

# S2 model verification from vendor docs

Four subagents checked the models on 2026-10-03, each from the vendor's own pages, two or three models apiece. The summaries below are condensed. Each model card's `sources` lists the URLs.

## Veo 3.1 (Google)

- Vertex GA `veo-3.1-generate-001` and `veo-3.1-fast-generate-001` were released 2025-11-17 and retire "November 17, 2026 or later". `veo-3.1-lite-generate-001` has been in preview since 2026-04-02 and takes no refs. The Gemini API preview IDs (generate, fast, lite) shut down on 2026-10-22. Source: docs.cloud.google.com .../veo/3-1-generate and ai.google.dev/gemini-api/docs/deprecations.
- Durations are 4, 6 or 8 s. On the Gemini API, 1080p, 4k, refs and extend force 8 s; Vertex states the 8 s rule only for refs. Output is 720p, 1080p or 4k, 16:9 or 9:16, at 24 fps. Vertex lists Fast at 720p and 1080p only, but both price lists show a Fast 4k price, so Google's own docs conflict.
- Up to 3 refs of type `asset`. No `style` type appears on any 3.1 page. The model also takes `image` plus `lastFrame`. Extend adds 7 s (Gemini API: 720p input, up to 148 s total; Vertex: up to 37 s total). The seed is a uint32 and `negativePrompt` is a Vertex parameter. The 1,024-token prompt limit is stated only on the Gemini API.
- Vertex prices per second (standard with audio / video only; fast with audio / video only): 720p and 1080p $0.40 / $0.20; fast 720p $0.10 / $0.08, fast 1080p $0.12 / $0.10; 4k $0.60 / $0.40.
- Google's three guides give three dialogue forms. The Cloud blog quotes the line (`A woman says, "We have to leave now."`). The Gemini API uses `Man: (Hand on his hunting knife) "That's no ordinary bear."`. The Vertex guide drops the quotes (`the man in the red hat says: Where is the rabbit?`). The card keeps the Vertex form because the target is Vertex GA. Sound is written `SFX: ...` and `Ambient noise: ...`. Several shots go in timestamp blocks `[00:00-00:02]`.

## Gemini Omni Flash (Google)

- `gemini-omni-1.1-flash` was released 2026-08-27 and is stable on the Gemini API, which calls it the default video model and keeps Veo for "scene extension, last-frame control, or legacy pipelines". The preview alias is `gemini-omni-flash-preview`. On Vertex it exists only as `gemini-omni-1.1-flash-preview`. Source: ai.google.dev/gemini-api/docs/video, /docs/models/gemini-omni-flash, /docs/omni.
- The endpoint is the Interactions API (`POST /v1beta/interactions`). `response_format` sets the aspect ratio and resolution, and `video_config.task` is one of text_to_video, image_to_video, reference_to_video, edit or extend.
- Output is 3-10 s, set by the prompt (there is no duration parameter). Extend adds up to 10 s, to 40 s total. Resolutions are 360p, 720p, 1080p (upscaled) and 4k (upscaled); aspect 16:9 or 9:16; 24 fps.
- Refs go in prompt tags: `<IMAGE_REF_N>` (no stated maximum; the guide's example uses 6), up to 3 `<VIDEO_REF_N>` of 3 s or less, and `<FIRST_FRAME>` / `<LAST_FRAME>`. There are no audio refs. No seed is documented and there is no negative prompt ("Do not do X" goes in the prompt).
- Price: $17.50 per 1M output tokens, which is about $0.034, $0.10, $0.15 and $0.30 per second at 360p, 720p, 1080p and 4k.
- Prompting: the model cuts between shots by default, so add "In a single continuous shot" for one. Timecodes have no zero padding (`[0-3s] ...`). Sound is written as `Sound design: ...`. **The guide gives no dialogue syntax (unverified).**

## MiniMax H3 (open weights)

- The HF repo is `MiniMaxAI/MiniMax-H3`, created 2026-07-28. It has two checkpoints: `H3-Base-FL2VA` (text plus 0-2 images as first and/or last frame) and `H3-Base-Ref2VA` (up to 9 images, 3 videos and 3 audio clips). The 2026-08-03 release date comes only from third parties. License: MiniMax H3 Community License. Users in the USA, EU, UK and Korea must apply.
- Output is 4-15 s at 24 fps, with a 768 px short side by default and native 32 kHz stereo audio. Aspect ratios 21:9 to 9:16. The checkpoints are CFG-distilled, so there is no negative prompt.
- The official prompt guide (`docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md`) uses three labelled fields: `integrated_multimodal_description:`, `overall_soundscape:` and `non_diegetic_music:` (`N/A` when empty). Shots are `[Shot N]`; a later shot starts `At 00:05.000, the camera cuts to ...`. Shot 1 opens with the style.
- Camera moves are written as type + amplitude + speed inside the sentence: "The camera pushes in with small amplitude at slow speed toward ...". Medium amplitude and normal speed are left out. The types are Push In/Pull Out, Zoom, Pan, Truck, Tilt, Pedestal, Arc, Tracking, Static, Shake and Roll.
- Dialogue form: `the baker with a calm, slightly raspy voice (S1) ... says: <d>[English] First batch of the morning.</d>`. A voiceover is written "says in an off-screen voiceover". On-screen text goes in double quotes.
- The guide does not mention the old bracket camera syntax (`[Pan left]`) at all, so calling it deprecated is unverified.
- Local field notes from earlier local renders (not vendor docs) give these numbers: frame counts on a 17k+5 grid, a trained range of about 124-362 frames, width and height in multiples of 32, and refs written `<Picture N>`. An informal format (style line, scene paragraph, `Timeline:` with `[0s-2s]` beats, a trailing `Avoid:` line) also renders well, but the card follows the vendor guide.

## Wan 2.2 (Alibaba, Apache 2.0, 2025-07-28)

- Checkpoints: T2V-A14B and I2V-A14B (480p and 720p; sizes 1280x720, 720x1280, 832x480, 480x832; 16 fps; 81 frames by default) and TI2V-5B (1280x704, 24 fps, 121 frames). Frames must be 4n+1. Sizes are multiples of 16 for the A14B models and 32 for 5B; this is derived from the VAE stride times the patch size, not stated in the docs.
- No native audio. **First/last frame (FLF2V) and VACE exist for Wan 2.1 only**; Wan 2.2 has no such repo, which corrects the research brief.
- The default negative prompt is the Chinese `sample_neg_prompt` in the configs. The prompt-extension system prompt targets about 60-200 words, puts the style first and adds at most 4 cinematic settings.
- The formula "Entity + Scene + Motion (+ aesthetics + stylization)" comes from Alibaba's Model Studio guide, which covers hosted Wan 2.5-3.0, so applying it to 2.2 is unverified. Wan 2.5 and 2.6 are hosted only.

## LTX-2 family (Lightricks)

- `LTX-2` (2026-01-03), `LTX-2.3` (2026-03-04, 22B) and **`LTX-2.5` (2026-07-23, current)**, under the LTX-2.x Community License.
- Frames must be 8n+1 and width and height multiples of 32. Base size is 768x512 at 24 fps (25 and 30 also allowed); the hosted API goes up to 20 s. Audio is generated jointly with the video.
- Conditioning: keyframes by `--image PATH FRAME STRENGTH`, plus a first/last-frame template. Camera LoRAs exist for LTX-2 19B only.
- The templates add a negative prompt automatically.
- Prompt guide: one flowing paragraph of 4-8 present-tense sentences, ordered shot, scene, action, characters, camera, audio. Multi-shot prompts name each cut in sequence ("A hard cut ..."). Dialogue goes in quotes (`She speaks quietly to herself, "He's late."`). "~200 words" is not in the current docs.

## Kling 3.0 (Kuaishou)

- Released 2026-02-06. The API IDs are `kling-v3`, `kling-v3-omni` and `kling-3.0-turbo`; the new REST endpoint is `POST /text-to-video/kling-3.0`. Durations are whole seconds from 3 to 15. Resolutions are 720p, 1080p and 4k on the API (Turbo: 720p and 1080p only); aspect ratios 16:9, 9:16 and 1:1. `settings.audio` is `native` or `off` and defaults to off. fps is unverified. Source: kling.ai/quickstart/klingai-video-3-model-user-guide and kling.ai/document-api.
- Multi-shot: 1-6 shots, each at least 1 s, with shot lengths summing to the total. Each shot prompt is at most 512 characters, and the API form is `shot n, m, words;`.
- Elements: up to 3 per request, each built from 2-4 images or a video, and they can carry a voice. The prompt names them as `@Name`. The model also takes a first frame and an optional last frame (no last frame alone). Turbo has neither elements nor frames.
- No seed or negative-prompt field in the new API ("the prompt can include positive and negative descriptions"). Prompts are capped at 3,072 characters, with 2,500 or fewer recommended.
- Dialogue: `Mom (softly, in a surprised tone): Wow, I didn't expect this plot at all.` The tone goes inside parentheses after the name, then a colon, and the guide's English example has no quotes. Language goes inside the parentheses too.
- Price: app credits per second are 9 at 720p and 12 at 1080p with audio, 6 and 8 without. The USD API price is unverified.

## Seedance 2.0 and 2.5 (ByteDance, BytePlus ModelArk)

- 2.0 IDs: `dreamina-seedance-2-0-260128`, plus `-fast-` and `-mini-` variants. **2.5 is live: `dreamina-seedance-2-5-260628`.** Its 2026-07-31 launch date comes from third parties only.
- 2.0: 4-15 s (or -1 for auto); 480p, 720p, 1080p and 4k (fast and mini top out at 720p); up to 9 images, 3 videos and 3 audio clips as refs. 2.5: 4-30 s; 480p to 1080p; up to 50 assets (30 images, 10 videos, 10 audio). Both: aspect ratios 16:9, 4:3, 1:1, 3:4, 9:16, 21:9 or `adaptive`; 24 fps; `generate_audio` defaults to true.
- The seed parameter is documented for the 1.x models only. There is no negative-prompt field; constraints go in the prompt ("avoid generating any text or subtitles"). Recommended prompt length is 1,000 English words or fewer.
- **Ref tags in the vendor's examples have a space: `@Image 1`, `@Video 1`, `@Audio 1`.** A subject is bound as `Girl @Image 1` or "Use the girl in @Image 1 as the main character". `@Image1` with no space appears only on third-party sites.
- Prompting: one camera move per shot, and `Shot 1:` / `Shot 2:` lines for multi-shot. Precise timestamps are "unstable". The guide puts dialogue in braces (`asks {How did the exam go?}`), while the API reference says double quotes, so the vendor's own docs conflict.
- Prices are discounted until 2026-10-07 (2.0 mini about $0.03/s at 720p, 2.0 fast about $0.09/s). List prices are unverified.

## Runway Gen-4.5

- API ID `gen4.5`, announced 2025-12-01 and still the flagship. `/v1/text_to_video` takes ratio `1280:720` or `720:1280`. `/v1/image_to_video` takes `promptImage` as the first frame and also allows 1104:832, 960:960, 832:1104 and 1584:672. Durations are whole seconds from 2 to 10, at 720p. Source: docs.dev.runwayml.com/api, help.runwayml.com.
- The schema has **no audio, no refs and no negative prompt**; "no audio" is inferred from the schema. The seed range is 0-4294967295 and `promptText` is capped at 1,000 characters (UTF-16 units). Price: 12 credits per second at $0.01 per credit, so $0.12/s.
- Text-to-video template: `[Camera] shot of [subject] [action] in [environment]. [Supporting descriptions]`. For image-to-video, describe motion only. Use positive phrasing. "Continuous, seamless shot" prevents cuts, and "The locked-off camera remains perfectly still." holds a static camera.
- Aleph 2.0 (`aleph2`) handles video-to-video editing.

## Luma Ray3.2

- **The current API model is `ray-3.2`** (Luma Agents API). Ray3 and Ray3.14 have no API ID in Luma's docs; the field guide that described them (2026-03-09) has been taken down (archive.org copy). Durations are `5s` and `10s` (10 s cannot combine with HDR, keyframes or loop). Resolutions are 360p, 540p, 720p and 1080p; aspect ratios 9:16, 3:4, 1:1, 4:3, 16:9 and 21:9. HDR and EXR are available. Keyframes go in `start_frame` / `end_frame`. The prompt is 1-6,000 characters. No audio, and no seed or negative prompt is documented. Source: docs.agents.lumalabs.ai/guides/videos/generation, lumalabs.ai/ray.
- Price: $0.30 per 5 s at 720p and $1.20 per 5 s at 1080p ("subject to change").
- Prompt rules (Ray3 field guide): about 100 words, present tense, mid-action verbs ("running", never "begins to run"), a secondary consequence (dust, fabric, reflections), one named camera move, positive only. Example: `A golden retriever running through a wheat field, ears flapping in the wind, dust particles catching golden hour sunlight, camera tracking alongside.`
