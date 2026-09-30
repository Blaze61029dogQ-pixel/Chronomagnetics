# SPDX-License-Identifier: MIT
# Copyright (c) 2026 James M. Lockwood
"""Repository integrity and consistency tests (``unittest``).

These tests check the repository: hashes, provenance, the derivation of the
release copy of the script, the consistency of the recorded runs, the
licence metadata, and a smoke test of the script's command-line interface.
They do not test the mathematics. The script's own checks do that (see
CLAIMS.md), and a passing check is not a proof.
"""

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import verify_repository as vr  # noqa: E402

# Historical SHA-256 values of the ORIGINAL artifacts as imported
# (provenance/FILES.md). These must never change. A new manuscript version is
# added as a release artifact, with its own hash in
# provenance/release_hashes.sha256, not by editing these values.
ORIGINAL_PDF_SHA256 = (  # Paper 1 PDF exactly as supplied (2026-09-29)
    "8c4b17317495ff791c3c8af2d0e5ad131e9115cf0c18ca332d1145dc853af256"
)
ORIGINAL_SI_PDF_SHA256 = (  # SI progress document v0.1 (Drive download, 2026-09-30)
    "fab5b718e5ff02728e0e8588525e3ca8fefd445fb1ffa82103e4fe05b85f0496"
)
ORIGINAL_SI_SCRIPT_SHA256 = (  # Google Docs text/plain export of the script
    "c682c895d51ce0acc09f260d4eede38e98be765c18268d1378e53d4be40dcb88"
)
ORIGINALS = {
    "paper/original/Paper1_AreaLaw_SU2_2026-09-28.pdf": ORIGINAL_PDF_SHA256,
    "supplementary/original/SI_YangMills_Tracks1-2_v0.1.pdf": ORIGINAL_SI_PDF_SHA256,
    "reproduction/original/SI_YangMills_reproduce_all.py": ORIGINAL_SI_SCRIPT_SHA256,
}

ORIGINAL_SCRIPT = "reproduction/original/SI_YangMills_reproduce_all.py"
RELEASE_SCRIPT = "reproduction/SI_YangMills_reproduce_all.py"
REMOVED_LINE = "# CONFIDENTIAL — DO NOT SHARE · DO NOT COPY · DO NOT REPRODUCE\r\n"


class Provenance(unittest.TestCase):
    def test_manifest(self):
        errors = []
        vr.check_manifest(errors)
        self.assertEqual(errors, [])

    def test_originals_match_historical_hashes(self):
        for path, digest in ORIGINALS.items():
            with self.subTest(path=path):
                self.assertEqual(vr.sha256(ROOT / path), digest)

    def test_source_hash_record_is_the_historical_record(self):
        recorded = vr.read_hash_file(ROOT / vr.SOURCE_HASHES)
        self.assertEqual(recorded, ORIGINALS)

    def test_recorded_hashes(self):
        errors = []
        vr.check_recorded_hashes(errors)
        self.assertEqual(errors, [])

    def test_release_script_is_original_minus_notice_line(self):
        orig = (ROOT / ORIGINAL_SCRIPT).read_bytes()
        rel = (ROOT / RELEASE_SCRIPT).read_bytes()
        lines = orig.splitlines(keepends=True)
        self.assertEqual(lines[1], REMOVED_LINE.encode("utf-8"))
        self.assertEqual(rel, lines[0] + b"".join(lines[2:]))
        self.assertNotIn(b"CONFIDENTIAL", rel)

    def test_release_hashes_cover_release_script(self):
        recorded = vr.read_hash_file(ROOT / vr.RELEASE_HASHES)
        self.assertIn(RELEASE_SCRIPT, recorded)
        self.assertEqual(recorded[RELEASE_SCRIPT], vr.sha256(ROOT / RELEASE_SCRIPT))


class Documentation(unittest.TestCase):
    def test_documentation_links(self):
        errors = []
        vr.check_links(errors)
        self.assertEqual(errors, [])

    def test_text_hygiene(self):
        errors = []
        vr.check_text_hygiene(errors)
        self.assertEqual(errors, [])

    def test_license_metadata_agree(self):
        lic = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertTrue(lic.startswith("MIT License\n"))
        self.assertIn("Copyright (c) 2026 James M. Lockwood\n", lic)
        cff = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
        self.assertRegex(cff, r"(?m)^license: MIT$")
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertRegex(pyproject, r'(?m)^license = "MIT"$')
        scope = (ROOT / "LICENSING.md").read_text(encoding="utf-8")
        for path in ORIGINALS:
            self.assertIn(f"`{path}`", scope)


class RecordedRuns(unittest.TestCase):
    """The committed run records must be internally consistent and must
    correspond to the committed scripts."""

    RUNS = {
        "results/quick": RELEASE_SCRIPT,
        "results/full": RELEASE_SCRIPT,
        "results/original-export/quick": ORIGINAL_SCRIPT,
        "results/original-export/full": ORIGINAL_SCRIPT,
    }

    def test_runs(self):
        for outdir, script in self.RUNS.items():
            with self.subTest(outdir=outdir):
                meta = json.loads((ROOT / outdir / "run_meta.json").read_text(encoding="utf-8"))
                report = json.loads((ROOT / outdir / "report.json").read_text(encoding="utf-8"))
                self.assertEqual(meta["script"], script)
                self.assertEqual(meta["script_sha256"], vr.sha256(ROOT / script))
                self.assertEqual(report["mode"], meta["mode"])
                counts = {s: sum(r["status"] == s for r in report["results"])
                          for s in ("PASS", "FAIL", "INFO")}
                m = re.match(r"SUMMARY: (\d+) PASS, (\d+) FAIL, (\d+) INFO", meta["summary_line"])
                self.assertIsNotNone(m)
                self.assertEqual((counts["PASS"], counts["FAIL"], counts["INFO"]),
                                 tuple(int(x) for x in m.groups()))
                self.assertEqual(meta["exit_status"], 1 if counts["FAIL"] else 0)
                log = (ROOT / outdir / "stdout.log").read_text(encoding="utf-8")
                self.assertIn(meta["summary_line"], log)

    def test_release_copy_reproduces_original_results(self):
        for mode in ("quick", "full"):
            with self.subTest(mode=mode):
                a = json.loads((ROOT / "results" / mode / "report.json").read_text(encoding="utf-8"))
                b = json.loads((ROOT / "results/original-export" / mode / "report.json").read_text(encoding="utf-8"))
                self.assertEqual(a["results"], b["results"])


class ScriptInterface(unittest.TestCase):
    """Smoke test of the release script's CLI and JSON report format on two
    fast sections. Needs numpy, scipy and mpmath (requirements.txt)."""

    def test_cli_json_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "report.json"
            proc = subprocess.run(
                [sys.executable, RELEASE_SCRIPT, "--sections", "S4,S10", "--json", str(out)],
                cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=600)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            report = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(report["mode"], "quick")
        self.assertEqual({r["section"] for r in report["results"]}, {"S4", "S10"})
        for r in report["results"]:
            self.assertEqual(set(r), {"section", "id", "desc", "tier", "status", "value", "expected"})
            self.assertIn(r["status"], {"PASS", "FAIL", "INFO"})
            self.assertIn(r["tier"], {"EXACT", "CERT", "NUM", "MC", "REG", "INFO"})


if __name__ == "__main__":
    unittest.main()
