---
name: ingest
description: "Absorb a sales call transcript and produce a structured PULL analysis. Use when user pastes a transcript, provides a file path, or says 'analyze this call'."
argument-hint: "[transcript text, file path, or 'batch' for multiple]"
---

Transform a sales call transcript into a structured PULL demand analysis.

## What This Skill Does

Takes raw sales call content (transcript, notes, or recording summary) and produces a scored PULL analysis in `demand/pull-analyses/`. Updates `demand/pull-index.json` with the new entry.

## Process

### Step 1: Get the Transcript

Accept input as:
- Pasted text (most common)
- File path to a transcript file
- "batch" keyword to process multiple files from a directory

If pasted text is very long (>10k words), offer to condense first:
- Keep ALL prospect lines (the buyer's voice matters most)
- Keep rep questions (lines ending with ?)
- Keep short rep lines (<15 words)
- Remove long rep demo explanations and product narration
- Remove AI-generated summaries

### Step 2: Read Context

Load `context.md` for:
- What the product does
- Hard constraints (disqualification criteria)
- ICP definition

Load `demand/pull-framework.md` for scoring methodology.

### Step 3: Analyze

For each PULL component, extract:
- A score (0-5)
- The direct evidence (quote from prospect)
- Your reasoning

Also extract:
- **Call type** — Is this actually a sales call? (vs. customer success, internal, partner)
- **Company context** — Size, industry, stage
- **Current tools** — What they use today
- **Primary trigger** — What brought them to this call
- **Buyer type** — Role category
- **Features that resonated** — What excited them
- **Timeline** — How urgent
- **Would close** — yes | likely | unlikely | no
- **Key insights** — Non-obvious observations

### Step 4: Write Analysis

Create `demand/pull-analyses/{slug}.md` where slug is `{company-name}-{date}` or the transcript ID if available.

Follow the template in `demand/pull-framework.md` (PULL Analysis Template section).

Use attribution tags:
- `[VERIFIED: transcript]` for direct quotes
- `[INFERRED: from context + statement]` for derived conclusions

### Step 5: Update Index

If `demand/pull-index.json` doesn't exist, create it.

Add entry:
```json
{
  "id": "{slug}",
  "file": "demand/pull-analyses/{slug}.md",
  "date": "YYYY-MM-DD",
  "company": "",
  "prospect": "",
  "prospect_title": "",
  "pull_score": 0,
  "classification": "demand | benefit | neither",
  "demand_strength": "very_high | high | medium | low | none",
  "primary_trigger": "",
  "buyer_types": [],
  "features_resonated": [],
  "would_close": "yes | likely | unlikely | no",
  "current_tools": [],
  "company_size": ""
}
```

### Step 6: Report

Display a summary:
```
## Analysis Complete: {Company} — {Prospect}

**PULL Score:** {X}/20 — {DEMAND | BENEFIT | NEITHER}
**Primary trigger:** {trigger}
**Would close:** {assessment}

**Key insight:** {most interesting finding}

Analysis saved to: demand/pull-analyses/{slug}.md
```

If this is the 5th+ analysis, suggest: "You have enough analyses for pattern synthesis. Want me to identify recurring demand triggers?"

## Batch Mode

When user says "batch" or "process all transcripts in X":

1. List available transcript files
2. Process in groups of 3 (parallel agents, write-to-file pattern)
3. Each agent writes analysis and returns status only
4. After batch completes, update pull-index.json with all new entries
5. Report summary: how many processed, score distribution, common triggers

## Quality Checks

- If the call isn't a sales call (customer success, internal meeting), note this and ask if they still want analysis
- If hard constraints from `context.md` are violated (e.g., prospect doesn't use required tech), flag as disqualified
- If prospect never articulates a project (P=0), classify as NEITHER regardless of other scores
