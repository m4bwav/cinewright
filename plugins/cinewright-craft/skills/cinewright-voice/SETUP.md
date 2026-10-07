# Setup: cinewright-voice

What [SKILL.md](SKILL.md) needs outside itself, what each piece is for, how to check it, and how to install it on each environment met so far. Format and rules: the protocol's `SETUP.md` spec. Check here with `evergreen.py setup <this folder>`; it reads the tables below, so keep their shape. Test runs that needed these pieces: [TESTS.md](TESTS.md); install lessons: [LEARNINGS.md](LEARNINGS.md); changes: [CHANGELOG.md](CHANGELOG.md); sources: [RESEARCH.md](RESEARCH.md).

When a step fails for a missing piece (command not found, a refused connection, an unknown model), or this environment is not in Environments met: run the check, tell the user what is missing and what it is for, install what you can after saying so, hand the rest to the user with the exact steps, re-check, then record what worked (`--record ... --verified`) and the environment (`--log`).

## Needs

| id | kind | check | for | if missing |
|---|---|---|---|---|
| python | command | `python --version >= 3.9 \| python3 --version >= 3.9` | runs `scripts/cine.py` in every step | required |
| ffmpeg | command | `ffmpeg -version` | decodes takes and cuts reference clips (`voice ref`), and reads audio for `voice measure` and `voice check` | required |
| comfyui | url | `http://127.0.0.1:8188/system_stats` | the default local route: designing and cloning voices with the TTS Audio Suite node pack (Step 3) | optional: a hosted engine, or the user's own TTS tool |
| ollama | url | `http://127.0.0.1:11434/api/tags` | drafting voice sheets, design prompts, delivery tags and rough transcripts (Step 2) | optional: write the drafts yourself |
| elevenlabs-key | env | `ELEVENLABS_API_KEY` | the hosted route: Voice Design, cloning, Voice Changer (Step 3) | optional: the local route |

## Install

### python

- any: https://www.python.org/downloads/ (3.9 or newer; standard library only)

### ffmpeg

- windows/winget: `winget install --id Gyan.FFmpeg -e` then open a new terminal so PATH updates (verified 2026-10-03 on windows/claude-code)
- macos/brew: `brew install ffmpeg`
- linux/apt: `sudo apt-get install -y ffmpeg` (admin)

### comfyui

- any: install ComfyUI from https://github.com/comfyanonymous/ComfyUI, then TTS Audio Suite from ComfyUI Manager (search "TTS Audio Suite"); each engine downloads its model on first use, several GB (manual, large)

### ollama

- any: https://ollama.com/download, then `ollama pull gemma4:12b` for a model that can also listen to clips (large)

### elevenlabs-key

- any: create a key at https://elevenlabs.io (account settings, API keys) and set `ELEVENLABS_API_KEY` in the environment (manual, secret, paid)

## Attempts

| date | need | env | route | result | took | notes |
|---|---|---|---|---|---|---|

## Environments met

| date | os | harness | missing | notes |
|---|---|---|---|---|
| 2026-10-07 | windows | claude-code | comfyui (not running), elevenlabs-key | ffmpeg 9.0.1; Ollama 0.40.0 with gemma4:12b (audio capability) |
