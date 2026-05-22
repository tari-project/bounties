---
repo: tari-project/faqqer
issue: 1
labels: [bounty, bounty-L]
original_size: none
---

## Bounty: Replace Faqqer with Self-Learning Multi-Channel AI Help Bot

**Tier:** L — 150,000 XTM

### Description

Faqqer is a basic Python Telegram bot that answers FAQ questions from static knowledge base files via OpenAI, posts blockchain stats, and runs periodic customer service analysis. Replace it with a production-quality, self-learning AI help system that works across multiple channels (Telegram, Discord, and potentially web embed), backed by a knowledge base that can be updated without code changes. The replacement should be built on or forked from an existing open-source knowledge-base AI help framework rather than written from scratch.

### Acceptance Criteria

- [ ] An open-source knowledge-base help framework is selected and documented (with rationale for the choice)
- [ ] The bot responds to user questions on Telegram with answers grounded in the Tari knowledge base (FAQ files, docs, prior Q&A)
- [ ] The bot responds to user questions on Discord with the same knowledge base
- [ ] Knowledge base content can be added/updated by editing files or using an admin interface, without code changes or redeployment
- [ ] The system learns from new Q&A interactions: questions that get positive feedback or admin-approved answers are incorporated into future responses
- [ ] Existing faqqer functionality is preserved: blockchain stats posting (configurable schedule) and customer service analysis (periodic channel scanning)
- [ ] Deployment is containerized (Docker) with clear setup documentation

### Context

- Current bot: https://github.com/tari-project/faqqer
- Python, Telegram-only, uses OpenAI API with static FAQ text files in `faqs/` directory
- Three jobs: FAQ responses (`faqqer_bot.py`), blockchain stats (`blockchain_job.py`), customer analysis (`customer_analysis_job.py`)
- Knowledge base is currently just flat text files, manually maintained
- Candidate open-source frameworks to evaluate: [Quivr](https://github.com/QuivrHQ/quivr), [Danswer](https://github.com/danswer-ai/danswer), [RAGFlow](https://github.com/infiniflow/ragflow), [Anything LLM](https://github.com/Mintplex-Labs/anything-llm), or similar RAG-based knowledge base systems
- The blockchain stats and customer analysis jobs can remain as separate scheduled tasks that post to configured channels

### How It Works

1. Comment on this issue to signal intent (courtesy, not a lock)
2. Fork the repo and do the work
3. Submit a PR that references the issue with a closing keyword (e.g. `Fixes #1`) so GitHub links your PR to the bounty automatically
4. Bounties are competitive. Multiple PRs may be submitted for the same bounty. Review comments are public, and contributors may borrow ideas from each other's work. The maintainer selects the PR that best solves the problem, considering code quality, completeness, and contributor behavior. In cases where multiple contributors made significant contributions, the maintainer may split the bounty. The maintainer's decision is final.
5. Earn XTM (processing may take up to a week; reach out to @possum on Discord with your Tari address)

### Notes

- Start with a proposal: which framework, why, and how you plan to integrate the existing faqqer jobs. Get approval before building.
- AI-assisted development is expected and encouraged
- If you get stuck, ask in Discord
