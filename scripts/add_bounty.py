#!/usr/bin/env python3
"""Add a new bounty issue from a GitHub issue.

Fetches the issue, creates the bounty markdown file from the template,
and appends it to summary.csv. You then review/edit the file, run
sync_issues.py to push it to GitHub, and generate_readme.py to update
the bounty board.

Usage:
    python3 scripts/add_bounty.py tari-project/universe 3128 S
    python3 scripts/add_bounty.py tari-project/tari 7715 M
    python3 scripts/add_bounty.py https://github.com/tari-project/tari/issues/7715 M
"""
import subprocess, json, sys, os, re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
ISSUES_DIR = os.path.join(ROOT_DIR, "issues")

TIERS = {"S", "M", "L", "XL"}

TEMPLATE = """---
repo: {repo}
issue: {issue}
labels: [bounty, bounty-{tier}]
original_size: {tier}
---

## Bounty: {title}

**Tier:** {tier} — reward TBD

### Description

{description}

### Acceptance Criteria

- [ ] TODO: add specific, verifiable, binary pass/fail criterion
- [ ] TODO: add criterion
- [ ] TODO: add criterion

### Context

{context}

### How to Claim

1. Comment on this issue to signal intent (courtesy, not a lock)
2. Fork the repo and do the work
3. Submit a PR that meets the acceptance criteria
4. First PR that passes review and gets merged wins the bounty
5. On acceptance, XTM payment is processed

### Notes

- AI-assisted development is expected and encouraged
- If you get stuck, ask in Discord
"""


def parse_args():
    args = sys.argv[1:]
    if len(args) < 2:
        print("Usage: add_bounty.py <repo> <issue#> <tier>", file=sys.stderr)
        print("   or: add_bounty.py <github-url> <tier>", file=sys.stderr)
        sys.exit(1)

    # Handle URL form: https://github.com/org/repo/issues/123
    url_match = re.match(r'https://github\.com/([^/]+/[^/]+)/issues/(\d+)', args[0])
    if url_match:
        repo = url_match.group(1)
        issue = int(url_match.group(2))
        tier = args[1].upper()
    else:
        repo = args[0]
        issue = int(args[1])
        tier = args[2].upper() if len(args) > 2 else None

    if tier not in TIERS:
        print(f"Error: tier must be one of {TIERS}, got '{tier}'", file=sys.stderr)
        sys.exit(1)

    return repo, issue, tier


def fetch_issue(repo, issue):
    result = subprocess.run(
        ["gh", "issue", "view", str(issue), "--repo", repo,
         "--json", "title,body,url,labels"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Error fetching {repo}#{issue}: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    return json.loads(result.stdout)


def make_slug(title):
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    return slug[:50]


def make_filename(repo, issue, title):
    short = repo.split("/")[1]
    slug = make_slug(title)
    return f"{short}-{issue}-{slug}.md"


def main():
    repo, issue, tier = parse_args()
    data = fetch_issue(repo, issue)

    title = data["title"]
    body = data.get("body", "") or ""
    url = data["url"]

    # Check if already exists
    existing = [f for f in os.listdir(ISSUES_DIR)
                if f.endswith(".md") and f"-{issue}-" in f and repo.split("/")[1] in f]
    if existing:
        print(f"Error: issue already exists as {existing[0]}", file=sys.stderr)
        sys.exit(1)

    fname = make_filename(repo, issue, title)
    fpath = os.path.join(ISSUES_DIR, fname)

    # Build context from original body (truncate if huge)
    context_text = f"- Original issue: {url}"
    if body:
        snippet = body[:500].replace('\n', '\n  ')
        context_text += f"\n- Original description:\n  {snippet}"

    content = TEMPLATE.format(
        repo=repo,
        issue=issue,
        tier=tier,
        title=title,
        description=f"TODO: Write a clear one-paragraph description based on the original issue.\n\nOriginal title: {title}",
        context=context_text,
    )

    with open(fpath, "w") as f:
        f.write(content)

    # Append to summary.csv
    csv_path = os.path.join(ISSUES_DIR, "summary.csv")
    with open(csv_path, "a") as f:
        f.write(f"{fname},{repo},{issue},{title},{url},{tier},$0,0\n")

    print(f"Created {fpath}")
    print(f"Appended to {csv_path}")
    print()
    print("Next steps:")
    print(f"  1. Edit issues/{fname} — write description & acceptance criteria")
    print(f"  2. python3 scripts/sync_issues.py issues/{fname}")
    print(f"  3. python3 scripts/generate_readme.py")


if __name__ == "__main__":
    main()
