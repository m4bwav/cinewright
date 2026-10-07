# cinewright-craft

Film craft skills for AI video, one per crew role. Each works on the project folder the core `cinewright` plugin sets up and ships its own `scripts/cine.py` (Python 3.9+, standard library, no network).

- `cinewright-script`: the screenwriter. A one-sentence logline, beats that are visible changes, one value turn per scene, a plain-text screenplay whose sluglines match the scene bible, and lines short enough for a generated voice (the continuity diff warns when a line does not fit its shot).
- `cinewright-design`: the production and costume designer. Turnaround sheets for each character, reference images cleaned of stray marks, a fixed description per prop (`bibles/props.json`, pasted verbatim into every prompt), costume arcs by scene and a color script.
- `cinewright-movement`: the movement director. Weight, contact and follow-through, one movement phrase per shot, fights as single exchanges, and hard subjects (animals, crowds, hands, liquids) framed few, large and side-on. Battles as a map, two sides with fixed screen direction, phases and scale built from few large figures.
- `cinewright-camera`: the cinematographer and gaffer. Lens family and per-shot lenses, depth of field, exposure, frame rate and shutter, the film's frame (2.39 inside a 16:9 render), anamorphic, lighting ratios and setups, color temperature. Writes them into the style bible, where the compiler and the continuity diff use them.
- `cinewright-history`: the film historian. About 70 compact style cards (movements, format eras, genres, directors, cinematographers); a request such as "shoot it like 1970s New Hollywood, 2.39" becomes style-bible fields, tried with `--style` before it is adopted.

- `cinewright-edit`: the editor. Assembles passing takes in card order, finds a multi-shot generation's own cuts, trims settle and drift frames, chooses each cut by Murch's rule of six, splits dialogue with J and L cuts, sets pace by average shot length, cuts battles around geography wides, and conforms the cut list with ffmpeg.
- `cinewright-finish`: the colorist and VFX finisher. Grade order (correct, balance, match, look) with measured values, color spaces for display-referred AI clips, the crop to the style's `frame_aspect`, day for night, crowd multiplication and cleanup in compositing, upscale and interpolation last, a tagged Rec.709 delivery.
- `cinewright-sound`: the sound designer and mixer. Six layers and stems, Chion's terms, fixing generated audio, battle sound in distance layers, music spotting, and a mix brought to a stated loudness target (web, EBU R128, ATSC A/85, Netflix, music streaming) and proven with `qc loud --preset`.
- `cinewright-voice`: the voice director. A voice sheet per character, a voice designed new or cut from generated takes, locked as reference clips with the exact engine settings (`bibles/voices.json`), routes through open TTS in ComfyUI, hosted TTS or the video model itself, and `voice check` on every new line (pitch and pace against the references).

This plugin needs the core `cinewright` plugin installed. License: MIT.
