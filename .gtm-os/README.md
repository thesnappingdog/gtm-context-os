# .gtm-os/ — OS machinery

Editor-agnostic infrastructure that *operates* the system — distinct from your GTM content (`context.md`, `demand/`, `segments/`, etc.) and from `.claude/`, which is Claude-Code-specific.

| Path | What it is |
|------|------------|
| `upgrade-log.md` | Adoption ledger (created in cloned instances, not the template). Agent-to-agent provenance of which template patterns this instance adopted, adapted, or skipped — and why, recorded one decision per entry ID. Maintained by `/gtm-os-upgrade`. |

**Conventions:**
- This directory is read **on demand**, not auto-loaded into context (see `.claudeignore`).
- `sensitive-terms.txt` (the pre-push leak sweep's per-clone term list) is **gitignored by design** — committing the terms you're keeping out of the repo would itself be the leak — but it is agent-maintained state, seeded by `/setup-env`.
- The adoption ledger **is** tracked — it's durable provenance, same class as the JSON indexes. The operator never reads or edits it.
