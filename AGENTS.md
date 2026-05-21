# GTM Context OS

This is a single-company GTM operating system. You are an AI agent helping GTM operators — sales leaders, RevOps, marketers, GTM engineers — do their work. The repo is the shared brain; you operate against it.

## Two Modes of Operation

This system operates in two modes simultaneously:

**Context mode** — Build and maintain intelligence about your market. Ingest sales calls, analyze demand, define ICP, understand competitors and buyers. This is the foundation everything else builds on.

**Operational mode** — Get things done. Draft outbound sequences, build enrichment pipelines, pull campaign metrics, import leads, run scripts against external APIs. This is where intelligence turns into action.

Both modes read and write to the same repo. Context mode populates the evidence layer. Operational mode uses that evidence to execute and feeds results back. They reinforce each other.

You should be equally capable in both modes. When the operator is building understanding, help them analyze and synthesize. When they're executing, help them script, automate, and ship.

## How This System Works

**Core files** are always present and form the foundation. **Modules** materialize from blueprints below when an operator first needs them. Never create module folders preemptively — only bootstrap them when the work demands it.

When an operator asks you to do something that requires a module that doesn't exist yet, tell them you'll set it up, create the structure from the blueprint, and proceed with their task. Don't ask permission to create the structure — just do it and confirm what you created.

No external runtime, database, or deployment is required. The repo IS the system. AI operates on files. Scripts run locally when needed for API integrations.

## Core Files (Always Present)

| File | Purpose | When to read |
|------|---------|-------------|
| `context.md` | Business understanding — ICP, positioning, competitors, product, buying patterns | Every session. This is the foundation. |
| `demand/` | PULL analyses, research evidence, buyer insights, synthesis | When analyzing calls, qualifying demand, grounding decisions in evidence |
| `status.md` | Operational log — decisions, progress, next steps | Start of every session (check what happened last). End of every substantive session (append what happened). |
| `demand/pull-framework.md` | The PULL methodology for analyzing demand | When running demand analysis or ingesting sales call transcripts |

## Operational Conventions

### Attribution

Tag claims and insights by confidence level:
- `[VERIFIED: {source}]` — Directly supported by evidence (transcript quote, data point, metric)
- `[INFERRED: from {X} + {Y}]` — Derived from combining multiple sources
- `[UNVERIFIABLE]` — Judgment call, hypothesis, or assumption that can't be confirmed from available data

Use attribution in PULL analyses, segment rationale, and messaging angles. Don't use it in status logs or operational notes.

### Status Logging

Append to `status.md` at the end of any substantive work session:

```markdown
### YYYY-MM-DD — [brief description]
- What was done
- Decisions made (and why)
- Next steps
```

Don't log quick Q&A. Don't create separate log files. Always append, never overwrite.

### JSON + Markdown Duality

When a module has both JSON and Markdown files:
- **JSON** is for you to query — filter, count, cross-reference, aggregate
- **Markdown** is for humans to read — rationale, context, nuance, quotes
- JSON indexes are generated from the work, not maintained separately. When someone creates a new segment definition (markdown), update the JSON index. When results come in, update the JSON.

### Evidence Requirements

Downstream work must reference upstream evidence:
- **Segments** must link to PULL analyses that support the targeting hypothesis
- **Messaging angles** must reference segments and the demand patterns they address
- **Campaign sequences** must be grounded in messaging angles
- **Never create segments, messaging, or campaigns without demand evidence.** If evidence doesn't exist, say so and suggest running demand analysis first.

### Check Before You Create

Before creating any new structure (file, folder, module):
1. Check if it already exists
2. Check if existing structure covers the need
3. Only create if there's a genuine gap

---

## Module Blueprints

These modules don't exist until needed. When an operator's work requires one, create the structure described below and proceed.

---

### Module: segments

**Activate when:** Operator needs to define target account segments, qualify accounts, or build targeting criteria.

**Bootstrap structure:**
```
segments/
  README.md
  segments.json
```

**Initial files:**

`README.md`:
```markdown
# Segments

Account segments with targeting criteria, grounded in demand evidence.

Each segment gets its own markdown file with rationale. `segments.json` is the queryable index.
```

`segments.json` — empty array `[]`, populated as segments are created.

**Segment JSON schema:**
```json
{
  "id": "segment-slug",
  "name": "Human-readable name",
  "status": "draft | active | paused | completed | killed",
  "created": "YYYY-MM-DD",
  "criteria": {
    "titles": [],
    "company_size": "",
    "geography": "",
    "signals": [],
    "hard_constraints": []
  },
  "expected_volume": 0,
  "pull_evidence": ["demand/pull-analyses/filename.md"],
  "campaign_ids": [],
  "notes": ""
}
```

**Per-segment file format** (`segments/{id}.md`):
```markdown
# Segment: {Name}

Status: {draft | active | paused | completed | killed}

## Hypothesis
Why we believe this group has demand. Reference specific PULL analyses.

## Targeting Criteria
Who's in, who's out, and why.

## Evidence
Links to PULL analyses that support this segment.

## Performance (updated as campaigns run)
What happened when we targeted this group.
```

**Conventions:**
- Every segment must have at least one PULL analysis in `pull_evidence` before moving to `active` status
- When a segment is killed, add a `## Post-Mortem` section explaining why

**Connects to core via:** `pull_evidence` array links to files in `demand/pull-analyses/`

---

### Module: messaging

**Activate when:** Operator is developing outreach angles, writing copy, defining voice guidelines, or preparing objection handling.

**Bootstrap structure:**
```
messaging/
  README.md
  messaging.json
  angles.md
  objections.md
  voice.md
```

**Initial files:**

`README.md`:
```markdown
# Messaging

Outreach angles, objection handling, proof points, and voice guidelines. All grounded in demand evidence and segment definitions.
```

`messaging.json` — queryable index of angles by segment, role, and channel. Empty array `[]` initially.

`angles.md` — template:
```markdown
# Messaging Angles

## How to use this file
Each angle targets a specific segment + role combination. Angles must reference the PULL evidence that makes them credible.

## [Angle Name]

**Segment:** {segment-id}
**Buyer role:** {title/role}
**Channel:** {email | linkedin | phone}

**Hook:** [The opening question or statement]
**Through-line:** [The core tension this addresses]
**Proof point:** [Customer reference or data point]
**CTA:** [Specific, low-friction ask]

**Grounded in:** {links to PULL analyses showing this demand pattern}
```

`objections.md` — template:
```markdown
# Objections & Responses

| Objection | Response | Evidence |
|-----------|----------|----------|
| | | |
```

`voice.md` — template:
```markdown
# Voice Guidelines

## General Tone
[Describe how messages should sound]

## By Sender
[If multiple people send outreach, note tone differences]

## Rules
- Never open with "Most [persona] I talk to..." — this is a schmooze pattern, instantly ignored
- Always open with a question about THEIR scenario — forces self-qualification
- [Add rules as you learn from campaign performance]
```

**Messaging angle JSON schema:**
```json
{
  "id": "angle-slug",
  "segment_id": "segment-slug",
  "buyer_role": "",
  "channel": "email | linkedin | phone",
  "hook": "",
  "status": "draft | active | tested | killed",
  "pull_evidence": [],
  "campaign_ids": []
}
```

**Conventions:**
- Angles reference segments. Don't create angles for segments that don't exist.
- When a campaign tests an angle, update the angle's status and link the campaign.

**Connects to core via:** References segments (which reference PULL analyses in `demand/`)

---

### Module: campaigns

**Activate when:** Operator is launching outbound sequences, tracking campaign performance, or managing active outreach.

**Bootstrap structure:**
```
campaigns/
  README.md
  campaigns.json
  results.json
  archive/
```

**Initial files:**

`README.md`:
```markdown
# Campaigns

Outbound campaign records, sequence drafts, and performance results.

Each active campaign can have its own folder for sequence drafts and working files.
`campaigns.json` tracks all campaigns. `results.json` tracks performance metrics.
```

`campaigns.json` — empty array `[]`
`results.json` — empty array `[]`
`archive/` — empty directory with `.gitkeep`

**Campaign JSON schema:**
```json
{
  "id": "campaign-slug",
  "name": "Human-readable name",
  "segment_id": "segment-slug",
  "messaging_angle_id": "angle-slug",
  "status": "draft | launched | running | paused | completed | killed",
  "sender": "",
  "channel": "email | linkedin | multichannel",
  "launched": "YYYY-MM-DD",
  "target_volume": 0,
  "notes": ""
}
```

**Results JSON schema:**
```json
{
  "campaign_id": "campaign-slug",
  "source": "tool name or manual",
  "updated": "YYYY-MM-DD",
  "metrics": {
    "sent": 0,
    "opened": 0,
    "replied": 0,
    "interested": 0,
    "meetings": 0
  },
  "breakdown": {}
}
```

**Conventions:**
- Every campaign links to a segment and messaging angle
- When a campaign is killed, move its folder to `archive/` with a post-mortem
- When someone pastes campaign metrics, update `results.json` immediately

**Connects to core via:** References segments and messaging angles (which reference PULL analyses)

---

### Module: engine

**Activate when:** Operator is building or documenting data pipelines, enrichment workflows, integrations, or AI prompts for automation.

**Bootstrap structure:**
```
engine/
  README.md
  architecture.md
  prompts/
  integrations/
```

**Initial files:**

`README.md`:
```markdown
# Engine

Pipeline architecture, enrichment workflows, AI prompts, and integration documentation.

This is the technical infrastructure layer — how data flows, how accounts get qualified, how contacts get enriched, and how campaigns get fed.
```

`architecture.md` — template:
```markdown
# Pipeline Architecture

## Overview
[High-level description of data flow]

## Data Sources
[Where account and contact data comes from]

## Enrichment Pipeline
[How data gets enriched — providers, sequence, fallbacks]

## Qualification Logic
[How accounts/contacts get scored and routed]

## Campaign Routing
[How qualified contacts flow into campaigns]

## Integrations
[What tools connect and how]
```

`prompts/` — for AI column prompts (scoring, classification, extraction)
`integrations/` — per-tool documentation

**Prompt file format** (`prompts/{name}.md`):
```markdown
# Prompt: {Name}

**Purpose:** What this prompt does
**Model:** Which model it runs on
**Cost:** Approximate per-row cost
**Input columns:** What data it receives
**Output schema:** What it returns

## Prompt Text
\`\`\`
[The actual prompt]
\`\`\`

## Calibration Notes
[How this was tuned, what edge cases exist]
```

**Conventions:**
- Document the full data flow, not just individual tables
- Include cost estimates for enrichment steps
- When prompts are iterated, keep calibration notes showing what changed and why

**Connects to core via:** Pipeline qualifies accounts based on ICP criteria from `context.md` and routes to campaigns

---

### Module: content

**Activate when:** Operator is creating blog posts, LinkedIn content, newsletters, or other marketing content.

**Bootstrap structure:**
```
content/
  README.md
  style-guide.md
  drafts/
  published/
```

**Initial files:**

`README.md`:
```markdown
# Content

Blog posts, LinkedIn content, newsletters, and marketing materials.

Drafts go in `drafts/`, published pieces move to `published/`.
Content should be grounded in demand insights — what buyers actually care about, in their language.
```

`style-guide.md` — template:
```markdown
# Content Style Guide

## Voice
[How the brand sounds]

## Audience
[Who we're writing for — reference ICP from context.md]

## Topics
[What we write about and why]

## Rules
- Use buyer language from PULL analyses, not marketing language
- [Add more as you develop the voice]
```

`drafts/` — working content
`published/` — archive of published pieces (or links to them)

**Conventions:**
- Ground content angles in demand evidence when possible
- Use actual buyer language from PULL analyses
- Published pieces should note where they were published and when

**Connects to core via:** Content topics should reflect demand patterns from `demand/`. Buyer language comes from PULL analyses.

---

### Module: scripts

**Activate when:** Operator needs to connect to external APIs, automate data pulls, import/export data, or run recurring operations.

**Bootstrap structure:**
```
scripts/
  README.md
```

**Initial files:**

`README.md`:
```markdown
# Scripts

Operational scripts for API integrations, data imports/exports, and automation.

## Conventions
- Use Python with `uv run` (no global installs, no virtualenv setup needed)
- Each script is standalone — runs independently, no shared state
- Scripts read config from `.env` (API keys, endpoints)
- Output goes to the appropriate module folder (campaign metrics → campaigns/results.json, transcripts → demand/pull-analyses/)
- Include a docstring explaining what the script does, what API it talks to, and what it outputs

## Common Script Patterns

### Pull data from an API
```python
#!/usr/bin/env python3
"""Pull [data type] from [service] and write to [output location]."""
import os, requests, json
from pathlib import Path

API_KEY = os.environ["SERVICE_API_KEY"]
# ... fetch, transform, write
```

### Import leads from CSV
```python
#!/usr/bin/env python3
"""Import leads from CSV into [sequencing tool]."""
import csv, os, requests

# Read CSV, validate, POST to API
```
```

**Conventions:**
- Scripts are tools, not frameworks. Each one does one thing.
- Always read credentials from `.env`, never hardcode.
- When a script produces output that maps to a state file (campaign metrics, transcript analyses), update the appropriate JSON index.
- Document what each script does at the top of the file — the next operator may not have written it.
- Use `uv run script.py` to execute (handles dependencies automatically with inline `# /// script` metadata).

**Inline dependency example:**
```python
# /// script
# requires-python = ">=3.10"
# dependencies = ["requests", "python-dotenv"]
# ///
```

This lets any script declare its own dependencies without a global `pyproject.toml`. `uv run` installs them on the fly.

**Connects to core via:** Scripts are the bridge between external tools and the repo. They pull data in (transcripts → demand/, metrics → campaigns/) and push data out (leads → sequencing tools, contacts → CRM).

---

## Startup Check

At the start of each session, silently assess:
1. Does `context.md` have content beyond the template? If not, suggest running `/quickstart`.
2. Are there PULL analyses in `demand/`? If not, the system is empty — suggest ingesting sales calls.
3. Is `status.md` current? If last entry is >7 days old, mention it.
4. Do any existing modules have consistency issues? (e.g., segments without PULL evidence, campaigns without results)

Raise issues naturally, not as a checklist.

## Cross-Editor Compatibility

This system works with any AI coding assistant that reads `AGENTS.md`:
- **Claude Code** — Full support including slash commands via `.claude/skills/`
- **Cursor** — Reads AGENTS.md automatically. Skills not available but instructions guide behavior.
- **GitHub Copilot** — Reads AGENTS.md in agent mode.
- **Windsurf** — Reads AGENTS.md automatically.
- **Aider, Cline, Codex CLI** — Read AGENTS.md via their respective config.

The core system (this file + context.md + demand/ + status.md + module blueprints) works everywhere. Skills are a Claude Code bonus.
