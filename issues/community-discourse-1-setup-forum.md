---
repo: tari-project/community-discourse
issue: 1
labels: [bounty, bounty-M]
original_size: none
my_size_note: "M: well-defined scope (install + configure), no code required, verification is manual but checklist-based"
---

## Bounty: Set Up Tari Community Discourse Forum

**Tier:** M — 60,000 XTM

### Description

Install and configure a production-ready Discourse forum instance on a Tari Labs-provided VPS to serve as the primary governance and community hub. This includes SSL, categories mapping to Tari workgroups, trust levels for progressive access, GitHub SSO, automated backups, and basic Tari branding. The result should be a fully operational forum, not a default install.

### Acceptance Criteria

- [ ] Discourse installed and running on provided VPS with SSL/TLS and a valid certificate
- [ ] Forum categories created: RFCs, Grant Proposals, Protocol Development, Ootle Development, Community & Ecosystem, Infrastructure & Security, General
- [ ] Trust levels configured: new users can read and reply; Trust Level 1 (earned through participation) can create topics; Trust Level 2+ can post in governance categories
- [ ] Authentication configured with email-based registration and GitHub SSO
- [ ] Automated daily backup schedule configured and verified (test a restore)
- [ ] Basic Tari branding applied (logo, colors, favicon) and admin credentials + setup documentation handed to the project lead

### Context

- Discourse is the standard for blockchain governance forums (MakerDAO, ENS, Uniswap, Aave, Compound, Arbitrum, Grin)
- Category structure maps to the four Tari workgroups plus governance process categories
- Trust levels map to Ostrom's boundary principle: participation earns privileges
- Reference installs: forum.grin.mw, governance.aave.com, discuss.ens.domains
- Discourse install guide: https://github.com/discourse/discourse/blob/main/docs/INSTALL-cloud.md
- VPS details will be provided after claim is confirmed

### How It Works

1. Comment on this issue to signal intent (courtesy, not a lock)
2. Fork the repo and do the work
3. Submit a PR that references the issue with a closing keyword (e.g. `Fixes #1`) so GitHub links your PR to the bounty automatically
4. Bounties are competitive. Multiple PRs may be submitted for the same bounty. Review comments are public, and contributors may borrow ideas from each other's work. The maintainer selects the PR that best solves the problem, considering code quality, completeness, and contributor behavior. In cases where multiple contributors made significant contributions, the maintainer may split the bounty. The maintainer's decision is final.
5. Earn XTM (processing may take up to a week; reach out to @possum on Discord with your Tari address)

### Notes

- VPS access will be provided after claim is confirmed
- AI-assisted development is expected and encouraged
- If you get stuck, ask in Discord
