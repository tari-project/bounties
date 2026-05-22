---
repo: tari-project/tari
issue: 7795
labels: [bounty, bounty-S]
original_size: S
---

## Bounty: Create Better Ledger Installer

**Tier:** S — 15,000 XTM

### Description

Replace the existing per-OS/per-model shell scripts for installing the Minotari app on Ledger hardware wallets with a single cross-platform installer. The installer should auto-detect the connected Ledger model (Nano S, Nano S Plus, Nano X, Stax), download the correct firmware file, and install it — all in one step. Support macOS, Windows, and Linux.

### Acceptance Criteria

- [ ] A single installer executable or script works for macOS, Windows, and Linux
- [ ] The installer detects the connected Ledger model automatically without user input
- [ ] The correct Minotari app binary is downloaded and installed for the detected model
- [ ] The installer reports clear success/failure status and handles errors (no device connected, unsupported model) gracefully

### Context

- Original issue: https://github.com/tari-project/tari/issues/7795
- Current scripts live in the repo, one per OS/ledger type
- Ledger model detection can use the Ledger USB HID interface or `ledgerctl` tooling

### How It Works

1. Comment on this issue to signal intent (courtesy, not a lock)
2. Fork the repo and do the work
3. Submit a PR that references the issue with a closing keyword (e.g. `Fixes #7795`) so GitHub links your PR to the bounty automatically
4. Bounties are competitive. Multiple PRs may be submitted for the same bounty. Review comments are public, and contributors may borrow ideas from each other's work. The maintainer selects the PR that best solves the problem, considering code quality, completeness, and contributor behavior. In cases where multiple contributors made significant contributions, the maintainer may split the bounty. The maintainer's decision is final.
5. Earn XTM (processing may take up to a week; reach out to @possum on Discord with your Tari address)

### Notes

- AI-assisted development is expected and encouraged
- If you get stuck, ask in Discord
