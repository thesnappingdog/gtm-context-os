---
paths:
  - "cli/**"
---

# CLI Module (the process tier)

One directory per named GTM process, in application form. Not `ops` (that indexes hand-run things; a process is one row there), not a workflow (hand-run first; the session is the async layer), not policy (that is `engine/{process}/`).

## Authorization

The trigger identifies a process; it does not authorize restructuring. For a request to extend a script chain, explain the trigger and propose the package with `build`/`act` and its `engine/{process}/` policy home in the response; ask for approval before creating it or changing the chain. Do not add a third script while awaiting the decision. An explicit request to build the package or approval already given authorizes that scope; proceed without asking again. This is the exception to automatic module bootstrap (AGENTS.md "Module: cli").

## The shape

- `cli/{process}/` — `README.md` (<150 lines), `AGENTS.md` (build rules), `check.py` (the ceiling), `pyproject.toml` (a package, not `# /// script`), the package, `tests/`, `records/`, and `deploy/` added on the deploy commit only
- Package: `cli.py` owns the **only** public surface — `build` (inputs → `review.csv`), `act` (approved rows → `final.csv`), and the `handoff` subcommand (`--plan` first). No `status`, no `doctor`, no per-stage commands: the run directory is the status
- `utilities/` holds the five shared things (config, pipeline, db, paid, suppression); a sixth needs two real callers. `commands/{theme}/` is themed by entity (`accounts/`, `timing/`, `people/`, `purchase/`, `handoff/`), one file per stage or producer, never invoked directly — the verbs compose it
- Born as two verbs, never as scripts plus tables

## Rules

- **Files are workflow state.** One dir per run under `_output/runs/{name}/`, one file per stage; skip if exists, delete to redo, rerun to resume. Policy snapshotted into `config-snapshot/`. The store holds paid payloads and decisions only; judgments recompute every run; the only read-back is the money anti-join. Zero SQL logic. Sync is the last synchronous stage of every verb
- **Two decision layers, never summed.** FIT (durable, refresh = replace) and TIMING (volatile, refresh = append with an observed-at). The refresh rule decides the layer. `commands/timing/` and the `timing` table are always in the blueprint, strongly recommended, not required by `check.py`
- **Binary, evidenced, deterministic first.** Verdicts are yes/no + reason + quoted evidence; no scores or tiers in output. Deterministic gates before model calls; hard exclusions are code, not prompt. Model calls: pinned model, temperature 0, parse-reject + one retry, then `failed`. Broad observe, narrow surface. A rank sorts qualified rows; it never gates
- **One producer contract:** `producer_many(keys) -> {key: {status: found|empty|failed, value, evidence[], observed_at}}`, batched, cost class declared (free / credit / quota / model). A new signal = one file in one theme + one key in the gate + one line in policy
- **Safety = the three write classes** from scripts: owned store → upsert; spend → `--max-{unit}` + sidecar; handoff → `--plan`. Let it crash with the two exceptions. Fail loud on dependencies
- **Policy is read from `engine/{process}/`, never edited from here.** Overflow goes into `qualify_{entity}` / `select_{entity}` pure functions. Yield is not a policy signal
- **Skills wrap the CLI; the CLI never wraps the agent.** No browsing, no `claude -p`, no orchestration inside the CLI. Four skills per process: `{process}-run`, `-configure` (never touches `cli/`), `-handoff`, `-help`. Agent never reads `.env`; DB reads through the CLI's connection; DB writes only via the two verbs; never delete review rows — fill `reject_reason`
- **The ceiling is mechanical.** `check.py` runs in tests and pre-commit. Limits live in one dict; raising one is allowed and visible — one commit naming the user-visible problem (a 10% band on size limits: 2,001 lines warns, 2,300 fails). A new table, command, persistent state, background process, config surface or abstraction needs a named user-visible problem and operator approval, proposed as a `check.py` delta
- **Deployment lives in `deploy/`, added on the deploy commit.** Bundle built from declared inputs (package + recorded policy version + env contract); `tests/test_deploy.py` imports every entrypoint at ceiling 0. Unattended rules from the workflows module bind: never `git commit`/`push`, durable output, the three authorization states. A unit that isn't this package's own adapter goes in `workflows/{name}/`; both kinds are listed in `workflows/README.md`

---

*Source of truth: AGENTS.md, "Module: cli (the process tier)". Read it for the full blueprint, the DDL, the generic `check.py`, and the `AGENTS.md` starter.*
