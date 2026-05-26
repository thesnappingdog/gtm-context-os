# Status

Current phase and progress for GTM operations.

## Current Focus

[What's the primary GTM activity right now?]

## Active Work

[What modules are in use, what's running, what's being built]

## Session Log

<!-- Append entries below as work happens -->

### 2026-05-26 — Skill architecture rework
- Split environment setup into two skills: `/setup-env` (base: Python, uv, brew, .env) and `/setup-api` (connect specific tools with hardcoded references for HubSpot, Gong, Fireflies, Lemlist, Clay, Apollo)
- Removed `/ingest` skill — PULL analysis process lives in `demand/pull-framework.md`, skills are for scaffolding not methodology
- Updated CLAUDE.md skill registry
- Identified remaining gaps: importing existing knowledge, account research, results→iteration cycle, recurring ops, sharing/exporting

### 2026-05-26 — Intake skill + DECISIONS.md
- Added `/intake` skill — process raw documents into structured knowledge. Incremental, honest attribution (`[CLAIMED]` tag), gap analysis as requests not criticism
- Created `DECISIONS.md` — full build history with architecture decisions, rejections, and reasoning
- Added `_intake/` to .gitignore (source docs sensitive, only `_processed.json` tracked)
- Discussed marketing modules — leaning toward broadening campaigns/ schema + enriching content/ blueprint rather than new modules
