---
repo: tari-project/tari
issue: 7829
labels: [bounty, bounty-S]
original_size: S
---

## Bounty: Console Wallet Key Migration

**Tier:** S — 15,000 XTM

### Description

The console wallet still stores legacy key types in its output table. On startup, the wallet should run an async batch migration that converts all legacy keys (accessed via `get_legacy_private_key(&self, key_id: &LegacyTariKeyId)`) to the current standard key format. This is required for wallet import via `minotari-cli` (issue #119) to work correctly against older wallets. The migration must not block wallet startup.

### Acceptance Criteria

- [ ] On startup, the wallet runs an async migration against the output table converting all legacy key types to the current standard format
- [ ] Migration runs in batches and does not block wallet startup
- [ ] A Rust integration test proves the migration correctly converts legacy keys and the wallet remains functional afterward

### Context

- Original issue: https://github.com/tari-project/tari/issues/7829
- Author: @SWvheerden
- Related: https://github.com/tari-project/minotari-cli/issues/119 (import fails with legacy key types)
- Key conversion entry point: `fn get_legacy_private_key(&self, key_id: &LegacyTariKeyId)`
- Target table: wallet output table

### How It Works

1. Comment on this issue to signal intent (courtesy, not a lock)
2. Fork the repo and do the work
3. Submit a PR that references the issue with a closing keyword (e.g. `Fixes #7829`) so GitHub links your PR to the bounty automatically
4. Bounties are competitive. Multiple PRs may be submitted for the same bounty. Review comments are public, and contributors may borrow ideas from each other's work. The maintainer selects the PR that best solves the problem, considering code quality, completeness, and contributor behavior. In cases where multiple contributors made significant contributions, the maintainer may split the bounty. The maintainer's decision is final.
5. Earn XTM (processing may take up to a week; reach out to @possum on Discord with your Tari address)

### Notes

- AI-assisted development is expected and encouraged
- If you get stuck, ask in Discord
- If you get stuck, ask in Discord
