# cinewright

Film craft for AI video. cinewright makes an agent plan a film like a crew and check it like a script supervisor, so separately generated shots keep the same people, wardrobe, props, eyelines, screen direction and light. Each shot is a generator-neutral shot card; a compiler turns a card plus the project's bibles into a given model's prompt.

Status: 0.1.0, the first release. Install routes proved on Windows 11: Claude Code, GitHub Copilot CLI and `gh skill`.

## What is here

| Plugin | Skills | For |
|---|---|---|
| `cinewright` | `cinewright` (director and router), `cinewright-shots` (shot list and coverage), `cinewright-continuity` (script supervisor), `cinewright-genvideo` (prompt compiler for nine models), `cinewright-qc` (take review with ffmpeg) | everyone |
| `cinewright-craft` | `cinewright-script` (logline, beats, dialogue), `cinewright-design` (turnarounds, props, costume, color), `cinewright-movement` (weight, fights, battles, hard subjects), `cinewright-camera` (lens, light, format), `cinewright-history` (style cards), `cinewright-edit` (cutting, pacing), `cinewright-finish` (grade, crop, VFX, delivery), `cinewright-sound` (layers, mix, loudness), `cinewright-voice` (character voices that match shot to shot) | deeper craft |
| `cinewright-dev` | `cinewright-curate` (add, verify and retire knowledge-base entries; refresh model cards; works in a clone of this repository) | maintainers |

A worked example lives in [examples/three-shot/](examples/three-shot/): a one-line idea taken through brief, script, shot list, bibles, design notes, a continuity diff that catches a planted error, and compiled Veo and MiniMax H3 prompts.

## Install

| Host | How |
|---|---|
| Claude Code | `/plugin marketplace add m4bwav/cinewright`, then `/plugin install cinewright@cinewright` (and `cinewright-craft@cinewright` for the craft skills) |
| GitHub Copilot CLI | `copilot plugin marketplace add m4bwav/cinewright`, then `copilot plugin install cinewright@cinewright` |
| Any agent with the GitHub CLI | `gh skill install m4bwav/cinewright cinewright-continuity --agent claude-code` (plain skill names; `--agent` picks the host folder) |
| claude.ai | Customize > Skills > Upload skill, one ZIP per skill from the release assets |

Install the core plugin first: the craft skills compile through `cinewright-genvideo`'s model cards. Installing copies the skill folders; nothing runs until a skill is used.

## What it runs and fetches

Each skill ships `scripts/cine.py` (Python 3.9+, standard library only). It reads and writes JSON and Markdown in your project folder. It makes no network calls and never renders: writing a prompt never starts a paid render. The qc commands call ffmpeg and ffprobe on clips you already have.

## Developing

```
python -m unittest discover -s tests     # tests
python scripts/cine.py kb lint           # schemas, links, copies, manifests
python scripts/cine.py budget            # size budgets (green, yellow, red)
python scripts/cine.py build             # copy shared/ into skills, rebuild indexes
python scripts/cine.py zip cinewright-continuity   # claude.ai upload ZIP in dist/
python scripts/cine.py kb due                      # entries past their re-check interval (cinewright-curate)
python scripts/cine.py scrub --names FILE          # private details in tracked files, before going public
```

Edit shared vocabulary, schemas and the library in `shared/`, never the copies inside skills; `build` copies them and `kb lint` fails on drift. The plan is [ai-docs/plans/PLAN.md](ai-docs/plans/PLAN.md).

## Credits

Ideas (not text) from MIT-licensed skill repositories, including DirectorSKILL: response-size ceilings, the repair cost ladder, one owning reference per dimension, continuing from the previous take's observed end state, one change per reroll. Film craft from Arijon, Block, Bordwell and Thompson, Brown, Cousins, Field, Katz, Landis, LoBrutto, Mascelli, McKee, Miller, Murch, Riley, Rowlands, Snyder, Thomas and Johnston, and Weston, cited in each entry.

## License

MIT, see [LICENSE](LICENSE).
