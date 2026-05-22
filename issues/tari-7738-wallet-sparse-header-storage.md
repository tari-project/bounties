---
repo: tari-project/tari
issue: 7738
labels: [bounty, bounty-M]
original_size: M
---

## Bounty: Wallet Sparse Scanned Block Header Storage

**Tier:** M — 60,000 XTM

### Description

The wallet currently saves only the last 720 scanned block headers. If the wallet needs to rescan beyond that window, it falls back to scanning from the wallet birthday, which is slow. Implement a sparse storage strategy that keeps all headers for recent blocks and progressively fewer headers for older blocks, so the wallet almost always has a recent-enough starting point for rescans.

### Acceptance Criteria

- [ ] `tip - 720` to `tip`: all block headers are saved
- [ ] `tip - 10,000` to `tip - 720`: 1 header per 100 blocks is saved
- [ ] `tip - 100,000` to `tip - 10,000`: 1 header per 1,000 blocks is saved
- [ ] `genesis` to `tip - 100,000`: 1 header per 5,000 blocks is saved
- [ ] When the wallet initiates a scan, it finds the most recent saved header and starts from there instead of the birthday

### Context

- Issue opened by @SWvheerden
- Related to #7685 (wallet UTXO scanner wipes scan progress when connecting to a node with a lower tip)
- Relevant code: wallet scanning logic in `base_layer/wallet/`

### How It Works

1. Comment on this issue to signal intent (courtesy, not a lock)
2. Fork the repo and do the work
3. Submit a PR that references the issue with a closing keyword (e.g. `Fixes #7738`) so GitHub links your PR to the bounty automatically
4. Bounties are competitive. Multiple PRs may be submitted for the same bounty. Review comments are public, and contributors may borrow ideas from each other's work. The maintainer selects the PR that best solves the problem, considering code quality, completeness, and contributor behavior. In cases where multiple contributors made significant contributions, the maintainer may split the bounty. The maintainer's decision is final.
5. Earn XTM (processing may take up to a week; reach out to @possum on Discord with your Tari address)

### Notes

- AI-assisted development is expected and encouraged
- If you get stuck, ask in Discord
