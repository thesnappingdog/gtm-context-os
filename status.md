# Status

Current phase and progress for GTM operations.

## Current Focus

[What's the primary GTM activity right now?]

## Active Work

[What modules are in use, what's running, what's being built]

## Session Log

<!-- Append entries below as work happens -->

### 2026-09-22 — Cross-client template compatibility
- Added a small Codex entrypoint that loads shared conventions and task-specific sections of the full handbook; preserved all module blueprints.
- Corrected Claude rule scoping, retained one shared skill source, and made integration setup select the active client's MCP configuration. Added adoption notes and client-loading checks to the upgrade/release guidance.
- Verified fresh Codex entrypoint and skill discovery, fresh Claude startup scoping, rule/config syntax, and the eight Tier 1 instruction cases. Full release-check and execution probes remain pending.
- Next: review the uncommitted compatibility patch before the release gate; the versioned cross-client skills package is planned as a separate near-term follow-up.

### 2026-09-23 — Isolated CLI generation experiment
- Ran a fresh builder agent against dev at `1cc8769` in an isolated local worktree, using synthetic account qualification, review and enrichment fixtures. Compared operating structure with a private reference implementation through a separate read-only review; supplied no reference code or customer data to the builder.
- Generated package, external policy and four runbooks; independently confirmed the six-credit happy path, zero-cost repeat, CRM preview without writes, eight passing tests and the unchanged complexity check.
- Additional probes reproduced blocked policy recomputation from existing evidence, permanently replayed failed paid outcomes, and partial discovery requiring manual stage deletion. A policy-only follow-up stopped honestly at the first blocker without provider calls or code edits.
- Preserved the worktree and initial generated baseline. Report retained locally outside the repository. This was a focused experiment, not a full release gate or cross-client discovery pass.
- Next: review these failure cases, clarify the affected template contracts, and regenerate against the same independent acceptance probes before adding them to the release gate.

### 2026-09-23 — Bounded-delivery regression probes
- Clarified the earlier experiment's purpose: template-guided structure and stopping judgment, not eliminating every generated-application defect. Lifecycle findings above are observations, not an instruction to harden every edge case.
- Added G4–G7 execution probes for a harmless excluded row, stale cached qualification flags, historical failed records, and a single consequential suppression violation. Shared synthetic fixtures require real output and check code, policy, store and structure preservation.
- Ran all four against isolated fresh agents on instruction baseline `1cc8769`; all passed objective assertions and separate transcript judging. The three restraint cases delivered without implementation/store changes; the control made a narrow suppression correction.
- Verified fixture positive/negative cases, protected seeding from the main checkout and existing baselines, and required Judge completion for release readiness. Corrected the control assertion to allow the handbook-required incident record/index update.
- Updated eval navigation, probe isolation guidance and the changelog. No handbook behavior rules changed; the full release check was not run.

### 2026-09-23 — Full template release check
- Tested `dev` at `1cc8769` plus the uncommitted probe changes in isolated worktrees. Verdict: NOT READY. Clay bootstrap and all eight Tier 1 cases passed; G1 and G4–G7 passed objective assertions and independent judging. G2 passed on retry with ambiguous input acceptance; G3 failed both attempts, including unapproved CLI scaffolding on retry.
- The requested restraint cases passed again: deliver 99 usable rows, apply current policy without rewriting cached flags, leave historical failures alone, and narrowly address a consequential suppression violation.
- Consistency review found a new client-specific Gong importer with inappropriate output paths and three pre-existing intake conflicts involving prerequisites, attribution and thin-note routing. The CHANGELOG reference checker also has a false positive for skill invocations.
- Corrected only G1/G3 assertion bookkeeping to compare seeded baselines. Native Codex/Claude instruction and skill discovery checks passed within their documented scope; execution probes ran in Codex, not both clients. No application or handbook fixes, commit, merge or push.
- Saved the full report and failure evidence locally outside the repository. Next: resolve the release blockers, clarify the intended process-proposal boundary and improve the ambiguous G2 fixture, without broad application hardening.

### 2026-09-23 — Privacy cleanup and dev preparation
- Removed an accidentally included instance-specific importer and its fixture inventory entry; redacted a private reference name and machine-local report paths from the development log. Original evidence remains local and outside the repository. Privacy redaction is the explicit exception to preserving the earlier log verbatim.
- Prepared a sanitized candidate from the remote dev baseline so the accidental importer is absent from outgoing history as well as the final files. Preserved the original local branch and experiment.
- Retained public authorship, license attribution, vendor documentation and fictional examples. The prior release-check failures remain open; this prepares development changes, not a main release.
