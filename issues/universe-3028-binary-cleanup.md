---
repo: tari-project/universe
issue: 3028
labels: [bounty, bounty-S]
original_size: S
---

## Bounty: Cleanup Old Binary Files After Update

**Tier:** S — 15,000 XTM

### Description

Users who have been running Tari Universe for a long time accumulate a folder of old binaries from successive updates. Implement automatic cleanup of old binary files after a successful update, retaining only the current (latest) binary to free up disk space.

### Acceptance Criteria

- [ ] After a successful update, all previously downloaded binary versions are deleted from the download directory
- [ ] The current (latest, just-installed) binary is always retained
- [ ] Cleanup runs automatically on startup or after update completion (no user action required)

### Context

- Issue opened by @brianp
- Binaries are downloaded to a version-named folder under the Tari Universe data directory during updates
- Relevant code: update/download logic in the Universe Tauri backend (`src-tauri/src/`)
- Check `BinaryResolver` or equivalent for download path patterns

### How It Works

1. Comment on this issue to signal intent (courtesy, not a lock)
2. Fork the repo and do the work
3. Submit a PR that references the issue with a closing keyword (e.g. `Fixes #3028`) so GitHub links your PR to the bounty automatically
4. Bounties are competitive. Multiple PRs may be submitted for the same bounty. Review comments are public, and contributors may borrow ideas from each other's work. The maintainer selects the PR that best solves the problem, considering code quality, completeness, and contributor behavior. In cases where multiple contributors made significant contributions, the maintainer may split the bounty. The maintainer's decision is final.
5. Earn XTM (processing may take up to a week; reach out to @possum on Discord with your Tari address)

### Notes

- AI-assisted development is expected and encouraged
- If you get stuck, ask in Discord
