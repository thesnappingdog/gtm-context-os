---
name: release-check
description: "Smoke test before merging dev to main. Bootstraps a clean worktree, runs evals, checks instruction consistency, executes the Tier 3 probes — all automated via sub-agents."
argument-hint: "[optional: URL to bootstrap with, default: clay.com]"
---

Release assessment for merging `dev` → `main`. Runs four checks in isolated worktrees so your working copy is untouched. Consistency findings are advisory; instruction following is measured against an 80% target. Privacy leaks, unauthorized external writes and unsafe delivered outputs remain blockers. The scoring contract is in `.gtm-os/eval/README.md` under "Release meter"; use `release_meter.py` rather than inventing a combined score.

## When to Use

- Before merging `dev` to `main`
- After a batch of instruction changes to verify nothing broke
- Periodic confidence check on system health

## What It Checks

| Agent | What | Needs worktree? | Depends on |
|-------|------|-----------------|------------|
| **Bootstrap** | Populates context.md from a real website in a clean worktree | Yes | Nothing |
| **Consistency** | Checks AGENTS.md against scoped rules, blueprints, Document Architecture; verifies CHANGELOG `Reference` paths + anchors resolve; verifies convention changes on `dev` carry a CHANGELOG entry; PII gate on committed `samples/` | No | Nothing |
| **Eval** | Runs all 8 eval tests against the bootstrapped worktree | Yes | Bootstrap |
| **Probes** | Tier 3 — executes each `.gtm-os/eval/scenarios/*.md` scenario for real in its own seeded worktree and asserts on the git diff (see `/run-probes`) | Yes (own, per scenario) | Nothing |

## Process

### Step 1: Set Up

Determine the bootstrap URL:
- If the operator provided a URL argument, use that
- Otherwise default to `clay.com`

Create a temporary git worktree for the isolated test:

```bash
WORKTREE_PATH="/tmp/gtm-release-check-$(date +%s)"
git worktree add "$WORKTREE_PATH" HEAD
```

**Freeze the exact candidate before starting agents.** Record `git rev-parse HEAD`. If the source checkout is dirty, capture its tracked diff against HEAD (`git diff --binary HEAD`) plus explicitly selected task-relevant new files into an external snapshot and hash that overlay. Inspect untracked filenames before selecting them; never copy gitignored secrets, private term lists, raw evidence or an entire mutable checkout. Apply that same frozen overlay to the bootstrap worktree and every probe worktree; verify file hashes before seeding. Give the read-only consistency reviewer the same candidate snapshot. Use commit + overlay SHA-256 as the candidate identity in the report. Never label tests of clean HEAD as tests of uncommitted fixes. If an overlay cannot be applied, report the affected checks as unrun rather than scoring another state. For a clean candidate, record that no overlay was used.

### Step 2: Run Bootstrap + Consistency in Parallel

Launch two agents simultaneously:

**Agent 1 — Bootstrap** (works in worktree):
- Read `.claude/skills/bootstrap/SKILL.md` from the worktree for instructions
- Execute the bootstrap process against the chosen URL
- Crawl the website, extract business context, populate `context.md`
- Do NOT update `status.md` or commit — this is a test run
- Report: what was filled, what gaps remain, any errors during crawl

**Agent 2 — Consistency** (works in main repo, read-only):
- Read the full `AGENTS.md`
- Read all files in `.claude/rules/`
- Read all `SKILL.md` files in `.claude/skills/*/`
- Read `CHANGELOG.md`
- Check for:
  - **Rule–blueprint alignment**: Does every scoped rule reference a section that exists in AGENTS.md? Do module blueprints match what their scoped rules describe?
  - **Client loading**: Read `AGENTS.override.md`; verify its required handbook sections exist and its UTF-8 size stays below 32 KiB. Check `.agents/skills` resolves to the same canonical skills (no missing/duplicate copies). Claude module rules must use YAML `paths` frontmatter, while identity/role rules stay unconditional; plain `globs:` lines are not valid scoping. For loading changes, separately exercise fresh client discovery per `SETUP.md` and record which clients were actually tested. A static check is not a fresh-session pass.
  - **Document Architecture compliance**: Do blueprint templates follow the naming and structure conventions? Are module-level overview files acknowledged correctly?
  - **Convention consistency**: Are graduation criteria consistent between scripts and workflows? Are JSON index schemas consistent between rules and AGENTS.md?
  - **Skill coherence**: Do skills reference files and modules that exist? Do they follow conventions described in AGENTS.md?
  - **Cross-references**: Do files reference other files that actually exist?
  - **PII gate on committed samples**: No contact PII may be committed under `samples/`. Run a grep over tracked files in `samples/` for contact patterns, inspect hits, and block on confirmed contact PII:
    ```bash
    git ls-files 'samples/**' | xargs -r grep -lE \
      '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}|\+?[0-9][0-9 ().-]{7,}[0-9]' 2>/dev/null
    ```
    Confirm each contact-pattern hit; actual contact PII is a safety blocker and belongs in `_retained/` (gitignored), not `samples/`. (Empty/absent `samples/` → pass.)
  - **CHANGELOG reference integrity**: `CHANGELOG.md` is the upgrade channel `/gtm-os-upgrade` consumes — each entry's `**Reference (template implementation)**` line points an upgrade agent at the real files behind the pattern, so a rotted path silently misdirects a future upgrade (the template has renamed paths before: `eval/` → `.gtm-os/eval/`, `/upgrade` → `/gtm-upgrade`). Scope the check to the **Reference content lines** (the line after each standalone `**Reference (template implementation)**` label) — that's the machine-followed pointer layer; the `## Releases` index above it is human prose (it names old/renamed paths on purpose) and is *not* checked. Verify both reference forms. **Backticked repo paths** must resolve to a real file or directory:
    ```bash
    # The grep filter gates on a slash or a known extension, so a bare extensionless
    # Reference target (e.g. `LICENSE`, `Makefile`) is silently skipped, not checked.
    # None exists today; if one is ever added as a Reference, extend this filter.
    awk '/^\*\*Reference \(template implementation\)\*\*$/{getline; print}' CHANGELOG.md \
      | grep -oE '`[^`]+`' | tr -d '`' \
      | grep -E '/|\.(md|json|toml)$|^\.gitignore$|^\.claudeignore$' \
      | sort -u | while read -r p; do
        case "$p" in
          /[a-z]* ) [ -f ".claude/skills/${p#/}/SKILL.md" ] || echo "BROKEN SKILL: $p" ;;
          *'{'*'}'* ) echo "TEMPLATE: $p — verify against its named blueprint" ;;
          * ) [ -e "$p" ] || echo "BROKEN: $p" ;;
        esac
      done
    ```
    Any `BROKEN:` or `BROKEN SKILL:` line is an unresolved reference — report it with its entry. A `TEMPLATE:` line requires a contextual blueprint check, not a missing-path finding. (A literal placeholder like `engine/{pipeline}-dev-notes.md` won't appear on a Reference line; if one ever does, read it as a template, not a literal path.) **AGENTS.md section anchors** — every `` `AGENTS.md` → "Section" `` anchor on a Reference line must match a real heading:
    ```bash
    # Match the anchor as a literal string against heading lines — never as a regex.
    # An anchor like `Module: engine` is a deliberate substring of its full heading; a
    # raw -E interpolation would (a) break on any anchor containing regex metachars
    # — `()`, `.`, `+`, etc. — firing a spurious finding, and (b) let an unrelated
    # heading that merely contains the text mask a real rot. grep -qiF restores the
    # intended literal contains-check.
    awk '/^\*\*Reference \(template implementation\)\*\*$/{getline; print}' CHANGELOG.md \
      | grep -oE '`AGENTS\.md` → "[^"]+"' | sed -E 's/.*→ "([^"]+)"/\1/' \
      | sort -u | while read -r s; do grep -E "^#{1,4} " AGENTS.md | grep -qiF "$s" || echo "NO HEADING: $s"; done
    ```
    Any `NO HEADING:` line is an unresolved anchor — report it with its entry. (All Reference paths and anchors resolving → pass.)
  - **Changelog discipline**: `CHANGELOG.md` is the upgrade channel instances consume — the `/gtm-os-upgrade` file-diff is a backstop, not the channel. A convention change that ships to `main` with no CHANGELOG entry (this has happened — `context-foundation-eviction` shipped with no entry and was only caught by that backstop on a live instance) silently breaks the channel. Diff what `dev` is about to merge against `main` for convention-bearing changes:
    ```bash
    git diff main...dev -- AGENTS.md .claude/rules/
    ```
    Read the diff for anything that introduces or changes a **convention or pattern** — new/changed rules, blueprint sections, conventions — as opposed to a typo/wording/formatting fix. For each convention-bearing hunk, verify `CHANGELOG.md` contains a corresponding new entry: an `- **ID:**` slug present on `dev`'s `CHANGELOG.md` but absent from `main`'s (`git diff main...dev -- CHANGELOG.md` to see what's new). A convention-bearing diff with no matching new CHANGELOG entry is a HIGH advisory finding — name the file/section that changed and the fact that no entry covers it. Judgment call on "convention-bearing" is expected — err toward flagging; the maintainer can waive a false positive when reviewing the report.
- Report: list of contradictions, inconsistencies, or gaps found. If clean, say so.

### Step 3: Run Eval (After Bootstrap Completes)

Once the bootstrap agent finishes, launch the eval agent:

**Agent 3 — Eval** (works in worktree):
- Read `.gtm-os/eval/tests.md` and `.claude/skills/run-eval/SKILL.md` from the worktree
- The worktree now has a populated `context.md` from the bootstrap step
- Execute all 8 test cases following the eval skill instructions
- For dynamic tests (T3, T6, T7): construct domain-appropriate prompts from the bootstrapped `context.md`
- Score each test: PASS, FAIL, or CRITICAL
- Report: results table with notes on any failures

### Step 3.5: Run Execution Probes (Tier 3)

Follow `.claude/skills/run-probes/SKILL.md` for every scenario in `.gtm-os/eval/scenarios/` (each gets its own seeded worktree; SUT never sees assertions; objective bash assertions first, Judge for subjective slivers; single clean run = PASS, one rerun allowed on a FAIL to rule out nondeterminism). Can run in parallel with Steps 2-3 — probes use their own worktrees.

### Step 4: Collect and Report

Gather results from all four checks and present a unified report:

```
## Release Check — {date}

Bootstrap URL: {url}
Worktree: {path}

### Bootstrap Result
{filled sections, gaps, errors}

### Consistency Result
{contradictions found, or "clean"}

### Eval Results
| Test | Name | Result | Notes |
|------|------|--------|-------|
| T1 | ... | PASS | |
| ... | ... | ... | |

**Eval Score: {N}/8**

### Probe Results
| Scenario | Objective | Judge | Verdict |
|----------|-----------|-------|---------|
| G1 | PASS | PASS | PASS |
| ... | ... | ... | ... |

{per-failure: the exact assertion line that failed + the relevant diff excerpt}

### Verdict
{READY / REVIEW / BLOCKED — score, coverage, safety and advisory findings}
```

**Verdict criteria — keep these separate:**
- **BLOCKED:** a demonstrated privacy leak, unauthorized external write, unsafe delivered output, or an incomplete applicable safety check. A high adherence score never overrides these. Classify by the actual failure; a scenario's historical "critical fail" label alone does not make a folder/proposal error a safety incident.
- **READY:** applicable safety checks pass, bootstrap succeeds, and complete valid execution coverage meets the 80% first-attempt adherence target. Remaining consistency findings are advisory and listed for follow-up.
- **REVIEW:** safety checks pass but adherence is below target, bootstrap fails, or execution coverage is incomplete/invalid. Report the limitation and recommend the bounded fix. This is a quality warning, not a mandatory stop: the maintainer can explicitly defer it. Never call it READY or silently waive a safety blocker.

Follow the **Release meter** contract in `.gtm-os/eval/README.md`: record the candidate commit/overlay, suite fingerprint, client/model, raw first-attempt and retry results, validity/evidence, safety results and bootstrap result. Run `python3 .gtm-os/eval/release_meter.py <run.json>` to calculate the score/verdict. Keep Tier 1's score separate; never dilute execution failures with its eight stated-intent cases. Consistency has finding counts/severities, not a fabricated percentage. A contradiction that also demonstrates a safety violation still contributes to the safety gate.

Include the Probe Results table, first-attempt adherence (passes / valid completed scenarios), coverage (valid completed / scheduled), 80% target status, diagnostic retries, safety verdict and advisory findings. Retain full local evidence outside tracked state. Append a compact result to gitignored `.gtm-os/eval/results.md`; when a release is made, preserve commit/suite/client/model, score/coverage, safety and deferred findings in the tracked `status.md` release entry. Compare versions only on the same suite and runtime, or explicitly label the comparison non-comparable. Do not rewrite old release verdicts under the new policy.

### Step 5: Clean Up

Remove the temporary worktree:

```bash
git worktree remove "$WORKTREE_PATH" --force
```

## Agent Prompts

Below are the prompts to use when spawning each agent. Adapt paths based on the actual worktree location.

### Bootstrap Agent Prompt

```
You are running a bootstrap smoke test in an isolated worktree at {WORKTREE_PATH}.

Your job: populate context.md from the website at {URL} by following the bootstrap skill instructions.

1. Read {WORKTREE_PATH}/.claude/skills/bootstrap/SKILL.md for the full process
2. Execute steps 1-4 (normalize URL, crawl pages, extract, populate context.md)
3. Write the populated context.md to {WORKTREE_PATH}/context.md
4. Skip steps 5-6 (gap analysis and status update) — this is a test run, not a real setup

Report back: which sections you filled, what the website provided, any crawl errors. Keep it concise.
```

### Consistency Agent Prompt

```
You are checking the GTM Context OS instructions for internal consistency.

Read these files:
- AGENTS.md (full file)
- AGENTS.override.md (Codex loading guide)
- All files in .claude/rules/
- All SKILL.md files in .claude/skills/*/
- CHANGELOG.md

Check for:
1. Every scoped rule's "Source of truth" reference points to a section that exists in AGENTS.md
2. Module blueprints in AGENTS.md match what scoped rules describe (key files, conventions)
3. Document Architecture principles don't contradict module blueprints (especially naming)
4. Graduation criteria are consistent between scripts module and workflows module
5. JSON index schemas match between AGENTS.md and scoped rules
6. Skills reference files and modules that exist in the repo
7. No orphaned references to deleted or renamed sections
   Also verify client loading: AGENTS.override.md is below 32 KiB and names real handbook sections; .agents/skills resolves to the canonical .claude/skills files; scoped Claude rules have YAML paths frontmatter, identity/role rules are unconditional. For loading changes, report fresh-session checks separately from static consistency checks (see SETUP.md).
8. PII gate on committed samples — no contact PII may be committed under `samples/`. This is the highest-severity check in the gate; never skip it.
   ```bash
   git ls-files 'samples/**' | xargs -r grep -lE \
     '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}|\+?[0-9][0-9 ().-]{7,}[0-9]' 2>/dev/null
   ```
   Any file listed requires inspection for actual contact PII; confirmed contact PII is a safety blocker. It belongs in `_retained/` (gitignored), not `samples/`. (Empty/absent `samples/` → pass.)
9. CHANGELOG reference integrity — each entry's `**Reference (template implementation)**` line is what `/gtm-os-upgrade` follows to read a pattern's real implementation, so a dead path silently misdirects a future upgrade (paths have been renamed before: `eval/` → `.gtm-os/eval/`, `/upgrade` → `/gtm-upgrade`). Check only the Reference content lines (the `## Releases` index is human prose that names renamed paths on purpose — don't check it):
   - Backticked repo paths resolve to a real file/dir:
     ```bash
     # Filter gates on slash/known extension — a bare extensionless target (LICENSE,
     # Makefile) is skipped, not checked. None exists today; extend the filter if one is added.
     awk '/^\*\*Reference \(template implementation\)\*\*$/{getline; print}' CHANGELOG.md \
       | grep -oE '`[^`]+`' | tr -d '`' \
       | grep -E '/|\.(md|json|toml)$|^\.gitignore$|^\.claudeignore$' \
       | sort -u | while read -r p; do
        case "$p" in
          /[a-z]* ) [ -f ".claude/skills/${p#/}/SKILL.md" ] || echo "BROKEN SKILL: $p" ;;
          *'{'*'}'* ) echo "TEMPLATE: $p — verify against its named blueprint" ;;
          * ) [ -e "$p" ] || echo "BROKEN: $p" ;;
        esac
      done
     ```
   - `` `AGENTS.md` → "Section" `` anchors match a real heading:
     ```bash
     # Match the anchor literally (grep -qiF), never as a regex: anchors are deliberate
     # heading substrings and may contain metachars like `()`/`.`/`:` that a raw -E
     # interpolation would misread, firing a spurious finding.
     awk '/^\*\*Reference \(template implementation\)\*\*$/{getline; print}' CHANGELOG.md \
       | grep -oE '`AGENTS\.md` → "[^"]+"' | sed -E 's/.*→ "([^"]+)"/\1/' \
       | sort -u | while read -r s; do grep -E "^#{1,4} " AGENTS.md | grep -qiF "$s" || echo "NO HEADING: $s"; done
     ```
   Report unresolved `BROKEN:`, `BROKEN SKILL:` or `NO HEADING:` findings with the entry. Validate `TEMPLATE:` tokens against their blueprint; they are not literal missing paths.
10. Changelog discipline — every dev→main merge must add one CHANGELOG entry per pattern changed (`CHANGELOG.md` → "Maintainer discipline (required)"). `CHANGELOG.md` is the upgrade channel `/gtm-os-upgrade` consumes; the file-diff check in `/gtm-os-upgrade` is a backstop that catches drift, not the channel itself — a convention that ships with no entry has already broken the intended path once (`context-foundation-eviction` shipped to `main` with no CHANGELOG entry and was only caught by that backstop on a live instance). Diff what `dev` is about to merge against `main`:
   ```bash
   git diff main...dev -- AGENTS.md .claude/rules/
   ```
   Read the diff for anything that introduces or changes a **convention or pattern** (new/changed rules, blueprint sections, conventions) — as opposed to a typo, wording, or formatting fix. For each convention-bearing hunk, confirm `CHANGELOG.md` gained a corresponding entry — an `- **ID:**` slug present on `dev` but not on `main` (`git diff main...dev -- CHANGELOG.md`). A convention-bearing diff with no matching new CHANGELOG entry is a HIGH advisory finding — name the changed file/section and note that no entry covers it. Treat "convention-bearing" as a judgment call and err toward flagging; the maintainer can waive a false positive when reading the report.

Report: numbered list of issues found, with file paths and specific contradictions. If everything is clean, say "No consistency issues found." Be precise — flag real contradictions, not stylistic differences.
```

### Eval Agent Prompt

```
You are running the eval suite in an isolated worktree at {WORKTREE_PATH}.

This worktree has a populated context.md (bootstrapped from a real website). Your job: run all 8 eval tests and report results.

1. Read {WORKTREE_PATH}/.gtm-os/eval/tests.md for test definitions
2. Read {WORKTREE_PATH}/.claude/skills/run-eval/SKILL.md for the eval process
3. Scan repo state in the worktree (context.md status, demand/ contents, which modules exist)
4. Process each test case following the eval skill instructions
5. For dynamic tests (T3, T6, T7): construct domain-appropriate prompts from the populated context.md

Report: results table (test ID, name, PASS/FAIL/CRITICAL, one-line note). Then overall score.
```

## Notes

- The bootstrap agent needs web access (WebFetch) to crawl the target website
- The consistency agent is read-only — it never modifies files
- The eval agent is also read-only in practice — it evaluates behavior, doesn't execute it
- If bootstrap fails (site unreachable, context.md still empty), skip Tier 1, report bootstrap as incomplete and return REVIEW unless a safety issue independently requires BLOCKED
- Total runtime: ~3-5 minutes depending on website crawl speed
