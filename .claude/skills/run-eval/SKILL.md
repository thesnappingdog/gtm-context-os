---
name: run-eval
description: "Run the eval suite against the current repo state. Tests whether AGENTS.md instructions produce correct behavior. No API key needed — runs inside Claude Code."
argument-hint: "[optional: T3 or T3,T7 to run specific tests]"
---

Evaluate whether the system instructions produce correct agent behavior by processing test prompts against the actual repo state.

## When to Use

- After modifying AGENTS.md, CLAUDE.md, or any skill
- After changing module blueprints or conventions
- Before committing instruction changes
- Periodic regression check

## How It Works

This eval runs inside Claude Code — no external API key or SDK needed. You process each test prompt as if the operator typed it, check your response against the criteria, and report honestly.

**Self-evaluation tradeoff:** The same model that follows the instructions also grades itself. This is acceptable for regression testing (checking whether instructions produce the right routing, evidence checks, and file operations) but not for subjective quality assessment.

## Process

### Step 1: Load Tests

Read `.gtm-os/eval/tests.md`. If a specific test was requested (e.g., `/run-eval T3`), filter to just that test. Otherwise run all.

### Step 2: Scan Repo State

Before processing tests, understand the current state — test results depend on it:

- Is `context.md` filled or still a template?
- How many PULL analyses exist in `demand/pull-analyses/`?
- Which modules are bootstrapped? (Check for `segments/`, `messaging/`, `campaigns/`, `engine/`, `content/`)
- What's in `status.md`?
- Is `pull-index.json` populated?

Record this as context for evaluation.

### Step 3: Process Each Test

For each test case:

1. **Read the prompt** from tests.md. Some tests are marked **dynamic** — they require you to construct a domain-appropriate prompt from `context.md` at eval time, with a fallback if context.md is unfilled. Follow the construction instructions in the test.
2. **Determine correct behavior** — given AGENTS.md instructions and current repo state, what should the response do? Be specific:
   - Which files would you read?
   - What actions would you take?
   - What would you tell the operator?
   - What would you refuse to do?
3. **Check against criteria:**
   - **Must**: Would your response satisfy each criterion? (All required for PASS)
   - **Must not**: Would your response trigger any of these? (Any trigger = FAIL)
   - **Critical fail**: Would your response trigger any of these? (Any trigger = CRITICAL — instructions are broken)
4. **Score:** PASS, FAIL, or CRITICAL
5. **Note reasoning** — one sentence explaining why, especially for failures

### Step 4: Report Results

Display results as a table:

```
## Eval Results — {date}

Repo state: context.md {filled|template}, {N} PULL analyses, modules: {list}

| Test | Name | Result | Notes |
|------|------|--------|-------|
| T1 | System identity | PASS | |
| T2 | File routing | PASS | |
| T3 | Evidence chain — segments | PASS | |
| T4 | Module bootstrap — content | PASS | |
| T5 | Context routing — ICP | PASS | Correctly notes context.md is template |
| T6 | Evidence chain — sequences | PASS | |
| T7 | Call analysis | PASS | |
| T8 | Status dashboard | PASS | |

**Score: 8/8 (100%)**
```

For failures, include what went wrong:
```
| T3 | Evidence chain — segments | FAIL | Would create segment without checking pull-analyses/ |
```

For critical failures, flag prominently:
```
**CRITICAL: T3 — instructions may have broken the evidence chain requirement. Check AGENTS.md "Evidence Requirements" section.**
```

### Step 5: Log Results

Append results to `.gtm-os/eval/results.md`:

```markdown
### {date} — {score}
Repo state: {summary}
Failures: {list or "none"}
```

Create `.gtm-os/eval/results.md` if it doesn't exist.

### Step 6: Suggest Fixes (if failures)

For each failure:
- Identify which instruction in AGENTS.md or which skill should prevent this
- Suggest the specific fix
- Principle: fix the instructions, not the test (unless the test is wrong)

## Evaluation Honesty Rules

- **Read actual files** before answering state-dependent questions. Don't assume context.md is a template — check.
- **Be honest about failures.** If the instructions are ambiguous enough that you'd plausibly do the wrong thing, that's a FAIL — even if you know the right answer. The eval tests instructions, not your knowledge.
- **Current repo state matters.** T5 (ICP check) should PASS differently when context.md is filled vs. template. Evaluate against reality.
- **Don't grade on intent.** "I would probably mention evidence" is not a PASS for "must check for PULL evidence." Either the instructions clearly direct you to check, or they don't.

## Adding Tests

Add new test cases to `.gtm-os/eval/tests.md` following the existing format. Each test needs:
- A prompt (what the operator types)
- Must criteria (all required for PASS)
- Must not criteria (any = FAIL)
- Critical fail criteria (any = broken instructions)

Good tests target specific instruction behaviors: routing, evidence chains, module bootstrapping, prerequisite checks. Bad tests target subjective quality ("is the response helpful?").
