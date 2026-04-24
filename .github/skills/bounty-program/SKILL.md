---
name: bounty-program
description: >
  Tari bounty program management. Use when: generating the NUD (No Update Detected) report,
  evaluating contributor quality on bounty PRs, detecting bot contributors, assessing PR quality,
  identifying AI-generated PR farms, managing bounty issue files, syncing issues to GitHub,
  regenerating the bounty board README, issuing bounty payouts, recording payments, tracking
  USDC conversion rates, checking KYC status, or flagging contributors who have exceeded the
  $600 reporting threshold. Also use when asked about contributor verdicts, PR red flags,
  claiming patterns, pending payouts, or whether a contributor is a bot.
argument-hint: 'nud | eval-contributors | pending-payouts | record-payment | kyc-status | add-bounty <repo> <issue#> <tier> | sync | readme'
---

# Tari Bounty Program

This workspace manages bounty issue descriptions as local Markdown files. Full workflow
documented in `AGENTS.md`. This skill covers the three recurring operational tasks:

---

## 1. NUD Report (No Update Detected)

Flags issues where a contributor commented or submitted a PR but the maintainer hasn't replied.

```bash
python3 scripts/nud_report.py          # writes NUD.md
python3 scripts/nud_report.py --dry-run
python3 scripts/nud_report.py --maintainer brianp
```

Threshold: >3 days since last contributor activity with no maintainer response.
Output: `NUD.md` grouped by maintainer.

After generating, always offer to run contributor quality evaluation on the flagged issues.

---

## 2. Contributor Quality Evaluation

For each issue flagged in the NUD report, evaluate the contributors and their PRs.

### Data Collection

For each flagged issue, fetch the full comment thread and linked PRs:

```bash
gh issue view <number> -R <repo> --json comments,closedByPullRequestsReferences
```

For each linked PR:

```bash
gh pr view <number> -R <repo> --json title,body,additions,deletions,changedFiles,commits,state
```

### Bot Detection Heuristics

Flag as **bot** if any of the following apply:

**Templated claim comments** — identical or near-identical across issues:
- *"👋 Hi there! I'm interested in working on this task. Before I start, I'd like to confirm a few details: 1. Bounty Amount..."*
- *"Claiming this bounty. Will have a PR up within the 14-day window."* (verbatim, on multiple issues)
- *"Claiming this bounty."* (bare, no substance)

**Cross-issue pattern** — same user claims 3+ issues within a few days with template comments.

**AI review loop fingerprints in commits:**
- `"address Gemini review feedback"`
- `"address Copilot review"` / `"address Claude review"`
- `"apply AI review suggestions"`
- Repeated fix/refactor commits with no corresponding code removal

**Maintainer has already called it out** — if a maintainer has explicitly said "sorry robot" or similar, treat as confirmed bot.

### PR Quality Signals

**Red flags (inflate skepticism):**
- High additions + **zero deletions** on a bug fix (over-generation, nothing was actually fixed/removed)
- PR body re-describes the issue rather than explaining the solution
- Commit history shows AI review cycle: generate → AI review → add more code → repeat
- Multiple near-identical PRs on the same issue from different suspected-bot accounts
- Bloated scope (styling extractions, irrelevant refactors) added alongside the fix

**Green signals (increase confidence):**
- Proportionate add/del ratio — bug fixes delete old code, features add new code
- Logical commit progression: introduce function → wire it → fix edge case → refactor from review (human review)
- PR body identifies **root cause**, not just symptoms
- Specific technical precision: names the registry key, the crate, the regex pattern, the file path
- Iterative improvements that show codebase familiarity (e.g., extending fix to Linux after fixing Windows)

### Verdict Categories

| Verdict | Criteria |
|---------|----------|
| **Human — good** | No bot signals, solid PR quality |
| **Human — weak** | No bot signals, but PR has quality issues |
| **Bot** | 2+ bot signals confirmed |
| **Bot (confirmed)** | Maintainer explicitly identified, or identical template across 5+ issues |
| **Unknown** | Insufficient data |

### Competing PRs

When multiple PRs are linked to the same issue, rank them:
1. Most surgical (lowest unnecessary additions, correct deletions)
2. Best root cause explanation
3. No AI review loop commits
4. Recommend closing the weaker ones with a brief reason.

### Output Format

Group by contributor. For each:

```
**@username** — issues: #X, #Y | verdict: [Human/Bot/Unknown]

- PR #N (issue #X): [brief assessment — adds/dels ratio, notable signals, recommendation]
- PR #N (issue #Y): [...]

⚠️ Red flags: [list if any]
```

Then a summary table:

| Contributor | Verdict | PRs | Recommendation |
|---|---|---|---|
| @ledgerpilot | Human — good | #3181 | Merge |
| @lunchfang | Bot | #3184, #3185 | Close |
| @0xPepeSilvia | Bot | #3182 ✓, #3183 ✓, #3180 ✗ | Merge #3182, #3183; close #3180 |

---

## 3. Payout Tracking & KYC

### Ledger

All payments are recorded in `payouts/ledger.csv`. Columns:

| Column | Description |
|--------|-------------|
| `date` | ISO-8601 date of payment (e.g. `2026-04-16`) |
| `contributor` | GitHub username |
| `github_url` | Full GitHub profile URL (e.g. `https://github.com/0xskr33p`) |
| `twitter` | Twitter/X handle including `@` (e.g. `@0xskr33p`), or empty if none found |
| `repo` | e.g. `tari-project/universe` |
| `issue` | Issue number |
| `issue_url` | Full GitHub issue URL (e.g. `https://github.com/tari-project/universe/issues/3028`) |
| `pr` | Merged PR number |
| `bounty_name` | Human-readable bounty title (from `issues/summary.csv` or local issue file) |
| `tier` | S / M / L / XL |
| `xtm_amount` | XTM issued (from `issues/summary.csv`) |
| `usdc_rate` | XTM price in USDC **at time of payment** (fetch spot price) |
| `usd_value` | `xtm_amount × usdc_rate` (computed) |
| `cumulative_usd` | Running YTD total USD for this contributor (per calendar year). Recomputed by `scripts/update_ledger_cumulative.py` |
| `kyc_status` | `not_required` / `pending` / `complete` / `exempt` |
| `notes` | Any relevant notes (e.g. "KYC docs submitted 2026-04-20") |

### Pending Payouts Workflow

To find what's owed but not yet paid:

1. For every bounty issue in `issues/summary.csv`, fetch linked PRs from the issue side:
```bash
gh issue view <number> -R <repo> --json closedByPullRequestsReferences
```
2. **Do NOT trust the `state` field inside `closedByPullRequestsReferences`** — it is always `null`. For each linked PR, individually check its real state:
```bash
gh pr view <pr_number> -R <repo> --json state,author,mergedAt -q '.state'
```
3. A PR is merged if `state == "MERGED"`.
4. Cross-reference merged PRs against `payouts/ledger.csv` by `(repo, issue)` — anything not in the ledger is pending.
5. Look up the XTM amount from `issues/summary.csv` for that issue.
6. Fetch the live XTM/USDC rate (see below) and compute USD value.
7. Output a pending payouts table:

```
## Pending Payouts

| Contributor | Issue | PR | Tier | XTM | USDC Rate | USD Value |
|---|---|---|---|---|---|---|
| @ledgerpilot | aiteen#1 | #3 | M | 60,000 | 0.0006087 | $36.52 |
```

### Recording a Payment

When the user confirms a payment was issued, append a row to `payouts/ledger.csv`:

```
2026-04-16,ledgerpilot,https://github.com/ledgerpilot,,tari-project/universe,3028,https://github.com/tari-project/universe/issues/3028,3181,Cleanup Old Binary Files After Update,S,15000,0.0042,63.00,,not_required,
```

Always ask the user to confirm: contributor, issue, PR, XTM amount, and **the USDC rate at time of payment** before writing.

**After appending rows**, always run:
```bash
python3 scripts/update_ledger_cumulative.py
```
This recomputes the `cumulative_usd` column for every row (per contributor, per calendar year, in date order).

**Contributor profile lookup:** Before recording a new contributor's first payment, visit their GitHub profile page (`https://github.com/<username>`) to find their Twitter/X handle. Record `github_url` as `https://github.com/<username>` and `twitter` as `@handle` if found, or leave empty if none. Only need to look up once per contributor — reuse from prior ledger rows for repeat payees.

### KYC Threshold Rules

**Threshold: $600 USD aggregate per contributor per calendar year.**

This is the IRS 1099-NEC reporting threshold. It applies to US persons. Since GitHub profiles don't reliably indicate nationality, apply the rule conservatively:

- The `cumulative_usd` column in the ledger tracks per-contributor YTD totals automatically (run `scripts/update_ledger_cumulative.py` after any changes).
- When a contributor's `cumulative_usd` **reaches or would exceed $600**, set `kyc_status = pending` on that payment and **hold it** until KYC is complete.
- Once `kyc_status = complete` is recorded for a contributor, subsequent payments proceed normally.
- If a contributor is confirmed non-US (explicitly stated, verifiable), `kyc_status = exempt` may be used with a note.

**KYC status check:** when asked, compute per-contributor annual totals from the ledger and output:

```
## KYC Status — Calendar Year 2026

| Contributor | YTD USD | KYC Status | Action |
|---|---|---|---|
| @ledgerpilot | $63.00 | not_required | — |
| @someContributor | $587.00 | not_required | ⚠️ Approaching $600 threshold |
| @bigContributor | $650.00 | pending | Hold payments until KYC complete |
```

**Warning threshold:** flag at $500 cumulative so you have time to initiate KYC before hitting $600.

### Getting the XTM/USDC Spot Rate

Fetch the live rate from CoinGecko before computing any payout:

```bash
curl -s "https://api.coingecko.com/api/v3/simple/price?ids=minotari&vs_currencies=usd" \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['minotari']['usd'])"
```

Or open https://www.coingecko.com/en/coins/minotari-tari and read the price directly.

Always record the **rate at time of payment** in the ledger, not today's rate if the payment was made on a prior day. If the payment date differs from today, ask the user to confirm the rate used.

---

## 4. Bounty Management

See `AGENTS.md` for full workflow. Quick reference:

**Add a new bounty:**
```bash
python3 scripts/add_bounty.py <org/repo> <issue#> <tier>
# Then rewrite the TODO placeholders per GUIDELINES.md
# Then: python3 scripts/sync_issues.py issues/<filename>.md
```

**Sync to GitHub:**
```bash
python3 scripts/sync_issues.py                         # all issues
python3 scripts/sync_issues.py issues/foo-123-bar.md   # specific file
```

**Regenerate README bounty board:**
```bash
python3 scripts/generate_readme.py
```

**Sizing tiers** (from `GUIDELINES.md`): S / M / L / XL — assume AI-assisted development.
Risk surface bump: if issue touches signing, wallet, consensus, or bridge code, go up one tier.

---

## Known Contributor Patterns (update as observed)

| Contributor | Pattern | Status |
|---|---|---|
| @lunchfang | Template claim bot — identical "👋 Hi there!" comments; @brianp confirmed "sorry robot" | Bot (confirmed) |
| @0xPepeSilvia | Bot — template claims, AI review commit loops; PRs vary in quality | Bot |
| @Tas4tari | Automated regression tester — scripted "Tested on Windows 11, version X.X.X" per release | Not a contributor |
| @ledgerpilot | Human — specific, non-templated comments; solid Rust PRs | Human |
