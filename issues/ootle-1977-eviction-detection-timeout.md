---
repo: tari-project/tari-ootle
issue: 1977
labels: [bounty, bounty-M]
original_size: M
---

## Bounty: Fix Eviction Detection Timeout in Offline Validator Test

**Tier:** M — 60,000 XTM

### Description

The "Offline validator gets evicted" cucumber test times out waiting for VN1 to list VN5 as evicted. The step looks for an eviction file at `validator_node/VN1/data/layer_one_transactions` which never appears. This may be a timing issue (eviction takes longer than the test timeout allows) or the eviction proof file path/mechanism may have changed. Investigate the root cause and fix the test.

### Acceptance Criteria

- [ ] The `I wait for VN1 to list VN5 as evicted in EVICT_PROOF` step completes successfully
- [ ] "Offline validator gets evicted" scenario passes end-to-end
- [ ] Root cause is documented in the PR description (timeout too short, path changed, or logic bug)

### Context

- Issue opened by @sdbondi
- Error: `Timeout waiting for eviction file at path .../validator_node/VN1/data/layer_one_transactions`
- Affected step: `integration_tests/tests/steps/validator_node.rs:619`
- Affected scenario in `tests/features/eviction.feature`

### How It Works

1. Comment on this issue to signal intent (courtesy, not a lock)
2. Fork the repo and do the work
3. Submit a PR that references the issue with a closing keyword (e.g. `Fixes #1977`) so GitHub links your PR to the bounty automatically
4. Bounties are competitive. Multiple PRs may be submitted for the same bounty. Review comments are public, and contributors may borrow ideas from each other's work. The maintainer selects the PR that best solves the problem, considering code quality, completeness, and contributor behavior. In cases where multiple contributors made significant contributions, the maintainer may split the bounty. The maintainer's decision is final.
5. Earn XTM (processing may take up to a week; reach out to @possum on Discord with your Tari address)

### Notes

- AI-assisted development is expected and encouraged
- If you get stuck, ask in Discord
