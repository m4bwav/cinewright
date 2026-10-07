# cinewright log

Older entries (S1 to S5): [log-ARCHIVE.md](log-ARCHIVE.md).

## 2026-10-04: session S6, evals and tuning

- Branch: S4 PR #5 merged into `main`, but S5 PR #6 was based on `s4/camera-history` and merged there 15 minutes later, so `main` lacks S5. Neither PR had review comments. `s6/evals` branched off `origin/s4/camera-history` (main plus S5); the S6 PR to `main` carries S5 with it. The runtime budget row question is still unanswered: genvideo's folder stays yellow and is reported, not cut.
- Harness: `evals/run_evals.py` (plan, run, report) and `evals/inspect_run.py`. Each run: a fresh folder under the system temp directory (refused on the repository's drive), a copy of the example without README, design notes or compiled prompts, a per-run copy of the plugin under test, `claude -p --restricted --strict-mcp-config --permission-mode dontAsk`, tools Read, Write, Edit, Bash (plus Skill in the with arm), Bash allowed only for cine.py, ffmpeg, ffprobe, cp, mkdir, ls and dir. Baselines add `--disable-slash-commands`. Graded on the Skill call (triggers stop as soon as it fires), the trace or a file (actions), checker scripts plus a three-vote Sonnet judge (outcomes). Results, traces and run folders stay outside the repository.
- Isolation probed on Claude Code 2.1.281: `--restricted` loads no user skills or plugins (only the plugin dir and the built-in skills), refuses a Read of the repository ("outside ... confines the file tools"), and `dontAsk` refused `ls D:/`. `cd <skill dir> && python scripts/cine.py ...` is allowed by the `Bash(python scripts/cine.py:*)` rule.
- Harness lessons from the pilot (sound and design on Haiku): `claude` on Windows is a `.CMD` wrapper that re-parses arguments, so a multi-line judge prompt arrived empty; the harness now calls the wrapped `claude.exe` and sends every prompt on stdin. `is_error` is set on a nonzero exit too, so a refusal is told apart by its message. The path scan reads only path fields (a Write's content held `d:\n`). A `mkdir -p out/:*` rule missed quoted and absolute paths.
- Cases: outcome-1 replaced for camera (`check_cabin.py`: 2.39 as `frame_aspect`, a `lighting` rule, both verbatim in every compiled prompt), history (`check_kubrick.py`: the kubrick card in `history`, no MOVE or LENS warning, no director's name in any prompt) and sound (`check_mix.py`: a generated cut with a hit near full scale mixed to the web preset, metered by ffmpeg ebur128). Each checker exits 1 on the untouched copy and on a wrong variant (render aspect 2.39; the name in the look; -14 LUFS / -1 dBTP) and 0 on a hand-made correct answer. Neighbour decoys (decoy-3) added to ten skills: three.js renders, cameras and fly-throughs (threewright), price and box-office charts (chartwright), vlog editing, VHS restoration, phone-video checks, podcast loudness and a vlog description. The design action now starts from a setup copy without props.json (no `rm` needed).
- Pilot results worth keeping: Haiku invoked cinewright-sound on "generate a lo-fi hip hop track" and on the podcast decoy; did not invoke it on the sound action case (mixed by hand to -23 LUFS); answered the design advice case without the skill.

## 2026-10-05: session S6 continued, matrix, two tuning rounds, worth

- Full matrix run on Mark's go (2026-10-04): 870 headless runs plus judge calls; then reruns after each fix. All runs including reruns: 2,368 headless runs, $300.46 reported by the CLI at list price (judge calls not counted; the runs now on record, one per matrix cell, report $88). Results, traces and run folders stay outside the repository (location in the vault sidecar note).
- Most first-matrix "failures" were the harness: twelve faults, each written up with its fix in [solutions/2026-10-05-headless-evals-on-windows-dead-ends.md](solutions/2026-10-05-headless-evals-on-windows-dead-ends.md). The biggest: `dontAsk` refuses `cp -r` whatever the rule, `Bash(python scripts/cine.py:*)` missed absolute paths, craft compile cases lacked the core plugin, the account's session limit (HTTP 429) read as 155 failures, a 30-turn cap cut Sonnet off, and the judge graded only the last message. Design: [decisions/2026-10-05-eval-harness-and-model-matrix.md](decisions/2026-10-05-eval-harness-and-model-matrix.md).
- Cases changed: camera, history and sound outcome-1 replaced (checkers `check_cabin.py`, `check_kubrick.py`, `check_mix.py`); continuity outcome-1 replaced by two one-word plants (scar side, sweater colour) the diff catches; genvideo outcome-1 graded by `check_veo.py`; router and shots outcomes run their `cine.py` checks; edit outcome-1 asks about a mid-shot fault too; decoy-3 against neighbours in ten skills; action evidence is the trace only where a baseline passed on a file.
- Tuning round 1 (descriptions, C-20261004-2/-3): sound, edit and finish exclude podcasts and music, vlogs and live footage, home-video restoration; genvideo, history, camera, shots and the router match the phrasings that undertriggered; qc trimmed for room; script runs the diff whenever a line changes (cinewright-script L-002). Round 2 (C-20261005-1): continuity reports the diff's errors before by-eye doubts (cinewright-continuity L-005), edit states the mid-shot rule (cinewright-edit L-004), qc builds the rubric with no clip and never by hand (cinewright-qc L-003), camera says "lighting a shot" after "a scene" drew the three.js decoy (cinewright-camera L-002).
- Runtime fix: `cine.py` crashed (TypeError, KeyError) on a characters.json in another shape that Opus wrote; `bible_entries()` now stops with the file, key and schema to fix. Test `test_malformed_bible_says_what_to_fix` (64 tests).
- Merge question (PLAN section 2, shots and continuity): no overlap. Neither skill fired on the other's triggers in any run; shots' triggers went to the router, qc's to continuity. No merge proposed.
- Worth (with versus without, pooled over three models, 18 with and 6 without runs per skill): no CUT. KEEP: design +78 points at 1.34x cost, sound +56 at 1.36x, genvideo +78 at 0.97x. TRIM (gain beyond noise at 1.5x the cost or more): camera +67 at 1.89x, edit +44 at 2.11x, finish +50 at 2.3x, history +67 at 1.67x, movement +61 at 2.9x, script +72 at 2.15x, router +78 at 2.39x, continuity +61 at 1.5x, qc +61 at 2.22x, shots +56 at 2.06x. Part of the cost ratio is that baselines give up early. Recorded in each evergreen.json `worth`.
- Where it stands (T-20261005-1 in every TESTS.md): Sonnet passes every case except four at 2 of 3 (design outcome, finish action, movement outcome, qc outcome). Opus fails seven cases at 1 or 2 of 3 (camera, continuity, movement, qc, script actions; shots outcome, whose crash is fixed but not rerun; continuity outcome after its fix not rerun). Haiku fails most action and outcome cases and several triggers: it answers in one turn without loading the skill; recorded, not tuned further (decision item 5). The S6 exit check does not pass yet, so no PR was opened; the next session finishes it.
- Budget: descriptions 3,888 of 4,000 (green; about 110 left for curate, which needs about 200: S7 will read yellow unless something is trimmed). genvideo's folder reads 166 KB (yellow, the unanswered runtime budget row; this session added `check_veo.py` and cases).

Check output (2026-10-05, Windows 11, Python 3.14.6 and 3.9.25):

```
$ python -m unittest discover -s tests
Ran 64 tests in 12.521s
OK
$ py -V:Astral/CPython3.9.25 -m unittest discover -s tests
Ran 64 tests in 12.140s
OK
$ python scripts/cine.py kb lint
kb lint: 13 skills, 0 errors
$ python scripts/cine.py budget
one description, characters                 344      350      500  green  cinewright-camera
all descriptions, characters               3888     4000     5500  green  13 skills
core descriptions, characters              1565     1800     2500  green  plugins/cinewright
skill folder KB                             166      150      300  yellow cinewright-genvideo
budget: YELLOW (tokens are bytes / 4, an estimate)
$ claude plugin validate . (and plugins/cinewright, plugins/cinewright-craft, plugins/cinewright-dev)
✔ Validation passed (four times)
$ evergreen.py lint <each skill>
13 skills: lint OK
```

Matrix after round 2 (with the skill: invocations for triggers, passes otherwise; baseline per model):

| skill | case | kind | haiku | sonnet | opus | baseline (h/s/o) |
|---|---|---|---|---|---|---|
| cinewright | action-1 | action | **FAIL** 1/3 | 3/3 | 3/3 | fail/fail/fail |
| cinewright | decoy-1 | trigger decoy | 0/3 invoked | 0/3 invoked | 0/3 invoked |  |
| cinewright | decoy-2 | trigger decoy | 0/3 invoked | 0/3 invoked | 0/3 invoked |  |
| cinewright | decoy-3 | trigger decoy | 0/3 invoked | 0/3 invoked | 0/3 invoked |  |
| cinewright | outcome-1 | outcome | **FAIL** 1/3 | 3/3 | 3/3 | fail/fail/fail |
| cinewright | trigger-1 | trigger | **FAIL** 0/3 invoked | 3/3 invoked | 3/3 invoked |  |
| cinewright | trigger-2 | trigger | 3/3 invoked | 3/3 invoked | 3/3 invoked |  |
| cinewright-camera | action-1 | action | **FAIL** 2/3 | 3/3 | **FAIL** 1/3 | fail/fail/fail |
| cinewright-camera | decoy-1 | trigger decoy | 0/3 invoked | 0/3 invoked | 0/3 invoked |  |
| cinewright-camera | decoy-2 | trigger decoy | 0/3 invoked | 0/3 invoked | 0/3 invoked |  |
| cinewright-camera | decoy-3 | trigger decoy | **FAIL** 3/3 invoked | 0/3 invoked | 0/3 invoked |  |
| cinewright-camera | outcome-1 | outcome | **FAIL** 0/3 | 3/3 | 3/3 | fail/fail/fail |
| cinewright-camera | trigger-1 | trigger | 3/3 invoked | 3/3 invoked | 3/3 invoked |  |
| cinewright-camera | trigger-2 | trigger | 3/3 invoked | 3/3 invoked | 3/3 invoked |  |
| cinewright-continuity | action-1 | action | 3/3 | 3/3 | **FAIL** 2/3 | fail/fail/fail |
| cinewright-continuity | decoy-1 | trigger decoy | 0/3 invoked | 0/3 invoked | 0/3 invoked |  |
| cinewright-continuity | decoy-2 | trigger decoy | 0/3 invoked | 0/3 invoked | 0/3 invoked |  |
| cinewright-continuity | outcome-1 | outcome | **FAIL** 0/3 | 3/3 | 3/3 | fail/pass/fail |
| cinewright-continuity | trigger-1 | trigger | 3/3 invoked | 3/3 invoked | 3/3 invoked |  |
| cinewright-continuity | trigger-2 | trigger | 2/3 invoked | 3/3 invoked | 3/3 invoked |  |
| cinewright-design | action-1 | action | **FAIL** 2/3 | 3/3 | 3/3 | fail/fail/fail |
| cinewright-design | decoy-1 | trigger decoy | 0/3 invoked | 0/3 invoked | 0/3 invoked |  |
| cinewright-design | decoy-2 | trigger decoy | 0/3 invoked | 0/3 invoked | 0/3 invoked |  |
| cinewright-design | outcome-1 | outcome | **FAIL** 1/3 | **FAIL** 2/3 | 3/3 | fail/fail/fail |
| cinewright-design | trigger-1 | trigger | 3/3 invoked | 3/3 invoked | 3/3 invoked |  |
| cinewright-design | trigger-2 | trigger | 2/3 invoked | 3/3 invoked | 3/3 invoked |  |
| cinewright-edit | action-1 | action | **FAIL** 0/3 | 3/3 | 3/3 | fail/fail/fail |
| cinewright-edit | decoy-1 | trigger decoy | 0/3 invoked | 0/3 invoked | 0/3 invoked |  |
| cinewright-edit | decoy-2 | trigger decoy | 0/3 invoked | 0/3 invoked | 0/3 invoked |  |
| cinewright-edit | decoy-3 | trigger decoy | **FAIL** 2/3 invoked | 0/3 invoked | 0/3 invoked |  |
| cinewright-edit | outcome-1 | outcome | **FAIL** 2/3 | 3/3 | 3/3 | fail/pass/pass |
| cinewright-edit | trigger-1 | trigger | 3/3 invoked | 3/3 invoked | 3/3 invoked |  |
| cinewright-edit | trigger-2 | trigger | 3/3 invoked | 3/3 invoked | 3/3 invoked |  |
| cinewright-finish | action-1 | action | **FAIL** 0/3 | **FAIL** 2/3 | 3/3 | fail/fail/pass |
| cinewright-finish | decoy-1 | trigger decoy | 0/3 invoked | 0/3 invoked | 0/3 invoked |  |
| cinewright-finish | decoy-2 | trigger decoy | 0/3 invoked | 0/3 invoked | 0/3 invoked |  |
| cinewright-finish | decoy-3 | trigger decoy | **FAIL** 1/3 invoked | 0/3 invoked | 0/3 invoked |  |
| cinewright-finish | outcome-1 | outcome | **FAIL** 1/3 | 3/3 | 3/3 | fail/fail/fail |
| cinewright-finish | trigger-1 | trigger | 3/3 invoked | 3/3 invoked | 3/3 invoked |  |
| cinewright-finish | trigger-2 | trigger | 2/3 invoked | 3/3 invoked | 3/3 invoked |  |
| cinewright-genvideo | action-1 | action | **FAIL** 2/3 | 3/3 | 3/3 | fail/fail/fail |
| cinewright-genvideo | decoy-1 | trigger decoy | 0/3 invoked | 0/3 invoked | 0/3 invoked |  |
| cinewright-genvideo | decoy-2 | trigger decoy | 0/3 invoked | 0/3 invoked | 0/3 invoked |  |
| cinewright-genvideo | decoy-3 | trigger decoy | 0/3 invoked | 0/3 invoked | 0/3 invoked |  |
| cinewright-genvideo | outcome-1 | outcome | **FAIL** 0/3 | 3/3 | 3/3 | fail/fail/fail |
| cinewright-genvideo | trigger-1 | trigger | **FAIL** 0/3 invoked | 3/3 invoked | 3/3 invoked |  |
| cinewright-genvideo | trigger-2 | trigger | **FAIL** 0/3 invoked | 3/3 invoked | 3/3 invoked |  |
| cinewright-history | action-1 | action | **FAIL** 0/3 | 3/3 | 3/3 | fail/fail/fail |
| cinewright-history | decoy-1 | trigger decoy | 0/3 invoked | 0/3 invoked | 0/3 invoked |  |
| cinewright-history | decoy-2 | trigger decoy | 0/3 invoked | 0/3 invoked | 0/3 invoked |  |
| cinewright-history | decoy-3 | trigger decoy | 0/3 invoked | 0/3 invoked | 0/3 invoked |  |
| cinewright-history | outcome-1 | outcome | **FAIL** 0/3 | 3/3 | 3/3 | fail/fail/fail |
| cinewright-history | trigger-1 | trigger | **FAIL** 0/3 invoked | 3/3 invoked | 3/3 invoked |  |
| cinewright-history | trigger-2 | trigger | 2/3 invoked | 3/3 invoked | 3/3 invoked |  |
| cinewright-movement | action-1 | action | **FAIL** 1/3 | 3/3 | **FAIL** 2/3 | fail/fail/fail |
| cinewright-movement | decoy-1 | trigger decoy | 0/3 invoked | 0/3 invoked | 0/3 invoked |  |
| cinewright-movement | decoy-2 | trigger decoy | 0/3 invoked | 0/3 invoked | 0/3 invoked |  |
| cinewright-movement | outcome-1 | outcome | **FAIL** 0/3 | **FAIL** 2/3 | 3/3 | fail/fail/fail |
| cinewright-movement | trigger-1 | trigger | 2/3 invoked | 3/3 invoked | 3/3 invoked |  |
| cinewright-movement | trigger-2 | trigger | 3/3 invoked | 3/3 invoked | 3/3 invoked |  |
| cinewright-qc | action-1 | action | **FAIL** 1/3 | 3/3 | **FAIL** 2/3 | fail/fail/fail |
| cinewright-qc | decoy-1 | trigger decoy | 0/3 invoked | 0/3 invoked | 0/3 invoked |  |
| cinewright-qc | decoy-2 | trigger decoy | 0/3 invoked | 0/3 invoked | 0/3 invoked |  |
| cinewright-qc | decoy-3 | trigger decoy | 0/3 invoked | 0/3 invoked | 0/3 invoked |  |
| cinewright-qc | outcome-1 | outcome | **FAIL** 0/3 | **FAIL** 2/3 | 3/3 | fail/fail/fail |
| cinewright-qc | trigger-1 | trigger | 3/3 invoked | 3/3 invoked | 3/3 invoked |  |
| cinewright-qc | trigger-2 | trigger | **FAIL** 1/3 invoked | 3/3 invoked | 3/3 invoked |  |
| cinewright-script | action-1 | action | 3/3 | 3/3 | **FAIL** 2/3 | fail/fail/fail |
| cinewright-script | decoy-1 | trigger decoy | 0/3 invoked | 0/3 invoked | 0/3 invoked |  |
| cinewright-script | decoy-2 | trigger decoy | 0/3 invoked | 0/3 invoked | 0/3 invoked |  |
| cinewright-script | decoy-3 | trigger decoy | 0/3 invoked | 0/3 invoked | 0/3 invoked |  |
| cinewright-script | outcome-1 | outcome | **FAIL** 2/3 | 3/3 | 3/3 | fail/fail/pass |
| cinewright-script | trigger-1 | trigger | 3/3 invoked | 3/3 invoked | 3/3 invoked |  |
| cinewright-script | trigger-2 | trigger | 3/3 invoked | 3/3 invoked | 3/3 invoked |  |
| cinewright-shots | action-1 | action | **FAIL** 0/3 | 3/3 | 3/3 | fail/fail/fail |
| cinewright-shots | decoy-1 | trigger decoy | 0/3 invoked | 0/3 invoked | 0/3 invoked |  |
| cinewright-shots | decoy-2 | trigger decoy | 0/3 invoked | 0/3 invoked | 0/3 invoked |  |
| cinewright-shots | decoy-3 | trigger decoy | 0/3 invoked | 0/3 invoked | 0/3 invoked |  |
| cinewright-shots | outcome-1 | outcome | **FAIL** 0/3 | 3/3 | **FAIL** 1/3 | fail/fail/fail |
| cinewright-shots | trigger-1 | trigger | **FAIL** 1/3 invoked | 3/3 invoked | 3/3 invoked |  |
| cinewright-shots | trigger-2 | trigger | **FAIL** 0/3 invoked | 3/3 invoked | 3/3 invoked |  |
| cinewright-sound | action-1 | action | **FAIL** 0/3 | 3/3 | 3/3 | fail/fail/fail |
| cinewright-sound | decoy-1 | trigger decoy | **FAIL** 1/3 invoked | 0/3 invoked | 0/3 invoked |  |
| cinewright-sound | decoy-2 | trigger decoy | 0/3 invoked | 0/3 invoked | 0/3 invoked |  |
| cinewright-sound | decoy-3 | trigger decoy | **FAIL** 1/3 invoked | 0/3 invoked | 0/3 invoked |  |
| cinewright-sound | outcome-1 | outcome | **FAIL** 1/3 | 3/3 | 3/3 | fail/pass/fail |
| cinewright-sound | trigger-1 | trigger | 3/3 invoked | 3/3 invoked | 3/3 invoked |  |
| cinewright-sound | trigger-2 | trigger | 3/3 invoked | 3/3 invoked | 3/3 invoked |  |
## [2026-10-05] index | rebuilt (15 entries)

## 2026-10-05: session S6 finished, harness rev 2, exit check, PR

- No comments from Mark since 2026-10-05; the runtime budget row question is still unanswered (genvideo's folder 167 KB, yellow, reported).
- Pending reruns on the old harness (24 runs): continuity outcome-1 and shots outcome-1, both arms, three models. Sonnet 3 of 3 on both; Opus 1 of 3 and 2 of 3.
- The Opus pattern (HANDOFF "Watch") is harness friction, decided on the traces: every Opus failure, 10 of 10 across two batches, began with one refused command (a `for` loop, `find`, a chained `cat` from Step 0), after which Opus said "Bash is blocked in this session" and never ran `cine.py`. The refusal text is Claude Code's generic "Permission to use Bash has been denied because Claude Code is running in don't ask mode"; interactively the same command prompts the user. 59 of 67 Opus runs with a refusal recovered. A skill rule would cost every user tokens for a test-only condition. Fix, harness rev 2: `--append-system-prompt` tells both arms a refusal covers that command only (names no tool, so the baseline learns nothing); every result records `harness`. Row added to [solutions/2026-10-05-headless-evals-on-windows-dead-ends.md](solutions/2026-10-05-headless-evals-on-windows-dead-ends.md).
- Rev-2 reproduction (40 runs): Opus camera, continuity, movement, qc and script actions 3 of 3 (were 1-2 of 3); shots outcome 3 of 3; continuity outcome 2 of 3; Sonnet finish action, movement and qc outcomes 3 of 3 (were 2 of 3; recorded as flaky, no skill edit). Baselines still fail on every action case.
- Design outcome-1: Sonnet's failing reply was right ("keep the negative prompt too, but know it's secondary"); the judge read that as relying on it. Expectation reworded (the fix offered is cleaning the reference) and rejudged: Sonnet 3 of 3. Side effect: the Opus baseline now passes, so on Opus this case shows no gain.
- Continuity outcome-1 Opus, the one Sonnet/Opus miss left: the run ran the diff, named both plants and said to copy the bible string exactly, but showed a one-word fix; the judge gave the word-for-word expectation 1 of 3. Recorded as a judge split, not tuned.
- Budget: Mark is near the weekly limit until Wednesday 2026-10-08 and chose the cheaper options: no full rev-2 rerun of the value cases (312 runs; the record is mixed and says so in each T- entry), no skill edits for 1-in-3 slips (each costs a three-model suite rerun). This session: 64 headless runs, $20.36 at list price, judge calls not counted.
- Lessons marked "rerun pending", judged against T-20261005-1 (all runs post-date their edits): confirmed camera L-002 `lighting-a-shot`, edit L-004 `mid-shot-rule`, finish L-003 `not-home-video`, history L-003 `director-look-question`, script L-002 `diff-not-counting`, sound L-003 `not-podcasts-or-music`, continuity L-005 `diff-errors-first`, qc L-003 `rubric-never-by-hand`, cinewright L-001 `idea-as-shots`. Retired to new LEARNINGS-ARCHIVE.md files (the edit did not move Haiku; Sonnet and Opus passed before and after; descriptions unchanged): edit L-003, genvideo L-006, shots L-001.
- Records: T-20261005-2 in every TESTS.md with the tests block and dated baselines (`record_tests.py`); worth recorded from `export-worth`: no CUT; KEEP design, sound, continuity (moved up from TRIM, +67 at 1.29x), genvideo; TRIM camera, edit, finish, history, movement, script, qc, shots, cinewright (recommendation only).
- Final matrix (88 cases): Sonnet 88 of 88, Opus 87 of 88 (continuity outcome-1, judge split), Haiku 52 of 88 (36 failures, each recorded under decision item 5: Haiku answers without loading the skill, or takes a neighbour's decoy). Full table: matrix-final-s6.md in the results folder (vault sidecar note).

Check output (2026-10-05, Windows 11, Python 3.14.6 and 3.9.25):

```
$ python -m unittest discover -s tests
Ran 64 tests in 12.792s
OK
$ py -V:Astral/CPython3.9.25 -m unittest discover -s tests
Ran 64 tests in 12.490s
OK
$ python scripts/cine.py kb lint
kb lint: 13 skills, 0 errors
$ python scripts/cine.py budget
all descriptions 3888 of 4000 green; skill folder KB 167 yellow cinewright-genvideo (the unanswered runtime row); everything else green
budget: YELLOW
$ claude plugin validate . (and plugins/cinewright, plugins/cinewright-craft, plugins/cinewright-dev)
✔ Validation passed (four times)
$ evergreen.py lint <each skill>
13 skills: lint OK
```
## [2026-10-05] index | rebuilt (15 entries)
## [2026-10-05] index | rebuilt (16 entries)

## 2026-10-06: cinewright-sound learns to conform sound to a tempo

- Source: field notes from recorded game sound effects fitted to a 90 BPM grid (2026-10-04 to 2026-10-06; a private project, unnamed per [decisions/2026-10-03-field-lessons-cited-without-the-private-source-s-name.md](decisions/2026-10-03-field-lessons-cited-without-the-private-source-s-name.md)). What transfers to film: conforming effects and foley to a cue's tempo.
- Added: entry `conform-to-tempo` in cinewright-sound (tempo match, then warp, then cut; Rubber Band `rubberband=tempo=R:transients=crisp:detector=percussive:pitchq=quality`, ratios 0.75-1.35; beats, eighths and triplets, grace notes ride the main hit; quiet edit points; stereo correlation before a mono mixdown; active RMS; report unheard until a person has auditioned it). One pointer line in SKILL.md Step 2. Records: C-20261006-1, R-20261006-1, evergreen.json counts. Description unchanged, so the trigger evals stand.
- Skipped: clip length following a game's production cycle (game-only); Unity import notes (not sound craft); the source's script names and paths (private, game-specific). The first draft of the entry was 1,001 estimated tokens (yellow); trimmed to green.
- Branch `sound/beat-grid-conform` off `origin/main` in a separate worktree; the main clone stays on `s6/evals`.

Check output (2026-10-06, Windows 11):

```
$ python -m unittest discover -s tests
Ran 64 tests ... OK
$ python scripts/cine.py kb lint
kb lint: 13 skills, 0 errors
$ python scripts/cine.py budget
skill folder KB 167 yellow cinewright-genvideo (the unanswered runtime row, unchanged); everything else green
budget: YELLOW
$ claude plugin validate . (and plugins/cinewright, plugins/cinewright-craft, plugins/cinewright-dev)
Validation passed (four times)
$ evergreen.py lint plugins/cinewright-craft/skills/cinewright-sound
cinewright-sound: lint OK
```

## 2026-10-06: session S7, curate, packaging, install proof, scrub

- S6 PR #7 merged with no comments; PR #8 (cinewright-sound beat-grid conform, another session) merged into main mid-session; `s7/package` rebased onto it. No answer yet on the runtime budget row: genvideo stays yellow, reported.
- cinewright-curate built in `plugins/cinewright-dev/` (evergreen unit via `evergreen.py init --pointer`, then `unregister`, the registry being another repo). Commands in the maintainer CLI, not the runtime: `kb due|new|verify|retire`; plus `cine.py scrub`. Decision: [decisions/2026-10-06-curate-commands-in-the-maintainer-cli-and-scrub-names-outside-the-repo.md](decisions/2026-10-06-curate-commands-in-the-maintainer-cli-and-scrub-names-outside-the-repo.md). Six new tests.
- Harness: `fixture: "repo"` (scripts, shared, plugins without cinewright-dev, filtered marketplace.json) for maintainer skills.
- Curate suite (budget week, Mark's cheaper-option rule): Sonnet 3 runs per case, Haiku and Opus 1, one baseline per model; 36 runs plus a 3-run Sonnet rerun. Sonnet outcome-1 failed 0 of 3: the table row `kb retire <slug> --reason R [--status deprecated]` was copied verbatim (curate L-001 `optional-flag-copied`); row split (C-20261006-2), rerun 3 of 3. Final T-20261006-2: Sonnet 6 of 6 cases, Opus 6 of 6 (its baseline also passed action and outcome by reading the CLI help: little gain on Opus), Haiku 3 of 6 (trigger-2, decoy-2, action-1; decision item 5 pattern, recorded not tuned). Deferred: 3 runs per case on Haiku and Opus.
- Description budget 4,082 of 4,000: YELLOW (curate adds 194 characters). Nothing trimmed; Mark's call.
- Install proof on the private repo (Windows): Claude Code marketplace, Copilot CLI marketplace and `gh skill install` each installed and triggered cinewright-continuity once; `gh skill` finds all 13 skills under `plugins/*/skills/`. claude.ai skill upload stopped at the preview (ZIP accepted); claude.ai marketplace and VS Code Copilot not run (they change Mark's account or settings). Second OS: untested elsewhere. Record: [notes/2026-10-06-s7-install-proof.md](notes/2026-10-06-s7-install-proof.md). Every test install removed.
- ZIPs: 13 built in `dist/` (gitignored, 44-70 KB each), release assets.
- Public scrub: 33 hits first. Research brief sections 1 and 2 (request path, local prior art with paths and private project names) moved verbatim to the vault sidecar note "Research brief sections 1 and 2, request and local prior art (private)"; the repo keeps a neutral version with the generalised field lessons. The private local-render skill's name replaced in PLAN, the log archive and one solution; one code comment's sample path neutralised. False positives fixed in scrub (string escapes, CLAUDE.local.md). Names list: vault sidecar `scrub-names.txt`. Now 0 hits. The repo is still private (D5 waits for Mark).
- evergreen 0.13.0 lint wants SETUP.md double-linked with every companion: qc's SETUP.md, RESEARCH, LEARNINGS and TESTS now link both ways.

Check output (2026-10-06, Windows 11, Python 3.14.6 and 3.9.25):

```
$ python -m unittest discover -s tests
Ran 70 tests in 18.792s
OK
$ py -V:Astral/CPython3.9.25 -m unittest discover -s tests
Ran 70 tests in 18.697s
OK
$ python scripts/cine.py kb lint
kb lint: 14 skills, 0 errors
$ python scripts/cine.py budget
all descriptions 4082 of 4000 yellow (curate); skill folder KB 167 yellow cinewright-genvideo (the unanswered runtime row); everything else green
budget: YELLOW
$ python scripts/cine.py scrub --names <vault sidecar scrub-names.txt>
scrub: 0 hits in 0 files
$ claude plugin validate . (and plugins/cinewright, plugins/cinewright-craft, plugins/cinewright-dev)
Validation passed (four times)
$ evergreen.py lint <each skill>   (evergreen 0.13.0)
14 skills: lint OK
```
## [2026-10-06] index | rebuilt (18 entries)
## [2026-10-06] index | rebuilt (18 entries)

## [2026-10-07] test | first end-to-end film (library adaptation, overnight)

- Mark's go 2026-10-06 21:00: "yes or as you recommend" to the four waiting items, but a test film before anything is submitted. Applied tonight: the runtime budget row and the description trim (budget GREEN). Waiting: claude.ai and VS Code routes, D5 public, release, registrations, submissions.
- The test: a 120 s adaptation of one novel chapter, planned with cinewright (25 cards, 8 sequences) and rendered in five passes on local H3. Findings, fixes and open items: [notes/2026-10-07-library-film-test.md](notes/2026-10-07-library-film-test.md).
- Compiler fixes on test/library-film: 362 frames for 15 s on H3, card-only travel, no double article, `cards export --film-json --sequence --model`. Lessons: design L-004, genvideo L-009 to L-011.

Check output (2026-10-07, Windows 11):

```
$ python -m unittest discover -s tests
Ran 73 tests ... OK
$ py -V:Astral/CPython3.9.25 -m unittest discover -s tests
Ran 73 tests ... OK
$ python scripts/cine.py kb lint
kb lint: 14 skills, 0 errors
$ python scripts/cine.py budget
budget: GREEN
```

## [2026-10-07] fix | dialogue: off-screen speakers and names (owner's review of the library film)

- Mark watched the best-of film and found two problems. A rival sorcerer's off-screen line was spoken by the hero (card 6D), and the hero's name was said less well than in his audiobook. He asked for no new render, only that the learnings go into this pass.
- Branch s7b/release (PR #10 had merged): `compile` writes off-screen lines with H3's voiceover phrase and adds a lips-closed clause for everyone else in the shot; models without a voiceover template leave the line out with a warning; `continuity diff` gains OFFSCREEN, SPEAKERS, TONE and PRONOUNCE; characters.json gains `pronounce`; the QC rubric marks off-screen lines; new failure code `name-misread`. Decision (proposed): [decisions/2026-10-07-off-screen-lines-compile-as-voiceovers-or-leave-the-prompt.md](decisions/2026-10-07-off-screen-lines-compile-as-voiceovers-or-leave-the-prompt.md).
- Lessons: genvideo L-012, script L-003. The night's genvideo lessons had been filed as L-006 to L-008, but L-006 already sat in the archive, so they are now L-009 to L-011 (note, HANDOFF and the entry above corrected).
- Budget: the dialogue reference went yellow (1,039 tokens) and was rewritten to fit; failures-motion trimmed back under 700.

```
$ python -m unittest discover -s tests
Ran 80 tests ... OK
$ py -V:Astral/CPython3.9.25 -m unittest discover -s tests
Ran 80 tests ... OK
$ python scripts/cine.py kb lint
kb lint: 14 skills, 0 errors
$ python scripts/cine.py budget
budget: GREEN
$ python scripts/cine.py scrub --names <sidecar scrub-names.txt>
scrub: 0 hits in 0 files
$ evergreen.py lint cinewright-genvideo ; evergreen.py lint cinewright-script
lint OK (both)
```
## [2026-10-07] index | rebuilt (20 entries)
## [2026-10-07] index | rebuilt (20 entries)

## [2026-10-07] release | S7b: history scrub before going public (blocked at the force-push)

- PR #11 merged; branch s7b/routes off main b588d23. All 13 ZIPs rebuilt from main (`cine.py zip`, 46-73 KB each; the old ones predated #11).
- Working tree clean: `scrub --names <sidecar scrub-names.txt>` 0 hits, `kb lint` 0 errors, budget GREEN.
- New check: going public publishes every old commit, and `scrub` only reads the working tree. The same patterns run over every blob reachable from any ref, every commit message and every PR title, body, comment and review found 10 distinct hits (36 lines): drive paths and private project names in old copies of the research brief, PLAN, the log, two next-session prompts and one solution, plus a sample drive path in an old eval-harness comment. Commit messages and PR text were clean.
- Mark chose (2026-10-07): rewrite history and force-push. `git filter-repo --replace-text` (pip `git-filter-repo`) on a fresh single-branch clone of main: 19 commits rewritten, HEAD tree unchanged (a371d77 before and after, so no current file changed), rescan of the rewritten history 0 lines. Backup of the old history: bundle `cinewright-pre-public-history-2026-10-07.bundle` next to the repo folder (outside it). Replacement list and the two scan scripts: vault sidecar (`history-rewrite-replacements.txt`, `history-scrub-scan.py`, `history-scrub-summary.py`).
- Blocked: Claude Code's auto-mode classifier refused the force-push of main and the deletion of the eight merged branches (they still point at old commits), and then a browser call for the claude.ai route. Nothing was pushed; the remote is unchanged. Limit to keep in mind: GitHub keeps each PR's head under `refs/pull/N/head`, which a force-push cannot move, so the old commits stay reachable from PR #1-#11 pages once public; only GitHub Support can purge those (or a fresh repository avoids them).
- Not yet done: claude.ai skill Upload, claude.ai Add marketplace, VS Code Copilot route, public, public retests, 0.1.0. A 0.1.0 tag must sit on main after this branch merges (the repo squash-merges).

## [2026-10-07] release | S7b: history rewritten, repo public, public routes retested, 0.1.0 PR

- Mark switched to manual mode and said "do all the things". The rewrite went out: `git push --force origin main` (b588d23 to 01df838, same tree a371d77), and the eight merged PR branches deleted. Two everlast docs-sync PRs (#12, #13) had opened from branches named after the machine's hostname, holding this session's first log entry; closed as superseded with their branches deleted, titles and bodies made neutral. Their head branch names still show on the closed PR pages; GitHub has no rename for a closed PR's head.
- Pre-public check on a fresh clone: history scan 0 lines; every PR title, body, comment and review 0 hits. `gh repo edit --visibility public` at 2026-10-07: PUBLIC.
- Public-route retests, nothing cached, one install and one trigger each, removed afterwards (`~/.claude/plugins/cache/cinewright/` deleted by hand):
  - Claude Code 2.1.x: `claude plugin marketplace add m4bwav/cinewright --scope local` + `claude plugin install cinewright@cinewright --scope local`: 5 skills. Haiku answered from its own knowledge without the skill (1 turn, $0.04); Sonnet called `Skill cinewright:cinewright-continuity`, then its `cine.py` (6 turns, $0.33). PASS on Sonnet; the Haiku miss is one run, not a suite result.
  - `gh skill install m4bwav/cinewright cinewright-continuity --agent claude-code --scope project`: exit 0 this time (the private run exited 2 after writing every file); `metadata:` block points at refs/heads/main; Sonnet called `Skill cinewright-continuity` ($0.20). PASS.
  - Copilot CLI: `copilot plugin marketplace add m4bwav/cinewright`, `copilot plugin install cinewright@cinewright`: "Installed 5 skills"; `copilot -p ... --output-format json` called `skill` with `{"skill":"cinewright-continuity"}`. PASS.
- Not run: claude.ai skill Upload, claude.ai Add marketplace, VS Code Copilot. The auto-mode classifier refused the browser for claude.ai ("unrequested commit in a connected app") even in manual mode; VS Code needs a user-settings change and the chat UI. They wait for Mark to approve them in a session.
- Versions 0.0.1 to 0.1.0 in marketplace.json (4) and each plugin's two manifests (6). ZIPs rebuilt from 01df838 in `dist/` (release assets, gitignored). Tag and GitHub Release wait for this PR to merge (squash merges: a tag on the branch would not be on main).
- Lesson for everlast (outside this repo): docs-sync PR mode names branches `everlast/docs-<HOSTNAME>-<stamp>` and puts the hostname in the PR title and body, which leaks it on a public repository.

Exit check (2026-10-07, Windows 11, s7b/routes):

```
$ python -m unittest discover -s tests
Ran 80 tests ... OK
$ py -V:Astral/CPython3.9.25 -m unittest discover -s tests
Ran 80 tests ... OK
$ python scripts/cine.py kb lint
kb lint: 14 skills, 0 errors
$ python scripts/cine.py budget
budget: GREEN
$ python scripts/cine.py scrub --names <sidecar scrub-names.txt>
scrub: 0 hits in 0 files
$ claude plugin validate . (and plugins/cinewright, plugins/cinewright-craft, plugins/cinewright-dev)
Validation passed (four times)
$ evergreen.py lint <each skill>
14 skills: lint OK
```

## [2026-10-07] release | S7c: v0.1.0 released, three account routes run

- PR #14 merged by Mark. Before the tag: `scrub --names <sidecar scrub-names.txt>` 0 hits, `kb lint` 0 errors, budget GREEN, 80 tests OK; the 13 ZIPs rebuilt from main (46-73 KB) and their unzipped contents scanned for private strings: clean.
- README still said "Status: 0.0.1, private": fixed in docs-only PR #15 (merged; the CI workflow is manual-dispatch only, so no checks ran; local checks above).
- Tag `v0.1.0` on main fad9ec6, pushed. Release: https://github.com/m4bwav/cinewright/releases/tag/v0.1.0, 13 assets (one ZIP per public skill).
- Account routes, Mark's yes in the session: claude.ai skill Upload PASS; claude.ai Add marketplace: trigger PASS, but the skill's scripts failed because the model guessed the plugin skill folder as `/mnt/skills/plugins/cinewright:cinewright-continuity`; VS Code Copilot Chat PASS through the Copilot CLI agent host (CLI install, settings change, `code chat`). Details and cleanup: [notes/2026-10-06-s7-install-proof.md](notes/2026-10-06-s7-install-proof.md). Lesson L-006 `claude-ai-plugin-skill-folder-unknown` in cinewright-continuity.
- Blocked: a follow-up chat message asking claude.ai's sandbox to list `/mnt/skills` (to learn the real plugin folder) was refused by the auto-mode classifier; nothing was sent. The next session finds the folder another way.
- Left for Mark: delete the uploaded test skill on claude.ai (permanent delete, switched off for now), remove the cinewright marketplace source there if the UI allows, close the VS Code window opened by `code chat -n`.
- Follow-ups: CI still has only `workflow_dispatch` (written for the private period); the repo is public, so push and pull_request triggers on GitHub-hosted runners are now free.

## [2026-10-07] build | cinewright-sets: set and location skill, wall strings in the compiler

- New craft skill `cinewright-sets` (evergreen, tier moderate, 30 days): set plan, per-wall strings, master plates, coverage and reverse angles, set light, plate check. Six entries: set-plan, wall-strings, master-plates, coverage-angles, set-light, set-check. Research: [RESEARCH.md](../plugins/cinewright-craft/skills/cinewright-sets/RESEARCH.md) R-20261007-1 (no dedicated set or location bible skill exists; DirectorSKILL and Storyboarder.ai's location editor are closest).
- Field test that shaped it: a real public building as 11 sets on a local image model. A reverse and an east-door shot written as framing words after the full room description both came back as the establishing view (2 of 2). L-001 `whole-room-string-pulls-to-hero-wall`.
- Runtime: location bible `walls` (key to a 20-300 character string), shot card `camera.faces`, compile adds the faced wall after the description, `cards validate` and `continuity diff` give WALL for an unknown key, the validator learned `propertyNames`. Three unit tests.
- Registered in both craft manifests, the craft and root READMEs, the router's pipeline table, PLAN §2 and CODEMAP. cinewright-design's trigger line no longer says sets.
- Worktree `cinewright-set` on branch `set-skill`, because the main clone was on another session's `voice-skill` branch with uncommitted work.

```
$ python -m unittest discover -s tests
Ran 83 tests ... OK
$ python scripts/cine.py kb lint
kb lint: 15 skills, 0 errors
$ python scripts/cine.py budget
budget: YELLOW (all descriptions 4338 characters, green up to 4000; the new skill's 342 tips it over)
$ python scripts/cine.py scrub --names <sidecar scrub-names.txt>
scrub: 0 hits in 0 files
$ claude plugin validate . (and the three plugins)
Validation passed (four times)
```
- Not yet run: the seven eval cases (evals/run_evals.py) for the new skill.
