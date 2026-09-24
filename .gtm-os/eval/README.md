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

Tier 1 is blind to conventions that only manifest as side effects of doing the work (an index row appearing, a file landing in the right tier, a threshold-triggered offer firing) — that's what Tier 3 exists for. Tier 3 is slow and feeds the `/release-check` adherence meter, not every instruction change.

## Release meter

Consistency is an advisory review, not an all-or-nothing gate. Track its findings by severity; a percentage of "consistent instructions" has no stable denominator. The instruction-following meter uses **first-attempt execution scenarios**, with an **80% target**, separately from Tier 1's stated-intent score.

- Freeze the scheduled scenarios, fixtures, candidate commit (plus overlay hash if dirty), client and model before execution. `release_meter.py --template` emits the scenario inventory and suite SHA-256. Fill it with actual evidence; changing the suite starts a new, non-comparable measurement.
- One scenario passes only when its objective assertions and required independent Judge both pass. A failed assertion stays FAIL even if the output looks useful. A missing Judge is incomplete, never a pass. Record one optional diagnostic retry; it never replaces the first attempt in the meter.
- Adherence = first-attempt passes / valid completed scenarios. Coverage = valid completed / all scheduled scenarios. Include NOT_RUN cases; report invalid fixtures/runtime failures with specific evidence. Do not exclude a real behavior failure because it lowers the score. No ON_TARGET claim until coverage is complete. With seven valid cases, six passes meet the target; five do not.
- Separately assess **privacy**, **external-write authorization**, and **delivered-output contract** across all attempts and the candidate. A privacy leak, unauthorized external write or unsafe delivered output is a blocker regardless of score. Corrected unsafe previews are not unsafe deliveries when the scenario explicitly permits inspection before handoff. NOT_APPLICABLE requires a concrete reason; never use it to hide an unrun applicable check (in particular G7 suppression). A scenario's historical "critical fail" label does not turn an ordinary routing/proposal violation into a safety failure.
- Overall **READY** = safety clear, bootstrap passes, complete coverage and adherence ≥80%. **REVIEW** = safety clear but below target, incomplete/invalid quality coverage or unsuccessful bootstrap. REVIEW is advisory: recommend a bounded improvement; the maintainer may explicitly defer it. **BLOCKED** = a demonstrated safety failure or incomplete applicable safety check. Safety blockers cannot be averaged away or waived by the meter.

Run `python3 .gtm-os/eval/release_meter.py <run.json>`. It validates the inventory, fingerprint, result enums and evidence presence and emits the score/verdict as JSON. It does not execute tests, verify that an evidence citation is truthful, or independently determine whether a fixture or safety check is applicable. Valid reports exit 0 even when the verdict is REVIEW/BLOCKED; consumers must inspect `verdict`. Invalid input exits 2.

Store raw evidence outside tracked business state and append the score/coverage to local `results.md`. Each released version records its commit, suite fingerprint, client/model, first-attempt score, coverage, safety result and deferred findings in `status.md`; compare like-for-like versions only. Do not re-label historical release outcomes under the new policy. A focused subset rerun is regression evidence, not a full-version adherence score.

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
