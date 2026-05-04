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

### How to Claim

1. Comment on this issue to signal intent (courtesy, not a lock)
2. Fork the repo and do the work
3. Submit a PR that meets the acceptance criteria
4. First PR that passes review and gets merged wins the bounty
5. On acceptance, XTM payment is processed

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