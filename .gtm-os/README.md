# .gtm-os/ — OS machinery

Editor-agnostic infrastructure that *operates* the system — distinct from your GTM content (`context.md`, `demand/`, `segments/`, etc.) and from `.claude/`, which is Claude-Code-specific.

| Path | What it is |
|------|------------|
| `eval/` | Instruction-correctness harness: `tests.md` (Tier 1 — behavioral) and `scenarios/` with `fixtures/` (Tier 3 — real execution, output/state assertions and bounded-delivery probes). Run via `/run-eval` or `/run-probes`; see `eval/README.md` for runtime requirements. |
| `upgrade-log.md` | Adoption ledger (created in cloned instances, not the template). Agent-to-agent provenance of which template patterns this instance adopted, adapted, or skipped — and why, recorded one decision per entry ID. Maintained by `/gtm-os-upgrade`. |

**Conventions:**
- This directory is read **on demand**, not auto-loaded into context (see `.claudeignore`).
- `eval/results.md` is gitignored (local run history). `eval/tests.md`, `eval/scenarios/`, `eval/fixtures/` and `eval/README.md` are tracked.
- `sensitive-terms.txt` (the pre-push leak sweep's per-clone term list) is **gitignored by design** — committing the terms you're keeping out of the repo would itself be the leak — but it is agent-maintained state, seeded by `/setup-env`.
- The adoption ledger **is** tracked — it's durable provenance, same class as the JSON indexes. The operator never reads or edits it.
