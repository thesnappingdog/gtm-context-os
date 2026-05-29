---
name: draft-sequence
description: "Draft an outbound sequence grounded in demand data. Use when messaging angles are defined and ready for copy."
argument-hint: "[segment-id or angle name]"
---

Write actual outbound message drafts with personalization variables, ready for import into sequencing tools.

## Prerequisites

- A segment must exist with messaging angles defined
- Messaging angles must have PULL evidence

If missing: suggest which prerequisite skill to run first.

## Process

### Step 1: Load Context

- Read `context.md` for product and positioning
- Read `messaging/angles.md` for the target angle
- Read `messaging/voice.md` for tone guidelines (if exists)
- Read linked PULL analyses for buyer language

### Step 2: Select Angle

If multiple angles exist for the segment:
- Display available angles with hooks
- Ask which one to use

If only one, confirm it.

### Step 3: Get Sample Accounts (Optional)

Ask: "Want to provide 3-5 sample accounts for personalization? (Paste CSV rows or describe them.) Or I can draft with generic variables."

If samples provided, use them for the personalized example.

### Step 4: Draft Sequence

Generate a 3-5 touch multichannel sequence:

**Touch 1: Cold Open** (Day 0)
- Channel: Email or LinkedIn
- Subject line with variables
- Body structure: Question → Consequence → Solution → Proof → CTA

**Touch 2: Follow-up** (Day 3-4)
- Callback to previous OR new angle on same theme
- Additional value or insight
- Softer CTA

**Touch 3: LinkedIn** (Day 4-5, if not primary channel)
- Connection request with short note (<200 chars)
- Different angle than email

**Touch 4: Value add** (Day 7-8)
- Resource, insight, or case study relevant to their scenario
- No hard sell

**Touch 5: Break-up** (Day 12-14)
- Acknowledge they're busy
- Final value point
- Easy out + door open

### Step 5: Opener Rules (Critical)

- NEVER open with "Most [persona] I talk to..." — schmooze pattern
- NEVER open with blanket assumptions about their situation
- ALWAYS open with a question about THEIR scenario
- Three opener types:
  - **Scenario question:** "Are you trying to get X right at {{company}}?"
  - **Challenge question:** "Have you figured out X, or is it still half-done?"
  - **Outcome question:** "Do your managers know what good looks like — or are they improvising?"

### Step 6: Show Personalized Example

If sample accounts were provided, show Touch 1 with all variables filled in.

### Step 7: Variables Reference

```
| Variable | Description | Source |
|----------|-------------|--------|
| {{first_name}} | Contact first name | CRM/list |
| {{company}} | Company name | CRM/list |
| {{title}} | Job title | CRM/list |
| {{signal}} | Personalization hook | Enrichment |
```

### Step 8: Bootstrap Campaigns Module (if needed)

If `campaigns/` doesn't exist, create it from the AGENTS.md blueprint.

### Step 9: Save

Write to `campaigns/{campaign-slug}/sequence-drafts.md`

Create campaign entry in `campaigns/campaigns.json` with status "draft".

### Step 10: Next Steps

"Sequence drafted for {segment} using {angle} angle.

Next steps:
- Review copy — adjust tone, add company-specific proof points
- Import into your sequencing tool
- Start with 50-100 prospects, measure reply rate
- After first batch: log performance data in the campaign folder"
