---
repo: tari-project/tari-ootle
issue: 1931
labels: [bounty, bounty-L]
original_size: L
---

## Bounty: Wallet Address Book

**Tier:** L — 150,000 XTM

### Description

Add an address book feature to the wallet daemon, allowing users to save, retrieve, and manage named Ootle addresses. This requires JSON-RPC CRUD endpoints (add, list, get, update, delete), persistent storage across restarts, and web UI integration so users can manage entries and select saved addresses when making transfers. Each entry stores a label, an Ootle address (`otl_loc_...`), and an optional memo field.

### Acceptance Criteria

- [ ] Wallet daemon persists address book entries across restarts
- [ ] JSON-RPC endpoints exist for: adding, listing, getting by name, updating, and deleting address book entries
- [ ] Duplicate names are rejected
- [ ] Web UI has an address book management page (add/edit/delete entries)
- [ ] Web UI transfer forms allow selecting a recipient from the address book
- [ ] Address validation is performed when adding/updating entries

### Context

- Issue opened by @sdbondi
- Relevant code: wallet daemon JSON-RPC layer and web UI in `tari-ootle`
- Was previously assigned to @martinserts, then unassigned

### How It Works

1. Comment on this issue to signal intent (courtesy, not a lock)
2. Fork the repo and do the work
3. Submit a PR that references the issue with a closing keyword (e.g. `Fixes #1931`) so GitHub links your PR to the bounty automatically
4. Bounties are competitive. Multiple PRs may be submitted for the same bounty. Review comments are public, and contributors may borrow ideas from each other's work. The maintainer selects the PR that best solves the problem, considering code quality, completeness, and contributor behavior. In cases where multiple contributors made significant contributions, the maintainer may split the bounty. The maintainer's decision is final.
5. Earn XTM (processing may take up to a week; reach out to @possum on Discord with your Tari address)

### Notes

- AI-assisted development is expected and encouraged
- If you get stuck, ask in Discord
