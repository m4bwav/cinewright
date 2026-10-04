# cinewright research brief (2026-10-03)

Read this when planning or building cinewright. Gathered 2026-10-03 by four research passes (local prior art, film craft, AI video, packaging). Numbers marked (verify) came from secondary sources; check the primary page before encoding them in the kb.

Contents: 1 Request · 2 Local prior art · 3 Film roles and checkable rules · 4 Sources · 5 History and style cards · 6 AI video models · 7 Coherence: causes and fixes · 8 Evaluation · 9 Existing skills to learn from · 10 Packaging for three hosts · 11 Token rules

## 1. Request

Mark's words: `D:/m4bwa/Claude/Projects/Ai/prompts/Cinematography Plugin Prompt.md`. In short: an evergreen plugin set with a knowledge base and skills for every film role (writer, choreographer, set designer, film historian, camera, sound, VFX, ...) plus AI video generation and editing. Used mostly with generated video. The problem to solve is generated clips that are random and incoherent; the goal is video that is both artistically and technically correct. Public repo, installable on Claude Desktop, Claude Code and GitHub Copilot. Ultimate, but never wasteful with tokens: small docs with pointers.

## 2. Local prior art (read before designing; do not copy private details into the public repo)

- `D:/m4bwa/Claude/Projects/Ai/comfyui-gen/skills/comfyui-gen/LEARNINGS.md`: MiniMax H3 lessons. The ones that generalise:
  - L-005: chained clips lose identity and prop continuity; the splice reads as a pause.
  - L-010: reference images keep characters on-model (name them in the prompt).
  - L-011: independent shots cut together read as the scene restarting; write cuts inside one long render, seams only at real changes of place, carry sound across cuts.
  - L-012: crowds face random ways; give a fixed screen direction string ("from the LEFT of the frame to the RIGHT") in every prompt (180-degree rule as a constant).
  - L-013: describe what IS in the shot; "avoid" lists lose against strong associations; add a CONTRAST sentence when two groups' looks bleed.
  - L-014: same seed keeps the opening whatever the text says; log each seed with a verdict.
  - L-015: a guide frame pinned at frame 0 fixes an opening that seeds and text cannot.
  - L-017: turnaround sheets hold identity across views; crop views into separate references.
  - L-019: the model copies small emblems from references; clean references first.
  - L-020/021: hard subjects (horse teams, wagons): side view, few, large in frame.
- `comfyui-gen/skills/comfyui-gen/h3_film.py` + `h3_tools.py`: a multi-shot `film.json` (shots, seeds, refs, guide frames, audio crossfades) and review helpers (contact sheet, frame grab, rewrite named shots, new pass with new seeds). cinewright's shot-list format should export to this.
- `comfyui-gen/ai-docs/notes/2026-09-29-*` (battle film research, visual bible, reference sets) and `ai-docs/plans/2026-09-29-*-prompt.md` (day-iteration prompts); review logs `D:/ComfyUI/output/video/NIGHT_2026-09-28.md`, `DAY_2026-09-29.md`.
- `D:/m4bwa/Claude/Projects/Ai/video-pipeline/README.md`: idea → local LLM writes structured shot prompts (style line, scene, timeline with sound, avoid list) → ComfyUI. Sections "Multi-shot films", "Keeping a character consistent", "Who is in which shot".
- `austin-shootout-video/` and `campfire-video/`: deterministic three.js films (threewright). One cue timeline drives picture and sound; 2.39:1; mixed to -16.7 LUFS.
- Template repo: `D:/m4bwa/Claude/Projects/Ai/threewright/` (`.claude-plugin/plugin.json` + `marketplace.json`, `AGENTS.md`, `CLAUDE.md` = `@AGENTS.md`, `.github/copilot-instructions.md` one line, `skills/<name>/{SKILL.md 42-59 lines, RESEARCH.md, CHANGELOG.md, LEARNINGS.md, TESTS.md, evergreen.json, evals/}`, `kb/{SCHEMA.md, INDEX.md + index.json generated, topics/ scenarios/ recipes/ rules/}`, `scripts/tw.mjs`, `evals/headless/`). Its SKILL.md: "read kb/INDEX.md once per session, then kb search / kb show <slug> --section; never read the whole kb/". chartwright (`Ai/chartwright`, `scripts/cw.py`) does the same.
- Evergreen spec: `D:/m4bwa/Claude/Projects/Ai/evergreen-protocol/protocol/PROTOCOL.md` (§2 unit anatomy, §10 indexes), `INTERVALS.md` (tiers: live, fast 3-21d, moderate 14-90d, slow 60-365d, glacial 270-900d), `PORTABILITY.md` (harness matrix), `TESTING.md`, `LEARNINGS-FORMAT.md`, `templates/`. Budgets: main file ideally < 200 lines (cap 500); RESEARCH current understanding < 60 lines; TESTS < 150; index ≈ 200 lines / 3k tokens, one line per entry `[title](path): when to read it`.

## 3. Film roles and checkable rules

Roles grouped into domains (★ = matters most when the camera is a generative model):

| Domain | Roles | Checkable core |
|---|---|---|
| Story and script ★ | writer, script editor | three acts ~25/50/25; Save the Cat 15 beats; slugline INT./EXT. PLACE – DAY; 1 page ≈ 1 min; every scene turns a value (McKee) |
| Direction and blocking ★ | director, AD, actor direction | coverage (master, mediums, OTS, CU); blocking diagram per scene |
| Shot design ★ | storyboard, previs, shot list | sizes EWS→ECU + insert; angles; moves (pan, tilt, dolly, truck, pedestal, crane, handheld, zoom, dolly zoom, whip, orbit); thirds, headroom, lead room, depth layers; Block: contrast and affinity |
| Cinematography ★ | DP, operator, focus | lens: 14-24 wide/distort, 35 natural, 50 normal, 85-135 portrait/compression; DoF; 24/25/30/60/120 fps; 180° shutter = 1/(2×fps); aspect 1.33/1.37/1.66/1.85/2.39/1.78/1.43/9:16; anamorphic (oval bokeh, horizontal flares) |
| Lighting ★ | gaffer, key grip | key/fill/back; key:fill 2:1 soft … 8:1 noir; hard vs soft (size and distance); Rembrandt/butterfly/split/loop; 3200 K / 5600 K / candle ~1900 K; motivated sources; golden/blue hour |
| Production design ★ | designer, art director, set, props, locations | color script per act/character; period accuracy; silhouette readability |
| Costume, hair, makeup ★ | costume, MUA | costume arc; progressive damage/dirt continuity |
| Movement | choreographer, stunts, fights | weight, momentum, contact, follow-through; one phrase per shot; reaction sells the hit |
| Continuity ★★ | script supervisor | 180° axis, 30° rule (+ one size step), eyeline match, screen direction, match on action; per-shot checklist: wardrobe, props, hand used, hair, wounds, weather, time of day, sun direction |
| Editing ★ | editor | Murch Rule of Six (emotion 51, story 23, rhythm 10, eye trace 7, 2D plane 5, 3D space 4); J/L cuts, match cut, smash cut, cross-cut, cutaway; cut on action; average shot length |
| Color and finishing ★ | colorist, DIT | scene- vs display-referred; ACES (ACEScct) or log→Rec.709; Rec.709 γ2.4 100 nits; sRGB web; DCI-P3 48 nits; HDR PQ 1000 nits / HLG; order: correct, balance, match, look; skin line; ASC CDL |
| VFX | supervisor, compositor, paint | match light direction, color temp, blacks, grain, motion blur, lens distortion, DoF, camera height; edges and spill |
| Sound and music | designer, foley, dialogue, mixer, composer, music supervisor | layers: dialogue, foley, hard FX, ambience, room tone, music; stems D/M/E; Chion (diegetic, synchresis, acousmêtre); loudness BS.1770: ATSC A/85 −24 LKFS ±2; EBU R128 −23 LUFS ±0.5, TP −1 dBTP; Netflix −27 LKFS dialogue-gated, TP −2 (verify); web ≈ −14 LUFS |
| History and genre | film historian | movement, era, genre and director cards (see §5) |
| Producing and delivery (light) | producer, casting, titles | casting becomes character design; delivery specs; likeness and music rights matter for AI |

Most valuable role for AI video: the script supervisor, because each clip is generated alone and nothing else carries identity, wardrobe, props, eyelines, screen direction and time of day across them.

## 4. Sources

Books (cite, never copy): ASC Manual 11th ed. (2022); Blain Brown, Cinematography: Theory and Practice and Motion Picture and Video Lighting; Mascelli, The Five C's; Katz, Shot by Shot; Block, The Visual Story; Mercado, The Filmmaker's Eye; Weston, Directing Actors; Hart, The Art of the Storyboard; McKee, Story; Field, Screenplay; Snyder, Save the Cat; Truby, Anatomy of Story; Riley, The Hollywood Standard; Rowlands, The Continuity Supervisor; Miller, Script Supervising and Film Continuity; LoBrutto, Filmmaker's Guide to Production Design; Landis, Costume Design; Murch, In the Blink of an Eye; Dancyger, Technique of Film and Video Editing; Van Hurkman, Color Correction Handbook; VES Handbook of Visual Effects; Brinkmann, Art and Science of Digital Compositing; Chion, Audio-Vision; Sonnenschein, Sound Design; Holman, Sound for Film and Television; Karlin and Wright, On the Track; Bordwell and Thompson, Film Art and Film History; Cousins, The Story of Film.

Web: ASC (https://theasc.com/american-cinematographer); ACES (https://docs.acescentral.com/background/about-aces-2/); EBU R128 v4 (https://tech.ebu.ch/docs/r/r128v4_0.pdf); Netflix Partner Help (https://partnerhelp.netflixstudios.com/hc/en-us; loudness https://backlothelp.netflix.com/hc/en-us/articles/360050414014; sound mix https://backlothelp.netflix.com/hc/en-us/articles/360001794307; cameras https://backlothelp.netflix.com/hc/en-us/articles/360000579527); StudioBinder (https://www.studiobinder.com/blog/ultimate-guide-to-camera-shots/); No Film School; Art of the Title; FilmGrab (https://film-grab.com, frame references); Bordwell's blog (https://www.davidbordwell.net/blog); Veo prompt guide (https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/video-gen-prompt-guide).

## 5. History and style cards

Compact form: one card per item (~60 tokens, tags not prose) covering look, lens, light, cut, sound, plus one reference film and timestamp. Shared vocabulary from §3 so cards combine ("noir + 2.39 + anamorphic"). Loaded only when a request names a style.
- Movements: silent and Soviet montage; German Expressionism; Classical Hollywood; noir; Italian Neorealism; French New Wave; New Hollywood; Dogme 95; Hong Kong action; J-horror; slow cinema; modern streaming look.
- Eras by format: 1.33 B&W nitrate grain; three-strip Technicolor 1935-55; CinemaScope 2.55→2.35; 1970s zooms and 5247 grain; 1980s diffusion and smoke; 1990s bleach bypass; DI teal-orange from 2000; large format with vintage glass from 2015.
- About 40 directors, one line of signature devices each (Kubrick, Anderson, Fincher, Spielberg, Wong Kar-wai, Kurosawa, Tarkovsky, Ozu, Hitchcock, Leone, Malick, Villeneuve; Deakins as DP).
- Genres: western, horror, thriller, rom-com, musical, sci-fi, war, documentary, music video, commercial.

## 6. AI video models (fast-changing: every card needs last_checked; most numbers verify)

Hosted:
- Veo 3.1 (Google): 4/6/8 s, 720p/1080p, 16:9 or 9:16, native audio and dialogue; reference images (Ingredients), first/last frame, Extend. Formula: cinematography + subject + action + context + style; dialogue in quotes; exclusions as positive description; timestamp blocks `[00:00-00:02]` for several shots. https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1
- Kling 3.0 (Feb 2026, Turbo, Omni): 3-15 s, native audio; Multi-Shot (~6 shots per generation); Elements (2-4 refs, can carry voice); start/end frames; dialogue tagged `Name (tone): "..."`. https://kling.ai/quickstart/klingai-video-3-model-user-guide
- Seedance 2.0 (Feb 2026; 2.5 from 2026-07-31): up to 15 s multi-shot with audio; up to 9 images, 3 videos, 3 audio addressed by `@Image1` tags; 2.5 reportedly 30 s and 50 refs (verify).
- Runway Gen-4.5 (Dec 2025) and Aleph (edit existing video: add/remove, new angle, relight). https://help.runwayml.com/hc/en-us/sections/47313458960403-Prompting-Guides-Examples
- Luma Ray3/Ray3.14: 1080p, loops, EXR, Modify (v2v); ~100 words, present tense, mid-action verbs, a secondary consequence.
- Sora 2: shut down (API closed 2026-09-24). Keep only its lesson: describe motion in beats or counts.
- Pika, Higgsfield: wrappers; low priority.
Local (ComfyUI):
- MiniMax H3 (open weights 2026-08-03): joint audio/video; camera moves written in the sentence as type + amplitude + speed; old `[Pan left]` brackets deprecated.
- Wan 2.2 (Apache; first/last frame; VACE: reference, pose, depth, inpaint/outpaint). Width and height divisible by 16, frames 4n+1. Wan 2.5/2.6 hosted, audio-driven.
- LTX-2 (2.3/2.5): open weights, joint audio/video ~20 s, depth input, camera LoRAs. https://huggingface.co/Lightricks/LTX-2
- HunyuanVideo 1.5: lowest VRAM floor.

## 7. Coherence: causes and fixes

Causes: text-to-video asked to invent everything; several actions or camera moves per clip; subject and camera moving against each other; clips past ~5-8 s and chained extends; no identity anchor; empty adjectives ("cinematic, epic"); off-spec size/fps; physics-heavy actions (hands, liquids, crowds, spins); no continuity record between shots.

Pipeline that works: logline → beats → shot list (one subject, one action, one camera move, 3-8 s) → style bible and character bible (identity strings and look locks pasted verbatim into every prompt) → reference sheets and turnarounds (image model; LoRA locally) → keyframe per shot (refs + fixed seed) → image-to-video per shot (first+last frame when the end state matters) → best of N takes → edit → grade all shots together → upscale and interpolate last.

Prompt order: shot size and angle, lens, camera move (+ amplitude, speed), subject identity string, one action in beats with start and end state, setting, light (source, direction, color temperature), style/grade, audio (quoted dialogue, SFX, ambience).

Controls: lock the seed while editing text, vary it for takes; negative prompts locally only, positive exclusions for hosted; last frame → next first frame only for continuous action; trim the first and last 0.5 s; hide bad frames with inserts and cutaways; audio first (lock VO or music, cut to the beat); native lip sync (Veo, Kling, Seedance, H3, LTX-2) or audio-driven (Wan 2.5/2.6, Seedance @Audio); multi-shot features for shot/reverse-shot coverage.

## 8. Evaluation

- VBench (subject/background consistency, flicker, motion smoothness, dynamic degree, aesthetic/imaging quality); VBench-2.0 (human fidelity, controllability, physics, commonsense; https://arxiv.org/abs/2503.21755); VideoScore2 (VLM judge for quality, prompt alignment, physics). CLIP/DINO similarity correlates poorly with overall quality; use it only for identity checks.
- Practical rubric: sample frames at 1-2 fps → contact sheet; identity vs reference sheet; VLM judge on the frame grid with a checklist (one action completed, camera move as asked, morphing/extra limbs/warped text, light and screen direction match the previous shot, style matches the bible); pass/fail per item → coded fix. Three strikes on one shot → re-plan the shot, stop re-prompting.

## 9. Existing skills to learn from (ideas yes, text no)

- DirectorSKILL (MIT): https://github.com/wuwangzhang1216/DirectorSKILL. Borrow the router-to-references SKILL.md, 13-step pipeline, per-model adapters, F1-F19 failure table (symptom → cause → fix, cheapest first), continuity bible, evals. Skip director-style overlays as a core feature.
- smixs/visual-skills (CC BY 4.0, attribution required for derivatives): https://github.com/smixs/visual-skills. Borrow: ban empty adjectives; scene formula (desire + obstacle + geometry + gaze + rhythm); shot cards with five anchors; mandatory audit before output; exact Seedance/Kling/Veo syntax.
- Emily2040/seedance-2.0 (closest competitor, a whole AI-filmmaking pipeline); fal-ai-community/skills (`cinematography`, kling, lip-sync, video-edit); remotion-dev/skills; HEOJUNFO/ai-film-crew (role prompts); nolanx-ai director-visual-language; Alisa0808/vibe-creating-skill. Topic: https://github.com/topics/ai-filmmaking.
- Research pipelines (MovieAgent, FilmAgent, DreamFactory, StoryAgent, Anim-Director): borrow the role split and a critique-the-plan step before rendering; skip their code.
- MCP: Comfy Partner MCP (https://docs.comfy.org/development/mcp), fal-mcp-server. cinewright should stay generator-agnostic and hand off to whatever renders.
- Gap found: no cinematography knowledge base that covers all film roles and targets all three hosts.

## 10. Packaging for three hosts

- Agent Skills standard (https://agentskills.io/specification): `name` ≤ 64 chars, lowercase-hyphen, matches folder; `description` ≤ 1024 chars; optional `license`, `compatibility`, `metadata`, `allowed-tools`. Keep to these six fields: claude.ai rejects Claude Code-only keys ("Unexpected key(s)"). Validator: `skills-ref validate`.
- Claude Code: `.claude-plugin/marketplace.json`; anthropics/skills slices one shared `skills/` tree into several plugins with `"source": "./"`, `"strict": false`, `"skills": [...]`. Install `/plugin marketplace add m4bwav/<repo>` then `/plugin install <plugin>@<marketplace>`. Check with `claude plugin validate .`. Skill listing gets ~1% of context; description + when_to_use cut at 1,536 chars, so triggers first.
- Claude Desktop / claude.ai: Customize > Skills > upload ZIP whose top level is the skill folder (code execution on); or Customize > Plugins > add marketplace from GitHub (same marketplace.json serves Code, Desktop, claude.ai; hooks, sub-agents and local MCP only in Cowork and Code). A ZIP holds one skill folder, so anything a skill needs must sit inside that folder.
- GitHub Copilot: skills found in `.github/skills/`, `.claude/skills/`, `.agents/skills/`, `~/.copilot/skills/`, `~/.agents/skills/` (VS Code also `~/.claude/skills/`). `gh skill install owner/repo [skill]` (gh 2.90+, preview) installs for Copilot, Claude Code, Cursor, Codex, Gemini CLI. Copilot CLI: `copilot plugin marketplace add owner/repo` finds `marketplace.json` in `.github/plugin/` or `.claude-plugin/` (untested; test it). Agent Plugins 1.0 (https://agent-plugins.org, 2026-08-06): root `plugin.json` with `$schema`; ship it beside `.claude-plugin/plugin.json`. AGENTS.md read by VS Code, Copilot CLI and the cloud agent.
- Unverified: VS Code's command to install from a marketplace; whether a Claude Code marketplace installs cleanly in Copilot CLI.

## 11. Token rules (Anthropic best practices + evergreen)

Add only what the model lacks; SKILL.md is a table of contents (< 500 lines, aim far lower); references one level deep; files over 100 lines open with a contents list; scripts are run, not read; one default, not a menu; consistent terms; third-person descriptions with trigger words first; no time-sensitive prose outside dated cards; evals first (≥ 3 scenarios + baseline, on Haiku, Sonnet and Opus).

## 12. Official listings (checked 2026-10-03)

- Claude directory (https://claude.ai/directory): submit a plugin bundle at https://claude.ai/directory/manage (portal opened 2026-09-25; Pro, Max, Team or Enterprise; Mark's Pro/Max account works). Skills alone are not a submission type; put them in a plugin bundle. Repo must be public before the listing goes live. Automated validation and security scan on every version, human review for a new listing; later versions are picked up from the tracked branch. One listing shows in every Claude app that supports its contents; Usage tab shows installs and skill runs. Checklist: https://claude.com/docs/plugins/pre-submission-checklist ; docs: https://claude.com/docs/directory/publish . Bound by the Software Directory Terms and Policy.
- GitHub Copilot: Copilot CLI has two marketplaces registered by default, `copilot-plugins` (GitHub's own, not open to outside listings as far as found) and `awesome-copilot` (community). awesome-copilot takes a skill as a PR into its `skills/` folder, or an external plugin (public GitHub repo, pinned SHA) via its external-plugin issue form, which runs validation and maintainer review, then adds it to `plugins/external.json`. https://github.com/github/awesome-copilot/blob/main/CONTRIBUTING.md , https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-finding-installing
- Plan implication for cinewright S7: submit the core plugin to the Claude directory and to awesome-copilot as an external plugin after the public release.
