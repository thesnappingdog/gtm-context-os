---
name: quickstart
description: "Guided first-use setup. Walk through filling context.md and ingesting the first sales call. Use when the repo is empty or context.md is unfilled."
---

Guided setup for first-time use of the GTM Context OS.

## When to Use

- The repo was just cloned and `context.md` is still template
- User says "help me get started" or "set this up"
- Startup check reveals empty context.md

## Process

### Step 1: Orient

"This is your GTM Context OS — a system that builds intelligence about your market from sales conversations and uses it to drive targeting, messaging, and outbound campaigns.

Everything starts with understanding your business and your buyers. Let's fill that in."

### Step 2: Fill context.md

Walk through each section conversationally — don't dump 20 questions at once:

**First, the basics:**
- What does your company do? (1-2 sentences)
- What stage are you at? (pre-revenue, early, growth, etc.)
- What's your product?

**Then ICP:**
- Who buys your product? (title, company type, size)
- What triggers them to look for a solution like yours?
- Are there hard constraints? (tech requirements, geography, company attributes that are non-negotiable)

**Then positioning:**
- What do you replace or compete with?
- How are you different?
- What's your value prop in one sentence?

**Then competitors:**
- Who else do prospects evaluate?
- Where do competitors fall short?

Fill in `context.md` as answers come in. Confirm the completed version with the user.

### Step 3: First Demand Evidence

"The system is built on understanding real buyer demand — not hypothetical pain points. The best source is sales call recordings.

Do you have recorded sales calls (from Gong, Fireflies, Zoom, or transcripts in any format)?"

**If yes:** "Paste a transcript or give me the file path. I'll run a PULL analysis and show you how the demand layer works."

Read `demand/pull-framework.md` and run a PULL analysis on the transcript. Save to `demand/pull-analyses/` and update `pull-index.json`.

**If no:** "That's fine — the demand layer builds over time. For now, let's capture your current hypothesis about who has demand."

Ask:
- Who do you think is most likely to buy right now?
- What situation are they in when they reach out?
- What alternatives have they tried?

Write this as `demand/hypothesis.md`:
```markdown
# Demand Hypothesis

**Date:** YYYY-MM-DD
**Status:** Untested

## Primary Scenario

**Who:** [role + company type]
**Trigger:** [what pushes them to act]
**Project:** [what they're trying to accomplish]
**Alternatives tried:** [what they've looked at]
**Why alternatives fail:** [the gap]

## How to Test

Ingest 5+ sales call transcripts to validate or refine this hypothesis.
```

### Step 4: Confirm Setup

"Your Context OS is ready. Here's what you have:

- `context.md` — Your ICP, positioning, and competitor landscape
- `demand/` — [Either first PULL analysis or hypothesis]
- `status.md` — Will track progress as you work

**Next steps:**
- Feed more sales calls to build the evidence layer (paste transcripts or use `/setup-api` to connect your call recorder)
- After 5+ analyses, patterns will emerge for segmentation
- Use `/gtm-status` anytime to see where things stand"

Update `status.md` with a setup entry.
