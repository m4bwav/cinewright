# cinewright-craft

Film craft skills for AI video, one per crew role. Each works on the project folder the core `cinewright` plugin sets up and ships its own `scripts/cine.py` (Python 3.9+, standard library, no network).

- `cinewright-script`: the screenwriter. A one-sentence logline, beats that are visible changes, one value turn per scene, a plain-text screenplay whose sluglines match the scene bible, and lines short enough for a generated voice (the continuity diff warns when a line does not fit its shot).
- `cinewright-design`: the production and costume designer. Turnaround sheets for each character, reference images cleaned of stray marks, a fixed description per prop (`bibles/props.json`, pasted verbatim into every prompt), costume arcs by scene and a color script.
- `cinewright-movement`: the movement director. Weight, contact and follow-through, one movement phrase per shot, fights as single exchanges, and hard subjects (animals, crowds, hands, liquids) framed few, large and side-on.

Camera and lighting, editing, color and VFX, sound and film history arrive in later releases. This plugin needs the core `cinewright` plugin installed. License: MIT.
