globs: messaging/**

# Messaging Module

Outreach angles, objection handling, proof points, and voice guidelines. All grounded in demand evidence and segment definitions.

## Messaging Angle JSON Schema (`messaging/messaging.json`)

```json
{
  "id": "angle-slug",
  "segment_id": "segment-slug",
  "status": "draft | active | tested | killed",
  "pull_evidence": [],
  "campaign_ids": []
}
```

## Key Files

- `angles.md` — messaging angles with hook, through-line, proof point, CTA per segment+role
- `objections.md` — objection/response table with evidence
- `voice.md` — tone guidelines, per-sender rules

## Conventions

- Angles reference segments. Don't create angles for segments that don't exist.
- When a campaign tests an angle, update the angle's status and link the campaign.
- Connects to core via segments (which reference PULL analyses)

---

*Source of truth: AGENTS.md, "Module: messaging" section. Read it for the full blueprint and worked example.*
