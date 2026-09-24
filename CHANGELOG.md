# Changelog

This file is the **upgrade channel** for instances cloned from this template. It is *not* a git log. Each entry describes a **pattern or mechanic** that changed — written so that a cloned instance's agent can evaluate whether the pattern applies to its own (unique, customized) structure and **adapt it, not copy files**.

Instances are expected to diverge. We do not ship folder structures or force migrations — we ship the patterns and mechanics that make the system efficient, and each instance decides how (or whether) to express them.

## How instances use this

Operators run `/gtm-os-upgrade` — **operator-initiated, never automatic**. The skill fetches the latest template, reconciles what's new against the actual instance (both this changelog *and* the real file diff, which catches drift never written up as an entry), and applies approved changes on a review branch — pausing before anything destructive. Decisions are recorded per entry ID in the instance's **adoption ledger** (agent-to-agent infrastructure, like the JSON indexes — operators never read or edit it). See `.claude/skills/gtm-os-upgrade/SKILL.md`.

## Maintainer discipline (required)

Every `dev` → `main` merge **must** add one entry per coherent pattern changed — one per *idea*, not one per commit. A change that touched six files but expressed one pattern is one entry. Write it at merge time, when the rationale is freshest. This is part of the release ritual (see `/release-check`).

## Entry format

```
### [YYYY-MM-DD] Short pattern name

- **ID:** stable-kebab-slug   (the adoption ledger references this — never reuse or rename)
- **Category:** methodology | convention | skill | mechanic | doc-architecture
- **Severity:** high | medium | low   (how much it matters *if* you have the problem)
- **Depends on:** other entry IDs, or none

**What changed** — the pattern/mechanic, stated independently of file paths.

**Why** — the rationale; the specific failure it prevents.

**How to assess fit** — how the instance agent decides whether this applies to *its* structure. Frame as a question about the instance, not an instruction to copy.

**How to adapt (not copy)** — the pattern vs. the literal template implementation. How to express the same idea in a differently-organized instance.

**Downstream risks / migration** — data that adopting could invalidate, references that could break, paths that need rerouting. Empty only if genuinely none.

**What I can't see from here** — checks the *instance* must run that the template author cannot anticipate. Distinct from Downstream risks (author-known): these are failure-mode *prompts* that force an agent through a check it might otherwise skip — e.g. "before gitignoring a directory, confirm nothing in it is tracked state a clone would lose." Write these whenever adopting the pattern is destructive or irreversible, so a mediocre agent run is as safe as a brilliant one. The mechanism's safety must live in the entry, not in hoping the instance agent is sharp.

**Reference (template implementation)** — where to read the full pattern in the template, for an agent that wants to go deep before adapting.
```

---

## Releases

Condensed index of what shipped under each `main` tag. Newest first. Each release groups the pattern entries (detailed below) that an instance would consider. This is the "what changed" summary; the entries are the "how to adopt it."

### `2026-08-25` — methodology rigor, autonomous-agent boundaries, reliability hardening

The largest release so far, mined from two live-instance harvests (one heavily-used multiplayer instance running scheduled autonomous ingestion; one operational instance running real data pipelines) plus a measured pipeline post-mortem. Everything customer-clean.

**Methodology — the one to actually adopt is the first:**
- **`pull-rubric-behavioral-anchors`** *(high · depends on `pull-score-band-reconciliation`)* — each PULL dimension gets its own 0-5 ladder of **behavioral anchors** (observable events checkable against the transcript), replacing the single adjective scale applied identically to all four. Named anti-pattern guards on the two drift-prone dimensions: Unavoidable scores the forcing function *and its date*, never a category-level necessity; Lacking scores the buyer's current alternative, never your own product's gaps. Rubric changes follow a Calibration discipline — dated note, declared pre/post non-comparability, no silent rescoring of the back catalogue. Motivated by a measured 2/27 reproducibility rate on the old scale.
- **`derived-state-coherence`** *(medium · depends on `pull-score-band-reconciliation`)* — against the drift class where a computed value silently stops agreeing with its source: **eliminate where recomputable** (thresholds defined once and referenced, never restated; synthesis counts/rates agent-owned and recomputed from the index, never hand-patched), **watch the rest** (`/gtm-os-health` recompute lenses + mechanical referential integrity). Findings are flag-only — reconciling re-interprets artifacts, so the operator decides.
- **`point-in-time-record-discipline`** *(low · depends on `dependency-liveness-probe`)* — four rules keeping dated records honest as reality moves: footnote-forward instead of rewriting; a root `archive/` with a superseded-pointer table; a re-entry ritual for known gaps; `status.md` rotation into `archive/status-{period}.md` so the every-session file stays small.
- **`ephemeral-work-conversation-only`** *(low)* — one-off outputs built *from* repo context (call prep, research briefs, ad-hoc summaries) are conversation-only: not written to module folders, not committed, not logged. Persist only what becomes durable evidence.
- **`customers-roster-convention`** *(low)* — once an instance has closed customers, a root `customers.md` roster is a named application of the Context Foundation eviction rule. Serves disqualification, expansion evidence, and prospecting-by-adjacency. Triggered by the first closed customer, never scaffolded empty.

**Autonomous agents and multiplayer — where the single-operator assumption broke:**
- **`workflow-write-boundary`** *(medium)* — a scheduled or unattended workflow writes files and **stops at the git boundary**; it never commits or pushes. Committing stays a human-reviewed act in a later interactive session, where someone who read the diff composes the message. This is the reference design that narrows three open multiplayer problems (write safety, audit trail, conflict with human sessions).
- **`write-authority-qualifier`** *(low)* — silent-reconcile is now conditional on holding write authority; a session without it *reports* drift instead of fixing it. Also names the role-conditional override-rule pattern: a later-loading scoped rule file determines session role (marker file → VCS identity → least privilege) and overrides specific base-rule behaviors, without forking the base rules.
- **`local-scheduler-graduation`** *(low · depends on `ops-operational-cli`)* — the scripts→workflows test is *who runs it*, and **any** unattended scheduler counts: launchd or cron on a persistent local machine graduates a script exactly like a hosted runtime. Infrastructure choice is not the test.

**Reliability hardening — the read path, the environment, and the push:**
- **`external-data-reliability`** *(medium · depends on `script-conventions`)* — a four-rule contract standing beside write-safety as its read-path sibling: retry minimum (429/transient 5xx/transport, with backoff, audited across sibling scripts), partial-batch preservation (one chunk's exception must not discard earlier chunks' paid-for results), negative caching (tombstone confirmed misses), deterministic extracts (a stable secondary tiebreak, not just a timestamp).
- **`dependency-liveness-probe`** *(medium)* — resuming after a gap, or acting on another session's unverified claims about external systems, means one cheap authenticated read per dependency *before* trusting recorded state. Tokens expire, free tiers auto-pause, caches go stale. `/gtm-os-health` gains the check; `check-deps` is a natural early `ops` entry.
- **`pre-push-leak-sweep`** *(medium)* — a leak sweep on the **outgoing diff** before any push, scanning added lines for secret patterns and instance-specific sensitive terms. One script serves three entry points (Claude Code PreToolUse hook, native git hook, manual). The term list stays gitignored — committing the names you're keeping out of the repo would itself be the leak.
- **`cross-os-onboarding`** *(low)* — a root `.gitattributes` plus per-OS install commands in `/setup-env` (macOS/Windows/Linux) instead of assuming brew, with Windows `npx`-shim notes.
- **`mcp-dependency-pinning`** *(low)* — pin an MCP server's unbounded SDK dependency in the committed config before shipping it, and read MCP transport error `-32000` as "the server process died at launch" (usually a dependency break), not as auth. Diagnostic: run the launch command by hand and read stderr.

**Tooling and template machinery:**
- **`execution-probes`** *(medium)* — a third eval tier that tests instructions by **executing** them: a scripted turn goes to a fresh agent session in a seeded worktree, and assertions run against the resulting git diff. Closes the structural blind spot where the single-turn eval could only grade *stated* intent, never the side effects conventions actually live in. Ships with two scenarios (index-row consistency; the synthesis threshold must produce an *offer*, not a fabrication) and gates `/release-check`.
- **`planning-tier`** *(medium · depends on `point-in-time-record-discipline`, `ephemeral-work-conversation-only`)* — two homes, one lifecycle, split at the **commitment boundary**: `_wip/` parks explored-but-uncommitted specs; `roadmap/` holds committed initiatives QA'd for cold agent pickup. The load-bearing ritual is the executability review ("could an agent pick this up cold?"). Activation threshold: 3+ committed multi-week initiatives — below that, a `## Next` block is the right altitude.
- **`upgrade-run-hygiene`** *(low)* — three mechanics for `/gtm-os-upgrade` runs: a **REMOVED** ledger status so deleted maintainer machinery isn't re-proposed every upgrade; a checkpoint commit predating the run; a reminder to reset the remote's default branch after merge.
- **`cross-agent-skill-mirror`** *(low)* — a committed `.agents/skills` → `.claude/skills` symlink exposes the skills to Codex and any agent reading the cross-agent SKILL.md standard. `.claude/skills/` stays canonical.
- **`model-capability-tiers`** *(low)* — model selection stated as capability tiers (default / strategic / quick) with one dated mapping line, instead of model names hardcoded across prose.

Also in this release (template-internal, not adoption entries): `/release-check`'s consistency agent now verifies that convention-bearing changes on `dev` carry a CHANGELOG entry — closing the gap that let `context-foundation-eviction` ship with no entry, caught only by the upgrade file-diff backstop.

### `2026-06-12` — operational CLI surface (`ops`)

Mined from a live-instance scan: the instance had grown several recurring, hand-run terminal operations that were getting lost in a flat script folder (one was nearly rebuilt from scratch because the agent didn't see it already existed).
- **`ops-operational-cli`** *(depends on `script-conventions`)* — a thin `ops` dispatcher (`scripts/ops.py`) becomes the curated, self-listing registry of recurring hand-run operations; `ops list` answers "what can this instance do," and an agent consults it before creating a new operational script. Promotion is operator-explicit (suggest, never auto-register). Also sharpens the `scripts`↔`workflows` graduation test from "would something break?" to "who runs it — you or a schedule?", and names graduation as sometimes a *fork* (script + workflow coexisting on a shared core) rather than a move.

### `2026-06-04` — operational pre-setup + self-improvement conventions

Mined from a live-instance operational harvest plus a recursive self-improvement audit (all customer-clean). Operational pre-setup — going from "context built" to "running a real data pipeline":
- **`script-write-safety`** — a script that mutates a system of record defaults to a dry-run, requires `--commit`, rolls out gradually (`--limit`/`--all`), upserts idempotently, and snapshots before overwrite.
- **`script-conventions`** — a standard script header (docstring + `ROOT` path anchor + credential idiom) and a live-scripts README table with tool/concern families that consolidate into a graduation candidate.
- **`per-workflow-readme`** — a per-workflow README skeleton with honest-stub Schedule/Rollback and a named pre-deployment state.
- **`datastore-integration-genre`** *(depends on `output-artifact-boundary`)* — a persistent datastore as a third `integrations/` genre, migrations as tracked schema-as-code, and a "a datastore doesn't graduate you" rule.

Methodology + mechanics, from a decision pass over known gaps:
- **`claimed-attribution-tag`** — `[CLAIMED: {source}]` (the company's own unconfirmed assertion, promotable to `[VERIFIED]`) becomes a first-class canon tag, no longer only inside `/bootstrap` and `/intake`. An agent meeting it mid-session has a definition without loading a skill, and won't misread it as the terminal `[UNVERIFIABLE]`.
- **`pull-score-band-reconciliation`** — the PULL interpretation/tier bands nest strictly inside the DEMAND/BENEFIT/NEITHER classification (one score → one label); classification thresholds unchanged.
- **`attribution-presence-enforcement`** *(depends on `claimed-attribution-tag`)* — eval T7 gains a presence tripwire and `/gtm-os-health` a presence lens; the robust check is routed to the trajectory-eval tier.
- **`skill-naming-convention`** — OS-meta skills take the `gtm-os-` prefix (`/gtm-os-status`, `/gtm-os-upgrade`); GTM-operation skills stay bare.

### `2026-05-29c` — engineering artifact patterns + upgrade-path v2

Three engineering artifact conventions, mined from a live instance's pipeline-hardening work:
- **`engine-dev-notes`** — when hardening a pipeline, keep a priority-ranked findings ledger in a sibling `engine/{pipeline}-dev-notes.md`, keeping the canonical doc clean.
- **`integration-diagnosis-doc`** — a second integration-doc genre: when a tool misbehaves, write a dated diagnosis (expected vs. observed, ruled-out, decisive test, fix options), distinct from the API-reference docs.
- **`script-consolidate-retire`** — the missing middle of the script lifecycle: fold overlapping scripts into one and delete the loser, so `scripts/` doesn't rot.

Also in this release (template-internal, not adoption entries): the `/upgrade` skill was rebuilt and renamed **`/gtm-upgrade`** — it now fetches the latest template (reconciling the real file diff, not just the changelog), works on a review branch, pauses before destructive changes, and records per-entry-ID ledger decisions.

### `2026-05-29b` — pipeline artifacts, upgrade path, OS namespace

The template's first upgrade-path release. Three patterns:
- **`output-artifact-boundary`** — separate repo state from transient pipeline artifacts; transient output goes in a gitignored `_output/`, write-only for agents.
- **`transient-looking-state`** *(depends on the above)* — a file in the artifact zone can still be *state* (append-only logs, cumulative records); audit before gitignoring or you lose history on the next clone.
- **`gtm-os-namespace`** — consolidate editor-agnostic OS machinery under `.gtm-os/`; the eval harness moves from `eval/` to `.gtm-os/eval/`.

Also in this release (template-internal, not adoption entries): the `CHANGELOG.md` upgrade channel itself, the `/gtm-upgrade` skill, and the adoption-ledger convention.

---

## Entries

### [2026-09-24] Rejected exports cannot remain at the ready path

- **ID:** rejected-output-boundary
- **Category:** convention
- **Severity:** high
- **Depends on:** output-artifact-boundary

**What changed** — When validation rejects an export produced in the current run, the agent must move it off the requested ready path to an explicitly blocked sibling, or complete an authorized bounded fix and revalidate before handoff. A warning in the response alone does not secure the artifact.

**Why** — An execution probe caught a suppressed account in an export. The agent reported the blocker correctly but left the unsafe file at the delivery path, where a later reader could use it without seeing the warning.

**How to assess fit** — Can a failed output remain indistinguishable from a ready deliverable after validation stops?

**How to adapt (not copy)** — Apply the boundary to the current run’s generated scratch output within existing write authority. Preserve the rejected file under a blocked name without overwriting evidence. Preserve source data, operator policy and unrelated prior artifacts; use existing run records to explain the rejection.

**Downstream risks / migration** — This does not authorize moving arbitrary historical files, relaxing policy, adding a quarantine framework or making external writes. No historical outputs are changed merely to adopt the convention.

**What I can't see from here** — Which path downstream users treat as ready, whether an existing blocked file must be preserved, and whether the session holds write authority over the produced artifact?

**Reference (template implementation)**
`AGENTS.md` → "Pipeline Artifacts and Output"; `.claude/rules/06-engine.md`; `.claude/rules/08-scripts.md`.

### [2026-09-24] Intake honors evidence prerequisites and claim provenance

- **ID:** intake-evidence-routing
- **Category:** skill
- **Severity:** high
- **Depends on:** claimed-attribution-tag

**What changed** — Company assertions remain CLAIMED until confirmed; insufficient call notes stay outside the scored-analysis corpus. Downstream routing checks demand, segment and angle prerequisites before creating artifacts.

**Why** — Organizing a deck or playbook must not turn self-report into verified fact or unsupported personas into evidence-backed segments.

**How to assess fit** — Does ingestion bypass the evidence rules used by normal segment and campaign work?

**How to adapt (not copy)** — Preserve raw sources and track deferred destinations on the source’s intake row so later evidence can resume routing without redoing completed sections. Keep strategic claims in the foundation with provenance; index only completed eligible analyses and check synthesis after saving them.

**Downstream risks / migration** — Existing claims, scores and artifacts are not silently rewritten or deleted. Flag legacy uncertainty for operator review.

**What I can't see from here** — Which existing sources independently confirm claims, and which imported artifacts were created before the prerequisites were enforced?

**Reference (template implementation)**
`.claude/skills/intake/SKILL.md`; `AGENTS.md` → "Attribution" and "Evidence Requirements"; `demand/pull-framework.md`.

### [2026-09-24] Reconcile actual index entities rather than every Markdown file

- **ID:** entity-aware-index-reconciliation
- **Category:** convention
- **Severity:** high
- **Depends on:** write-authority-qualifier

**What changed** — Health and scoped index rules follow each module’s schema: paths where defined, IDs/sections otherwise. Reference documents and unscored notes are not entities. Ambiguous orphan rows are reported instead of deleted. The messaging overview includes its existing three content-file routes.

**Why** — A valid angle index has multiple entities in one file and no file field; a generic file-per-row check can corrupt it while claiming to repair drift.

**How to assess fit** — Does reconciliation assume all module indexes share the PULL schema?

**How to adapt (not copy)** — Read the local entity convention first. Repair only unambiguous navigation drift within write authority; preserve uncertain rows and derived classifications for review.

**Downstream risks / migration** — Do not migrate schemas or delete historical rows merely to adopt this check. Existing documented instance schemas take precedence.

**What I can't see from here** — How does each local index resolve its entities, and do any custom references depend on fields the template does not have?

**Reference (template implementation)**
`AGENTS.md` → "JSON Indexes — AI-Maintained Infrastructure"; `.claude/rules/09-json-indexes.md`; `.claude/skills/gtm-os-health/SKILL.md`.

### [2026-09-24] Process triggers propose structural migration before scaffolding

- **ID:** process-proposal-authorization
- **Category:** convention
- **Severity:** medium
- **Depends on:** process-cli-tier

**What changed** — A repeated script chain triggers a process proposal, not implicit migration permission. The reply names the package, build/act verbs and policy home before asking for approval. An explicit package request or existing approval still permits immediate scoped work.

**Why** — Automatic module bootstrap and structural approval previously gave conflicting instructions when an operator requested a third script.

**How to assess fit** — Does a small script-chain extension trigger unapproved restructuring or another chained script?

**How to adapt (not copy)** — Make the process-specific authorization boundary an explicit exception to generic bootstrap guidance, and mirror it in the client’s relevant scoped excerpts.

**Downstream risks / migration** — Existing packages and scripts remain unchanged. Do not ask again when scoped authorization already exists.

**What I can't see from here** — Is the operator asking to build a process package, or only to extend an existing script chain? Use the session’s actual authorization.

**Reference (template implementation)**
`AGENTS.md` → "Module: cli" and "Module: scripts"; `.claude/rules/01-system-identity.md`; `.claude/rules/08-scripts.md`; `.claude/rules/12-cli.md`.

### [2026-09-24] Advisory consistency and an evidence-based release adherence meter

- **ID:** release-adherence-meter
- **Category:** mechanic
- **Severity:** medium
- **Depends on:** execution-probes, bounded-delivery-probes

**What changed** — Consistency becomes advisory. A deterministic meter reports first-attempt execution adherence against an 80% target, valid coverage and separate safety checks. READY meets the target with complete coverage; REVIEW is a deferrable quality warning; BLOCKED is a safety failure or incomplete applicable safety proof. Reference checks resolve skill invocations and template placeholders contextually. The execution suite now supplies sufficient transcript evidence for scored PULL work and permits the specific handbook-required development note for the suppression fix; output and source-integrity assertions remain intact.

**Why** — One instruction inconsistency should not create a perpetual all-or-nothing gate. A useful meter must expose missing coverage and nondeterminism rather than hide them behind easier tests or successful retries.

**How to assess fit** — Does release checking conflate advisory instruction quality, test-harness defects and consequential safety violations?

**How to adapt (not copy)** — Freeze the candidate (including a hashed dirty overlay applied to every isolated worktree), suite and runtime; retain first attempts, diagnostic retries, validity evidence and independent judgments. Keep Tier 1 separate. Track each release’s score/coverage and deferred findings in its existing operational log. Use the instance’s own stable case inventory.

**Downstream risks / migration** — The assessment policy changes, not prior outcomes: historical NOT READY results remain intact. No safety failure is waived by a high percentage. Comparisons across changed suites/models require an explicit non-comparability note.

**What I can't see from here** — Are invalidity and safety-applicability claims backed by evidence? Did all scheduled cases run, and are the source records sufficient to reproduce the reported score?

**Reference (template implementation)**
`.gtm-os/eval/README.md`; `.gtm-os/eval/release_meter.py`; `.gtm-os/eval/test_release_meter.py`; `.claude/skills/release-check/SKILL.md`; `.claude/skills/run-probes/SKILL.md`.

### [2026-09-23] Execution probes for bounded delivery and engineering restraint

- **ID:** bounded-delivery-probes
- **Category:** mechanic
- **Severity:** medium
- **Depends on:** execution-probes

**What changed**
Four execution scenarios test whether an agent delivers a bounded business result without
turning every exception or stored failure into engineering work: one harmless excluded row,
stale cached qualification flags, historical failed records, and a control where one suppressed
account really does violate the current contract. Assertions require actual output and preserve
code, policy and source state where no repair is needed. Fixture helpers and seed baselines live
outside the worker worktree; scenario/assertion material is removed before the worker starts.

**Why**
Correct folder placement and a working happy path do not prove stopping judgment. A model can
deliver the task and then build machinery for an irrelevant edge case, or treat accumulated
store state as both absolute truth and an obligation to repair. Conversely, restraint must not
teach it to dismiss consequential violations merely because they affect one row.

**How to assess fit**
Does the instance test agent behavior through isolated execution? Do agents expand bounded
tasks into cleanup, backfill or recovery projects based on individual results or historical counts?

**How to adapt (not copy)**
Use a small existing local tool, synthetic observations and an explicit current contract. Require
the requested artifact, check unexpected mutations including ignored/untracked files, and judge
the explanation separately. Include a consequential-error control. Keep expected answers outside
the worker's context. These are regression tests, not new failure-rate thresholds or an application
hardening mandate; `/release-check` discovers the scenarios automatically.

**Downstream risks / migration**
No business policy or data migration. More execution scenarios increase release-check time.
Worker isolation changes remove eval material only in disposable probe worktrees, never a live instance.

**What I can't see from here**
Whether a different runtime truly isolates workers and judges, or personal instructions affect
the result. One clean smoke run does not establish causality or production readiness.

**Reference (template implementation)**
`.gtm-os/eval/scenarios/`; `.gtm-os/eval/fixtures/restraint.py`; `.gtm-os/eval/README.md`; `.claude/skills/run-probes/SKILL.md`.

### [2026-09-22] Small Codex entrypoint, full shared handbook, valid Claude rule scopes

- **ID:** cross-client-instruction-loading
- **Category:** mechanic
- **Severity:** high
- **Depends on:** cross-agent-skill-mirror

**What changed**
The complete handbook stays intact. Codex receives a short `AGENTS.override.md` that requires the common operating conventions, role rules, context/status reads and task-specific handbook sections. Claude module rules use YAML `paths` frontmatter; system identity and role restrictions stay unconditional. Both clients keep one shared skill source. Bootstrap and single-session eval are described by their capabilities; execution-probe parity is not claimed without a validated runtime.

**Why**
The handbook grew beyond Codex's default 32 KiB automatic instruction budget, cutting off most module blueprints. Meanwhile plain `globs:` text in Claude rule files did not implement the advertised conditional loading. Skill discovery and instruction loading are separate contracts.

**How to assess fit**
Does this instance use Codex with a handbook larger than its automatic instruction budget? Do Claude rules claim path scoping without valid YAML `paths` frontmatter? Are portable skills described as Claude-only?

**How to adapt (not copy)**
Keep the instance's handbook and module names. Add or adapt a small Codex entrypoint that requires shared conventions and routes to the instance's own section headings; keep business policy in the handbook. Correct scoped metadata without changing rule bodies. Establish role restrictions before any startup reconciliation, in every client. Preserve the existing canonical skill location and resolve its discovery link.

**Downstream risks / migration**
Codex loads the override instead of the root handbook automatically; an incomplete loader can omit duties or role restrictions. Never replace an existing instance override wholesale. Correcting Claude scoping removes accidental unconditional coverage, so the entrypoint must require shared conventions and the relevant blueprint before creating new module files. Existing restricted-contributor rules must remain unconditional.

**What I can't see from here**
Custom section names, nested instruction files, personal instruction budgets, and platform-specific symlink handling. Verify fresh client loading and all shared skill paths on the operator's actual platform; a file existing is not proof that the client loaded it.

**Reference (template implementation)**
`AGENTS.override.md`; `AGENTS.md` → "Works in any agent, not just Claude Code" and "Cross-Editor Compatibility"; `.claude/CLAUDE.md`; `.claude/rules/`; `SETUP.md` → "Codex Instruction and Skill Discovery"; `.claude/skills/release-check/SKILL.md`.

### [2026-09-22] Integration setup follows the active AI client

- **ID:** client-aware-integration-setup
- **Category:** skill
- **Severity:** medium
- **Depends on:** cross-agent-skill-mirror

**What changed**
Setup reuses active connections and writes the selected client's MCP configuration: Claude Code's `.mcp.json` or Codex's trusted-project `.codex/config.toml`. Named environment variables are passed without embedding secrets; `.env` for scripts is not assumed to populate the MCP client. Read-only validation happens in the selected client before reporting a connection ready. The shared native push hook is activated for either client.

**Why**
A shared skill could be visible in Codex yet write only Claude's configuration, producing a configured file without a usable connection.

**How to assess fit**
Do multiple clients operate this instance, or does setup assume `.mcp.json` works everywhere? Has a connection been called ready without an actual tool read?

**How to adapt (not copy)**
Detect the active client and intended scope, preserve existing settings, and merge only the needed server entry. Follow the server's actual transport/auth contract. Describe any remaining trust, environment, OAuth or reload step. Keep shared skill instructions in their existing canonical directory.

**Downstream risks / migration**
Do not duplicate an existing user/plugin connection into project configuration, overwrite unrelated settings, or copy secret values into tracked files. No existing connections are migrated merely by upgrading these instructions.

**What I can't see from here**
Whether the client inherits the required environment, trusts this project, or uses an existing authenticated plugin connection. Verify with a read-only call in that client; do not assume the other client's success transfers.

**Reference (template implementation)**
`.claude/skills/setup-env/SKILL.md`; `.claude/skills/setup-api/SKILL.md`; `SETUP.md` → "MCP Servers" and "Push Leak Sweep".

### [2026-09-22] The process tier — `cli/{process}/` with a mechanical ceiling

- **ID:** process-cli-tier
- **Category:** convention
- **Severity:** high
- **Depends on:** ops-operational-cli, script-conventions, write-safety-classes, engine-policy-dir, three-state-results

**What changed**
A third resting place between one-purpose scripts and unattended workflows: a **process package** — one directory per named GTM process, in application form. Two public verbs (`build`: inputs → a reviewable artifact; `act`: the approved subset → the final artifact) plus a `--plan`-first `handoff`; no status/doctor/per-stage commands (the run directory *is* the status). Files are workflow state (one dir per run, one file per stage, skip-if-exists, delete to redo, rerun to resume); the store holds paid payloads and decisions only, zero SQL logic. Verdicts are binary and evidenced, deterministic gates before model calls, ranking sorts already-qualified rows and never gates. Two decision layers per account — FIT (durable, replace) and TIMING (volatile, append) — never summed; TIMING is always in the blueprint, strongly recommended, not required. One producer contract (`found | empty | failed`, evidence, observed-at, cost class). Policy read from `engine/{process}/`, never edited from the package. Skills wrap the CLI; the CLI never wraps the agent. **The ceiling is a shipped script**, `check.py`, run in tests and pre-commit: public commands, tables, SQL logic, `except Exception`, LOC, README length, test-LOC ≤ code-LOC, banned control-plane vocabulary, and every `deploy/` entrypoint referenced by a test. Limits live in one dict; raising one is allowed and visible (one commit naming the user-visible problem; a 10% soft band on size limits so 2,001 lines warns rather than fails). **The trigger:** two scripts run by hand in a fixed order to produce one output is a process — start the package; don't add a third script, and don't fold the chain into one big phase-subcommand file. `ops` gains the ability to route to a process entrypoint as one more row. Package layout: `cli.py` owns the only public surface; `utilities/` holds five shared things (a sixth needs two callers); `commands/{entity}/` is themed by entity, one file per stage, never invoked directly.

**Why**
One instance built the same lead process three times in three weeks. Version one was ten scripts chained by hand. Version two was born as a control plane — 21 command files, a status command that was the most-typed and the one that timed out, a database that became the business logic (dozens of functions, triggers and views), additive scoring that produced a review tier full of irrelevant rows — and grew 5× in eight days while the operator wrote "keep it simple" in every session. Version three is two verbs, files as state, a policy trio the operator edits, and a `check.py` that fails the build; it is the version that shipped. A second instance's largest file is a phase-subcommand pipeline script sitting in `scripts/` because nothing in the template said when a chain becomes a package, and its `workflows/` holds three pre-deployment directories that are process packages by content. The evidence for shipping the check as code rather than prose is that the prose did nothing.

**How to assess fit**
Is there a pair (or chain) of scripts you run by hand in a fixed order before a review? Is the largest file in the repo a pipeline script with phase subcommands? Does a `workflows/` directory hold hand-run multi-stage code? Has a pipeline grown a status command, a job table, or a scoring tier? Any yes is the trigger.

**How to adapt (not copy)**
`cli/` is the name two instances converged on; an instance with an established equivalent maps it rather than renaming. The load-bearing parts are: two verbs and no control plane; files as state; the policy boundary in `engine/`; the shipped `check.py` with limits in one visible dict; the entity-themed `commands/` layout; and the trigger. The ceiling numbers are one instance's — keep them until a second package gives you a reason to move one, then move it in a commit that says why. A one-stage process (a single script that grew a policy) is still a package if it has a gate and a spend; a single script that merely got scheduled is not (see `workflows-narrowed`).

**Downstream risks / migration**
Moving a chain into a package changes every invocation path — `ops` rows, skills, READMEs, and any scheduler entry — in one commit; grep for the old script names first. Policy extracted from code into `engine/{process}/` changes nothing until the code reads it; prove the same rows qualify before and after at ceiling 0. A `workflows/` directory holding process code is *reported*, never moved by the upgrade.

**What I can't see from here**
Whether the chain you'd package has a stage that spends money without a receipt — packaging it puts the sidecar and the ceiling around it, which will surface any duplicate purchases the chain has been making silently. Check the provider's billing for the last few runs before trusting the new estimate.

**Reference (template implementation)**
`AGENTS.md` → "Module: cli (the process tier)" (blueprint, DDL, generic `check.py`, `AGENTS.md` starter) and "Module: scripts" (the trigger, the two graduation exits, `ops` routing); `.claude/rules/12-cli.md`; `.gtm-os/eval/scenarios/G3-process-trigger.md`; `/gtm-os-health` lens 5b.

---

### [2026-09-22] `workflows/` narrowed to what runs unattended and isn't one package's adapter

- **ID:** workflows-narrowed
- **Category:** convention
- **Severity:** medium
- **Depends on:** process-cli-tier, workflow-write-boundary, local-scheduler-graduation

**What changed**
The process's code lives in its package; the package's *own* deployment adapter (function entrypoint, Dockerfile, plist, an n8n export that calls this package) lives in `cli/{process}/deploy/`, added on the deploy commit and never before, with a `tests/test_deploy.py` that imports every entrypoint at ceiling 0 and a bundle built from declared inputs (package + recorded policy version + env contract). `workflows/` keeps three things: the **inventory** (`workflows/README.md` — every deployment unit of both kinds, with target, trigger, an **ownership line**, declared status, last-verified date); **units that are not one package's adapter** (a plist over a standalone script — the script stays in `scripts/`, no package ceremony; a graph spanning processes; a no-code flow with side effects); and **legacy directories**, reported and never moved. Ownership is decided by the unit's documented responsibility ("exposes/schedules `cli/x` `build`" vs. "owns orchestration across X and Y"), never by counting imports; health flags ambiguity for review. The per-unit README is a deployment contract (Infrastructure · Schedule · Inputs and output · Authorization · Status · Rollback) and is also what a package README gains on its deploy commit.

**Why**
The old blueprint split on execution mode (hand-run vs unattended) and three instances didn't use it as designed: one had three `workflows/` directories, none deployed, holding what were process packages by content; another registered its one workflow in `ops` as a hand-run operation. The 2026-09 review (two independent reviewers) converged on: the package is the unit, deployment is a property added to it, and a location-split directory forces a move at the first graduation that a fork-not-move rule was supposed to prevent. But a top-level home is still needed for deployment units that don't belong to one package, and one place to answer "what runs unattended" — hence the narrow survival rather than retirement. The reviewers' strongest objection to co-location — a wrapper breaks while local runs keep working, observed once — is met by the deploy test, not by the directory.

**How to assess fit**
Does a `workflows/{name}/` here hold the actual code of a process that is hand-run? Is there a scheduled unit whose README doesn't say what it owns? Can you answer "what runs unattended in this instance" from one file?

**How to adapt (not copy)**
Nothing moves on adoption. Add the inventory README and an ownership line to each existing unit's README; that alone captures most of the value. New deployments follow the split: one package's adapter → that package's `deploy/`; anything else → `workflows/{name}/`. An instance without `cli/` yet has only the second kind and the old structure is already correct for it.

**Downstream risks / migration**
Advisory. Moving legacy process code out of `workflows/` changes invocation paths a scheduler depends on — the upgrade reports, the operator moves in their own session, the old entry keeps working until they do. `/gtm-os-upgrade` treats this entry as report-only.

**What I can't see from here**
Whether a scheduler entry on a machine you can't see (a colleague's laptop, a hosted cron) points at a path you're about to change. Check every scheduler, not just the one on this machine, before renaming a directory.

**Reference (template implementation)**
`AGENTS.md` → "Module: workflows" (inventory, ownership, the deployment contract) and "Module: cli" → Deployment; `.claude/rules/10-workflows.md`; `/gtm-os-health` lens 5b; `/gtm-os-upgrade` advisory-only entries.

---

### [2026-09-22] Unattended runs: durable output, fixed authorized spend, three authorization states

- **ID:** unattended-authorization
- **Category:** convention
- **Severity:** medium
- **Depends on:** workflow-write-boundary, write-safety-classes

**What changed**
Three rules for any unattended run, wherever its artifact lives. (1) **Durable output.** The write boundary stays literal — never `git commit` or `git push` — and "write files and stop" now says *where*: a durable review location (a bucket, the store, `_output/` on a persistent machine), because a cloud function's filesystem is transient; a later interactive session imports, reviews and commits. (2) **The three write classes apply with the human removed.** Owned-store writes are allowed. Spend is allowed up to an **authorized maximum fixed in the deployment contract, which names its period**; the run may compute a smaller effective allowance from remaining budget or input size, may never exceed or raise the authorized one, and repeated invocations inside a period draw from one budget — never fresh authorization. (3) **Three authorization states** for external system-of-record writes, declared in the contract: *none* (the default — the run stops before any such write); *standing authorization with bounded scope* (once the operator is happy with the setup, they sign a scope: system, operation, eligible records and fields, limits, per run or per period; the run enforces it and stops when it would exceed it; `--plan` is the preview at sign-off and on every scope change, not per run); *per-run approval* (anything outside a standing scope). The agent never signs a scope; a person does, in the repo.

**Why**
The 2026-08 write boundary answered git and nothing else. Two reviewers independently found that it left three things undefined: what "write files" means on a transient filesystem; whether an unattended run may spend, and against what budget; and whether a `--plan`-gated CRM write can ever run without a human — under which an ordinary nightly CRM sync would be impossible by definition. The three states make "accepted to be automated once the operator is happy with the setup" a written scope rather than a vibe, and keep the OS's standing rule — approval never delegates to the agent — intact.

**How to assess fit**
Does any scheduled job here write into a CRM or sequencer? Under what written authorization? Does any scheduled job spend credits, and is the ceiling in a file someone signed or in a variable someone set? Where does a cloud job's output land, and would it survive the container?

**How to adapt (not copy)**
The contract sections are the pattern; instances with an existing README shape add an `## Authorization` block and a named period on the spend ceiling. A job that today runs `--plan`-gated writes unattended without a scope is not made safe by this entry — it is made *visible*; write the scope it has been operating under, and have the operator sign it or shrink it.

**Downstream risks / migration**
An unattended job that today writes to a system of record with no declared scope is, under this rule, in the *none* state — adopting the rule literally would stop it. Declare its scope first, then adopt. Budget accounting across invocations in a period needs a place to keep the running total (the store, or a file in the durable output location).

**What I can't see from here**
Whether a "standing" scope was actually signed by the person accountable for the external system, or by whoever set up the job. The rule's safety is the signature; confirm who it is.

**Reference (template implementation)**
`AGENTS.md` → "Module: workflows" (Conventions for unattended runs; the deployment contract's Authorization section) and "Module: cli" → Deployment; `.claude/rules/10-workflows.md`.

---

### [2026-09-21] Write-safety as three classes — ceiling for spend, plan for records, nothing for owned stores

- **ID:** write-safety-classes
- **Category:** convention
- **Severity:** high
- **Depends on:** script-write-safety, external-data-reliability

**What changed**
The single dry-run-by-default + `--commit` switch is replaced by three write classes, each with exactly one control. (1) A **free write into a store the script owns** (its datastore, `_output/`, a JSON index) gets no flag — just an idempotent upsert on a natural key. (2) **Spend** (enrichment credits, search quota, model calls) gets a **per-invocation ceiling** (`--max-{unit}`) enforced in-process before each submission, estimate printed, whole units trimmed in input order to fit — and *never a dry-run*, because the money leaves at submission, before any row lands, so a preview mode gates nothing. (3) An **irreversible write into an external system of record** (CRM create/update, sequence enrollment) gets **`--plan`**: run every read, print the per-row plan, stop before the first write; plus `--limit N` to prove it small and a snapshot before overwriting. The class is stated in the script header. Alongside it, the **paid-boundary sidecar** is the one recovery pattern the template recommends: receipt before money, provider run ID bound before polling, raw response archived before parsing, crash = poll the existing run and never resubmit.

**Why**
A live instance's dev-notes caught the `--commit` flag meaning three different things by day two of a lead pipeline (write to own DB / spend credits / push to CRM), and every command grew a dual dry-run/real surface to carry it. Its rebuilt pipeline banned dry-run outright: for paid providers the ceiling is the real safety, and a "dry run" of a purchase either spends or proves nothing. The one place a preview is free — a CRM write you can fully compute from reads — is the one place that keeps a preview flag, under a name that says what it does. The sidecar exists because it prevented a real 47-row duplicate purchase after a mid-run crash.

**How to assess fit**
Does any script here spend credits or quota behind a `--dry-run`/`--commit` gate? Then the dry run is either spending or lying. Do writer scripts use one flag for writes of different reversibility? Has a crashed run ever been re-run from the top and paid twice?

**How to adapt (not copy)**
The pattern is the classification, not the flag names. Existing `--commit` scripts keep working — this changes what *new* scripts do and what a retrofit targets first: any script whose "dry run" sits in front of a paid call (convert to a ceiling), then any script that mixes an owned-store write and a system-of-record write behind one flag (split the controls). Instances with a CLI convention of their own express `--max-{unit}` / `--plan` in their own vocabulary.

**Downstream risks / migration**
Operators and skills that pass `--dry-run` to a converted script will get an unknown-flag error — grep skills, `ops` rows, and READMEs for the old flags when converting. A script that previously wrote nothing without `--commit` now writes to its owned store by default; confirm the store it writes to is really its own (class 1) and not a shared system of record (class 3) before removing the gate.

**What I can't see from here**
Whether a store your scripts write "freely" is actually consumed by someone else as a system of record — a shared warehouse table other teams read is class 3, not class 1, regardless of who created it. Check who reads each table before declaring the write free.

**Reference (template implementation)**
`AGENTS.md` → "Module: scripts" (Write-safety, Three-state results, the sidecar under External-data reliability, Let it crash); `.claude/rules/08-scripts.md`; `.claude/skills/setup-api/SKILL.md` Step 4.

---

### [2026-09-21] Three-state results: found / empty / failed

- **ID:** three-state-results
- **Category:** convention
- **Severity:** medium
- **Depends on:** external-data-reliability

**What changed**
A script that asks the world a question about an entity — a probe, a lookup, a search, a classification — records one of `found | empty | failed` per entity, never a boolean and never a missing row. `empty` is a confirmed miss: cache it and don't re-ask. `failed` is a transient error: retry next run. No row means never asked. And expected-bad input (a dead homepage, an empty search result, an unparseable page) is a *row outcome* — `failed` or `empty` on that row — never an exception that takes the batch down.

**Why**
Seen three times across two instances: an `enriched: true/false` column that collapsed "we looked and there was nothing" into "we never looked," so every miss was re-paid on every run; and a single connection timeout that crashed a 25-domain batch because the dead site raised instead of landing as a row. The negative-cache tombstone rule already implied the first half; this names the vocabulary so it's the same in every column, log line, and review CSV.

**How to assess fit**
Do any enrichment or probe tables use a boolean for "did we find it"? Does a batch loop let one bad input raise past the row?

**How to adapt (not copy)**
The three names are the pattern — use them as the status column's exact values so a query can tell the states apart. Existing booleans migrate by mapping `true → found` and `false → ` *whichever of empty/failed the code can actually distinguish* — if it can't, that's the bug this fixes.

**Downstream risks / migration**
Queries and downstream filters on the old boolean need updating in the same change. A `false` that was really "never asked" becomes re-askable (and re-payable) once it's `failed` — decide per table whether the old falses are `empty` (keep) or `failed` (retry) before migrating.

**What I can't see from here**
Whether anything downstream (a scoring model, a segment filter) treats the old boolean's `false` as a negative signal — it may have been silently scoring "never enriched" as "not a fit."

**Reference (template implementation)**
`AGENTS.md` → "Module: scripts" (Three-state results; Let it crash); `.claude/rules/08-scripts.md`; `engine/integrations/datastore.md` → Schema conventions.

---

### [2026-09-21] `engine/{process}/` — operator-owned policy, with a change protocol

- **ID:** engine-policy-dir
- **Category:** convention
- **Severity:** medium
- **Depends on:** engine-dev-notes, write-safety-classes

**What changed**
Once a pipeline makes decisions, its policy lives in `engine/{process}/` as small operator-editable files: a gate (hard exclusions + qualifying evidence any-of + supporting evidence), a selection policy (buckets/archetypes, patterns, caps, never-select), an optional rank profile (sort weights over already-qualified rows — a sort key, never summed with the gate), and the classification prompt (verbatim quotes required, exact output JSON). Each carries a provenance `_comment`. Rules: **code produces the signal, policy decides whether it qualifies** (never edit policy to make code convenient; never hard-code a threshold the policy owns); **observations are durable, policy is current** (an excluded class stays recorded and requalifies on a policy change without re-crawl or re-purchase); the **change protocol** is the operator's whole interface — smallest edit, policy surface only, zero-cost proof (delete the stage output downstream of the knob, rerun at ceiling 0, report which rows moved), one commit naming the knob, stop, `git revert` to roll back; **not a rules language** — conditionals overflow into two pure functions in the pipeline, not a richer schema; and **yield is not a policy signal** — a thin run is cohort supply, never a reason to loosen a gate. The "Two Modes of Operation" section gains the boundary this makes physical: policy edits are operator work, structure needs a named problem.

**Why**
Three instances put decision policy in `engine/` as JSON without coordination (a qualification file, target-roles, scoring profiles, a v2 policy trio) because that's where the pipeline docs were — and the operator's own summary was "editing anything via JSON templates is great." One instance's parked "operator vs. engineer mode" question was resolved not by a mode switch but by *directory*: its configure skill never touches the code tree, and its agent rules say never edit policy for code's convenience. The protocol (smallest edit + zero-cost proof + one commit) is what let a non-engineer operator tune a live pipeline safely. The yield rule is one sentence because nearly every run record in that instance ended with "this is cohort supply, not a scoring tweak."

**How to assess fit**
Does a pipeline here hard-code a threshold, exclusion list, or bucket definition an operator has asked to change? Are policy values already in a JSON file at the engine root that the operator edits by hand? Has an agent ever proposed loosening a gate because a run came back thin?

**How to adapt (not copy)**
The four file kinds are a menu, not a mandate — a pipeline with only a gate has only `gate-policy.json`. An instance whose policy already lives elsewhere (a scoring-profiles file at the engine root) moves it into the per-process subdirectory only if it has more than one process; otherwise a pointer is enough. The load-bearing parts are the signal/policy split, the provenance comment, and the change protocol.

**Downstream risks / migration**
Moving a policy file breaks the path in every script that loads it — grep before moving. Extracting a hard-coded threshold into policy changes nothing until the code reads the file; land both in one commit with a zero-cost proof that the same rows qualify before and after.

**What I can't see from here**
Whether an existing policy file is *actually* operator-edited or has quietly become code's config — if only the agent ever edits it, it isn't policy yet and the protocol has no operator to serve.

**Reference (template implementation)**
`AGENTS.md` → "Module: engine" (`engine/{process}/` bullet) and "Two Modes of Operation"; `.claude/rules/06-engine.md`.

---

### [2026-09-21] Run records — the third `engine/` doc genre

- **ID:** records-genre
- **Category:** doc-architecture
- **Severity:** low
- **Depends on:** engine-dev-notes, output-artifact-boundary

**What changed**
Beside dev-notes (why the code is shaped the way it is) and integration diagnoses (why a tool misbehaves), a **run record** is the per-run operational memory: `engine/records/{date}-{pipeline}-{run-id}.md` with a fixed skeleton — identities (run/batch IDs, input and output SHA-256, the reproduction command), spend vs. ceiling, what broke, fixed live vs. deferred, the stop boundary ("no contact data was purchased and nothing was distributed"), and measurements labelled known / derived / unknown. A record is a doc *about* a run; the run's artifacts stay in `_output/`. Written for any run that spent money, broke, or changed a decision. Alongside it, the datastore genre gains one rule: **workflow state is files** (one directory per run, one file per stage, skip-if-exists, delete to redo, rerun to resume); the store holds paid payloads and decisions only, with zero SQL logic.

**Why**
One instance wrote 22 such records over three weeks of a lead pipeline; they are what made its "keep patching or reboot" decision *measurable* — spend per qualified row, failure classes by frequency, what was fixed live vs. deferred — instead of a memory. The same instance had earlier let its database become the business logic (dozens of functions, triggers and views) and found that files-as-state plus a store for money-only rows was the design that survived.

**How to assess fit**
Has a pipeline run ever gone wrong in a way nobody could reconstruct a week later? Does a "how much did last month's runs cost per qualified account" question take an afternoon? Is there SQL logic in the store that a code reader can't see?

**How to adapt (not copy)**
Name and location are free; the skeleton's fields are the pattern, and the stop boundary line is the one to never drop — it is what a later reader needs to know nothing irreversible happened. Instances with an existing run-log location (a `.gtm-os/` run log, a records dir beside the pipeline code) keep it and adopt the skeleton.

**Downstream risks / migration**
None structural. A records directory in `engine/` must not become an artifact dump — the "doc about a run, not an artifact of it" line is the guard.

**What I can't see from here**
Whether run records here would carry PII (a named contact in a "what broke" line). If so, the record goes in `_retained/` with a manifest line, and only a redacted one in `engine/records/`.

**Reference (template implementation)**
`AGENTS.md` → "Module: engine" (Run records bullet); `.claude/rules/06-engine.md`; `engine/integrations/datastore.md` → Role.

---

### [2026-08-12] The planning tier — roadmap/ and _wip/

- **ID:** planning-tier
- **Category:** doc-architecture
- **Severity:** medium
- **Depends on:** point-in-time-record-discipline, ephemeral-work-conversation-only

**What changed**
A planning tier with two homes and one lifecycle, split at the commitment boundary: `_wip/` (explored-but-uncommitted specs and blueprints — not-a-module `_`-prefix family, sketchy on purpose, README with per-doc status tags and a "what DID ship" graduation ledger) and a `roadmap/` module (committed initiatives: index README with status table + dependency graph + dated state-reconciliation deltas; per-initiative files with objective/acceptance criteria, *verified* current state, ordered steps, and traceability to what they close). The load-bearing ritual is the **executability review**: periodically, and before any delegated run, each open plan is audited against "could an agent pick this up cold?" — placeholder IDs and stale current-state fail. Activation threshold: 3+ committed multi-week initiatives; below that, a `## Next` block in the status log is the right altitude.

**Why**
Two live instances independently invented the two halves — one grew a full committed-plans module that survived a 7-week operator absence as the sole re-entry point (plans executed as scoped by cold sessions); the other grew an explorations-parking tier whose graduation ledger stopped blueprints from rotting or being re-derived. The tier between "todo scratch" and "shipped state" is a demonstrated need, and the two-home split matters: mixing sketches into the index an agent reads for its next task erodes the executability standard, and merging them hides the commitment decision the rest of the OS treats as a deliberate act.

**How to assess fit**
Does the instance carry multi-week work whose ordering lives in someone's head or a bloated todo? Are there blueprint/spec docs scattered in module folders that were never committed to? Has a session ever re-derived a plan that already existed?

**How to adapt (not copy)**
Names and locations are free (an instance may already have an equivalent under another name — map it, don't duplicate); the load-bearing parts are the commitment boundary between the two homes, the executability review, the graduation ledger in the exploration tier, and the activation threshold. The plan-doc template adapts to the instance's own attribution and traceability conventions.

**Downstream risks / migration**
Existing planning docs scattered elsewhere should be *moved or pointed to*, not duplicated — two maps of record is worse than none. An over-eager bootstrap on a small instance adds ceremony without payoff (respect the threshold).

**What I can't see from here**
Whether the instance already runs an external planner (Linear, Notion) as the real map of record — if so, adopt only `_wip/` (explorations rarely live well in ticket systems) and make the roadmap README a pointer to the external source of truth rather than a competing copy.

**Reference (template implementation)**
`AGENTS.md` → "Module: roadmap (the planning tier)"; `.claude/rules/11-planning.md`.

### [2026-08-12] Derived-state coherence

- **ID:** derived-state-coherence
- **Category:** mechanic
- **Severity:** medium
- **Depends on:** pull-score-band-reconciliation

**What changed**
Two moves against the drift class where a value computed from a source silently stops agreeing with it. **Eliminate where recomputable:** classification thresholds are defined in exactly one place (the scoring framework; other docs reference, never restate — one sanctioned, release-check-watched rule excerpt aside), and every derived number in `synthesis.md` (counts, rates, distributions) is agent-owned and recomputed from `pull-index.json` on update, never hand-patched. **Watch the rest:** `/gtm-os-health` gains a derived-state coherence check (classification recompute against the instance's *own documented* bands including judgment boundaries; synthesis-number recompute against headline *and* the doc's own tables) plus a mechanical referential-integrity sharpening of the evidence-chain check (every non-null cross-file ID resolves; `active` status requires populated links). Coherence findings are flag-only — reconciling re-interprets artifacts, so the operator decides.

**Why**
Three live drift incidents, all invisible to eyeball review: an instance ran an operative DEMAND floor differing from its documented one for weeks; another's synthesis headline disagreed with its own table three sections down (both plausibly wrong-looking to nobody); a third ran an `active` campaign with null evidence links and an angle ID that existed nowhere. Every individual number looks fine — only recomputation catches the class. The checks were acceptance-tested against a live instance and flagged exactly its two known drifts, zero false positives (after learning the lens must read the instance's own bands, not assume the template's — that lesson is encoded in the check).

**How to assess fit**
Does the instance store any value in two places where one is derived from the other — thresholds restated in prose, counts in a synthesis, cross-file IDs? (Yes, structurally, for every instance with a synthesis or campaigns.)

**How to adapt (not copy)**
Single-source whatever is recomputable in the instance's own doc set; point the health lenses at the instance's actual derived sites. The recompute must honor the instance's documented rubric verbatim — custom bands, tiebreak fields, judgment boundaries — never the template's defaults.

**Downstream risks / migration**
First run on a lived-in instance may surface real, old drift — resolve as operator decisions (which value is current?), not bulk auto-fixes. Marking synthesis numbers agent-owned changes editing habits; a hand-edit to a distribution table will now be overwritten on next regeneration.

**What I can't see from here**
Whether the instance's synthesis states derived numbers in prose forms a recompute can't match mechanically (spelled-out numbers, percentages of subsets) — inventory what the synthesis actually claims before wiring the lens, and rewrite unmatchable claims into recomputable form as part of adoption.

**Reference (template implementation)**
`demand/pull-framework.md` (threshold single-source declaration + "Derived numbers are recomputed" rule); `.claude/skills/gtm-os-health/SKILL.md` (check 2 referential-integrity sharpening + check 8).

### [2026-08-12] Execution probes — eval Tier 3

- **ID:** execution-probes
- **Category:** mechanic
- **Severity:** medium
- **Depends on:** none

**What changed**
A third eval tier that tests instructions by *executing* them: a scripted operator turn goes to a fresh agent session in a seeded, isolated worktree running the repo's real instructions, and assertions run against the resulting git diff — index rows appearing, files landing in the right tier, threshold-triggered offers firing. Scenarios are markdown files (seed script + scripted turns + objective bash assertions + optional judge assertions + forbidden conditions); a `run-probes` skill is the harness; `/release-check` runs all scenarios as a gate. Ships with two scenarios: G1 (a PULL analysis must produce a consistent index row and nothing stray) and G2 (the 5th analysis must trigger a synthesis *offer*, not a silent fabrication).

**Why**
The single-turn eval asks what the agent *would* do and grades the description — it is structurally blind to conventions that only manifest as side effects of doing the work. This blindness is documented, not theoretical: a prior release scored 8/8 on an eval that could not have failed on any of its changes, and a live instance measurably eroded a header convention (~20%) with no instrument noticing. Validity discipline is the load-bearing part: three separated contexts (scripted Operator; System-Under-Test that never sees assertions; mechanical assertions first, Judge only for subjective slivers), so the test cannot grade itself.

**How to assess fit**
Instances that customize instructions (most mature ones do) have the same blindness about their own conventions: does anything verify your custom rules produce their side effects? The template's scenarios test template conventions; the mechanism is the adoptable part.

**How to adapt (not copy)**
Keep the harness; write scenarios for the instance's own load-bearing conventions (its indexes, its routing rules, its thresholds). Assert on objective state (jq/grep on the diff), not response wording. Keep the set small — probes are slow; they gate releases/upgrades, not every session.

**Downstream risks / migration**
Probes spawn real agent sessions — they cost tokens and minutes per scenario; fixture seeds drift as schemas evolve (regenerate fixtures from the same schema the rules state). A probe PASS is a smoke signal, not a statistical guarantee.

**What I can't see from here**
Whether the instance's agent runtime supports isolated worktrees and sub-agent spawning (the harness assumes both) — if not, the fallback is running scenarios in a scratch clone and asserting manually.

**Reference (template implementation)**
`.claude/skills/run-probes/SKILL.md`; `.gtm-os/eval/scenarios/G1-pull-index-follows.md`; `.gtm-os/eval/scenarios/G2-synthesis-trigger.md`; `.claude/skills/release-check/SKILL.md` (Step 3.5 + verdict criteria).

### [2026-08-12] Upgrade-run hygiene: REMOVED ledger status, checkpoint, default-branch reset

- **ID:** upgrade-run-hygiene
- **Category:** mechanic
- **Severity:** low
- **Depends on:** none

**What changed**
Three small mechanics for `/gtm-os-upgrade` runs: (1) the adoption ledger's status vocabulary gains **REMOVED** — for template-maintainer machinery deleted from a customer instance, recorded with exactly what was deleted so future upgrade runs don't re-propose it; (2) the run now commits a checkpoint at the very start (a bare commit, if the tree isn't already clean) as a rollback point that predates the run itself; (3) the completion step gains a reminder to reset the remote's default branch after merge, if the hosting provider repointed it at the upgrade branch.

**Why**
All three came out of live-instance dogfood: a run had no way to record "we deliberately removed this, don't add it back"; a run-start checkpoint closes the gap between starting the run and creating the review branch; and a live instance's `origin/HEAD` sat on a merged upgrade branch for weeks because nothing prompted a check.

**How to assess fit**
Any instance that runs `/gtm-os-upgrade` benefits — these are process mechanics, not structural changes.

**How to adapt (not copy)**
The REMOVED status is vocabulary — add it to however the instance's ledger already records decisions. The checkpoint and default-branch reset are procedure, not file shape.

**Downstream risks / migration**
None — REMOVED entries must name exactly what was removed, or future runs can't honor "do not re-propose."

**What I can't see from here**
Whether the instance's hosting provider even has a default-branch concept — bare remotes don't, so skip that step if not applicable.

**Reference (template implementation)**
`.claude/skills/gtm-os-upgrade/SKILL.md` (Step 1, Step 7, Step 8).

### [2026-08-12] Graduation test: any unattended scheduler counts, infra is not the test

- **ID:** local-scheduler-graduation
- **Category:** convention
- **Severity:** low
- **Depends on:** ops-operational-cli

**What changed**
The scripts→workflows graduation test — "who runs it, you or a schedule" — is clarified: *any* unattended scheduler qualifies, not just a hosted/cloud one. launchd or cron on a persistent local machine counts exactly like a hosted runtime or a different platform's scheduler entirely. Infrastructure choice is not the test.

**Why**
A live instance ships launchd `.plist` + `run.sh` workflow pairs and even an Apps Script runtime; all correctly belong in `workflows/` even though none of them are "cloud" in the deployed-SaaS sense the graduation wording could be read to imply.

**How to assess fit**
Does the instance run cron/launchd jobs that are still filed under `scripts/`?

**How to adapt (not copy)**
Reclassify by the who-runs-it test alone; the workflow README skeleton applies regardless of runtime.

**Downstream risks / migration**
None.

**What I can't see from here**
Whether a "scheduled" job is actually still hand-triggered in practice — check the schedule is real before graduating it.

**Reference (template implementation)**
`AGENTS.md`, "Module: workflows" (the graduation test) and "Module: scripts" (the Graduation paragraph); `.claude/rules/10-workflows.md` (Graduation Test); `.claude/rules/08-scripts.md` (Graduation). The test is restated on **both sides** of the scripts↔workflows boundary — an instance adopting this must sweep all four, not just the workflows-side pair.

### [2026-08-12] customers.md: the won-accounts roster as a named eviction pattern

- **ID:** customers-roster-convention
- **Category:** doc-architecture
- **Severity:** low
- **Depends on:** none

**What changed**
Once an instance has closed customers, a root-level `customers.md` (won accounts: name + one-line note/evidence pointer) becomes a named pattern — an application of the existing Context Foundation eviction rule: `context.md` keeps the count and notable clusters plus a pointer, the roster itself lives in `customers.md`. It serves three reads: disqualification (don't re-prospect won logos), expansion evidence (won-deal analyses as proof), and prospecting-by-adjacency (seed list for finding similar accounts). Trigger is the first closed customer — it is not scaffolded empty at bootstrap.

**Why**
Won accounts are exactly the kind of operational data the Context Foundation eviction rule already targets (fast-changing, needed only in specific tasks), but without a named destination an agent has no default place to put them — they either bloat `context.md` or scatter across module folders. Naming the file gives the eviction a fixed target and the three reads a home.

**How to assess fit**
Does the instance have closed customers listed inside `context.md` (an eviction candidate) or scattered across other files?

**How to adapt (not copy)**
Location and shape are free — the load-bearing part is one small roster file with evidence pointers, plus a `context.md` pointer to it. This is an optional-file pattern, not a new always-present Core File.

**Downstream risks / migration**
None real.

**What I can't see from here**
Whether the CRM is the natural source of truth instead — if the roster would just mirror the CRM, keep only the pointer + clusters in `context.md` and skip the file.

**Reference (template implementation)**
`AGENTS.md`, "Context Foundation: keep it strategic, evict the operational" (under "Operational Conventions").

### [2026-08-12] Ephemeral work is conversation-only

- **ID:** ephemeral-work-conversation-only
- **Category:** convention
- **Severity:** low
- **Depends on:** none

**What changed**
One-off outputs built *from* the repo's context for a transient purpose — call prep, prospect research briefs, ad-hoc summaries — are now named as conversation-only: don't write them into module folders, don't commit them, don't log them to `status.md`. If a working file is needed, use scratch space. Persist only what becomes durable evidence — e.g. a PULL analysis once the call happened and produced a transcript.

**Why**
The system has many "persist X to Y" rules and none naming what *not* to persist; agents default to writing files, silently inflating repo surface with artifacts nobody re-reads. A live instance caught itself committing a call-prep doc and wrote this rule the same hour; it held.

**How to assess fit**
Does the repo hold one-off prep/research files no one re-read?

**How to adapt (not copy)**
Adopt the rule; optionally sweep existing one-off artifacts to archive or delete.

**Downstream risks / migration**
An over-eager agent might refuse to persist something that IS durable evidence — the test is "does it carry evidential weight beyond the moment."

**What I can't see from here**
Whether operators deliberately keep call-prep files as a workflow (some do) — ask before sweeping.

**Reference (template implementation)**
`AGENTS.md`, "Ephemeral Work Stays in Conversation" (under "Operational Conventions"); `.claude/rules/01-system-identity.md` (Ephemeral Work).

### [2026-08-12] Write authority: qualify silent-reconcile + name the role-override pattern

- **ID:** write-authority-qualifier
- **Category:** mechanic
- **Severity:** low
- **Depends on:** none

**What changed**
Silent-reconcile (and silent-fix behavior generally) is now qualified by write authority: a session fixes drift silently only if it holds write authority over the file in question; a session without write authority reports the drift instead of fixing it. Separately, the role-conditional override-rule pattern is named as the sanctioned way to add roles to an instance without forking base rules: a later-loading, scoped rule file (e.g. `.claude/rules/NN-contributor-mode.md`, `globs: *`) determines the session's role early — a gitignored marker file wins, falling back to VCS identity, unknown identity defaulting to least privilege — and overrides specific base-rule behaviors for the restricted role, short-circuiting immediately for the privileged role.

**Why**
Base rules were written for a single operator and silently assume reader = writer. The first multi-user instance had to discover and resolve the contradiction itself: its contributor sessions are read-only on shared context and indexes, but the base "reconcile silently" rule would have had them silently fix files they're forbidden to touch. Its contributor mode instead suspends index reconciliation and reports drift. Naming the pattern means the next multi-user instance doesn't have to rediscover it — and template upgrades to base rules won't collide with instance role carve-outs, because the carve-outs live in a separate file, not patched into the base rule.

**How to assess fit**
Single-operator instances: adopt the qualifier — it's inert until a second role exists, so it costs nothing. Multi-user instances: does any base rule instruct behavior a restricted role can't perform? Are role carve-outs currently patched directly into base rules (an upgrade collision risk)?

**How to adapt (not copy)**
The qualifier clause is drop-in wherever a rule says "fix silently." The override-rule file's shape adapts to however the instance actually detects roles — the load-bearing parts are: a separate file (not an edit to the base rule), an early role short-circuit, a least-privilege default for unknown identity, and base rules left untouched.

**Downstream risks / migration**
None for single-operator instances. For multi-user instances, an over-broad override rule could suppress reconciliation for the operator too if the short-circuit isn't first in the file — the privileged-role check must run before any restricted-role logic.

**What I can't see from here**
How the instance identifies humans in practice — shared machines, shared git identities, service accounts committing on someone's behalf. Verify the role-detection fallback (marker file → VCS identity → least privilege) actually distinguishes its people before relying on it.

**Reference (template implementation)**
`.claude/rules/09-json-indexes.md` (Rules); `.claude/rules/01-system-identity.md` (Startup Check); `AGENTS.md`, "JSON Indexes — AI-Maintained Infrastructure" and "Roles and write authority" (under "How This System Works").

### [2026-08-12] Workflow write boundary: scheduled jobs write files, humans commit

- **ID:** workflow-write-boundary
- **Category:** convention
- **Severity:** medium
- **Depends on:** none

**What changed**
A scheduled or unattended workflow that produces repo state (analyses, index updates, pulled data) writes files and stops at the git boundary — it never runs `git commit` or `git push`. Committing stays a human-reviewed act performed in a later interactive session: the operator (with their agent) reviews the accumulated working-tree diff and composes the commit message.

**Why**
A live instance ran both designs. Design A: a scheduled CI job ran an ingestion-and-analysis pipeline and committed and pushed straight to main, unreviewed. It failed badly and invisibly: a misconfigured API key made the analysis step silently produce nothing for about 10 days, yet the job still committed daily — a cursor file always advanced, so every commit message claimed new analyses had been produced. The result was a false audit trail, discovered only by accident. Design B, the replacement (five-plus weeks clean at time of writing): the same pipeline runs on the same schedule, but the job contains zero git commands — new files accumulate in the working tree, and a later interactive session reviews the diff and commits with an accurate, human-composed message. The core failure: a scheduled job's commit message describes what the job *intended* to do, not what actually happened; a human composing the message after reading the diff cannot make that error, because they are describing an artifact in front of them, not reciting a plan. Three concerns resolve at once: write safety (nothing becomes repo state unreviewed), audit trail (the message is written by someone who looked at the diff, so it cannot silently lie), and conflict with human sessions (new output arrives as a reviewable diff, not a fait accompli already on main). The honest tradeoff: unattended output piles up uncommitted if the operator stays away — tracked in the working tree, never lost, but not yet repo state until someone reviews it.

**How to assess fit**
Does the instance have, or plan, any scheduled or unattended job that writes repo files? Does any current automation run `git commit` or `git push`?

**How to adapt (not copy)**
Strip git operations out of scheduled jobs; let their output accumulate as ordinary working-tree files. Make reviewing and committing automation output part of session-start habits, not a separate ritual. If an instance genuinely needs unattended commits (e.g. a repo nobody opens interactively), the minimum safe version commits to a branch for PR review — never straight to main — but the file-boundary design is preferred whenever a human session exists to close the loop.

**Downstream risks / migration**
Existing automation that currently commits must be changed carefully: check that nothing downstream pulls the repo expecting the automation's commits to land on a schedule. Uncommitted accumulation also means backup discipline matters more — the working tree isn't pushed until a human commits it, so a lost or wiped machine can lose unreviewed output.

**What I can't see from here**
Whether anything consumes the instance's repo remotely on a schedule — a dashboard cloning main, another agent pulling for its own state — that silently depends on the automation's commits landing. Trace consumers of the repo before removing an automation's push step.

**Reference (template implementation)**
`AGENTS.md`, "Module: workflows" → "The write boundary"; `.claude/rules/10-workflows.md` (Conventions); `ROADMAP.md`, "Multiplayer" → "Autonomous agents."

### [2026-08-12] PULL rubric: per-dimension behavioral anchors

- **ID:** pull-rubric-behavioral-anchors
- **Category:** methodology
- **Severity:** high
- **Depends on:** pull-score-band-reconciliation

**What changed**
Each PULL dimension is scored against its own 0-5 ladder of behavioral anchors — observable events checkable against the transcript — replacing the single adjective scale ("crystal clear / strong / vague / weak / absent") that applied identically to all four dimensions. The two drift-prone dimensions carry named anti-pattern guards: Unavoidable scores the forcing function and its date, never a category-level necessity true of the whole market; Lacking scores the buyer's current alternative, never your own product's gaps. A Calibration discipline governs rubric changes: dated note, declared pre/post non-comparability, no silent rescoring of the back catalogue.

**Why**
A shared adjective scale is not reproducible: it makes the scorer invent what each number means for each dimension, per session, and different sessions (different days, different model generations) invent differently. Measured on a live instance when 27 calls were accidentally scored twice by independent runs: 2/27 identical totals, 2.5-point mean gap on a 20-point scale, and 11/27 flipped their DEMAND/BENEFIT/NEITHER classification — meaning which action bucket a prospect landed in depended on which run scored it. ~70% of the variance sat in Unavoidable (inflated by justifications true of every ICP account) and Lacking (scored against the vendor's gaps — the wrong company). The failure is invisible in normal use: no call is ever scored twice, every individual score looks plausible, and aggregates absorb the noise — it only surfaces near band boundaries, which is exactly where segments and sequences trigger.

**How to assess fit**
Does the instance's scoring rubric use adjective/clarity anchors shared across dimensions? Is the corpus scored across multiple sessions or model generations (it almost certainly is)? Are decisions triggered at band thresholds?

**How to adapt (not copy)**
Adopt the structure, not the template's specific anchors: per-dimension ladders of observable events, sharpened with the instance's own domain events (its deal triggers, its buyers' actual alternatives); anti-pattern guards on whichever dimensions the instance's own mis-scorings concentrate in; the Calibration discipline verbatim. The template's ladders are a sound domain-neutral starting point.

**Downstream risks / migration**
Adopting changes score semantics: totals scored under the old rubric are not comparable to new ones. Date the switch in a calibration note, mark the seam in synthesis so aggregates don't mix eras, and do NOT rescore existing analyses — rescoring silently rewrites the evidence base that segments and messaging already cite. If legacy precision must be stated, estimate the noise band (the measured instance used ±2 points) rather than fabricating comparability.

**What I can't see from here**
Whether downstream artifacts (segments' pull_evidence, messaging angles, active campaigns) cite specific pre-change scores or classifications that sat near a band boundary — grep for cited scores of 13-15 before adopting, and re-examine only those *if a live decision depends on one*, as a deliberate operator call, not a bulk rescore. Also whether any automation ingests scores assuming continuity — a scheduled synthesis or dashboard needs the seam date.

**Reference (template implementation)**
`demand/pull-framework.md` ("PULL Analysis: Scoring a Sales Call" — the four ladders + "Calibration discipline"); `.claude/rules/02-demand.md` (Methodology).

### [2026-08-12] Point-in-time record discipline

- **ID:** point-in-time-record-discipline
- **Category:** convention
- **Severity:** low
- **Depends on:** dependency-liveness-probe

**What changed**
Four mutually reinforcing rules for how dated/historical documents stay honest as reality moves, mined from a live instance that invoked them as settled precedent repeatedly over two months: (1) **Footnote, don't rewrite** — a point-in-time record (a dated status entry, a review, an audit, an archived research doc) is never edited to match later reality; corrections live forward, in the newer entry/doc, pointing back. (2) **Root `archive/` with a superseded-pointer table** — point-in-time reports accumulating at repo root move to a root-level `archive/` whose README states nothing there is the plan of record and maps each doc to where its content lives now; this complements, not replaces, the existing per-module archive convention (`campaigns/archive/`). (3) **Re-entry ritual for gaps** — the wrap-up before a known gap names one explicit re-entry doc; the first session after a gap live-probes dependencies (the dependency-liveness-probe convention), classifies state into stable/delivered vs. decaying, and if the old plan no longer fits, writes a new superseding doc rather than patching the stale one. (4) **`status.md` rotation** — when a period is clearly closed, its entries roll verbatim into `archive/status-{period}.md`, leaving one summary line + pointer; recent entries stay in `status.md` so the file every session reads stays small.

**Why**
Two failure modes this prevents. Silently rewritten history: when a point-in-time record gets "helpfully" edited to match later facts, nobody can reconstruct what was known when, and corrections become invisible instead of traceable. Unbounded/rotting records: the instance that evolved these rules hit `status.md` at ~1000 lines / 188KB after months of appends, and root-level reports (reviews, audits) piled up with no way for a reader to tell which were stale. The instance invoked these four rules by name repeatedly as settled precedent — the mark of a convention that carries real weight rather than ceremony.

**How to assess fit**
Does the instance have dated records that get "helpfully" edited later instead of corrected forward? Point-in-time reports (reviews, decks, audits, research docs) sitting at repo root with no marker distinguishing them from living docs? A status log big enough that reading it costs real context? Multi-week operator gaps where the next session needs to know what's still true?

**How to adapt (not copy)**
The mechanics are location-free — a per-module archive works as well as a root one if that's the instance's shape. The superseded-pointer table and the footnote-forward rule are the load-bearing parts, not the folder name `archive/`. Apply rotation to any append-only log that grows unbounded, not just `status.md`.

**Downstream risks / migration**
Rotation moves content that other docs may deep-link to — grep for links into the section of `status.md` being rolled before moving it. An over-eager agent might archive recent entries; only clearly-closed periods should roll.

**What I can't see from here**
Whether this instance has any automation (scripts, dashboards) that parses `status.md` directly — check consumers before the first rotation, since a script expecting entries at a fixed offset would break silently.

**Reference (template implementation)**
`AGENTS.md` → "Status Logging" (footnote + rotation), "Document Architecture" (root archive genre + re-entry ritual); `.claude/rules/01-system-identity.md` → "Status Logging".

### [2026-08-12] Dependency liveness probe

- **ID:** dependency-liveness-probe
- **Category:** convention
- **Severity:** medium
- **Depends on:** none

**What changed**
A session that resumes after a time gap, or that is about to act on another session's stated-but-unverified claims about external systems, live-probes each external dependency (one cheap authenticated read per API/datastore) before trusting recorded state. `/gtm-os-health` gains a dependency-liveness check that enumerates the instance's dependencies and attempts one cheap read against each, reporting dead/expired/paused ones. A `check-deps` op is suggested as a natural early `ops` entry for instances with several integrations.

**Why**
Three failure shapes from a live instance, all generic: a token expired mid-work and only surfaced as an opaque auth failure; a free-tier database auto-paused during an idle stretch and the next session's writes silently failed against it; a stale read-through cache almost caused a four-figure-credit paid re-fetch, caught only because the operator dry-ran and diffed hit/miss counts before committing. The pattern: recorded state (status.md, roadmap) has no decay model — it records what was true as-of writing. External systems decay on their own clock regardless: tokens expire, free tiers auto-pause, caches go stale.

**How to assess fit**
Does the instance depend on external systems that can die while nobody is looking — token TTLs, free tiers that pause, caches with staleness windows? Has it ever resumed after weeks idle?

**How to adapt (not copy)**
The probe list derives from the instance's own integrations (`.env` keys, `.mcp.json` servers, `engine/integrations/*.md`) — not a fixed list. Wire it as a startup habit (Startup Check bullet), a health check (`/gtm-os-health`), and optionally an `ops` entry, not as a new standalone script family.

**Downstream risks / migration**
Probes that WRITE anything are not probes — keep them strictly read-only. A probe storm against rate-limited APIs can itself trip 429s, so cap it at one call per dependency.

**What I can't see from here**
Which of the instance's dependencies have safe cheap read endpoints — pick per-integration probe calls deliberately (an auth'd whoami/metadata read), and confirm none of them count against tight quotas before wiring them in.

**Reference (template implementation)**
`AGENTS.md` → "Startup Check", "Module: scripts" (`ops` dispatcher paragraph); `.claude/rules/01-system-identity.md` → "Startup Check"; `.claude/skills/gtm-os-health/SKILL.md` (Step 2, check 7).

### [2026-08-12] MCP dependency pinning

- **ID:** mcp-dependency-pinning
- **Category:** convention
- **Severity:** low
- **Depends on:** none

**What changed**
`/setup-api` (where MCP server entries actually get authored) now carries a convention: before committing a `uvx`/`npx`-launched MCP server config, check whether it declares an unbounded dependency on a still-evolving SDK (e.g. `mcp>=1.0.0` with no ceiling) and pin it in the committed config if so (e.g. `--with "mcp<2"`). It also documents the diagnostic for MCP transport error `-32000`: opaque by design, usually means the server process died at launch (a dependency break), not auth — the way to see the real cause is to run the server's launch command by hand and read stderr. The same pin-the-SDK caution gets one line in `AGENTS.md`'s integrations section so it survives outside the skill.

**Why**
The live failure: `mcp-server-bigquery` declared `mcp>=1.0.0` with no ceiling. `mcp` 2.0 shipped and broke the server. Every fresh clone hit an opaque `-32000` until someone ran the launch command by hand and read stderr to find the real cause. The fix has to land in the *committed* config/skill, not a gitignored local file — otherwise other clones never receive it.

**How to assess fit**
Does this instance's MCP setup (inline in `/setup-api`, or a committed `.mcp.json`/`.mcp.json.example` if the instance has since added one) launch any server via `uvx`/`npx` with an unpinned fast-moving SDK dependency?

**How to adapt (not copy)**
Pin in whichever file is committed and actually reaches new clones — for this template that's the skill itself, since MCP config is scaffolded inline rather than shipped as a tracked example file. Note the pin's reason next to it. Record the `-32000`-means-run-it-by-hand diagnostic once, wherever the instance documents MCP troubleshooting.

**Downstream risks / migration**
Pins go stale — without the reason noted next to a pin, a future agent can't tell whether it's still needed or safe to lift once the SDK stabilizes.

**What I can't see from here**
Which MCP servers this instance actually runs and what their real SDK constraints are — audit the instance's live `.mcp.json` entries at adoption time; this entry can't know them.

**Reference (template implementation)**
`.claude/skills/setup-api/SKILL.md` (Step 4 pin note, Step 5 `-32000` diagnostic), `AGENTS.md` → "Module: engine" (integrations doc-genre bullet).

### [2026-08-12] Cross-OS onboarding

- **ID:** cross-os-onboarding
- **Category:** mechanic
- **Severity:** low
- **Depends on:** none

**What changed**
The repo ships a root `.gitattributes` (normalizes text to LF on checkout) and an OS-aware environment setup: `/setup-env` Step 2 lists per-OS install commands (macOS/brew, Windows/winget, Linux/apt) instead of assuming brew, plus a Windows notes line covering the `npx` shim issue.

**Why**
A real Windows collaborator's onboarding broke three separate ways: CRLF checkout turned their first commit into a whole-repo diff, the setup instructions assumed Homebrew and had no Windows path, and an MCP server launched via `npx` failed to start — Windows resolves `npx` to a `.cmd` shim that process-spawn can't invoke directly, so the launch silently died.

**How to assess fit**
Could anyone ever clone this instance onto a non-macOS machine? Does the instance already have a `.gitattributes`?

**How to adapt (not copy)**
Add `.gitattributes` before the first cross-OS collaborator joins. If the repo already has CRLF content, run a one-time renormalization (`git add --renormalize .`) as its own dedicated commit, separate from other changes. Wrap any `npx`-launched MCP server's command with `cmd /c` on Windows.

**Downstream risks / migration**
A renormalization commit touches every affected file at once — keep it as a standalone commit so `git blame` stays usable on surrounding history.

**What I can't see from here**
Whether the instance's existing checkouts have `core.autocrlf` set inconsistently across machines — each collaborator should re-clone or renormalize locally after adopting this, rather than assume their existing working copy is already clean.

**Reference (template implementation)**
`.gitattributes`, `.claude/skills/setup-env/SKILL.md` (Step 2).

### [2026-08-12] External-data reliability contract

- **ID:** external-data-reliability
- **Category:** convention
- **Severity:** medium
- **Depends on:** script-conventions

**What changed**
A four-rule contract for scripts that *read* from external systems, standing beside write-safety as its read-path sibling. (1) **Retry minimum** — every script wrapping an external HTTP API retries 429 and transient 5xx (500/502/503/504) plus transport errors/timeouts, with backoff (honoring a provider's retry-after over a generic one); when multiple API wrapper scripts exist, their retry policies get audited side by side rather than left to drift. (2) **Partial-batch preservation** — a loop chunking/paging through paid API calls catches per-chunk, logs which range failed, and continues, instead of letting one chunk's exception discard earlier chunks' already-paid-for results; silent truncation/over-return gets its own check, distinct from exceptions. (3) **Negative caching** — a read-through cache over an external lookup caches confirmed misses too, as a tombstone row with the same TTL/freshness semantics as a hit, so absence-of-row means "not yet fetched," never "known miss." (4) **Deterministic extracts** — an aggregate/window query picking "the latest/best" row per group uses a fully deterministic order (a stable secondary tiebreak key, not just a timestamp that can tie), verified by running the extract twice and diffing byte-for-byte.

**Why**
Each rule maps to a real cost proven in a live instance's pipeline hardening. A cache with no tombstone re-fetches and re-pays for the same known miss on every run, forever. A batch loop with no per-chunk isolation throws away results it already paid an API for the moment one chunk errors. Retry logic written ad hoc per script drifts — one script "learns" a lesson from an outage and its siblings quietly don't, so the same outage repeats on them. And a tie-broken "latest row" query with no secondary key silently rotates which row wins across runs, propagating nondeterminism into whatever it feeds (scoring, segments) without ever raising an error.

**How to assess fit**
Does this instance have scripts calling paid or quota'd external APIs? Does it have a read-through cache over any external lookup? Does it have an aggregate/window extract ("latest per account," "best score per company") whose output feeds scoring or segmentation? Any yes means the corresponding rule applies; an instance with only read-only, unpaginated, uncached pulls can skip the parts that don't fit yet.

**How to adapt (not copy)**
Apply the rules to existing wrapper scripts opportunistically, on next touch, rather than a retrofit sweep. Do the retry-policy audit once, side by side across every script that wraps an external API, so policies converge instead of drifting further apart. The tombstone rule may require a schema change — if the cache table has no way to represent "checked, found nothing" distinct from "never checked," that's a migration, not a code change (see `engine/integrations/datastore.md` → "Schema conventions" for the migrations discipline). The deterministic-extract rule is a query change only: add the tiebreak key to the `ORDER BY`.

**Downstream risks / migration**
Adding tombstones to an existing cache needs a way to distinguish legacy absence-of-row (genuinely never checked) from the new tombstone semantics (checked, confirmed miss) — a blanket "no row = fetch it" backfill run right after the migration handles this once. Adding retries can mask a real outage if backoff is unbounded — cap attempts (a max retry count or elapsed-time ceiling), don't let a hung dependency retry forever.

**What I can't see from here**
Whether an existing cache table's schema can represent a miss at all — it may need a new column or an added row shape, not just new application logic; check before assuming the tombstone rule is a pure code change. Whether any downstream consumer already treats absence-of-row as "known miss" (rather than "not yet fetched") — grep every reader of the cache table before adding tombstones, or a consumer that currently (incorrectly but harmlessly) skips missing rows may start behaving differently once tombstones exist.

**Reference (template implementation)**
`AGENTS.md` → "Module: scripts" (External-data reliability convention block, beside Write-safety); `.claude/rules/08-scripts.md`; `engine/integrations/datastore.md` → "Schema conventions" (negative-cache tombstone note).

### [2026-08-12] Pre-push leak sweep

- **ID:** pre-push-leak-sweep
- **Category:** mechanic
- **Severity:** medium
- **Depends on:** none

**What changed**
A leak sweep runs before any `git push`: it scans the outgoing commits (added lines of everything not yet on a remote) for secret-looking patterns (API keys, tokens, private-key blocks) and for instance-specific sensitive terms, and blocks the push on a hit. One script (`.githooks/pre-push`) serves three entry points: a Claude Code PreToolUse hook in the shipped `.claude/settings.json` (zero setup — guards agent-initiated pushes), an optional native git pre-push hook (`git config core.hooksPath .githooks`, guards human pushes), and manual invocation. The term list lives in a **gitignored** `.gtm-os/sensitive-terms.txt` — deliberately local, because committing the names you're keeping out of the repo would itself be the leak.

**Why**
A push publishes; a leak caught after push is already cached and indexed. Point-in-time discipline (release-check sweeps, careful review) doesn't cover ad-hoc pushes — the failure mode is an agent or operator pushing a routine change that happens to carry a customer name or a pasted key. A standing gate at the push boundary makes the sweep automatic instead of remembered.

**How to assess fit**
Does this instance push to any remote another party could ever see (public repo, org-shared repo, vendor access)? Even for fully private repos, the secret-pattern half still applies — credentials don't belong in git history regardless of visibility.

**How to adapt (not copy)**
Adopt the mechanism (sweep outgoing commits at the push boundary, block on hit), then localize the term list: customer names, internal codenames, unreleased product names. Keep the term file out of version control. If the instance's agent config differs, wire the same script into whatever pre-push interception the tooling offers; the script itself is agent-agnostic bash.

**Downstream risks / migration**
False positives block pushes — short or common words in the term list will match inside larger words' boundaries less often than you'd fear (whole-word matching), but generic terms ("acme") can still fire; keep the list specific. The Claude Code hook only takes effect in new sessions (settings are read at session start). The native git hook requires the one-time `core.hooksPath` config per clone — until run, only agent pushes are guarded.

**What I can't see from here**
Whether secrets or sensitive terms are *already* in the repo's history — this gate only checks outgoing new commits. Run the sweep's patterns over full history (`git log -p | grep -E ...`) once at adoption; anything already pushed needs rotation (secrets) or a history decision (names), not just a gate.

**Reference (template implementation)**
`.githooks/pre-push`, `.claude/settings.json` (hooks block), `AGENTS.md` ("Push Leak Sweep and Sensitive Terms" — including the agent duty to maintain the term list and to never edit it to get a push through), `.claude/skills/setup-env/SKILL.md` (Step 5 seeds the per-clone term list), `SETUP.md` ("Push Leak Sweep").

### [2026-08-12] Cross-agent skill mirror

- **ID:** cross-agent-skill-mirror
- **Category:** mechanic
- **Severity:** low
- **Depends on:** none

**What changed**
The skills in `.claude/skills/` are exposed to Codex (and any agent reading the cross-agent SKILL.md standard) via a committed relative symlink `.agents/skills` → `.claude/skills`. `AGENTS.md` gains a short "Works in any agent" note naming the layers: `AGENTS.md` = agent-agnostic brain, `.claude/` = Claude Code layer, `.agents/skills` = shared mirror. `.claude/skills/` stays canonical — skills are edited there, never through the mirror.

**Why**
Operators increasingly run the same instance from more than one coding agent (e.g. Codex for precision coding). Without the mirror, a Codex session sees `AGENTS.md` but none of the skills, so it silently rebuilds or skips workflows the instance already has. Codex discovers repo-level skills at `.agents/skills` and supports symlinked skill folders; skill frontmatter (`name` + `description`) is the same standard both agents read, so one symlink closes the gap with no sync machinery.

**How to assess fit**
Does anyone operate this instance from an agent other than Claude Code, or might they? If strictly Claude Code-only, skip — the symlink is inert but pointless.

**How to adapt (not copy)**
If the instance keeps skills in the standard location, the same one-line symlink works: `mkdir -p .agents && ln -s ../.claude/skills .agents/skills` (relative link, so clones work). If skills were customized or relocated, point the symlink at wherever the instance's skills actually live. Also note in the instance's `AGENTS.md` which skills are Claude Code-bound (anything orchestrating parallel sub-agents) vs. agent-portable.

**Downstream risks / migration**
On Windows, git symlinks require developer mode / `core.symlinks=true`; without it the checkout materializes a plain text file and Codex sees no skills — a copy or junction is the fallback. Claude Code-specific skills will also be listed in Codex; their descriptions may auto-trigger there and degrade (no sub-agent runtime). Keep such skills' descriptions honest about where they run.

**What I can't see from here**
Whether the instance's skills have accreted references to Claude Code-only tooling (Task/agent spawning, MCP servers configured only in `.mcp.json`) that would fail confusingly in another agent — skim each skill's body before advertising it cross-agent, and confirm the symlink survives a fresh clone on the operators' actual platforms.

**Reference (template implementation)**
`.agents/skills` (symlink), `AGENTS.md` ("Works in any agent, not just Claude Code").

### [2026-08-12] Model selection as capability tiers

- **ID:** model-capability-tiers
- **Category:** convention
- **Severity:** low
- **Depends on:** none

**What changed**
Model-selection guidance is stated as capability tiers (default / strategic / quick) with a single dated current-mapping line, instead of hardcoded model names scattered in prose.

**Why**
Hardcoded model names go stale every model generation; instances that cloned the old section are now silently pointing at previous-generation models. One mapping line makes rotation a one-line edit.

**How to assess fit**
Does the instance's `CLAUDE.md` (or any doc/skill/script) name specific models? More than one place?

**How to adapt (not copy)**
Restate as tiers, keep exactly one dated mapping line, route all other references to the tier names.

**Downstream risks / migration**
Scripts or workflow configs that pin model IDs (API calls) should keep pinning explicit IDs — this convention is for guidance prose, not API parameters. Don't collapse a pinned model ID in a script into a tier reference.

**What I can't see from here**
Whether the instance has model names embedded in run configs/cron jobs that prose changes won't reach — grep for model names repo-wide before declaring adoption done.

**Reference (template implementation)**
`.claude/CLAUDE.md` (Model Selection section).

---

### [2026-06-12] `ops` — a curated operational CLI surface

- **ID:** ops-operational-cli
- **Category:** convention
- **Severity:** medium
- **Depends on:** script-conventions

**What changed**
Recurring, hand-run operations (a weekly report, a sourcing run, a data refresh) get a single curated home: a thin dispatcher, `ops`, whose `OPERATIONS` table is the registry and whose `ops list` answers "what can this instance *do*." It's a router, not a framework — it shells out to standalone scripts with `uv run` (passthrough args), so every registered script stays directly runnable and keeps its own inline deps. The dispatcher is created lazily, on the first promotion, not at scripts bootstrap. Promotion is operator-explicit: an agent *suggests* adding a script when it looks like a robust recurring op, and never auto-registers. The same change sharpens the `scripts`↔`workflows` boundary — the graduation test moves from "would something break if it stopped?" (true of load-bearing scripts too) to "**who runs it** — you, or a schedule?", and graduation is named as sometimes a *fork* (a hand-run script and a deployed workflow coexisting on a shared core) rather than a move.

**Why**
Two failures. (1) A flat script folder mixes throwaway/test scripts, dormant one-shots, and the two or three operations you actually run every week — and the recurring set, the highest-value-to-not-duplicate, doesn't stand out. An agent asked to "do the weekly report" can miss that the script already exists and rebuild it. A registry the agent consults before creating kills that. (2) The old graduation test conflated *load-bearing* with *deployed* — a weekly report breaks your reporting if you skip it, so "something breaks" wrongly labels it a workflow, while the rest of the same doc said manually-run scripts stay in `scripts/`. The execution-mode test removes the contradiction.

**How to assess fit**
Do you run any operation from the terminal *on a cadence, by hand* — and does your `scripts/` folder (or its equivalent) hold more than a handful of files, mixing one-shots with things you re-run? If yes, you have the discoverability problem `ops` solves. If every script is genuinely run-once-and-discard, you don't need the registry yet.

**How to adapt (not copy)**
The pattern is "a single curated, self-listing registry of the recurring operations, consulted before creating a new one — populated only on explicit approval." Express it however your instance is organized: the literal template form is a `scripts/ops.py` with an `OPERATIONS` dict and subprocess routing, but a Makefile/justfile target list, a `console_scripts` group, or a documented command index serves the same role. Keep two properties: it stays *curated* (you opt operations in; agents don't auto-add), and it's the *first thing checked* before a new operational script is written.

**Downstream risks / migration**
- No files move and nothing is renamed; existing scripts are untouched until you choose to register one. Adopting is additive.
- If your instance wrote down the old "if it stops, something breaks → workflow" test anywhere (a local rules file, a README), update it. Under the corrected test a load-bearing *hand-run* script is still a script — so re-check anything you previously moved to `workflows/` on the old reading.

**What I can't see from here**
- Whether you already have an improvised version of this (a `Makefile`, a "common commands" section, shell aliases). If so, fold it into one surface rather than adding a second — two registries is worse than none.
- Whether any operation you'd register mutates a system of record. `ops` is a read-only router and adds no guardrails of its own; the *target* script still owns its `--commit`/dry-run safety. Confirm that before treating an `ops <name>` run as safe.

**Reference (template implementation)**
`AGENTS.md` → "Module: scripts" (the `ops` dispatcher subsection + the `ops.py` skeleton); `AGENTS.md` → "Module: workflows" (the reworked graduation test + the fork note); `.claude/rules/08-scripts.md`; `.claude/rules/10-workflows.md`.

### [2026-06-04] `[CLAIMED]` is a first-class attribution tag

- **ID:** claimed-attribution-tag
- **Category:** methodology
- **Severity:** medium
- **Depends on:** none

**What changed**
The attribution vocabulary gains a fourth, canonized tag: `[CLAIMED: {source}]` — the company's own assertion about itself (website, pitch deck, playbook): useful context, not yet independently confirmed, and **promotable to `[VERIFIED]`** once demand evidence or data confirms it. It is now defined in the canon's Attribution section alongside `[VERIFIED]` / `[INFERRED]` / `[UNVERIFIABLE]`. The key framing: `[CLAIMED]` marks *provenance* (who asserted it), the other three mark *confidence* — which is why a claim can be both made and later verified. `[CLAIMED]` is explicitly distinguished from `[UNVERIFIABLE]`: claimed is confirmable-but-unconfirmed and promotes; unverifiable is terminal and never promotes.

**Why**
The seeding skills (`/bootstrap`, `/intake`) already wrote `[CLAIMED]` into `context.md` — the guaranteed-read foundation file — and one skill defined it, but the canon (the always-loaded rules + the source-of-truth Attribution section) defined only the other three tags. An agent working mid-session from the canon, without having loaded those skills, would meet a `[CLAIMED]` tag with no definition and have to guess. The dangerous wrong guess is `[CLAIMED]` ≈ `[UNVERIFIABLE]`, which is backwards: it freezes a promotable claim as permanently unconfirmable and invites discarding useful context as junk. Canonizing the tag makes every agent behave identically and correctly the moment it meets the tag, with no skill load required.

**How to assess fit**
Does your instance seed `context.md` (or anything else) from company-authored material — a website crawl, a pitch deck, a playbook — and tag it to mark "this is the company's claim, not confirmed"? If you use `/bootstrap` or `/intake`, you already produce `[CLAIMED]` tags and this applies. If your instance only ever records `[VERIFIED]`/`[INFERRED]`/`[UNVERIFIABLE]` and never seeds from marketing material, the tag is harmless to define and simply goes unused.

**How to adapt (not copy)**
Add `[CLAIMED]` to wherever *your* instance defines its attribution vocabulary (the canon doc the agent always reads), with two load-bearing properties stated: (1) it is *provenance, not a confidence judgment*; (2) it *promotes to `[VERIFIED]`* and is *not* a synonym for `[UNVERIFIABLE]`. The exact wording and file are yours; the distinction is the pattern. If you maintain a single full definition plus skills that use the tag, keep the full definition in one place and have the skills point to it — two full definitions drift apart.

**Downstream risks / migration**
- If your instance, before this entry, had agents interpret an in-context `[CLAIMED]` tag as `[UNVERIFIABLE]` (the natural wrong guess), any decision made on that reading was treating promotable company context as terminal-unconfirmable. Re-reading those `[CLAIMED]` claims under the corrected definition may reclassify how they inform segments/messaging — none of the data changes, but its standing does.
- No tag is renamed or removed and no file is reformatted, so existing `[VERIFIED]`/`[INFERRED]`/`[UNVERIFIABLE]` tags are untouched. This is additive to the vocabulary.

**What I can't see from here**
- Your instance may have improvised a *different* marker for the same idea (`[ASSUMED]`, `[MARKETING]`, an untagged "per their site" note). If so, reconcile to one tag rather than running two vocabularies — and decide whether to rewrite the old marker or just stop minting it. A repo-wide grep for stray attribution-like brackets in `context.md` will surface these; the template author can't see what you coined.
- If you ever ran a health/lint check that flagged `[CLAIMED]` as an unknown tag, update that check to accept it now that it's canon.

**Reference (template implementation)**
`AGENTS.md` → "Attribution"; `.claude/rules/01-system-identity.md` → "Attribution"; `.claude/skills/bootstrap/SKILL.md` and `.claude/skills/intake/SKILL.md` (producers); `SETUP.md` (Step 2, operator-facing mention).

---

### [2026-06-04] Script write-safety for system-of-record mutations

- **ID:** script-write-safety
- **Category:** convention
- **Severity:** medium (data-loss risk if missed)
- **Depends on:** none

**What changed**
A script that mutates an external system of record (CRM, sequencer, datastore) follows four guardrails: default to a **dry-run** (write nothing without an explicit `--commit`), support **`--limit N`/`--all`** for graduated rollout, **upsert idempotently** on a natural key, and **snapshot before overwrite** (a read-only backup run first, routed to a durable home). Gated on writes — read-only scripts are exempt.

**Why**
The template already contemplated scripts that push to a CRM/sequencer but said nothing about doing it safely. An agent-written import with no dry-run can silently overwrite a live system of record — the only data-loss-class failure mode in the operational layer. These guardrails make the operation reversible and rerunnable for a few lines of code.

**How to assess fit**
Do you (or will you) run scripts that write to an external system — a CRM import, a sequencer push, a datastore upsert? If yes, applies the first time you write one. Read-only / pull-only instances can skip until they add a writer.

**How to adapt (not copy)**
The pattern is the four guardrails, not the literal flag names. Express `--commit`/`--limit`/`--all` (or your CLI's equivalent) however your scripts take arguments; the load-bearing parts are dry-run-by-default and snapshot-before-overwrite.

**Downstream risks / migration**
Additive guidance. Existing writer scripts without a dry-run gate are the ones to retrofit first.

**What I can't see from here**
- Whether a given script writes to a system of record or only reads is something only you can tell per script — apply the convention to the writers, not to harmless pulls.

**Reference (template implementation)**
`AGENTS.md` → "Module: scripts" (Conventions); `.claude/rules/08-scripts.md`; `.claude/skills/setup-api/SKILL.md` (Step 4).

---

### [2026-06-04] Standard script header + scripts navigation conventions

- **ID:** script-conventions
- **Category:** doc-architecture
- **Severity:** low
- **Depends on:** none

**What changed**
Scripts get a standard shape and the `scripts/` module gets a navigation surface. Every script opens with a fixed **header** — a docstring (purpose · what it talks to · in→out + which output tier · write-safety state) plus a **`ROOT` path anchor** (`Path(__file__).resolve().parent.parent`) that all tier paths derive from — and a **credential idiom** (env → `.env` → `.mcp.json` fallback, erroring on the exact missing var). `scripts/README.md` becomes a **live-scripts table** (only live scripts; retired ones drop off). Scripts are named in tool/concern **families**, and a hardened multi-step chain consolidates into one pipeline script exposing phases as subcommands — the natural graduation candidate.

**Why**
The template said only "document what each script does at the top" — no shape — so scripts and the README drifted as they accumulated. The header is the operator-facing interface that makes a script safe to hand off or graduate; the `ROOT` anchor is what makes output-routing reliable from any directory; the table + families give the consolidate/retire lifecycle a concrete surface to act on.

**How to assess fit**
Do you have (or expect) more than a couple of scripts? If yes, the header + table pay off immediately. A single-script instance can skip the table until the folder grows.

**How to adapt (not copy)**
Adopt the header *fields* and the `ROOT`-anchor idiom in whatever language your scripts use; keep the README a live-only inventory in your own format. The families/consolidation guidance is gated on "when a chain hardens" — not a mandate to consolidate prematurely.

**Downstream risks / migration**
Additive. Existing scripts can adopt the header opportunistically on next touch; no rewrite required.

**What I can't see from here**
- If you already track scripts somewhere else (a wiki, code comments), fold it into the README table rather than running two inventories that drift.

**Reference (template implementation)**
`AGENTS.md` → "Module: scripts"; `.claude/rules/08-scripts.md`; `.claude/skills/setup-api/SKILL.md` (Step 4).

---

### [2026-06-04] Per-workflow README skeleton

- **ID:** per-workflow-readme
- **Category:** doc-architecture
- **Severity:** low
- **Depends on:** none

**What changed**
The workflows module gains a per-workflow `README.md` **skeleton**: purpose (+ "replaces the local `scripts/X` execution model") · numbered what-it-does (pointing to the engine spec for depth) · an Infrastructure table (dependency · purpose · credentials env-var) · Schedule · Output + downstream consumers · Status · Rollback. **Schedule and Rollback are mandatory but may be honestly stubbed with reasoning before deployment** and filled on the deploy commit. Names the **pre-deployment** holding state — the README modeling the target shape while the producing code still lives in `scripts/`.

**Why**
The template shipped the workflows index-table header and the per-workflow file listing but never modeled what goes *inside* the README — the highest-friction part of graduation. The honest-stub convention prevents both fabricated deploy docs and silently-missing rollback steps: a stub is a TODO you can see; a missing section is a gap you'll forget.

**How to assess fit**
Do you graduate scripts into deployed/scheduled workflows? If yes, applies the first graduation. If you never deploy automation, skip — the `workflows/` module stays unused.

**How to adapt (not copy)**
The pattern is the section set + the honest-stub rule + the split-doc boundary (thin README = deployment contract; engine doc = spec). Section names and order are yours.

**Downstream risks / migration**
Additive (a doc skeleton). If your workflow READMEs already exist, retrofit the missing sections (especially Rollback) on next touch.

**What I can't see from here**
- Whether your deployment target needs sections this skeleton omits (a region, a secret-manager ref, a runbook link) — add them; the skeleton is a floor, not a ceiling.

**Reference (template implementation)**
`AGENTS.md` → "Module: workflows"; `.claude/rules/10-workflows.md`.

---

### [2026-06-04] Persistent datastore as a third integration genre

- **ID:** datastore-integration-genre
- **Category:** convention
- **Severity:** medium
- **Depends on:** output-artifact-boundary

**What changed**
`engine/integrations/` gains a **third doc genre** (alongside the API *reference* and the integration *diagnosis* doc): a **persistent-datastore reference** — role · connection · read-vs-write staging · schema conventions · migrations · when-it-graduates — shipped as a generic `engine/integrations/datastore.md` skeleton. **Migrations are tracked schema-as-code** (ordered, version-stamped DDL, header-commented) — the opposite of the gitignored `_output/`/`_retained/` *data* tiers. A datastore does **not** by itself trigger graduation to `workflows/`; while it stays `scripts/`-tier its migrations live in a top-level `{datastore}/migrations/` directory. Open hardening items go in a sibling `engine/{datastore}-dev-notes.md`.

**Why**
The template repeatedly referenced "persistent data stores" and listed `migrations/` as optional, but never said how to set one up, where the schema lives before a workflow exists, or how to document it — and the only `integrations/` genre shipped was API-reference-shaped (wrong for a DB). The gap let an operator conclude "I have a database, so I'm a workflow" (premature graduation), or strand migrations with nowhere to live.

**How to assess fit**
Do scripts need to read/write structured state *across runs* that has outgrown flat files (a cumulative account table, scored cohorts, longitudinal metrics)? If yes, this applies. If markdown + JSON indexes suffice — most instances — skip; the genre is optional.

**How to adapt (not copy)**
Document *your* store with the genre's section set, in your stack's idiom (the skeleton uses generic Postgres/Supabase examples — your vendor, connection form, and migration tool are yours). The load-bearing parts: schema-tracked / data-gitignored, the read-then-write staging, and "a datastore doesn't graduate you."

**Downstream risks / migration**
- If you currently keep schema DDL untracked or hand-edit a live schema, move to tracked, ordered migrations before the schema drifts from the files.
- This refines the prior "migrations live in the workflow directory" guidance: that's true only for a store a single workflow *owns*; a store shared across scripts keeps its migrations at repo root.

**What I can't see from here**
- Whether your store is workflow-owned or script-shared determines where its migrations live — only you know the ownership. Classify before you place them.
- Pooled vs. direct connection, region/latency, and security posture (row-level security) are deployment specifics the template can't choose for you — document them in your reference.

**Reference (template implementation)**
`AGENTS.md` → "Module: engine" (Conventions) and "Module: workflows"; `.claude/rules/06-engine.md`; `.claude/rules/10-workflows.md`; `engine/integrations/datastore.md`; `.gitignore`.

---

### [2026-06-04] PULL score-band reconciliation

- **ID:** pull-score-band-reconciliation
- **Category:** methodology
- **Severity:** medium
- **Depends on:** none

**What changed**
`pull-framework.md` carried three overlapping-but-divergent band sets (a score of 12 was simultaneously "Moderate", "BENEFIT", and "Tier 3 Weak"). The **classification** bands — DEMAND (14-20) / BENEFIT (8-13) / NEITHER (0-7) — are now the single source of truth, and the finer interpretation sub-bands and synthesis scorecard tiers are **re-derived to nest strictly inside them** (Strong 17-20 + Moderate 14-16 = DEMAND; 8-13 = BENEFIT; 0-7 = NEITHER). No sub-band crosses a classification boundary, so any score yields exactly one label.

**Why**
A borderline call (12, 13, 14) landed on a different label depending on which table the agent read, producing inconsistent `pull-index.json` classifications and scorecard tiers. The classification bands were already the only set propagated downstream, so they were the de-facto truth; the other tables just disagreed with it.

**How to assess fit**
Have you customized your PULL score bands or tier tables? If your framework doc has interpretation/tier bands that don't line up with your DEMAND/BENEFIT/NEITHER thresholds, this applies. If you only ever use the three classification bands, you're already consistent.

**How to adapt (not copy)**
Pick your classification thresholds as the anchor and make every finer band nest inside one class. The pattern is "one score → one label," not the specific 14/8/0 cutoffs (yours may differ).

**Downstream risks / migration**
- **The classification thresholds did not change** (14/8/0), so existing PULL analyses keep their DEMAND/BENEFIT/NEITHER classification — nothing is reclassified. Only the finer *sub-band labels* and scorecard *tier* boundaries shifted; a synthesis regenerated after adopting may move a borderline prospect between tiers (never between classes).
- If your instance *did* change classification thresholds, that's a different, heavier migration — re-run classification on existing analyses.

**What I can't see from here**
- If you set your own thresholds, confirm no finer band straddles a class boundary after adopting — the defect is any sub-band spanning the 13/14 (or 7/8) line.

**Reference (template implementation)**
`demand/pull-framework.md` (scoring rubric + Full Scorecard tiers).

---

### [2026-06-04] Attribution-presence enforcement

- **ID:** attribution-presence-enforcement
- **Category:** mechanic
- **Severity:** low
- **Depends on:** claimed-attribution-tag

**What changed**
Attribution was load-bearing but unenforced. Two complementary checks now cover it: eval **T7** gains a light **presence** criterion (a described PULL analysis must use the confidence tags — presence, not per-claim density, not dating; a sparse-but-tagged analysis passes), and **`/gtm-os-health` Check 6** gains a flag-only **presence lens** that flags (LOW) an evidence-bearing artifact carrying *zero* confidence tags — the accumulated-corpus case the clean-room eval can't see. The ROADMAP routes the *robust* git-diff version to the trajectory-eval tier.

**Why**
An agent could quietly stop attributing and every gate stayed green. T7 is the cheap tripwire (does a fresh analysis use the convention at all?); the health lens is the state backstop (did the corpus drift to unattributed?). Deliberately *not* added to the behavioral eval as a structural check — that split keeps the eval behavioral and the state-audit in health, per the "verify is blind to conventions" architecture.

**How to assess fit**
Do you rely on attribution in PULL analyses / segment rationale / messaging? If yes, both checks apply. If you customized T7 or `/gtm-os-health`, fold the presence checks into your versions.

**How to adapt (not copy)**
The pattern is presence-not-density, flag-only, four-tag, no-dating-requirement. Express the T7 Must and the health lens in your eval/health docs' own wording; skip pure-template artifacts (`_EXAMPLE.md`, an empty instance) so you don't false-flag.

**Downstream risks / migration**
Additive checks; nothing reinterprets data. A first health run after adopting may surface old unattributed analyses — that's the point (recommend re-attributing on next touch; never rewrite claims unilaterally).

**What I can't see from here**
- Your `_EXAMPLE.md` or template fixtures already attribute; make sure your health lens skips them, or it reports a false finding on shipped artifacts.

**Reference (template implementation)**
`.gtm-os/eval/tests.md` (T7); `.gtm-os/eval/README.md`; `.claude/skills/gtm-os-health/SKILL.md` (Check 6); `ROADMAP.md` (Trajectory evals).

---

### [2026-06-04] OS-meta skill-naming convention

- **ID:** skill-naming-convention
- **Category:** convention
- **Severity:** low
- **Depends on:** none

**What changed**
Slash commands follow a two-class naming rule. **GTM-operation skills** — each does one GTM-domain task (querying demand, drafting a sequence) — stay **bare** (`/pull-query`, `/draft-sequence`). **OS-meta skills** — they operate on the OS or the instance itself (auditing instance state, reporting cross-module status, upgrading the instance) — take the **`gtm-os-`** prefix. Two prior `gtm-` outliers are renamed onto the convention: `/gtm-status` → `/gtm-os-status` and `/gtm-upgrade` → `/gtm-os-upgrade`, forming the `gtm-os-{health,status,upgrade}` trio. `run-eval` and `release-check` are grandfathered bare (heavily cross-referenced; the rule resolves outliers, not a retroactive mass-rename).

**Why**
Three naming styles coexisted (bare, `gtm-os-`, `gtm-`) with no rule connecting them, so a meta command's name had to be memorized rather than derived. The test "does it act on a GTM artifact, or on the OS itself?" lets an agent or operator predict the right command and signals at a glance which commands touch system machinery.

**How to assess fit**
Do you have skills with mixed prefixes? List `.claude/skills/`. If your meta/system skills use an inconsistent prefix, this applies. If you renamed or added your own skills, decide per skill which class it's in. No Claude Code skills → skip.

**How to adapt (not copy)**
The pattern is the two-class rule and the `gtm-os-` marker for OS-meta — not a mandate to rename every skill. Rename only your *orphan-styled* meta skills; leave bare GTM-operation skills bare; grandfather heavily-referenced ones. A rename must be **atomic**: directory, SKILL.md `name`, every doc that lists it, and every cross-skill reference change in one commit, or `/`-autocomplete and cross-references break.

**Downstream risks / migration**
- A skill rename is only complete if atomic. For the upgrade skill specifically, the rename also touches its working-branch name, its one-time bootstrap-install sentence, and its install path — update all together.
- Operator muscle-memory, external runbooks, or saved prompts that type the old command stop resolving — there is no alias.
- Historical release notes that name a skill at a past tag stay verbatim (they record the name as it was); don't rewrite history.

**What I can't see from here**
- **The self-refresh trap for the upgrade skill.** An instance that still has the *old-named* upgrade skill runs it by its old name, and that old skill self-refreshes by fetching the template's *old-named* directory — which no longer exists after this rename. Clean path: install/keep the skill under the new name and remove the old directory in the *same* operation, so the running skill never points at a vanished template path.
- Whether *your* meta skills are truly OS-meta or GTM-operation is a judgment only you can make for skills you authored — classify by what a skill operates on, not by the word in its name.

**Reference (template implementation)**
`.claude/CLAUDE.md` (skill table); `.claude/skills/gtm-os-status/`; `.claude/skills/gtm-os-upgrade/`; `.claude/skills/gtm-os-health/SKILL.md` (the self-referential-checks table that motivates the convention).

---

### [2026-05-29] `_output/` artifact boundary

- **ID:** output-artifact-boundary
- **Category:** convention
- **Severity:** medium
- **Depends on:** none

**What changed**
Script and pipeline output is split into two classes. **Repo state** — PULL analyses, segment/messaging/campaign docs, JSON indexes, scoring and enrichment specs, small reference lookup tables — is permanent and lives in module folders. **Transient artifacts** — enrichment CSVs, scored account batches, intermediate processing files, exports for external tools — are disposable and live in a gitignored `_output/` directory at the repo root. `_output/` is **write-only for agents**: an agent never browses or reads it to inform a decision, because its contents may be stale, partial, or from a different run. (A single pipeline run's own scripts may chain intermediate files through it — the prohibition is on *agent reasoning*, not on the pipeline's internal plumbing.)

**Why**
Without the boundary, pipeline runs dump artifacts into module folders (`engine/`, `scripts/`, `segments/`), and agents later read that debris back as if it were authoritative state. The write-only rule is the load-bearing part: it stops an agent from grounding a decision in stale intermediate data that looks like repo state but isn't.

**How to assess fit**
Does this instance run scripts or pipelines that produce data files (CSVs, JSON batches, tool exports)? Where do those land today? If artifacts are written into module folders, or if there's an ad-hoc `output/`, `exports/`, `tmp/`, or `data/` directory holding pipeline products, this applies. If the instance only ever produces markdown docs and JSON indexes — no data-file pipeline — it does not apply and should be skipped.

**How to adapt (not copy)**
The pattern is **the boundary plus the write-only discipline**, not the literal folder name. An instance that already has an output directory under another name (e.g. `exports/`) can either rename it to `_output/` or keep its own name and adopt the rules: gitignored, write-only for agents, never referenced from module docs. Express the discipline wherever this instance documents script behavior and agent conventions — the location and wording will differ per instance.

**Downstream risks / migration**
- Artifacts currently sitting *inside* module folders should be moved to the output directory or deleted. Any module doc that points at one (`see engine/scored.csv`) becomes a broken reference — find and fix those before/after the move.
- Scripts with hardcoded output paths into module folders need their paths rerouted to the output directory.
- Add the output directory to `.gitignore` (and confirm nothing already committed under it should be preserved as repo state — if it should, extract it into a doc or index first).

**What I can't see from here**
- **Before gitignoring the output directory, audit it for transient-*looking* state** — an append-only log, a cumulative record, anything another doc treats as the source of truth. If deleting it would lose history you can't regenerate, it's state: promote it to a tracked location *before* gitignoring, or you'll silently discard it on the next clone. (See the follow-up entry `transient-looking-state`.)

**Reference (template implementation)**
`AGENTS.md` → "Pipeline Artifacts and Output"; `.claude/rules/06-engine.md` and `.claude/rules/08-scripts.md` (conventions); `.claude/skills/setup-api/SKILL.md` (output routing); `.gitignore`; `README.md` (structure block).

---

### [2026-05-29] Transient-looking state in the artifact zone

- **ID:** transient-looking-state
- **Category:** convention
- **Severity:** medium (data-loss risk if missed)
- **Depends on:** output-artifact-boundary

**What changed**
Refines the repo-state-vs-transient split. A file can sit in the artifact/output zone yet be **repo state** — typically an append-only or longitudinal record (a running metrics log, a cumulative history) that another doc treats as the persistent source of truth. Being a data file (CSV/JSON) in the output directory does not make it transient. Before gitignoring or clearing the output zone, audit it and promote any such file to a tracked module location.

**Why**
The original `output-artifact-boundary` model assumed *data files = transient*. Real pipelines produce transient-*looking* state. A blanket gitignore of the output directory silently discards that history on the next clone — a data-loss failure mode that surfaced in a live instance: an append-only weekly metrics log was living inside the artifact directory, and the instance agent (not the original changelog entry) caught that wholesale-gitignoring it would erase the history. This entry encodes that catch so it doesn't depend on the agent being sharp.

**How to assess fit**
Only relevant if you adopted `output-artifact-boundary` and have an output/artifact directory. Audit it: is anything in there append-only, cumulative, or referenced by another doc as the source of truth? If yes, this applies. If the directory holds only regenerable per-run outputs, skip.

**How to adapt (not copy)**
Move the state file to wherever tracked state belongs in *your* structure (e.g. a metrics folder under the relevant module), update the script that writes it and any doc that reads it, then gitignore the artifact zone wholesale. If moving is genuinely too costly, whitelist the one file in `.gitignore` — but a tracked file inside a gitignored zone re-muddies the boundary the parent entry exists to draw, so prefer moving.

**Downstream risks / migration**
- Reroute the producing script's output path; update any doc that references the file by path.
- Confirm nothing else writes to the old path.

**What I can't see from here**
- Your output directory may hold *more than one* kind of state. Audit every file, not just the obvious one — a per-run detail file is transient, but a roll-up beside it may be state.

**Reference (template implementation)**
`AGENTS.md` → "Pipeline Artifacts and Output" (the transient-looking-state caution paragraph and the audit-before-gitignore rule).

---

### [2026-05-29] `.gtm-os/` namespace for OS machinery

- **ID:** gtm-os-namespace
- **Category:** doc-architecture
- **Severity:** low (organizational; no behavior change)
- **Depends on:** none

**What changed**
OS-internal, editor-agnostic machinery moves under one hidden namespace, `.gtm-os/`. The eval harness relocates from top-level `eval/` to `.gtm-os/eval/`; the adoption ledger lives at `.gtm-os/upgrade-log.md`. The reasoning: `.claude/` already holds Claude-Code-specific system files (rules, skills), but the eval harness and the ledger are *editor-agnostic* — they needed a home that isn't tied to one editor and isn't mixed in with operator GTM content at the top level. `.gtm-os/` = how the OS operates itself; everything else top-level = your GTM data.

**Why**
Keeps the top level for GTM content (`context.md`, `demand/`, `segments/`, …) and consolidates system machinery so "OS internals" is visibly distinct from "my data." Sits alongside `.claude/` as its editor-agnostic counterpart.

**How to assess fit**
Applies to any instance with a top-level `eval/` directory (it ships with the template, so most). If you've customized `eval/tests.md` for your domain, this still applies — you're relocating your customized harness, not replacing it.

**How to adapt (not copy)**
`git mv` your existing `eval/` to `.gtm-os/eval/` — keep your domain-specific tests and results intact. Update path references: `.gitignore` (`eval/results.md` → `.gtm-os/eval/results.md`), `.claudeignore` (`eval/` → `.gtm-os/`), and any skill that reads `eval/tests.md` or `eval/results.md` (`run-eval`, `release-check`). Conceptual "eval" mentions and the `/run-eval` skill name don't change — only literal paths. Add a short `.gtm-os/README.md` describing the namespace. If your instance organizes things differently, the principle is "editor-agnostic OS machinery under one namespace" — the exact folder name is yours.

**Downstream risks / migration**
- Any doc or script referencing `eval/tests.md` or `eval/results.md` *by path* breaks until updated — grep for the `eval/` path form and fix.
- Worktree-based flows (`/release-check`) read the path inside the worktree, so the same rename applies there.

**What I can't see from here**
- You may have *other* top-level files that are really OS machinery (a custom lint, a local config the agent maintains) — consider moving those under `.gtm-os/` too while you're here.
- External tooling (CI, scripts outside the repo) may hardcode `eval/` paths. A grep inside the repo won't find those — check anything that runs the eval from outside.

**Reference (template implementation)**
`.gtm-os/README.md` (namespace doc); `.claudeignore` and `.gitignore` (ignore paths); `.claude/skills/run-eval/` and `.claude/skills/release-check/` (updated path refs).

---

### [2026-05-29] Pipeline dev-notes companion doc

- **ID:** engine-dev-notes
- **Category:** doc-architecture
- **Severity:** medium
- **Depends on:** none

**What changed**
When auditing or hardening a pipeline, findings live in a sibling `engine/{pipeline}-dev-notes.md`, not inside the canonical pipeline doc. Findings are priority-ranked (P0 must-fix-before-next-run → P3 nice-to-have); each has a fixed shape — **Status** (open / fixed / wontfix / out-of-scope) · **Files** (line refs) · **Problem** · **Decision/Fix** · **Follow-up**. The doc also carries a "Pipeline Stages" scope table (what's in-pipeline vs campaign-execution vs one-off — which decides what graduates) and named design-decision initiatives that record *deferrals with the evidence still missing*.

**Why**
A hardening effort spans sessions. Without a ledger, the *why* behind each fix evaporates, settled WONTFIX decisions get re-litigated, and deferrals lose track of what evidence they're waiting on. Keeping it *beside* the canonical doc (not inside) keeps that doc clean while preserving the full audit trail.

**How to assess fit**
Do you have an `engine/` with pipeline scripts you audit or harden over time? If you only keep markdown docs with no evolving pipeline code, skip.

**How to adapt (not copy)**
The pattern is a priority-ranked, fixed-shape findings ledger living next to the system doc — not the literal filename. Name it for your pipeline; one dev-notes per pipeline if you have several. The priority bands and the per-finding shape are the load-bearing parts.

**Downstream risks / migration**
Additive (a new doc). If you currently keep audit notes *inside* a canonical pipeline doc, move them out so the canonical doc stays clean.

**What I can't see from here**
You may already track findings ad-hoc (TODOs in code, a scratch file). Consolidate into the dev-notes rather than adding a third place they can drift apart.

**Reference (template implementation)**
`AGENTS.md` → "Module: engine" Conventions; `.claude/rules/06-engine.md`.

---

### [2026-05-29] Integration diagnosis doc (second genre)

- **ID:** integration-diagnosis-doc
- **Category:** convention
- **Severity:** low
- **Depends on:** none

**What changed**
`engine/integrations/` now has two doc genres. The pre-populated files are API *references* (auth, endpoints, rate limits — what the tool *is*). When you debug a *misbehaving* integration, write the second kind — an integration **diagnosis** doc: a dated **bottom-line verdict**, **expected vs. actually-observed** (with real evidence), **ruled-out** hypotheses, remaining **hypotheses**, a **decisive test** to discriminate them, and **fix options** with trade-offs.

**Why**
Debugging a flaky integration is expensive and the knowledge evaporates. A diagnosis doc captures the hard-won finding as a durable artifact instead of guesswork re-derived the next time the same tool acts up.

**How to assess fit**
Have you ever debugged an integration that wasn't doing what you expected (a sync that silently drops data, an API field that's always empty)? If you run integrations at all, this applies the first time one misbehaves. No integrations yet → skip until you have one.

**How to adapt (not copy)**
A doc *shape*, not a folder requirement — write it wherever you keep integration docs. The skeleton (verdict · expected vs. observed · ruled-out · hypotheses · decisive test · fix options) is the reusable part.

**Downstream risks / migration**
Additive.

**What I can't see from here**
A diagnosis doc goes stale once the issue is fixed. Date it and note when it's resolved, so a later reader knows it's history, not a live problem.

**Reference (template implementation)**
`AGENTS.md` → "Module: engine" Conventions; `.claude/rules/06-engine.md`.

---

### [2026-05-29] Script lifecycle: consolidate → retire

- **ID:** script-consolidate-retire
- **Category:** convention
- **Severity:** low
- **Depends on:** none

**What changed**
The script lifecycle gains its missing middle: create → **consolidate → retire** → graduate. When two scripts overlap, fold them into one and **delete** the loser; record what superseded a retired script; keep `scripts/README.md` listing only *live* scripts; prefer a thin CLI wrapper around the survivor over reviving a retired script.

**Why**
The template documented *create* and *graduate* (→ workflows) but not consolidate/retire — the operations that keep `scripts/` from rotting into a pile of overlapping, half-broken near-duplicates an agent can no longer tell apart.

**How to assess fit**
Do you have a `scripts/` folder that's accumulated more than a couple of scripts, some overlapping? Few or no scripts → a no-op until the folder grows.

**How to adapt (not copy)**
Pure discipline — no files to create. Apply it the next time you notice two scripts doing overlapping work: consolidate, delete, record. Adapt *where* you record the supersession to your own conventions (commit message, dev-notes, README).

**Downstream risks / migration**
Deleting a script is destructive if something external calls it.

**What I can't see from here**
A script may be referenced by an external scheduler, a teammate's runbook, or a cron you set up outside the repo. A repo-internal check won't find those — confirm nothing external invokes a script before retiring it.

**Reference (template implementation)**
`AGENTS.md` → "Module: scripts" (Lifecycle); `.claude/rules/08-scripts.md`.
