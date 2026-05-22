---
repo: tari-project/universe
issue: 3178
labels: [bounty, bounty-M]
original_size: M
---

## Bounty: Fix Custom Node Data Location on macOS with NAS (SMB Mount)

**Tier:** M — 60,000 XTM

### Description

The custom node data location feature (merged in PR #3068) does not work on macOS when the target directory is a NAS via SMB mount. Users selecting a network-mounted path encounter an error when attempting to move/use the node data on the remote volume. Investigate and fix the issue so that SMB-mounted volumes work, or provide a clear error message explaining the limitation.

### Acceptance Criteria

- [ ] The failure when using a NAS (SMB mount) as the custom node data location on macOS is reproduced and root-caused
- [ ] Either: the fix allows SMB-mounted volumes to work end-to-end, or: the UI detects network-mounted paths and shows a clear error message before attempting the move
- [ ] Root cause and chosen approach are documented in the PR description

### Context

- Issue opened by @brianp
- Original feature: #3057 (Mainnet db is huge, can we move it elsewhere?)
- Pitch: #2304 (Install Directory Settings)
- Implementation: PR #3068 (feat: node data location settings)
- Platform: macOS 15.7.3, NAS local network SMB mount

### How It Works

1. Comment on this issue to signal intent (courtesy, not a lock)
2. Fork the repo and do the work
3. Submit a PR that references the issue with a closing keyword (e.g. `Fixes #3178`) so GitHub links your PR to the bounty automatically
4. Bounties are competitive. Multiple PRs may be submitted for the same bounty. Review comments are public, and contributors may borrow ideas from each other's work. The maintainer selects the PR that best solves the problem, considering code quality, completeness, and contributor behavior. In cases where multiple contributors made significant contributions, the maintainer may split the bounty. The maintainer's decision is final.
5. Earn XTM (processing may take up to a week; reach out to @possum on Discord with your Tari address)

### Notes

- AI-assisted development is expected and encouraged
- If you get stuck, ask in Discord
