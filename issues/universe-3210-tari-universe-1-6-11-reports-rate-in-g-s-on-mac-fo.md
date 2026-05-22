---
repo: tari-project/universe
issue: 3210
labels: [bounty, bounty-S]
original_size: S
---

## Bounty: Fix incorrect hashrate unit display on macOS

**Tier:** S — 15,000 XTM

### Description

Tari Universe on macOS incorrectly displays CPU mining hashrate in G/s (graphs per second), which is the unit used for Cuckoo Cycle (c29) mining. Since macOS does not support c29 mining, all mining power values on Mac should be displayed in H/s (hashes per second). The UI needs to detect the active mining algorithm and show the appropriate unit.

### Acceptance Criteria

- [ ] CPU hashrate on macOS is displayed in H/s (not G/s)
- [ ] The unit correctly reflects the active mining algorithm (H/s for RandomX, G/s for c29 on platforms that support it)
- [ ] No regression on other platforms — Windows/Linux still show correct units for their respective algorithms

### Context

- Original issue: https://github.com/tari-project/universe/issues/3210
- Screenshot showing the bug: the UI displays "G/s" for CPU mining on Mac where it should show "H/s"
- Mac only runs RandomX (SHA-3 based), not Cuckoo Cycle (c29), so graph-rate units are never appropriate on macOS

### How It Works

1. Comment on this issue to signal intent (courtesy, not a lock)
2. Fork the repo and do the work
3. Submit a PR that references the issue with a closing keyword (e.g. `Fixes #3210`) so GitHub links your PR to the bounty automatically
4. Bounties are competitive. Multiple PRs may be submitted for the same bounty. Review comments are public, and contributors may borrow ideas from each other's work. The maintainer selects the PR that best solves the problem, considering code quality, completeness, and contributor behavior. In cases where multiple contributors made significant contributions, the maintainer may split the bounty. The maintainer's decision is final.
5. Earn XTM (processing may take up to a week; reach out to @possum on Discord with your Tari address)

### Notes

- AI-assisted development is expected and encouraged
- If you get stuck, ask in Discord
