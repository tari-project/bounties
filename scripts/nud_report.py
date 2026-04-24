#!/usr/bin/env python3
"""NUD (No Update Detected) report — flags bounty issues where a contributor
commented or submitted a PR but the maintainer has not responded.

For each open bounty issue:
  - Fetch all comments in chronological order
  - Find the last comment by a non-maintainer (contributor activity)
  - Check if the maintainer has replied AFTER that comment
  - If not → NUD flag

Output: a Markdown report grouped by maintainer, ready to share.

Usage:
    python3 scripts/nud_report.py                # write NUD.md
    python3 scripts/nud_report.py --dry-run      # print to stdout
    python3 scripts/nud_report.py --maintainer SWvheerden  # one maintainer only
"""
import subprocess, json, sys, os, re, yaml, glob
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR   = os.path.dirname(SCRIPT_DIR)
ISSUES_DIR = os.path.join(ROOT_DIR, "issues")
OUT_FILE   = os.path.join(ROOT_DIR, "NUD.md")

MAINTAINERS = {"metalaureate", "SWvheerden", "sdbondi", "stringhandler", "brianp"}

# Map repo → assigned maintainer (mirrors generate_readme.py)
REPO_MAINTAINER = {
    "tari-project/tari":               "SWvheerden",
    "tari-project/minotari-cli":       "SWvheerden",
    "tari-project/tari-ootle":         "sdbondi",
    "tari-project/universe":           "brianp",
    "tari-project/faqqer":             "metalaureate",
    "tari-project/aiteen":             "metalaureate",
    "tari-project/community-discourse":"metalaureate",
}

# Threshold: flag if last contributor comment is older than this many days
STALE_DAYS = 3


def load_issues():
    issues = []
    for fpath in sorted(glob.glob(os.path.join(ISSUES_DIR, "*.md"))):
        with open(fpath) as f:
            content = f.read()
        fm = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not fm:
            continue
        meta = yaml.safe_load(fm.group(1))
        title_m = re.search(r'^## Bounty:\s*(.+)$', content, re.MULTILINE)
        title = title_m.group(1).strip() if title_m else os.path.basename(fpath)
        tier = "?"
        for label in meta.get("labels", []):
            if label.startswith("bounty-") and label[7:] in ("S","M","L","XL"):
                tier = label[7:]

        maintainer = REPO_MAINTAINER.get(meta["repo"], "unknown")
        issues.append({
            "repo":       meta["repo"],
            "issue":      meta["issue"],
            "title":      title,
            "tier":       tier,
            "maintainer": maintainer,
            "url":        f"https://github.com/{meta['repo']}/issues/{meta['issue']}",
        })
    return issues


def fetch_issue_data(repo, issue_num):
    """Fetch state, comments (with author + timestamp), and linked PR status."""
    result = subprocess.run(
        ["gh", "issue", "view", str(issue_num), "-R", repo,
         "--json", "state,comments,closedByPullRequestsReferences"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  WARN: failed to fetch {repo}#{issue_num}: {result.stderr.strip()}", file=sys.stderr)
        return None
    return json.loads(result.stdout)


def days_ago(iso_str):
    if not iso_str:
        return 9999
    dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
    delta = datetime.now(timezone.utc) - dt
    return delta.days


def analyse_issue(issue, data):
    """Return a NUD record if the issue needs maintainer follow-up, else None."""
    state = data.get("state", "OPEN")
    if state != "OPEN":
        return None  # Skip closed issues

    maintainer = issue["maintainer"]
    comments = data.get("comments", []) or []

    # Find last comment by a contributor (non-maintainer)
    last_contributor = None
    for c in reversed(comments):
        author = (c.get("author") or {}).get("login", "")
        if author and author not in MAINTAINERS:
            last_contributor = c
            break

    if not last_contributor:
        return None  # No contributor activity, nothing to follow up on

    # Check if the maintainer replied AFTER the last contributor comment
    last_contributor_time = last_contributor.get("createdAt", "")
    maintainer_replied_after = False
    for c in comments:
        author = (c.get("author") or {}).get("login", "")
        if author == maintainer and c.get("createdAt", "") > last_contributor_time:
            maintainer_replied_after = True
            break

    if maintainer_replied_after:
        return None  # Maintainer is on top of it

    contributor_author = (last_contributor.get("author") or {}).get("login", "unknown")
    age_days = days_ago(last_contributor_time)
    snippet = last_contributor.get("body", "").strip().replace("\n", " ")[:120]

    # Count total unique contributor commenters
    contributor_commenters = {
        (c.get("author") or {}).get("login", "")
        for c in comments
        if (c.get("author") or {}).get("login", "") not in MAINTAINERS
        and (c.get("author") or {}).get("login", "")
    }

    linked_prs = data.get("closedByPullRequestsReferences", []) or []
    has_pr = bool(linked_prs)

    return {
        "url":          issue["url"],
        "title":        issue["title"],
        "repo":         issue["repo"],
        "number":       issue["issue"],
        "tier":         issue["tier"],
        "maintainer":   maintainer,
        "last_commenter": contributor_author,
        "last_comment_age": age_days,
        "last_comment_snippet": snippet,
        "contributor_count": len(contributor_commenters),
        "has_pr":       has_pr,
    }


def render_report(nuds, filter_maintainer=None):
    now = datetime.now(timezone.utc).strftime("%B %d, %Y at %H:%M UTC")
    lines = [
        "# Bounties Awaiting Maintainer Response",
        "",
        f"*Generated: {now}*",
        "",
        f"> Issues where a contributor has commented or submitted a PR but the assigned maintainer has not replied. Threshold: >{STALE_DAYS} days.",
        "",
    ]

    # Group by maintainer
    by_maintainer = {}
    for n in nuds:
        m = n["maintainer"]
        if filter_maintainer and m != filter_maintainer:
            continue
        by_maintainer.setdefault(m, []).append(n)

    if not by_maintainer:
        lines.append("✅ No open issues awaiting maintainer response.")
        return "\n".join(lines)

    total = sum(len(v) for v in by_maintainer.items())

    for maintainer in sorted(by_maintainer):
        items = sorted(by_maintainer[maintainer], key=lambda x: -x["last_comment_age"])
        lines += [
            f"## @{maintainer}  ({len(items)} issue{'s' if len(items) != 1 else ''})",
            "",
            "| Issue | Tier | Has PR | Contributors | Last Activity | Snippet |",
            "|-------|:----:|:------:|:------------:|:-------------:|---------|",
        ]
        for n in items:
            pr_flag = "🟡 Yes" if n["has_pr"] else "—"
            age_str = f"{n['last_comment_age']}d ago"
            snippet = n["last_comment_snippet"]
            if len(snippet) == 120:
                snippet += "…"
            lines.append(
                f"| [{n['repo'].split('/')[1]} #{n['number']} — {n['title']}]({n['url']}) "
                f"| {n['tier']} | {pr_flag} | {n['contributor_count']} "
                f"| @{n['last_commenter']} · {age_str} | *{snippet}* |"
            )
        lines.append("")

    return "\n".join(lines)


def main():
    dry_run = "--dry-run" in sys.argv
    filter_maintainer = None
    if "--maintainer" in sys.argv:
        idx = sys.argv.index("--maintainer")
        filter_maintainer = sys.argv[idx + 1].lstrip("@") if idx + 1 < len(sys.argv) else None

    issues = load_issues()
    print(f"Checking {len(issues)} bounties...", file=sys.stderr)

    nuds = []
    for issue in issues:
        print(f"  {issue['repo']}#{issue['issue']} ...", end=" ", file=sys.stderr, flush=True)
        data = fetch_issue_data(issue["repo"], issue["issue"])
        if data is None:
            print("skip", file=sys.stderr)
            continue
        record = analyse_issue(issue, data)
        if record:
            age = record["last_comment_age"]
            if age > STALE_DAYS:
                print(f"NUD ({age}d)", file=sys.stderr)
                nuds.append(record)
            else:
                print(f"recent ({age}d)", file=sys.stderr)
        else:
            print("ok", file=sys.stderr)

    report = render_report(nuds, filter_maintainer)

    if dry_run:
        print(report)
    else:
        with open(OUT_FILE, "w") as f:
            f.write(report + "\n")
        print(f"\nWrote {OUT_FILE} ({len(nuds)} issues flagged)", file=sys.stderr)


if __name__ == "__main__":
    main()
