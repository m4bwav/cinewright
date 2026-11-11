# Handoff

## Current state
- Released: v0.2.0 on main 0e05a61 (2026-10-24), https://github.com/m4bwav/cinewright/releases/tag/v0.2.0 (15 skill ZIPs; cinewright-curate ships only in the dev plugin). v0.1.0 on fad9ec6. Repo public since 2026-10-07.
- Install routes (record: [notes/2026-10-06-s7-install-proof.md](notes/2026-10-06-s7-install-proof.md)): Claude Code, Copilot CLI, `gh skill`, claude.ai skill Upload and VS Code Copilot Chat all PASS. claude.ai Add marketplace: the skill triggers, but its `cine.py` calls fail because the model guesses the plugin skill folder (`/mnt/skills/plugins/cinewright:cinewright-continuity`). LEARNINGS L-006 `claude-ai-plugin-skill-folder-unknown` in cinewright-continuity.
- VS Code route caveat: installed with the Copilot CLI into `~/.copilot/installed-plugins/`, which VS Code reads; VS Code's own Install button was not exercised.

- cinewright-voice (14th skill) built 2026-10-07 on branch voice-skill, merged to main as PR #18 (https://github.com/m4bwav/cinewright/pull/18) on 2026-10-07 after merging cinewright-sets into it; Sonnet evals 7/7, Haiku and Opus not run. Description budget YELLOW (4,680/4,000 with cinewright-sets; red at 5,500). TTS Audio Suite in ComfyUI not installed on the PC: install only with Mark's go, then run the design-then-clone route once and record it in the skill's SETUP.md.

- Branch cartwheel-night, PR #21 (https://github.com/m4bwav/cinewright/pull/21), waiting for review: `qc measure`, `compile --sequence --join`, card `music` field, tests copy `assets/` (91 OK). From a 60 s comedy field test; details in the 2026-10-07 log entry. Budget yellow: shared/lib 104 KB.

- Branch preproduction-gaps (2026-10-09, PR waiting for review): prop `states` and card `props`, prop and location refs now sent to the model, `shared/lib/cine_post.py` (animatic, grade measure/match; shipped by edit and finish only), entries prop-sheets, lora-or-references, animatic, shot-matching, blockout-control, identity-score. Budget yellow: runtime shared/lib 120 KB (green 100, red 150), one entry 714/700 tokens. Details: 2026-10-09 log entry.

- Branch critic-research-2026-10-15 (2026-10-15): `qc judge` / `qc agree` / standing claims, six critic entries, `air-steps`; research note [research/2026-10-15-critic-research.md](research/2026-10-15-critic-research.md). Open from it, in order: per-region crops and geometry checks (screen side, people count, gaze, smile) before the judge; pairwise take ranking in a command; voice checks as commands (forced alignment, speaker similarity); score `qc judge --twice` on the reviewer's own verdicts, not the agent's.

- Branch fight-plans (2026-10-15, PR waiting for review): fight plan schema, `cine_fight.py` check and sheet (movement only), entries fight-plan, fight-from-a-book, fight-previs, eval action-2 (3/3 Sonnet), harness allow list for `cine_*.py`. Research [research/2026-10-15-fight-planning.md](research/2026-10-15-fight-planning.md). Budget: runtime 145 KB of red 150, so the next runtime addition needs a trim first. Open from it: the five local tests at the end of the research note (H3 timecoded hits first); `pw.py duel` in polywright only if test 1 shows blades survive depth control.

- Branch sets-and-loras-2026-10-15: entry blocking-marks, set-light, master-plates, set-check, lora-or-references; research [research/2026-10-15-sets-and-loras.md](research/2026-10-15-sets-and-loras.md). Open from it: port the marks check (prototype `set_check.py` in the duel's set folder, about 10 KB) into the runtime as `continuity marks` or a sets-only `cine_set.py`, after trimming about 6 KB elsewhere in shared/lib; a card field for the camera's plan position and per-card marks; lora-or-references sits at 1,199 of 1,200 tokens, so split it before the next addition.

- Branch books-track1 (2026-10-22, book-learnings track 1): `qc measure` flicker per shot (warns only, L-006), vocab `flicker` and `lip-lag`, random review sides and gate-rejected takes in the label queue (take-selection, judge-calibration), identity against the take's own first face, LTX-2 stage-1 QC rule; evals action-2 and outcome-2. Runtime shared/lib is at 150 KB with about 30 bytes left before red: the next runtime addition needs a real trim (a module split or a cut feature), not a reworded comment.

- Books track 2 (2026-10-22, branch books-track2): cutting and continuity from Katz, Mascelli and Murch. Card fields `pov`, `role`, `protects`, `camera.settle`, `cast[].position_end`, `eyeline_end`, `enters`, `exits`; diff codes EXIT-ENTRY, LOOK-TRACK, MIDDLE-SWAP, ESTABLISH, POV, ROLE; entries point-of-view, group-staging, vehicles, cut-points. Runtime red line raised to 200 KB by Mark (decision 2026-10-22-books-track2), so runtime additions no longer need a trim first. Left for track 4: STRAIGHT-IN, three-quarter default, camera height, `qc cutcheck`, `bg-tangent`, `ots-wrong`.

- Books track 3 (2026-10-22, branch books-track3): visual structure and light from Block, Brown, FilmCraft and Phillips. Scene `intensity`, `space`, `color`; card `line`, `attention`, `light.tone`, `light.atmosphere`; style `visual_structure`; `cards graph`; diff SPACE, KEY-SIDE, ATTENTION; look-pass entry and eight codes; `cine_post.py grade measure --plan`, `grade stabilize`, `grade match --sat --warm`. Runtime 182 KB of red 200. Left for track 4 (decision 2026-10-22-books-track3 G13): arc, push-in and dolly-zoom tokens, lens and focus rules, framing.md, a measured attention check (`qc cutcheck`).

- Books track 4 (2026-10-22, branch books-track4): framing and prompt vocabulary. Card `camera.horizon`, `camera.dutch`, `cast[].view`; moves push-in, arc, dolly-zoom; diff STRAIGHT-IN, HORIZON, DUTCH; rubric `framing` and vocab failures-framing; entries frame-tension, move-grammar. Runtime 185 KB of red 200, about 15 KB left for track 7. No `qc cutcheck` (decision 2026-10-22-books-track4 H8).

- Books track 7 (2026-10-22, branch books-track7): the last cinewright books track. Entries blender-passes (sets) and previs-animation (movement), one line each in master-plates, animatic, blockout-control, fight-previs; the sets description names blockout control passes (L-008 `description-names-blockout-passes`). No runtime change: 185 of 200 KB. Open: whether Mist depth does as well as inverse depth on H3; whether a Line Art pass beats Canny on clay; the previs animation checks against real takes.

- Technique harvest (2026-11-09, 0.5.1): docs only, entry genvideo `h3-long-takes`. Batch 2 (0.5.3; install-test numbers 0.5.4): H3 lint built in `compile` (warn-only, thresholds unmeasured; GPU A/B in harvest posts/1xqfux1.md). Open: `cine.py qc rank` deferred (shared/lib 193 of 200 KB).

## Video analysis track

Prompt: [plans/2026-11-11-video-analysis-continue-prompt.md](plans/2026-11-11-video-analysis-continue-prompt.md). Session 1 (2026-11-11, branch video-analysis-s1, 0.6.0).

Done:
- Diagnosis: [research/2026-11-11-room-scale-failure.md](research/2026-11-11-room-scale-failure.md). Nexus Prominence room 1 is about 16 H wide in the mod against at least 6.2 H in the film: sizes were multipliers of a sample box read off thumbnails, never measured in character heights.
- Research: [film analysis and Gemini](research/2026-11-11-film-analysis-and-gemini-video.md), [AI-video detection](research/2026-11-11-ai-video-detection.md) (both partly unverified, marked inline), [Gemini test](research/2026-11-11-gemini-video-test.md) (gemini-3-flash-preview, 45 s, under a cent: room size close, cuts and timecodes wrong).
- Film notation 0.1 schema (`shared/schemas/film-notation.schema.json`); new skill cinewright-analyze with `scripts/cine_analyze.py` (probe, shots, frame, pan, scale, notate, rebuild; lives in the skill, not shared/lib, which is at 193 of 200 KB) and entries film-notation, room-scale, extraction-routes, ai-video-tells. Tests TestAnalyze (7). Example: `examples/film-notation/` (room 1 measure file, notation, Markdown view, level brief).

Next, in order:
1. Prove it on the benchmark (step 7): find the Project Nexus character height in SceneTools units (the brief assumes 2.0 units, unverified), then write a madnesswright issue or brief with room 1 at about 6.2 x 3.2 H and a side-by-side render with a character at the back wall. No madnesswright code changes (stop point).
2. `aidetect` command (ffprobe tags, c2patool if present, 32 sampled frames, flow-warp residual, ORB homography inliers, FFT and Laplacian, contact sheet) per the detection research's version-1 design; calibrate on our own renders vs phone clips.
3. Pan on cel animation: ORB or landmark matching on the background instead of whole-frame phase correlation (L-20261111-2), so `pan_px` works on the benchmark.
4. Measure rooms 2-10 of the benchmark and fill the notation from shots (Gemini draft plus frames).
5. Harvest and scout targets (step 6): technique-harvest targets and everscout beats for film analysis and notation, AI-video detection, video extraction with Gemini.
6. Run evergreen-test on cinewright-analyze's 8 cases.

Waiting on Mark: nothing yet. Paid Gemini runs past a small test need his go.

## Waiting on Mark
- claude.ai cleanup: delete the uploaded test skill cinewright-continuity (permanent delete; switched off for now), remove the cinewright marketplace source if the UI offers it, close the VS Code window `code chat -n` opened.
- Old commits stay reachable from PR #1-#11 pages (refs/pull); only GitHub Support can purge. Closed PRs #12-#13 show a hostname in their head branch name.
- everlast docs-sync PR mode puts the hostname in branch, title and body: fix in everlast before the next sync to this public repo.
- Registrations (evergreen, mark-local) and directory or awesome-copilot submissions: each needs its own go. Hold the Claude directory until the claude.ai plugin route runs its scripts.
- Audiobook pronunciation of the hero's name and the 4 s H3 test: still open.

## Open from the film test
- Sequence header puts every cast member in every shot; no per-scene constants; the 300-word guide for multi-shot H3.

## Next single action
- Run [next-session-prompt.md](next-session-prompt.md) (S7d: make the skills find their own folder on claude.ai, public CI triggers, 0.1.1).

- 2026-11-01: wiki live (https://github.com/m4bwav/cinewright/wiki), update steps in ai-docs/notes/2026-11-01-github-wiki.md; social preview set. Hosted CI on since PR #70.
