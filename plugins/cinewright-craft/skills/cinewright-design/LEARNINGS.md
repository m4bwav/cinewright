# Learnings: cinewright-design

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format: [MAINTENANCE.md](MAINTENANCE.md) (LEARNINGS-FORMAT in the evergreen protocol). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a workaround, an environment fact, a failed test. Check existing entries first: add, update, retire or none. Trigger and Hypothesis are required.

## Active

### L-001 · 2026-10-04 · Make each character one turnaround sheet; crop the views into separate references
- Trigger: Field lesson 017 of the maintainer's local renders, 2026-09-29, 'Turnaround sheets hold one identity across views; costume sheets invent symbols'
- Hypothesis: An image model keeps identity inside one image far better than across separate generations, and a whole sheet passed as one reference leaves each view few pixels
- Rule: Generate one three-view sheet per character and costume on flat light and grey, crop each view, and check every sheet for symbols the text did not ask for
- Evidence: C-20261004-1 (references/turnaround-sheets.md), confirmed 2026-10-04
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-04

### L-002 · 2026-10-04 · Clean every reference before use; it outranks the prompt
- Trigger: Field lesson 019 of the maintainer's local renders, 2026-09-29, 'A video model copies a reference picture's small emblems onto the character, so clean every reference first'
- Hypothesis: A reference image conditions what it shows more strongly than any text, including exclusion lines
- Rule: Paint out every unwanted mark before the reference goes into a shot, keep the original as `_orig`, and inspect at full size
- Evidence: C-20261004-1 (references/clean-references.md), confirmed 2026-10-04
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-04

### L-003 · 2026-10-04 · A prop named by one word changes look between shots; give it a fixed description
- Trigger: 2026-10-03, first local render of the three-shot example: the qc rubric failed 1A on prop-drift (a cardboard box where the story meant a tin matchbox)
- Hypothesis: The model invents a prop's look from its name each generation, as it does identity
- Rule: Describe every held or close-up prop once in bibles/props.json; the compiler pastes it verbatim and the diff warns when one is missing
- Evidence: C-20261004-1 (references/prop-constants.md, shared/lib/cine.py prop_words), confirmed 2026-10-04
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-04

### L-004 · 2026-10-06 · Name what an invented effect is made of, and what it lacks; a familiar word draws the familiar thing
- Trigger: 2026-10-06 library test (an adapted fantasy novel): the bible said 'ghostly dragon heads of fire' for a spell, and both guide stills drew winged, lizard-bodied dragons; the owner checked the source: the spell is a bodiless head and neck of fire and light
- Hypothesis: Image and video models resolve a noun like 'dragon' to its most common picture; adjectives such as 'ghostly' do not remove the body
- Rule: For every invented effect, write in design.md and the bibles its substance (fire, light, glass), its parts and the parts it does NOT have ('no body, no wings, no legs'), and how it ends; check the source or its lore before the references are made; keep a real creature of the same name visibly different
- Evidence: v1 guide stills s7_magi (rejected), regenerated with the substance wording on 2026-10-06
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-06

### L-005 · 2026-10-15 · A character's `refs` cannot follow a costume stage or a wound; every sheet goes to every card
- Trigger: a rapier duel from a novel: the antagonist has two wardrobe stages (cloak and hood up, then cloak off), each with its own turnaround as costume-arc asks; character `refs` is one flat list, and the compiler (`generation_refs`) sends all of it with every card the character is in, so both stages would reach every shot. The owner then asked whether wounds need a reference per stage too.
- Hypothesis: the bible keys wardrobe by scene but not refs, so the rule "one sheet per costume" cannot be honoured by the compiler; wound stages hit the same wall. Research (2026-10-15): no measured test of per-stage references against text exists for any model, but practitioner guides (Techloy, InVideo, Elser AI, Aug 2026), film costume and make-up practice (stage-labelled doubles and continuity photos per stage) and reference-to-video papers (OpenS2V-Nexus 2025, Aura 2026: a strong reference suppresses the prompt) agree that a clean sheet heals a wound the text describes; the maintainer's own renders saw blood come and go between text-only shots.
- Rule: until refs can be keyed like wardrobe, keep only the current stage's crops in the character's `refs` and swap them in the same change that starts the next stage's scene; never list two stages at once. Make each later stage (and each wound stage) by editing the kept picture of the earlier one, the wound by a local edit on the wound area only (cinewright-movement entry wounds-and-healing, rule 1), so the face stays; describe the wound once, on the character's own left or right, matching the picture. Conflict to settle: wounds-and-healing's last rule keeps temporary marks in card text with the clean sheet for identity, which comfyui-gen L-056 (`state-needs-its-own-ref`: the words lose to a clean face ref) and the research above contradict for a wound that lasts across cards; a one-card mark can stay text. Proposed change: `refs` keyed like `wardrobe` (`{"default": [...], "1b": [...]}`), resolved per card by scene.
- Evidence: the duel project's bibles/characters.json (stage 1 crops listed, 1b crops kept on disk), refs/sheets/edit_src.py; research summary in that project's README, "Wound stages".
- Scope: skill (costume-arc, turnaround-sheets) and shared compiler
- Confirmed (2026-10-15, later): the first card after the cloak came off (scene 1b) swapped the antagonist's `refs` as the rule says, and every earlier card's compile then carried the cloak-off sheets too. Workaround: compile into a second folder just before the swap and render the earlier cards from it. It does not scale to wounds: the hero has four wound stages and none is a scene change, so scene-keyed `refs` would not reach them either; the change needs a stage a card's cast member can name (`refs: {"default": [...], "L1": [...]}` with `"refs_stage": "L1"` on the cast entry, falling back to the scene id). The first wound stage was made as a local edit of the kept view (comfyui-gen L-124 `wound-by-changed-pixels`).
- Resolved (2026-10-16): `refs` takes the keyed form (`{"default": [...], "1b": [...], "L1": [...]}`), resolved per card by the cast entry's `refs_stage`, then the scene id, then `default`; `continuity diff` errors on an unknown stage and warns when a stage goes back. A scratch copy of the duel with staged refs and no swaps compiled to exactly the files the three swap snapshots hold (48 of 48), so the snapshots can go once this ships. Rule from now on: key `refs` by stage, never swap. The wounds-and-healing conflict is settled for lasting wounds (their own stage); one-card marks stay text.
- Confirmed (2026-10-16, after the merge): the duel project dropped its two swap snapshots; the real recompile matched them file for file (48 of 48). Its second wound stage then needed only a new `refs` key and `refs_stage` on the cards from the first wounded card, with no snapshot and no change to earlier cards' compiles.
- Status: active · helpful 4 · harmful 0 · last_confirmed 2026-10-16

### L-006 · 2026-10-15 · Image models draw a rapier as a dagger; start a period weapon's sheet from a public-domain museum photo
- Trigger: prop sheets for the same duel: Z-Image (four prompts, two seeds each, length given in words and as a ratio) and a FLUX.2 Klein lengthening edit all drew short daggers with ring guards; a coin kept a portrait and letters until a Klein edit wore its faces blank.
- Hypothesis: rare object shapes lose to the model's common one; length in words does not move it.
- Rule: for a historical weapon or object the models do not know, take an open-access museum photograph (The Met, CC0), keep its real hilt or detail, and build the full view from it in code at the catalogued size; send one ref per prop when two people and several props share a card (the duel's busiest card uses exactly 9 slots). comfyui-gen L-121 has the steps and the script.
- Evidence: comfyui-gen LEARNINGS L-121 (merged 2026-10-15).
- Scope: skill (prop-sheets)
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-15

### L-007 · 2026-10-16 · A fighter out of frame takes his new wound stage at his first card in frame; a back wound no sheet shows stays text; a sheathed weapon the story took away is a second weapon in the refs
- Trigger: the duel's later stages: the antagonist's bitten fingers (exchange 15) happen in a close-up that shows only his hand, his back wound (19) faces away from every camera that sees his face, and the hero's three-quarter sheet still shows his rapier in its scabbard though he holds it from the first exchange and loses it in the thirteenth.
- Hypothesis: the cut-on-contact rule (a card that shows the wound happen keeps the old sheet) assumes the wounded fighter is in that card; a front three-quarter sheet cannot carry a back; whatever a sheet shows, the model may copy into the hand.
- Rule: when the wounding card does not show the fighter (only his hand, or he is off frame), start his new stage at the first card that shows him after it. Keep a wound on his back as text while every shot that sees him sees his front. Make each stage sheet match the story at that point: an empty scabbard once the sword is in hand or on the floor (one local edit, "only the open top of the empty scabbard hanging from the belt", worked 1 of 4 and 1 of 4 again). An object run through a limb is composited in code from the prop's own sheet (an edit model will not add it), with the edit model used only for the blood, and the object pasted back over the edit (field lesson 127, an object through a figure by composite).
- Evidence: the duel project's refs (`locke-L3-3q`, `locke-L4-3q`, `gray-king-1b-bitten-3q`, `gray-king-1b-ribs-3q`) and cards 1AH-1AZ; continuity diff 0 errors, 0 warnings.
- Scope: skill (costume-arc, wound stages); builds on L-005
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-16
