---
repo: tari-project/tari
issue: 7164
labels: [bounty, bounty-L]
original_size: L
---

## Bounty: JMT Data Optimization

**Tier:** L — 150,000 XTM

### Description

Jellyfish Merkle Tree (JMT) data is the single largest consumer of storage in the base node database — `jmt_node_data` alone accounts for 6.4 GB out of 11.4 GB total. Investigate the root cause of the excessive size (9.6M entries averaging 669 bytes each), propose an optimization strategy, and implement it. This likely involves changes to node serialization, pruning of historical JMT nodes, or restructuring how JMT data is stored in LMDB.

### Acceptance Criteria

- [ ] Root cause of JMT data size is investigated and documented in the issue
- [ ] A proposed optimization solution is written up with expected size reduction
- [ ] The optimization is implemented and reduces `jmt_node_data` storage by at least 50%
- [ ] Existing functionality (block validation, state queries, reorgs) continues to work correctly
- [ ] Benchmarks comparing before/after storage sizes are provided

### Context

- Issue opened by @stringhandler
- `jmt_node_data`: 9,601,158 entries, 6.4 GB, avg 669 bytes, depth 4
- `jmt_unique_key_data`: 2,615,793 entries, 302.1 MB
- `jmt_value_data`: 2,615,793 entries, 231.8 MB
- Total LMDB map size: 11.6 GB; JMT tables account for ~60%
- Relevant code: `base_layer/core/src/chain_storage/lmdb_db/`

### How It Works

1. Comment on this issue to signal intent (courtesy, not a lock)
2. Fork the repo and do the work
3. Submit a PR that references the issue with a closing keyword (e.g. `Fixes #7164`) so GitHub links your PR to the bounty automatically
4. Bounties are competitive. Multiple PRs may be submitted for the same bounty. Review comments are public, and contributors may borrow ideas from each other's work. The maintainer selects the PR that best solves the problem, considering code quality, completeness, and contributor behavior. In cases where multiple contributors made significant contributions, the maintainer may split the bounty. The maintainer's decision is final.
5. Earn XTM (processing may take up to a week; reach out to @possum on Discord with your Tari address)

### Notes

- This touches core storage infrastructure — PR will require thorough review
- AI-assisted development is expected and encouraged
- If you get stuck, ask in Discord
