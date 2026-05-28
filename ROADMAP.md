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
After someone clones and disconnects from the template repo, they have no way to pull in new skills, eval tests, framework improvements, or rule changes we ship later. Need a mechanism — could be a merge-from-upstream script, a `/upgrade` skill that cherry-picks template changes without clobbering operator content, or something else. Tricky because operator files (context.md, demand/, segments/) must never be touched, but system files (AGENTS.md, .claude/skills/, eval/) should update. TBD — ideas exist, needs design.

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
Agents running on schedules or triggers, operating on the repo without a human in the loop. This is where it gets hard:
- **Write safety** — An agent that auto-ingests transcripts and writes PULL analyses is fine. An agent that auto-creates segments or kills campaigns based on stale data is dangerous. Need a classification of which operations are safe for autonomous execution vs. which require human approval.
- **Conflict with human sessions** — An agent runs at 3am and updates synthesis.md. A human opens a session at 9am and their context is stale. Need a way to surface "things changed since your last session" — possibly a hook, possibly a `/what-changed` skill.
- **Audit trail** — When an agent makes a decision (created a segment, updated an angle's status, archived a campaign), the reasoning needs to be traceable. status.md entries are a start but might need richer provenance — who/what triggered it, what evidence was used, what the alternatives were.
- **Guardrails** — Rate limits on autonomous writes. Mandatory human review for destructive operations (kill segment, archive campaign). Maybe a "proposed changes" staging area that agents write to and humans approve.
- **State coherence** — Multiple agents running in parallel could produce conflicting state. Agent A updates synthesis while Agent B creates a segment based on the old synthesis. Need either locking, sequencing, or eventual consistency with reconciliation.

No design yet — this is the problem space. The single-operator model works today; multiplayer is where the architecture gets tested.

## Ideas (Not Yet Scoped)

- **Auto-calibrate eval tests on bootstrap** — When `/bootstrap` or `/quickstart` fills context.md, automatically rewrite eval fallback prompts to match the domain. Currently the eval runner constructs dynamic prompts at eval time, but pre-baked domain-specific tests would be more reliable.
- **Synthesis diff** — When updating synthesis.md with a new batch, produce a "what changed" summary: new patterns, shifted rates, emerging/dying triggers. Currently the temporal comparison is manual.
- **Campaign feedback loop** — When campaign metrics come in, automatically check whether the messaging angle's demand evidence still holds. Flag angles where results diverge from PULL predictions.
- **Multi-repo sync** — For teams running separate repos (e.g., sales vs. marketing), a way to sync shared state (segments, ICP, demand evidence) without merging repos.
- **File naming conventions for LLM efficiency** — Agent instructions need tighter guidance on naming files. Names should be specific enough to disambiguate without reading the file (e.g., `account-scoring-model.md` not `scoring-model.md` — there could be multiple scoring models). Optimize for the LLM, not the human: an agent scanning a directory listing should be able to route correctly from filenames alone. Applies to PULL analyses, engine docs, campaign files, scripts. Audit current naming patterns and add conventions to AGENTS.md.
