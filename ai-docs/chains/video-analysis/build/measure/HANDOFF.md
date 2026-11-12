# HANDOFF: video analysis chain measure

Status: ready

Split out of the "Video analysis track" in ai-docs/HANDOFF.md on 2026-11-11. Steps are in the chain prompt.

Done:
- Session 1: madnesswright issue https://github.com/m4bwav/madnesswright/issues/91 (room 1 at 6.2 x 3.2 H).
- Manager: H = 3.10 SceneTools units (Character_Dummy rig, prefab scale 1.2), answered on #91; room 1 about 19.2 x 9.9 units.
- Session 3: step 3 first pass, measure files for rooms 2, 3, 5, 8, 10 (lower bounds only); see ai-docs/research/2026-11-11-rooms-2-10-first-pass.md.
- Session 2: step 2 done, `pan` uses ORB landmarks + RANSAC by default (see log 2026-11-11 measure chain, session 2).

Next:
1. Step 3 second pass: run `shots` on the whole film, take the first wide shot after each room's entry cut (frames in Ai/madnesswright-lab/nexus/measure), `pan` only inside that shot, add a horizon or a door ruler, re-run `scale`; then size rooms 4, 6, 7, 9 and write the rooms 2-10 notation (`examples/film-notation`).
2. Step 1 remainder: side-by-side render with a character at the back wall. Needs a Unity build of the madnesswright level at the new size; this chain may not change madnesswright, so it belongs to whoever takes #91.

Waiting on Mark: nothing for step 3.
