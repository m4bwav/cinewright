---
title: The 3D route for fights: a posed blockout as the video control
summary: Study (2026-10-16) of building a fight in 3D and turning it into video. Motion sources and their licences, which control passes and models hold two bodies, a blade and their facing on a 16 GB GPU, what exists to build on and what it costs, and a previs test on two hard cards of a rapier duel from a novel. Recommendation - keep MiniMax H3 and put the posed figures into its control. The H3 test (2026-10-17) - figures in the control removed a duplicated fighter and held the start and end states; depth held a fighter's back to the camera through the action but not after it.
tags: [research, fights, previs, blender, controlnet, depth, pose, canny, scail, motion-capture]
date: 2026-10-16
---

# The 3D route for fights: a posed blockout as the video control

Question (the owner, after the first full render of a rapier duel from a novel): build the fight in 3D, then turn it into video?

Why it came up (field lesson 128): every control in that film was a Canny render of the empty set, held still. It holds the walls and the camera, never the people. The timed beats (open test 2 of [2026-10-15-fight-planning](2026-10-15-fight-planning.md)) made most hits land, but nothing held who stands where or which way they face. Cards with little or no control opened on the cast references as a lineup facing the lens. Two-shots drifted to both fighters facing the lens (3 of 4 takes of one blade cross, 4 of 4 of a cloak throw). An over-the-shoulder card never put the far fighter's back to the camera (0 of 3), and a second copy of one fighter appeared in 3 of about 180 takes. Facing is the first thing lost.

Method: one web research pass (sources below, labelled vendor, paper, forum or inference); a survey of what polywright and the film's own set blockout already do; and a previs test on two of the hardest cards, built and rendered (Blender only, no video model run).

## Recommendation

1. **Stay on MiniMax H3 and change only the control.** H3 speaks the lines, takes the character and prop references, and has the timed beats. Its installed Fun ControlNet Union 2.0 already accepts Canny, depth, pose, layout boxes and gray (vendor). No new model is needed to test the idea.
2. **Pose the two fighters in Blender at the set plan's marks, keyed by hand per exchange.** Use the crowd route's segmented mannequin with two-bone IK and rigid blades. That is enough for a control at 0.6 strength, it is headless, and it needs no licence. Motion capture and Kimodo come later, as a v1 for the poses a box mannequin cannot carry (lying on the floor, a tumble).
3. **First test Canny of the clay with the figures in it**, since it is the smallest change from what the film uses. Then depth with thickened blades, then pose. Use tonight's seeds and prompts, so the control is the only variable.
4. **Build polywright's `pw.py duel` only if that test holds facing better than tonight's takes.** It did, in part (see "The H3 test"): building it waits for the owner's go-ahead. SCAIL-2 stays the fallback for two-body action that H3 cannot hold even with figures in the control.

## Motion source

| Source | Licence (for a film) | How an agent drives it headless | Two fighters | Verdict |
|---|---|---|---|---|
| Keyframed poses on a segmented mannequin (this test) | none needed | a JSON of named poses keyed in seconds, IK to hand and foot targets, rendered by `pw.py bpy` | both in one scene, so contact and occlusion are exact | **v0.** About 30 minutes of agent time a card, after the script. Weak for lying, rolling and falling bodies. |
| Mixamo | free with an Adobe ID; royalty-free in films; no redistribution of the raw files, no training on them (vendor FAQ, forum repost) | no API: someone downloads FBX clips by hand once, then Blender imports and retargets them headless | one clip per person; contact timing aligned by hand | v1 for walks, kicks and falls. The sword grip needs adjusting per clip (forum). |
| CMU mocap (BVH) | free for research and commercial use; no resale (forum mirrors) | BVH import in Blender | single-person clips | no fencing category; filler only |
| NVIDIA Kimodo | code Apache-2.0; SOMA and G1 weights under the NVIDIA Open Model License, commercial use allowed; the SMPL-X weights are research-only (vendor) | `kimodo_gen` CLI: text plus full-body keyframes, end-effector constraints and root paths; under 3 GB VRAM with the text encoder on the CPU (vendor) | single person | **v1 candidate:** the keyed poses become its keyframes, and it fills the motion between them. Output is NPZ, not BVH, so it needs a converter. |
| GVHMR (video to motion) | "educational, research and non-profit purposes only" (vendor licence); SMPL is non-commercial too | ComfyUI-MotionCapture | trackers swap fighters at contact (earlier note) | research only: not for a film that may be shown |
| Cascadeur | free tier non-commercial | no headless mode | | rejected |
| Free fight packs (MoCap Online sword pack, Rokoko's 10 fight clips) | the MoCap Online page states no licence; Rokoko's is free | FBX import | single person | no rapier or fencing clip with a clear licence found |

**Blades have no skeleton.** Every route carries the weapon the same way: a rigid part on the hand (a weapon bone with a Child Of constraint in a rig, or a matrix on the wrist as in this test), animated separately when it leaves the hand. SCAIL's and OpenPose's skeletons carry no weapon, so a pose control says nothing about a blade (paper, inference). A blade survives only in depth, Canny or a mask.

## Control passes and models (16 GB GPU)

| Model and control | On the machine | Two bodies, occlusion | Blade about 11 px | Facing | Identity from the film's refs |
|---|---|---|---|---|---|
| **H3 + Fun ControlNet Union 2.0**: Canny, depth, pose (DWPose style), layout, gray, HED, MLSD, scribble; one control video (vendor) | yes | depth and Canny carry occlusion; pose has only draw order | Canny draws the blade's outline; depth at 2.8 times the real width shows a solid bar (this test) | depth and Canny show the body's shape; pose shows it only when face points are left out of a turned head (this test) | yes, through H3's reference pictures |
| SCAIL-2 (Wan base, native in ComfyUI, fp8 and NVFP4 repacks; 512p and 704p; code Apache-2.0, card says MIT) | no weights | built for it: a 3D skeleton drawn as cylinders, one colour per person; the paper calls multi-person accuracy "not as precise" | no weapon in the skeleton | strong (3D limbs) | multi-reference input is "experimental" (vendor) |
| Wan 2.1 VACE 14B (GGUF Q5 about 11 GB) or Wan 2.2 Fun Control A14B (Apache-2.0) | no weights | depth, pose and masks; PrevizWhiz drove two and three people with per-character skeleton layers and masks (paper) | untested | per pass | one reference image |

None of them speaks the dialogue. The film's talking cards stay on H3 whatever drives the fight cards.

## What exists to build on, and what it costs

- **The set blockout** (the film's `build_room.py`, 322 lines): the room from the set plan, and every card's camera from the plan's coverage. The test reuses it whole (`exec` up to its render loop), so the figures stand in the same room and lens as the controls the film already uses.
- **polywright `pw.py crowd`** (field lesson 097: a crowd's depth video drives H3 at 0.6/0.4): the 10-part mannequin, the inverse-depth material, the COCO-18 joint order and the skeleton colours. The test reuses its geometry and conventions, but not its walk-cycle poser.
- **`pw.py bpy`**: runs the test script headless. Blender 5.2 renders 107 frames at 864x480 in about 36 s (depth twice on the CPU in Cycles, clay in Workbench), so a card's previs costs well under a minute and can run while a video queue holds the GPU.
- **The test scripts** (in the film folder, not in a plugin): `duel_previs.py` 339 lines, `post.py` 92 lines, one pose file per card (27-36 lines). Building them and posing two cards took about 1.5 agent hours, including two fixes found on the sheets.
- **`pw.py duel` (proposed, about 650 lines in the earlier note).** Read the fight plan's phrases and exchanges plus a pose file per card. Write depth, thick-blade depth, clay and Canny, pose with hidden face points, per-fighter and weapon masks, layout boxes, a contact-gap report and a sheet. The test covers about half of that. Estimate: 550-700 lines across `pw.py` and `pw_bpy.py` with tests and docs, about 3-5 agent hours. A Kimodo bridge (NPZ to the mannequin) adds about 150 lines and 1-2 hours. A Mixamo FBX retarget adds about 150 lines and 1-2 hours, plus the owner's one-time download.
- **polywright size budget** (`scripts/budget.py`): the installed skills folder is 420 KB today (green up to 400, yellow up to 800, red above 800). `pw.py duel` at 30-40 KB puts it near 460 KB, still yellow, with no risk of red. A pose library shipped as JSON would add a few KB more. Say so in the PR, since it stays yellow.

## The previs test (done 2026-10-16)

Two cards the review showed are hard:

- **A cloak throw over one fighter's shoulder.** In 4 of 4 takes the near fighter turned to face the lens, and one take added a second copy of him.
- **A kick to a kneeling man, who tumbles onto his back while his rapier flies out of frame.** One take of four added a second copy of the kneeling man.

Each card was posed at the set plan's marks for its phrase, through the card's own camera, at H3's length (107 frames, 4.46 s).

What the sheets showed:

- **The near fighter's back reads as a back in depth and Canny.** Over the shoulder, his head and shoulder fill the frame edge as a dark mass, and the far fighter faces the lens squarely. Neither fact was anywhere in the old room-only control.
- **The pose pass drew the near fighter's eyes and nose though his back was to the camera.** polywright's crowd joints always include the face points. To a pose control, that says he faces the lens: the very fault under test. Fix: leave the nose and eyes out when the face turns from the lens (head-to-nose against head-to-camera, dot product under 0.15), and leave out an ear behind the head, as a detector would. A `pw.py duel` must do the same, and so should the crowd route's front ranks when they march away.
- **The card's end state could not be shot from its own camera.** The kick card's camera (eye height 1.2 m, 35 mm, 4 m off, level) sees the floor only beyond about 4.2 m, so a man lying on his back at his mark is below the frame. One of tonight's takes got there by cheating the geometry. The previs tilts the camera 9 degrees down. A previs checks that every end state is in frame before any render. The set check cannot: it places people as points.
- **Blades:** at the real width (1.6 cm) the depth pass shows a thin, broken line at a 4 m two-shot. At 2.8 times (4.5 cm) it is a solid bar. Canny of the clay draws both edges at either width. Whether H3 keeps a blade from either is open test 1, still to run.
- **The box mannequin fails on the floor.** A fighter on his back reads as a crumpled block in depth and as a small tangle in pose. Standing, kneeling and kicking read well. Lying, rolling and falling poses are where a rigged body (Mixamo or Kimodo) pays.

## The H3 test (run 2026-10-17)

Four takes, each one of tonight's takes re-rendered with the same prompt, references and seed, with only the control changed (0.6 strength, ending at 0.4 of the steps, as tonight):

| Take | Tonight's take it repeats | Control |
|---|---|---|
| cloak t1 | the near fighter faced the lens | Canny of the clay with the figures |
| cloak t2 | the same | depth, thick blades |
| kick t1 | a second copy of the kneeling man | Canny of the clay with the figures (camera tilted 9 degrees) |
| kick t2 | the same | pose, hidden face points left out |

About 15 minutes of GPU time. Judge them with the same frame strips as the film's review: the facing, a second copy, the hits on their beats, blade survival.

- **If Canny with figures fixes the facing,** `pw.py duel` is worth building, and the film's two-shots get previs controls.
- **If none does,** run open test 4 (SCAIL-2) on the kick card.

**Result** (the owner's go-ahead on 2026-10-17; 4 takes in 40 minutes, sharing the GPU with another film's render; frame strips every 0.4 s and full-size frames):

| Take | Facing and copies | Hits and states |
|---|---|---|
| cloak t1, Canny with figures | no better: both fighters side by side facing the lens, as in tonight's take | the cloak thrown and fallen on its beats |
| cloak t2, thick-blade depth | **the near fighter's back to the camera, over his shoulder, to 1.2 s**, three-quarter toward the far fighter through the throw (2.0 s); turned to the lens from 2.4 s | the cloak thrown at 1.6-2.0 s; the face bared |
| kick t1, Canny with figures | **one kneeling man, no copy**, kneeling from frame 0 | kick at 1.2-1.6 s, tumble at 2.4-2.8 s, on his back with the blade on the floor from 3.2 s: every beat, and the end state in frame (the tilted camera) |
| kick t2, pose | no copy | starts standing and kneels by 1.2 s (inside the trimmed part); kick, tumble and end state land |

- **Figures in the control fix copies and states.** Tonight's kick takes added a second kneeling man in 2 of 4; the previs takes in 0 of 2, and the Canny take is the best of the six.
- **Facing holds while the control's figures hold it, then drifts.** Depth kept the near fighter's back to the camera through the first half; once the action was spent he turned to the lens as before (field lesson 128). The previs had him turn three-quarter at the throw, so part of the drift may be the pose file's own. Next: key his back to the camera to the last frame, and try depth at 0.8/0.6 (open question 2).
- **Canny of figures is not enough for a two-shot standing still:** it draws two outlines a model can fill facing either way. Depth carries which side is the back.
- Verdict: `pw.py duel` is worth building for the two-shots and the floor states. It waits for the owner. The kick card's Canny take is proposed to the owner as that card's pick.

## Open questions

- H3's Union 2.0 takes one control video. Is a composite better than one pass: depth with the clay's Canny edges drawn over it, or a layout-box pass for the two fighters (the model card lists layout, which suggests subjects)? Untested.
- The vendor's examples run the control at full strength (1.0). The film runs 0.6/0.4 so H3 can paint freely. With people in the control, 0.8/0.6 may be needed, as for exact formations in the crowd route.
- Does the control conflict with the prompt when they disagree? The kick card's text says the fighter lands "at frame left", and the control has to agree. A previs makes the card's text checkable against its own picture.

## Sources

- MiniMax H3 Fun ControlNet Union 2.0 model card, control types, strength and lengths (vendor): https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union-2.0; ComfyUI tutorial (still for v1): https://docs.comfy.org/tutorials/video/minimax/minimax-h3-fun-controlnet
- SCAIL (paper, multi-person accuracy): https://arxiv.org/html/2512.05905v3; SCAIL-2: https://github.com/zai-org/SCAIL-2; Wan-Animate-2: https://huggingface.co/Wan-AI/Wan-Animate-2-14B
- Wan VACE: https://docs.comfy.org/tutorials/video/wan/vace, https://huggingface.co/QuantStack/Wan2.1_14B_VACE-GGUF; Wan 2.2 Fun Control: https://huggingface.co/alibaba-pai/Wan2.2-Fun-A14B-Control
- Kimodo: https://github.com/nv-tlabs/kimodo; GVHMR licence: https://raw.githubusercontent.com/zju3dv/GVHMR/main/LICENSE; Mixamo licensing (forum repost of the FAQ): https://community.adobe.com/questions-696/mixamo-faq-licensing-royalties-ownership-eula-and-tos-589400
- Free fight clips: https://mocaponline.itch.io/free-3d-sword-animation-pack, https://rokoko.com/resources/motion-library-10-free-fight-and-weapon-animations
- PrevizWhiz (Autodesk Research, CHI 2026): https://arxiv.org/abs/2602.03838

Related: builds on [2026-10-15-fight-planning](2026-10-15-fight-planning.md) (its open tests 1 and 4) and [2026-10-13-battle-crowd-compositing](2026-10-13-battle-crowd-compositing.md).
