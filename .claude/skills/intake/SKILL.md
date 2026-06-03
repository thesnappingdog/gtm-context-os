---
name: intake
description: "Process raw documents into structured, attributed knowledge. Drop docs into _intake/, run this skill to dissect them into the right places. Incremental — run as many times as needed."
argument-hint: "[optional: specific file path or 'all' to process everything in _intake/]"
---

Dissect raw documents into clean, compartmentalized, attributed knowledge across the repo.

## Core Principle

Your job is to be a diligent librarian, not a skeptic. Accept what the user provides, organize it properly, tag it honestly, and ask smart questions about gaps. Never dismiss inputs — instead, place them and ask what would strengthen them.

**Bad:** "This ICP definition has no evidence backing it — marking as unverifiable."
**Good:** "I've placed your ICP definition in context.md. To strengthen it with data, do you have win/loss rates by segment, pipeline metrics, or recorded sales calls?"

## When to Use

- First time: user has existing documents (pitch decks, playbooks, competitor analyses, CRM exports, product docs) and wants to bootstrap their context OS
- Later: user has new documents to add — a fresh competitor analysis, updated pricing, new call recordings
- Anytime: user says "process this", "add this to the system", "intake these docs"

## Intake Folder

Documents go in `_intake/` at repo root. Create it if it doesn't exist.

```
_intake/
  pitch-deck.pdf
  sales-playbook.docx
  competitor-comparison.xlsx
  recent-call-notes.md
  pricing-2024.pdf
  _processed.json          ← tracks what's been processed
```

`_processed.json` tracks which files have been processed and when:
```json
[
  {"file": "pitch-deck.pdf", "processed": "2025-03-15", "outputs": ["context.md"]}
]
```

On each run, only process files not in `_processed.json` (unless user says "reprocess all").

## Process

### Step 1: Scan

List everything in `_intake/`. Compare against `_processed.json`. Report:
- New files to process
- Previously processed files (skip unless asked)
- File types detected

If user pointed to a specific file (not in `_intake/`), process it directly.

### Step 2: Read and Classify

For each document, identify what type it is:

| Document type | Look for | Examples |
|---|---|---|
| Pitch deck / overview | Company description, value prop, market size, team | PDF slides, investor deck |
| Sales playbook | Objection handling, talk tracks, qualification criteria | Internal docs, wikis |
| Competitor analysis | Feature comparisons, positioning maps, win/loss reasons | Spreadsheets, docs |
| Call notes / summaries | Buyer quotes, deal context, meeting notes | Text files, CRM exports |
| CRM export | Deal data, contact lists, pipeline metrics | CSV, spreadsheets |
| Product docs | Features, specs, roadmap, architecture | Internal docs |
| Pricing / packaging | Tiers, deal sizes, discounting rules | Sheets, PDFs |
| ICP / persona docs | Target profiles, buyer personas, market research | Docs, presentations |
| Marketing content | Blog posts, case studies, landing page copy | Docs, URLs |
| Process docs | Workflows, SOPs, team structures | Internal docs |

### Step 3: Extract and Attribute

For each document, extract structured facts. Tag every claim:

**Facts** (directly stated and verifiable):
- Company has 50 employees → `[VERIFIED: {source document}]`
- Product launched in 2023 → `[VERIFIED: {source document}]`
- Revenue is $2M ARR → `[VERIFIED: {source document}]`

**Positioned claims** (stated but reflect a perspective):
- "We're the only platform that does X" → `[CLAIMED: {source document}]` — place it, but note it's a positioning statement
- "Our ICP is VP Engineering at Series B" → `[CLAIMED: {source document}]` — accept as working definition, note what would validate it
- "Competitors can't handle enterprise scale" → `[CLAIMED: {source document}]` — competitive assertion, useful but partial

**Derived insights** (you inferred by combining sources):
- Pitch deck says "mid-market" + pricing shows $20K ACV → `[INFERRED: from pitch deck + pricing]`

The key distinction: `[CLAIMED]` is not a judgment — it means "this is what the company believes, and it's useful context." It becomes `[VERIFIED]` when demand evidence or data confirms it.

### Step 4: Route to Destinations

Place extracted knowledge into the right locations:

**→ context.md**
- Company basics (what they do, stage, size, product)
- ICP definition (firmographic + demographic criteria)
- Positioning (value prop, differentiation)
- Competitors (names, strengths, weaknesses, displacement angles)
- Buying patterns (triggers, timeline, process)
- Disqualification rules

When updating context.md, merge with existing content. Don't overwrite — add, refine, or flag conflicts.

**→ demand/**
- Call notes or meeting summaries → `demand/pull-analyses/` if they contain enough buyer voice for PULL analysis
- Call notes too thin for PULL analysis → `demand/pull-analyses/` with a note that evidence is partial
- Market research with buyer behavior data → `demand/` as supporting evidence
- Win/loss analysis → `demand/` as supporting evidence

**→ messaging/ (bootstrap if needed)**
- Objection handling → `messaging/objections.md`
- Talk tracks → `messaging/angles.md`
- Voice/tone guidelines → `messaging/voice.md`
- Case study quotes or proof points → `messaging/angles.md` proof points

**→ segments/ (bootstrap if needed)**
- Named segments or personas → `segments/{name}.md` (targeting criteria, hypothesis, and rationale live in this markdown file)
- Segment index entry (id, name, status, pull_evidence) → `segments/segments.json`

**→ campaigns/ (bootstrap if needed)**
- Past campaign data → `campaigns/campaigns.json` + relevant campaign folder
- Sequence templates → `campaigns/{name}/`

**→ engine/ (bootstrap if needed)**
- Pipeline/workflow docs → `engine/architecture.md`
- Tool configurations → `engine/integrations/`

**→ content/ (bootstrap if needed)**
- Published content → `content/published/`
- Style guides → `content/style-guide.md`

When a document spans multiple destinations, extract the relevant pieces to each. The source file stays in `_intake/` as reference.

### Step 5: Update Indexes

After routing, update any relevant JSON indexes:
- New PULL analyses → update `demand/pull-index.json`
- New segments → update `segments/segments.json`
- New campaigns → update `campaigns/campaigns.json`
- New campaign metrics → update `campaigns/campaigns.json` (add metrics to the campaign entry)

### Step 6: Gap Analysis

After processing, assess what's well-covered and what needs more depth. Frame gaps as requests, not criticisms.

**Coverage report:**
```
## What I Learned

### Well-Covered
- Company overview: clear product description, stage, team size
- Competitors: 4 competitors identified with positioning differences
- Product: feature set documented with pricing tiers

### Needs More Depth
- **ICP definition** — I have titles and company sizes from the playbook, 
  but no data on which segments actually convert. Do you have:
  - Win/loss rates by segment?
  - Pipeline data showing where deals come from?
  - Close rates by company size or title?

- **Demand evidence** — Positioning claims are placed but unvalidated. 
  To test whether your ICP actually has demand:
  - Do you have recorded sales calls or transcripts?
  - Call notes with buyer quotes?
  - Discovery call recordings from Gong/Fireflies/Zoom?

- **Campaign history** — No past performance data found. If you have:
  - Outbound metrics (sent/opened/replied/meetings)?
  - Which messages/angles worked best?
  - A/B test results?

### Conflicts Detected
- Pitch deck says ICP is "mid-market (200-2000 employees)" but 
  playbook targets "SMB (50-500)". Which is current?
```

**Rules for gap analysis:**
- Max 3-4 gaps per run. Don't overwhelm.
- Frame each gap as "here's what would make this stronger" with a specific ask
- If the system is early (first intake), focus on the highest-leverage gaps: demand evidence and ICP validation
- If the system has existing PULL analyses, cross-reference new inputs against demand evidence. Flag where claims align or conflict with what buyers actually say.

### Step 7: Update Tracking

Add processed files to `_processed.json` with timestamp and output destinations.

Update `status.md` with what was ingested and key findings.

## Incremental Runs

Each run only processes new files. The system accumulates knowledge over time:

- **Run 1:** Pitch deck + playbook → bootstraps context.md, asks for data
- **Run 2:** User drops in CRM export → adds pipeline metrics, refines ICP with numbers
- **Run 3:** User adds call recordings → PULL analyses validate or challenge ICP assumptions
- **Run 4:** User drops competitor update → refreshes context.md competitors section

On each run, check if new inputs resolve gaps flagged in previous runs. "Last time I noted your ICP lacked conversion data — this CRM export fills that gap. Updating context.md with verified segment performance."

## Handling Conflicts

When new documents contradict existing repo content:
1. Don't silently overwrite
2. Flag the conflict: "Pitch deck (2024) says X, but your just-added competitor analysis says Y"
3. Ask the user which is current
4. Update with proper attribution showing the source

## What This Skill Does NOT Do

- Does not run full PULL analyses on call transcripts — that's a separate process guided by `demand/pull-framework.md`
- Does not generate strategy or recommendations — it organizes what exists
- Does not evaluate whether the business strategy is good — it structures it honestly
- Does not delete or archive source documents — they stay in `_intake/` for reference
