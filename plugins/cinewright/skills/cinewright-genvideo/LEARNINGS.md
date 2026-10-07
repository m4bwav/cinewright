# Learnings: cinewright-genvideo

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format: [MAINTENANCE.md](MAINTENANCE.md) (LEARNINGS-FORMAT in the evergreen protocol). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a workaround, an environment fact, a failed test. Check existing entries first: add, update, retire or none. Trigger and Hypothesis are required.

## Active

### L-001 · 2026-10-03 · Keep the verbatim identity guard in the compiler
- Trigger: 2026-10-03, first run of `compile --sequence` on the example: the header described only the first card's cast, and the guard stopped with 'identity of tomas not verbatim in 1C'
- Hypothesis: Multi-card output paths are easy to get wrong silently; the guard turns a silent drift into a stop
- Rule: Never weaken the guard; any new output mode must pass it on the example before it ships
- Evidence: C-20261003-1 (shared/lib/cine.py compile_cards, tests/test_cine.py), confirmed 2026-10-03
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-03

### L-002 · 2026-10-03 · Never present a cinewright default as a vendor number
- Trigger: 2026-10-03: the first Veo card carried a 150-word guide; the re-check found Google gives only a 1,024-token cap
- Hypothesis: A plausible number written next to vendor facts reads as a vendor fact
- Rule: Label every cinewright default in a model card as 'its own default, unverified'
- Evidence: C-20261003-1 (references/veo-3-1.md Numbers), confirmed 2026-10-03
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-03

### L-003 · 2026-10-03 · Take a model's syntax from the vendor's guide, not from notes or briefs
- Trigger: 2026-10-03 re-verification: three syntax claims in the research brief and local field notes differed from vendor guides (Seedance `@Image1` vs `@Image 1`; H3 bracket moves vs amplitude sentences; H3 Timeline beats vs labelled fields)
- Hypothesis: Second-hand prompt syntax drifts as vendors revise guides; local notes record what worked once, not the documented form
- Rule: Write a card's Compile block from the vendor's own example and test it with a regex that must match that example too
- Evidence: C-20261003-2 (tests/test_cine.py TestModelCards), confirmed 2026-10-03
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-03

### L-004 · 2026-10-03 · Shots in one generation must restate where each person stands
- Trigger: 2026-10-03, first local H3 compile of the three-shot example with `--sequence`: card 1A's frame positions and props in hand were missing, because people are described once in the shared header
- Hypothesis: The header carries who people are; where they stand changes per shot and has to travel with the shot
- Rule: Every sequence block includes the staging part (position and prop in hand); a new layout must keep it
- Evidence: C-20261003-2 (shared/lib/cine.py card_parts staging), confirmed 2026-10-03
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-03

### L-005 · 2026-10-03 · An eyeline needs a target, not only a frame direction
- Trigger: 2026-10-03, first local H3 render of the three-shot example (one 14 s generation, seed 101): card 1B said 'Maren is looking toward frame right' and she looked almost into the lens; take 2, same seed, with 'looking toward frame right, at Tomas' fixed it
- Hypothesis: A bare direction is weak conditioning next to a close-up's pull toward the lens; a named person or object gives the gaze somewhere to land
- Rule: The compiler writes every eyeline as direction plus the card's looks_at (a character by name, an object as written); cards should always fill looks_at
- Evidence: C-20261003-2 (shared/lib/cine.py card_parts, failures-picture eyeline-wrong row), confirmed 2026-10-03 by a same-seed re-render
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-03

### L-009 · 2026-10-07 · A simile in the source becomes a literal object; rewrite it as what is seen
- Trigger: library film test 2026-10-06: the novel's sorcerers hang in the sky "as though from wires"; pasted into the prompt, the image model drew wires from their backs
- Hypothesis: Models render every concrete noun in the prompt; "as though" does not mark it as a comparison
- Rule: Before a source line goes into a card, rewrite similes and metaphors as the visible fact ("floating free, held up by nothing"), and never keep the compared object's noun
- Evidence: s8 ruin still (rejected) vs the rewritten still and v2-v5 renders, no wires; ai-docs/notes/2026-10-07-library-film-test.md
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-07

### L-010 · 2026-10-07 · A count in an identity string is drawn literally
- Trigger: library film test: "a beard streaked with five distinct white strands" rendered as five rigid white prongs in every text-only take
- Hypothesis: A number plus a noun reads as countable separate objects, so the model makes them distinct and stiff
- Rule: Describe texture, not counts, in identity strings ("shot through with thin streaks of white"), and let a face reference carry the detail
- Evidence: v1 sections 2, 3, 5 (prongs) vs v2-v5 with the new wording and the face reference (none)
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-07

### L-011 · 2026-10-07 · A location reference still carries its composition and its mistakes into the shot
- Trigger: library film test: an H3 reference of a ruin with a coiled fire-dragon and two brown-robed figures put coiled necks and brown robes into both renders that used it; a dream still with a half-dome Ward kept the half-dome
- Hypothesis: Reference-to-video copies objects and layout from every picture, not only the identity it was meant for
- Rule: Pass identity references (faces, costume sheets) freely; pass a location or moment still only when everything in it is right, otherwise describe the place in text
- Evidence: v2 and v3 section 8 (drift) vs v4 section 8 without the still (none); v2/v3 dream vs v4 dream
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-07

### L-012 · 2026-10-07 · A line from a speaker who is not in the shot comes out of a face that is
- Trigger: library film test, owner's review on 2026-10-07: card 6D had only the hero in shot and a rival sorcerer's shout from the dark as dialogue; the compiled H3 prompt wrote it as a plain "says" line and the hero said it. The owner has seen the same swap in other generated videos
- Hypothesis: Joint audio-video models lip-sync speech to a visible mouth; a name in the prompt does not tell them the speaker is absent. The H3 guide has an exact phrase for this ("says in an off-screen voiceover", then the on-screen lips stay closed) that the compiler did not use
- Rule: Keep every speaker in the card's cast. When the line must stay off screen, compile with the model's voiceover template (H3 `dialogue_offscreen`) and the silent clause for everyone in shot; on a model with none, leave the line out of the prompt and lay it in the mix. `continuity diff` OFFSCREEN and `compile` warn
- Evidence: library_120s_best_c section 6 (wrong mouth); compile of 6D after the fix writes the voiceover form; tests TestSpeakers (7). No re-render yet: the fix is unverified on H3 output
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-07
