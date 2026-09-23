---
name: run-probes
description: "Execution probes (eval Tier 3) — run the agent for real in a seeded worktree and assert on the git diff, not on stated intent. Catches convention side-effects (index rows, file placement, threshold-triggered offers) that the single-turn eval is structurally blind to. Slow; runs as part of /release-check, or standalone on demand."
argument-hint: "[optional: scenario ID, e.g. G1 — default runs all scenarios]"
---

# Run Execution Probes

Tier 3 of the eval stack. `/run-eval` (Tier 1) asks the model what it *would* do and grades the description; the consistency check (Tier 2) inspects the repo as-is. Probes **execute**: a scripted operator turn goes to a fresh agent session in an isolated worktree running the repo's real instructions, and the scenario's assertions run against the resulting `git diff`. A convention that only manifests as a side effect of doing the work — an index row appearing, output landing in the right tier, an offer firing on a state threshold — is only checkable here.

Scenarios live in `.gtm-os/eval/scenarios/*.md`. Each has: **Seed** (bash, run in the worktree), **Turns** (scripted operator prompts), **Assert (objective)** (bash — the primary gate), optional **Assert (subjective/transcript)** (Judge), and **Forbidden** (critical fails).

Some scenarios use shared fixture helpers in `.gtm-os/eval/fixtures/`. These are test-harness
code, never agent instructions or application code. G4–G7 test bounded delivery and restraint:
use the existing tool to finish the task, interpret stored observations in context, and avoid
unrequested engineering. Their positive control requires a real contract violation to be
addressed or blocked. Do not expand these probes into application-hardening benchmarks.

## Validity discipline (non-negotiable)

Three separate contexts, so the test can't grade itself:

- **Operator** — the scripted turns from the scenario file, passed verbatim. Never improvised, never reveals assertions.
- **System-Under-Test (SUT)** — a fresh sub-agent in the seeded worktree, instructed to act as the repo's agent per the worktree's own `AGENTS.md` and rules. It sees the operator turn and nothing else — **never the scenario file, never the assertions**.
- **Judge** — you (the orchestrator) run the objective bash assertions mechanically; a fresh sub-agent judges only the subjective/transcript assertions, seeing the final diff + SUT transcript, not the SUT's context.

Assert on objective state wherever possible; the LLM-judge is for the genuinely subjective slivers only.

## Process (per scenario)

```
1. SEED    WT="/tmp/gtm-probe-{scenario}-$(date +%s)"; git worktree add "$WT" HEAD
           create a separate temporary HARNESS directory outside $WT
           copy the scenario and .gtm-os/eval/fixtures/ into HARNESS
           export PROBE_SUPPORT="$HARNESS/fixtures" PROBE_STATE="$HARNESS/state"
           remove .gtm-os/eval/ from $WT before the worker starts (it contains answers)
           run the scenario's Seed block from $WT root
           record seed changes separately from worker changes; assertions/baselines stay in HARNESS
2. RUN     spawn the SUT sub-agent (default-tier model — the model a real instance session runs):

           "You are the AI agent operating the GTM Context OS repo at {WT}.
            Read {WT}/AGENTS.md and the relevant .claude/rules/ files and follow them
            exactly as a live session would — including silent side-effect duties
            (index maintenance, file routing, startup reconciliation). Work only
            inside {WT}. Do not inspect git history, other worktrees, or test-harness
            material outside this worktree. Then handle this operator message:
            ---
            {turn text}
            ---
            Do the work for real (write the actual files), then reply to the operator
            as you would in-session."

           Capture the SUT's reply verbatim (it is the transcript for the Judge).
           Multi-turn scenarios: continue the SAME SUT agent with the next turn.
3. ASSERT  run the scenario's objective bash block from $WT root; record PASS/FAIL lines.
           Check Forbidden conditions explicitly.
           Include new/untracked and relevant ignored files; git diff alone is insufficient.
           A nonzero assertion exit or FAIL line is a failure; a missing baseline is HARNESS ERROR.
4. JUDGE   if the scenario has subjective/transcript assertions: spawn a fresh sub-agent
           with the final `git -C $WT status --porcelain`, `git -C $WT diff`, the new
           file contents named by the assertions, and the SUT reply — ask it to score
           ONLY those listed assertions PASS/FAIL with one-line reasons.
5. CLEAN   git worktree remove "$WT" --force
           remove this scenario's HARNESS directory after reporting (unless operator wants artifacts kept)
```

## Failure taxonomy (report honestly)

- **PROBE FAIL** — objective assertion failed or a Forbidden condition hit: the instructions produced a real violation. This is the signal the tier exists for.
- **JUDGE FAIL** — a listed transcript assertion failed. Report it separately from objective failures;
  a scenario with required judging cannot PASS until both objective and Judge checks pass. Missing
  required judging is an unresolved HARNESS ERROR. In particular G7's absent-output branch is not a
  pass without the Judge confirming the specific suppression finding and honest blocked delivery.
- **HARNESS ERROR** — seed didn't apply, SUT errored, worktree issue: not a verdict on the instructions. Fix the harness, rerun; never count as PASS.

Probes are single-run smoke signals, not statistics: one clean run = PASS for the gate; a FAIL is worth one rerun to rule out nondeterminism before treating it as real (two fails = real).

## Report format

```
## Probe Results — {date}

| Scenario | Objective | Judge | Verdict |
|----------|-----------|-------|---------|
| G1 …     | PASS      | PASS  | PASS    |

{per-failure: the exact assertion line that failed + the relevant diff excerpt}
```

Standalone runs: report only (never write results into repo state). Under `/release-check`: the probe verdict feeds the release verdict — any PROBE FAIL, required JUDGE FAIL, or unresolved HARNESS ERROR blocks READY.
