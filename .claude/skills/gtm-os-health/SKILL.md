---
name: gtm-os-health
description: "Audit the health of THIS instance's lived-in state — structural completeness, evidence chains, index integrity, output hygiene, drift, and context.md consistency (conflicts + cached-vs-source drift). Reports findings and fixes safe drift; flags judgment calls. Runs inside Claude Code, no API key."
argument-hint: "[optional: module name to scope the audit, e.g. engine]"
---

Audit whether this instance's accumulated state is well-formed. Modules grow organically over many sessions; this surfaces the structural drift that no single task ever flags — a module missing its overview map, a broken evidence chain, an output directory rotting into a junk drawer.

## When to Use

- Periodically, or when something feels off ("did we ever write the engine overview?")
- After a module has grown a lot (several new docs) in a short span
- Before a `/handover`, so the next session inherits a clean read of the state
- When the silent session-start reconcile hints at something worth a deeper look

**This is not `/run-eval`.** Eval tests whether the *rules* produce correct behavior (clean-room, behavioral). This tests whether *this lived-in repo* is well-formed (instance state). A health failure means the instance drifted; an eval failure means the instructions are wrong. Keep them separate — don't add state audits to the eval suite, and don't use this to judge instruction correctness.

| Check | Question it answers | Target |
|-------|--------------------|--------|
| `/run-eval` | Do the rules produce correct behavior? | The system |
| `/release-check` | Are the rules internally coherent? | Template docs |
| **`/gtm-os-health`** | Is this lived-in instance well-formed? | Instance state |

## Process

### Step 1: Scope

If a module argument was given (e.g. `/gtm-os-health engine`), audit only that module's checks. Otherwise audit the whole instance.

Identify the scratch-output directory: default `_output/`, but instances may rename it (read `.gitignore` — the disposable, gitignored output dir). Note the name; the output-hygiene checks use it.

### Step 2: Run the Checks

Run each category. For every finding, classify it: **OK**, **auto-fixed** (safe drift you corrected silently), or **needs decision** (a judgment call you flag, never auto-resolve).

**1. Structural completeness** — does each instantiated module have its blueprint-defined overview?
- `engine/` exists → is `engine/architecture.md` present? An engine with 3+ single-concern stage docs (pipeline/scoring/enrichment) and no `architecture.md` is the canonical gap — the territory exists without the map. Flag it; offer to build it from the AGENTS.md engine blueprint.
- `demand/` with 5+ PULL analyses → are `demand/synthesis.md` and `demand/key-learnings.md` present? (The synthesis trigger may have been missed.)
- For each instantiated module, cross-check its canonical files against the blueprint in AGENTS.md and the scoped rule in `.claude/rules/`. Flag missing canonical/overview files.

**2. Evidence chains** — does downstream work cite upstream evidence?
- Every `active` segment has ≥1 `pull_evidence` entry pointing to a file that exists.
- Every messaging angle references a segment that exists.
- Every campaign references a messaging angle (and segment) that exists.
- Flag dangling references (a link to a file that's gone) and unfounded artifacts (a segment/angle/campaign with no evidence).

**3. Index integrity** — do JSON indexes match the markdown on disk?
- For each index (`pull-index.json`, `segments.json`, `messaging.json`, `campaigns.json`): every entry's `file` exists; every markdown file in the module dir has an index entry.
- This is the one category you **auto-fix silently** (matches the session-start reconcile rule): add missing entries, drop orphaned ones, then report what you reconciled.

**4. Output hygiene** — is output following the three-tier convention? (See AGENTS.md "Pipeline Artifacts and Output".)
- Scratch dir (`_output/`/renamed): numbered-iteration siblings (`foo.csv`, `foo2.csv`, `foo3.csv`), underscore-"protected" files (the "protect this file" anti-pattern), or a large stale pile? Flag and recommend promote-or-purge — never auto-delete.
- `_retained/`: any file present with no corresponding line in `_retained/manifest.md`? Manifest missing entirely? Flag — gitignored data with no tracked record is how `_retained/` rots.
- Tracked-under-gitignored: no tracked file should live inside a gitignored zone (the scratch dir, `_retained/`) except a whitelisted manifest. Run `git ls-files _output _retained` (substitute the renamed scratch dir from Step 1) — any hit other than `_retained/manifest.md` is a file committed under a gitignored zone, which a clone silently loses (or leaks, if it carries PII under `_retained/`). Flag CRITICAL under `_retained/` (same PII concern as `samples/`), MED otherwise — recommend extracting genuine repo-state into a tracked doc/index first; never auto-delete.
- `samples/`: any committed file containing contact-PII patterns? Run the same grep `/release-check` uses:
  ```bash
  git ls-files 'samples/**' | xargs -r grep -lE \
    '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}|\+?[0-9][0-9 ().-]{7,}[0-9]' 2>/dev/null
  ```
  Any hit is CRITICAL — PII leaked into a committed sample; it belongs in `_retained/`.

**5. Drift & orphans**
- `status.md` — present and recently updated? A long-stale log on an active instance is worth flagging.
- Canonical docs reference files that actually exist (no broken cross-refs).
- Once `architecture.md` exists: are there stage docs at engine root it doesn't mention? (orphan stages — the map is behind the territory.)
- Files sitting in module dirs that nothing references.

**6. Context foundation** — is `context.md` internally consistent and current? (See AGENTS.md "Context Foundation".) Flag-only; **never auto-resolve** — the "current" value is ground truth only the operator holds.
- **Conflicts (the payload):** scan for two statements that disagree about the same fact — a headcount stated in one section and contradicted in another, a positioning claim that violates a product rule. Report each as a candidate: quote both statements with their locations and ask which is current. Don't pick a winner. This is the check that catches the contradictions a growing file accretes.
- **Cached-vs-source drift:** where a pointer in `context.md` names a source of truth (e.g. "source of truth: `demand/synthesis.md`", "live-sourced from the CRM API"), diff the cached values against that source and flag divergence. The pointer tells you exactly what to compare, so this lens is reliable — not open-ended contradiction-hunting.
- **Age:** list dated `[VERIFIED: … · YYYY-MM]` claims oldest-first, so the eye lands on the most likely-stale. **No expiry rule** — undated facts are never flagged (dating is the opt-in decay signal), and an old date is a prompt to re-confirm, not an error. Don't decide per-fact when something becomes obsolete.
- **Attribution presence:** attribution is load-bearing in the evidence-grounded artifacts (`demand/` PULL analyses, segment rationale, messaging angles — see AGENTS.md "Attribution"). Where Age checks whether *dated* tags have gone stale, this checks whether the convention is *applied at all*: scan those artifacts for any use of the confidence tags (`[VERIFIED]` / `[CLAIMED]` / `[INFERRED]` / `[UNVERIFIABLE]`). Flag (LOW) an artifact that makes evidence claims with **zero** confidence tags — the corpus may have drifted to unattributed. Count them; don't adjudicate any single claim, don't demand a density, and don't demand dating (dating stays opt-in). Skip pure-template artifacts: the shipped `_EXAMPLE.md` already attributes, and a near-empty instance with no real analyses is OK, not a finding.

### Step 3: Report

Present a health report. Overall verdict first, then findings grouped by category, each with severity and a concrete recommended action.

```
## GTM OS Health — {date}

**Verdict:** Healthy | Minor drift | Needs attention

### Auto-fixed
- {index reconciles performed, if any}

### Needs decision
- [HIGH] engine/ has 5 stage docs but no architecture.md — the pipeline has no overview map.
  → Offer: build it from the engine blueprint as a high-level map with cross-refs.
- [CRITICAL] samples/contacts.csv contains email patterns — PII leaked into a committed sample.
  → Move to _retained/ (+ manifest line); replace with a masked slice if a sample is needed.
- [MED] _output/ holds test_accounts{,2,3,4}.csv — numbered-iteration accretion.
  → Promote the keeper, purge the rest.
- [MED] context.md conflict: "~7 SMB sellers" (Company) vs 8 CCMs listed (Organization) — same fact, two values.
  → Surface both; ask the operator which is current. Don't auto-resolve.
- [LOW] 3 of 9 PULL analyses make evidence claims with no `[VERIFIED]`/`[CLAIMED]`/`[INFERRED]`/`[UNVERIFIABLE]` tags — attribution convention may have lapsed.
  → List the files; recommend re-attributing on next touch. Don't edit claims unilaterally.

### OK
- Evidence chains intact · indexes reconciled · status.md current · context.md consistent
```

## Fix vs Flag Policy

- **Auto-fix silently:** index reconciliation only (this is already the session-start behavior — do it and report it).
- **Flag and offer:** missing overview files, structural gaps, suspected output rot. Never auto-create a doc or auto-delete a file — that respects "Check Before You Create" and the rule that output is the operator's to clear.
- **CRITICAL, surface loudly:** PII in committed samples. Recommend the move; don't rewrite the file unilaterally.
- **Flag, never resolve — context.md conflicts & drift:** the "current" value is ground truth only the operator holds. Quote both conflicting statements (or the cached value vs its named source); never pick a winner or edit `context.md` unilaterally.

## Relationship to the Startup Check

The silent session-start reconcile (see `.claude/rules/01-system-identity.md`) is the lightweight heartbeat — it fixes index drift and checks evidence chains quietly, every session. This skill is the full physical: the on-demand, deep audit. The startup check can defer to it ("for a full check, run `/gtm-os-health`"); they don't duplicate each other.

## Notes

- Read-mostly: the only writes are silent index reconciles. Everything else is reported for the operator to act on.
- Honest reporting: if a check can't run (a module isn't bootstrapped, an index is absent), say so — don't infer health from a check you skipped.
