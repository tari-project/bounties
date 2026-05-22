---
repo: tari-project/tari
issue: 7736
labels: [bounty, bounty-M]
original_size: S
my_size_note: "Bumped from S to M: touches signing code (risk surface rule)"
---

## Bounty: Create Offline Signing Cucumber Test

**Tier:** M — 60,000 XTM

### Description

The cucumber testing suite has unit tests for offline signing but lacks a complete integration test covering the full gRPC flow. Write a cucumber test that creates a view-only wallet, initiates an offline signing process via gRPC, signs the transaction using a full-spend wallet, broadcasts via the view-only wallet, and verifies the receiving wallet confirms the funds.

### Acceptance Criteria

- [ ] A cucumber test creates a view-only wallet and starts an offline signing process via gRPC
- [ ] The transaction details are signed using a full-spend wallet
- [ ] The signed transaction is broadcast via the view-only wallet
- [ ] The receiving wallet has the funds confirmed for the test to pass

### Context

- Issue opened by @SWvheerden
- Existing offline signing unit tests: `base_layer/wallet/tests/` (search for `offline` / `one_sided`)
- gRPC service definitions: `applications/minotari_app_grpc/proto/wallet.proto`
- Existing cucumber step definitions: `integration_tests/tests/steps/wallet_steps.rs`
- Relevant code: cucumber test suite in `integration_tests/`

### How It Works

1. Comment on this issue to signal intent (courtesy, not a lock)
2. Fork the repo and do the work
3. Submit a PR that references the issue with a closing keyword (e.g. `Fixes #7736`) so GitHub links your PR to the bounty automatically
4. Bounties are competitive. Multiple PRs may be submitted for the same bounty. Review comments are public, and contributors may borrow ideas from each other's work. The maintainer selects the PR that best solves the problem, considering code quality, completeness, and contributor behavior. In cases where multiple contributors made significant contributions, the maintainer may split the bounty. The maintainer's decision is final.
5. Earn XTM (processing may take up to a week; reach out to @possum on Discord with your Tari address)

### Notes

- AI-assisted development is expected and encouraged
- If you get stuck, ask in Discord
