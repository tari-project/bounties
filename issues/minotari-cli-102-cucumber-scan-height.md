---
repo: tari-project/minotari-cli
issue: 102
labels: [bounty, bounty-S]
original_size: S
---

## Bounty: Fix Cucumber Wallet Scan Height Validation

**Tier:** S — 15,000 XTM

### Description

The `wallet_scanned_to_height` cucumber test step does not actually validate the scan height. It currently ignores the height parameter and just calls `wallet_previously_scanned()`. Fix the step to save the height when the wallet scans and verify that the wallet actually scanned to the specified height.

### Acceptance Criteria

- [ ] The wallet records the height to which it has scanned during the test
- [ ] The `wallet_scanned_to_height` cucumber step verifies the wallet scanned to the specified height (not just that it scanned at all)
- [ ] Existing cucumber scenarios that use this step continue to pass

### Context

- Issue opened by @SWvheerden
- Current broken code in the cucumber steps:
  ```rust
  async fn wallet_scanned_to_height(world: &mut MinotariWorld, height: String) {
      let _ = height; // Use the height parameter
      wallet_previously_scanned(world).await;
  }
  ```
- Relevant code: cucumber test steps in `minotari-cli`

### How It Works

1. Comment on this issue to signal intent (courtesy, not a lock)
2. Fork the repo and do the work
3. Submit a PR that references the issue with a closing keyword (e.g. `Fixes #102`) so GitHub links your PR to the bounty automatically
4. Bounties are competitive. Multiple PRs may be submitted for the same bounty. Review comments are public, and contributors may borrow ideas from each other's work. The maintainer selects the PR that best solves the problem, considering code quality, completeness, and contributor behavior. In cases where multiple contributors made significant contributions, the maintainer may split the bounty. The maintainer's decision is final.
5. Earn XTM (processing may take up to a week; reach out to @possum on Discord with your Tari address)

### Notes

- AI-assisted development is expected and encouraged
- If you get stuck, ask in Discord
