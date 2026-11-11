# Why the Nexus Prominence room 1 came out too big (2026-11-11)

Benchmark film: https://www.youtube.com/watch?v=v0suvMY3GgM (14:22, 1280x720 30 fps; local copy in Ai/madnesswright-lab/nexus/video.mp4.webm, not in any repo). Level: madnesswright `examples/NexusProminence`, generator `Editor/NexusProminenceBuilder.cs`.

## How the level was made

1. Pulled the film with yt-dlp at 480p, contact sheets with ffmpeg `fps=1/9,tile=4x6` (later 1 frame per 4 s at 720p).
2. Read the sheets by eye and named ten rooms.
3. Cloned the SceneTools sample room (SamplePlayground_PG) ten times and gave each a `RoomSpec` Width/Depth **multiplier of the sample box** (room 1: 1.0 x 0.8 after the owner asked for it smaller).
4. Dressed each room with primitives from the frames; rendered with NexusShots and compared renders with the sheets by eye.

## Measured gap (room 1, film 0:26 vs build m)

Unit H = one standing character, head to feet. In the film frame at 0:26 a standing guard is about 215 px tall.

| | Film (0:26) | Mod (build m) |
|---|---|---|
| Back wall width | about 5-7 H (window 900 px = 4.2 H, wall to right corner 1120 px = 5.2 H, left corner off frame) | 31.5 units = about 16 H (2-unit player marker) |
| Back wall height | about 2.2 H (floor line y 545 to ceiling y 70) | not measured |
| Floor depth | shallow, about 1-1.5 H in front of the wall | sample depth x 0.8, several H |

The mod room is about 2.5-3x too wide and several times too deep.

## Causes

1. **No unit.** Sizes were multipliers of a sample box whose size in character heights nobody knew. Nothing in the pipeline converted pixels to H.
2. **No measuring step.** Contact-sheet thumbnails (320 px tiles, one frame per 4-9 s) are good for naming rooms, not for scale. No frame at full size was measured.
3. **Camera mismatch ignored.** The film is a side-on 2.5D stage (low camera, shallow floor, wide back wall seen across a pan). The game camera looks down at 3/4 from far back. A room that reads right in the film needs its floor depth set from the film, not from the sample.
4. **Pans not stitched.** The room's full width only shows across a pan (0:22-0:40). Sampling single frames sees part of the wall each time; without stitching (or tracking the pan) the width is a guess.
5. **Compare step had no scale reference.** Renders were checked against the film without a character at known height standing in both.

## What the new pipeline must do (requirements for `scale` and `breakdown`)

- Detect shots, then for each set: pick frames where a character stands on the floor, measure H in pixels at that floor row, and express wall width, wall height and floor depth in H with a confidence.
- Stitch pans (frame-to-frame translation) so a wall wider than one frame gets measured once.
- Record the camera (height, angle, lens guess) so a game camera can be matched, and output floor plans in H that a level builder converts with its own character height.
- The comparison is a side-by-side at the same H: film frame and render, with a character at known height in both.
