---
repo: tari-project/minotari-cli
issue: 113
labels: [bounty, bounty-M]
original_size: S
my_size_note: "Bumped from S to M: touches wallet reorg handling (risk surface rule)"
---

## Bounty: Add Payref Tracking to Wallet

**Tier:** M — 60,000 XTM

### Description

The payment reference (payref) is computed as the hash of the commitment and mined block hash. If a reorg moves a transaction to a different block, the payref changes and the old one becomes stale. Add a tracking table that stores previous payrefs alongside the transaction ID, and update the existing query endpoints to also search this table so that lookups by old payrefs still return the correct transaction.

### Acceptance Criteria

- [ ] A new database table stores old payrefs with their transaction ID and relevant output hash when a block reorg changes a transaction's payref
- [ ] The endpoint `/accounts/{name}/completed_transactions/by_payref/{payref}` also searches the tracking table and returns the correct transaction
- [ ] The endpoint `/accounts/{name}/displayed_transactions/by_payref/{payref}` also searches the tracking table and returns the correct transaction

### Context

- Issue opened by @SWvheerden
- PR #114 is already open from @Stackwyre — review status unknown
- Relevant code: `minotari-cli` wallet database and REST endpoints

### How It Works

1. Comment on this issue to signal intent (courtesy, not a lock)
2. Fork the repo and do the work
3. Submit a PR that references the issue with a closing keyword (e.g. `Fixes #113`) so GitHub links your PR to the bounty automatically
4. Bounties are competitive. Multiple PRs may be submitted for the same bounty. Review comments are public, and contributors may borrow ideas from each other's work. The maintainer selects the PR that best solves the problem, considering code quality, completeness, and contributor behavior. In cases where multiple contributors made significant contributions, the maintainer may split the bounty. The maintainer's decision is final.
5. Earn XTM (processing may take up to a week; reach out to @possum on Discord with your Tari address)

### Notes

- AI-assisted development is expected and encouraged
- If you get stuck, ask in Discord
