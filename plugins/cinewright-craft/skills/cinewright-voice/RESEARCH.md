# Research: cinewright-voice

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); dependencies in [SETUP.md](SETUP.md); schedule and state in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Topic: Consistent character voices for AI video: voice sheets, voice design and cloning (open and hosted TTS), reference clips from generated takes, voice conversion, video-model voices and lip-sync, measuring drift, rights and consent; local routes through ComfyUI and Ollama. Tier `fast`. Last refresh 2026-10-07; next due 2026-10-21.

## Current understanding

- Settled (craft): a voice sheet plus a replayable reference clip plus a pronunciation list is how animation, games and audiobooks keep a voice (GDC Vault 2010, 2016; ACX; CMOS Shop Talk 2019).
- Settled (engines, 2026-10-07): design-then-clone is the documented open recipe (Qwen3-TTS, Apache-2.0); hosted ElevenLabs locks a voice by voice_id + model + settings + seed. Licences differ per engine (table in references/voice-engines.md).
- Settled (video models, 2026-10-07): only Kling 3.0 binds a custom voice across shots; prompt-only models drift; the fix is voice conversion (keep timing) or regenerate plus lip-sync.
- Settled (local, tested 2026-10-07): ComfyUI core has no TTS; TTS Audio Suite is the maintained pack. Ollama has no TTS; gemma4 with the audio capability transcribes roughly and misjudges speaker gender.
- Settled (measure, tested 2026-10-07): stdlib YIN pitch separates male and female clips by about 12 semitones; music under a line corrupts it. Identity needs an ear or a speaker-embedding model with a per-character baseline.
- Unverified: Flow Voice Ingredients for Veo (one blog), Sora 2 API cameo voices, VoxCPM2 and Fish S2 licences, per-engine VRAM beyond Qwen3-TTS.

## Open questions

- TTS Audio Suite's licence is NOASSERTION: safe to recommend for commercial work?
- Does any engine persist a speaker embedding the suite exposes (Qwen3 x-vector, Chatterbox conds)?
- SIM floors across emotional takes of the same character: no source sets one.
- Will Ollama document audio input outside MLX?

## Search plan

Four tracks; every refresh runs at least one query on each, scoped to the time since the last refresh.

Subject:

- GitHub API `repos/QwenLM/Qwen3-TTS`, `repos/index-tts/index-tts`, `repos/resemble-ai/chatterbox` (releases, licence)
- ElevenLabs changelog; `kling.ai/blog voice`; `Veo voice reference <month> <year>`

Tooling:

- `api.github.com/repos/diodiogod/TTS-Audio-Suite` (pushed_at, releases); `search/repositories?q=comfyui+tts&sort=updated`
- `github.com/ollama/ollama/releases` grep audio; `path:SKILL.md "voice" "reference audio"`

Practice:

- `AI film consistent character voice <month> <year>`; HN Algolia "voice changer veo"
- `NO FAKES Act House markup`; `AI Act Article 50 code of practice`

Testing:

- `site:arxiv.org speaker similarity zero-shot TTS <year>`; seed-tts-eval releases

## Findings

### R-20261007-1 · 2026-10-07 · Baseline research for a new unit · m 0.6
- Tracks: subject, tooling, practice, testing
- Two research passes and a local test; full notes with sources in the repository's ai-docs/research/2026-10-07-voice-consistency.md.
- Led to: C-20261007-1
