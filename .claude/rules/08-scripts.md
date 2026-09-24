---
paths:
  - "scripts/**"
---

# Scripts Module

Local tools for API integrations, data imports/exports, and manual operations. Run these from your terminal when you need them.

## Conventions

- Use Python with `uv run` — no global installs, no virtualenv needed
- Each script is standalone — runs independently, no shared state
- Read credentials from `.env`, never hardcode
- Repo state goes to the appropriate module folder (PULL analyses → demand/, metrics → campaigns/)
- Transient pipeline output (enrichment CSVs, scored lists, intermediate data) goes to `_output/` — never into module folders
- When writing script code, route output paths to `_output/` for transient data — the convention applies to scripts you write, not just your direct file operations
- `_output/` is the script default; promoting a run's output to `samples/` (committed, PII-safe) or `_retained/` (durable, private) is a deliberate act, never a script's automatic write target. See AGENTS.md "Pipeline Artifacts and Output"
- `_output/` is write-only for agents: don't browse, search, or read it back to inform your work — its contents are ephemeral and unreliable (stale, partial, or from a different run). Only read an `_output/` path the operator explicitly points you to. (Scripts you write may chain intermediate files through `_output/` within a single pipeline run — that's plumbing, not a state read.)
- Every script opens with the standard header: a docstring (purpose · talks-to · in→out + which tier · write-safety state) and a `ROOT = Path(__file__).resolve().parent.parent` anchor that all tier paths derive from, so it runs correctly from any directory. Credential idiom: env first, fall back to parsing `.env`, else exit naming the exact missing var; on Claude Code the key may already live in `.mcp.json` — read it there rather than duplicating
- **Write-safety — three classes, one control each**, never a generic dry-run/`--commit` switch: a *free write into a store the script owns* → idempotent upsert on a natural key, no flag; *spend* (credits, quota, model calls) → a per-invocation `--max-{unit}` ceiling checked before each submission, estimate printed, never a dry-run (the money leaves at submission); an *irreversible write into an external system of record* (CRM, sequencer) → `--plan` runs every read and stops before the first write, plus `--limit N` to prove it small and a snapshot before overwriting. State the class in the header. Read-only scripts need none of this. Full convention: AGENTS.md "Module: scripts"
- **Three-state results** — a script that asks the world about an entity records `found | empty | failed` per entity, never a boolean: `empty` is a confirmed miss (cache it, don't re-ask), `failed` retries next run, no row means never asked
- **External-data reliability** — the read-path sibling of write-safety: a script wrapping an external API retries 429/transient 5xx/transport errors with backoff (audit sibling scripts' retry policies side by side, they drift); a chunked/paged batch loop preserves earlier chunks' paid-for results on a later chunk's exception; a read-through cache stores tombstones for confirmed misses, not just hits; a "latest row per group" query uses a deterministic secondary tiebreak (an ID), not just a timestamp; and every spending submission wears the **paid-boundary sidecar** — receipt before money, provider run ID before polling, raw response archived before parsing, crash = poll the existing run, never resubmit. Full convention: AGENTS.md "Module: scripts"
- **Let it crash** — retries are for transport only. Unexpected exceptions propagate with a traceback; one observed error is a bug report, not a reason to add a handler. Only two places handle errors on purpose: the paid boundary and the external-dependency check (unreachable source → stop loud, before work). Expected-bad input (dead page, empty search) is a row outcome (`failed`/`empty`), never an exception that takes the batch down
- Name scripts in tool/concern families. **The process trigger:** when two scripts are run by hand in a fixed order to produce one output, that is a process — propose `cli/{process}/` under the cli module's authorization boundary; do not add a third script to the chain, and do not fold the chain into one big phase-subcommand script (no ceiling, no policy surface, no tests). `scripts/README.md` is a live-scripts table (only live scripts; retired ones drop off)
- **The `ops` dispatcher** — `scripts/ops.py` is the curated registry of recurring, hand-run operations; `ops list` is "what can this instance do." Promotion is operator-explicit: when a script looks like a robust recurring op, *suggest* adding it ("want it in `ops`?"), never auto-register. Before writing a new operational script, check `ops list` and `scripts/README.md` so you don't duplicate one that already exists. Created on first promotion, not at bootstrap. Full pattern: AGENTS.md "Module: scripts"
- Use inline `# /// script` metadata for dependencies:

```python
# /// script
# requires-python = ">=3.10"
# dependencies = ["requests", "python-dotenv"]
# ///
```

- Scripts are tools, not frameworks. Each one does one thing.
- When a script produces output that maps to a state file, update the appropriate JSON index.

## Lifecycle

Scripts go create → consolidate → retire → graduate. When two scripts overlap, fold them into one and **delete** the loser — don't keep superseded near-duplicates. Record what replaced a retired script (commit message, and the engine dev-notes if one exists). Keep `scripts/README.md` a list of *live* scripts only. If an ad-hoc need for a retired script resurfaces, prefer a thin CLI wrapper around the surviving script over reviving the dead one.

## Graduation

Two exits. (1) The script becomes part of a **process** (the trigger above) → `cli/{process}/` — about what the thing is, not how it runs. (2) A standalone script starts running **unattended** — plist, cron, a cloud function wrapping just this script → the wrapper and its deployment contract go in `workflows/{name}/`; the script stays here, still directly runnable. Still typing the command → it's a script; register recurring ones in `ops` (which also routes to process entrypoints). A datastore connection is neither test.

---

*Source of truth: AGENTS.md, "Module: scripts" section. Read it for the full blueprint and patterns.*
