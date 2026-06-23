globs: workflows/**

# Workflows Module

Production-grade automated workflows that have graduated from `scripts/`. These run on schedules, connect to persistent data stores, or are deployed to cloud environments.

## Graduation Test

Who runs it? If you still type the command, it's a script (register recurring ones in `ops`). If it runs unattended — scheduled, deployed, or triggered by another system — it's a workflow. *Not* the test: "would something break if it stopped?" — that's true of load-bearing hand-run scripts too. The discriminator is unattended execution, not importance. Graduation can be a fork rather than a move: a script and its deployed counterpart can coexist, sharing a callable core.

## Key Structure

- Each workflow gets its own directory: `workflows/{workflow-name}/`
- Per-workflow: `README.md`, entrypoint, `pyproject.toml` (or language equivalent), `.env.example`
- Optional: `Dockerfile`, `migrations/`, `config/`

## Conventions

- Use `pyproject.toml` with locked dependencies, not inline `# /// script` metadata
- Each workflow's README documents: what it does, infrastructure deps, how to deploy, how to monitor, how to roll back — follow the per-workflow README skeleton in AGENTS.md "Module: workflows". Schedule and Rollback are mandatory but may be honestly stubbed before deploy and filled on the deploy commit; a workflow can exist pre-deployment (README modeling the target shape while the producing code still lives in `scripts/`)
- Infrastructure docs (schemas, migrations) live in the workflow directory *for a store the workflow owns*; a store shared across scripts keeps its migrations at repo root and its reference in `engine/integrations/`. API reference docs stay in `engine/integrations/`
- Test changes before deploying and document rollback steps
- Cross-reference from `engine/architecture.md` when the workflow implements a pipeline stage
- When decommissioned, remove the directory; if reverting to manual use, move logic back to `scripts/`

---

*Source of truth: AGENTS.md, "Module: workflows" section. Read it for the full blueprint and conventions.*
