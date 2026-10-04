# Setup: cinewright-qc

What [SKILL.md](SKILL.md) needs outside itself, what each piece is for, how to check it, and how to install it on each environment met so far. Format and rules: the protocol's `SETUP.md` spec. Check here with `evergreen.py setup <this folder>`; it reads the tables below, so keep their shape.

When a step fails for a missing piece (command not found, a module that will not import, a refused connection, an unknown model), or this environment is not in Environments met: run the check, tell the user what is missing and what it is for, install what you can after saying so, hand the rest to the user with the exact steps, re-check, then record what worked (`--record ... --verified`) and the environment (`--log`).

## Needs

| id | kind | check | for | if missing |
|---|---|---|---|---|
| python | command | `python --version >= 3.9 \| python3 --version >= 3.9` | runs `scripts/cine.py` in every step | required |
| ffmpeg | command | `ffmpeg -version` | contact sheets (`qc sheet`), loudness (`qc loud`), last frames (`takes lastframe`) | required |
| ffprobe | command | `ffprobe -version` | clip facts for `qc sheet` and `qc spec`; ships with ffmpeg | required |

## Install

### python

- any: https://www.python.org/downloads/ (3.9 or newer; standard library only)

### ffmpeg

- windows/winget: `winget install --id Gyan.FFmpeg -e` then open a new terminal so PATH updates (verified 2026-10-03 on windows/claude-code)
- macos/brew: `brew install ffmpeg`
- linux/apt: `sudo apt-get install -y ffmpeg` (admin)
- any: https://ffmpeg.org/download.html

### ffprobe

- any: installed with ffmpeg; if `ffprobe` is missing, the ffmpeg build is a minimal one: install the full build above.

## Attempts

| date | need | env | route | result | took | notes |
|---|---|---|---|---|---|---|

## Environments met

| date | os | harness | missing | notes |
|---|---|---|---|---|
| 2026-10-03 | windows | claude-code | none | ffmpeg 9.0.1 full build from winget (Gyan.FFmpeg) |
