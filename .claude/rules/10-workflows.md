globs: workflows/**

# Workflows Module

Production-grade automated workflows that have graduated from `scripts/`. These run on schedules, connect to persistent data stores, or are deployed to cloud environments.

## Graduation Test

If you stop running it, does something break? If yes, it's a workflow. If no, it belongs in `scripts/`.

## Key Structure

- Each workflow gets its own directory: `workflows/{workflow-name}/`
- Per-workflow: `README.md`, entrypoint, `pyproject.toml` (or language equivalent), `.env.example`
- Optional: `Dockerfile`, `migrations/`, `config/`

## Conventions

- Use `pyproject.toml` with locked dependencies, not inline `# /// script` metadata
- Each workflow's README documents: what it does, infrastructure deps, how to deploy, how to monitor, how to roll back
- Infrastructure docs (schemas, migrations) live in the workflow directory; API reference docs stay in `engine/integrations/`
- Test changes before deploying and document rollback steps
- Cross-reference from `engine/architecture.md` when the workflow implements a pipeline stage
- When decommissioned, remove the directory; if reverting to manual use, move logic back to `scripts/`

---

*Source of truth: AGENTS.md, "Module: workflows" section. Read it for the full blueprint and conventions.*
