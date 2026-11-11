# Continue prompt: cinewright video analysis, film notation, AI-video detection

This prompt does not change between sessions. State lives in `ai-docs/HANDOFF.md` (section "Video analysis track"), never here.

## Goal

Make cinewright as good at taking a film apart as musicwright is at a song (audio to notation and back):

1. **Film breakdown and notation.** From a video (local file or YouTube URL), produce a written record of every shot, scene, camera move, blocking and choreography, set (layout and measured scale), costume, prop, lighting, colour, edit rhythm and audio layer (dialogue, music, effects). It should be complete enough to **rebuild something similar** from the record alone: a shot list for AI video, or a level or mod (madnesswright scenes).
2. **AI-video detection and teardown.** Scripts and rules that score how likely a video is AI-made: gibberish or warping text, hands, object permanence, physics, temporal flicker, lighting and shadow mismatches, "too perfect" skin and surfaces, identity drift, provenance metadata (C2PA, SynthID where it can be checked), and model-specific tells. Plus breaking an AI video into the same notation so its shots can be rebuilt or studied.
3. **Content extraction route, including Gemini.** Research what Google Gemini's native video understanding gives us (YouTube URL input, timestamps, frame sampling rate, audio and video together, long context) that Anthropic and OpenAI models cannot. Measure whether it is worth using, against a local pipeline (ffmpeg scene detection, PySceneDetect, frame sampling plus Claude vision, Whisper, monocular depth for room scale, pose estimation for choreography).

## Motivating failure (the first test case)

madnesswright built a Project Nexus level from the fan film https://www.youtube.com/watch?v=v0suvMY3GgM and it looked wrong: **the first room was far bigger in the mod than in the film.** Find how that analysis was done (madnesswright repo, its ai-docs and its everlast vault sidecar) and write down why it failed. Then use this video as the benchmark: the new pipeline must recover the first room's dimensions (from character height as the scale reference, plus depth or camera geometry) and the layout of each set, and the rebuilt room has to match the film when compared side by side.

## Load state first

1. Read `AGENTS.md`, `CODEMAP.md`, `ai-docs/HANDOFF.md`, the newest entries in `ai-docs/log.md` and `ai-docs/plans/PLAN.md`.
2. Read the cinewright skills this touches: `cinewright-qc`, `cinewright-shots`, `cinewright-continuity`, `cinewright-craft` (sets, movement, design, sound, edit). Read musicwright-compose's transcribe/notate section as the model to copy.
3. Read the everscout and technique-harvest setup (Ai/everscout, Ai/technique-harvest) so new targets match how existing beats are written.

## Order of work

1. **Diagnose** the madnesswright room-scale failure and log it.
2. **Research** (sources go in `ai-docs/research/`, with dates): film-analysis tooling, scene and shot detection, camera-motion and depth estimation, pose and choreography capture, audio stem separation; AI-video detection methods and research benchmarks; Gemini video API limits, pricing, terms (including YouTube input), compared with Claude and OpenAI. Run a real Gemini test on the benchmark video only if an API key is available; otherwise record what is needed on an askwright page.
3. **Design a film notation format** (a versioned JSON/YAML schema plus a readable Markdown view): scene, shot, timecode, framing, lens, move, blocking positions on a floor plan, set dimensions with confidence, costume and prop ids, light, audio cues. Map it onto the existing shot cards and bibles so a breakdown can feed `cinewright-genvideo` and madnesswright directly.
4. **Build scripts** in `scripts/` (stdlib Python plus optional ffmpeg, PySceneDetect, Whisper, depth model; degrade gracefully): `breakdown` (video to notation), `scale` (room and set measurement), `aidetect` (scored report with evidence frames), `rebuild` (notation to shot list or level brief). Add tests.
5. **Knowledge base**: a new skill or skills (e.g. `cinewright-analyze`, `cinewright-aidetect`) with references, kept small (package size budget). Run evergreen-test with trigger cases and decoys.
6. **Harvest and scout targets**: add technique-harvest targets and everscout beats for (a) film analysis, notation and rebuilding from documentation, (b) AI-video detection, (c) video content extraction, including Gemini and other multimodal models.
7. **Prove it** on the benchmark: breakdown, rebuild the first room's brief for madnesswright, and compare it with the film (side-by-side frames). Record the result.

## Stop points (ask on an askwright page, keep working on other steps)

- Paid API spend (Gemini or others) beyond a small test.
- Any change to madnesswright itself beyond writing a brief or an issue.
- Publishing a release that changes public skill names.

## Hand-over rules

- Commit on a branch, open a PR, merge it yourself once checks pass (per global rules); tag and release if the version is bumped. Update installed plugins after a release.
- Log every session in `ai-docs/log.md`; research in `ai-docs/research/`; decisions in `ai-docs/decisions/`.
- Last step: run evergreen-wrapup, update `ai-docs/HANDOFF.md` ("Video analysis track": done, next, waiting on Mark), then print exactly:

`Execute D:/m4bwa/Claude/Projects/Ai/cinewright/ai-docs/plans/2026-11-11-video-analysis-continue-prompt.md`
