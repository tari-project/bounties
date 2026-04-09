#!/usr/bin/env python3
"""Sync bounty markdown files to GitHub issues.

Preserves original issue body as a collapsed comment before overwriting.
Strips YAML frontmatter, pushes body as issue description, applies labels.

Usage:
    python3 scripts/sync_issues.py                       # sync all issues/*.md
    python3 scripts/sync_issues.py issues/foo-123-bar.md  # sync specific file(s)
"""
import subprocess, sys, os, re, yaml, glob

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
ISSUES_DIR = os.path.join(ROOT_DIR, "issues")


def get_files():
    """Get list of files to sync from args or all issues/*.md."""
    if len(sys.argv) > 1:
        return sys.argv[1:]
    return sorted(glob.glob(os.path.join(ISSUES_DIR, "*.md")))


def sync_file(fpath):
    """Sync a single bounty file to GitHub."""
    with open(fpath) as f:
        content = f.read()

    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not match:
        print(f"SKIP {fpath}: no frontmatter found")
        return False

    meta = yaml.safe_load(match.group(1))
    body = match.group(2).strip()
    repo = meta['repo']
    issue = meta['issue']
    labels = meta.get('labels', [])

    print(f"\n=== {repo}#{issue} ({os.path.basename(fpath)}) ===")

    # Fetch current issue body
    result = subprocess.run(
        ["gh", "issue", "view", str(issue), "--repo", repo,
         "--json", "body", "-q", ".body"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  FETCH FAILED: {result.stderr.strip()}")
        return False
    original_body = result.stdout.strip()

    # Preserve original as collapsed comment (skip if already a bounty rewrite)
    if original_body and not original_body.startswith("## Bounty:"):
        comment_text = (
            "<details><summary>Original issue description "
            "(preserved before bounty rewrite)</summary>\n\n"
            f"{original_body}\n\n</details>"
        )
        result = subprocess.run(
            ["gh", "issue", "comment", str(issue), "--repo", repo,
             "--body", comment_text],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"  COMMENT FAILED: {result.stderr.strip()}")
            return False
        print(f"  Original body saved as comment")
    else:
        print(f"  Skipping comment (body empty or already bounty format)")

    # Update issue body
    result = subprocess.run(
        ["gh", "issue", "edit", str(issue), "--repo", repo, "--body", body],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  BODY FAILED: {result.stderr.strip()}")
        return False
    print(f"  Body updated")

    # Create labels if needed, then apply
    for label in labels:
        subprocess.run(
            ["gh", "label", "create", label, "--repo", repo, "--force"],
            capture_output=True, text=True
        )
    if labels:
        result = subprocess.run(
            ["gh", "issue", "edit", str(issue), "--repo", repo,
             "--add-label", ",".join(labels)],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"  LABELS FAILED: {result.stderr.strip()}")
            return False
        print(f"  Labels applied: {labels}")

    return True


def main():
    files = get_files()
    if not files:
        print("No issue files found.", file=sys.stderr)
        sys.exit(1)

    print(f"Syncing {len(files)} file(s)...")
    ok = 0
    fail = 0
    for fpath in files:
        if sync_file(fpath):
            ok += 1
        else:
            fail += 1

    print(f"\nDone. {ok} synced, {fail} failed.")
    if fail:
        sys.exit(1)


if __name__ == "__main__":
    main()
