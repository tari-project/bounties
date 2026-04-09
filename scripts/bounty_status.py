#!/usr/bin/env python3
"""Check claim status of all bounty issues and produce a Markdown report.

Reads issues/*.md for metadata, fetches comments from GitHub, and classifies
each bounty as: PR Submitted, Claimed, Interest, or Open.

Tracks state between runs so you can see what changed.

Usage:
    python3 scripts/bounty_status.py                # write STATUS.md, show changes
    python3 scripts/bounty_status.py --dry-run      # print to stdout only
"""
import subprocess, json, sys, os, re, yaml, glob
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
ISSUES_DIR = os.path.join(ROOT_DIR, "issues")
STATE_FILE = os.path.join(ROOT_DIR, ".scratch", "bounty_state.json")

TIER_XTM = {"S": "15,000", "M": "60,000", "L": "150,000", "XL": "450,000"}

# Maintainers / leads whose confirmation counts as assignment
LEADS = {"metalaureate", "SWvheerden", "sdbondi", "stringhandler", "brianp"}

# Signals that a comment is claiming or expressing intent
CLAIM_SIGNALS = [
    r"(?:i['\u2019]?d like to|i want to|i am|i'm)\s+(?:claim|work on|take|pick up|start)",
    r"claiming this",
    r"assign\s+(?:this\s+)?to me",
    r"working on this",
    r"(?:my |i )pr\s+(?:submitted|already open|opened)",
    r"pr submitted",
    r"/attempt",
    r"can i start",
    r"interested in (?:picking|working|taking)",
    r"i would (?:like to|be happy to|love to)\s+(?:work|take|claim|pick)",
]
CLAIM_RE = re.compile("|".join(CLAIM_SIGNALS), re.IGNORECASE)

# Signals a lead confirmed an assignment
CONFIRM_SIGNALS = [
    r"(?:absolutely|perfect|thanks|assigned|go ahead|confirmed|approved)",
]
CONFIRM_RE = re.compile("|".join(CONFIRM_SIGNALS), re.IGNORECASE)

# Bot-like or low-quality comments to discount
BOT_SIGNALS = [
    r"bounty amount.*TBD",
    r"acceptance criteria.*what exactly",
    r"Automated by.*OpenCode",
    r"this is still an issue",
]
BOT_RE = re.compile("|".join(BOT_SIGNALS), re.IGNORECASE)


def load_issues():
    """Load all issue metadata from local files."""
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
            if label.startswith("bounty-"):
                tier = label[7:]
        issues.append({
            "file": os.path.basename(fpath),
            "repo": meta["repo"],
            "issue": meta["issue"],
            "title": title,
            "tier": tier,
        })
    return issues


def fetch_comments(repo, issue):
    """Fetch comments for a single issue."""
    result = subprocess.run(
        ["gh", "issue", "view", str(issue), "-R", repo,
         "--json", "comments",
         "--jq", '.comments[] | {author: .author.login, body: .body, created: .createdAt}'],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return []
    comments = []
    for line in result.stdout.strip().split("\n"):
        if not line:
            continue
        try:
            comments.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return comments


def fetch_prs(repo, issue):
    """Check if there's a linked/mentioned PR."""
    result = subprocess.run(
        ["gh", "issue", "view", str(issue), "-R", repo,
         "--json", "timelineItems",
         "--jq", '.timelineItems[] | select(.typename == "CrossReferencedEvent") | .source.url // empty'],
        capture_output=True, text=True
    )
    prs = [u.strip() for u in result.stdout.strip().split("\n") if u.strip() and "/pull/" in u]
    return prs


def classify(repo, comments, prs):
    """Classify an issue's claim status from its comments and linked PRs.

    Returns a dict with:
        status: "PR Submitted" | "Claimed" | "Interest" | "Open"
        first_claimant: {author, date} or None
        all_claimants: [{author, date}]
        confirmed_by: lead username or None
        pr_links: [urls]
    """
    claim_records = []   # [{author, date}]
    confirmed_by = None
    has_pr = bool(prs)
    pr_submitter = None
    pr_links = list(prs)

    for c in comments:
        author = c.get("author", "")
        body = c.get("body", "")
        created = c.get("created", "")
        date_str = created[:10] if created else ""

        # Lead comments: check for confirmation (only counts if someone already claimed)
        if author in LEADS:
            if claim_records and CONFIRM_RE.search(body):
                # Check if the lead is @-mentioning a claimant
                for rec in claim_records:
                    if f"@{rec['author']}" in body:
                        confirmed_by = author
                        break
                else:
                    # No explicit mention, but if they replied after a claim, likely confirming
                    confirmed_by = author
            continue

        if BOT_RE.search(body):
            continue

        # Check for PR submission (must be the commenter's own PR)
        pr_submit = re.search(
            r'(?:(?:my |i |pr submitted|pr already open|pr opened).*?(?:https?://\S+/pull/)(\d+)'
            r'|(?:https?://\S+/pull/)(\d+).*(?:submitted|opened|created))',
            body, re.IGNORECASE
        )
        if not pr_submit:
            pr_submit = re.search(
                r'(?:pr\s*#(\d+)\s+is\s+(?:already\s+)?open|pr\s+submitted.*?#(\d+))',
                body, re.IGNORECASE
            )
        if pr_submit:
            has_pr = True
            pr_submitter = author
            pr_num = next((g for g in pr_submit.groups() if g), None)
            if pr_num:
                url = f'https://github.com/{repo}/pull/{pr_num}'
                if url not in pr_links:
                    pr_links.append(url)

        if CLAIM_RE.search(body):
            if not any(r["author"] == author for r in claim_records):
                claim_records.append({"author": author, "date": date_str})

    first = claim_records[0] if claim_records else None

    if has_pr:
        submitter = pr_submitter or (first["author"] if first else "unknown")
        status = "PR Submitted"
    elif claim_records and confirmed_by:
        status = "Claimed"
    elif claim_records:
        status = "Interest"
    else:
        status = "Open"

    return {
        "status": status,
        "first_claimant": first,
        "all_claimants": claim_records,
        "confirmed_by": confirmed_by,
        "pr_links": pr_links,
    }


def load_previous_state():
    """Load the previous run's state from JSON."""
    if not os.path.exists(STATE_FILE):
        return {}
    with open(STATE_FILE) as f:
        return json.load(f)


def save_state(issues, results):
    """Save current state for next run's diff."""
    state = {}
    for issue, r in zip(issues, results):
        key = f"{issue['repo']}#{issue['issue']}"
        claimant_names = [c["author"] for c in r["all_claimants"]]
        state[key] = {
            "status": r["status"],
            "claimants": claimant_names,
            "confirmed_by": r["confirmed_by"],
            "title": issue["title"],
            "tier": issue["tier"],
        }
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def compute_changes(issues, results, prev_state):
    """Compute what changed since last run."""
    changes = []
    for issue, r in zip(issues, results):
        key = f"{issue['repo']}#{issue['issue']}"
        prev = prev_state.get(key)
        claimant_names = [c["author"] for c in r["all_claimants"]]
        if not prev:
            changes.append((issue, "NEW", None, r["status"], claimant_names))
            continue
        if prev["status"] != r["status"]:
            changes.append((issue, "STATUS", prev["status"], r["status"], claimant_names))
        elif set(prev.get("claimants", [])) != set(claimant_names):
            new_claimants = [c for c in claimant_names if c not in prev.get("claimants", [])]
            if new_claimants:
                changes.append((issue, "NEW_CLAIMANT", prev["status"], r["status"], new_claimants))
    return changes


def render_report(issues, results, changes, prev_state):
    """Render the status report as Markdown."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Bounty Status Report",
        "",
        f"Generated: {now}",
        "",
    ]

    # Changes section (only if there's a previous run to compare against)
    if prev_state:
        if changes:
            lines.append("## Changes Since Last Run")
            lines.append("")
            for issue, change_type, old_status, new_status, claimants in changes:
                repo_short = issue["repo"].split("/")[1]
                ref = f'{repo_short}#{issue["issue"]}'
                url = f'https://github.com/{issue["repo"]}/issues/{issue["issue"]}'
                if change_type == "NEW":
                    lines.append(f"- **NEW** [{ref}]({url}) {issue['title']} ({new_status})")
                elif change_type == "STATUS":
                    claimant_str = ", ".join(f"@{c}" for c in claimants) if claimants else ""
                    lines.append(f"- **{old_status} \u2192 {new_status}** [{ref}]({url}) {issue['title']} {claimant_str}")
                elif change_type == "NEW_CLAIMANT":
                    claimant_str = ", ".join(f"@{c}" for c in claimants)
                    lines.append(f"- **New interest** [{ref}]({url}) {issue['title']} from {claimant_str}")
            lines.append("")
        else:
            lines.append("## Changes Since Last Run")
            lines.append("")
            lines.append("No changes.")
            lines.append("")

    # Action needed section
    action_items = []
    for issue, r in zip(issues, results):
        if r["status"] == "Interest" and r["all_claimants"]:
            action_items.append((issue, r, "Claim waiting for lead confirmation"))
        elif r["status"] == "PR Submitted":
            action_items.append((issue, r, "PR needs review"))

    if action_items:
        lines.append("## Action Needed")
        lines.append("")
        lines.append("| Issue | Repo | First Claim | Other Interest | Action |")
        lines.append("|-------|------|-------------|----------------|--------|")
        for issue, r, action in action_items:
            repo_short = issue["repo"].split("/")[1]
            url = f'https://github.com/{issue["repo"]}/issues/{issue["issue"]}'
            first = r["first_claimant"]
            first_str = f'@{first["author"]} ({first["date"]})' if first else ""
            others = [c for c in r["all_claimants"] if c != first] if first else []
            others_str = ", ".join(f'@{c["author"]}' for c in others) if others else ""
            lines.append(f"| [#{issue['issue']}]({url}) {issue['title']} | {repo_short} | {first_str} | {others_str} | {action} |")
        lines.append("")

    # Summary
    buckets = {"PR Submitted": [], "Claimed": [], "Interest": [], "Open": []}
    for issue, r in zip(issues, results):
        buckets[r["status"]].append((issue, r))

    total = len(issues)
    lines.append("## Summary")
    lines.append("")
    lines.append(f"| Status | Count |")
    lines.append(f"|--------|------:|")
    for status in ["PR Submitted", "Claimed", "Interest", "Open"]:
        count = len(buckets[status])
        if count:
            lines.append(f"| {status} | {count} |")
    lines.append(f"| **Total** | **{total}** |")
    lines.append("")

    # Detail table
    lines.append("## All Bounties")
    lines.append("")
    lines.append("| Issue | Repo | Tier | XTM | Status | First Claim | Confirmed By | Others |")
    lines.append("|-------|------|:----:|----:|--------|-------------|:------------:|--------|")

    status_order = {"PR Submitted": 0, "Claimed": 1, "Interest": 2, "Open": 3}
    tier_order = {"XL": 0, "L": 1, "M": 2, "S": 3}
    all_rows = []
    for issue, r in zip(issues, results):
        all_rows.append((issue, r))

    all_rows.sort(key=lambda row: (status_order.get(row[1]["status"], 9), tier_order.get(row[0]["tier"], 9)))

    for issue, r in all_rows:
        repo_short = issue["repo"].split("/")[1]
        url = f'https://github.com/{issue["repo"]}/issues/{issue["issue"]}'
        xtm = TIER_XTM.get(issue["tier"], "?")
        first = r["first_claimant"]
        first_str = f'@{first["author"]} ({first["date"]})' if first else ""
        confirmed_str = f'@{r["confirmed_by"]}' if r["confirmed_by"] else ""
        others = [c for c in r["all_claimants"] if c != first] if first else []
        others_str = ", ".join(f'@{c["author"]}' for c in others) if others else ""
        pr_str = " ".join(f'[PR]({u})' for u in r["pr_links"]) if r["pr_links"] else ""
        notes = pr_str
        lines.append(
            f"| [#{issue['issue']}]({url}) {issue['title']} "
            f"| {repo_short} | {issue['tier']} | {xtm} "
            f"| {r['status']} | {first_str} | {confirmed_str} | {others_str} {notes} |"
        )

    lines.append("")
    return "\n".join(lines)


def main():
    dry_run = "--dry-run" in sys.argv
    issues = load_issues()
    prev_state = load_previous_state()

    if prev_state:
        print(f"Checking {len(issues)} bounties (comparing against previous run)...", file=sys.stderr)
    else:
        print(f"Checking {len(issues)} bounties (first run, no previous state)...", file=sys.stderr)

    results = []
    for issue in issues:
        repo = issue["repo"]
        num = issue["issue"]
        print(f"  {repo}#{num}...", file=sys.stderr, end=" ", flush=True)
        comments = fetch_comments(repo, num)
        prs = fetch_prs(repo, num)
        r = classify(repo, comments, prs)
        results.append(r)
        label = r["status"]
        if r["first_claimant"]:
            label += f" (@{r['first_claimant']['author']} {r['first_claimant']['date']})"
            if r["confirmed_by"]:
                label += f" confirmed by @{r['confirmed_by']}"
        print(label, file=sys.stderr)

    changes = compute_changes(issues, results, prev_state)
    report = render_report(issues, results, changes, prev_state)

    # Print changes summary to stderr
    if prev_state and changes:
        print(f"\n--- {len(changes)} change(s) since last run ---", file=sys.stderr)
        for issue, change_type, old_status, new_status, claimants in changes:
            repo_short = issue["repo"].split("/")[1]
            ref = f'{repo_short}#{issue["issue"]}'
            if change_type == "STATUS":
                c_str = f" ({', '.join(f'@{c}' for c in claimants)})" if claimants else ""
                print(f"  {old_status} -> {new_status}: {ref}{c_str}", file=sys.stderr)
            elif change_type == "NEW_CLAIMANT":
                print(f"  New interest: {ref} from {', '.join(f'@{c}' for c in claimants)}", file=sys.stderr)
            elif change_type == "NEW":
                print(f"  New bounty: {ref} ({new_status})", file=sys.stderr)
    elif prev_state:
        print("\nNo changes since last run.", file=sys.stderr)

    if dry_run:
        print(report)
    else:
        out_path = os.path.join(ROOT_DIR, "STATUS.md")
        with open(out_path, "w") as f:
            f.write(report)
        save_state(issues, results)
        print(f"\nWrote STATUS.md ({len(issues)} bounties)", file=sys.stderr)


if __name__ == "__main__":
    main()
