# GTM Context OS — Codex entrypoint

`AGENTS.md` is the complete, authoritative handbook for this single-company GTM operating system. It deliberately contains all conventions, module blueprints, and examples. This file is only a loading guide: Codex loads it instead of the large handbook at session start. Read the required handbook sections from disk; do not rely on an automatically injected or truncated copy.

## Start every session

1. Read `AGENTS.md` from the beginning through **Operational Conventions**, stopping before **Module Blueprints**. Also read its **Startup Check** section. These are the shared operating rules, including evidence requirements, attribution, write authority, index maintenance, file routing, and status logging.
2. Check for applicable instance-specific role/contributor rules and closer `AGENTS.override.md` / `AGENTS.md` files before accessing restricted content or making any write. Codex does not automatically load `.claude/rules/`: inspect any instance-specific rules there explicitly, especially role restrictions. Follow **Roles and write authority** in the handbook; do not assume that silent reconciliation grants write authority.
3. Read `context.md` and `status.md` within that authority, then perform the Startup Check. Respect the handbook's restrictions on reading scratch outputs.

Read sections by their headings, not fixed line numbers. If a tool truncates a required read, continue until that section is complete. The handbook stays one file; there is no need to load every module blueprint for every task.

## Load the task's guidance before acting

| Task | Required handbook section / reference |
|------|---------------------------------------|
| Analyze calls or ingest demand evidence | `demand/pull-framework.md`, plus handbook **Attribution**, **JSON Indexes — AI-Maintained Infrastructure**, and **Synthesis Trigger** |
| Create or change a module | Its **Module: …** blueprint; read the module's existing README/overview first if present |
| Write scripts or connect tools | **Module: scripts** and **Module: engine** |
| Build or change a process package | **Module: cli (the process tier)** and **Module: engine**; include the package's own instructions |
| Schedule or deploy anything | **Module: workflows**; for a package adapter, also the cli blueprint's deployment guidance |
| Plan initiatives or explore future work | **Module: roadmap (the planning tier)** |
| Change repo structure or output paths | **Check Before You Create**, **Document Architecture**, and **Pipeline Artifacts and Output**, plus the affected module blueprint |
| Evolve this template or upgrade an instance | **Cross-Editor Compatibility**, `CHANGELOG.md`, and the relevant skill; keep this loader pointing at the handbook rather than duplicating its policy |

## Shared skills

Repo skills are discovered through `.agents/skills`, a relative symlink to the canonical `.claude/skills/` directory. Invoke with `$skill-name` or natural language. Read the skill's `SKILL.md` before using it; edit the canonical source, never create a second copy for Codex. If discovery fails, check the link and open the canonical skill directly; report the discovery problem.

Skills requiring only files, shell, or web access can run in either client when those capabilities are available. `bootstrap` can use concurrent fetches instead of subagents; `run-eval` is a single-session check. `release-check` and `run-probes` require isolated workers and judges: follow their runtime requirements and report an unavailable harness honestly rather than treating a prose walkthrough as an execution pass. Do not assume Claude-specific argument substitution, tools, hooks, or MCP configuration are supplied by Codex.
