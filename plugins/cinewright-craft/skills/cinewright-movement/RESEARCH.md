# Research: cinewright-movement

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Topic: Movement for AI video: weight and contact, one phrase per shot, fights and stunts, and hard subjects (animals, crowds, hands, liquids). Tier `slow`. Last refresh 2026-10-04; next due 2027-02-01.

## Current understanding

- Settled (craft): anticipation, contact, follow-through and settle (Thomas and Johnston 1981; Williams 2001); effort qualities (Laban 1980); one exchange per shot in fights (Katz 1991).
- Settled (AI-specific, field lessons 020 and 021): hard subjects render when few, large and side-on; a far column of animals cannot be drawn; an animal-drawn vehicle from behind gets its order wrong.
- Moving: physics and anatomy keep improving model by model; re-check the hard-subject list at each refresh.
- Unverified: the local resolution figure (1056-1344 px for animals) comes from one local model.

## Open questions

- Which hard subjects have hosted 2026 models fixed? (S8 renders, one per subject)
- Should the HARD-SUBJECT check also look at MWS cards with many named figures?

## Search plan

Four tracks; every refresh runs at least one query on each, scoped to the time since the last refresh.

Subject:

- `animation principles weight follow-through reference <year>`
- `fight choreography for camera film <year>`

Tooling:

- `path:SKILL.md "choreography"` on GitHub code search; skills.sh weekly installs for `motion`
- `https://registry.modelcontextprotocol.io/v0/servers?search=motion`

Practice:

- `AI video horse legs crowd hands fix <month> <year>`
- `site:reddit.com/r/aivideo fight scene consistent`

Testing:

- `video generation physics anatomy benchmark <year>` (VBench-2.0 and successors)
- `path:SKILL.md movement evals`

Best sources (primary first): Thomas and Johnston, The Illusion of Life; Williams, The Animator's Survival Kit; Laban, The Mastery of Movement; Katz, Film Directing Shot by Shot. Noisy: one-off viral clips without settings.

## Findings log

Newest first. `Track` is subject, tooling, practice, or testing.

### R-20261015-1 · 2026-10-15 · Subject: fight choreography documents, AI fight practice, 3D previs
- Summary: Fight directors write fights operator first, in a numbered list or a table with a column per fighter and an arrow (FDC); the arc is a story decision per phrase, planned from the end, never a graph; music timing lives in animatics and bar sheets. AI makers plan fights in images (storyboard grids on hosted models); on local H3 hits land only when each hit has its own timecode, distant fighters smear, speed LoRAs change the moves, faces swap between fighters. SCAIL-style 3D skeletons and Blender rigs are the open route from staged motion to video; weapons vanish from skeleton controls. Nothing 3D tested on fights yet.
- Track: subject, practice, tooling
- Sources: ai-docs/research/2026-10-15-fight-planning.md (full list), https://web.archive.org/web/20150311201049/http://www.academieduello.com:80/news-blog/recording-choreography/, https://www.reddit.com/r/StableDiffusion/comments/1vsjezd/, https://github.com/zai-org/SCAIL
- Magnitude: moderate
- Applied: C-20261015-2

### R-20261014-1 · 2026-10-14 · Subject: violence, wounds, healing and flight on local video models
- Summary: Local open weights refuse nothing; contact (stab, impalement) lands with a pinned still of the moment; fight LoRA advice conflicts between a forum test (spear, trident) and the field record (swords, axes); no source shows a wound healing; flying heroes come from storyboard references and first/end frames, and similes about wires draw wires.
- Track: subject
- Sources: ai-docs/research/2026-10-14-violence-healing-flight.md (full list), https://www.reddit.com/r/StableDiffusion/comments/1wtcitg/, https://www.reddit.com/r/StableDiffusion/comments/1x050ne/
- Magnitude: minor
- Applied: C-20261014-1

### R-20261013-1 · 2026-10-13 · Subject: crowds staged in 3D drive the video model
- Summary: A 3D crowd blockout rendered to depth (plus pose for the front ranks) drives Wan VACE or Fun Control; practitioners build battles from layers and cuts (House of David season 2: under 200 extras plus AI crowds on Unreal bases). Coarse proxies work better than detailed ones as reference video.
- Track: subject
- Sources: https://www.vp-land.com/stories/house-of-david-season-2-used-253-ai-generated-shots-here-s-how-they-did-it, https://docs.comfy.org/built-in-nodes/conditioning/video-models/wan-vace-to-video, https://github.com/smixs/visual-skills, ai-docs/research/2026-10-13-battle-crowd-compositing.md
- Magnitude: minor
- Applied: C-20261013-1

### R-20261004-1 · 2026-10-04 · Initial research
- Summary: Built from the research brief §3 movement row and §7 coherence causes (subject), field lessons 020 and 021 (practice), the competitor study (tooling: no competitor checks crowd framing), and TESTING.md (testing: the diff's HARD-SUBJECT and ONE-ACTION warnings are checkable).
- Track: subject
- Sources: https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation, https://en.wikipedia.org/wiki/Laban_movement_analysis
- Magnitude: n/a (initial)
- Applied: C-20261004-1
