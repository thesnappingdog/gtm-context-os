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

### JSON Indexes — AI-Maintained Infrastructure

JSON index files (e.g., `segments.json`, `campaigns.json`, `pull-index.json`) are **your internal navigation system**. They exist so you can quickly trace relationships between entities without re-reading every markdown file.

**Design principles:**
- **You create and maintain these.** The operator never edits or reads them directly.
- **Update them automatically** as a side effect of work — when you create a segment markdown file, update segments.json in the same operation. Don't ask permission.
- **Keep schemas minimal** — only store what you need to navigate relationships. IDs, names, statuses, and links to other entities. Don't store data that requires the operator to manually paste it back.
- **Markdown is for humans** — rationale, context, nuance, quotes, buyer language live in `.md` files. JSON is for you to query and link.
- **Reconcile on session start** — if indexes look out of sync with the markdown files, fix them silently.

**Pull index schema** (`demand/pull-index.json`):
```json
{
  "id": "acme-jane-doe",
  "company": "Acme Corp",
  "prospect": "Jane Doe",
  "pull_score": 16,
  "classification": "demand (14+) | benefit (8-13) | neither (0-7)",
  "would_close": "yes | likely | unlikely | no",
  "primary_trigger": "scaling_team",
  "buyer_type": "vp_engineering",
  "features_resonated": ["integration", "reporting"],
  "date": "2026-01-15",
  "file": "demand/pull-analyses/acme-jane-doe.md"
}
```

This schema is derived from the PULL analysis template in `demand/pull-framework.md`. When you write a PULL analysis, extract these fields into the index entry. The full analysis (quotes, context, reasoning) stays in the markdown file.

### Synthesis Trigger

After saving a PULL analysis and updating `pull-index.json`, check the analysis count. If there are 5+ analyses and `demand/synthesis.md` does not exist, offer to create it — patterns need at least this many data points to be meaningful. If `synthesis.md` already exists, check whether the new analysis introduces a pattern not yet captured and offer to update it.

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

`segments.json` — empty array `[]`, auto-maintained as segments are created.

**Segment JSON schema (minimal — for AI navigation):**
```json
{
  "id": "segment-slug",
  "name": "Human-readable name",
  "status": "draft | active | paused | killed",
  "pull_evidence": ["demand/pull-analyses/filename.md"],
  "campaign_ids": []
}
```

Targeting criteria, rationale, and performance notes live in the segment's markdown file — not duplicated here.

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

**Worked example** (`segments/new-people-leaders.md`):
```markdown
# Segment: New People Leaders Building From Scratch

Status: active

## Hypothesis
New VP/Head of People hired at 100-300 person companies with no existing performance infrastructure. They have 3-6 months to show results to the board. This creates unavoidable demand — they must ship a review process, and spreadsheets won't cut it.

## Targeting Criteria
**In:**
- Title: VP People, Head of People, Chief People Officer — joined within last 6 months
- Company: 100-300 employees, Series A-B, no existing performance management tool detected
- Signal: recently hired into a newly created role (LinkedIn job change + no predecessor in role)

**Out:**
- Companies with Lattice/Culture Amp/15Five already in tech stack
- People leaders at companies >500 (different buying process, committee decisions)
- Consultants or fractional people leaders (no budget authority)

## Evidence
- [demand/pull-analyses/acme-jane-smith.md](demand/pull-analyses/acme-jane-smith.md) — PULL 18/20, board deadline, building from zero
- [demand/pull-analyses/betaco-mike-chen.md](demand/pull-analyses/betaco-mike-chen.md) — PULL 15/20, new hire, inherited spreadsheet mess

Pattern: 3 of 5 "demand" classified calls share this profile. Board pressure or exec mandate is the common accelerant.

## Performance
- C1-new-leaders campaign: 4.2% reply rate, 2 meetings from 120 leads (launched 2026-02-01)
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

`messaging.json` — AI-maintained index linking angles to segments and evidence. Empty array `[]` initially.

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

**Messaging angle JSON schema (minimal — for AI navigation):**
```json
{
  "id": "angle-slug",
  "segment_id": "segment-slug",
  "status": "draft | active | tested | killed",
  "pull_evidence": [],
  "campaign_ids": []
}
```

Buyer role, channel, hook text, and rationale live in `angles.md` — not duplicated in JSON.

**Worked example** (entry in `angles.md`):
```markdown
## Board Deadline — New People Leader

**Segment:** new-people-leaders
**Buyer role:** VP People / Head of People
**Channel:** email

**Hook:** "Are you building a review process from scratch, or replacing one that stopped working?"
**Through-line:** New people leaders at growing companies get 3-6 months to show the board they've built real infrastructure. Spreadsheets won't survive the first cycle at 150+ people.
**Proof point:** "A VP People at a 180-person SaaS company ran their first review cycle in 3 weeks after searching for 2 months." [INFERRED: from acme-jane-smith PULL analysis — compressed timeline, fast implementation was decisive]
**CTA:** "Worth a 15-min look at how [product] handles first-cycle setup?"

**Grounded in:**
- [demand/pull-analyses/acme-jane-smith.md] — board mandate, 6-week deadline, rejected Lattice for complexity
- [demand/pull-analyses/betaco-mike-chen.md] — inherited spreadsheets, needed something live in Slack
```

**Conventions:**
- Angles reference segments. Don't create angles for segments that don't exist.
- When a campaign tests an angle, update the angle's status and link the campaign.

**Connects to core via:** References segments (which reference PULL analyses in `demand/`)

---

### Module: campaigns

**Activate when:** Operator is launching campaigns of any kind — outbound sequences, content programs, paid ads, events, webinars — or wants to track what's been run.

**Bootstrap structure:**
```
campaigns/
  README.md
  campaigns.json
  archive/
```

**Initial files:**

`README.md`:
```markdown
# Campaigns

Campaign records and working files. "Campaign" means any coordinated GTM effort targeting a segment — outbound sequences, content pushes, paid programs, events, whatever your team runs.

Each active campaign can have its own folder for drafts and working files.
`campaigns.json` is maintained by the AI to link campaigns back to segments and messaging.
```

`campaigns.json` — empty array `[]`, auto-maintained
`archive/` — empty directory with `.gitkeep`

**Campaign JSON schema (minimal — for AI navigation):**
```json
{
  "id": "campaign-slug",
  "name": "Human-readable name",
  "type": "outbound | content | paid | event | other",
  "segment_id": "segment-slug",
  "messaging_angle_id": "angle-slug",
  "status": "draft | active | paused | completed | killed"
}
```

The `type` field distinguishes how the campaign reaches its audience. All types follow the same evidence chain (segment → messaging → campaign). Details like channel, sender, metrics, and sequence drafts live in the campaign's own folder (`campaigns/{id}/`), not in the JSON.

**If the operator pastes results or metrics**, store them in the campaign's folder as markdown or add to the JSON entry as an optional `metrics` object. Don't require a separate results file — let it emerge if the operator actually tracks metrics.

**Conventions:**
- Every campaign links to a segment and messaging angle
- What "campaign" means is defined by the operator — don't force outbound-only assumptions
- When a campaign is killed, move its folder to `archive/` with a post-mortem

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
  integrations/        ← ships pre-populated with API references for common tools
```

**Note:** `engine/integrations/` exists from initial setup with references for HubSpot, Gong, Fireflies, Lemlist, Clay, and Apollo. When bootstrapping the engine module, keep these files — only create `README.md`, `architecture.md`, and `prompts/`.

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
  topics.md
  style-guide.md
  drafts/
  published/
```

**Initial files:**

`README.md`:
```markdown
# Content

Blog posts, LinkedIn content, newsletters, and marketing materials.

Topics are derived from demand patterns — what buyers actually search for, ask about, and struggle with. `topics.md` maps demand evidence to content ideas. Drafts go in `drafts/`, published pieces move to `published/`.
```

`topics.md` — template:
```markdown
# Content Topics

Topics derived from demand evidence. Each topic should connect to real buyer scenarios.

## How to Use

Review PULL analyses for recurring triggers, questions, and language patterns. Each becomes a topic cluster.

## Topic Map

| Topic | Demand Pattern | PULL Evidence | Content Ideas | Status |
|-------|---------------|---------------|---------------|--------|
| | | | | |

## Topic Development Rules
- Every topic must reference at least one PULL analysis or demand pattern
- Write about what buyers are already searching for, not what you wish they'd search for
- Use their language — if they say "scaling reviews" not "performance management transformation", use "scaling reviews"
- One topic per demand trigger — don't combine unrelated buyer scenarios
```

`style-guide.md` — template:
```markdown
# Content Style Guide

## Voice
[How the brand sounds]

## Audience
[Who we're writing for — reference ICP from context.md]

## Topics
See topics.md for demand-derived topic clusters.

## Distribution
[Where content gets published — LinkedIn, blog, newsletter, etc.]
[Cadence — how often, what format per channel]

## Rules
- Use buyer language from PULL analyses, not marketing language
- Lead with the scenario, not the product
- [Add more as you develop the voice]
```

`drafts/` — working content
`published/` — archive of published pieces (or links to them)

**Conventions:**
- Ground content topics in demand evidence — `topics.md` is the bridge between PULL analyses and content planning
- Use actual buyer language from PULL analyses
- Published pieces should note where they were published, when, and performance if tracked
- When new PULL analyses reveal recurring questions or triggers, check if they map to existing topics or suggest new ones

**Connects to core via:** Content topics are derived from demand patterns in `demand/`. Buyer language comes from PULL analyses. `topics.md` explicitly links topics to evidence.

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
1. Does `context.md` have content beyond the template? If not, suggest running `/start` (Claude Code) or ask "what should I do first?" (other editors).
2. Are there PULL analyses in `demand/`? If not, the system is empty — suggest ingesting sales calls.
3. Is `status.md` current? If last entry is >7 days old, mention it.
4. **Reconcile JSON indexes** — if any module's JSON index is out of sync with its markdown files (missing entries, stale statuses, broken links), fix it silently. Don't ask.
5. Do any existing modules have broken evidence chains? (e.g., segments without PULL evidence links, campaigns pointing to deleted segments)

Raise issues naturally, not as a checklist. Fix index drift silently — only mention it if you find broken evidence chains that need operator input.

## Cross-Editor Compatibility

This system works with any AI coding assistant. `AGENTS.md` is the single source of truth; editor-specific pointer files redirect to it.

| Editor | How it loads instructions |
|--------|-------------------------|
| Claude Code / Cowork | `.claude/rules/` (scoped) + `.claude/CLAUDE.md` + skills |
| Cursor | Reads `.cursorrules` → points to `AGENTS.md` |
| GitHub Copilot | Reads `AGENTS.md` directly in agent mode |
| Windsurf | Reads `.windsurfrules.md` → points to `AGENTS.md` |
| Aider | Via `read: AGENTS.md` in config |
| Cline | Add `AGENTS.md` to context files |

The core system (this file + context.md + demand/ + status.md + module blueprints) works everywhere. Skills are a Claude Code bonus — other editors get the same methodology and blueprints via AGENTS.md.
