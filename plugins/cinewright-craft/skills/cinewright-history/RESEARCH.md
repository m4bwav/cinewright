# Research: cinewright-history

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Topic: Film history style cards for AI video: movements, eras, genres, directors and cinematographers, applied through style-bible fields. Tier `glacial`. Last refresh 2026-10-04; next due 2027-10-04.

## Current understanding

- Settled (craft): movement, era and genre devices (Bordwell and Thompson; Cousins); format dates from the aspect-ratio and film-stock pages (checked 2026-10-04).
- Settled (runtime, 2026-10-04): a style reaches prompts only through style-bible fields; card ids sit in `history` for the record; `--style FILE` tries a look without editing the bible.
- Unverified: every `~` timestamp (approximate, unchecked against a copy); whether naming directors or films in prompts drifts or is refused per model.

## Open questions

- Which `~` timestamps are wrong by more than five minutes? Check against copies when a card is used in a brief.
- Do two cards combined (era plus director) stay distinct in renders, or average out?

## Search plan

Four tracks; every refresh runs at least one query on each, scoped to the time since the last refresh.

Subject:

- `film movement history style devices <year>`
- `cinematographer signature style interview <year>`

Tooling:

- `path:SKILL.md "film style"` on GitHub code search; skills.sh weekly installs for `film style`
- `https://registry.modelcontextprotocol.io/v0/servers?search=film`

Practice:

- `AI video in the style of director prompt <month> <year>`
- `video model artist name policy <year>`

Testing:

- `style consistency video generation evaluation <year>`
- `path:SKILL.md style evals`

Best sources (primary first): Bordwell and Thompson, Film History and Film Art; Cousins, The Story of Film; American Cinematographer interviews; FilmGrab for frames. Noisy: listicles of 'director styles'.

## Findings log

Newest first. `Track` is subject, tooling, practice, or testing.

### R-20261004-1 · 2026-10-04 · Initial research
- Summary: Built from the research brief §5 card list (subject: 12 movements, 8 eras, 10 genres, 40 directors and cinematographers), format dates checked this session (Wikipedia, Film and Digital Times), PLAN §10's exit check (practice: a style request must change compiled prompts in checkable ways), and TESTING.md (testing: the compile and diff checks prove it).
- Track: subject
- Sources: https://en.wikipedia.org/wiki/Aspect_ratio_(image), https://en.wikipedia.org/wiki/List_of_motion_picture_film_stocks, https://www.fdtimes.com/2013/09/12/angenieux-25-250-optimo-dp/, https://theasc.com/american-cinematographer
- Magnitude: n/a (initial)
- Applied: C-20261004-1
