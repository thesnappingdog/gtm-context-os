globs: **/*.json

# JSON Index Maintenance

JSON indexes (`pull-index.json`, `segments.json`, `messaging.json`, `campaigns.json`) are your internal navigation infrastructure.

## Rules

- **You create and maintain these.** The operator never edits or reads them.
- **Update automatically** — when you create/modify a markdown file in a module directory, update that module's JSON index in the same operation.
- **Keep schemas minimal** — IDs, names, statuses, and links. Don't store data requiring operator input.
- **Markdown is for humans** — rationale, quotes, nuance live in `.md` files. JSON is for you to query and link.
- **Reconcile on session start** — fix drift silently, don't ask.

---

*Source of truth: AGENTS.md, "JSON Indexes — AI-Maintained Infrastructure" section.*
