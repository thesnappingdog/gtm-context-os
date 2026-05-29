# Changelog

This file is the **upgrade channel** for instances cloned from this template. It is *not* a git log. Each entry describes a **pattern or mechanic** that changed — written so that a cloned instance's agent can evaluate whether the pattern applies to its own (unique, customized) structure and **adapt it, not copy files**.

Instances are expected to diverge. We do not ship folder structures or force migrations — we ship the patterns and mechanics that make the system efficient, and each instance decides how (or whether) to express them.

## How instances use this

Operators run `/upgrade` — **operator-initiated, never automatic**. The instance's agent reads the entries it hasn't considered yet, assesses fit against the actual instance, and proposes, per item, what to adopt, adapt, or skip — with reasoning. Decisions are recorded in the instance's **adoption ledger** (agent-to-agent infrastructure, like the JSON indexes — operators never read or edit it). See `.claude/skills/upgrade/SKILL.md`.

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

## Entries

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
