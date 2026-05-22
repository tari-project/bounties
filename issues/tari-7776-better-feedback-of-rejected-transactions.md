---
repo: tari-project/tari
issue: 7776
labels: [bounty, bounty-M]
original_size: M
---

## Bounty: Better Feedback of Rejected Transactions

**Tier:** M — 60,000 XTM

### Description

When a base node's mempool rejects a wallet transaction, the wallet currently receives only a generic "validation failure" message. Extend the HTTP interface to propagate the specific rejection reason (e.g., double-spend of commitment X, insufficient fee, invalid range proof) so the wallet can display actionable feedback to the user. The change must be backward-compatible — older wallets that don't understand the new fields must continue to function normally.

### Acceptance Criteria

- [ ] The wallet receives a specific, human-readable reason when the mempool rejects a transaction (not just a generic validation error)
- [ ] The rejection reason identifies the exact failure (e.g., which commitment was double-spent, which rule was violated)
- [ ] Older wallet versions continue to work correctly against a base node with this change (backward-compatible HTTP response)
- [ ] At least one integration or cucumber test verifies that a rejected transaction surfaces the detailed reason to the wallet

### Context

- Original issue: https://github.com/tari-project/tari/issues/7776
- The mempool validation logic already knows the specific reason; this is about surfacing it through the HTTP API
- Must only modify the HTTP interface (not gRPC) per the original issue constraints

### How It Works

1. Comment on this issue to signal intent (courtesy, not a lock)
2. Fork the repo and do the work
3. Submit a PR that references the issue with a closing keyword (e.g. `Fixes #7776`) so GitHub links your PR to the bounty automatically
4. Bounties are competitive. Multiple PRs may be submitted for the same bounty. Review comments are public, and contributors may borrow ideas from each other's work. The maintainer selects the PR that best solves the problem, considering code quality, completeness, and contributor behavior. In cases where multiple contributors made significant contributions, the maintainer may split the bounty. The maintainer's decision is final.
5. Earn XTM (processing may take up to a week; reach out to @possum on Discord with your Tari address)

### Notes

- AI-assisted development is expected and encouraged
- If you get stuck, ask in Discord
