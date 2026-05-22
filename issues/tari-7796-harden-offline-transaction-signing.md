---
repo: tari-project/tari
issue: 7796
labels: [bounty, bounty-L]
original_size: L
---

## Bounty: Harden Offline Transaction Signing

**Tier:** L — 150,000 XTM

### Description

The offline signing JSON payload currently contains all transaction data in plaintext, leaving it vulnerable to man-in-the-middle tampering between the view wallet and the signing device. Harden this by adding a cryptographic signature over the entire JSON payload, signed with the view key. The offline signer (console wallet or hardware wallet) must verify this signature before signing any transaction, ensuring the data has not been modified in transit. The same protection must apply to multisig offline signing flows.

### Acceptance Criteria

- [ ] A new domain-separated signature scheme is defined for offline signing verification
- [ ] The view wallet signs the full JSON payload contents using the view key with the new domain separator as the challenge
- [ ] The offline signer verifies the signature before proceeding with transaction signing; signing is refused if verification fails
- [ ] Multisig offline signing uses the same verification flow
- [ ] At least one unit test demonstrates that an invalid signature is rejected by the signer
- [ ] At least one cucumber test demonstrates that a tampered JSON payload is rejected by the signer

### Context

- Original issue: https://github.com/tari-project/tari/issues/7796
- Related: tari#7736 (offline signing cucumber test, already merged)
- Risk surface: directly touches signing and key material — sized L accordingly
- The domain signature prevents replay and cross-context attacks on the challenge hash

### How It Works

1. Comment on this issue to signal intent (courtesy, not a lock)
2. Fork the repo and do the work
3. Submit a PR that references the issue with a closing keyword (e.g. `Fixes #7796`) so GitHub links your PR to the bounty automatically
4. Bounties are competitive. Multiple PRs may be submitted for the same bounty. Review comments are public, and contributors may borrow ideas from each other's work. The maintainer selects the PR that best solves the problem, considering code quality, completeness, and contributor behavior. In cases where multiple contributors made significant contributions, the maintainer may split the bounty. The maintainer's decision is final.
5. Earn XTM (processing may take up to a week; reach out to @possum on Discord with your Tari address)

### Notes

- AI-assisted development is expected and encouraged
- If you get stuck, ask in Discord
