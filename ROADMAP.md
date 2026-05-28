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

## Ideas (Not Yet Scoped)

- **Auto-calibrate eval tests on bootstrap** — When `/bootstrap` or `/quickstart` fills context.md, automatically rewrite eval fallback prompts to match the domain. Currently the eval runner constructs dynamic prompts at eval time, but pre-baked domain-specific tests would be more reliable.
- **Synthesis diff** — When updating synthesis.md with a new batch, produce a "what changed" summary: new patterns, shifted rates, emerging/dying triggers. Currently the temporal comparison is manual.
- **Campaign feedback loop** — When campaign metrics come in, automatically check whether the messaging angle's demand evidence still holds. Flag angles where results diverge from PULL predictions.
- **Multi-repo sync** — For teams running separate repos (e.g., sales vs. marketing), a way to sync shared state (segments, ICP, demand evidence) without merging repos.
