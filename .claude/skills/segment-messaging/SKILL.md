---
name: segment-messaging
description: "Match a segment to messaging angles based on PULL evidence. Use after segmentation when developing outreach angles."
argument-hint: "[segment-id or segment name]"
---

Develop messaging angles for a segment, grounded in demand evidence.

## Prerequisites

- `segments/segments.json` must exist with at least one segment
- The target segment must have `pull_evidence` entries
- `context.md` must be filled (for positioning context)

If segments module doesn't exist: "No segments defined yet. Identify your first segment before developing messaging."

If segment has no PULL evidence: "This segment has no linked PULL analyses. Run `/pull-query` to find relevant evidence and link it first."

## Process

### Step 1: Load Context

- Read `context.md` for positioning and product context
- Read `segments/{segment-id}.md` for segment rationale
- Read each PULL analysis linked in `pull_evidence`
- If `messaging/` module exists, read existing angles to avoid duplication

### Step 2: Extract Buyer Language

From the linked PULL analyses, extract:
- Direct quotes about their project
- How they describe the problem (in their words, not yours)
- What triggers urgency
- What alternatives they tried and why they failed
- What features or outcomes excited them

### Step 3: Develop Angles

For each buyer role in the segment, propose 1-2 messaging angles:

```
## Angle: {Name}

**Segment:** {segment-id}
**Buyer role:** {title}
**Channel:** {email | linkedin}

**Hook:** {opening question — must be about THEIR scenario}
**Through-line:** {the core tension this addresses}
**Proof point:** {customer reference or data point}
**CTA:** {specific, low-friction ask}

**Grounded in:** {PULL analysis files where this pattern appears}
**Buyer language:** {actual quotes that inspired this angle}
```

### Step 4: Bootstrap Messaging Module (if needed)

If `messaging/` doesn't exist, create it from the blueprint in AGENTS.md.

### Step 5: Save

- Write angles to `messaging/angles.md`
- Update `messaging/messaging.json` with new angle entries
- Confirm what was created

### Step 6: Suggest Next Steps

"Messaging angles ready for {segment}. Next steps:
- Review and refine the angles
- Run `/draft-sequence` to write actual outbound sequences
- Test with a small batch (100 prospects) before scaling"

## Angle Quality Rules

- Every angle must reference at least one PULL analysis
- Hooks must be questions about the buyer's scenario, never statements about your product
- Proof points must be verifiable (real customer outcomes, not hypothetical)
- If you can't find demand evidence for an angle, say so — don't fabricate
