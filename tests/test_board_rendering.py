import json
import subprocess
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from scripts import generate_readme


class BoardRenderingTests(unittest.TestCase):
    def test_last_updated_uses_an_unpadded_utc_day(self):
        for day in (7, 27):
            with self.subTest(day=day), patch.object(generate_readme, "datetime") as clock:
                now = datetime(2026, 11, day, 13, 4, tzinfo=timezone.utc)
                clock.now.return_value = now
                readme = generate_readme.render_readme([])
                self.assertIn(f"*Last updated: {now:%B} {day}, 2026 at 13:04 UTC*", readme.splitlines())
                clock.now.assert_called_once_with(timezone.utc)

    def test_markdown_files_round_trip_as_utf8(self):
        with TemporaryDirectory() as tmp, patch.object(generate_readme, "ROOT_DIR", tmp):
            issues = Path(tmp, "issues")
            issues.mkdir()
            issues.joinpath("example.md").write_text(
                "---\nrepo: tari-project/universe\nissue: 1\n---\n## Bounty: Café\n",
                encoding="utf-8",
            )
            with patch.object(generate_readme, "fetch_bounty_issues", return_value=[]) as fetch:
                with patch("sys.argv", ["generate_readme.py"]):
                    generate_readme.main()
                fetch.assert_called_once_with({"tari-project/universe#1": "Café"})
            self.assertIn("0 bounties — 0 XTM", Path(tmp, "README.md").read_text(encoding="utf-8"))

    def test_issue_list_reads_utf8_titles_from_gh(self):
        title = "Réseau"
        item = {"number": 1, "title": title, "url": "https://example.org/1", "labels": []}
        payload = json.dumps([item], ensure_ascii=False)
        run = subprocess.run

        def emit_json(command, **kwargs):
            self.assertEqual(command[:3], ["gh", "issue", "list"])
            return run(
                [sys.executable, "-I", "-X", "utf8", "-c", "import sys; print(sys.argv[1])", payload],
                **kwargs,
            )

        with patch.object(generate_readme, "REPOS", ["tari-project/universe"]):
            with patch.object(subprocess, "run", side_effect=emit_json):
                issues = generate_readme.fetch_bounty_issues({})
        self.assertEqual(issues[0]["title"], title)
