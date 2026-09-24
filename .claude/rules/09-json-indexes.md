---
paths:
  - "**/*.json"
---

# JSON Index Maintenance

JSON indexes (`pull-index.json`, `segments.json`, `messaging.json`, `campaigns.json`) are your internal navigation infrastructure.

## Rules

- **You create and maintain these.** The operator never edits or reads them.
- **Update automatically** — when creating/modifying an indexed entity, update its row in the same operation. Follow the module's actual schema: README/reference documents, synthesis and unscored notes are not entities; multiple angles share `angles.md`. Do not invent a `file` field for schemas that use IDs or sections.
- **Keep schemas minimal** — IDs, names, statuses, and links. Don't store data requiring operator input.
- **Markdown is for humans** — rationale, quotes, nuance live in `.md` files. JSON is for you to query and link.
- **Reconcile on session start** — fix drift silently, don't ask, if this session holds write authority over the index; a read-only session reports drift instead of fixing it.

---

*Source of truth: AGENTS.md, "JSON Indexes — AI-Maintained Infrastructure" section.*
