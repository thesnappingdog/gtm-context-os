globs: engine/**

# Engine Module

Pipeline architecture, enrichment workflows, AI prompts, and integration documentation.

## Key Files

- `architecture.md` — data flow overview (sources, enrichment, qualification, routing)
- `prompts/` — AI column prompts with purpose, model, cost, input/output schema, calibration notes
- `integrations/` — per-tool API references (pre-populated with HubSpot, Gong, Fireflies, Lemlist, Clay, Apollo)

## Conventions

- Document the full data flow, not just individual tables
- Include cost estimates for enrichment steps
- Keep calibration notes when prompts are iterated
- `integrations/` ships pre-populated — when bootstrapping the engine module, keep these files
- Pipeline stage docs (scoring models, enrichment specs) live at engine root — one file per concern, flat is fine when names are descriptive
- Reference data files (JSON lookup tables, mappings) are fine at engine root — they're small and part of repo state
- Pipeline run artifacts (enrichment CSVs, scored batches, intermediate files) never go in `engine/` — they go in `_output/`
- When hardening a pipeline, keep findings in a sibling `engine/{pipeline}-dev-notes.md` (priority-ranked P0–P3, each with Status / Files / Problem / Decision / Follow-up) — not in the canonical doc. It records why fixes were made, which deferrals await evidence, and which scripts are in-pipeline vs not (the scope boundary that decides what graduates)
- `integrations/` has two doc genres: API *references* (auth, endpoints) and — when debugging a misbehaving tool — a *diagnosis* doc (dated verdict · expected vs. observed · ruled-out · hypotheses · decisive test · fix options)

---

*Source of truth: AGENTS.md, "Module: engine" section. Read it for the full blueprint and templates.*
