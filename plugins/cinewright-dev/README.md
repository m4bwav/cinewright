# cinewright-dev

Maintainer tools for the cinewright knowledge base: adding, verifying and retiring reference entries, and refreshing model cards when a video model changes.

Skill: `cinewright-curate`. It works in a clone of the cinewright repository and runs `python scripts/cine.py kb` (`due`, `new`, `verify`, `retire`, `lint`), which edits files under `plugins/` and `shared/` and writes a CHANGELOG line. It fetches nothing by itself; the pages you re-check are yours to open. It is listed in the cinewright marketplace for maintainers and is never submitted to plugin directories. People who only want to make films do not need it. Use the core `cinewright` plugin instead. License: MIT.
