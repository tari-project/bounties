## Tend Integration

This project uses [Tend](https://github.com/metalaureate/tend-cli) for workflow coordination.

### Setup

Prefer the generated hook command from .github/hooks/tend.json for automated lifecycle events. Do not assume `tend` is on PATH in non-interactive shells.

If you need to run Tend manually and `tend` is not on PATH, install it:

```bash
curl -sSL https://raw.githubusercontent.com/metalaureate/tend-cli/main/bin/tend -o /usr/local/bin/tend && chmod +x /usr/local/bin/tend
```

### On Startup

1. Read `.tend/TODO` — propose pending items to the developer and ask what to work on.
2. Review recent git history for context on what's already been done.

### During Work

- `tend emit working "<description>"` — automatically emitted by hooks on each prompt, but emit manually when switching tasks.
- `tend emit done "<summary>"` — **IMPORTANT: always emit when you finish a task.** This is the primary signal that work completed.
- `tend emit stuck "<what you need>"` — emit when you cannot proceed without human input (e.g., need a decision, credentials, access, or clarification).
- `tend emit waiting "<what you're waiting for>"` — emit when blocked on an external dependency (e.g., CI, deployment, API response).

### On Completion

- Emit `tend emit done "<summary of what you accomplished>"` before going idle.
- If there are items in `.tend/TODO`, note the next item but wait for the developer to assign it (do not auto-start).

### Relay (Cloud Monitoring)

If `TEND_RELAY_TOKEN` is set in your environment, `tend emit` automatically posts events to the relay so the developer can monitor your progress in real-time.

Verify relay connectivity at startup:

```bash
echo "TEND_RELAY_TOKEN=${TEND_RELAY_TOKEN:-NOT SET}"
tend relay debug
```

If the token is not set and you are running in a remote or cloud environment, inform the developer so they can provide `TEND_RELAY_TOKEN` for your session.

### Event Format

If `tend` is not available, append a single line to `.tend/events`:

```
<ISO-8601-timestamp> <session-id> <state> <message>
```

Use `$TEND_SESSION_ID` as the session ID if set, otherwise use `_cli`.

States: `working`, `done`, `stuck`, `waiting`, `idle`.

Example:
```
2026-03-13T14:20:00 _cli working refactoring narrative engine
2026-03-13T14:45:00 _cli done refactored narrative engine (PR #204)
2026-03-13T14:46:00 _cli stuck needs database credentials for staging
```

---

## Bounty Issue Workflow

This repo manages bounty issue descriptions as local Markdown files. **Nothing touches GitHub until the developer explicitly runs the sync step.**

### Structure

```
GUIDELINES.md                    # Sizing criteria, template, label conventions
discourse_bounty_example.md      # Example bounty for reference
issues/
  summary.csv                    # CSV index: file, repo, issue#, title, URL, tier, USD, XTM
  tari-7715-lmdb-unit-tests.md   # One file per bounty issue
  ootle-1931-wallet-address-book.md
  universe-3128-seed-word-import.md
  faqqer-1-replace-with-ai-help-bot.md
  ...
scripts/
  add_bounty.py                  # Scaffold a new bounty file from a GitHub issue
  sync_issues.py                 # Push bounty bodies + labels to GitHub
  generate_readme.py             # Regenerate README.md from GitHub labels
```

### File Format

Each issue file has YAML frontmatter for sync metadata, then the bounty template body:

```yaml
---
repo: tari-project/tari          # GitHub org/repo
issue: 7715                      # GitHub issue number
labels: [bounty, bounty-M]       # Labels to apply
original_size: M                 # Size from the original issue author
my_size_note: "optional note"    # Explain any re-sizing decisions
---
```

The body follows the template in `GUIDELINES.md`: Description, Acceptance Criteria, Context, How to Claim, Notes.

### Adding a New Bounty

When the developer says "add a bounty for org/repo#123, size M":

1. Run `python3 scripts/add_bounty.py org/repo 123 M` to scaffold the file and append to CSV
2. Read the original issue content (included in the scaffolded context section)
3. Rewrite the TODO placeholders:
   - **Description**: One clear paragraph someone unfamiliar with the codebase can understand
   - **Acceptance criteria**: 3-5 items, each specific, verifiable, binary pass/fail
4. Size using the 4 dimensions in `GUIDELINES.md` (scope clarity, codebase familiarity, verification complexity, risk surface) — **assume AI-assisted development**
5. If the issue touches signing, wallet, consensus, or bridge code, bump up one tier (risk surface rule)
6. Present the file to the developer for review
7. On approval, run `python3 scripts/sync_issues.py issues/{filename}.md` to push to GitHub
8. Run `python3 scripts/generate_readme.py` to update the bounty board

### Quality Checklist

Before marking a bounty file as ready:

- **Description**: One clear paragraph understandable by someone unfamiliar with the codebase
- **Acceptance criteria**: 3-5 items, each specific, verifiable, and binary pass/fail. No hedges ("if feasible"), no vague timing ("automatically")
- **Tier**: Correct per all 4 sizing dimensions. Risk surface bump applied where needed
- **Context**: Links to relevant code paths, error messages, related issues/PRs, file paths
- **Template**: All sections present (Description, ACs, Context, How to Claim, Notes)

### Syncing to GitHub

```bash
python3 scripts/sync_issues.py                        # sync all issues
python3 scripts/sync_issues.py issues/foo-123-bar.md  # sync specific file
```

The sync script:
1. Reads each `.md` file's frontmatter (`repo`, `issue`, `labels`)
2. Preserves the original issue body as a collapsed comment (first sync only)
3. Pushes the bounty body as the issue description
4. Creates and applies labels

### Regenerating the README

```bash
python3 scripts/generate_readme.py           # write README.md
python3 scripts/generate_readme.py --dry-run # preview without writing
```

Queries GitHub for all issues with the `bounty` label, pulls tier from `bounty-S/M/L/XL` labels,
uses clean titles from local issue files. Commit and push to update the public bounty board.

**Do not edit issues on GitHub directly.** The markdown files are the source of truth.
