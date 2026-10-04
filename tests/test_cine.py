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

    def test_loud(self):
        code, text = run("qc", "loud", self.clip)
        self.assertEqual(code, 1, text)
        self.assertRegex(text, r"integrated -\d+\.\d LUFS")
        code, text = run("qc", "loud", self.clip, "--target", "-22", "--tolerance", "2")
        self.assertEqual(code, 0, text)

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
