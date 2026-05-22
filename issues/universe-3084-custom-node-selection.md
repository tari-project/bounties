---
repo: tari-project/universe
issue: 3084
labels: [bounty, bounty-M]
original_size: L
my_size_note: "Downgraded from L to M: with AI, adding a settings text field + connecting to a user-specified node is standard UI+backend work, not complex cross-repo"
---

## Bounty: Support Custom Node Selection for Remote Connection

**Tier:** M — 60,000 XTM

### Description

In some regions, switching between Local, Remote, and Remote & Local node modes still cannot provide a stable connection. Add the ability for users to specify a custom remote node address in Settings. When Remote mode is selected, the app should connect to the user-specified node instead of the default, improving sync speed and connection stability for users in underserved regions.

### Acceptance Criteria

- [ ] A custom node address input field is available in the Settings UI alongside the existing Remote/Local connection options
- [ ] When Remote mode is selected, users can enter a custom remote node address
- [ ] The app connects to and syncs from the user-specified node when configured
- [ ] Invalid addresses are validated and produce a clear error message

### Context

- Issue reported by @xt1085
- The current Settings UI has a three-way selector: Local, Remote, and Remote & Local
- In Remote mode, the app connects to a hardcoded set of Tari seed nodes
- The custom node field should appear when Remote or Remote & Local is selected
- Relevant code: Settings UI (React/TypeScript frontend) and node connection logic in `src-tauri/src/`

### How It Works

1. Comment on this issue to signal intent (courtesy, not a lock)
2. Fork the repo and do the work
3. Submit a PR that references the issue with a closing keyword (e.g. `Fixes #3084`) so GitHub links your PR to the bounty automatically
4. Bounties are competitive. Multiple PRs may be submitted for the same bounty. Review comments are public, and contributors may borrow ideas from each other's work. The maintainer selects the PR that best solves the problem, considering code quality, completeness, and contributor behavior. In cases where multiple contributors made significant contributions, the maintainer may split the bounty. The maintainer's decision is final.
5. Earn XTM (processing may take up to a week; reach out to @possum on Discord with your Tari address)

### Notes

- AI-assisted development is expected and encouraged
- If you get stuck, ask in Discord
