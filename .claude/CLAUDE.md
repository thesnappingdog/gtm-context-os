# Claude Code Configuration

Read `AGENTS.md` in the repo root for full system instructions, module blueprints, and operational conventions.

This file adds Claude Code-specific capabilities (skills) on top of the universal AGENTS.md instructions.

## Skills

Available slash commands for GTM operations:

| Skill | Purpose |
|-------|---------|
| `/start` | First thing to run — checks repo state, recommends what to do next |
| `/bootstrap` | Fastest setup — give a website URL, agents crawl and populate context.md |
| `/quickstart` | Guided first-use setup — fill context.md, first demand evidence |
| `/setup-env` | Check base technical environment — Python, uv, .env, .mcp.json |
| `/setup-api` | Connect a specific tool — scaffolds scripts, MCP config, integration docs |
| `/intake` | Process raw documents into structured knowledge — drop docs in `_intake/`, run to dissect |
| `/gtm-status` | Dashboard of current GTM state across all modules |
| `/pull-query` | Search demand analyses for evidence |
| `/segment-messaging` | Match a segment to messaging angles using PULL evidence |
| `/draft-sequence` | Write an outbound sequence grounded in demand data |
| `/run-eval` | Run eval suite against current repo state — tests instruction correctness |

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

## JSON Index Maintenance

JSON indexes (`pull-index.json`, `segments.json`, `messaging.json`, `campaigns.json`) are your internal infrastructure. The operator never reads or edits them.

**When to update:**
- You create/modify a markdown file in a module directory → update that module's JSON index in the same operation
- Session start → reconcile indexes silently (fix drift, don't ask)
- Operator pastes data that implies state changes → update indexes as side effect

**Never ask the operator** to update an index, verify an index, or paste data specifically to feed an index. These are your files.
