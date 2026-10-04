# cinewright-craft

Film craft skills for AI video, one per crew role. Each works on the project folder the core `cinewright` plugin sets up and ships its own `scripts/cine.py` (Python 3.9+, standard library, no network).

- `cinewright-script`: the screenwriter. A one-sentence logline, beats that are visible changes, one value turn per scene, a plain-text screenplay whose sluglines match the scene bible, and lines short enough for a generated voice (the continuity diff warns when a line does not fit its shot).
- `cinewright-design`: the production and costume designer. Turnaround sheets for each character, reference images cleaned of stray marks, a fixed description per prop (`bibles/props.json`, pasted verbatim into every prompt), costume arcs by scene and a color script.
- `cinewright-movement`: the movement director. Weight, contact and follow-through, one movement phrase per shot, fights as single exchanges, and hard subjects (animals, crowds, hands, liquids) framed few, large and side-on. Battles as a map, two sides with fixed screen direction, phases and scale built from few large figures.
- `cinewright-camera`: the cinematographer and gaffer. Lens family and per-shot lenses, depth of field, exposure, frame rate and shutter, the film's frame (2.39 inside a 16:9 render), anamorphic, lighting ratios and setups, color temperature. Writes them into the style bible, where the compiler and the continuity diff use them.
- `cinewright-history`: the film historian. About 70 compact style cards (movements, format eras, genres, directors, cinematographers); a request such as "shoot it like 1970s New Hollywood, 2.39" becomes style-bible fields, tried with `--style` before it is adopted.

Editing, color and VFX, and sound arrive in later releases. This plugin needs the core `cinewright` plugin installed. License: MIT.
