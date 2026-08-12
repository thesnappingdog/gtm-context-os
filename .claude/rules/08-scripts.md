globs: scripts/**

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
- **Write-safety** — a script that mutates an external system of record (CRM, sequencer, datastore) defaults to a dry-run and requires `--commit` to write; support `--limit N`/`--all` for graduated rollout, upsert idempotently on a natural key, and snapshot before overwriting. Read-only scripts need none of this. Full convention: AGENTS.md "Module: scripts"
- **External-data reliability** — the read-path sibling of write-safety: a script wrapping an external API retries 429/transient 5xx/transport errors with backoff (audit sibling scripts' retry policies side by side, they drift); a chunked/paged batch loop preserves earlier chunks' paid-for results on a later chunk's exception; a read-through cache stores tombstones for confirmed misses, not just hits; and a "latest row per group" query uses a deterministic secondary tiebreak (an ID), not just a timestamp. Full convention: AGENTS.md "Module: scripts"
- Name scripts in tool/concern families; when a multi-step chain hardens, consolidate it into one pipeline script exposing phases as subcommands — the natural graduation candidate to `workflows/`. `scripts/README.md` is a live-scripts table (only live scripts; retired ones drop off)
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

When a script is deployed to run on a schedule, deployed to a cloud environment, or becomes production code that other systems depend on, it belongs in `workflows/` — not here. The test is **who runs it**: if you still type the command it's a script (register recurring ones in `ops`); if it runs unattended it's a workflow. "Something would break if it stopped" is true of load-bearing scripts too, so it doesn't discriminate. Graduation can be a fork, not a move — a hand-run script and a deployed workflow can coexist, sharing a callable core.

---

*Source of truth: AGENTS.md, "Module: scripts" section. Read it for the full blueprint and patterns.*
