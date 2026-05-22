---
repo: tari-project/minotari-cli
issue: 119
labels: [bounty, bounty-L]
original_size: L
---

## Bounty: Migration from Console Wallet

**Tier:** L — 150,000 XTM

### Description

Implement a migration path that imports an already-synced console wallet database into the new wallet format. The migrated wallet must preserve display transaction IDs so that users see the same transaction history they had in the console wallet. Importing from a pre-synced database avoids the slow full-chain rescan that would otherwise be required via a base node.

### Acceptance Criteria

- [ ] A CLI command or workflow accepts a synced console wallet database file and imports it into the new wallet
- [ ] All completed transactions from the console wallet appear in the new wallet with identical display transaction IDs
- [ ] The migrated wallet shows the same balance as the source console wallet
- [ ] The migrated wallet contains the same set of unspent outputs as the source
- [ ] A test or demonstration proves round-trip correctness (export → import → verify balance and transaction IDs match)

### Context

- Original issue: https://github.com/tari-project/minotari-cli/issues/119
- The console wallet stores transaction history in a local SQLite database
- Display transaction IDs are the primary user-facing identifier and must not change during migration
- Risk surface: touches wallet balances and transaction state — sized L accordingly

### How It Works

1. Comment on this issue to signal intent (courtesy, not a lock)
2. Fork the repo and do the work
3. Submit a PR that references the issue with a closing keyword (e.g. `Fixes #119`) so GitHub links your PR to the bounty automatically
4. Bounties are competitive. Multiple PRs may be submitted for the same bounty. Review comments are public, and contributors may borrow ideas from each other's work. The maintainer selects the PR that best solves the problem, considering code quality, completeness, and contributor behavior. In cases where multiple contributors made significant contributions, the maintainer may split the bounty. The maintainer's decision is final.
5. Earn XTM (processing may take up to a week; reach out to @possum on Discord with your Tari address)

### Notes

- AI-assisted development is expected and encouraged
- If you get stuck, ask in Discord
