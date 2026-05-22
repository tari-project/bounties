---
repo: tari-project/tari-ootle
issue: 1975
labels: [bounty, bounty-S]
original_size: S
---

## Bounty: Fix Event Topic Assertion in Indexer Cucumber Test

**Tier:** S — 15,000 XTM

### Description

The cucumber test expects the event topic `std.vault.pay_fee` but the system now emits `Account.pay_fee` after a refactor. Update the test assertion in `integration_tests/tests/steps/indexer.rs` to use the correct current event topic names.

### Acceptance Criteria

- [ ] The `indexer INDEXER scans the network events for account ACC_1 with topics ...` step uses the correct current topic names
- [ ] "Indexer GraphQL requests events over network substate indexing" scenario passes end-to-end
- [ ] No other indexer test assertions are broken by the topic name change

### Context

- Issue opened by @sdbondi
- Error: `Unexpected topic at index 1. Events emitted were {std.component.created, Account.pay_fee}. Expected topic std.vault.pay_fee`
- Affected step: `integration_tests/tests/steps/indexer.rs:99`
- Affected scenario in `tests/features/indexer.feature`
- @0xskr33p has expressed interest in working on this

### How It Works

1. Comment on this issue to signal intent (courtesy, not a lock)
2. Fork the repo and do the work
3. Submit a PR that references the issue with a closing keyword (e.g. `Fixes #1975`) so GitHub links your PR to the bounty automatically
4. Bounties are competitive. Multiple PRs may be submitted for the same bounty. Review comments are public, and contributors may borrow ideas from each other's work. The maintainer selects the PR that best solves the problem, considering code quality, completeness, and contributor behavior. In cases where multiple contributors made significant contributions, the maintainer may split the bounty. The maintainer's decision is final.
5. Earn XTM (processing may take up to a week; reach out to @possum on Discord with your Tari address)

### Notes

- AI-assisted development is expected and encouraged
- If you get stuck, ask in Discord
