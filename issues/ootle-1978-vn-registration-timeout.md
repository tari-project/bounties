---
repo: tari-project/tari-ootle
issue: 1978
labels: [bounty, bounty-M]
original_size: M
---

## Bounty: Fix VN Registration Detection Timeout in State Sync Test

**Tier:** M — 60,000 XTM

### Description

The "New validator node registers and syncs" cucumber test times out waiting for VN2 to report itself as registered after sending a registration transaction. The miner mines to the next epoch, but VN2 gets stuck at block height 40 and never picks up its registration. This could be a race condition where VN2 hasn't processed the block containing its registration, or the epoch boundary logic doesn't trigger registration pickup in time.

### Acceptance Criteria

- [ ] The `the validator node VN2 is listed as registered` step passes
- [ ] "New validator node registers and syncs" scenario passes end-to-end
- [ ] Investigation confirms whether the `mines to the next epoch` step mines enough blocks for VN2 to see the registration

### Context

- Issue opened by @sdbondi
- Error: `Timed out waiting for validator node to pick up registration (current block height: 40)`
- Affected step: `integration_tests/tests/steps/validator_node.rs:255`
- Affected scenario in `tests/features/state_sync.feature`

### How It Works

1. Comment on this issue to signal intent (courtesy, not a lock)
2. Fork the repo and do the work
3. Submit a PR that references the issue with a closing keyword (e.g. `Fixes #1978`) so GitHub links your PR to the bounty automatically
4. Bounties are competitive. Multiple PRs may be submitted for the same bounty. Review comments are public, and contributors may borrow ideas from each other's work. The maintainer selects the PR that best solves the problem, considering code quality, completeness, and contributor behavior. In cases where multiple contributors made significant contributions, the maintainer may split the bounty. The maintainer's decision is final.
5. Earn XTM (processing may take up to a week; reach out to @possum on Discord with your Tari address)

### Notes

- AI-assisted development is expected and encouraged
- If you get stuck, ask in Discord
