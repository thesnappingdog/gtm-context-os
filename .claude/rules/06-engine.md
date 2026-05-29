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

---

*Source of truth: AGENTS.md, "Module: engine" section. Read it for the full blueprint and templates.*
