# HANDOFF: video analysis chain measure

Status: finished

Split out of the "Video analysis track" in ai-docs/HANDOFF.md on 2026-11-11. Steps are in the chain prompt.

Done:
- Session 1: madnesswright issue https://github.com/m4bwav/madnesswright/issues/91 (room 1 at 6.2 x 3.2 H).
- Manager: H = 3.10 SceneTools units (Character_Dummy rig, prefab scale 1.2), answered on #91; room 1 about 19.2 x 9.9 units.
- Session 3: step 3 first pass, measure files for rooms 2, 3, 5, 8, 10 (lower bounds only); see ai-docs/research/2026-11-11-rooms-2-10-first-pass.md.
- Session 4: PR #118 checks confirmed green; step 3 second pass sized rooms 6 (3.8 H) and 9 (5.7 H, door ruler); shots.json found only 29 shots.
- Session 2: step 2 done, `pan` uses ORB landmarks + RANSAC by default (see log 2026-11-11 measure chain, session 2).

- Session 5: step 3 done. shots at 0.15 (51 shots); rooms 4 (3.6 x 1.44 H) and 7 (3.6 x 1.95 H, only measured ceiling) from wide frames; notation examples/film-notation/nexus-rooms2-10.notation.md; PR #120 merged. Doors measure about 1.1 H, not 1.4.

Next:
1. None for this chain. Step 1's side-by-side render (character at the back wall) needs a Unity build of the madnesswright level, which this chain may not change; it goes with whoever takes madnesswright #91.
2. Optional later: depth for rooms 2-10 needs a frame with a horizon or two figures at different depths.

Waiting on Mark: nothing.
