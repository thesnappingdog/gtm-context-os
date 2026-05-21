# Claude Code Configuration

Read `AGENTS.md` in the repo root for full system instructions, module blueprints, and operational conventions.

This file adds Claude Code-specific capabilities (skills) on top of the universal AGENTS.md instructions.

## Skills

Available slash commands for GTM operations:

| Skill | Purpose |
|-------|---------|
| `/quickstart` | Guided first-use setup — fill context.md, ingest first call |
| `/ingest` | Absorb a sales call transcript → structured PULL analysis |
| `/gtm-status` | Dashboard of current GTM state across all modules |
| `/pull-query` | Search demand analyses for evidence |
| `/segment-messaging` | Match a segment to messaging angles using PULL evidence |
| `/draft-sequence` | Write an outbound sequence grounded in demand data |

## Model Selection

- **Default (orchestration, execution):** Sonnet
- **Strategic work (PULL analyses, positioning, novel thinking):** Opus agents
- **Quick lookups:** Haiku

## Write-to-File Pattern for Bulk Analysis

When processing multiple transcripts:
1. Agent reads source, performs analysis
2. Agent writes output to file (e.g., `demand/pull-analyses/{id}.md`)
3. Agent returns only status — NOT the full analysis text
4. Main instance orchestrates batches, never sees full analysis content

Max 3 parallel agents to avoid context overflow.
