# Gemini video test on the benchmark (2026-11-11)

One small paid call: `generateContent` on `gemini-3-flash-preview`, YouTube URL https://www.youtube.com/watch?v=v0suvMY3GgM, `video_metadata` start 0 s, end 45 s, fps 2. Script: a stdlib urllib call (no SDK). Prompt: a JSON shot list (start, end, size, move, who, action, on-screen text, sounds) plus the first room's size in standing-character heights.

## Model ids

The key's `models` list (2026-11-11) shows gemini-2.5-flash/pro, gemini-3-flash-preview, gemini-3.1-pro-preview, gemini-3.1-flash-lite and `-latest` aliases. It does **not** list `gemini-3.8-flash`, `3.6-flash` or the "Gemini 4" names quoted in [2026-11-11-film-analysis-and-gemini-video.md](2026-11-11-film-analysis-and-gemini-video.md) from the pricing page; treat those rows as unconfirmed for this key. Always list models before a run.

## Result

- Time 34 s. Usage: 7,065 video tokens for 45 s at 2 fps (about 157 tokens a second), 99 text, 1,053 output, 1,128 thinking; 9,345 total. Cost well under one cent.
- Room estimate at 0:18: back wall about 7 H wide, 2.5 H tall, floor about 2 H deep, "4/5" confidence. Measured (cine_analyze scale, 0:26): at least 6.2 H wide, 2.63 H tall, 2.7-3.7 H deep. Width and height agree within about 15%; depth is low.
- Shot list: wrong structure. It split the opening into seven shots (cuts at 0:03, 0:08, 0:17, 0:26, 0:36, 0:40); ffmpeg scene detection and the frames show one continuous take 0:00-0:40.6 (titles, crane down the skyline, pan along the checkpoint) then a cut. It called the crane down a "tilt up" and described a fight beat ("Hank drops from the ceiling") that needs checking against frames.
- On-screen text read correctly (titles, billboards, the location HUD, the animator credit).

## Verdict

Gemini is worth it for a cheap first-draft description (text, who, what, sounds) of long films straight from a URL, and its rough room size is a useful cross-check. Never take its cuts or timecodes: shots come from `cine_analyze shots`, sizes from `scale`. This matches the extraction-routes rules.
