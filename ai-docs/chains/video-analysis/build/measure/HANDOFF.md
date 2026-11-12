# HANDOFF: video analysis chain measure

Status: ready

Split out of the "Video analysis track" in ai-docs/HANDOFF.md on 2026-11-11. Steps are in the chain prompt.

Done:
- Session 1: madnesswright issue https://github.com/m4bwav/madnesswright/issues/91 (room 1 at 6.2 x 3.2 H).
- Manager: H = 3.10 SceneTools units (Character_Dummy rig, prefab scale 1.2), answered on #91; room 1 about 19.2 x 9.9 units.
- Session 2: step 2 done, `pan` uses ORB landmarks + RANSAC by default (see log 2026-11-11 measure chain, session 2).

Next:
1. Step 3: measure rooms 2-10 of the benchmark (local copy Ai/madnesswright-lab/nexus/video.mp4.webm); use `shots` to split pan ranges at cuts, `frame` + `scale` per room, `pan` for wide walls.
2. Step 1 remainder: side-by-side render with a character at the back wall. Needs a Unity build of the madnesswright level at the new size; this chain may not change madnesswright, so it belongs to whoever takes #91.

Waiting on Mark: nothing for step 3.
