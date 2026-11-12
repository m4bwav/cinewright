# HANDOFF: video analysis chain measure

Status: waiting

Split out of the "Video analysis track" in ai-docs/HANDOFF.md on 2026-11-11. Steps are in the chain prompt.

Done (2026-11-11, session 1):
- Step 1 brief: madnesswright issue https://github.com/m4bwav/madnesswright/issues/91 (room 1 at 6.2 x 3.2 H). Character height H is NOT verified: SceneTools samples bound it to 2.5-3.8 units (CO_Door 4.32 tall implies about 3.3-3.8; CO_Seat 0.63 implies about 2.5; NavMesh agentHeight 2 is Unity's default). The brief's 2.0 is probably low.

Next:
1. Measure H in-game (needs Mark to stand a character by a door in Playground, or read the player collider from the game bundles), then the side-by-side render with a character at the back wall.
2. Step 2: ORB/landmark pan on cel backgrounds (L-20261111-2). Can run without Mark.
3. Step 3: rooms 2-10.

Waiting on Mark: in-game character height for issue #91 (no askwright page made; the question is in the issue).
