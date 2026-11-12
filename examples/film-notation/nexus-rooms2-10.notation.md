# Film notation: Nexus Prominence fan film, rooms 2-10

Source: https://www.youtube.com/watch?v=v0suvMY3GgM, 2d-animation, 862.161 s. Unit: H (one standing character; H = 3.10 SceneTools units, see madnesswright issue #91). Room 1 is in [nexus-room1.notation.md](nexus-room1.notation.md).

Every size comes from one wide frame per room run through `cine_analyze.py scale` (measure files `roomN.measure.json` beside this file). All are `estimated`. Width is the visible back wall; it is a lower bound when a corner is off frame. Height is the wall visible above the floor line; only room 7 shows its ceiling, so the other heights are lower bounds too. No frame gives depth (no horizon, no two figures at clearly different depths), so depth is `?` throughout; for a level build, use room 1's depth ratio (about 0.5 x width) until a better frame turns up.

## Sets

| Set | Time | Width H | Height H | Depth H | Bound | Frame |
|---|---|---|---|---|---|---|
| Room 2: wanted hall | 1:56 | 3.3 | 1.1 | ? | width and height lower | mid, two agents |
| Room 3: controls office | 2:52 | 3.1 | 1.1 | ? | width and height lower | mid, guard firing |
| Room 4: cargo bay | 4:37 | 3.6 | 1.4 | ? | both corners in, height lower | high three-quarter wide, office window in back wall |
| Room 5: sniper loft | 5:16 | 1.6 | 0.6 | ? | weak: high angle, one corner | high three-quarter |
| Room 6: shutter garage | 6:22 | 3.8 | 1.6 | ? | width and height lower | wide, standing guard; door 1.07 H |
| Room 7: spotlight corridor | 6:41 | 3.6 | 1.95 | ? | width lower, height measured | side-on wide, ceiling lamps in view; door 1.13 H |
| Room 8: locker room | 8:04 | 4.3 | 1.9 | ? | width and height lower | mid, lockers about 1.1 H |
| Room 9: break room | 8:36 | 5.7 | 2.4 | ? | door taken as 1.4 H ruler | dim wide, no standing figure |
| Room 10: control tower | 10:36 | 4.1 | 1.6 | ? | width and height lower | mid, TUVSTER / ADMIN ROOM signs |

## Reading the numbers for a level

- Room 7 is the one measured ceiling: 1.95 H, below room 1's 2.63 H. Corridors read lower than the opening street room.
- Doors measure 1.07-1.13 H in rooms 6 and 7, smaller than the 1.4 H assumed from room 1; room 9's width leans on that 1.4 H and may be about 20% too large (about 4.6 H with a 1.1 H door).
- Most rooms land at 3-4.5 H of visible wall, about half of room 1. Since corners are often off frame, a builder should treat 4-5 H as the working width and confirm in play.

## Shots used

Shot boundaries from `cine_analyze.py shots --threshold 0.15` (51 shots; 0.3 gave 29 and merged rooms). The film is mostly long takes with camera moves, so a room's wide frame sits inside a long shot, not at its start: rooms 4 (S021) and 7 (S026) were found on a 1 fps contact sheet of the shot.
