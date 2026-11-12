# Benchmark rooms 2-10: first measuring pass (2026-11-11)

Film v0suvMY3GgM, local copy Ai/madnesswright-lab/nexus/video.mp4.webm. Frames and sheets in Ai/madnesswright-lab/nexus/measure/ (sheet_01/02 = one tile per 8 s, 6 across; grid9.jpg = the nine frames below with 50 px grids).

## Frames used

| Room | Time | Shot | Measure file |
|---|---|---|---|
| 2 wanted hall | 1:56 | mid, two agents, wall base y 440 | examples/film-notation/room2.measure.json |
| 3 controls office | 2:52 | mid, guard firing | room3.measure.json |
| 4 cargo bay | 4:28 | close on a guard | none (no full figure) |
| 5 sniper loft | 5:16 | high three-quarter, left corner at x 840 | room5.measure.json |
| 6 shutter garage | 6:28 | close, crouched | none |
| 7 spotlight corridor | 7:00 | close | none |
| 8 locker room | 8:04 | mid, lockers about 1.1 H | room8.measure.json |
| 9 break room | 9:40 | dim, figures cut off | none |
| 10 control tower | 10:36 | mid, TUVSTER / ADMIN ROOM signs | room10.measure.json |

## Results (`scale`)

Room 2: 3.3 H wide (lower bound), wall 1.13 H visible; room 3: 3.1 H, 1.07 H; room 5: 1.6 H; room 8: 4.3 H, 1.9 H; room 10: 4.1 H, 1.6 H. All `estimated`: every frame has the ceiling above the frame, at least one corner off, no horizon, and the characters stand 70-240 px in front of the wall line, so the numbers bound the room and do not size it.

## What this pass taught

- One frame per room, picked at fixed times off a contact sheet, lands on mid or close shots most of the time: the film cuts to fights after its establishing shot. Room 1 worked because 0:26 is the establishing wide.
- Next pass must pick frames per room from `shots`: the first wide shot after the room's entry cut (largest wall area, a full standing figure), then `pan` only inside that shot. `pan` over a fixed 12 s window crossed cuts (rooms 4, 5, 7 gave 1000-1800 px, which are cut jumps, not pans).
- Ceilings are rarely in frame; height needs either a tilt (`pan` reports tilt_px) or a door as a second ruler (door about 1.4 H in room 1).
- Rooms 4, 6, 7, 9 need a wide frame found first; their sizes stay `guess`.
