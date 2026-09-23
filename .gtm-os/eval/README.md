# Eval Suite

Tests that handbook instructions produce correct agent behavior. Tier 1 runs in Codex or Claude Code with no separate API key or external dependencies.

## Running

**Claude Code:** `/run-eval` (all tests) or `/run-eval T3` (specific test) — Tier 1. For Tier 3, `/run-probes` (all scenarios) or `/run-probes G1`; both run as part of `/release-check`.

**Codex:** `$run-eval` (all tests) or `$run-eval T3` (specific test), after loading the handbook sections required by `AGENTS.override.md`.

**Other editors:** Ask "Run the eval suite in .gtm-os/eval/tests.md against the current repo state" — Tier 1 only. The probes' current execution harness is validated in Claude Code; another runtime must preserve worker/judge isolation and run the assertions before claiming equivalent coverage. Tier 1 does not prove automatic instruction or skill discovery; check fresh client loading separately as described in `SETUP.md`.

## Tiers

| Tier | What it does | Where |
|------|-------------|-------|
| 1 — behavioral | Asks what the agent *would* do and grades the described response | `tests.md` (T1–T8), via `/run-eval` |
| 2 — structural | Inspects the repo as-is for invariant violations | the consistency agent in `/release-check` |
| 3 — execution probes | *Runs* the agent in a seeded worktree; checks actual outputs and changes, including untracked/ignored files where specified | `scenarios/*.md` (G1–G7), via `/run-probes` |

Tier 1 is blind to conventions that only manifest as side effects of doing the work (an index row appearing, a file landing in the right tier, a threshold-triggered offer firing) — that's what Tier 3 exists for. Tier 3 is slow and runs as a `/release-check` gate, not on every instruction change.

## Execution scenarios

| ID | Behavior under test | Required result |
|----|---------------------|-----------------|
| G1 | PULL analysis/index consistency | Real analysis plus matching index entry |
| G2 | Synthesis threshold | Offer synthesis when the threshold is reached |
| G3 | Script-chain graduation | Propose the process package at the structural boundary |
| G4 | One harmless exception among 100 rows | Deliver 99 valid rows; report the exclusion without extra engineering |
| G5 | Stored qualification disagrees with current policy | Apply current policy; preserve historical flags rather than treating them as truth or a repair queue |
| G6 | Many failed records belong to older runs | Deliver the current 25 accounts; do not launch historical repair work |
| G7 | One suppressed account violates the export contract | Correct narrowly or block with evidence; do not dismiss consequential errors as a small minority |

G4–G7 test **bounded delivery and engineering judgment**, not production readiness or elimination
of every application defect. The operator asks for a business result, not "avoid overengineering."
Fixtures make impact and provenance explicit; they do not encode a universal acceptable failure
percentage. G7 is the control against teaching blanket inaction or tolerance of consequential errors.

Shared fixture support lives in `fixtures/restraint.py`. `/run-probes` copies it outside the worker
worktree and keeps seed baselines/expected outputs there. The assertions check actual delivery,
unchanged store/policy/code, unexpected new files and directories, and append-only status updates.
A fresh Judge evaluates only the listed reporting/stop conditions. No external APIs or credentials
are needed. A single passing run is a smoke signal, not proof that the template alone caused the behavior.

## Test Cases

See `tests.md` for the full list. Summary:

| ID | Tests | Pass Criteria | Critical Fail |
|----|-------|---------------|---------------|
| T1 | "What is this repo?" | Mentions demand/PULL, describes as working system | Describes as wiki or code project |
| T2 | "Where to put a call analysis?" | Points to demand/pull-analyses/ | Points to wrong directory |
| T3 | Segment creation (dynamic — persona from context.md) | Checks for PULL evidence first | Creates segment without evidence |
| T4 | "Start content work" | Bootstraps content/ from blueprint incl. topics.md | Creates arbitrary structure |
| T5 | "What's our ICP?" | Reads context.md, notes if unfilled | Invents company details |
| T6 | Sequence drafting (dynamic — persona from context.md) | Checks prerequisites (segments, messaging) | Drafts without evidence chain |
| T7 | Call analysis (dynamic — built from context.md) | Applies PULL, identifies project/urgency/alternatives/gaps, attributes claims by confidence | Doesn't recognize as demand analysis |
| T8 | "Show GTM status" | Reads status + modules, suggests next steps | Reports nonexistent modules |

## How It Works

The eval runs inside your AI editor session. The AI processes each test prompt against the actual repo state, checks its response against the criteria, and reports honestly.

**Self-evaluation tradeoff:** The same model grades itself. This is fine for regression testing (routing, evidence checks, file operations) but not for subjective quality. If you need independent evaluation, have a second person review the results.

## Results

Results are logged to `.gtm-os/eval/results.md` after each run.

## Adding Tests

Add test cases to `tests.md` following the existing format. Good tests target specific instruction behaviors:
- File routing (where does X go?)
- Evidence chain enforcement (does it check prerequisites?)
- Module bootstrapping (does it follow the blueprint?)
- Prerequisite checks (does it refuse to skip steps?)

Bad tests target subjective quality ("is the response helpful?").

When a test fails, fix the instructions (AGENTS.md or skill files), not the test — unless the test is wrong.
