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

When a script is deployed to run on a schedule, deployed to a cloud environment, or becomes production code that other systems depend on, it belongs in `workflows/` — not here. If you stop running it and something breaks, it's a workflow.

---

*Source of truth: AGENTS.md, "Module: scripts" section. Read it for the full blueprint and patterns.*
