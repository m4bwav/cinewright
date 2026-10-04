# cinewright (core plugin)

Plan AI video like a film crew. Five skills:

- `cinewright`: the director. Takes an idea through brief, bibles, shot cards, continuity check, prompts, render, QC and edit, and says which skill handles each stage.
- `cinewright-shots`: the shot planner. Blocks each scene, picks the coverage the cut needs, writes one card per shot, prints the shot list (`cine.py cards list`) and groups shots into generations.
- `cinewright-continuity`: the script supervisor. Writes character, prop, location, scene-axis and style bibles, then diffs every shot card against them: identity strings, wardrobe, props in hand, the 180-degree rule, screen direction, eyelines, the 30-degree rule, time of day.
- `cinewright-genvideo`: the prompt compiler. Turns a checked card plus the bibles into one model's prompt and settings for Veo 3.1, Gemini Omni Flash, Kling 3.0, Seedance 2.5, Runway Gen-4.5, Luma Ray3.2, MiniMax H3, Wan 2.2 or LTX-2, with the cost of a hosted take.
- `cinewright-qc`: the take reviewer. Contact sheets, spec and loudness checks (ffmpeg), a rubric built from the shot card, and failure codes routed to the cheapest fix.

Each skill ships `scripts/cine.py` (Python 3.9+, standard library, no network). Writing a prompt never starts a render; hosted renders cost money and the skills ask first.

For deeper craft install `cinewright-craft`: script, design and movement now; camera, edit and sound later. License: MIT.
