---
paths:
  - "workflows/**"
---

# Workflows Module

What runs **unattended** — scheduled (any scheduler, launchd/cron on your own machine included) or triggered by another system — and is **not one process package's own adapter**. Since 2026-09 the code of a process lives in `cli/{process}/` and that package's own adapter lives in its `deploy/`; this module is narrower than it was.

## What lives here

- `workflows/README.md` — the **inventory** of every deployment unit of both kinds: target, trigger, **ownership line** (exposes/schedules `cli/{p}` `{verb}` | owns orchestration across X and Y), declared status, last-verified date. Rows for `cli/{process}/deploy/` adapters link there; nothing is copied
- `workflows/{name}/` — units that aren't one package's adapter: a plist/cron line over a standalone `scripts/` script (the script stays in `scripts/`, no package ceremony), a graph spanning several processes or services (n8n/Make export), a no-code flow with side effects. Each has the deployment-contract `README.md` (Infrastructure · Schedule · Inputs and output · Authorization · Status · Rollback), the export or thin wrapper, and a locked environment if it has code
- Legacy directories holding real process code: keep them; `/gtm-os-health` reports "process package by content — `cli/{name}/` is its home now" and never moves code; `/gtm-os-upgrade` treats the move as advisory

## Conventions

- **Ownership is by documented responsibility, not import count.** Only exposes/schedules one package's operation → that package's `deploy/`. Owns independent orchestration → here. Health flags ambiguity for review, never concludes a move
- **Graduation is a fork, not a move.** Don't create a unit before it's deployed — no schedule until single runs are boring
- **The write boundary.** An unattended run never runs `git commit` or `git push`; committing is a human-reviewed act in a later interactive session. **Durable output:** repo-bound output lands somewhere that survives the worker (a bucket, the store, `_output/` on a persistent machine) — a cloud function's filesystem is transient
- **The three write classes apply with the human removed.** Owned store: allowed. Spend: up to an authorized maximum fixed in the contract, which names its period; the run may compute a smaller allowance, never exceed or raise it; repeated invocations in a period share one budget. External system-of-record writes: governed by the authorization state
- **Three authorization states** in the contract: *none* (default — stop before any external system-of-record write); *standing, bounded scope* (operator signs system · operation · eligible records/fields · limits · per run or per period once they're happy with the setup; the run enforces it and stops when it would exceed it; `--plan` is the preview at sign-off and on scope change, not per run); *per-run approval* (anything outside a standing scope). The agent never signs a scope
- Cross-reference from `engine/architecture.md` when a unit implements a pipeline stage. Decommissioning removes the directory and the inventory row

---

*Source of truth: AGENTS.md, "Module: workflows". Read it for the full blueprint and the deployment-contract skeleton.*
