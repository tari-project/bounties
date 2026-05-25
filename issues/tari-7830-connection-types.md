---
repo: tari-project/tari
issue: 7830
labels: [bounty, bounty-M]
original_size: M
---

## Bounty: Connection types

**Tier:** M — 60,000 XTM

### Description

Extend peer transport configuration so the node can explicitly choose both protocol availability and connection preference order. Replace the current two-mode behavior with four `TransportType` options: `Tor` (Tor only), `Tcp` (TCP only), `TorTcp` (both enabled, prefer Tor), and `TcpTor` (both enabled, prefer TCP, and the new default). The change is scoped to peer selection only — specifically which protocols are available and the preference order used when choosing new peers and the addresses they should dial. Nothing outside peer selection is affected.

### Acceptance Criteria

- [ ] `TransportType` defines exactly four modes: `Tor`, `Tcp`, `TorTcp`, and `TcpTor`.
- [ ] Mode behavior is implemented as specified: `Tor` enables Tor only, `Tcp` enables TCP only, `TorTcp` enables both and prefers Tor, and `TcpTor` enables both and prefers TCP.
- [ ] Default peer transport mode is `TcpTor`.
- [ ] Unit tests cover peer selection for all four modes and verify the correct preference order is applied when choosing new peers and dial addresses.
- [ ] Cucumber tests verify correct peer selection behavior for all four modes.
- [ ] No behavior outside peer selection is changed (no regressions in non-peer networking).

### Context

- Original issue: https://github.com/tari-project/tari/issues/7830


### How It Works

1. Comment on this issue to signal intent (courtesy, not a lock)
2. Fork the repo and do the work
3. Submit a PR that references the issue with a closing keyword (for example, `Fixes #7830`) so GitHub links your PR to the bounty automatically
4. Bounties are competitive. Multiple PRs may be submitted for the same bounty. Review comments are public, and contributors may borrow ideas from each other's work. The maintainer selects the PR that best solves the problem, considering code quality, completeness, and contributor behavior. In cases where multiple contributors made significant contributions, the maintainer may split the bounty. The maintainer's decision is final.
5. Earn XTM (processing may take up to a week; reach out to @possum on Discord with your Tari address)

### Notes

- AI-assisted development is expected and encouraged
- If you get stuck, ask in Discord
