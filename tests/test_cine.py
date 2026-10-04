"""Tests for scripts/cine.py and shared/lib/cine.py. Run: python -m unittest discover -s tests"""
import importlib.util
import json
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
    for name in ("plugins", "shared", ".claude-plugin", "examples", "ai-docs", "README.md", "LICENSE", "AGENTS.md", "CODEMAP.md"):
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

    def test_example_compiled_files_are_current(self):
        for sub, extra in (("veo", []), ("veo-sequence", ["--sequence"])):
            out_dir = self.tmp / sub
            code, out = run("compile", EXAMPLE, "--model", "veo", "--out", out_dir, *extra)
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

    def test_compile_rejects_unsupported_format(self):
        proj = self.tmp / "p"
        shutil.copytree(EXAMPLE, proj)
        edit(proj / "bibles/style.json", '"aspect_ratio": "16:9"', '"aspect_ratio": "4:3"')
        code, out = run("compile", proj, "--model", "veo")
        self.assertNotEqual(code, 0)
        self.assertIn("aspect 4:3 not offered", out)

    def test_unknown_model(self):
        code, out = run("compile", EXAMPLE, "--model", "nosuchmodel")
        self.assertEqual(code, 1)
        self.assertIn("no model card", out)


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
        cam.update({"side": "B", "crosses_axis": True, "cross_reason": "Tomas crosses the line on screen"})
        self.assertEqual(self.codes(p), [("1C", "EYELINE")], "on side B the eyeline must flip to frame-right")
        p.cards[2]["cast"][0]["eyeline"] = "frame-right"
        self.assertEqual(self.codes(p), [])


class TestBudgetZip(Base):
    def test_budget_green(self):
        code, out = run("budget")
        self.assertEqual(code, 0, out)
        self.assertIn("budget: GREEN", out)

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
