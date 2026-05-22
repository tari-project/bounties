---
repo: tari-project/universe
issue: 2657
labels: [bounty, bounty-S]
original_size: M
my_size_note: "Downgraded from M to S: tracking a boolean in-memory state and checking it on OS resume is straightforward with AI"
---

## Bounty: Persist Mining State Across Sleep/Resume

**Tier:** S — 15,000 XTM

### Description

When resuming from sleep mode, Tari Universe restarts mining even if the user had previously manually paused/stopped the miner. The app should track whether the user manually stopped mining during the current session (in-memory, not persisted to disk) and respect that state on system resume instead of unconditionally restarting mining.

### Acceptance Criteria

- [ ] When the user manually stops/pauses mining, that state is tracked in-memory for the current session
- [ ] On system resume from sleep, the app does not automatically restart mining if the user had manually stopped it during this session
- [ ] If the user has not manually stopped mining (i.e., mining was running when sleep occurred), mining resumes normally

### Context

- Issue reported by @SolfataraEmit
- Platform: macOS 15.5 (but applies cross-platform)
- The wallet backup re-prompt on resume was a separate bug, already addressed
- Relevant code: mining state management and OS event handling in the Universe Tauri backend

### How It Works

1. Comment on this issue to signal intent (courtesy, not a lock)
2. Fork the repo and do the work
3. Submit a PR that references the issue with a closing keyword (e.g. `Fixes #2657`) so GitHub links your PR to the bounty automatically
4. Bounties are competitive. Multiple PRs may be submitted for the same bounty. Review comments are public, and contributors may borrow ideas from each other's work. The maintainer selects the PR that best solves the problem, considering code quality, completeness, and contributor behavior. In cases where multiple contributors made significant contributions, the maintainer may split the bounty. The maintainer's decision is final.
5. Earn XTM (processing may take up to a week; reach out to @possum on Discord with your Tari address)

### Notes

- AI-assisted development is expected and encouraged
- If you get stuck, ask in Discord
