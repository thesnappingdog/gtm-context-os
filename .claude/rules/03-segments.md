globs: segments/**

# Segments Module

Account segments with targeting criteria, grounded in demand evidence.

## Segment JSON Schema (`segments/segments.json`)

```json
{
  "id": "segment-slug",
  "name": "Human-readable name",
  "status": "draft | active | paused | killed",
  "pull_evidence": ["demand/pull-analyses/filename.md"],
  "campaign_ids": []
}
```

## Per-Segment File Format (`segments/{id}.md`)

Sections: Hypothesis, Targeting Criteria (In/Out), Evidence (links to PULL analyses), Performance.

## Conventions

- Every segment needs at least one PULL analysis in `pull_evidence` before moving to `active`
- When killed, add a `## Post-Mortem` section explaining why
- Connects to core via `pull_evidence` linking to `demand/pull-analyses/`

---

*Source of truth: AGENTS.md, "Module: segments" section. Read it for the full blueprint and worked example.*
