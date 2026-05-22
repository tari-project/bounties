---
repo: tari-project/universe
issue: 3111
labels: [bounty, bounty-S]
original_size: S
my_size_note: "Original issue labeled XS, but spec only defines S/M/L/XL tiers. Mapped to S."
---

## Bounty: Update Linux Build Documentation

**Tier:** S — 15,000 XTM

### Description

The Universe README documents `.deb`/`.AppImage` build outputs, but these are not actually produced as official release artifacts. Official Linux releases were discontinued due to low usage and high maintenance burden, though Linux builds still work from source. Update the README to accurately describe the current Linux build process and available artifacts.

### Acceptance Criteria

- [ ] README is updated to accurately describe the current Linux build process (build from source)
- [ ] References to `.deb`/`.AppImage` artifacts are removed or corrected
- [ ] Build-from-source instructions for Linux are clear and tested

### Context

- Issue reported by @kn0wmad
- Official Linux releases were discontinued — Linux users accounted for <1% of Universe user base
- Linux builds still succeed in CI; several team members use Linux day-to-day
- The app works when built from source; just no official prebuilt artifacts

### How It Works

1. Comment on this issue to signal intent (courtesy, not a lock)
2. Fork the repo and do the work
3. Submit a PR that references the issue with a closing keyword (e.g. `Fixes #3111`) so GitHub links your PR to the bounty automatically
4. Bounties are competitive. Multiple PRs may be submitted for the same bounty. Review comments are public, and contributors may borrow ideas from each other's work. The maintainer selects the PR that best solves the problem, considering code quality, completeness, and contributor behavior. In cases where multiple contributors made significant contributions, the maintainer may split the bounty. The maintainer's decision is final.
5. Earn XTM (processing may take up to a week; reach out to @possum on Discord with your Tari address)

### Notes

- AI-assisted development is expected and encouraged
- If you get stuck, ask in Discord
