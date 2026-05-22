---
repo: tari-project/tari-ootle
issue: 1974
labels: [bounty, bounty-M]
original_size: M
my_size_note: "Kept at M: touches ownership proof / cryptographic validation (risk surface rule)"
---

## Bounty: Fix Claim Burn Ownership Proof in Cucumber Tests

**Tier:** M — 60,000 XTM

### Description

Two transfer cucumber tests fail at the claim burn step with "ownership proof validation failed". The integration test's burn proof construction is out of sync with the current wallet daemon validation logic, likely after recent claim burn changes in PR #1969. Update the proof construction in the test steps to match the current validation requirements.

### Acceptance Criteria

- [ ] The `When I claim burn BURN_PROOF and spend it into account ... using wallet daemon ...` step passes
- [ ] "Transfer tokens to account that does not previously exist" scenario passes end-to-end
- [ ] "Transfer tokens to existing account" scenario passes end-to-end
- [ ] Existing claim burn scenarios in `claim_burn.feature` continue to pass

### Context

- Issue opened by @sdbondi
- Error: `Invalid param 'claim_proof.ownership_proof': ownership proof validation failed`
- Affected step: `integration_tests/tests/steps/wallet_daemon.rs:53`
- Likely caused by PR #1969 changing claim burn validation logic
- Affected scenarios in `tests/features/transfer.feature`

### How It Works

1. Comment on this issue to signal intent (courtesy, not a lock)
2. Fork the repo and do the work
3. Submit a PR that references the issue with a closing keyword (e.g. `Fixes #1974`) so GitHub links your PR to the bounty automatically
4. Bounties are competitive. Multiple PRs may be submitted for the same bounty. Review comments are public, and contributors may borrow ideas from each other's work. The maintainer selects the PR that best solves the problem, considering code quality, completeness, and contributor behavior. In cases where multiple contributors made significant contributions, the maintainer may split the bounty. The maintainer's decision is final.
5. Earn XTM (processing may take up to a week; reach out to @possum on Discord with your Tari address)

### Notes

- AI-assisted development is expected and encouraged
- If you get stuck, ask in Discord
