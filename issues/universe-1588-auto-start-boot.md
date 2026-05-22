---
repo: tari-project/universe
issue: 1588
labels: [bounty, bounty-M]
original_size: M
---

## Bounty: Fix Auto-Start on System Boot (Windows)

**Tier:** M — 60,000 XTM

### Description

Enabling "Auto-start on system boot" in Tari Universe on Windows 11 does not actually register the app to launch on startup. Tari Universe is not visible in Task Scheduler after enabling the setting, and the app does not relaunch after a system restart. This bug has persisted across dozens of versions from 0.9.x through 1.6.x. Fix the auto-start registration mechanism so it correctly creates a startup entry on Windows.

### Acceptance Criteria

- [ ] Enabling "Auto-start on system boot" correctly registers Tari Universe to launch on system boot (via Task Scheduler, registry Run key, or Startup folder)
- [ ] The app launches automatically after a system restart when the setting is enabled
- [ ] The auto-start entry is visible and verifiable through the relevant Windows mechanism
- [ ] Disabling the setting removes the auto-start entry

### Context

- Issue reported by @Tas4tari
- Platform: Windows 11, Aspire A315-59
- Consistently reproduced across versions 0.9.811 through 1.6.3 (over 100 "still an issue" comments)
- Relevant code: auto-start setting implementation in the Universe Tauri backend (likely `tauri-plugin-autostart` or equivalent)

### How It Works

1. Comment on this issue to signal intent (courtesy, not a lock)
2. Fork the repo and do the work
3. Submit a PR that references the issue with a closing keyword (e.g. `Fixes #1588`) so GitHub links your PR to the bounty automatically
4. Bounties are competitive. Multiple PRs may be submitted for the same bounty. Review comments are public, and contributors may borrow ideas from each other's work. The maintainer selects the PR that best solves the problem, considering code quality, completeness, and contributor behavior. In cases where multiple contributors made significant contributions, the maintainer may split the bounty. The maintainer's decision is final.
5. Earn XTM (processing may take up to a week; reach out to @possum on Discord with your Tari address)

### Notes

- AI-assisted development is expected and encouraged
- If you get stuck, ask in Discord
