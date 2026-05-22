---
repo: tari-project/universe
issue: 3204
labels: [bounty, bounty-M]
original_size: M
---

## Bounty: Fix Tari Universe Terminating External xmrig Processes on Shutdown

**Tier:** M — 60,000 XTM

### Description

When Tari Universe shuts down, it kills all running xmrig processes on the system — not just the ones it spawned. If a user is running an independent xmrig instance (started before or after TU), closing TU terminates that external process too. The shutdown logic needs to be scoped so that TU only terminates its own child processes, leaving any independently started xmrig instances untouched.

### Acceptance Criteria

- [ ] Closing Tari Universe does not terminate xmrig processes that were started independently (before or after TU launched)
- [ ] Closing Tari Universe still correctly terminates xmrig processes that TU itself spawned
- [ ] Verified on at least one platform (macOS or Linux or Windows) with reproduction steps: start external xmrig, open TU, wait for CPU mining, close TU, confirm external xmrig is still running
- [ ] No regressions in normal TU shutdown behavior (mining stops, resources released)

### Context

- Original issue: https://github.com/tari-project/universe/issues/3204
- The bug suggests TU's shutdown code is using process-name-based killing (e.g. `killall xmrig` or equivalent) rather than tracking and terminating its own child PIDs
- Likely fix area: the process management / mining lifecycle code that handles cleanup on app close

### How It Works

1. Comment on this issue to signal intent (courtesy, not a lock)
2. Fork the repo and do the work
3. Submit a PR that references the issue with a closing keyword (e.g. `Fixes #3204`) so GitHub links your PR to the bounty automatically
4. Bounties are competitive. Multiple PRs may be submitted for the same bounty. Review comments are public, and contributors may borrow ideas from each other's work. The maintainer selects the PR that best solves the problem, considering code quality, completeness, and contributor behavior. In cases where multiple contributors made significant contributions, the maintainer may split the bounty. The maintainer's decision is final.
5. Earn XTM (processing may take up to a week; reach out to @possum on Discord with your Tari address)

### Notes

- AI-assisted development is expected and encouraged
- If you get stuck, ask in Discord
