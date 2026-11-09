# Research: cinewright-genvideo

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Topic: AI video model prompting and compiling (Veo, Kling, Seedance, Runway, Luma, Wan, LTX-2, MiniMax H3). Tier `fast`. Last refresh 2026-10-03; next due 2026-10-17.

## Current understanding

- Nine model cards, all re-checked from vendor pages on 2026-10-03 (R-20261003-2): Veo 3.1, Gemini Omni Flash, Kling 3.0, Seedance 2.5, Runway Gen-4.5, Luma Ray3.2, MiniMax H3, Wan 2.2, LTX-2.5. Sora 2 is shut down (no card).
- Each vendor has its own dialogue form: Veo `says:` with no quotes, Kling `Name (tone): line`, Seedance `{line}` in braces, H3 `(S1) says: <d>[English] line</d>`, LTX `says, "line"`. Omni has none documented. Runway, Luma and Wan make no sound at all.
- Multi-shot syntax differs too: Veo `[00:00-00:02]`, Omni `[0-3s]`, Kling `Shot 1,` with lengths in the settings, Seedance `Shot 1:`, H3 `[Shot 2] At 00:05.000, the camera cuts to`, LTX "A hard cut jumps to", Runway `[00:00 through 00:02]`.
- Local models add a frame grid and a size rule: H3 17k+5 (field notes), Wan 4n+1 at 16 fps with fixed sizes, LTX 8n+1 with multiples of 32.
- Veo 3.1 (checked 2026-10-03): Vertex GA IDs `veo-3.1-generate-001` and `-fast-` since 2025-11-17, retirement 2027-05-04 or later (moved, R-20261105-2); Gemini API preview IDs listed with earliest shutdown 2026-10-22 and `gemini-omni-1.2-flash` named as replacement. No Veo 4 on any Google page.
- Veo 3.1 numbers: 4/6/8 s, 720p/1080p/4k (1080p, 4k and refs force 8 s), 16:9 or 9:16, 24 fps, 1,024-token prompt cap, up to 3 asset refs, no style refs, seed uint32.
- Veo prompt form: cinematography, subject, action, context, style; audio in its own sentences; timestamp blocks `[00:00-00:02]` for several shots (blog only, not in the docs pages).
- Contested: dialogue syntax. The blog uses quotes, the Gemini API page speaker labels, the prompt guide a colon with no quotes. cinewright uses the prompt-guide form (newest page, updated 2026-10-01).
- Unverified: how to stop burnt-in subtitles. Google documents nothing; community advice is colon dialogue and negative-prompt nouns.

## Open questions

- Which IDs offer 4k on Vertex (GA or preview)? Google's pages disagree.
- Does `negativePrompt` still work on the Gemini API? It is missing from the current page.
- Omni dialogue syntax and seed support are undocumented; the first paid Omni take should settle the dialogue form.
- Seedance: the guide puts dialogue in braces, the API reference in quotes. Which one avoids burnt-in captions?

## Search plan

Four tracks; every refresh runs at least one query on each, scoped to the time since the last refresh.

Subject:

- `Veo 3.1 OR "Gemini Omni" video prompt guide changes <month> <year>`
- `Kling OR Seedance OR Runway video model release <month> <year>`

Tooling:

- `path:SKILL.md "video prompt"` on GitHub code search, sorted by recently updated; skills.sh weekly installs for `video prompt`
- `https://registry.modelcontextprotocol.io/v0/servers?search=video generation`
- Supersession sweep: `"video prompt" skill deprecated OR archived <year>`; archive flag on DirectorSKILL and smixs/visual-skills

Practice:

- `"prompt" Veo OR Kling consistency workflow site:reddit.com <month>`
- `site:simonwillison.net OR site:latent.space video model <year>`

Testing:

- `video generation prompt adherence benchmark <year>` (VBench-2.0, VideoScore2)
- `path:SKILL.md veo evals`

Best sources (primary first): Vendor docs and deprecation pages first (aistudio.google.com/docs/deprecations, Vertex model pages), vendor prompt guides second. Noisy: third-party Veo blogs and 'Veo 4' speculation.

## Findings log

Newest first. `Track` is subject, tooling, practice, or testing.

### R-20261109-1 · 2026-11-09 · Tooling: IV Studio as an H3 reference app
- Summary: IV Studio 1.0 (MIT, hollisorg/iv-studio): lint.js and ranking.js are worth reading; lint rules adapted into cine.py compile (h3_lint), ranking into take-selection.md. H3 Recast (Bambushu, MIT) rules into minimax-h3.md, untested.
- Track: practice, tooling
- Sources: r/StableDiffusion 1xqfux1, https://github.com/hollisorg/iv-studio, https://github.com/Bambushu/h3-recast
- Magnitude: minor
- Applied: C-20261109-3

### R-20261105-2 · 2026-11-05 · Omni 1.2 Flash replaces 1.1; Veo Vertex end moved; Google docs moved
- Summary: `gemini-omni-1.2-flash` released 2026-11-05: 3-15 s by a `duration` parameter, lower prices, control tags deprecated, extended total 30 s. `gemini-omni-1.1-flash` routes to it from 2026-12-03. Veo 3.1 Vertex GA retirement is 2027-05-04 or later; `veo-3.1-lite-generate-001` is in preview with no refs. Gemini API docs now live at aistudio.google.com/docs. Web search found no third-party coverage of 1.2 yet; the vendor pages carry it. Still undocumented: Omni dialogue syntax in the part read, and whether numbered ref wording helps.
- Track: subject. Tooling, practice, testing: not searched, this pass settled a flagged contradiction.
- Sources: https://aistudio.google.com/docs/omni, https://aistudio.google.com/docs/models/gemini-omni-flash, https://aistudio.google.com/docs/deprecations, https://aistudio.google.com/docs/pricing, https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/model-versions, https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/veo/3-1-generate
- Magnitude: 0.6
- Applied: C-20261105-3

### R-20261014-1 · 2026-10-14 · Practice: violence, fight LoRAs and the forced end frame on MiniMax H3
- Summary: See the movement skill's R-20261014-1 and ai-docs/research/2026-10-14-violence-healing-flight.md. For this skill: local H3 refuses nothing (hosted strips blood); Combat Base V2 versus Weapon Combat is unresolved; first/last-frame H3 overshoots and snaps onto its end frame.
- Track: practice
- Sources: https://huggingface.co/JOKER141/MiniMax-H3-Combat-Base-V2, https://huggingface.co/RunningHubAI/rh-v1-weapon-combat-lora, https://www.reddit.com/r/StableDiffusion/comments/1wtcitg/, https://www.reddit.com/r/StableDiffusion/comments/1wmhny6/
- Magnitude: minor
- Applied: C-20261014-1

### R-20261013-1 · 2026-10-13 · Practice: crowd prompting and subject limits
- Summary: Tiered crowds (hero, featured, groups), movement lanes, a stress ladder and per-frame scoring (seedance.tv crowd workflow, 2026-09-13); one reference per subject with a role, subject-count stability limits for Seedance (smixs visual-skills); no open model holds more than about 4 identities (Phantom); Kling 3.0 best crowd motion in one vendor test (Beeble).
- Track: practice
- Sources: https://www.seedance.tv/blog/comfyui-crowd-video-workflow, https://github.com/smixs/visual-skills, https://beeble.ai/blog/canvas-tutorial-crowd-vfx, https://github.com/HKUDS/ViMax, ai-docs/research/2026-10-13-battle-crowd-compositing.md
- Magnitude: minor
- Applied: C-20261013-1

### R-20261003-2 · 2026-10-03 · Every model re-verified from vendor docs (S2)
- Summary: four subagents read the vendor pages; full notes are in the repo's ai-docs/research/2026-10-03-s2-model-verification.md. Corrections to the S1 brief: Luma's API model is ray-3.2 (Ray3 and 3.14 have no API ID); LTX-2.5 is current; Wan 2.2 has no first/last-frame or VACE (2.1 only); Seedance 2.5 is live; Seedance tags have a space (`@Image 1`); H3's official form uses labelled fields and `with small amplitude at slow speed`, and the guide does not mention the old bracket camera syntax.
- Track: subject
- Sources: model card `sources` lists (veo-3-1, gemini-omni, kling-3, seedance-2-5, runway-gen-4-5, luma-ray-3-2, minimax-h3, wan-2-2, ltx-2)
- Magnitude: 0.6 (several brief claims wrong)
- Applied: C-20261003-2

### R-20261003-1 · 2026-10-03 · Initial research
- Summary: Veo 3.1 re-checked from Google pages for the model card: IDs and dates, durations, sizes, refs, timestamps, dialogue forms (subject). Tooling: no competitor compiles one card into several models' syntax. Practice: community subtitle workarounds, marked unverified. Testing: compile output is checked by the identity-verbatim guard and by tests.
- Track: subject
- Sources: https://ai.google.dev/gemini-api/docs/veo, https://ai.google.dev/gemini-api/docs/deprecations, https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/veo/3-1-generate, https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1
- Magnitude: n/a (initial)
- Applied: C-20261003-1
