#!/usr/bin/env python3
"""Generate README.md bounty board from GitHub issue labels.

Queries all repos for issues labeled 'bounty', extracts tier from
bounty-S/M/L/XL labels, and uses local issue file titles for clean display.

Requires: gh CLI authenticated, PyYAML installed.

Usage:
    python3 scripts/generate_readme.py          # write README.md
    python3 scripts/generate_readme.py --dry-run # print to stdout only
"""
import subprocess, json, sys, os, re, yaml
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)

REPOS = [
    "tari-project/tari",
    "tari-project/minotari-cli",
    "tari-project/tari-ootle",
    "tari-project/universe",
    "tari-project/faqqer",
    "tari-project/aiteen",
    "tari-project/community-discourse",
    "tari-project/wxtm-bridge-frontend",
]

TIER_ORDER = {"L": 0, "M": 1, "S": 2, "XL": -1}


def load_local_titles():
    """Build lookup of clean titles from local issue files (repo#number -> title)."""
    titles = {}
    issues_dir = os.path.join(ROOT_DIR, "issues")
    if not os.path.isdir(issues_dir):
        return titles
    for fname in os.listdir(issues_dir):
        if not fname.endswith(".md"):
            continue
        with open(os.path.join(issues_dir, fname)) as f:
            content = f.read()
        m = re.search(r'^## Bounty:\s*(.+)$', content, re.MULTILINE)
        if not m:
            continue
        fm = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not fm:
            continue
        meta = yaml.safe_load(fm.group(1))
        key = f"{meta['repo']}#{meta['issue']}"
        titles[key] = m.group(1).strip()
    return titles


def fetch_bounty_issues(local_titles):
    """Query GitHub for all issues with the 'bounty' label (open + closed)."""
    issues = []
    for repo in REPOS:
        short = repo.split("/")[1]
        result = subprocess.run(
            ["gh", "issue", "list", "-R", repo, "--label", "bounty", "--state", "all",
             "--json", "number,title,labels,url,state,comments,closedByPullRequestsReferences",
             "--limit", "100"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"WARN: failed to query {repo}: {result.stderr.strip()}", file=sys.stderr)
            continue
        for item in json.loads(result.stdout):
            tier = "?"
            for label in item["labels"]:
                name = label["name"]
                if name.startswith("bounty-") and name[7:] in TIER_ORDER:
                    tier = name[7:]
                    break
            key = f"{repo}#{item['number']}"
            title = local_titles.get(key, item["title"])
            linked_prs = item.get("closedByPullRequestsReferences", []) or []
            open_prs = []
            for pr in linked_prs:
                pr_num = pr["number"]
                pr_url = pr["url"]
                # Check PR state
                pr_result = subprocess.run(
                    ["gh", "pr", "view", str(pr_num), "-R", repo,
                     "--json", "state", "-q", ".state"],
                    capture_output=True, text=True
                )
                pr_state = pr_result.stdout.strip() if pr_result.returncode == 0 else "UNKNOWN"
                open_prs.append({"number": pr_num, "url": pr_url, "state": pr_state})
            state = item.get("state", "OPEN")
            if state == "CLOSED" and any(pr["state"] == "MERGED" for pr in open_prs):
                status = "Merged"
            elif any(pr["state"] == "OPEN" for pr in open_prs):
                status = "PR Open"
            elif state == "CLOSED":
                status = "Closed"
            else:
                status = "Open"
            issues.append({
                "repo": short,
                "number": item["number"],
                "title": title,
                "url": item["url"],
                "tier": tier,
                "status": status,
                "prs": open_prs,
                "comments": len(item.get("comments", [])),
            })
    # Sort: Open first, then PR Open, then Merged/Closed; within group by tier
    status_order = {"Open": 0, "PR Open": 1, "Merged": 2, "Closed": 3}
    issues.sort(key=lambda i: (status_order.get(i["status"], 99),
                                TIER_ORDER.get(i["tier"], 99),
                                i["repo"], i["number"]))
    return issues


MAINTAINERS = {
    "tari": "SWvheerden",
    "minotari-cli": "SWvheerden",
    "tari-ootle": "sdbondi",
    "universe": "brianp",
    "faqqer": "metalaureate",
    "aiteen": "metalaureate",
    "community-discourse": "metalaureate",
    "wxtm-bridge-frontend": "brianp",
}

TIER_PRICING = {
    "S":  {"xtm": "15,000"},
    "M":  {"xtm": "60,000"},
    "L":  {"xtm": "150,000"},
    "XL": {"xtm": "450,000"},
}


def render_readme(issues):
    """Render the README markdown from a list of issues."""
    lines = [
        "# Tari Bounty Program",
        "",
        "Open bounties for the Tari ecosystem. Pick one, ship it, get paid.",
        "",
        "## How It Works",
        "",
        "1. Browse the bounty board below",
        "2. Comment on the GitHub issue to signal intent (courtesy, not a lock)",
        "3. Fork the repo and do the work",
        "4. Submit a PR that references the issue with a closing keyword (e.g. `Fixes #1234`) so GitHub links your PR to the bounty automatically",
        "5. First PR that passes review and gets merged wins the bounty",
        "6. Get paid in XTM",
        "",
        "## Bounty Board",
        "",
        "| Issue | Repo | Tier | XTM | Maintainer | Status | PRs | Activity |",
        "|-------|------|:----:|----:|-----------|--------|:---:|:--------:|",
    ]
    tier_counts = {}
    total_xtm = 0
    xtm_vals = {"S": 15000, "M": 60000, "L": 150000, "XL": 450000}
    for i in issues:
        t = i["tier"]
        tier_counts[t] = tier_counts.get(t, 0) + 1
        total_xtm += xtm_vals.get(t, 0)
        p = TIER_PRICING.get(t, {"xtm": "?"})
        # Format PR links
        pr_parts = []
        for pr in i["prs"]:
            icon = "\u2705" if pr["state"] == "MERGED" else "\U0001f7e1"
            pr_parts.append(f'[{icon} #{pr["number"]}]({pr["url"]})')
        pr_cell = " ".join(pr_parts) if pr_parts else "\u2014"
        # Format status
        status = i["status"]
        if status == "Merged":
            status_cell = "\u2705 Merged"
        elif status == "PR Open":
            status_cell = "\U0001f7e1 PR Open"
        elif status == "Closed":
            status_cell = "\u26ab Closed"
        else:
            status_cell = "\U0001f7e2 Open"
        # Activity (comment count)
        comments = i["comments"]
        activity = f'\U0001f4ac {comments}' if comments > 0 else "\u2014"
        maintainer = MAINTAINERS.get(i["repo"], "?")
        lines.append(
            f'| [#{i["number"]} \u2014 {i["title"]}]({i["url"]}) '
            f'| {i["repo"]} | {t} | {p["xtm"]} '
            f'| @{maintainer} | {status_cell} | {pr_cell} | {activity} |'
        )
    lines.append("")
    lines.append(f"**{len(issues)} bounties \u2014 {total_xtm:,} XTM**")
    lines.append("")
    updated = datetime.now(timezone.utc).strftime("%B %-d, %Y at %H:%M UTC")
    lines.append(f"*Last updated: {updated}*")
    lines.append("")
    lines.append("### Tier Summary")
    lines.append("")
    lines.append("| Tier | Count | XTM |")
    lines.append("|:----:|:-----:|----:|")
    for tier in ["S", "M", "L", "XL"]:
        if tier in tier_counts:
            p = TIER_PRICING[tier]
            lines.append(f"| {tier} | {tier_counts[tier]} | {p['xtm']} |")
    lines.append("")
    return "\n".join(lines)


def main():
    dry_run = "--dry-run" in sys.argv
    local_titles = load_local_titles()
    issues = fetch_bounty_issues(local_titles)
    readme = render_readme(issues)

    if dry_run:
        print(readme)
    else:
        readme_path = os.path.join(ROOT_DIR, "README.md")
        with open(readme_path, "w") as f:
            f.write(readme)
        print(f"Wrote README.md ({len(issues)} issues from GitHub labels)", file=sys.stderr)


if __name__ == "__main__":
    main()
