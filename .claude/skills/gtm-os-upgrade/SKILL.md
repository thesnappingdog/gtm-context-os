---
name: gtm-os-upgrade
description: "Upgrade this GTM Context OS instance to the latest template developments. Fetches the latest template, reconciles what's new against THIS instance's structure, and applies approved changes on a review branch — pausing before anything destructive. Operator-initiated."
argument-hint: "[optional: local path to a template checkout, e.g. ../gtm-context-os — defaults to fetching the public repo]"
---

Bring this instance up to date with the latest template developments — **without re-cloning and without migrating operator content**. The template ships *patterns and mechanics*, not folder structures. Your job is to fetch the latest template, work out what's new, and express each new idea in *this* instance's layout — or decide it doesn't apply.

## Core principles

- **Adapt, don't copy.** Patterns translate into this instance's structure. The template's folder names are illustrative, not mandatory. You rewrite the instance's own files; you never paste template files over operator content.
- **Operator-initiated, never autonomous.** Never run on a schedule.
- **Everything happens on a branch.** Nothing touches the operator's working state until they review the diff and merge.
- **Pause before anything destructive.** Additive/prose changes flow to the diff for review; destructive changes stop and require an explicit plain-language go-ahead (see the destructive rule below).
- **Never touch operator content** except as an approved item explicitly requires.

## What "destructive" means (the pause rule)

The branch makes everything *technically* recoverable, but a destructive change buried in a large diff can be rubber-stamped on review. Pausing forces you to **explain the consequence in plain language at decision time** instead of hoping the operator spots it. Apply this test to every proposed change: *"could this lose or silently re-interpret something the operator already has?"*

- **Pause + explain + require explicit ack:**
  - Deleting or overwriting operator content (PULL analyses, segments, messaging, `context.md`, synthesis, indexes).
  - Relocating or gitignoring anything *currently tracked* (a tracked file moving into a gitignored zone can be orphaned).
  - Anything that changes the *meaning* of existing data — e.g. a scoring-band change that would reclassify existing PULL analyses or stale a synthesis doc.
  - Deleting files.
- **Auto-apply on the branch → review via diff (no pause):**
  - Adding new files or skeletons.
  - Editing instruction prose (`AGENTS.md`, `.claude/rules/`).
  - New folders; `.gitignore` additions that don't strand a tracked file.
  - Doc wording fixes.

## Process

### Step 1: Fetch the latest template
- If `$ARGUMENTS` gives a local template path (e.g. `../gtm-context-os`), use it as the source.
- Otherwise shallow-clone the canonical public repo to a throwaway temp dir:
  `git clone --depth 1 https://github.com/thesnappingdog/gtm-context-os <tmp>`
  Read from it; delete it at the end. This is a **read-only reference** — no remote is added to the instance, nothing is merged file-to-file.
- If you can't reach the template, stop and tell the operator.

### Step 2: Work out what's new — two sources, not one
1. **The CHANGELOG (curated intent).** Read the template's `CHANGELOG.md`. Each entry has a stable `ID` and explains what changed, why, how to assess fit, and how to adapt. This is the *explanation layer*.
2. **The real file diff (catches drift).** The CHANGELOG can lag reality; comparing actual files surfaces template improvements never written up as entries. **Probe, don't dump** — a naive `diff -r` of two structurally-diverged repos is mostly noise (instances rename docs, reorganize sections). Instead, check specific system files for known-divergence signals: does the instance's `AGENTS.md` carry each major section the template's does (synthesis spec, conventions, blueprints)? Does `.claude/CLAUDE.md`'s skill table list every skill that actually exists? Which `.claude/skills/` and `.claude/rules/` exist in the template but not here? Surface real gaps as **uncatalogued differences** alongside the changelog entries.

   **Exclude template-maintainer machinery** — it exists to *build* the template, not to run an instance, so never propose porting it: the `release-check` skill, the CHANGELOG's "Maintainer discipline" section, `docs/`, `ROADMAP.md`.

Then compute **unconsidered entries**: read this instance's adoption ledger (`.gtm-os/upgrade-log.md`). An entry is *considered* iff its `ID` appears in the ledger. Unconsidered = any upstream entry ID **absent from the ledger — regardless of date**. There is no date watermark; never infer coverage from dates. If the ledger doesn't exist, this is the first upgrade: every entry is unconsidered, and you'll create the ledger at the end.

If there are no unconsidered entries and no uncatalogued differences, tell the operator the instance is current and stop.

### Step 3: Assess each item against THIS instance (read-only)
No branch yet — assessment is read-only, so nothing is created if the operator decides not to proceed. For each unconsidered entry (and each uncatalogued difference), in severity order (high → low):
1. Read its **How to assess fit**, then actually inspect the instance — read the relevant files, check the structure. Don't assess from the entry text alone.
2. Read the entry's **Reference** files in the fetched template if you need the full intent.
3. Decide **Adopt** / **Adapt** (applies but lands differently here — describe the difference) / **Skip** (doesn't apply, or it's maintainer-only machinery — give the reason).
4. Check **Depends on**: don't propose adopting something whose prerequisite this instance skipped or hasn't adopted — flag it.
5. Classify each proposed change as **destructive** or **safe** per the rule above, naming the actual files/analyses/indexes it would touch or invalidate.

**Updating this skill is just one of the items.** The newest version of `gtm-os-upgrade` is in the fetched template — if it's newer, treat adopting it as an ordinary (safe) item. That's how the instance stays current without any special self-refresh mechanism.

### Step 4: Present the plan
Show a per-item plan, grouped, **destructive items clearly flagged**:

```
## Template upgrade — N unconsidered entries + M uncatalogued differences

### Adopt (safe — will apply to the branch)
- [some-id] Short name (severity)
  Fit: <what in this instance makes it apply>
  Change in our idiom: <what files change, expressed in THIS layout>
  Touches: <files>

### Adapt (safe)
- ...

### ⚠ Destructive — needs your explicit go-ahead before I apply
- [other-id] Short name
  What it does here: <plain-language consequence — what could be lost or re-interpreted>
  Files: <...>

### Suggest skip
- [id] ... — reason it doesn't apply here.
```

### Step 5: Create the branch, then apply
Only after the operator has seen the plan:
- Create a branch `gtm-os-upgrade-<today>` (use the current date). Commit a checkpoint first if the working tree isn't already clean, so there's a guaranteed restore point. All changes land here.
- **Safe items:** apply directly to the branch.
- **Destructive items:** stop on each one, restate the plain-language consequence, and apply only after the operator explicitly acks that specific item. If they decline, skip it and record the decision.

Make every change *in this instance's idiom* — respect `AGENTS.md` (check-before-you-create, evidence chains, index maintenance).

### Step 6: Verify
Run `/run-eval` (and any domain-specific eval fixtures the instance has). Report results plainly. If something regressed, surface it — don't bury it. Note that the behavioral eval is structurally blind to convention adoption, so passing eval is necessary, not sufficient — the operator's diff review is the real check.

### Step 7: Record decisions in the ledger
Append one decision **per entry ID** to `.gtm-os/upgrade-log.md` (create it on first run) — adopted, adapted, *and* skipped, each with reason and date. This is the instance's provenance: why it diverged, decided when. Also record any uncatalogued difference you acted on, keyed by a short slug, so it isn't re-proposed. Format:

```markdown
# Upgrade Adoption Ledger
<!-- Agent-to-agent infrastructure, like the JSON indexes. The operator never reads or edits this file. -->

One decision per template CHANGELOG entry ID. An entry is **considered** iff its ID appears below.
"Unconsidered" = any upstream entry ID absent here, regardless of date. No date watermark — coverage is the set of IDs present.

## CHANGELOG entries

### output-artifact-boundary — ADAPTED — 2026-05-29
Kept existing exports/ rather than renaming to _output/ (scripts hardcode it); adopted write-only discipline.

### gtm-os-namespace — SKIPPED — 2026-05-29
<reason it doesn't apply here>

## Uncatalogued differences (caught by the real file diff, not in the CHANGELOG)

### claude-md-skill-table — ADOPTED — 2026-05-29
<what was stale and what you fixed>
```

### Step 8: Hand off for review
Tell the operator the work is on branch `gtm-os-upgrade-<today>`. They review the diff and either merge it or discard the branch (discard = zero cost — nothing touched their working state). Clean up the temp template checkout.

## First-time bootstrap (existing instances)

An instance cloned before this skill existed won't have it. It can't be pushed in — the operator pulls it once. The simplest install is one sentence to the agent: *"install the gtm-os-upgrade skill from the template."* The agent fetches `.claude/skills/gtm-os-upgrade/SKILL.md` from the public repo and writes it into `.claude/skills/gtm-os-upgrade/`. After that first install, every future run re-fetches the template and keeps the skill current as an ordinary item (Step 3) — so the bootstrap is one-time, ever. New clones ship the skill and need no bootstrap.
