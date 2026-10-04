# cinewright (core plugin)

Plan AI video like a film crew. Three skills:

- `cinewright`: the director. Takes an idea through brief, bibles, shot cards, continuity check, prompts, render, QC and edit, and says which skill handles each stage.
- `cinewright-continuity`: the script supervisor. Writes character, location, scene-axis and style bibles, then diffs every shot card against them: identity strings, wardrobe, props in hand, the 180-degree rule, screen direction, eyelines, the 30-degree rule, time of day.
- `cinewright-genvideo`: the prompt compiler. Turns a checked card plus the bibles into one model's prompt and settings. Veo 3.1 only so far; more models in later releases.

Each skill ships `scripts/cine.py` (Python 3.9+, standard library, no network). Writing a prompt never starts a render; hosted renders cost money and the skills ask first.

For deeper craft (script, camera, design, edit, sound) install `cinewright-craft` when it has skills. License: MIT.
