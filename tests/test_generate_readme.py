"""CLI regressions for preserving the board when GitHub fetches fail."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "generate_readme.py"
LAST_COMPLETE_BOARD = "# Last complete bounty board\nKeep this until every query succeeds.\n"
ISSUE = {
    "number": 1,
    "title": "Example bounty",
    "labels": [{"name": "bounty-S"}],
    "url": "https://github.com/tari-project/tari/issues/1",
    "state": "OPEN",
    "comments": [],
    "closedByPullRequestsReferences": [],
}
FAKE_GH = """#!/usr/bin/env python3
import json
import os
import sys
repo = sys.argv[sys.argv.index('-R') + 1]
response = json.loads(os.environ['FAKE_GH_RESPONSES']).get(repo, {})
print(json.dumps(response.get('issues', [])))
print(response.get('error', ''), file=sys.stderr)
sys.exit(response.get('exit_code', 0))
"""


class GenerateReadmeTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)
        (self.root / "scripts").mkdir()
        shutil.copy2(SCRIPT, self.root / "scripts" / SCRIPT.name)
        self.readme = self.root / "README.md"
        self.readme.write_text(LAST_COMPLETE_BOARD)
        self.bin_dir = self.root / "bin"
        self.bin_dir.mkdir()
        fake_gh = self.bin_dir / "gh"
        fake_gh.write_text(FAKE_GH)
        fake_gh.chmod(0o755)

    def run_generator(self, responses, *args):
        env = os.environ.copy()
        env["PATH"] = str(self.bin_dir) + os.pathsep + env.get("PATH", "")
        env["FAKE_GH_RESPONSES"] = json.dumps(responses)
        return subprocess.run(
            [sys.executable, str(self.root / "scripts" / SCRIPT.name), *args],
            cwd=self.root, env=env, capture_output=True, text=True,
        )

    def assert_failed_safely(self, result, repo, reason):
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.readme.read_text(), LAST_COMPLETE_BOARD)
        self.assertIn(repo, result.stderr)
        self.assertIn(reason, result.stderr)
        self.assertNotIn("Wrote README.md", result.stderr)

    def test_authentication_failure_preserves_existing_board(self):
        result = self.run_generator({"tari-project/tari": {
            "exit_code": 1, "error": "authentication expired",
        }})
        self.assert_failed_safely(result, "tari-project/tari", "authentication expired")

    def test_later_failure_does_not_publish_partial_results(self):
        result = self.run_generator({
            "tari-project/tari": {"issues": [ISSUE]},
            "tari-project/minotari-cli": {
                "exit_code": 1, "error": "API rate limit exceeded",
            },
        })
        self.assert_failed_safely(result, "tari-project/minotari-cli", "API rate limit exceeded")

    def test_dry_run_failure_does_not_print_partial_board(self):
        result = self.run_generator({
            "tari-project/tari": {"issues": [ISSUE]},
            "tari-project/minotari-cli": {"exit_code": 1, "error": "network unavailable"},
        }, "--dry-run")
        self.assert_failed_safely(result, "tari-project/minotari-cli", "network unavailable")
        self.assertEqual(result.stdout, "")

    def test_successful_queries_update_board(self):
        result = self.run_generator({"tari-project/tari": {"issues": [ISSUE]}})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Example bounty", self.readme.read_text())
        self.assertIn("1 bounties", self.readme.read_text())
        self.assertIn("Wrote README.md", result.stderr)

    def test_successful_empty_queries_remain_valid(self):
        result = self.run_generator({})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("0 bounties", self.readme.read_text())


if __name__ == "__main__":
    unittest.main()
