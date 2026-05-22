---
repo: tari-project/wxtm-bridge-frontend
issue: 103
labels: [bounty, bounty-S]
original_size: S
---

## Bounty: Mitigate Next.js CVE Risk by Pinning Version

**Tier:** S — 15,000 XTM

### Description

The `wxtm-bridge-frontend` currently depends on `"next": "^16.1.1"`, which allows npm/yarn to resolve any semver-compatible version in the 16.x range, including versions with known CVEs. Pin Next.js to exactly `16.1.7` (the latest patched release) and remove the `^` caret to prevent unintended resolution to vulnerable versions. Update `eslint-config-next` to match.

### Acceptance Criteria

- [ ] `package.json` specifies `"next": "16.1.7"` (exact, no caret)
- [ ] `eslint-config-next` version is updated to `"16.1.7"` (exact, no caret) to match
- [ ] `package-lock.json` / `yarn.lock` is regenerated with the pinned versions
- [ ] The app builds successfully (`npm run build` or `yarn build` passes with no new errors)
- [ ] Wrap/unwrap flow verified working end-to-end via TU with the updated bridge frontend (screenshot or recording)

### Context

- Original issue: https://github.com/tari-project/wxtm-bridge-frontend/issues/103
- Current versions: `"next": "^16.1.1"`, `"eslint-config-next": "^16.1.1"`
- Next.js changelog: https://github.com/vercel/next.js/releases
- The frontend depends on private `@aspect` npm packages (api & contracts). To test locally you either need an npm token for the private registry, or build the public `api` and `contracts` repos locally and link them as dependencies
- Full integration testing requires running the bridge frontend as a tapplet inside Tari Universe (TU)

### How It Works

1. Comment on this issue to signal intent (courtesy, not a lock)
2. Fork the repo and do the work
3. Submit a PR that references the issue with a closing keyword (e.g. `Fixes #103`) so GitHub links your PR to the bounty automatically
4. Bounties are competitive. Multiple PRs may be submitted for the same bounty. Review comments are public, and contributors may borrow ideas from each other's work. The maintainer selects the PR that best solves the problem, considering code quality, completeness, and contributor behavior. In cases where multiple contributors made significant contributions, the maintainer may split the bounty. The maintainer's decision is final.
5. Earn XTM (processing may take up to a week; reach out to @possum on Discord with your Tari address)

### Notes

- AI-assisted development is expected and encouraged
- If you get stuck, ask in Discord
