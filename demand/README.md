# Demand

Evidence-based understanding of who has demand for your product and why.

## What Goes Here

- **PULL analyses** (`pull-analyses/`) — One per sales call or prospect conversation. Structured using the PULL framework. Created as calls are analyzed.
- **Pull index** (`pull-index.json`) — Machine-queryable index of all analyses. Auto-maintained by the AI as analyses are added. Schema defined in AGENTS.md.
- **Synthesis** (`synthesis.md`) — Patterns across multiple analyses. Created by the AI after 5+ analyses accumulate — not before, since patterns need data.
- **Buyer insights** (`buyer-insights.md`) — Synthesized patterns about buyer behavior, triggers, and conversion signals. Emerges after synthesis, when enough evidence exists to generalize.
- **Hypothesis** (`hypothesis.md`) — Initial demand hypothesis if no call transcripts are available yet. Created during `/quickstart` as a starting point to validate.

## How It Works

1. Paste sales call transcripts — the AI reads `pull-framework.md` and produces a PULL analysis per call
2. `pull-index.json` gets updated automatically as analyses are added
3. After 5+ analyses, the AI synthesizes patterns into `synthesis.md`
4. Use `/pull-query` to search analyses for evidence when building segments or messaging
5. As patterns solidify, `buyer-insights.md` captures generalizable buyer behavior

## The PULL Framework

See `pull-framework.md` for the full methodology.
