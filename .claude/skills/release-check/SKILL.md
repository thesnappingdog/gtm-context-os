---
name: release-check
description: "Smoke test before merging dev to main. Bootstraps a clean worktree, runs evals, checks instruction consistency — all automated via sub-agents."
argument-hint: "[optional: URL to bootstrap with, default: clay.com]"
---

Automated release gate for merging `dev` → `main`. Runs three checks in an isolated worktree so your working copy is untouched.

## When to Use

- Before merging `dev` to `main`
- After a batch of instruction changes to verify nothing broke
- Periodic confidence check on system health

## What It Checks

| Agent | What | Needs worktree? | Depends on |
|-------|------|-----------------|------------|
| **Bootstrap** | Populates context.md from a real website in a clean worktree | Yes | Nothing |
| **Consistency** | Checks AGENTS.md against scoped rules, blueprints, Document Architecture; verifies CHANGELOG `Reference` paths + anchors resolve; PII gate on committed `samples/` | No | Nothing |
| **Eval** | Runs all 8 eval tests against the bootstrapped worktree | Yes | Bootstrap |

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
  - **Document Architecture compliance**: Do blueprint templates follow the naming and structure conventions? Are module-level overview files acknowledged correctly?
  - **Convention consistency**: Are graduation criteria consistent between scripts and workflows? Are JSON index schemas consistent between rules and AGENTS.md?
  - **Skill coherence**: Do skills reference files and modules that exist? Do they follow conventions described in AGENTS.md?
  - **Cross-references**: Do files reference other files that actually exist?
  - **PII gate on committed samples**: No contact PII may be committed under `samples/`. Run a grep over tracked files in `samples/` for contact patterns and flag any hit as CRITICAL:
    ```bash
    git ls-files 'samples/**' | xargs -r grep -lE \
      '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}|\+?[0-9][0-9 ().-]{7,}[0-9]' 2>/dev/null
    ```
    Any file listed is a likely PII leak — it belongs in `_retained/` (gitignored), not `samples/`. (Empty/absent `samples/` → pass.)
  - **CHANGELOG reference integrity**: `CHANGELOG.md` is the upgrade channel `/gtm-os-upgrade` consumes — each entry's `**Reference (template implementation)**` line points an upgrade agent at the real files behind the pattern, so a rotted path silently misdirects a future upgrade (the template has renamed paths before: `eval/` → `.gtm-os/eval/`, `/upgrade` → `/gtm-upgrade`). Scope the check to the **Reference content lines** (the line after each standalone `**Reference (template implementation)**` label) — that's the machine-followed pointer layer; the `## Releases` index above it is human prose (it names old/renamed paths on purpose) and is *not* checked. Verify both reference forms. **Backticked repo paths** must resolve to a real file or directory:
    ```bash
    # The grep filter gates on a slash or a known extension, so a bare extensionless
    # Reference target (e.g. `LICENSE`, `Makefile`) is silently skipped, not checked.
    # None exists today; if one is ever added as a Reference, extend this filter.
    awk '/^\*\*Reference \(template implementation\)\*\*$/{getline; print}' CHANGELOG.md \
      | grep -oE '`[^`]+`' | tr -d '`' \
      | grep -E '/|\.(md|json|toml)$|^\.gitignore$|^\.claudeignore$' \
      | sort -u | while read -r p; do [ -e "$p" ] || echo "BROKEN: $p"; done
    ```
    Any `BROKEN:` line is a dead reference — flag as CRITICAL with the entry it appears under. (A literal placeholder like `engine/{pipeline}-dev-notes.md` won't appear on a Reference line; if one ever does, read it as a template, not a literal path.) **AGENTS.md section anchors** — every `` `AGENTS.md` → "Section" `` anchor on a Reference line must match a real heading:
    ```bash
    # Match the anchor as a literal string against heading lines — never as a regex.
    # An anchor like `Module: engine` is a deliberate substring of its full heading; a
    # raw -E interpolation would (a) break on any anchor containing regex metachars
    # — `()`, `.`, `+`, etc. — firing a spurious CRITICAL, and (b) let an unrelated
    # heading that merely contains the text mask a real rot. grep -qiF restores the
    # intended literal contains-check.
    awk '/^\*\*Reference \(template implementation\)\*\*$/{getline; print}' CHANGELOG.md \
      | grep -oE '`AGENTS\.md` → "[^"]+"' | sed -E 's/.*→ "([^"]+)"/\1/' \
      | sort -u | while read -r s; do grep -E "^#{1,4} " AGENTS.md | grep -qiF "$s" || echo "NO HEADING: $s"; done
    ```
    Any `NO HEADING:` line means the anchor rotted (heading renamed/removed) — flag as CRITICAL with its entry. (All Reference paths and anchors resolving → pass.)
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

### Step 4: Collect and Report

Gather results from all three agents and present a unified report:

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

### Verdict
{READY / NOT READY — with specific blockers if not ready}
```

**Verdict criteria:**
- **READY**: Eval 8/8, no consistency contradictions, bootstrap completed successfully
- **NOT READY**: Any eval failure, any critical consistency issue, or bootstrap couldn't populate context.md

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
8. CHANGELOG reference integrity — each entry's `**Reference (template implementation)**` line is what `/gtm-os-upgrade` follows to read a pattern's real implementation, so a dead path silently misdirects a future upgrade (paths have been renamed before: `eval/` → `.gtm-os/eval/`, `/upgrade` → `/gtm-upgrade`). Check only the Reference content lines (the `## Releases` index is human prose that names renamed paths on purpose — don't check it):
   - Backticked repo paths resolve to a real file/dir:
     ```bash
     # Filter gates on slash/known extension — a bare extensionless target (LICENSE,
     # Makefile) is skipped, not checked. None exists today; extend the filter if one is added.
     awk '/^\*\*Reference \(template implementation\)\*\*$/{getline; print}' CHANGELOG.md \
       | grep -oE '`[^`]+`' | tr -d '`' \
       | grep -E '/|\.(md|json|toml)$|^\.gitignore$|^\.claudeignore$' \
       | sort -u | while read -r p; do [ -e "$p" ] || echo "BROKEN: $p"; done
     ```
   - `` `AGENTS.md` → "Section" `` anchors match a real heading:
     ```bash
     # Match the anchor literally (grep -qiF), never as a regex: anchors are deliberate
     # heading substrings and may contain metachars like `()`/`.`/`:` that a raw -E
     # interpolation would misread, firing a spurious CRITICAL.
     awk '/^\*\*Reference \(template implementation\)\*\*$/{getline; print}' CHANGELOG.md \
       | grep -oE '`AGENTS\.md` → "[^"]+"' | sed -E 's/.*→ "([^"]+)"/\1/' \
       | sort -u | while read -r s; do grep -E "^#{1,4} " AGENTS.md | grep -qiF "$s" || echo "NO HEADING: $s"; done
     ```
   Any `BROKEN:` or `NO HEADING:` line is CRITICAL — name the CHANGELOG entry it appears under.

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
- If bootstrap fails (site unreachable, context.md still empty), skip the eval and report the bootstrap failure as the blocker
- Total runtime: ~3-5 minutes depending on website crawl speed
