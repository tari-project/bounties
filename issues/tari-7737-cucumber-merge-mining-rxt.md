---
repo: tari-project/tari
issue: 7737
labels: [bounty, bounty-S]
original_size: S
---

## Bounty: Convert Merge Mining Cucumber Tests to RandomX-Tari

**Tier:** S — 15,000 XTM

### Description

The cucumber merge mining tests currently require an external Monero daemon (MoneroD) because they mine using RandomX-Monero (RxM). Convert these tests to use RandomX-Tari (RxT) instead, which does not require a MoneroD connection. This removes the external dependency and makes the test suite self-contained.

### Acceptance Criteria

- [ ] All cucumber merge mining tests mine using RxT instead of RxM
- [ ] No external MoneroD dependency is required to run the merge mining tests
- [ ] All cucumber merge mining tests pass

### Context

- Issue opened by @SWvheerden
- Relevant code: cucumber test suite in `integration_tests/`
- RxT mining does not need MoneroD, simplifying CI and local development

### How It Works

1. Comment on this issue to signal intent (courtesy, not a lock)
2. Fork the repo and do the work
3. Submit a PR that references the issue with a closing keyword (e.g. `Fixes #7737`) so GitHub links your PR to the bounty automatically
4. Bounties are competitive. Multiple PRs may be submitted for the same bounty. Review comments are public, and contributors may borrow ideas from each other's work. The maintainer selects the PR that best solves the problem, considering code quality, completeness, and contributor behavior. In cases where multiple contributors made significant contributions, the maintainer may split the bounty. The maintainer's decision is final.
5. Earn XTM (processing may take up to a week; reach out to @possum on Discord with your Tari address)

### Notes

- AI-assisted development is expected and encouraged
- If you get stuck, ask in Discord
