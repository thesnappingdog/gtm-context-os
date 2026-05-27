globs: campaigns/**

# Campaigns Module

Campaign records for any coordinated GTM effort — outbound sequences, content pushes, paid programs, events.

## Campaign JSON Schema (`campaigns/campaigns.json`)

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

## Conventions

- Every campaign links to a segment and messaging angle
- "Campaign" is defined by the operator — don't force outbound-only assumptions
- When killed, move folder to `archive/` with a post-mortem
- If operator pastes metrics, store in the campaign's folder or as an optional `metrics` object in JSON

---

*Source of truth: AGENTS.md, "Module: campaigns" section. Read it for the full blueprint.*
