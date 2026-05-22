---
repo: tari-project/tari
issue: 7715
labels: [bounty, bounty-M]
original_size: M
---

## Bounty: Create LMDB Unit Tests

**Tier:** M — 60,000 XTM

### Description

LMDB correctness in the base node is currently untested. Create a reproducible test chain (genesis block, 10 main-chain blocks, and a 10-block fork from block 5) and write two unit tests: one that writes the chain to a new LMDB file and bit-compares it against a reference, and one that loads the LMDB file and verifies all headers, blocks, outputs, inputs, kernels, and accumulated data can be fetched correctly through the full range of query methods.

### Acceptance Criteria

- [ ] A test chain is created with a genesis block, 10 main-chain blocks, and a 10-block fork from block 5
- [ ] All block data is saved in a JSON file for reproducibility
- [ ] A write test creates a new LMDB file from the JSON data and bit-compares it against the reference file
- [ ] A read test loads the LMDB file and verifies all 15 main-chain headers, 5 reorged headers, and all blocks can be fetched
- [ ] The read test verifies per-block queries: outputs by header_hash, inputs by header_hash, kernels by header_hash, output by hash, unspent output by commitment, output by payref, outputs with spend state at height, kernel by excess sig, and header containing kernel by MMR position

### Context

- Issue opened by @SWvheerden
- An earlier attempt (PR #7716 by Copilot agent) was closed; this bounty is for a human-quality implementation
- Relevant code: `base_layer/core/src/chain_storage/lmdb_db/`

### How It Works

1. Comment on this issue to signal intent (courtesy, not a lock)
2. Fork the repo and do the work
3. Submit a PR that references the issue with a closing keyword (e.g. `Fixes #7715`) so GitHub links your PR to the bounty automatically
4. Bounties are competitive. Multiple PRs may be submitted for the same bounty. Review comments are public, and contributors may borrow ideas from each other's work. The maintainer selects the PR that best solves the problem, considering code quality, completeness, and contributor behavior. In cases where multiple contributors made significant contributions, the maintainer may split the bounty. The maintainer's decision is final.
5. Earn XTM (processing may take up to a week; reach out to @possum on Discord with your Tari address)

### Notes

- AI-assisted development is expected and encouraged
- If you get stuck, ask in Discord
