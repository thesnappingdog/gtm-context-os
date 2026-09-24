---
paths:
  - "engine/**"
---

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
- Pipeline run artifacts (enrichment CSVs, scored batches, intermediate files) never go in `engine/` — they go in `_output/` (disposable scratch). A representative, PII-safe output worth keeping graduates to `samples/`; a full or PII-bearing dataset goes in `_retained/` (logged in its manifest) or an external store — never committed. See AGENTS.md "Pipeline Artifacts and Output"
- **Rejected output must not remain ready.** A delivery-contract violation in this run’s generated export requires moving it off the requested ready path to a clearly blocked sibling (for example, `export.csv` → `export.blocked.csv`, without overwriting evidence), or an authorized bounded fix followed by regeneration and verification. A blocked reply alone is insufficient. This disposition is part of the requested validation within existing write authority; preserve source data, policy and unrelated prior artifacts. See AGENTS.md "Pipeline Artifacts and Output".
- When hardening a pipeline, keep findings in a sibling `engine/{pipeline}-dev-notes.md` (priority-ranked P0–P3, each with Status / Files / Problem / Decision/Fix / Follow-up) — not in the canonical doc. It records why fixes were made, which deferrals await evidence, and which scripts are in-pipeline vs not (the scope boundary that decides what graduates)
- `engine/{process}/` holds the policy a process decides with — gate, select, optional rank profile, classification prompt — as small JSON/MD files with a provenance `_comment`. **Operator-owned**: code produces the signal, policy decides whether it qualifies; never edit policy to make code convenient. Change protocol: smallest edit, only the policy surface, zero-cost proof (delete the stage output downstream of the knob, rerun at ceiling 0), one commit naming the knob, stop. Not a rules language — overflow goes into two pure functions in the pipeline. Yield is not a policy signal: a thin run is cohort supply, not a reason to loosen a gate
- `integrations/` has two doc genres: API *references* (auth, endpoints) and — when debugging a misbehaving tool — a *diagnosis* doc (dated verdict · expected vs. observed · ruled-out · hypotheses · decisive test · fix options)
- **Run records** are the third `engine/` doc genre beside dev-notes and diagnoses: `engine/records/{date}-{pipeline}-{run-id}.md` — identities + input/output hashes + reproduction command · spend vs. ceiling · what broke · fixed-live vs. deferred · the stop boundary · measurements labelled known/derived/unknown. A doc *about* a run, not an artifact of it (those stay in `_output/`). Write one for any run that spent money, broke, or changed a decision
- A persistent datastore is an optional third `integrations/` genre — when scripts need durable state across runs, document it as `integrations/{datastore}.md` (role · connection · read-vs-write path · schema conventions · migrations). Schema is tracked as version-stamped DDL migrations (in a top-level `{datastore}/migrations/` while scripts-tier); data is never committed; a datastore alone doesn't trigger graduation. Workflow state is files (one dir per run, one file per stage, skip-if-exists); the store holds paid payloads and decisions only, with zero SQL logic. See AGENTS.md "Module: engine" + `engine/integrations/datastore.md`

---

*Source of truth: AGENTS.md, "Module: engine" section. Read it for the full blueprint and templates.*
