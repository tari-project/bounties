---
repo: tari-project/universe
issue: 3128
labels: [bounty, bounty-S]
original_size: S
---

## Bounty: Fix Seed Word Import Mnemonic Error

**Tier:** S — 15,000 XTM

### Description

The seed word import in Tari Universe fails when users enter words one per line (pressing Enter between words) instead of space-separated. The input parser reads newlines as part of the mnemonic and produces `Mnemonic Error: Only ChineseSimplified, ChineseTraditional, English, French, Italian, Japanese, Korean and Spanish are defined natural languages`. Copy-pasting the full phrase also fails because the confirmation tick never becomes available. Fix the input handling to accept both newline-separated and space-separated seed words.

### Acceptance Criteria

- [ ] Seed word import handles words entered one per line (newline-separated) in addition to space-separated
- [ ] Seed word import works correctly when copy-pasting the full phrase
- [ ] The confirmation tick becomes available once valid seed words are detected, regardless of whitespace format

### Context

- Issue reported by @Triton-S
- The workaround is typing each word followed by a space (not Enter) — this works
- Platform: Windows 11, Remote Minotari node
- Relevant code: seed import UI component in the Universe Tauri frontend

### How It Works

1. Comment on this issue to signal intent (courtesy, not a lock)
2. Fork the repo and do the work
3. Submit a PR that references the issue with a closing keyword (e.g. `Fixes #3128`) so GitHub links your PR to the bounty automatically
4. Bounties are competitive. Multiple PRs may be submitted for the same bounty. Review comments are public, and contributors may borrow ideas from each other's work. The maintainer selects the PR that best solves the problem, considering code quality, completeness, and contributor behavior. In cases where multiple contributors made significant contributions, the maintainer may split the bounty. The maintainer's decision is final.
5. Earn XTM (processing may take up to a week; reach out to @possum on Discord with your Tari address)

### Notes

- AI-assisted development is expected and encouraged
- If you get stuck, ask in Discord
