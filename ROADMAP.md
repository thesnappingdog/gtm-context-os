# Roadmap

Ideas and planned improvements. Not prioritized — this is a scratchpad for what's next.

## Up Next

### CRM exploration and engine bootstrapping
After connecting a CRM via `/setup-api`, there's no guided path to understanding what's already in it. The system should be able to explore the CRM schema (fields, objects, custom properties), identify which fields are actually populated and useful, surface data quality issues, and use all of that to bootstrap `engine/architecture.md` with a real picture of the current data flow — not a blank template.

Could be a new skill (`/explore-crm`?) or an extension of `/setup-api`. The output would be:
- Field inventory with fill rates and sample values
- Recommended fields for segmentation, triggers, and enrichment
- Draft `engine/architecture.md` grounded in what actually exists
- Gaps identified (e.g., "no industry field — enrichment needed")

### Data bootstrapping beyond CRM
Same idea for other connected systems — call recorders (what meetings exist, what's transcribed, what's not), enrichment tools (what data is already available), sequencing tools (what campaigns are running). The goal: when someone connects a tool, the system should learn from it, not just document the API.

### Upgrade path for existing instances
**Implemented (advisory model + fetch-the-template).** Instances upgrade by adopting *described patterns*, not by syncing files: the `/gtm-os-upgrade` skill fetches the latest template (shallow clone of the public repo, read-only reference), reconciles what's new against the instance's (unique, customized) structure — using both the pattern-shaped `CHANGELOG.md` *and* the real file diff, which catches template drift never written up as an entry — and applies approved changes on a review branch, pausing before anything destructive. Operator-initiated, recorded per entry ID in an agent-to-agent adoption ledger. Operator files are never touched by construction (we ship intent, not folders). See `CHANGELOG.md` and `.claude/skills/gtm-os-upgrade/`.

Open follow-ups:
- **Verify coverage for adopted conventions.** The eval suite tests behavior (routing/evidence/identity), so it's structurally blind to whether an adopted *convention* actually works — a live adoption scored 8/8 on an eval that couldn't have failed on that change. Proposed split: behavioral conventions rely on the "What I can't see from here" entry prompts; mechanically-checkable invariants ("no CSV in module folders," "no module doc references the output dir," "nothing tracked under a gitignored zone") get a lightweight structural lint folded into `/release-check`. Decision pending: this split vs. extending the eval suite itself. Don't bloat the behavioral eval with filesystem invariants.
  - **Empirically confirmed (`2026-05-29c` release-check):** a full `/release-check` of three new doc-convention patterns + the `/gtm-upgrade` rebuild scored **8/8 — and could not have failed on any of it.** The *consistency agent* was the only check that actually vetted the changes (caught orphaned-reference risk, confirmed rule↔blueprint alignment). This is concrete evidence the behavioral eval is the wrong instrument for convention coverage. Leaning: make the consistency/structural check in `/release-check` the home for convention invariants, and add a small set of mechanical assertions to it (orphaned skill/path references, every CHANGELOG "Reference" path resolves, no stale renamed-skill mentions) — keep the behavioral eval for behavior. Open question is whether to *also* grow the behavioral eval for the few conventions that do produce observable behavior.
- **Untested paths:** a methodology entry that invalidates existing operator data (the genuinely dangerous case); batched review when an instance is many entries behind; missing-prerequisite handling (`Depends on` an entry that was skipped).

### Trajectory evals: test conventions by executing them

The current eval suite (`/run-eval`, T1–T8) is **single-turn, stated-intent**: the prompt is "what *would* you do if asked X," and the model grades its own *described* response. The eval skill says so outright — *"the eval agent is also read-only in practice — it evaluates behavior, doesn't execute it."* That's the root cause of the convention-blindness empirically confirmed in the upgrade thread above (ROADMAP "Verify coverage for adopted conventions"): conventions only manifest as **side effects of doing the work** — where the file lands, whether `pull-index.json` got the new row, whether a retired script's loser was actually deleted, whether transient output went to `_output/` and not the module folder. A "what would you do" answer produces none of those, so nothing can check them.

Two complementary instruments fill the gap (the static one is the existing thread; this is the dynamic one):
- **Static structural lint** (already proposed above) — check the repo *as-is* for invariant violations. Cheap, no execution.
- **Trajectory / state evals** (this entry) — actually *run* the agent for one or more turns in a worktree, then assert on the resulting `git diff`. Catches the agent *producing* a violation, and catches failures that are **emergent over turns** (writes a PULL analysis in turn 2, forgets the index in turn 5; doesn't offer synthesis when the 5th analysis crosses the threshold).

Two sub-shapes, don't conflate them:
- **Execution probes (cheap)** — one action, real side effect, objective assertion. "Retire script B for A" → is B deleted? is `scripts/README.md` updated? One turn, no simulated chat. (Another candidate: "analyze this call" → does the *written* PULL analysis carry confidence tags? T7 only sees the agent's stated intent; the git diff of the actual file is where attribution-presence is truly checkable.)
- **Golden session replays (expensive)** — scripted multi-turn operator ↔ agent, needed *only* when the interesting failure emerges across turns. Source material: real session logs from live instances — distilled, they're better than synthetic because they encode the workflows that actually matter.

Validity discipline (so multi-turn self-grading survives): **three separate contexts** — Operator (scripted turns, never improvised by default), System-Under-Test (fresh session, real instructions, *never sees the rubric*), Judge (sees the final diff + transcript). And **assert on objective state, not response quality** — git-diffable facts need no judgment; reserve the LLM-judge for the genuinely subjective slivers.

Where it lives: **Tier 3 of `/release-check`**, not `/run-eval`. Real execution is slow and flaky — a small curated set gating dev→main, not something on every instruction change. Fits the existing release-check architecture (it already spawns bootstrap/consistency/eval sub-agents in a worktree).

A full spec with a worked golden scenario (PULL analysis → index side-effect, the exact blind spot T7 can't see) is kept in the maintainer notes.

### Extracting clean context from unfinished sessions

Sessions often end before the work resolves — mid-diagnosis, mid-decision, mid-build. The chat holds a mix of durable insight (worth keeping) and ephemeral back-and-forth (noise, dead ends already superseded). There's no codified discipline for triaging what to persist and where, so it's improvised each time.

A good pattern has emerged in practice — **layered persistence, most-durable first:**
- **Module artifact** (`engine/`, `demand/`, …) — the durable findings: what was concluded, what was ruled out, open hypotheses, the decisive next test. The real output; ideally written *as you go*, not reconstructed at wrap-up.
- **`status.md`** — a session log entry: what happened, decisions, next steps.
- **`todo.md` / open tasks** — reconcile *stale* items so they reflect the new state, not the pre-session assumption; make the next concrete action explicit.
- **Handover** (`/handover`) — a continuation message pointing at the artifact and the open fork.
- **Memory** — durable preferences/working-style, not task state.

The key judgment is durable-vs-ephemeral: an unresolved fork should be captured *with its alternatives and the test that would decide it*; superseded attempts and dead ends can be dropped. The best outcome is that most context is *already* in the repo because it was written as the work happened — wrap-up then just reconciles stale state and points the way forward.

Could be a skill (`/wrap-up`?) or an extension of `/handover`: detect stale todo/status state, verify open decisions are captured with their alternatives, separate durable findings from ephemera, route each to the right layer, then generate the handover. `/handover` today produces the continuation message; this is the broader *extract-and-reconcile* step that should precede it.

## Hooks

Ideas for Claude Code hooks that automate housekeeping:

- **Auto-commit on context.md changes** — After `/bootstrap` or `/quickstart` fills context.md, auto-commit so the baseline is captured before the operator starts editing.
- **Auto-commit on PULL analysis** — When a new file lands in `demand/pull-analyses/`, commit it with the prospect/company name in the message. Prevents losing analysis work if a session crashes.
- **Index reconciliation on session start** — Pre-session hook that checks JSON indexes match their markdown sources. Currently this is an instruction in AGENTS.md; a hook would make it automatic.
- **Status log reminder on session end** — Post-session hook that checks if substantive work was done (file changes beyond .json indexes) and reminds to update status.md if it wasn't touched.

## Multiplayer

The repo currently assumes a single operator working with a single AI session. That breaks in two directions:

### Multiple humans
A sales lead, a RevOps person, and a marketer all working in the same repo. Problems to solve:
- **Concurrent edits** — Two people analyzing calls at the same time, both updating pull-index.json. Git handles file-level conflicts but JSON index merges are painful. Might need per-file indexes that get reconciled, or a merge strategy for JSON arrays.
- **Ownership and boundaries** — Who can change context.md? Who can kill a segment? Who can modify AGENTS.md? Currently there are no roles or permissions — anyone can change anything. Might need lightweight ownership conventions (not ACLs, just "talk to X before changing Y").
- **Visibility** — When someone adds a PULL analysis or changes a messaging angle, others need to know without reading every commit. status.md is the current mechanism but it's manual. Could be solved by hooks that post to Slack, or a `/changelog` skill that summarizes recent changes.
- **Branching model** — Do people work on main? Feature branches per campaign? PRs for anything that touches system files? Need conventions that balance safety with speed — GTM operators aren't engineers and won't tolerate heavy git workflows.

### Autonomous agents
Agents running on schedules or triggers, operating on the repo without a human in the loop. The write-safety / audit-trail / conflict-with-human-sessions trio now has a reference design — **the write boundary**: a scheduled workflow writes files and stops at the git boundary; it never commits or pushes. Committing stays a human-reviewed act in a later interactive session. See AGENTS.md, "Module: workflows" → "The write boundary," and CHANGELOG `workflow-write-boundary`. What's still open:
- **Write safety** — *Narrowed by the write boundary*: an agent that auto-ingests transcripts and writes PULL analyses never becomes repo state unreviewed. Still open: classifying which *kinds* of unattended writes are safe to accumulate vs. which need escalation before a human even sees the next diff (auto-creating segments, killing campaigns) — folds into Guardrails below.
- **Conflict with human sessions** — *Resolved by the write boundary*: an agent running at 3am produces uncommitted files, not a silent update to main. A human opening a session at 9am finds a reviewable diff, not stale context masquerading as current. A `/what-changed`-style surface for "here's what accumulated" is a nice-to-have now, not a gap.
- **Audit trail** — *Resolved for the commit layer*: a human-composed commit message, written after reading the diff, can't silently misdescribe what an unattended job did — the failure mode that motivated the write boundary (CHANGELOG `workflow-write-boundary`). Still open: richer *decision* provenance for judgment calls an agent makes mid-session (created a segment, updated an angle's status, archived a campaign) — who/what triggered it, what evidence was used, what the alternatives were.
- **Guardrails** — Still open. Rate limits on autonomous writes. Mandatory human review for destructive operations (kill segment, archive campaign). A "proposed changes" staging area is partly given for free at the file level by the write boundary; the open question is which operations should never even reach the working tree unattended.
- **State coherence** — Still open. Multiple agents running in parallel could produce conflicting state. Agent A updates synthesis while Agent B creates a segment based on the old synthesis. Need either locking, sequencing, or eventual consistency with reconciliation.

Write safety, audit trail, and conflict-with-human-sessions have a reference design now (the write boundary); guardrails classification and state coherence across parallel agents are still open problem space. The single-operator model works today; multiplayer is where the architecture gets tested.

## Ideas (Not Yet Scoped)

- **Auto-calibrate eval tests on bootstrap** — When `/bootstrap` or `/quickstart` fills context.md, automatically rewrite eval fallback prompts to match the domain. Currently the eval runner constructs dynamic prompts at eval time, but pre-baked domain-specific tests would be more reliable.
- **Synthesis diff** — When updating synthesis.md with a new batch, produce a "what changed" summary: new patterns, shifted rates, emerging/dying triggers. Currently the temporal comparison is manual.
- **Campaign feedback loop** — When campaign metrics come in, automatically check whether the messaging angle's demand evidence still holds. Flag angles where results diverge from PULL predictions.
- **Multi-repo sync** — For teams running separate repos (e.g., sales vs. marketing), a way to sync shared state (segments, ICP, demand evidence) without merging repos.
- ~~**File naming conventions for LLM efficiency**~~ — **Done.** Expanded into "Document Architecture" section in AGENTS.md. Covers file naming (kebab-case, name for the question answered), single-concern docs, split/don't-split criteria, module-level overview tables, cross-referencing conventions.
