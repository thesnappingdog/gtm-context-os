# Integration References

Pre-shipped API references for common GTM tools. Used by `/setup-api` to scaffold connections.

Each file covers auth, key endpoints, code patterns, rate limits, and gotchas for one tool. When `/setup-api` connects a tool that has a reference here, it reads the file instead of relying on hardcoded instructions.

For unlisted tools, `/setup-api` builds a reference from the tool's API docs and saves it here.

`datastore.md` is a different genre — the skeleton for documenting an optional persistent datastore (Postgres/Supabase/warehouse) when scripts need durable state across runs. Copy it to `{datastore}.md` and fill it in; most instances never need one.
