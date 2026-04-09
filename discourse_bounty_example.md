## 🏷️ Bounty: Set Up Tari Governance Discourse Forum

**Tier:** M — 60,000 XTM

### Description

Set up and configure a Discourse forum instance on a Tari Labs-provided VPS to serve as the primary governance hub for the Tari community. This is where RFC discussions, grant proposals, governance debates, and community announcements will live. The forum needs to be production-ready, not a default install.

### Acceptance Criteria

- [ ] Discourse installed and running on provided VPS
- [ ] SSL/TLS configured with valid certificate
- [ ] Forum categories created: RFCs, Grant Proposals, Protocol Development, Ootle Development, Community & Ecosystem, Infrastructure & Security, General
- [ ] Trust levels configured: new users can read and reply; Trust Level 1 (earned through participation) can create topics; Trust Level 2+ can post in governance categories
- [ ] Moderation tools enabled and tested
- [ ] Authentication configured (email-based registration, optionally GitHub SSO)
- [ ] Automated daily backup schedule configured and verified
- [ ] Basic branding applied (Tari logo, colors, favicon)
- [ ] Admin credentials and documentation handed to Simon

### Context

- Discourse is the de facto standard for blockchain governance forums, used by MakerDAO, ENS, Uniswap, Aave, Compound, Arbitrum, and Grin
- Category structure maps to the four Tari workgroups plus governance process categories
- Trust levels map to Ostrom's boundary principle: participation earns privileges
- Reference installs: forum.grin.mw, governance.aave.com, discuss.ens.domains
- Discourse install guide: https://github.com/discourse/discourse/blob/main/docs/INSTALL-cloud.md

### How to Claim

1. Comment on this issue to signal intent (courtesy, not a lock)
2. Fork the repo and do the work
3. Submit a PR that meets the acceptance criteria
4. First PR that passes review and gets merged wins the bounty
5. On acceptance, XTM payment is processed

### Notes

- VPS access will be provided after claim is confirmed
- AI-assisted development is expected and encouraged
- If you get stuck, ask in Discord
- If you can't complete it within 14 days of claiming, let us know so someone else can pick it up