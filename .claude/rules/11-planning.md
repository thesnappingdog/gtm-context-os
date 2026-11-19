---
paths:
  - "roadmap/**"
  - "_wip/**"
---

# Planning Tier (roadmap/ + _wip/)

Two homes, one lifecycle, split at the **commitment boundary**: `_wip/` holds explored-but-uncommitted specs/blueprints (not-a-module, `_`-prefix family, sketchy-on-purpose, README with status tags + a "what DID ship" graduation ledger); `roadmap/` holds committed initiatives QA'd for cold agent pickup.

## Conventions

- `roadmap/README.md` is the map of record: initiative table (Ready / In progress / Blocked / Done), dependency graph when ordering is non-obvious, dated state-reconciliation deltas
- Per-initiative file: objective + acceptance criteria, verified current state (real identifiers, attribution tags), ordered steps, dependencies/risks, traceability to what it closes
- **Executability review**: before delegated runs and periodically, audit each open plan — "could an agent pick this up cold?" Placeholder IDs, stale current-state, or re-litigated decisions fail; a plan that fails is a `_wip/` doc in the wrong tier
- Superseded plans correct forward (README delta or a superseding doc), never silent rewrites; before a known gap, the README names one re-entry doc
- Commitment moves are deliberate: graduate a `_wip/` doc by rewriting it to plan shape; dead explorations stay in `_wip/` with an honest status tag
- Don't bootstrap this module under 3 committed initiatives — a `## Next` block in `status.md`/todo is the right altitude below that

---

*Source of truth: AGENTS.md, "Module: roadmap (the planning tier)" section. Read it for the full blueprint and templates.*
