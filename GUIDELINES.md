# Tari Bounty Program Guidelines

---

## Labels

Standardize across all repos in the `tari-project` GitHub organization:

- `bounty` — base label, applied to all bounty issues
- `bounty-S` — Small
- `bounty-M` — Medium
- `bounty-L` — Large
- `bounty-XL` — Extra Large

Remove legacy labels: `E-bounty` or untiered `bounty` without a size suffix.

**All open bounties across the org:** `https://github.com/search?q=org%3Atari-project+label%3Abounty+state%3Aopen&type=issues`

---

## Tiered Pricing

Fixed price per tier. No negotiation. You see the size label, you know the payout.

| Tier | XTM | Typical Scope | Approval |
|------|-----|---------------|----------|
| **S** | 15,000 | Doc fix, translation, single test, config change, small bug fix | Workgroup lead |
| **M** | 60,000 | Test suite, feature, SDK example, tutorial, CI fix, integration test, tool setup | Workgroup lead |
| **L** | 150,000 | SDK port, significant feature, tool integration, complex multi-file work | Workgroup lead |
| **XL** | 450,000 | Major feature (FFI rewrite), new application, complex cross-repo work | Steward body |

---

## GitHub Issue Template

Rewrite all bounty issues in place using this format. Apply `bounty` plus the appropriate size label (`bounty-S`, `bounty-M`, `bounty-L`, `bounty-XL`).

```markdown
## Bounty: [Title]

**Tier:** [S / M / L / XL] — [15,000 / 60,000 / 150,000 / 450,000] XTM

### Description

[One paragraph. What needs to be built, fixed, or produced. Be specific enough that someone unfamiliar with the codebase can understand the task.]

### Acceptance Criteria

- [ ] [Criterion 1: specific, verifiable, binary pass/fail]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

### Context

[Links to relevant code, docs, RFCs, or discussions.]

### How It Works

1. Comment on this issue to signal intent (courtesy, not a lock)
2. Fork the repo and do the work
3. Submit a PR that references the issue with a closing keyword (e.g. `Fixes #1234`) so GitHub links your PR to the bounty automatically
4. Bounties are competitive. Multiple PRs may be submitted for the same bounty. Review comments are public, and contributors may borrow ideas from each other's work. The maintainer selects the PR that best solves the problem, considering code quality, completeness, and contributor behavior. In cases where multiple contributors made significant contributions, the maintainer may split the bounty. The maintainer's decision is final.
5. Earn XTM (processing may take up to a week; reach out to @possum on Discord with your Tari address)

### Notes

- AI-assisted development is expected and encouraged
- If you get stuck, ask in Discord
```

---

## Sizing Criteria

When assigning a tier, evaluate four dimensions. Sizes assume AI-assisted development.

**1. Scope clarity.** Well-defined input/output = S/M. Ambiguous requirements or design decisions needed = L/XL.

**2. Codebase familiarity required.** Can someone pick this up cold from docs? S/M. Requires Tari-specific architecture knowledge or cross-repo dependencies? L/XL.

**3. Verification complexity.** Can acceptance be checked by running a test? S/M. Requires manual review or multi-step validation? L/XL.

**4. Risk surface.** Touches consensus, wallet, bridge, or signing code? Bump up one tier and flag for additional review. Pure docs, tests, or tooling? Size as-is.