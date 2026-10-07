# Research: cinewright-sets

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Topic: Set and location design for AI video: set plans, per-wall location strings, master plates, coverage and reverse angles, set light, plate checks. Tier `moderate`. Last refresh 2026-10-07; next due 2026-11-06.

## Current understanding

- Settled (craft): art departments hand the DP a scaled ground plan with a north arrow, elevations, key art, location photos and overheads; coverage is planned per set, with wild walls for the reverse (filmlocal; howtofilmschool; ScreenSkills AAD guide).
- Settled (AI practice, 2026): anchor every shot at a set to one establishing image and pass it as a reference in every call; generate the widest shot first; fix light with a named source, a color temperature and a key side, never reworded (Higgsfield 2026-07-27; HackerNoon 2026-07-23; invideo Seedance guide).
- Settled (field test, 2026-10-07): a whole-room description pulls every angle to its hero wall; framing words alone do not turn the camera. Per-wall strings are the fix (L-001).
- Moving fast: 3D world sources (World Labs Marble, HY-World 2.0 from 2026-04-16, HunyuanWorld-Voyager), angle-edit LoRAs (Qwen-Image-Edit-2511 Multiple-Angles, Flux 2 Multiple Angles), reference slot counts per video model.
- Unverified: angle-edit models on interiors past about 45 degrees (no measured drift numbers found); location LoRAs for sets (no primary source); Seedance 2.5's 50-reference claim (vendor).

## Open questions

- Do the per-wall plates hold when passed as references to a video model with characters added (H3, Veo)?
- Does a 3D blockout plus depth beat wall strings enough on a local image model to make it the default?
- Should `sets/<id>.md` become a schema the CLI can check (doors and windows per wall)?

## Search plan

Four tracks; every refresh runs at least one query on each, scoped to the time since the last refresh.

Subject:

- `production design ground plan coverage wild walls <year>`
- `location scout package sun path film <year>`

Tooling:

- `path:SKILL.md "location bible"` and `path:SKILL.md "set design"` on GitHub code search; skills.sh installs for `storyboard`, `location`
- `https://registry.modelcontextprotocol.io/v0/servers?search=3d%20world`
- `ComfyUI multi angle camera node <month> <year>`; World Labs Marble changelog; HY-World releases

Practice:

- `consistent location AI video reverse angle <month> <year>`
- `reference to video environment reference image <model> <year>`

Testing:

- `scene consistency benchmark video generation background <year>` (WorldScore and successors)
- `path:SKILL.md storyboard evals`

Best sources (primary first): vendor docs and model cards (Google, Runway, Kling, MiniMax, ByteDance, World Labs, Tencent), Hugging Face cards, ComfyUI blog; LoBrutto for craft. Noisy: prompt packs and aggregator blogs restating vendor claims.

## Findings log

Newest first. `Track` is subject, tooling, practice, or testing.

### R-20261007-2 · 2026-10-07 · Field test: a real public building as eleven sets
- Track: practice · magnitude 0.6
- Eleven locations, 34 planned stills on a local image model, 16:9, one seed per set. The two off-wall shots rendered first (a reverse to the fireplace wall, an east-door shot) both came back as the establishing desk-and-windows view: the description named the desk and windows. Rewritten as per-wall strings for the re-render. Led to the `walls` field, `camera.faces` and entry wall-strings.

### R-20261007-1 · 2026-10-07 · Initial research
- Track: subject, tooling, practice, testing · magnitude n/a (creation)
- Subject: ground plans at 1/4 inch to 1 foot with a north arrow; overheads; wild and flyaway walls; virtual art departments and digital twins (filmlocal; howtofilmschool; ASC on The Book of Boba Fett; No Film School volume glossary).
- Tooling: no dedicated set or location bible skill found. Closest: DirectorSKILL (continuity bible with a location schema, MIT, about 179 stars), Storyboarder.ai location editor (a locked reference image and 4 angles per location), ComfyUI-qwenmultiangle (about 1.2k stars), ComfyUI_HYWorld2 (pano to views), pytorch360convert, preview360panorama.
- Practice: master plate first, location plate in every call, last frame carried forward; reference slots Veo 3.1 3, Runway Gen-4 1-3, Kling 3.0 4, MiniMax H3 1-5, Seedance 2.0 9 images; blockout as depth saved 7-8 tries per angle in one account; signage garbles, add text in post.
- Testing: WorldScore ranks 3D and photometric consistency (HunyuanWorld-Voyager first, 2025); no checker for set plates found, so the skill's check is a checklist plus the WALL diff.
- Sources: https://filmlocal.com/?p=1450172, https://higgsfield.ai/blog/consistent-characters-locations, https://hackernoon.com/every-ai-generated-shot-invents-its-own-light-heres-how-to-keep-lighting-consistent, https://huggingface.co/fal/Qwen-Image-Edit-2511-Multiple-Angles-LoRA, https://docs.worldlabs.ai/marble/export/gaussian-splat/index.md, https://github.com/Tencent-Hunyuan/HY-World-2.0, https://github.com/wuwangzhang1216/DirectorSKILL, https://help.storyboarder.ai/en/articles/14067900-how-to-create-consistent-locations-with-the-location-editor, https://arxiv.org/pdf/2506.04225
