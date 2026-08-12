# Persistent Datastore — genre reference (template)

**Optional — most instances never need this.** Markdown files + JSON indexes are the default state layer. Add a
persistent datastore only when scripts need to read/write structured state **across runs** — a cumulative account
table, scored cohorts, longitudinal metrics — that has outgrown flat files. Example vendors: a hosted Postgres
(e.g. Supabase), a warehouse. This file is the *genre skeleton*: copy it to `engine/integrations/{datastore}.md`
and fill it in. A persistent datastore is a **third `integrations/` genre**, alongside the API *reference* and the
integration *diagnosis* doc.

## Role

The durable layer scripts read/write **across runs** — keep it distinct from:
- upstream **sources** (a CRM, a warehouse you extract *from*), and
- the disposable `_output/` scratch and private `_retained/` tiers (per-run artifacts, not state).

It is infrastructure, not a run artifact: its **schema is tracked as code**; its **data is never committed**.

## Connection

| | |
|---|---|
| Host / project | `{project ref or host}` |
| Read / inspect path | `{hosted console / MCP / read-only connection — usable immediately, no stored secret}` |
| Write path | `{CLI / driver / psql via a connection string}` |
| Connection-string env var | `{STORE}_DB_URL` (in `.env`, gitignored) |
| Port note | `{pooled vs. direct — pick per workload}` |

**Dual path, staged by need.** Wire the **read/inspect** path first — query immediately, nothing to store. Defer
the **write** path — the connection string in `.env`, which the agent typically can't edit — until a script
actually needs to write state. Standing up a writable store you don't yet write to is premature.

## Common commands

```
{query}                  # run a read query
{new-migration <name>}   # create a migration file
{apply | push}           # apply pending migrations in order
{diff}                   # diff local migrations vs. the live schema
{dump}                   # dump schema for reference only — never read a dump back as live state; query the DB
```

## Schema conventions

- **Anchor every table on a stable upstream identity key**, normalized the same way on every write, so rows
  reconcile across runs. Index that key.
- **Cohort tables vs. identity tables.** A per-run cohort table carries a `run_id` / `scored_at` stamp — a re-run
  *appends a new cohort*, never overwrites. An identity-keyed table *upserts* — lifecycle state accumulates on one
  row. Decide which a table is before you create it.
- **Negative-cache tombstones.** A read-through cache table over an external lookup should upsert a tombstone row
  for a confirmed miss too, not just a hit — absence-of-row must mean "not yet fetched," never "known miss," or
  every miss gets re-paid on every run. See AGENTS.md "Module: scripts" → External-data reliability.
- **Raw + promoted.** Keep the full raw response in a JSON column (lose nothing) and promote the scalars you
  actually query into typed columns.
- **Security posture.** Document row-level security on/off, and gate it before exposing any client-side key.

## Migrations — tracked schema-as-code

Schema changes live as ordered, version-stamped DDL files in a migrations directory,
`{version-or-timestamp}_{verb-noun}.sql`, applied in order, each with a header comment (purpose · grain · key ·
where it fits the pipeline). Two load-bearing rules:

1. **Migration files are *tracked*** — the opposite of the gitignored `_output/` / `_retained/` *data* tiers. The
   data never commits; the schema definition always does.
2. **Never hand-edit the live schema without a matching migration**, or schema-diff drifts. If the apply path
   stamps its own version IDs, rename local files to match so `diff` / `list` stay clean.

Where migrations live depends on who owns the store — see "When this graduates."

## Dev-notes

Track open hardening items (a deferred RLS decision, secrets the operator must add to `.env`, a normalization a
future writer must honor) in a sibling `engine/{datastore}-dev-notes.md`, using the priority-ranked dev-notes
genre (see AGENTS.md "Module: engine").

## When this graduates → `workflows/`

A datastore does **not** by itself make you a workflow — only being scheduled/deployed does (re-apply the
graduation test). Until then the store is `scripts/`-tier and its migrations live in a top-level
`{datastore}/migrations/` directory (a project-wide store many scripts may share). On graduation: a store a single
workflow *owns* moves its schema/migration docs into that workflow's directory; a store *shared* across scripts
stays at root, and its connection reference stays here in `engine/integrations/`.
