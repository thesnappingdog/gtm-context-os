globs: scripts/**

# Scripts Module

Operational scripts for API integrations, data imports/exports, and automation.

## Conventions

- Use Python with `uv run` — no global installs, no virtualenv needed
- Each script is standalone — runs independently, no shared state
- Read credentials from `.env`, never hardcode
- Output goes to the appropriate module folder (metrics → campaigns/, transcripts → demand/)
- Use inline `# /// script` metadata for dependencies:

```python
# /// script
# requires-python = ">=3.10"
# dependencies = ["requests", "python-dotenv"]
# ///
```

- Scripts are tools, not frameworks. Each one does one thing.
- When a script produces output that maps to a state file, update the appropriate JSON index.

---

*Source of truth: AGENTS.md, "Module: scripts" section. Read it for the full blueprint and patterns.*
