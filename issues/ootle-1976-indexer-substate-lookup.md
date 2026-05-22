---
repo: tari-project/tari-ootle
issue: 1976
labels: [bounty, bounty-S]
original_size: S
---

## Bounty: Fix Indexer Substate Lookup in Wallet Daemon Test

**Tier:** S — 15,000 XTM

### Description

The "Wallet daemon is able to connect to indexer" cucumber test fails with a 404 when querying the indexer for a substate version. The indexer hasn't synced the substate before the assertion runs. The steps prior to the failing assertion (template publish, counter invoke) all succeed, so the substate exists on-chain but the indexer hasn't indexed it in time. Add a wait/retry mechanism before the substate version check.

### Acceptance Criteria

- [ ] The `the indexer INDEXER returns version 1 for substate COUNTER/components/Counter` step passes
- [ ] The "Wallet daemon is able to connect to indexer" scenario passes end-to-end
- [ ] A wait/retry mechanism is added for indexer sync before the substate version check

### Context

- Issue opened by @sdbondi
- Error: `ErrorResponse { source: reqwest::Error { kind: Status(404) }, details: Some("Substate component_... not found") }`
- Affected step: `integration_tests/tests/steps/indexer.rs:178`
- Affected scenario in `tests/features/indexer.feature`
- The `local_search_only=true` query parameter may also be too restrictive

### How It Works

1. Comment on this issue to signal intent (courtesy, not a lock)
2. Fork the repo and do the work
3. Submit a PR that references the issue with a closing keyword (e.g. `Fixes #1976`) so GitHub links your PR to the bounty automatically
4. Bounties are competitive. Multiple PRs may be submitted for the same bounty. Review comments are public, and contributors may borrow ideas from each other's work. The maintainer selects the PR that best solves the problem, considering code quality, completeness, and contributor behavior. In cases where multiple contributors made significant contributions, the maintainer may split the bounty. The maintainer's decision is final.
5. Earn XTM (processing may take up to a week; reach out to @possum on Discord with your Tari address)

### Notes

- AI-assisted development is expected and encouraged
- If you get stuck, ask in Discord
