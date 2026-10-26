"""Tests for scripts/cine.py and shared/lib/cine.py. Run: python -m unittest discover -s tests"""
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CLI = REPO / "scripts" / "cine.py"
EXAMPLE = REPO / "examples" / "three-shot"
SKILLS = REPO / "plugins" / "cinewright" / "skills"

_spec = importlib.util.spec_from_file_location("cine_lib", REPO / "shared" / "lib" / "cine.py")
lib = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lib)


def run(*args, script=CLI):
    r = subprocess.run([sys.executable, str(script)] + [str(a) for a in args], capture_output=True, text=True, encoding="utf-8")
    return r.returncode, r.stdout + r.stderr


def copy_repo(dst):
    for name in ("plugins", "shared", ".claude-plugin", "examples", "ai-docs", "assets", "README.md", "LICENSE", "AGENTS.md", "CODEMAP.md"):
        src = REPO / name
        if src.is_dir():
            shutil.copytree(src, dst / name, ignore=shutil.ignore_patterns("__pycache__"))
        else:
            shutil.copy2(src, dst / name)
    return dst


def edit(path, old, new):
    text = lib.read_text(path)
    assert old in text, old
    lib.write_text(path, text.replace(old, new, 1))


class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()


class TestKb(Base):
    def test_index_from_skill_copy(self):
        skill = self.tmp / "cinewright-continuity"
        shutil.copytree(SKILLS / "cinewright-continuity", skill)
        (skill / "references" / "INDEX.md").unlink()
        code, out = run("kb", "index", script=skill / "scripts" / "cine.py")
        self.assertEqual(code, 0, out)
        text = (skill / "references" / "INDEX.md").read_text(encoding="utf-8")
        self.assertIn("- `eyelines`:", text)
        self.assertIn("- `thirty-degree-rule`:", text)

    def test_search(self):
        code, out = run("kb", "search", "eyeline")
        self.assertEqual(code, 0, out)
        self.assertIn("eyelines", out)
        self.assertEqual(out.count("screen-direction ("), 1, "copies of one vocab entry must be listed once")
        code, _ = run("kb", "search", "zzzqqq")
        self.assertEqual(code, 1)

    def test_show_section(self):
        code, out = run("kb", "show", "thirty-degree-rule", "--section", "Numbers")
        self.assertEqual(code, 0, out)
        self.assertIn("30 degrees azimuth", out)
        self.assertIn("https://en.wikipedia.org/wiki/30-degree_rule", out)
        self.assertNotIn('"https', out, "quoted list items must be unquoted")
        code, _ = run("kb", "show", "thirty-degree-rule", "--section", "Nope")
        self.assertEqual(code, 1)

    def test_lint_clean(self):
        code, out = run("kb", "lint")
        self.assertEqual(code, 0, out)

    def test_lint_catches_drift(self):
        root = copy_repo(self.tmp)
        edit(root / "plugins/cinewright/skills/cinewright-continuity/references/shot-sizes.md", "## Rules", "## Rules\n\n- hand edit")
        code, out = run("--root", root, "kb", "lint")
        self.assertEqual(code, 1)
        self.assertIn("drift from shared/vocab/shot-sizes.md", out)

    def test_lint_catches_extra_frontmatter_key_and_bad_entry(self):
        root = copy_repo(self.tmp)
        edit(root / "plugins/cinewright/skills/cinewright/SKILL.md", "license: MIT", "license: MIT\nversion: 1")
        edit(root / "plugins/cinewright/skills/cinewright/references/pipeline.md", "slug: pipeline", "slug: pipe-line")
        code, out = run("--root", root, "kb", "lint")
        self.assertEqual(code, 1)
        self.assertIn("frontmatter keys outside the six allowed: version", out)
        self.assertIn("slug 'pipe-line' must equal the file name", out)

    def test_lint_catches_private_path(self):
        root = copy_repo(self.tmp)
        edit(root / "plugins/cinewright/README.md", "License: MIT.", "License: MIT. See " + "D:" + "/work/notes.")
        code, out = run("--root", root, "kb", "lint")
        self.assertEqual(code, 1)
        self.assertIn("local drive path", out)


class TestCurate(Base):
    CARD = "plugins/cinewright/skills/cinewright-genvideo/references/wan-2-2.md"

    def test_due_lists_cards_with_claims(self):
        code, out = run("kb", "due", "--days", "0")
        self.assertEqual(code, 0, out)
        self.assertIn("wan-2-2.md  [model card]", out)
        self.assertIn("claim:", out)
        self.assertIn("shared/vocab/shot-sizes.md", out)
        self.assertNotIn("cinewright-continuity/references/shot-sizes.md", out, "copies are listed by their source")

    def test_new_verify_retire_entry(self):
        root = copy_repo(self.tmp)
        code, out = run("--root", root, "kb", "new", "cinewright-camera", "anamorphic-flare", "--title", "Anamorphic flare",
                        "--summary", "Horizontal blue streak flares from anamorphic lenses and how to prompt them.",
                        "--tags", "camera,lens", "--source", "https://example.com/flare")
        self.assertEqual(code, 0, out)
        p = root / "plugins/cinewright-craft/skills/cinewright-camera/references/anamorphic-flare.md"
        self.assertIn("## Rules", lib.read_text(p))
        self.assertIn("`anamorphic-flare`", lib.read_text(p.parent / "INDEX.md"))
        code, out = run("--root", root, "kb", "new", "cinewright-camera", "anamorphic-flare", "--title", "Again",
                        "--summary", "x" * 30, "--tags", "camera", "--source", "https://example.com/a")
        self.assertNotEqual(code, 0, "a slug that exists must be refused")
        code, out = run("--root", root, "kb", "verify", "anamorphic-flare", "--source", "https://example.com/second",
                        "--note", "no change")
        self.assertEqual(code, 0, out)
        meta, body = lib.parse_frontmatter(lib.read_text(p))
        self.assertEqual(meta["sources"], ["https://example.com/flare", "https://example.com/second"])
        self.assertRegex(body, r"## Notes\n\n- \d{4}-\d\d-\d\d: verified against https://example.com/second; no change")
        code, out = run("--root", root, "kb", "retire", "anamorphic-flare", "--reason", "merged into lens-choice")
        self.assertEqual(code, 0, out)
        self.assertFalse(p.exists())
        self.assertNotIn("anamorphic-flare", lib.read_text(p.parent / "INDEX.md"))
        self.assertRegex(lib.read_text(p.parent.parent / "CHANGELOG.md"), r"### C-\d{8}-\d+ · [\d-]+ · Retired entry anamorphic-flare")
        code, out = run("--root", root, "kb", "lint")
        self.assertEqual(code, 0, out)

    def test_retire_refuses_referenced_entry_and_vocab(self):
        root = copy_repo(self.tmp)
        code, out = run("--root", root, "kb", "retire", "eyelines", "--reason", "test")
        self.assertNotEqual(code, 0)
        self.assertIn("still names eyelines", out)
        code, out = run("--root", root, "kb", "retire", "shot-sizes", "--reason", "test")
        self.assertNotEqual(code, 0)
        self.assertIn("shared vocab used by", out)

    def test_retire_model_card_keeps_file(self):
        root = copy_repo(self.tmp)
        code, out = run("--root", root, "kb", "retire", "wan-2-2", "--reason", "vendor shut it down")
        self.assertEqual(code, 0, out)
        text = lib.read_text(root / self.CARD)
        self.assertIn("status: shut-down", text)
        self.assertRegex(text, r"- \d{4}-\d\d-\d\d: shut-down; vendor shut it down\n\n## Compile")
        code, out = run("--root", root, "kb", "lint")
        self.assertEqual(code, 0, out)

    def test_verify_vocab_source_rebuilds_copies(self):
        root = copy_repo(self.tmp)
        code, out = run("--root", root, "kb", "verify", "shot-sizes", "--source", "https://example.com/sizes")
        self.assertEqual(code, 0, out)
        copy = lib.read_text(root / "plugins/cinewright/skills/cinewright-continuity/references/shot-sizes.md")
        self.assertIn("verified against https://example.com/sizes", copy)
        code, out = run("--root", root, "kb", "lint")
        self.assertEqual(code, 0, out)

    def test_scrub(self):
        root = copy_repo(self.tmp)
        names = self.tmp / "names.txt"
        names.write_text("# private\nsecretproject\n", encoding="utf-8")
        # split so kb lint and scrub do not flag this file
        lan, host, mail = "192.168." + "1.5", "DESKTOP-" + "ABC1234", "a@" + "b.org"
        (root / "ai-docs" / "x.md").write_text("host %s at %s, mail %s, ok@example.com, see SecretProject\n"
                                               % (host, lan, mail), encoding="utf-8")
        code, out = run("--root", root, "scrub", "--names", names)
        self.assertEqual(code, 1, out)
        for what in ("hostname (%s)" % host, "LAN address (%s)" % lan, "email (%s)" % mail, "private name (SecretProject)"):
            self.assertIn("ai-docs/x.md:1: " + what, out)
        self.assertNotIn("ok@example.com", out)


class TestBuild(Base):
    def test_build_propagates_source_change(self):
        root = copy_repo(self.tmp)
        edit(root / "shared/vocab/shot-sizes.md", "## Pitfalls", "## Pitfalls\n\n- new pitfall")
        code, out = run("--root", root, "kb", "lint")
        self.assertEqual(code, 1, "source change without build must fail lint")
        code, out = run("--root", root, "build")
        self.assertEqual(code, 0, out)
        self.assertIn("copied shared/vocab/shot-sizes.md", out)
        copy = (root / "plugins/cinewright/skills/cinewright-genvideo/references/shot-sizes.md").read_text(encoding="utf-8")
        self.assertIn("- new pitfall", copy)
        self.assertRegex(copy, r"<!-- copied from shared/vocab/shot-sizes.md sha256:[0-9a-f]{64}; edit the source -->")
        code, out = run("--root", root, "kb", "lint")
        self.assertEqual(code, 0, out)


class TestCards(Base):
    def test_validate_example(self):
        code, out = run("cards", "validate", EXAMPLE)
        self.assertEqual(code, 0, out)
        self.assertIn("3 cards, 0 errors", out)

    def test_validate_rejects_bad_card(self):
        proj = self.tmp / "p"
        shutil.copytree(EXAMPLE, proj)
        edit(proj / "cards/1B.json", '"duration_s": 4', '"duration_s": 12')
        code, out = run("cards", "validate", proj)
        self.assertEqual(code, 1)
        self.assertIn("12 is above 8", out)

    def test_new_copies_bible_strings(self):
        proj = self.tmp / "p"
        shutil.copytree(EXAMPLE, proj)
        code, out = run("cards", "new", proj, "--id", "1D", "--scene", "1", "--cast", "maren")
        self.assertEqual(code, 0, out)
        card = json.loads((proj / "cards/1D.json").read_text(encoding="utf-8"))
        bible = json.loads((proj / "bibles/characters.json").read_text(encoding="utf-8"))["characters"][0]
        self.assertEqual(card["cast"][0]["identity"], bible["identity"])
        self.assertEqual(card["order"], 4)
        code, out = run("cards", "validate", proj)
        self.assertEqual(code, 1, "a new card holds TODO until filled")
        self.assertIn("still holds TODO", out)

    def test_export_film_json(self):
        out_file = self.tmp / "film.json"
        code, out = run("cards", "export", EXAMPLE, "--film-json", "--out", out_file)
        self.assertEqual(code, 0, out)
        film = json.loads(out_file.read_text(encoding="utf-8"))
        self.assertEqual((film["name"], film["width"], film["height"], film["target_seconds"]), ("the_last_match", 1280, 720, 14))
        self.assertEqual([s["length"] for s in film["shots"]], [144, 96, 96])
        self.assertEqual([s["seed"] for s in film["shots"]], [101, 102, 103])
        self.assertEqual(list(film), ["name", "target_seconds", "width", "height", "seam_audio_xfade", "shots"])

    def test_export_film_json_sequence(self):
        proj = model_project(self.tmp)
        edit(proj / "bibles/style.json", '"resolution": "720p"', '"resolution": "480p"')
        out_file = self.tmp / "film.json"
        code, out = run("cards", "export", proj, "--film-json", "--sequence", "--model", "minimax-h3", "--out", out_file)
        self.assertEqual(code, 0, out)
        film = json.loads(out_file.read_text(encoding="utf-8"))
        self.assertEqual([s["name"] for s in film["shots"]], ["1A+1B+1C"], "one shot per generation, named like the compiled prompt")
        self.assertEqual((film["width"], film["height"]), (864, 480))
        self.assertEqual((film["shots"][0]["length"] - 5) % 17, 0, "frames on the model's grid")
        code, out = run("cards", "export", proj, "--film-json", "--sequence")
        self.assertNotEqual(code, 0, "--sequence without --model")


class TestCompile(Base):
    def test_compile_veo(self):
        out_dir = self.tmp / "veo"
        code, out = run("compile", EXAMPLE, "--model", "veo", "--out", out_dir)
        self.assertEqual(code, 0, out)
        bible = json.loads((EXAMPLE / "bibles/characters.json").read_text(encoding="utf-8"))["characters"]
        ids = {c["id"]: c["identity"] for c in bible}
        durations = {}
        for cid, cast in (("1A", ["maren", "tomas"]), ("1B", ["maren"]), ("1C", ["tomas"])):
            text = (out_dir / ("%s.txt" % cid)).read_text(encoding="utf-8")
            for c in cast:
                self.assertIn(ids[c], text)
            self.assertTrue(text.startswith(("Wide shot", "Medium close-up")), text[:40])
            params = json.loads((out_dir / ("%s.params.json" % cid)).read_text(encoding="utf-8"))
            durations[cid] = params["durationSeconds"]
            self.assertEqual(params["model"], "veo-3.1-generate-001")
        self.assertEqual(durations, {"1A": 6, "1B": 4, "1C": 4})
        self.assertIn("Maren says quietly: Last one.", (out_dir / "1B.txt").read_text(encoding="utf-8"))
        self.assertIn("Maren is looking toward frame right, at Tomas.", (out_dir / "1B.txt").read_text(encoding="utf-8"))
        self.assertIn("Maren is looking down, at the tin matchbox.", (out_dir / "1A.txt").read_text(encoding="utf-8"))

    def test_example_compiled_files_are_current(self):
        for sub, model, extra in (("veo", "veo", []), ("veo-sequence", "veo", ["--sequence"]),
                                  ("minimax-h3-sequence", "minimax-h3", ["--sequence", "--resolution", "480p"]),
                                  ("veo-new-hollywood", "veo", ["--style", EXAMPLE / "styles" / "new-hollywood-239.json"])):
            out_dir = self.tmp / sub
            code, out = run("compile", EXAMPLE, "--model", model, "--out", out_dir, *extra)
            self.assertEqual(code, 0, out)
            for f in out_dir.iterdir():
                committed = EXAMPLE / "compiled" / sub / f.name
                self.assertEqual(f.read_text(encoding="utf-8"), committed.read_text(encoding="utf-8"), "rerun the compile commands in examples/three-shot/README.md")

    def test_compile_sequence_uses_timestamps(self):
        code, out = run("compile", EXAMPLE, "--model", "veo", "--sequence")
        self.assertEqual(code, 0, out)
        self.assertIn("== 1B+1C", out)
        self.assertIn("[00:00-00:04]", out)
        self.assertIn("[00:04-00:08]", out)

    def test_music_goes_in_the_music_slot(self):
        proj = self.tmp / "p"
        shutil.copytree(EXAMPLE, proj)
        edit(proj / "cards/1B.json", '"sound":', '"music": "a lone cello, slow and low", "sound":')
        code, out = run("compile", proj, "--model", "minimax-h3", "--sequence", "--resolution", "480p", "--out", self.tmp / "h3")
        self.assertEqual(code, 0, out)
        text = "".join(f.read_text(encoding="utf-8") for f in (self.tmp / "h3").glob("*.txt"))
        self.assertIn("non_diegetic_music: A lone cello, slow and low.", text)
        code, out = run("compile", proj, "--model", "veo", "--card", "1B", "--out", self.tmp / "veo")
        self.assertEqual(code, 0, out)
        self.assertIn("Music: A lone cello, slow and low.", (self.tmp / "veo" / "1B.txt").read_text(encoding="utf-8"))

    def test_join_names_the_new_place_at_the_cut(self):
        proj = self.tmp / "p"
        shutil.copytree(EXAMPLE, proj)
        locs = json.loads((proj / "bibles/locations.json").read_text(encoding="utf-8"))
        locs["locations"].append({"id": "cliff", "name": "Cliff", "int_ext": "EXT",
                                  "description": "a storm-lashed cliff path below the lighthouse"})
        (proj / "bibles/locations.json").write_text(json.dumps(locs), encoding="utf-8")
        scenes = json.loads((proj / "bibles/scenes.json").read_text(encoding="utf-8"))
        outside = dict(scenes["scenes"][0], id="0", location="cliff")
        scenes["scenes"].insert(0, outside)
        (proj / "bibles/scenes.json").write_text(json.dumps(scenes), encoding="utf-8")
        edit(proj / "cards/1A.json", '"scene": "1"', '"scene": "0"')
        args = ["compile", proj, "--model", "minimax-h3", "--sequence", "--resolution", "480p"]
        code, out = run(*args)
        self.assertEqual(code, 0, out)
        self.assertIn("== 1A ", out)  # a new scene splits the generation
        code, out = run(*(args + ["--join", "--out", self.tmp / "h3"]))
        self.assertEqual(code, 0, out)
        self.assertIn("== 1A+1B+1C", out)
        text = (self.tmp / "h3" / "1A+1B+1C.txt").read_text(encoding="utf-8")
        head, shot2 = text.split("[Shot 2]", 1)
        self.assertIn("storm-lashed cliff path", head)
        self.assertIn("the camera cuts to the round lamp room", shot2.lower())

    def test_compile_rejects_unsupported_format(self):
        proj = self.tmp / "p"
        shutil.copytree(EXAMPLE, proj)
        edit(proj / "bibles/style.json", '"aspect_ratio": "16:9"', '"aspect_ratio": "4:3"')
        code, out = run("compile", proj, "--model", "veo")
        self.assertNotEqual(code, 0)
        self.assertIn("aspect 4:3 not offered", out)

    def test_compile_adds_the_faced_wall(self):
        proj = self.tmp / "p"
        shutil.copytree(EXAMPLE, proj)
        edit(proj / "bibles/locations.json", '"props": ["brass lens", "workbench"]',
             '"props": ["brass lens", "workbench"], "walls": {"stairs": "an iron spiral staircase going down through a hatch in the floor"}')
        edit(proj / "cards/1B.json", '"side": "A"', '"side": "A", "faces": "stairs"')
        code, out = run("cards", "validate", proj)
        self.assertEqual(code, 0, out)
        code, out = run("compile", proj, "--model", "veo", "--out", self.tmp / "out")
        self.assertEqual(code, 0, out)
        self.assertIn("An iron spiral staircase going down", (self.tmp / "out/1B.txt").read_text(encoding="utf-8"))
        self.assertNotIn("spiral staircase", (self.tmp / "out/1A.txt").read_text(encoding="utf-8"))

    def test_unknown_wall_is_an_error(self):
        proj = self.tmp / "p"
        shutil.copytree(EXAMPLE, proj)
        edit(proj / "cards/1B.json", '"side": "A"', '"side": "A", "faces": "north"')
        code, out = run("continuity", "diff", proj)
        self.assertNotEqual(code, 0)
        self.assertIn("WALL", out)

    def test_wall_names_are_checked(self):
        proj = self.tmp / "p"
        shutil.copytree(EXAMPLE, proj)
        edit(proj / "bibles/locations.json", '"props": ["brass lens", "workbench"]',
             '"props": ["brass lens", "workbench"], "walls": {"North Wall": "rain-streaked windows over the dark sea"}')
        code, out = run("cards", "validate", proj)
        self.assertNotEqual(code, 0)
        self.assertIn("North Wall", out)

    def test_unknown_model(self):
        code, out = run("compile", EXAMPLE, "--model", "nosuchmodel")
        self.assertEqual(code, 1)
        self.assertIn("no model card", out)


class TestProps(Base):
    """Prop sheets as refs, prop states and featured props (pre-production gaps, 2026-10-09)."""

    def project(self):
        proj = self.tmp / "p"
        shutil.copytree(EXAMPLE, proj)
        props = json.loads((proj / "bibles/props.json").read_text(encoding="utf-8"))
        props["props"][0]["refs"] = ["refs/matchbox_3q.png", "refs/matchbox_hand.png"]
        props["props"][0]["states"] = [{"name": "open", "description": "the same small dented tin matchbox, lid flipped open, three matches left inside",
                                        "refs": ["refs/matchbox_open.png"]}]
        props["props"].append({"name": "brass lens", "description": "a huge dark brass-and-glass Fresnel lens taller than a man, ringed glass prisms",
                               "refs": ["refs/lens.png"]})
        lib.write_text(proj / "bibles/props.json", json.dumps(props, indent=2))
        edit(proj / "bibles/locations.json", '"props":', '"refs": ["refs/lamp_room.png"], "props":')
        edit(proj / "cards/1A.json", '"holding": "tin matchbox",', '"holding": "tin matchbox", "holding_state": "open",')
        edit(proj / "cards/1A.json", '"action":', '"props": [{"name": "brass lens", "where": "behind them"}], "action":')
        return proj

    def test_states_featured_props_and_set_refs_compile(self):
        proj = self.project()
        code, out = run("compile", proj, "--model", "minimax-h3", "--card", "1A", "--resolution", "480p", "--out", self.tmp / "h3")
        self.assertEqual(code, 0, out)
        text = (self.tmp / "h3" / "1A.txt").read_text(encoding="utf-8")
        params = json.loads((self.tmp / "h3" / "1A.params.json").read_text(encoding="utf-8"))
        refs = params["refs"]
        # characters first, then the state's sheet (not the plain prop's), the featured prop, the set
        self.assertNotIn("refs/matchbox_3q.png", refs)
        self.assertLess(refs.index("refs/matchbox_open.png"), refs.index("refs/lens.png"))
        self.assertEqual(refs[-1], "refs/lamp_room.png")
        n = refs.index("refs/matchbox_open.png") + 1
        self.assertIn("lid flipped open, three matches left inside <Picture %d>" % n, text)
        self.assertIn("ringed glass prisms <Picture %d>, behind them." % (refs.index("refs/lens.png") + 1), text)
        # the set's sheet is named where the set is described, or the model has no word to tie it to
        self.assertIn("<Picture %d>" % len(refs), text)
        self.assertEqual(text.count("<Picture %d>" % len(refs)), 1)

    def test_unknown_state_is_a_continuity_error(self):
        proj = self.project()
        edit(proj / "cards/1A.json", '"holding_state": "open"', '"holding_state": "melted"')
        code, out = run("continuity", "diff", proj)
        self.assertIn("state 'melted'", out)
        self.assertNotEqual(code, 0, out)


@unittest.skipUnless(shutil.which("ffmpeg"), "ffmpeg not on PATH")
class TestPost(Base):
    """cine_post.py: animatic and grade (pre-production gaps, 2026-10-09)."""
    POST = REPO / "shared" / "lib" / "cine_post.py"

    def ffmpeg(self, *args):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + [str(a) for a in args], check=True)

    def test_animatic_times_the_cards(self):
        stills = self.tmp / "stills"
        stills.mkdir()
        self.ffmpeg("-f", "lavfi", "-i", "testsrc2=s=640x360", "-frames:v", "1", stills / "1A.png")
        out = self.tmp / "anim.mp4"
        code, text = run("animatic", EXAMPLE, "--stills", stills, "--out", out, "--size", "320x180", script=self.POST)
        self.assertEqual(code, 0, text)
        self.assertIn("no still for 1B, 1C", text)
        dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)],
                             capture_output=True, text=True).stdout
        self.assertAlmostEqual(float(dur), 14.0, delta=0.1)
        sheet = out.with_suffix(".timing.md").read_text(encoding="utf-8")
        self.assertIn("| 1B | 00:06.000 | 00:10.000 | 4 |", sheet)

    def test_grade_match_moves_toward_the_ref_and_hits_a_luma_target(self):
        ref, dark = self.tmp / "ref.png", self.tmp / "dark.mp4"
        self.ffmpeg("-f", "lavfi", "-i", "testsrc2=s=320x180", "-frames:v", "1", ref)
        self.ffmpeg("-f", "lavfi", "-i", "testsrc2=s=320x180:d=1,eq=brightness=-0.2:saturation=0.5", dark)
        code, text = run("grade", "match", dark, "--ref", ref, "--luma", "60", "--apply", self.tmp / "out", script=self.POST)
        self.assertEqual(code, 0, text)
        cube = (self.tmp / "grade" / "dark.cube").read_text(encoding="utf-8").splitlines()
        self.assertIn("LUT_3D_SIZE 17", cube)
        self.assertEqual(len(cube), 4 + 17 ** 3)
        report = json.loads((self.tmp / "grade" / "grade.json").read_text(encoding="utf-8"))
        self.assertAlmostEqual(report["files"][str(dark)]["after_luma"], 60, delta=4)


class TestFight(Base):
    """cine_fight.py: fight plans replayed and held against the cards (fight plans, 2026-10-15)."""
    FIGHT = REPO / "shared" / "lib" / "cine_fight.py"

    def plan(self, **over):
        p = {"id": "match", "scene": "1", "question": "Will Tomas get the last match?", "ending": "Tomas holds the match to his chest.",
             "bpm": 120,
             "fighters": [{"id": "maren", "goal": "keep the match", "side": "frame-left", "right": "tin matchbox"},
                          {"id": "tomas", "goal": "get the match", "side": "frame-right"}],
             "phrases": [{"id": "P1", "ahead": "maren", "why": "she has the only light", "pause_secs": 2},
                         {"id": "P2", "ahead": "tomas", "margin": 2, "why": "she gives it up"}],
             "exchanges": [
                 {"n": 1, "phrase": "P1", "lead": "maren", "with": "tin matchbox", "move": "thumbs the box open", "answer": "Tomas watches",
                  "result": "none", "secs": 3, "card": "1A", "changes": [{"who": "maren", "right": "single match"}]},
                 {"n": 2, "phrase": "P1", "lead": "maren", "with": "single match", "move": "holds the match out", "answer": "Tomas reaches",
                  "result": "none", "secs": 2, "card": "1B"},
                 {"n": 3, "phrase": "P2", "lead": "tomas", "move": "takes the match", "answer": "Maren lets go", "result": "disarm",
                  "card": "1C", "changes": [{"who": "tomas", "right": "single match"}]}]}
        p.update(over)
        f = self.tmp / "match.json"
        f.write_text(json.dumps(p), encoding="utf-8")
        return f, p

    def test_clean_plan_against_the_example_cards(self):
        f, _ = self.plan()
        code, text = run("check", f, "--project", EXAMPLE, script=self.FIGHT)
        self.assertEqual(code, 0, text)
        self.assertIn("0 errors, 0 warnings", text)

    def test_weapon_after_it_changed_hands_and_one_sided_fight(self):
        f, p = self.plan()
        p["exchanges"].append({"n": 4, "phrase": "P2", "lead": "maren", "with": "single match", "move": "snatches at it", "answer": "Tomas pulls away", "result": "miss"})
        p["phrases"] = [dict(x, ahead="maren") for x in p["phrases"]] + [{"id": "P3", "ahead": "maren", "why": "she still wins here"}]
        f.write_text(json.dumps(p), encoding="utf-8")
        code, text = run("check", f, script=self.FIGHT)
        self.assertEqual(code, 1, text)
        self.assertIn("WEAPON (move 4): maren moves with the single match, but holds nothing", text)
        self.assertIn("ONE-SIDED", text)

    def test_cards_held_to_the_plan(self):
        f, p = self.plan()
        p["fighters"][0]["marks"] = ["soot on her left cheek"]
        p["exchanges"][2]["card"] = "1A"
        f.write_text(json.dumps(p), encoding="utf-8")
        code, text = run("check", f, "--project", EXAMPLE, script=self.FIGHT)
        self.assertIn("MARK (move 1): card 1A: copy maren's mark 'soot on her left cheek'", text)
        self.assertIn("CARD (move 3): card 1A comes before the previous exchange's card in the cut", text)
        p["exchanges"][1]["card"] = "1A"
        p["exchanges"][2]["card"] = "1A"
        f.write_text(json.dumps(p), encoding="utf-8")
        code, text = run("check", f, "--project", EXAMPLE, script=self.FIGHT)
        self.assertIn("ONE-EXCHANGE", text)
        self.assertIn("TIME", text)

    def test_sheet_grid_and_csv(self):
        f, _ = self.plan()
        code, text = run("sheet", f, "--out", self.tmp / "out", script=self.FIGHT)
        self.assertEqual(code, 0, text)
        sheet = (self.tmp / "out" / "match.sheet.md").read_text(encoding="utf-8")
        self.assertIn("| 3 | 7.0 (4.3) | Maren lets go | <- | takes the match | disarm | 1C | added |", sheet)
        rows = (self.tmp / "out" / "match.csv").read_text(encoding="utf-8").splitlines()
        self.assertEqual(rows[0], "n,time_s,phrase,ahead_score,result,lead,card")
        self.assertEqual(rows[3], "3,7.0,P2,-2,disarm,tomas,1C")
        code, text = run("sheet", f, "--project", EXAMPLE, "--out", self.tmp / "cut", script=self.FIGHT)
        self.assertTrue((self.tmp / "cut" / "match.csv").read_text(encoding="utf-8").splitlines()[3].startswith("3,10.0,"))


class TestRefStages(Base):
    """Character refs keyed like wardrobe: a wound or costume stage gets its own sheet (design L-005, 2026-10-16)."""

    def project(self, refs, stage_1a=None, stage_1b=None, name="p"):
        proj = self.tmp / name
        shutil.copytree(EXAMPLE, proj)
        ch = json.loads((proj / "bibles/characters.json").read_text(encoding="utf-8"))
        ch["characters"][0]["refs"] = refs
        lib.write_text(proj / "bibles/characters.json", json.dumps(ch, indent=2))
        for cid, stage in (("1A", stage_1a), ("1B", stage_1b)):
            if stage:
                edit(proj / "cards" / ("%s.json" % cid), '"id": "maren",', '"id": "maren", "refs_stage": "%s",' % stage)
        return proj

    def compiled_refs(self, proj, card):
        out = self.tmp / ("h3_" + card)
        code, log = run("compile", proj, "--model", "minimax-h3", "--card", card, "--resolution", "480p", "--out", out)
        self.assertEqual(code, 0, log)
        return (json.loads((out / ("%s.params.json" % card)).read_text(encoding="utf-8"))["refs"],
                (out / ("%s.txt" % card)).read_text(encoding="utf-8"))

    def levels(self, proj):
        return sorted({(i["level"], i["card"]) for i in lib.continuity_diff(lib.Project(proj)) if i["code"] == "REFS"})

    def test_stage_picks_its_sheet_and_only_its_sheet(self):
        proj = self.project({"default": ["refs/maren.png"], "wet": ["refs/maren_wet.png"]}, stage_1b="wet")
        refs, _ = self.compiled_refs(proj, "1A")
        self.assertIn("refs/maren.png", refs)
        self.assertNotIn("refs/maren_wet.png", refs)
        refs, text = self.compiled_refs(proj, "1B")
        self.assertEqual(refs, ["refs/maren_wet.png"])
        self.assertIn("<Picture 1>", text)
        code, out = run("cards", "validate", proj)
        self.assertEqual(code, 0, out)
        self.assertEqual(self.levels(proj), [])

    def test_tags_follow_the_reference_order(self):
        proj = self.project({"default": ["refs/maren.png", "refs/maren_face.png"],
                             "wet": ["refs/maren_wet.png", "refs/maren_face.png"]}, stage_1b="wet")
        refs, text = self.compiled_refs(proj, "1B")
        self.assertEqual(refs, ["refs/maren_wet.png", "refs/maren_face.png"])
        self.assertIn("<Picture 1> <Picture 2>", text)

    def test_scene_id_is_the_fallback_key(self):
        proj = self.project({"default": ["refs/maren.png"], "1": ["refs/maren_s1.png"]})
        refs, _ = self.compiled_refs(proj, "1B")
        self.assertEqual(refs, ["refs/maren_s1.png"])

    def test_unknown_stage_is_an_error_and_going_back_a_warning(self):
        proj = self.project({"default": ["refs/maren.png"], "wet": ["refs/maren_wet.png"]}, stage_1b="dry")
        self.assertEqual(self.levels(proj), [("error", "1B")])
        proj = self.project({"default": ["refs/maren.png"], "wet": ["refs/maren_wet.png"]}, stage_1a="wet", name="p2")
        self.assertEqual(self.levels(proj), [("warning", "1B")])

    def test_staged_refs_need_a_default(self):
        proj = self.project({"wet": ["refs/maren_wet.png"]})
        code, out = run("cards", "validate", proj)
        self.assertNotEqual(code, 0, out)
        self.assertIn("missing required 'default'", out)

    def test_film_json_sends_stages_per_shot(self):
        proj = self.project({"default": ["refs/maren.png"], "wet": ["refs/maren_wet.png"]}, stage_1b="wet")
        film = lib.film_json(lib.Project(proj))
        self.assertNotIn("refs/maren_wet.png", film.get("refs", []))
        shots = {s["name"]: s.get("refs", []) for s in film["shots"]}
        self.assertEqual(shots["shot_1A"], ["refs/maren.png"])
        self.assertEqual(shots["shot_1B"], ["refs/maren_wet.png"])


class TestContinuity(Base):
    def test_clean(self):
        code, out = run("continuity", "diff", EXAMPLE)
        self.assertEqual(code, 0, out)
        self.assertIn("0 errors, 0 warnings", out)

    def test_planted_error_caught(self):
        code, out = run("continuity", "diff", EXAMPLE, "--with", EXAMPLE / "planted" / "1C.json")
        self.assertEqual(code, 1)
        self.assertIn("ERROR 1C AXIS", out)
        self.assertIn("ERROR 1C EYELINE", out)

    def test_malformed_bible_says_what_to_fix(self):
        p = self.tmp / "p"
        shutil.copytree(EXAMPLE, p)
        lib.write_text(p / "bibles" / "characters.json", json.dumps({"characters": {"maren": {"name": "Maren"}}}))
        code, out = run("continuity", "diff", p)
        self.assertEqual(code, 1, out)
        self.assertIn("bibles/characters.json: want", out)
        self.assertNotIn("Traceback", out)

    def project(self):
        return lib.Project(EXAMPLE)

    def codes(self, p):
        return sorted({(i["card"], i["code"]) for i in lib.continuity_diff(p) if i["level"] == "error"})

    def test_wardrobe_identity_prop_time(self):
        p = self.project()
        p.cards[1]["cast"][0]["wardrobe"] = "a red raincoat"
        p.cards[1]["cast"][0]["holding"] = "tin matchbox"
        p.cards[2]["cast"][0]["identity"] = p.cards[2]["cast"][0]["identity"].replace("twelve", "ten")
        p.cards[2]["time_of_day"] = "day"
        self.assertEqual(self.codes(p), [("1B", "PROP"), ("1B", "WARDROBE"), ("1C", "IDENTITY"), ("1C", "TIME")])

    def test_thirty_degree_rule(self):
        p = self.project()
        twin = json.loads(json.dumps(p.cards[1]))
        twin.update({"id": "1D", "order": 4})
        twin["camera"]["azimuth_deg"] = 60
        p.cards = [p.cards[0], p.cards[1], twin]
        self.assertIn(("1D", "30-DEGREE"), self.codes(p))
        twin["camera"]["size"] = "ECU"  # MCU -> ECU is two steps: legal
        self.assertNotIn(("1D", "30-DEGREE"), self.codes(p))

    def test_positions_and_travel(self):
        p = self.project()
        p.cards[0]["cast"][0]["position"], p.cards[0]["cast"][1]["position"] = "frame-right", "frame-left"
        p.scene_map["1"]["axis"]["travel"] = {"tomas": "left-to-right"}
        p.cards[2]["cast"][0]["travel"] = "right-to-left"
        self.assertEqual(self.codes(p), [("1A", "POSITION"), ("1C", "DIRECTION")])

    def test_crossing_with_reason_flips_expectations(self):
        p = self.project()
        cam = p.cards[2]["camera"]
        cam.update({"side": "B", "crosses_axis": True, "cross_reason": "subject-crosses: Tomas crosses the line on screen"})
        self.assertEqual(self.codes(p), [("1C", "EYELINE")], "on side B the eyeline must flip to frame-right")
        p.cards[2]["cast"][0]["eyeline"] = "frame-right"
        self.assertEqual(self.codes(p), [])
        self.assertNotIn(("1C", "AXIS"), self.warns(p))
        cam["cross_reason"] = "it looks cool"
        self.assertIn(("1C", "AXIS"), self.warns(p), "a reason that names no legal way to cross")

    # ---------- cutting and continuity (books track 2) ----------

    def warns(self, p):
        return sorted({(i["card"], i["code"]) for i in lib.continuity_diff(p) if i["level"] == "warning"})

    def twin(self, p, src, cid, order):
        c = json.loads(json.dumps(p.cards[src]))
        c.update({"id": cid, "order": order})
        p.cards.append(c)
        return c

    def test_next_card_starts_from_position_end(self):
        p = self.project()
        d = self.twin(p, 0, "1D", 4)
        d["camera"]["azimuth_deg"] = 30
        d["cast"][1]["holding"] = "single match"  # Tomas took it in 1C
        self.assertEqual(self.codes(p), [])
        p.cards[0]["cast"][0]["position_end"] = "frame-right"  # Maren walks past Tomas in 1A
        p.cards[0]["cast"][1]["position_end"] = "frame-left"
        self.assertIn(("1D", "POSITION"), self.codes(p), "1D still uses the opening block")
        d["cast"][0]["position"], d["cast"][1]["position"] = "frame-right", "frame-left"
        self.assertNotIn(("1D", "POSITION"), self.codes(p))

    def test_exit_and_entry_sides(self):
        p = self.project()
        p.cards[0]["cast"][0]["exits"] = "frame-right"
        p.cards[1]["cast"][0]["enters"] = "frame-right"
        self.assertIn(("1B", "EXIT-ENTRY"), self.codes(p))
        p.cards[1]["cast"][0]["enters"] = "frame-left"
        self.assertNotIn(("1B", "EXIT-ENTRY"), self.codes(p))

    def test_watcher_turns_against_the_travel(self):
        p = self.project()
        p.scene_map["1"]["axis"]["travel"] = {"tomas": "left-to-right"}
        m = p.cards[1]["cast"][0]  # Maren looks frame-right at Tomas
        m["eyeline_end"] = "frame-left"
        self.assertNotIn(("1B", "LOOK-TRACK"), self.warns(p), "right to left follows a left-to-right walk")
        m["eyeline"], m["eyeline_end"] = "frame-left", "frame-right"
        self.assertIn(("1B", "LOOK-TRACK"), self.warns(p))

    def test_middle_person_keeps_one_side(self):
        p = self.project()
        p.chars["nell"] = dict(p.chars["tomas"], name="Nell")
        p.scene_map["1"]["axis"]["positions"] = {"nell": "frame-left", "maren": "center", "tomas": "frame-right"}
        nell = dict(p.cards[0]["cast"][1], id="nell", position="frame-left", looks_at="maren", eyeline="frame-right")
        p.cards[0]["cast"] = [nell, dict(p.cards[0]["cast"][0], position="frame-right")]
        d = self.twin(p, 0, "1D", 4)
        d["cast"] = [dict(p.cards[0]["cast"][1], position="frame-left"), dict(p.cards[2]["cast"][0], position="frame-right", eyeline="frame-left")]
        p.cards = [p.cards[0], d]
        self.assertIn(("1D", "MIDDLE-SWAP"), self.warns(p))
        d["cast"][0]["position"] = "frame-right"
        self.assertNotIn(("1D", "MIDDLE-SWAP"), self.warns(p))

    def test_pov_role_protection_and_establish(self):
        p = self.project()
        p.cards[2]["pov"] = "nobody"
        self.assertIn(("1C", "POV"), self.codes(p))
        p.cards[2]["pov"] = "tomas"
        p.cards[2]["camera"]["framing"] = "pov"
        self.assertIn(("1C", "POV"), self.warns(p), "1B before it shows Maren looking, not Tomas")
        p.cards[2]["pov"] = "maren"
        self.assertNotIn(("1C", "POV"), self.warns(p))
        d = self.twin(p, 1, "1D", 4)
        d.update({"role": "protection", "protects": "9Z"})
        self.assertIn(("1D", "ROLE"), self.codes(p))
        d["protects"] = "1B"
        self.assertNotIn(("1D", "ROLE"), self.codes(p))
        e = self.twin(p, 2, "1E", 5)
        e["camera"]["framing"] = "insert"
        e["cast"] = []
        e["props"] = [{"name": "brass lantern key"}]
        self.assertIn(("1E", "ESTABLISH"), self.warns(p))
        e["props"] = [{"name": "tin matchbox"}]  # Maren held it in 1A
        self.assertNotIn(("1E", "ESTABLISH"), self.warns(p))

    def test_compile_says_entries_end_states_and_held_moves(self):
        p, prof, _ = compile_one(EXAMPLE, "minimax-h3", "1B")
        c = json.loads(json.dumps(p.cards[1]))
        c["cast"][0].update({"enters": "frame-left", "position_end": "center", "eyeline_end": "down"})
        c["camera"]["settle"] = True
        text = lib.compile_cards(p, [c], prof, False, "480p")[0][1]
        self.assertIn("Maren enters the frame on the left.", text)
        self.assertIn("Maren ends in the center of the frame.", text)
        self.assertIn("Maren turns, looking down.", text)
        self.assertIn("The camera holds, then pushes in with small amplitude at slow speed, then holds.", text)
        _, vprof, _ = compile_one(EXAMPLE, "veo", "1B")
        self.assertIn("slow dolly in that starts and ends on a held frame", lib.compile_cards(p, [c], vprof)[0][1])


class TestBudgetZip(Base):
    def test_budget_not_red(self):
        # PLAN 6: CI fails at red; a yellow row is reported to Mark, not failed
        code, out = run("budget")
        self.assertEqual(code, 0, out)
        self.assertNotIn("budget: RED", out)

    def test_model_cards_have_their_own_row(self):
        spec = importlib.util.spec_from_file_location("cine_cli", CLI)
        cli = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cli)
        rows = cli.measure(REPO)
        self.assertIn("cinewright-genvideo/references/", rows["card_tokens"][1])
        worst = REPO / rows["entry_tokens"][1]
        self.assertNotIn("model", lib.parse_frontmatter(lib.read_text(worst))[0], "model cards must not count as entries")

    def test_budget_status_thresholds(self):
        spec = importlib.util.spec_from_file_location("cine_cli", CLI)
        cli = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cli)
        self.assertEqual([cli.status(v, 80, 120) for v in (80, 81, 120, 121)], ["green", "yellow", "yellow", "red"])

    def test_budget_red_fails(self):
        root = copy_repo(self.tmp)
        skill = root / "plugins/cinewright/skills/cinewright/SKILL.md"
        lib.write_text(skill, lib.read_text(skill) + "\n".join("- filler line %d" % i for i in range(80)) + "\n")
        code, out = run("--root", root, "budget")
        self.assertEqual(code, 2, out)
        self.assertIn("budget: RED", out)

    def test_zip_has_skill_folder_on_top(self):
        code, out = run("zip", "cinewright-continuity", "--out", self.tmp)
        self.assertEqual(code, 0, out)
        with zipfile.ZipFile(self.tmp / "cinewright-continuity.zip") as z:
            names = z.namelist()
        self.assertEqual({n.split("/")[0] for n in names}, {"cinewright-continuity"})
        self.assertIn("cinewright-continuity/SKILL.md", names)
        self.assertIn("cinewright-continuity/scripts/cine.py", names)


class TestVocabularyAgreement(unittest.TestCase):
    def test_lib_tokens_match_schema(self):
        cam = json.loads((REPO / "shared/schemas/shot-card.schema.json").read_text(encoding="utf-8"))["properties"]["camera"]["properties"]
        self.assertEqual(lib.SIZES, cam["size"]["enum"])
        self.assertEqual(sorted(lib.MOVE_WORDS), sorted(cam["move"]["enum"]))
        self.assertEqual(sorted(lib.ANGLE_WORDS), sorted(cam["angle"]["enum"]))

    def test_vocab_entries_list_every_schema_token(self):
        cam = json.loads((REPO / "shared/schemas/shot-card.schema.json").read_text(encoding="utf-8"))["properties"]["camera"]["properties"]
        sizes = (REPO / "shared/vocab/shot-sizes.md").read_text(encoding="utf-8")
        moves = (REPO / "shared/vocab/camera-moves.md").read_text(encoding="utf-8")
        for t in cam["size"]["enum"]:
            self.assertIn("`%s`" % t, sizes)
        for t in cam["move"]["enum"]:
            self.assertIn("`%s`" % t, moves)


if __name__ == "__main__":
    unittest.main()


# ---------- S2: one test per model card, checked against the vendor's own example ----------

# Short excerpts of each vendor's published example prompt, kept only to prove the shape rules below
# also hold for the vendor's text. Sources: the model card's `sources`.
VENDOR = {
    "veo": "the man in the red hat says: Where is the rabbit?",  # Vertex prompt guide
    "veo-seq": "[00:00-00:02] Medium shot from behind a young female explorer",  # Cloud blog, Veo 3.1 guide
    "omni": "Continuous, unbroken handheld shot of a fluffy tabby cat sitting on a sunny windowsill. Sound design: Gentle breeze, distant bird chirps.",
    "omni-seq": "[0-3s] A person is walking",
    "kling": "Mom (softly, in a surprised tone): Wow, I didn't expect this plot at all.",
    "seedance": "Shot 2: Girl @Image 1 pushes the door open and enters the dormitory. One of them smiles and asks {How did the exam go? Did you pass?}.",
    "runway": "Medium shot of a cowboy perched on a horse in a dusty environment. The horse rears violently, its body twisting, causing the cowboy to lose his seat and begin to fall off to the left.",
    "luma": "A golden retriever running through a wheat field, ears flapping in the wind, dust particles catching golden hour sunlight, camera tracking alongside.",
    "h3": ("integrated_multimodal_description: [Shot 1] Live-action, cinematic, a medium-wide shot frames a baker opening the shutters of a small street bakery before sunrise. "
           "The camera pushes in with small amplitude at slow speed as the middle-aged baker with a calm, slightly raspy voice (S1) places a fresh loaf on the wooden counter and says: <d>[English] First batch of the morning.</d> "
           "[Shot 2] At 00:05.000, the camera cuts to a close-up of steam rising from the sliced bread while the baker's final words carry over from the previous shot."
           "\n\noverall_soundscape: Wooden shutters scrape open over a quiet street as trays clink softly inside the bakery."
           "\n\nnon_diegetic_music: A soft acoustic-guitar pattern at a moderate tempo, joined by sparse upright-bass notes and a gentle fade at the end."),
    "wan": "Two anthropomorphic cats in comfy boxing gear and bright gloves fight intensely on a spotlighted stage.",
    "ltx": ("A wide shot frames a rainy city intersection at dusk, neon signs reflecting on wet asphalt. She speaks quietly to herself, \"He's late.\" "
            "A hard cut jumps to a low-angle shot of a man's scuffed boots stepping into a puddle at the curb; the music drops to a low drone."),
}
MODELS = ["veo", "omni", "kling", "seedance", "runway", "luma", "minimax-h3", "wan", "ltx2"]
DRAFT_RES = {"minimax-h3": "480p"}  # the example's 720p is not on H3's size ladder


def model_project(tmp, refs=False):
    proj = tmp / "proj"
    shutil.copytree(EXAMPLE, proj)
    if refs:
        edit(proj / "bibles/characters.json", '"voice": "low, dry, unhurried",', '"voice": "low, dry, unhurried",\n      "refs": ["refs/maren-turnaround.png"],')
    return proj


def compile_one(proj, model, card=None, sequence=False):
    p = lib.Project(proj)
    _, _, prof = lib.find_model_card(repo_ctx(), model)
    cards = [c for c in p.cards if card is None or c["id"] == card]
    return p, prof, lib.compile_cards(p, cards, prof, sequence, DRAFT_RES.get(model))


def repo_ctx():
    dirs = [s / "references" for s in sorted(p.parent for p in SKILLS.glob("*/SKILL.md"))]
    return lib.Context(dirs, dirs, REPO / "shared" / "schemas")


class TestModelCards(Base):
    def both(self, pattern, vendor_key, text, flags=0):
        """The shape rule must hold for the vendor's own example and for our output."""
        self.assertRegex(VENDOR[vendor_key], re.compile(pattern, flags), "rule does not fit the vendor example")
        self.assertRegex(text, re.compile(pattern, flags))

    def test_every_model_compiles_and_keeps_identity(self):
        bible = {c["id"]: c["identity"] for c in json.loads((EXAMPLE / "bibles/characters.json").read_text(encoding="utf-8"))["characters"]}
        cards = {c["id"]: c for c in lib.Project(EXAMPLE).cards}
        for model in MODELS:
            _, prof, _ = compile_one(EXAMPLE, model, "1A")
            for seq in ([False, True] if "timestamp" in prof else [False]):
                _, _, res = compile_one(EXAMPLE, model, sequence=seq)
                for label, text, params, warnings, info in res:
                    for cid in label.split("+"):
                        for m in cards[cid]["cast"]:
                            self.assertIn(bible[m["id"]], text, (model, label, m["id"]))

    def test_identity_guard_fires_on_every_model(self):
        p = lib.Project(EXAMPLE)
        for model in MODELS:
            _, _, prof = lib.find_model_card(repo_ctx(), model)
            broken = dict(prof, order=[k for k in prof["order"] if k != "subject"])
            with self.assertRaises(SystemExit, msg=model) as cm:
                lib.compile_cards(p, [p.cards[1]], broken, False, DRAFT_RES.get(model))
            self.assertIn("identity of maren not verbatim", str(cm.exception))

    def test_veo(self):
        _, _, res = compile_one(EXAMPLE, "veo", "1B")
        self.both(r"\bsays( \w+)?: [A-Z][^\"]*\?|\bsays( \w+)?: [A-Z][^\"]+\.", "veo", res[0][1])
        _, _, res = compile_one(EXAMPLE, "veo", sequence=True)
        self.both(r"^\[[0-9]{2}:[0-9]{2}-[0-9]{2}:[0-9]{2}\] [A-Z]", "veo-seq", res[1][1], re.M)

    def test_omni(self):
        _, _, res = compile_one(EXAMPLE, "omni", "1B")
        label, text, params, warnings, info = res[0]
        self.assertTrue(text.startswith("In a single continuous shot."))
        self.both(r"Sound design: [A-Za-z]", "omni", text)
        self.assertNotIn("seed", params)
        self.assertEqual(info["est_usd"], 0.4)
        _, _, res = compile_one(EXAMPLE, "omni", sequence=True)
        self.assertEqual(res[0][0], "1A+1B", "10 s cap: 1A and 1B share a generation")
        self.both(r"^\[[0-9]+-[0-9]+s\] [A-Za-z]", "omni-seq", res[0][1], re.M)

    def test_kling(self):
        _, _, res = compile_one(EXAMPLE, "kling", "1B")
        text, params = res[0][1], res[0][2]
        self.both(r"\b[A-Z][a-z]+ \([^)]+\): [A-Z][^\"]", "kling", text)
        self.assertTrue(text.startswith("The round lamp room"), "setting first, as in the guide's examples")
        self.assertEqual(params["duration"], 4)
        _, _, res = compile_one(EXAMPLE, "kling", sequence=True)
        label, text, params, _, info = res[0]
        self.assertEqual(label, "1A+1B+1C")
        self.assertIn("Shot 2, ", text)
        self.assertEqual(sum(params["multi_shot"]), params["duration"])

    def test_seedance(self):
        proj = model_project(self.tmp, refs=True)
        _, _, res = compile_one(proj, "seedance", "1B")
        text, params = res[0][1], res[0][2]
        self.both(r"\b[A-Z][a-z]+ @Image \d", "seedance", text)
        self.both(r"\b(says|asks)( \w+)? \{[^}]+\}", "seedance", text)
        self.assertEqual(params["reference_images"], ["refs/maren-turnaround.png"])
        self.assertNotIn("seed", params)
        self.assertTrue(text.endswith("Avoid generating any text, subtitles or watermark."))
        _, _, res = compile_one(EXAMPLE, "seedance", sequence=True)
        self.both(r"^Shot \d: [A-Z]", "seedance", res[0][1], re.M)

    def test_runway(self):
        _, _, res = compile_one(EXAMPLE, "runway", "1B")
        text, params, warnings = res[0][1], res[0][2], res[0][3]
        self.both(r"^(Medium|Wide|Close|Extreme|Full)[ -]?\w* (shot|close-up)", "runway", text)
        self.assertLessEqual(len(text), 1000)
        self.assertEqual(params["ratio"], "1280:720")
        self.assertNotIn("Last one", text)
        self.assertTrue(any("no speech" in w for w in warnings))

    def test_luma(self):
        _, _, res = compile_one(EXAMPLE, "luma", "1B")
        text, params = res[0][1], res[0][2]
        self.both(r"^[A-Z][^.]*?\b(a|an)\b", "luma", text)  # subject first, not a camera term
        self.assertFalse(re.match(r"^(Medium|Wide|Close)", text))
        self.both(r"camera (tracking|dolly|pan)|dolly in|tracking", "luma", text)
        self.assertEqual(params["duration"], "5s")

    def test_minimax_h3_fifteen_seconds(self):
        card = (SKILLS / "cinewright-genvideo" / "references" / "minimax-h3.md").read_text(encoding="utf-8")
        prof = json.loads(next(x for x in card.splitlines() if x.startswith('{"model_id": "H3')))
        self.assertEqual(lib.plan_length(15, prof), (15.083, 362), "15 s plans the 362-frame maximum, not 345")

    def test_travel_only_from_the_card_and_no_double_article(self):
        proj = model_project(self.tmp)
        scenes = json.loads((proj / "bibles/scenes.json").read_text(encoding="utf-8"))
        scenes["scenes"][0]["axis"]["travel"] = {"maren": "left-to-right"}
        (proj / "bibles/scenes.json").write_text(json.dumps(scenes), encoding="utf-8")
        c = json.loads((proj / "cards/1A.json").read_text(encoding="utf-8"))
        c["cast"][0]["looks_at"] = "the tin matchbox"
        (proj / "cards/1A.json").write_text(json.dumps(c), encoding="utf-8")
        _, _, res = compile_one(proj, "veo", "1A")
        text = res[0][1]
        self.assertNotIn("Maren is moving", text, "a scene's travel is not stated on a card that does not travel")
        self.assertNotIn("the the", text)
        self.assertIn("at the tin matchbox", text)

    def test_minimax_h3(self):
        proj = model_project(self.tmp, refs=True)
        _, _, res = compile_one(proj, "minimax-h3", "1B")
        text, params = res[0][1], res[0][2]
        self.both(r"^integrated_multimodal_description: \[Shot 1\] ", "h3", text)
        self.both(r"\n\noverall_soundscape: [A-Z].*\n\nnon_diegetic_music: ", "h3", text, re.S)
        self.both(r"The camera \w+ in with small amplitude at slow speed", "h3", text)
        self.both(r"\(S1\)[^:<]* says[^:]*: <d>\[English\] [^<]+</d>", "h3", text)
        self.assertIn("Maren <Picture 1>, a lean woman", text)
        self.assertEqual((params["width"] % 32, params["height"] % 32, (params["length"] - 5) % 17), (0, 0, 0))
        _, _, res = compile_one(EXAMPLE, "minimax-h3", sequence=True)
        label, text, params, _, _ = res[0]
        self.assertEqual(label, "1A+1B+1C")
        self.both(r"\[Shot 2\] At 00:\d\d\.\d{3}, the camera cuts to [a-z]", "h3", text)
        self.assertEqual(text.count("\n\n"), 2, "one description paragraph, then the two sound fields")

    def test_sequence_keeps_featured_props(self):
        proj = model_project(self.tmp)
        for cid, change in (("1B", {"props": [{"name": "single match", "where": "in her fingers"}]}),
                            ("1C", {"props": [{"name": "tin matchbox", "where": "on the sill"}],
                                    "sound": "rain on the glass, muffled wind"})):
            path = proj / "cards" / ("%s.json" % cid)
            c = json.loads(path.read_text(encoding="utf-8"))
            c.update(change)
            path.write_text(json.dumps(c), encoding="utf-8")
        _, _, res = compile_one(proj, "minimax-h3", sequence=True)
        text = res[0][1]
        self.assertIn("A small dented tin matchbox with a hinged lid, scratched silver, the size of a palm, on the sill.", text,
                      "a featured prop on a later card reaches its shot block")
        self.assertEqual(text.count("one long wooden kitchen match with a red head"), 1, "a held prop is said once")
        self.assertEqual(text.count("rain on the glass, muffled wind".capitalize()), 1, "a shared soundscape is said once")

    def test_wan(self):
        _, _, res = compile_one(EXAMPLE, "wan", "1B")
        text, params = res[0][1], res[0][2]
        self.both(r"^[A-Z0-9][^\[\]<>{}]*\.$", "wan", text)  # plain prose, no tags or brackets
        self.assertTrue(text.startswith("35mm film look"), "style first")
        self.assertEqual((params["frame_num"] % 4, params["width"] % 16, params["height"] % 16, params["fps"]), (1, 0, 0, 16))
        self.assertIn("字幕", params["negative_prompt"])
        _, _, res = compile_one(EXAMPLE, "wan", "1A")
        self.assertEqual(res[0][2]["frame_num"], 81, "a 6 s card stops at the 81-frame default")
        self.assertTrue(any("split the card" in w for w in res[0][3]))

    def test_ltx2(self):
        _, _, res = compile_one(EXAMPLE, "ltx2", "1B")
        text, params = res[0][1], res[0][2]
        self.both(r"\b[a-z]+, \"[^\"]+\"", "ltx", text)
        self.assertNotIn("\n", text)
        self.assertEqual((params["num_frames"] % 8, params["width"] % 32, params["height"] % 32), (1, 0, 0))
        _, _, res = compile_one(EXAMPLE, "ltx2", sequence=True)
        self.assertNotIn("\n", res[0][1])
        self.both(r"A hard cut jumps to [a-z]", "ltx", res[0][1])

    def test_status_and_claims_on_every_card(self):
        for model in MODELS:
            path, meta, prof = lib.find_model_card(repo_ctx(), model)
            self.assertEqual(meta["status"], "current", model)
            self.assertTrue(meta["volatile_claims"], model)
            self.assertEqual(meta["last_checked"], "2026-10-03", model)


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "ffmpeg not installed")
class TestQc(Base):
    def setUp(self):
        super().setUp()
        self.clip = self.tmp / "take.mp4"
        r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=size=320x180:rate=24:duration=4",
                            "-f", "lavfi", "-i", "sine=frequency=440:duration=4", "-shortest", "-c:v", "mpeg4", "-c:a", "aac",
                            str(self.clip)], capture_output=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.proj = model_project(self.tmp)

    def test_sheet(self):
        out = self.tmp / "s.png"
        code, text = run("qc", "sheet", self.clip, "--out", out)
        self.assertEqual(code, 0, text)
        self.assertIn("8 frames at 2 fps", text)
        self.assertGreater(out.stat().st_size, 1000)

    def test_spec_pass_and_fail(self):
        code, text = run("qc", "spec", self.clip, "--project", self.proj, "--card", "1B")
        self.assertEqual(code, 0, text)
        self.assertIn("0 failed", text)
        code, text = run("qc", "spec", self.clip, "--project", self.proj, "--card", "1A")
        self.assertEqual(code, 1, text)
        self.assertIn("card needs 6s", text)
        self.assertIn("spec-mismatch", text)
        long = self.tmp / "long.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=size=320x180:rate=24:duration=8",
                        "-f", "lavfi", "-i", "sine=frequency=440:duration=8", "-shortest", "-c:v", "mpeg4", "-c:a", "aac", str(long)], check=True)
        code, text = run("qc", "spec", long, "--project", self.proj, "--card", "1B+1C")
        self.assertEqual(code, 0, text)
        self.assertIn("for a 8s card", text)

    def test_measure_finds_the_planned_cut_and_dead_air(self):
        cut = self.tmp / "cut.mp4"
        r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=size=320x180:rate=24:duration=4",
                            "-f", "lavfi", "-i", "mandelbrot=size=320x180:rate=24", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono",
                            "-filter_complex", "[1:v]trim=duration=4,setpts=PTS-STARTPTS[b];[0:v][b]concat=n=2:v=1:a=0[v]",
                            "-map", "[v]", "-map", "2:a", "-t", "8", "-c:v", "mpeg4", "-c:a", "aac", str(cut)], capture_output=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        code, text = run("qc", "measure", cut, "--project", self.proj, "--card", "1B+1C")
        self.assertIn("cut-planned", text)
        self.assertIn("planned cut at 4.00s found", text)
        self.assertIn("dead-air", text)
        self.assertRegex(text, r"score \d+/100")
        out = self.tmp / "m.json"
        run("qc", "measure", self.clip, "--json", "--out", out)
        m = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(m["cuts"], [])
        self.assertEqual(m["shots"][0]["card"], "whole")

    def test_measure_warns_on_flicker_only(self):
        code, text = run("qc", "measure", self.clip)
        self.assertNotIn("flicker:", text.replace("flicker %", ""))
        self.assertNotRegex(text, r"WARN flicker")
        bad = self.tmp / "flicker.mp4"  # brightness up on every other frame: the take a re-render or deflicker fixes
        r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(self.clip), "-vf",
                            "eq=brightness='0.04*mod(n,2)':eval=frame", "-c:v", "mpeg4", "-q:v", "2", "-c:a", "copy", str(bad)],
                           capture_output=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        code, text = run("qc", "measure", bad)
        self.assertRegex(text, r"WARN\s+flicker\s+whole: brightness jumps \d+\.\d times a second")
        self.assertNotRegex(text, r"FAIL\s+flicker")

    def test_loud(self):
        code, text = run("qc", "loud", self.clip)
        self.assertEqual(code, 1, text)
        self.assertRegex(text, r"integrated -\d+\.\d LUFS")
        code, text = run("qc", "loud", self.clip, "--target", "-22", "--tolerance", "2")
        self.assertEqual(code, 0, text)

    def test_loud_preset(self):
        code, text = run("qc", "loud", self.clip, "--preset", "ebu-r128")
        self.assertEqual(code, 1, text)
        self.assertIn("preset ebu-r128", text)
        self.assertIn("target -23.0 +/- 0.2", text)
        self.assertIn("(max -1.0)", text)
        code, text = run("qc", "loud", self.clip, "--preset", "netflix")
        self.assertIn("approximate", text)
        self.assertIn("(max -2.0)", text)
        code, text = run("qc", "loud", self.clip)
        self.assertIn("target -18.0 +/- 2.0", text)
        self.assertIn("(max -2.0)", text)
        code, text = run("qc", "loud", self.clip, "--preset", "ebu-r128", "--target", "-22", "--tolerance", "2")
        self.assertEqual(code, 0, text)
        self.assertIn("target -22.0 +/- 2.0", text)

    def test_rubric_round_trip(self):
        code, text = run("qc", "rubric", self.proj, "--card", "1B", "--clip", self.clip)
        self.assertEqual(code, 0, text)
        path = self.proj / "qc" / "1B.rubric.json"
        rub = json.loads(path.read_text(encoding="utf-8"))
        ids = [i["id"] for i in rub["items"]]
        for want in ("identity:maren", "wardrobe:maren", "props:maren", "eyeline:maren", "camera", "end-state", "audio", "seam", "text"):
            self.assertIn(want, ids)
        self.assertNotIn("direction:maren", ids, "no travel on this card")
        for it in rub["items"]:
            self.assertTrue(it["codes"], "check %s has no failure code" % it["check"])
            it["verdict"] = "pass"
        lib.write_text(path, json.dumps(rub))
        code, text = run("qc", "rubric", "--read", path)
        self.assertEqual(code, 0, text)
        self.assertIn("PASS", text)
        for it in rub["items"]:
            if it["id"] == "identity:maren":
                it.update(verdict="fail", code="identity-drift", note="braid gone after 2 s")
            if it["id"] == "camera":
                it.update(verdict="fail", code="wrong-move", note="fast push")
            if it["id"] == "style":
                it.update(verdict="fail", code="look-drift")
        lib.write_text(path, json.dumps(rub))
        code, text = run("qc", "rubric", "--read", path)
        self.assertEqual(code, 1, text)
        self.assertIn("FAIL, 3 failed", text)
        self.assertLess(text.index("rung 1"), text.index("rung 7"))
        self.assertIn("--fix", text)
        rub["items"][0]["code"] = "loudness-off"
        lib.write_text(path, json.dumps(rub))
        code, text = run("qc", "rubric", "--read", path)
        self.assertEqual(code, 1)
        self.assertIn("does not belong", text)

    def test_rubric_carries_the_faced_wall(self):
        locs = json.loads((self.proj / "bibles" / "locations.json").read_text(encoding="utf-8"))
        locs["locations"][0]["walls"] = {"east": "facing a solid panelled wall under a gallery"}
        lib.write_text(self.proj / "bibles" / "locations.json", json.dumps(locs))
        card = json.loads((self.proj / "cards" / "1B.json").read_text(encoding="utf-8"))
        run("qc", "rubric", self.proj, "--card", "1B")
        rub = json.loads((self.proj / "qc" / "1B.rubric.json").read_text(encoding="utf-8"))
        self.assertEqual([i for i in rub["items"] if i["check"] == "set"], [])
        card["camera"]["faces"] = "east"
        lib.write_text(self.proj / "cards" / "1B.json", json.dumps(card))
        code, text = run("qc", "rubric", self.proj, "--card", "1B")
        self.assertEqual(code, 0, text)
        rub = json.loads((self.proj / "qc" / "1B.rubric.json").read_text(encoding="utf-8"))
        st = [i for i in rub["items"] if i["check"] == "set"]
        self.assertEqual(len(st), 1)
        self.assertIn("solid panelled wall under a gallery", st[0]["ask"])
        self.assertIn("set-drift", st[0]["codes"])

    def test_standing_claims_join_the_rubric(self):
        lib.write_text(self.proj / "qc" / "standing.json", json.dumps({"*": [
            {"id": "no-air-steps", "claim": "Nobody takes walking steps on the air.", "code": "air-steps", "why": "reviewer"}]}))
        code, text = run("qc", "rubric", self.proj, "--card", "1B")
        self.assertEqual(code, 0, text)
        path = self.proj / "qc" / "1B.rubric.json"
        rub = json.loads(path.read_text(encoding="utf-8"))
        st = [i for i in rub["items"] if i["id"] == "standing:no-air-steps"]
        self.assertEqual(len(st), 1)
        self.assertEqual((st[0]["check"], st[0]["codes"]), ("action", ["air-steps"]))
        for it in rub["items"]:
            it["verdict"] = "fail" if it["id"] == "standing:no-air-steps" else "pass"
        lib.write_text(path, json.dumps(rub))
        code, text = run("qc", "rubric", "--read", path)
        self.assertEqual(code, 1, text)
        self.assertIn("air-steps", text)
        lib.write_text(self.proj / "qc" / "standing.json", json.dumps({"*": [{"id": "x", "claim": "y", "code": "nope"}]}))
        code, text = run("qc", "rubric", self.proj, "--card", "1B")
        self.assertNotEqual(code, 0)
        self.assertIn("needs a failure code", text)

    def test_agree_stats(self):
        s = lib.agree_stats([("yes", "yes")] * 8 + [("no", "no")] * 1 + [("no", "yes")] * 1)
        self.assertEqual((s["n"], round(s["agree"], 2), round(s["kappa"], 2)), (10, 0.9, 0.62))
        self.assertEqual(s["yes"][:2], (8, 9))
        self.assertLess(s["yes"][2], 0.89)

    def test_judge_and_agree(self):
        import http.server, threading
        seen = {}

        class Fake(http.server.BaseHTTPRequestHandler):
            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                seen["prompt"], seen["images"] = body["prompt"], body["images"]
                ids = re.findall(r"^\[([^\]]+)\]", body["prompt"], re.M)
                reply = {"seen": ["a", "b", "c", "d"], "verdicts": [{"id": i, "v": "yes" if k % 2 == 0 else "no", "why": "w"}
                                                                      for k, i in enumerate(ids)]}
                out = json.dumps({"response": json.dumps(reply)}).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(out)

            def log_message(self, *a):
                pass

        srv = http.server.HTTPServer(("127.0.0.1", 0), Fake)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        self.addCleanup(srv.server_close)
        self.addCleanup(srv.shutdown)
        run("qc", "rubric", self.proj, "--card", "1B", "--clip", self.clip)
        path = self.proj / "qc" / "1B.rubric.json"
        code, text = run("qc", "judge", path, "--host", "http://127.0.0.1:%d" % srv.server_port)
        self.assertEqual(code, 0, text)
        self.assertIn("[action#1] Maren slowly stretches", seen["prompt"])
        self.assertNotIn("Does the action happen", seen["prompt"], "the card's action goes as clause claims, not one question")
        self.assertIn("describe exactly what you see", seen["prompt"])
        self.assertEqual(len(seen["images"]), 1)
        rub = json.loads(path.read_text(encoding="utf-8"))
        judged = [i for i in rub["items"] if "vlm" in i]
        self.assertTrue(judged and all(i["look"] == "sheet" for i in judged))
        for it in rub["items"]:
            it["verdict"] = "pass"
        lib.write_text(path, json.dumps(rub))
        code, text = run("qc", "agree", self.proj)
        self.assertEqual(code, 0, text)
        self.assertIn("prompt %s" % lib.JUDGE_VERSION, text)
        self.assertIn("its yes right", text)

    def test_every_check_has_codes_and_every_code_a_check(self):
        codes = lib.taxonomy(repo_ctx())
        self.assertGreaterEqual(len(codes), 20)
        self.assertEqual(set(x["check"] for x in codes.values()), set(lib.CHECKS))
        for c, x in codes.items():
            self.assertIn(x["rung"], range(1, 9), c)

    def test_takes_log_and_lastframe(self):
        code, text = run("compile", self.proj, "--model", "veo", "--out", self.proj / "compiled" / "veo")
        self.assertEqual(code, 0, text)
        for i in range(3):
            code, text = run("takes", "log", self.proj, "--card", "1B", "--model", "veo", "--verdict", "fail",
                             "--fix", "identity-drift", "--file", self.clip, "--change", "seed 103" if i else "first take")
            self.assertEqual(code, 0, text)
        self.assertIn("three strikes", text)
        rec = json.loads((self.proj / "takes" / "1B-3.json").read_text(encoding="utf-8"))
        self.assertEqual(rec["model_id"], "veo-3.1-generate-001")
        self.assertEqual(len(rec["prompt_sha256"]), 64)
        code, text = run("takes", "log", self.proj, "--card", "1B", "--model", "veo", "--verdict", "fail", "--fix", "nonsense")
        self.assertNotEqual(code, 0)
        png = self.tmp / "last.png"
        code, text = run("takes", "lastframe", self.clip, "--out", png, "--take", self.proj / "takes" / "1B-3.json",
                         "--observed", "match held out toward frame right")
        self.assertEqual(code, 0, text)
        self.assertTrue(png.is_file())
        self.assertIn("planned end state: Match held out", text)
        rec = json.loads((self.proj / "takes" / "1B-3.json").read_text(encoding="utf-8"))
        self.assertEqual(rec["observed_end_state"], "match held out toward frame right")


# ---------- S3: prop bible, shot list, dialogue and hard-subject checks ----------

class TestPreproduction(Base):
    BOX = "a small dented tin matchbox with a hinged lid, scratched silver, the size of a palm"

    def project(self):
        return lib.Project(EXAMPLE)

    def warnings(self, p):
        return sorted({(i["card"], i["code"]) for i in lib.continuity_diff(p) if i["level"] == "warning"})

    def test_prop_description_compiled_verbatim(self):
        _, _, res = compile_one(EXAMPLE, "veo", "1A")
        self.assertIn("holding " + self.BOX, res[0][1])
        _, _, res = compile_one(EXAMPLE, "minimax-h3", sequence=True)
        self.assertIn("Maren is on the left of the frame, holding " + self.BOX, res[0][1], "the staging part carries the prop (genvideo L-004)")

    def test_prop_guard(self):
        orig = lib.card_parts

        def lossy(*a, **k):
            return {key: v.replace("dented ", "") for key, v in orig(*a, **k).items()}
        lib.card_parts = lossy
        try:
            p = self.project()
            _, _, prof = lib.find_model_card(repo_ctx(), "veo")
            with self.assertRaises(SystemExit) as cm:
                lib.compile_cards(p, [p.cards[0]], prof)
            self.assertIn("prop 'tin matchbox' not verbatim", str(cm.exception))
        finally:
            lib.card_parts = orig

    def test_prop_bible_validated(self):
        proj = self.tmp / "p"
        shutil.copytree(EXAMPLE, proj)
        edit(proj / "bibles/props.json", '"description": "one long wooden kitchen match with a red head"', '"description": "a match"')
        code, out = run("cards", "validate", proj)
        self.assertEqual(code, 1)
        self.assertIn("bibles/prop-bible", out)

    def test_prop_without_description_warns(self):
        p = self.project()
        p.props.pop("single match")
        self.assertIn(("1B", "PROP"), self.warnings(p))
        p.props = {}
        self.assertEqual(self.warnings(p), [], "no prop bible: listed props need no description")

    def test_rubric_names_prop_description(self):
        items = lib.rubric_items(self.project(), self.project().cards[0])
        props = [i["ask"] for i in items if i["check"] == "props"]
        self.assertTrue(props and self.BOX in props[0], props)

    def test_dialogue_length(self):
        p = self.project()
        self.assertEqual(self.warnings(p), [])
        p.cards[1]["dialogue"][0]["line"] = "This is the last one we have, and your hands are much steadier than mine tonight."
        self.assertIn(("1B", "DIALOGUE"), self.warnings(p))
        p.cards[1]["duration_s"] = 8
        self.assertNotIn(("1B", "DIALOGUE"), self.warnings(p))

    def test_hard_subject(self):
        p = self.project()
        p.cards[0]["action"] = "A herd of horses gallops past the lighthouse in the storm."
        self.assertIn(("1A", "HARD-SUBJECT"), self.warnings(p))
        p.cards[0]["camera"]["size"] = "MS"
        self.assertNotIn(("1A", "HARD-SUBJECT"), self.warnings(p))

    def test_cast_count(self):
        p = self.project()
        self.assertEqual(self.warnings(p), [])
        p.cards[0]["action"] = "Ten spearmen brace on the left; ten pale creatures sprint in from the right."
        self.assertIn(("1A", "CAST-COUNT"), self.warnings(p))
        p.cards[0]["action"] = "Three fishermen haul a net for ten seconds beside two boats and five long oars."
        self.assertNotIn(("1A", "CAST-COUNT"), self.warnings(p))
        self.assertEqual(lib.counted_people("12 soldiers and a dozen archers, then 2 minutes of rain")[0], 24)
        self.assertEqual(lib.counted_people("one man walks four steps")[0], 0)

    def test_cards_list(self):
        code, out = run("cards", "list", EXAMPLE)
        self.assertEqual(code, 0, out)
        self.assertIn("| 2 | 1B | MCU | eye-level | 45 | dolly-in | 50 | Maren |", out)
        self.assertTrue(out.rstrip().endswith("shot list: 3 shots, 1 scene(s), 14s"), out[-80:])

    def test_example_script_matches_bibles_and_cards(self):
        script = (EXAMPLE / "script.md").read_text(encoding="utf-8")
        p = self.project()
        for s in p.scenes["scenes"]:
            self.assertIn(s["heading"] + "\n", script)
        for c in p.cards:
            for d in c.get("dialogue", []):
                self.assertIn(d["line"], script)


class TestSpeakers(Base):
    """Library film test (2026-10-07): an off-screen rival's line came out of the hero's mouth, and an invented name was misread."""

    def offscreen(self):
        p = lib.Project(EXAMPLE)
        c = next(c for c in p.cards if c["id"] == "1C")  # Tomas alone in the shot
        c["dialogue"] = [{"character": "maren", "line": "Maren keeps the light.", "tone": "from the stairs"}]
        return p, c

    def compiled(self, p, model, card):
        _, _, prof = lib.find_model_card(repo_ctx(), model)
        return lib.compile_cards(p, [card], prof, False, DRAFT_RES.get(model))[0]

    def test_h3_offscreen_line_is_a_voiceover_with_closed_lips(self):
        p, c = self.offscreen()
        _, text, _, warnings, _ = self.compiled(p, "minimax-h3", c)
        self.assertIn("off screen, (S1) says in an off-screen voiceover from the stairs: <d>[English] Maren keeps the light.</d> "
                      "while the lips of Tomas remain completely closed.", text)
        self.assertTrue(any("1C: Maren speaks off screen" in w for w in warnings), warnings)

    def test_h3_onscreen_line_keeps_the_others_silent(self):
        p = lib.Project(EXAMPLE)
        c = next(c for c in p.cards if c["id"] == "1A")  # Maren and Tomas in shot
        c["dialogue"] = [{"character": "maren", "line": "Hold it steady."}]
        _, text, _, _, _ = self.compiled(p, "minimax-h3", c)
        self.assertIn("(S1) says: <d>[English] Hold it steady.</d> while the lips of Tomas remain completely closed.", text)
        self.assertNotIn("voiceover", text)

    def test_model_without_voiceover_leaves_the_line_for_the_mix(self):
        p, c = self.offscreen()
        _, text, _, warnings, _ = self.compiled(p, "veo", c)
        self.assertNotIn("Maren keeps the light", text)
        self.assertTrue(any("left out of the prompt" in w and "lay it in the mix" in w for w in warnings), warnings)

    def test_pronounce_respells_spoken_words_only(self):
        p, c = self.offscreen()
        p.pronounce = {"Maren": "MAH-ren"}
        _, text, _, _, _ = self.compiled(p, "minimax-h3", c)
        self.assertIn("<d>[English] MAH-ren keeps the light.</d>", text)
        self.assertIn("Maren with a low, dry, unhurried voice", text, "the name stays as written outside the line")
        self.assertEqual(lib.spoken(p, "Marena and Maren."), "Marena and MAH-ren.", "whole words only")

    def test_continuity_flags_offscreen_two_speakers_tone_and_names(self):
        p, c = self.offscreen()
        warn = lambda: sorted({i["code"] for i in lib.continuity_diff(p) if i["card"] == "1C"})
        self.assertEqual(warn(), ["OFFSCREEN", "PRONOUNCE"])
        p.pronounce = {"Maren": "Maren"}
        self.assertEqual(warn(), ["OFFSCREEN"])
        c["dialogue"] = [{"character": "tomas", "line": "Coming.", "tone": "mutters"}, {"character": "maren", "line": "Hurry."}]
        self.assertEqual(warn(), ["OFFSCREEN", "SPEAKERS", "TONE"])

    def test_rubric_marks_offscreen_line(self):
        p, c = self.offscreen()
        audio = [i["ask"] for i in lib.rubric_items(p, c) if i["check"] == "audio"]
        self.assertIn("Maren (off screen, no visible mouth) says", audio[0])

    def test_character_bible_accepts_pronounce(self):
        bible = json.loads((EXAMPLE / "bibles/characters.json").read_text(encoding="utf-8"))
        bible["pronounce"] = {"Maren": "MAH-ren"}
        self.assertEqual(lib.validate(bible, json.loads((REPO / "shared/schemas/character-bible.schema.json").read_text(encoding="utf-8"))), [])


# ---------- S4: style fields from cinewright-camera and cinewright-history ----------

NH = EXAMPLE / "styles" / "new-hollywood-239.json"


class TestStyle(Base):
    """PLAN §10 S4 exit check: "shoot it like 1970s New Hollywood, 2.39" changes the compiled prompts in checkable ways."""
    BOX = TestPreproduction.BOX

    def styled(self, model, sequence=False):
        p = lib.Project(EXAMPLE, style=NH)
        _, _, prof = lib.find_model_card(repo_ctx(), model)
        return p, lib.compile_cards(p, p.cards, prof, sequence, DRAFT_RES.get(model))

    def test_new_hollywood_changes_compiled_prompts(self):
        nh = json.loads(NH.read_text(encoding="utf-8"))
        base = json.loads((EXAMPLE / "bibles/style.json").read_text(encoding="utf-8"))
        frame = "Composed for a 2.39:1 widescreen crop, heads and action inside the middle 74% of the frame height."
        for model, seq in (("veo", False), ("minimax-h3", True), ("kling", False)):
            _, _, before = compile_one(EXAMPLE, model, sequence=seq)
            p, after = self.styled(model, seq)
            self.assertEqual(len(before), len(after))
            for (_, old, oldp, _, _), (_, new, newp, _, _) in zip(before, after):
                self.assertIn(nh["look"], new)
                self.assertNotIn(base["look"], new)
                self.assertIn(nh["lighting"], new, "lighting compiles verbatim")
                self.assertIn(frame, new, "the 2.39 frame becomes a composition sentence")
                self.assertNotIn("2.39", old)
                self.assertEqual(oldp.get("aspectRatio"), newp.get("aspectRatio"), "the render aspect stays a size the model offers")
                self.assertEqual(new.count(nh["lighting"]), 1, "said once per generation")
            for c in p.cards:
                for m in c.get("cast", []):
                    self.assertTrue(any(p.chars[m["id"]]["identity"] in t for _, t, _, _, _ in after))
        _, h3 = self.styled("minimax-h3", True)
        self.assertIn("Maren is on the left of the frame, holding " + self.BOX, h3[0][1], "staging part kept (genvideo L-004)")

    def test_style_guard(self):
        orig = lib.card_parts

        def lossy(*a, **k):
            return {key: v.replace("Low-key light, ", "") for key, v in orig(*a, **k).items()}
        lib.card_parts = lossy
        try:
            p = lib.Project(EXAMPLE, style=NH)
            _, _, prof = lib.find_model_card(repo_ctx(), "veo")
            with self.assertRaises(SystemExit) as cm:
                lib.compile_cards(p, [p.cards[0]], prof)
            self.assertIn("style lighting not verbatim", str(cm.exception))
        finally:
            lib.card_parts = orig

    def test_lens_and_move_warnings(self):
        def warn(p):
            return sorted({(i["card"], i["code"]) for i in lib.continuity_diff(p) if i["level"] == "warning"})
        p = lib.Project(EXAMPLE, style=NH)
        self.assertEqual(warn(p), [])
        p.style["lens_family"] = "spherical zooms, 25-250mm"
        self.assertEqual(warn(p), [("1A", "LENS")], "24mm is outside 25-250mm")
        p.style["allowed_moves"] = ["static", "zoom-in", "zoom-out", "handheld"]
        self.assertIn(("1B", "MOVE"), warn(p), "a dolly-in in a zooms-only style")
        p.style.pop("lens_family")
        p.style.pop("allowed_moves")
        self.assertEqual(warn(p), [], "no family and no move list: nothing to check")

    def test_frame_words(self):
        st = {"aspect_ratio": "16:9"}
        self.assertEqual(lib.frame_words(st), "")
        st["frame_aspect"] = "1.78:1"
        self.assertEqual(lib.frame_words(st), "", "same as the render")
        st["frame_aspect"] = "1.37:1"
        self.assertIn("middle 77% of the frame width", lib.frame_words(st))
        self.assertEqual(lib.lens_range("primes 24-50mm and a 25-250mm zoom"), (24, 250))
        self.assertIsNone(lib.lens_range("vintage primes"))

    def test_style_option_and_schema(self):
        for args in (("cards", "validate"), ("continuity", "diff")):
            code, out = run(*args, EXAMPLE, "--style", NH)
            self.assertEqual(code, 0, out)
        bad = self.tmp / "bad.json"
        st = json.loads(NH.read_text(encoding="utf-8"))
        st["allowed_moves"] = ["static", "fly", "static"]
        st["frame_aspect"] = "scope"
        bad.write_text(json.dumps(st), encoding="utf-8")
        code, out = run("cards", "validate", EXAMPLE, "--style", bad)
        self.assertEqual(code, 1)
        for msg in ("'fly' is not one of", "items repeat", "'scope' does not match"):
            self.assertIn(msg, out)
        code, out = run("compile", EXAMPLE, "--model", "veo", "--card", "1B", "--style", NH)
        self.assertIn("Composed for a 2.39:1 widescreen crop", out)
        self.assertIn('"aspectRatio": "16:9"', out)


def tone(path, hz, seconds=3.0, lead=0.3):
    """A clip whose only sound is a steady tone: a stand-in voice with a known pitch."""
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i",
                        "sine=frequency=%s:duration=%s,volume=0.3,adelay=%d,apad=whole_dur=%s" % (hz, seconds, lead * 1000, seconds + 2 * lead),
                        "-ar", "24000", str(path)], capture_output=True)
    assert r.returncode == 0, r.stderr
    return path


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "ffmpeg not installed")
class TestVoice(Base):
    def setUp(self):
        super().setUp()
        self.proj = model_project(self.tmp)
        (self.proj / "voices" / "maren").mkdir(parents=True)
        tone(self.proj / "voices" / "maren" / "neutral.wav", 180)
        self.bible = {"voices": [{"character": "maren",
                                  "sheet": {"age": "sixties", "gender": "female", "pitch": "low", "pace": "unhurried", "timbre": "dry"},
                                  "refs": [{"file": "voices/maren/neutral.wav", "text": "Last one. Your hands are steadier than mine.",
                                            "emotion": "neutral", "source": "take", "from": "takes/2A-1.mp4"}],
                                  "rights": "original designed voice"}]}
        lib.write_text(self.proj / "bibles" / "voices.json", json.dumps(self.bible))

    def test_measure_reads_pitch_and_pace(self):
        code, text = run("voice", "measure", self.proj / "voices" / "maren" / "neutral.wav", "--text", "one two three four five six", "--json")
        self.assertEqual(code, 0, text)
        m = json.loads(text)
        self.assertAlmostEqual(m["f0_median_hz"], 180, delta=3)
        self.assertLess(m["range_st"], 1)
        self.assertAlmostEqual(m["wpm"], 120, delta=12)
        self.assertEqual(m["warnings"], [])

    def test_ref_cuts_a_span(self):
        src = tone(self.tmp / "take.wav", 220, seconds=6)
        out = self.tmp / "ref.wav"
        code, text = run("voice", "ref", src, "--start", "1", "--end", "4", "--out", out, "--text", "Hold the match steady.")
        self.assertEqual(code, 0, text)
        self.assertIn("24000 Hz", text)
        self.assertRegex(text, r"pitch median 2[12]\d Hz")
        self.assertLess(lib.voice_measure(out)["seconds"], 3.2)

    def test_check_bible_and_lines(self):
        code, text = run("voice", "check", self.proj)
        self.assertEqual(code, 0, text)
        self.assertIn("maren: 1 reference(s), emotions neutral", text)
        code, text = run("voice", "check", self.proj, "--character", "maren", "--clip", tone(self.tmp / "same.wav", 186))
        self.assertEqual(code, 0, text)
        self.assertIn("PASS", text)
        code, text = run("voice", "check", self.proj, "--character", "maren", "--clip", tone(self.tmp / "low.wav", 104))
        self.assertEqual(code, 1, text)
        self.assertIn("DRIFT pitch -9.5 semitones", text)
        self.assertIn("wrong gender or age", text)

    def test_check_catches_bible_errors(self):
        self.bible["voices"][0]["refs"][0]["file"] = "voices/maren/missing.wav"
        self.bible["voices"].append({"character": "nobody", "sheet": self.bible["voices"][0]["sheet"], "refs": [], "rights": "x"})
        lib.write_text(self.proj / "bibles" / "voices.json", json.dumps(self.bible))
        code, text = run("voice", "check", self.proj)
        self.assertEqual(code, 1, text)
        self.assertIn("reference voices/maren/missing.wav is missing", text)
        self.assertIn("'nobody' is not in characters.json", text)
        self.assertIn("shorter than 10 characters", text)
        code, text = run("cards", "validate", self.proj)
        self.assertEqual(code, 1, text)
        self.assertIn("bibles/voice-bible", text)


class TestBeats(Base):
    """Card beats: timed hits compiled as a timeline for models that take timecodes (open test 2, 2026-10-16)."""
    BEATS = [{"t0": 0, "t1": 1.2, "text": "Maren lifts the match toward Tomas"},
             {"t0": 1.2, "t1": 2.0, "text": "the flame gutters in the draught"},
             {"t0": 2.0, "t1": 4.4, "text": "Tomas cups his hands round it"}]

    def project(self, beats=None):
        base = Path(tempfile.mkdtemp(dir=self.tmp))
        proj = model_project(base)
        c = json.loads((proj / "cards/1B.json").read_text(encoding="utf-8"))
        c["beats"] = beats if beats is not None else self.BEATS
        (proj / "cards/1B.json").write_text(json.dumps(c), encoding="utf-8")
        return proj

    def test_h3_compiles_a_timeline_in_place_of_the_action(self):
        _, _, res = compile_one(self.project(), "minimax-h3", "1B")
        text, warnings = res[0][1], res[0][3]
        self.assertIn("at slow speed. Timeline: [0.0s-1.2s] Maren lifts the match toward Tomas. [1.2s-2.0s] The flame gutters in the draught. "
                      "[2.0s-4.4s] Tomas cups his hands round it.", text)
        self.assertNotIn("Maren slowly stretches her arm out", text, "the beats replace the action")
        self.assertTrue(any("beats run to 4.4s: keep the last 4s in the edit" in w for w in warnings), warnings)

    def test_models_without_timecodes_get_the_action(self):
        _, _, res = compile_one(self.project(), "veo", "1B")
        self.assertIn("Maren slowly stretches her arm out toward Tomas", res[0][1])
        self.assertNotIn("Timeline", res[0][1])
        self.assertTrue(any("takes no timecodes" in w for w in res[0][3]), res[0][3])

    def test_beats_past_the_rendered_clip_fail(self):
        proj = self.project(self.BEATS[:2] + [{"t0": 2.0, "t1": 5.0, "text": "Tomas cups his hands round it"}])
        with self.assertRaises(SystemExit) as cm:
            compile_one(proj, "minimax-h3", "1B")
        self.assertIn("beats run to 5.0s, past the 4.458s render", str(cm.exception))

    def test_validate_wants_beats_in_order_without_overlap(self):
        code, out = run("cards", "validate", self.project())
        self.assertEqual(code, 0, out)
        bad = [{"t0": 0, "t1": 1.2, "text": "Maren lifts the match"}, {"t0": 1.0, "t1": 2.0, "text": "the flame gutters"},
               {"t0": 3.0, "t1": 2.5, "text": "Tomas cups his hands"}, {"t0": 3.0, "t1": 17, "text": "the match goes out"}]
        code, out = run("cards", "validate", self.project(bad))
        self.assertEqual(code, 1, out)
        self.assertIn("beats[1] (1.0-2.0s) overlaps or runs backward", out)
        self.assertIn("beats[2] (3.0-2.5s) overlaps or runs backward", out)
        self.assertIn("beats[3].t1: 17 is above 16", out)

    def test_fight_check_reads_marks_in_beats(self):
        f = self.tmp / "match.json"
        plan = {"id": "match", "scene": "1", "question": "Who gets the match?", "ending": "Tomas holds it.",
                "fighters": [{"id": "maren", "goal": "keep it", "side": "frame-left", "right": "single match", "marks": ["soot on her left cheek"]},
                             {"id": "tomas", "goal": "get it", "side": "frame-right"}],
                "phrases": [{"id": "P1", "ahead": "maren", "why": "she has it"}, {"id": "P2", "ahead": "tomas", "why": "she gives it", "margin": 2}],
                "exchanges": [{"n": 1, "phrase": "P1", "lead": "maren", "with": "single match", "move": "holds the match out",
                               "answer": "Tomas reaches", "result": "none", "secs": 3, "card": "1B"},
                              {"n": 2, "phrase": "P2", "lead": "tomas", "move": "takes it", "answer": "Maren lets go", "result": "disarm",
                               "card": "1C", "changes": [{"who": "tomas", "right": "single match"}]}]}
        f.write_text(json.dumps(plan), encoding="utf-8")
        fight = REPO / "shared" / "lib" / "cine_fight.py"
        code, text = run("check", f, "--project", self.project(), script=fight)
        self.assertIn("copy maren's mark 'soot on her left cheek'", text)
        proj = self.project()
        edit(proj / "cards/1B.json", '"action": "Maren', '"action": "Maren, soot on her left cheek,')
        code, text = run("check", f, "--project", proj, script=fight)
        self.assertIn("copy maren's mark 'soot on her left cheek'", text, "a timecoded prompt drops the action, so its marks do not count")
        beats = [dict(self.BEATS[0], text="Maren, soot on her left cheek, lifts the match")] + self.BEATS[1:]
        code, text = run("check", f, "--project", self.project(beats), script=fight)
        self.assertNotIn("soot on her left cheek", text)


class TestVisualStructure(Base):
    """Books track 3: Block's visual structure and Brown's light rules in the diff, compile, graph and rubric."""

    def project(self):
        return lib.Project(EXAMPLE)

    def warns(self, p, code):
        return sorted(i["card"] for i in lib.continuity_diff(p) if i["code"] == code)

    def test_space_warnings(self):
        p = self.project()
        self.assertEqual(self.warns(p, "SPACE"), [])
        p.scene_map["1"]["space"] = "flat"  # 1A has a 24mm lens, 1B dollies in
        self.assertEqual(self.warns(p, "SPACE"), ["1A", "1B"])
        p.scene_map["1"]["space"] = "deep"
        self.assertEqual(self.warns(p, "SPACE"), [])
        for c in p.cards:
            c["camera"]["move"] = "static"
        self.assertEqual(self.warns(p, "SPACE"), ["1C"], "a deep scene of static eye-level frames only warns once")

    def test_key_side_broad_light(self):
        p = self.project()
        self.assertEqual(self.warns(p, "KEY-SIDE"), [])  # both singles are keyed on the side the face turns to
        p.cards[2]["light"]["key_side"] = "frame-right"  # Tomas looks frame-left: the key is now on the near side
        self.assertEqual(self.warns(p, "KEY-SIDE"), ["1C"])
        p.cards[2]["light"]["motivation"] = "broad window light, the sea side"
        self.assertEqual(self.warns(p, "KEY-SIDE"), [])
        p.cards[2]["light"].pop("motivation")
        p.cards[2]["light"]["tone"] = "hide"
        self.assertEqual(self.warns(p, "KEY-SIDE"), [])

    def test_attention_jump_and_position(self):
        p = self.project()
        p.cards[1]["attention"] = {"start": 3, "end": 3}
        p.cards[2]["attention"] = {"start": 7, "end": 7}
        self.assertEqual(self.warns(p, "ATTENTION"), ["1C"])
        p.cards[2]["attention"] = {"start": 2, "end": 2}
        self.assertEqual(self.warns(p, "ATTENTION"), [], "one cell over is not a jump across the frame")
        p.cards[2]["attention"] = {"start": 7}
        p.cards[2]["intensity"] = 80
        self.assertEqual(self.warns(p, "ATTENTION"), [], "a jump at a peak is planned contrast")
        p.cards[2]["cast"][0]["position"] = "frame-right"
        self.assertEqual(self.warns(p, "ATTENTION"), ["1C"], "cell 7 is the left column, Tomas stands frame right")

    def test_compile_writes_structure_and_light_words(self):
        proj = self.tmp / "p"
        shutil.copytree(EXAMPLE, proj)
        scenes = json.loads(lib.read_text(proj / "bibles/scenes.json"))
        scenes["scenes"][0]["space"] = "flat"
        lib.write_text(proj / "bibles/scenes.json", json.dumps(scenes))
        edit(proj / "cards/1C.json", '"light": {"key_side": "frame-left", "quality": "soft"}',
             '"line": "diagonal", "attention": {"start": 4, "end": 5}, "light": {"key_side": "frame-left", "quality": "soft", '
             '"motivation": "the brazier at frame left", "atmosphere": "smoke", "tone": "hide"}')
        code, out = run("compile", proj, "--model", "veo", "--card", "1C")
        self.assertEqual(code, 0, out)
        for words in ("Flat space: a wall square to the camera", "Strong diagonal lines cut across the frame",
                      "Tomas's face is in the left of the frame, ending in the center", "on the far side of the face",
                      "the firelight flickers and the shadows jump", "the smoke is backlit", "the face stays hidden in shadow"):
            self.assertIn(words, out)
        edit(proj / "cards/1C.json", '"key_side": "frame-left"', '"key_side": "frame-right"')
        code, out = run("compile", proj, "--model", "veo", "--card", "1C")
        self.assertNotIn("far side of the face", out, "a broad key is not the upstage side")

    def test_cards_validate_reads_the_new_fields(self):
        proj = self.tmp / "p"
        shutil.copytree(EXAMPLE, proj)
        edit(proj / "cards/1A.json", '"beat":', '"intensity": 140, "line": "zigzag", "beat":')
        code, out = run("cards", "validate", proj)
        self.assertEqual(code, 1, out)
        self.assertIn("140 is above 100", out)
        self.assertIn("zigzag", out)

    def graph_project(self, levels, climax=None, peaks=None):
        proj = self.tmp / "g"
        shutil.copytree(EXAMPLE, proj)
        scenes = json.loads(lib.read_text(proj / "bibles/scenes.json"))
        base = scenes["scenes"][0]
        scenes["scenes"] = [dict(json.loads(json.dumps(base)), id=str(i + 1), intensity=lv, space=sp, color={"hue": hue})
                            for i, (lv, sp, hue) in enumerate(levels)]
        lib.write_text(proj / "bibles/scenes.json", json.dumps(scenes))
        style = json.loads(lib.read_text(proj / "bibles/style.json"))
        style["visual_structure"] = {"climax": climax, "plans": [{"component": "saturation", "mode": "peaks", "peaks": peaks or []}]}
        lib.write_text(proj / "bibles/style.json", json.dumps(style))
        card = json.loads(lib.read_text(proj / "cards/1C.json"))
        for f in proj.glob("cards/*.json"):
            f.unlink()
        for i in range(len(levels)):
            lib.write_text(proj / "cards" / ("%dA.json" % (i + 1)), json.dumps(dict(card, id="%dA" % (i + 1), scene=str(i + 1), order=i + 1)))
        return proj

    def test_cards_graph_flags_a_bad_curve(self):
        proj = self.graph_project([(10, "flat", "blue"), (30, "flat", "blue"), (30, "flat", "blue"), (20, "deep", "amber")], climax="4", peaks=["1"])
        code, out = run("cards", "graph", proj, "--csv", self.tmp / "g.csv")
        self.assertEqual(code, 0, out)
        for flag in ("FLAG CLIMAX", "FLAG FLAT", "FLAG SAME: scenes 2 and 3", "FLAG PEAK: saturation spikes at scene 1"):
            self.assertIn(flag, out)
        self.assertIn("order,card,scene,scene_intensity", lib.read_text(self.tmp / "g.csv"))

    def test_cards_graph_passes_a_shaped_curve(self):
        proj = self.graph_project([(10, "flat", "blue"), (45, "limited", "blue"), (95, "deep", "red"), (30, "flat", "amber")], climax="3", peaks=["3"])
        code, out = run("cards", "graph", proj)
        self.assertIn("0 flag(s)", out)
        code, out = run("cards", "graph", EXAMPLE)
        self.assertIn("FLAG INTENSITY: no scene has an intensity", out)

    def test_rubric_hides_identity_and_asks_space_and_attention(self):
        p = self.project()
        p.scene_map["1"]["space"] = "limited"
        p.cards[1]["attention"] = {"start": 6, "end": 6}
        p.cards[2]["attention"] = {"start": 4}
        p.cards[2]["light"]["tone"] = "hide"
        items = {i["id"]: i for i in lib.rubric_items(p, p.cards[2])}
        self.assertEqual(items["identity:tomas"]["verdict"], "na")
        self.assertIn("Limited space", items["space"]["ask"])
        self.assertIn("in the left of the first frame, where 1B left the eye in the right", items["attention"]["ask"])
        self.assertIsNone(lib.rubric_items(p, p.cards[1])[0]["verdict"])
        codes = lib.taxonomy(repo_ctx())
        self.assertEqual({c: codes[c]["check"] for c in ("flat-light", "space-break", "attention-jump", "pan-strobe")},
                         {"flat-light": "light", "space-break": "space", "attention-jump": "attention", "pan-strobe": "camera"})


class TestFraming(Base):
    """Books track 4: framing, camera angles and moves (Mateu-Mestre, Mascelli, Katz, Block)."""

    def warns(self, p, code):
        return sorted(i["card"] for i in lib.continuity_diff(p) if i["code"] == code)

    def test_straight_in_cut_on_people_across_the_frame(self):
        p = lib.Project(EXAMPLE)
        b = p.cards[1]
        b["cast"] = json.loads(json.dumps(p.cards[0]["cast"]))  # the same two people, frame left and right
        b["camera"]["azimuth_deg"] = 90  # 1A is a WS at 90: a straight-in cut to the MCU
        self.assertEqual(self.warns(p, "STRAIGHT-IN"), ["1B"])
        b["camera"]["azimuth_deg"] = 60
        self.assertEqual(self.warns(p, "STRAIGHT-IN"), [], "30 degrees round is a move in and around")
        b["camera"]["azimuth_deg"] = 90
        for m in b["cast"]:
            m["position"] = "center"
        self.assertEqual(self.warns(p, "STRAIGHT-IN"), [], "a centred subject may take a straight-in cut")
        b["cast"][0]["position"] = "frame-left"
        p.cards[0]["camera"]["size"], b["camera"]["size"] = "MCU", "WS"
        self.assertEqual(self.warns(p, "STRAIGHT-IN"), [], "cutting straight back out is not a cut-in")

    def test_horizon_against_the_angle_and_dutch_pairs(self):
        p = lib.Project(EXAMPLE)
        a, b, c = (x["camera"] for x in p.cards)
        a["angle"], a["horizon"] = "low", "upper-third"
        self.assertEqual(self.warns(p, "HORIZON"), ["1A"])
        a["horizon"] = "lower-third"
        self.assertEqual(self.warns(p, "HORIZON"), [])
        a["angle"], a["horizon"] = "overhead", "middle"
        self.assertEqual(self.warns(p, "HORIZON"), ["1A"])
        a["horizon"] = "above-frame"
        self.assertEqual(self.warns(p, "HORIZON"), [])
        b["angle"] = c["angle"] = "dutch"
        b["dutch"] = c["dutch"] = "left"
        self.assertEqual(self.warns(p, "DUTCH"), ["1C"], "Maren and Tomas tilt the same way")
        c["dutch"] = "right"
        self.assertEqual(self.warns(p, "DUTCH"), [])
        a["dutch"] = "right"  # opposite to 1B, so only the side set on a non-dutch angle warns
        self.assertEqual(self.warns(p, "DUTCH"), ["1A"], "dutch side on an overhead angle")

    def test_compile_writes_horizon_dutch_view_and_new_moves(self):
        proj = self.tmp / "p"
        shutil.copytree(EXAMPLE, proj)
        edit(proj / "cards/1C.json", '"angle": "eye-level"', '"angle": "dutch", "dutch": "right", "horizon": "lower-third"')
        edit(proj / "cards/1C.json", '"move": "static"', '"move": "arc-left"')
        edit(proj / "cards/1C.json", '"id": "tomas"', '"id": "tomas", "view": "three-quarter-back"')
        code, out = run("compile", proj, "--model", "veo", "--card", "1C")
        self.assertEqual(code, 0, out)
        for words in ("dutch angle, the frame tilted down to the right, the horizon on the lower third of the frame",
                      "the camera arcs slowly left around the subject", "only the cheek line showing"):
            self.assertIn(words, out)
        code, out = run("compile", proj, "--model", "minimax-h3", "--card", "1C", "--resolution", "480p")
        self.assertIn("The camera arcs left around the subject", out)
        code, out = run("cards", "new", proj, "--id", "1D", "--scene", "1", "--cast", "maren")
        self.assertEqual(json.loads(lib.read_text(proj / "cards/1D.json"))["cast"][0]["view"], "three-quarter")

    def test_framing_codes_reach_the_rubric(self):
        p = lib.Project(EXAMPLE)
        self.assertIn("framing", {i["check"] for i in lib.rubric_items(p, p.cards[0])})
        codes = lib.taxonomy(repo_ctx())
        self.assertEqual({c: codes[c]["check"] for c in ("edge-tangent", "bg-tangent", "ots-wrong", "horizon-split", "flat-depth")},
                         {"edge-tangent": "framing", "bg-tangent": "framing", "ots-wrong": "framing", "horizon-split": "camera", "flat-depth": "space"})
        self.assertIn("push-in", lib.SPACE_3D)


_pspec = importlib.util.spec_from_file_location("cine_post_lib", REPO / "shared" / "lib" / "cine_post.py")
post = importlib.util.module_from_spec(_pspec)
_pspec.loader.exec_module(post)


class TestLookMeasures(Base):
    """cine_post.py grade measure --plan, grade stabilize, grade match --sat/--warm (books track 3)."""
    POST = REPO / "shared" / "lib" / "cine_post.py"

    def ffmpeg(self, *args):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + [str(a) for a in args], check=True)

    def stripes(self, name, expr):
        f = self.tmp / name
        self.ffmpeg("-f", "lavfi", "-i", "color=c=gray:s=320x180", "-vf", "format=yuv444p,geq=lum='255*gt(mod(%s,24),12)':cb=128:cr=128" % expr,
                    "-frames:v", "1", f)
        return post.look_stats(f)

    def test_edge_orientation_reads_the_dominant_line(self):
        h, v, d = self.stripes("h.png", "Y"), self.stripes("v.png", "X"), self.stripes("d.png", "X+Y")
        self.assertGreater(h["horizontal"], 0.8)
        self.assertGreater(v["vertical"], 0.8)
        self.assertGreater(d["diagonal"], 0.8)

    def shots(self, levels, names=("1A", "1B", "1C", "1D")):
        out = []
        for name, b in zip(names, levels):
            f = self.tmp / ("take_%s-1.mp4" % name)
            self.ffmpeg("-f", "lavfi", "-i", "testsrc2=s=160x90:d=1,eq=brightness=%s" % b, f)
            out.append(f)
        return out

    def plan_project(self, plan, color=None):
        proj = self.tmp / "p"
        if not proj.exists():
            shutil.copytree(EXAMPLE, proj)
        d = json.loads(lib.read_text(proj / "cards/1C.json"))
        lib.write_text(proj / "cards/1D.json", json.dumps(dict(d, id="1D", order=4)))
        style = json.loads(lib.read_text(proj / "bibles/style.json"))
        style["visual_structure"] = {"plans": [plan]}
        lib.write_text(proj / "bibles/style.json", json.dumps(style))
        if color:
            scenes = json.loads(lib.read_text(proj / "bibles/scenes.json"))
            scenes["scenes"][0]["color"] = color
            lib.write_text(proj / "bibles/scenes.json", json.dumps(scenes))
        return proj

    def test_plan_progression_follows_and_runs_against(self):
        files = self.shots(["-0.3", "-0.1", "0.1", "0.3"])  # brighter shot by shot
        proj = self.plan_project({"component": "brightness", "mode": "progression", "from": "dark", "to": "bright"})
        code, out = run("grade", "measure", "--plan", proj, *files, script=self.POST)
        self.assertEqual(code, 0, out)
        self.assertIn("luma rho +1.00 follows over the cut", out)
        files = self.shots(["0.3", "0.1", "-0.1", "-0.3"])  # the same shots in the wrong order
        code, out = run("grade", "measure", "--plan", proj, *files, script=self.POST)
        self.assertEqual(code, 1, out)
        self.assertIn("AGAINST", out)

    def test_plan_colour_row_by_class(self):
        files = self.shots(["-0.35"] * 4)
        proj = self.plan_project({"component": "shape", "mode": "progression"}, color={"brightness": "bright"})
        code, out = run("grade", "measure", "--plan", proj, *files, script=self.POST)
        self.assertEqual(code, 1, out)
        self.assertIn("OFF brightness dark, planned bright", out)
        self.assertIn("plan shape: not measured", out)

    def test_stabilize_removes_slow_drift(self):
        clip = self.tmp / "drift.mp4"
        self.ffmpeg("-f", "lavfi", "-i", "testsrc2=s=160x90:r=24:d=4", "-vf", "eq=brightness='-0.15+0.075*t':eval=frame", clip)
        code, out = run("grade", "stabilize", clip, "--out", self.tmp / "st", script=self.POST)
        self.assertEqual(code, 0, out)
        before, after = (float(x) for x in re.search(r"drift ([\d.]+) -> ([\d.]+)", out).groups())
        self.assertGreater(before, 20)
        self.assertLess(after, before / 4)
        self.assertIn("WARN", out, "a drift this large is flagged for a look by eye")

    def test_match_holds_a_saturation_and_warmth_target(self):
        ref, shot = self.tmp / "ref.png", self.tmp / "shot.mp4"
        self.ffmpeg("-f", "lavfi", "-i", "testsrc2=s=160x90", "-frames:v", "1", ref)
        self.ffmpeg("-f", "lavfi", "-i", "testsrc2=s=160x90:d=1,eq=saturation=0.25", shot)  # chroma about 0.19, like a real shot
        code, out = run("grade", "match", shot, "--ref", ref, "--strength", "0", "--sat", "0.08", "--warm", "0.10", "--apply", self.tmp / "out", script=self.POST)
        self.assertEqual(code, 0, out)
        was, now = post.look_stats(shot), post.look_stats(self.tmp / "out" / "shot.mp4")
        self.assertGreater(abs(was["chroma"] - 0.08), 0.08)
        self.assertGreater(abs(was["warmth"] - 0.10), 0.08)
        self.assertLess(abs(now["chroma"] - 0.08), 0.03)
        self.assertLess(abs(now["warmth"] - 0.10), 0.03)
