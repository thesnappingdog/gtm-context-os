# Demand

Evidence-based understanding of who has demand for your product and why.

## What Goes Here

- **PULL analyses** (`pull-analyses/`) — One per sales call or prospect conversation. Structured using the PULL framework. Created as calls are analyzed.
- **Pull index** (`pull-index.json`) — Machine-queryable index of all analyses. Auto-maintained by the AI as analyses are added. Schema defined in AGENTS.md.
- **Notes** (`notes/`) — Raw call notes, meeting summaries, and thin inputs that aren't detailed enough for full PULL analysis. Useful as context and raw material for future analysis when better transcripts arrive.
- **Research** (`research/`) — Market research, win/loss analyses, buyer behavior data, and other evidence that informs demand understanding but isn't a single-call PULL analysis.
- **Synthesis** (`synthesis.md`) — Patterns across multiple analyses. Created by the AI after 5+ analyses accumulate — not before, since patterns need data.
- **Key learnings** (`key-learnings.md`) — Actionable distillation of who buys, when, and why: targeting, messaging, and the qualification framework. Produced alongside `synthesis.md` after a full batch of analyses.
- **Hypothesis** (`hypothesis.md`) — Initial demand hypothesis if no call transcripts are available yet. Created during `/quickstart` as a starting point to validate.

## How It Works

1. Paste sales call transcripts — the AI reads `pull-framework.md` and produces a PULL analysis per call
2. `pull-index.json` gets updated automatically as analyses are added
3. After 5+ analyses, the AI synthesizes patterns into `synthesis.md`
4. Use `/pull-query` to search analyses for evidence when building segments or messaging
5. Alongside `synthesis.md`, `key-learnings.md` distills who buys, when, and why — the actionable layer for targeting and messaging

## The PULL Framework

See `pull-framework.md` for the full methodology.
