---
repo: tari-project/aiteen
issue: 1
labels: [bounty, bounty-M]
original_size: none
---

## Bounty: Replace Aiteen with a Robust i18n Pipeline

**Tier:** M — 60,000 XTM

### Description

Aiteen is a custom Python i18n pipeline that audits missing translations across locale JSON files, translates them via OpenAI, patches locale files, and runs QA checks. It was built in a time crunch and has hardcoded paths, manual multi-step CLI workflow, and no CI integration. Replace it with an established open-source i18n management solution (or a significantly improved pipeline) that integrates into CI, supports all Tari projects (Universe, WXTM Bridge, and future apps), and produces high-quality AI translations with a review workflow.

### Acceptance Criteria

- [ ] A replacement i18n solution is selected and documented (with rationale); candidates include [Tolgee](https://github.com/tolgee/tolgee-platform), [Weblate](https://github.com/WeblateOrg/weblate), [Traduora](https://github.com/ever-co/ever-traduora), or a rewrite of the current pipeline with proper CLI/CI support
- [ ] The solution detects missing translations by comparing locale files against the English source
- [ ] Missing strings are translated via AI (OpenAI or equivalent) with context-aware prompts
- [ ] A review/approval step exists before translations are merged (PR-based or admin UI)
- [ ] The pipeline runs in CI (GitHub Actions) and can be triggered on PRs that modify English locale files
- [ ] Works with both Universe (`public/locales/`) and WXTM Bridge (`wxtm-bridge-frontend/public/locales/`) locale structures

### Context

- Current tool: https://github.com/tari-project/aiteen
- Python scripts: `i18n_checker.py` (audit), `i18n_translator.py` (translate via OpenAI), `i18n_patch_locales.py` (patch), `i18n_qa.py` (QA matrix)
- Locale format: JSON files under `public/locales/{lang}/` directories
- Currently requires manual 4-step CLI workflow with hardcoded local paths
- Used for `tari-project/universe` and `tari/wxtm-bridge`

### How It Works

1. Comment on this issue to signal intent (courtesy, not a lock)
2. Fork the repo and do the work
3. Submit a PR that references the issue with a closing keyword (e.g. `Fixes #1`) so GitHub links your PR to the bounty automatically
4. Bounties are competitive. Multiple PRs may be submitted for the same bounty. Review comments are public, and contributors may borrow ideas from each other's work. The maintainer selects the PR that best solves the problem, considering code quality, completeness, and contributor behavior. In cases where multiple contributors made significant contributions, the maintainer may split the bounty. The maintainer's decision is final.
5. Earn XTM (processing may take up to a week; reach out to @possum on Discord with your Tari address)

### Notes

- Start with a brief proposal on which approach (hosted platform vs. improved pipeline) before building
- AI-assisted development is expected and encouraged
- If you get stuck, ask in Discord
