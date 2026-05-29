---
name: upgrade
description: "Check the GTM Context OS template for new patterns and propose what applies to THIS instance. Operator-initiated. Adapts patterns to your structure — never forces template folders or clobbers your content."
argument-hint: "[optional: path or URL to template source, e.g. ../gtm-context-os]"
---

Pull new **patterns and mechanics** from the template and propose how to apply them to *this* instance. The template ships ideas, not folder structures — your instance is unique, and your job here is to translate each idea into your own layout, or decide it doesn't apply.

## Core Principle

**Adapt, don't copy.** The template's `CHANGELOG.md` describes patterns independently of file paths. You assess each against the actual instance, then propose changes *in this instance's idiom*. You never overwrite operator content, and you never impose the template's folder structure. The operator approves every item before anything changes.

This is **operator-initiated only** — never run autonomously, never on a schedule.

## What You Need

- **Template source.** The `$ARGUMENTS` path/URL if given, else the canonical template repo (`https://github.com/thesnappingdog/gtm-context-os`). For local testing the operator may pass a sibling path like `../gtm-context-os`. If you can't reach it, stop and tell the operator.
- **The template `CHANGELOG.md`** — the list of patterns, each with a stable `ID`.
- **This instance's adoption ledger** — `.gtm-os/upgrade-log.md`. Agent-to-agent infrastructure (same class as the JSON indexes — the operator never reads or edits it). If it doesn't exist, this is the first upgrade: treat every changelog entry as unconsidered, and create the ledger at the end.

## Process

### Step 1: Load both sides
Read the template `CHANGELOG.md` and the instance ledger. Compute **unconsidered entries** = entries whose `ID` has no decision recorded in the ledger. If there are none, tell the operator the instance is current and stop.

### Step 2: Assess each unconsidered entry against THIS instance
For each entry, in order of severity (high → low):

1. Read its **How to assess fit**. Then actually inspect the instance — read the relevant files, check the structure. Don't assess from the entry text alone.
2. If you need to understand the pattern deeply, read the entry's **Reference** files in the template source. Understand the *intent*, not just the implementation.
3. Decide one of:
   - **Adopt** — applies cleanly; you can express it here.
   - **Adapt** — applies, but this instance's structure means it lands differently than the template (e.g. a directory already exists under another name). Describe the difference.
   - **Skip** — doesn't apply to this instance. Give the reason.
4. Check **Depends on**: if an entry depends on a pattern this instance skipped or hasn't adopted, flag it — don't propose adopting something whose prerequisite is missing.
5. Surface **Downstream risks / migration** *concretely for this instance*: name the actual files, analyses, or indexes that adopting would touch or invalidate. This is where you catch things like "adopting the new band definition would reclassify 3 of our PULL analyses and invalidate synthesis.md."

### Step 3: Present the proposal
Show the operator a per-item proposal, grouped:

```
## Template upgrade — considered N entries (up to tag YYYY-MM-DD)

### Recommended: adopt
- [output-artifact-boundary] _output/ artifact boundary (medium)
  Fit: we run pipeline.py which writes CSVs into engine/ today.
  Proposed change in our idiom: rename exports/ → _output/, gitignore it,
  reroute 3 scripts' output paths, adopt write-only discipline in scripts/README.
  Touches: .gitignore, scripts/{a,b,c}.py, scripts/README.md, AGENTS.md conventions.
  Downstream: 2 module docs reference engine/*.csv — will fix those refs.

### Adapt with changes
- ...

### Suggest skip
- [some-id] ... — reason it doesn't apply here.
```

Order by severity. Be specific about *what files change* and *what could break*. The operator decides per item.

### Step 4: Apply approved items
For each approved item, make the change **in this instance's idiom** — not by copying template files. Respect everything in `AGENTS.md`: check-before-you-create, evidence chains, index maintenance. Never modify operator content beyond what the approved item requires.

### Step 5: Verify
Run `/run-eval` after applying. If the instance has its own domain eval fixtures, run those too. Report results. If anything regressed, surface it — don't bury it.

### Step 6: Record decisions in the ledger
Append to `.gtm-os/upgrade-log.md` (create it on first run). Record every entry you considered — adopted, adapted, *and* skipped — with the reason and date. The ledger is the instance's provenance: why it diverged from the template, decided by whom, when.

```markdown
# Upgrade ledger
<!-- Agent-to-agent. The operator never edits this. -->

Considered up to template tag: 2026-05-29

### output-artifact-boundary — ADAPTED — 2026-05-29
Renamed existing exports/ to _output/ rather than adding a new dir.
Rerouted pipeline.py, export_csv.py output paths.
Adopted write-only discipline in scripts/README.md and AGENTS.md.

### some-other-id — SKIPPED — 2026-05-29
We don't run content workflows; the content-topic mechanic doesn't apply.
```

## Rules

- **Operator-initiated, never autonomous.** Every applied change is operator-approved, per item.
- **Adapt, don't copy.** Patterns translate into this instance's structure. The template's folder names are illustrative, not mandatory.
- **Never touch operator content** except as an approved item explicitly requires.
- **Surface downstream effects before applying**, especially anything that would invalidate existing analyses, segments, or indexes. A methodology change can silently corrupt the *meaning* of data computed under the old rule — catch it here.
- **The ledger is yours, not the operator's** — maintain it as a side effect, like the JSON indexes. Don't ask the operator to read or edit it.
- **Bootstrapping note:** on the very first upgrade this skill may not yet exist in the instance. The operator can run the flow ad hoc by pointing this session at the template's `CHANGELOG.md` and following this process; adopting the `upgrade` skill itself can be the first ledger entry.
