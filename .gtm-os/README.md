# .gtm-os/ — OS machinery

Editor-agnostic infrastructure that *operates* the system — distinct from your GTM content (`context.md`, `demand/`, `segments/`, etc.) and from `.claude/`, which is Claude-Code-specific.

| Path | What it is |
|------|------------|
| `eval/` | Instruction-correctness test harness — checks that AGENTS.md produces correct agent behavior. Run via `/run-eval` (Claude Code) or by asking any editor to run `.gtm-os/eval/tests.md`. |
| `upgrade-log.md` | Adoption ledger (created in cloned instances, not the template). Agent-to-agent provenance of which template patterns this instance adopted, adapted, or skipped — and why, recorded one decision per entry ID. Maintained by `/gtm-upgrade`. |

**Conventions:**
- This directory is read **on demand**, not auto-loaded into context (see `.claudeignore`).
- `eval/results.md` is gitignored (local run history). `eval/tests.md` and `eval/README.md` are tracked.
- The adoption ledger **is** tracked — it's durable provenance, same class as the JSON indexes. The operator never reads or edits it.
