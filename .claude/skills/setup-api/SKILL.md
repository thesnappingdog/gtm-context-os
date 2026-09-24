---
name: setup-api
description: "Connect a specific tool — CRM, call recorder, enrichment, sequencing. Scaffolds scripts, MCP config, and integration docs. Use when operator says 'connect HubSpot' or 'I need to pull transcripts from Gong'."
argument-hint: "[tool name or category, e.g. 'hubspot', 'call recording', 'gong']"
---

Help the operator connect a specific external tool to their GTM system.

## When to Use

- User says "connect HubSpot", "set up Gong", "I need to pull transcripts"
- User names a tool category: "call recording", "CRM", "enrichment", "sequencing"
- After `/setup-env` confirms the base environment is ready

## Process

### Step 1: Identify the Tool

If user named a specific tool, proceed. If they named a category, ask which tool:

**Categories and common tools:**
- **Call recording:** Gong, Fireflies, Chorus, Zoom, Google Meet
- **CRM:** HubSpot, Salesforce, Pipedrive, Close
- **Enrichment:** Clay, Apollo, Clearbit, ZoomInfo, Exa
- **Sequencing:** Lemlist, Instantly, Smartlead, Apollo Sequences, HeyReach
- **Research:** Exa, Perplexity
- **Datastore (persistent state):** Postgres, Supabase, a hosted warehouse — for structured state scripts read/write across runs. Document it with the datastore genre (`engine/integrations/datastore.md`), not the API-reference template below; most instances never need one.

### Step 2: Load Integration Reference

Check if `engine/integrations/{tool}.md` exists. If it does, read it — it has auth details, endpoints, code patterns, and gotchas.

If it doesn't exist, use web search to find the tool's API docs. Build a reference and save it to `engine/integrations/{tool}.md` using the template in "For Unlisted Tools" below.

### Step 3: Configure Auth

Add the tool's credentials to `.env`:
```
# {Tool Name}
{TOOL}_API_KEY=
```

Tell the user exactly where to find the key (from the integration reference: which settings page, what scopes, any gotchas).

### Step 4: Set Up Integration

**If MCP server available** (noted in integration reference):
Identify the active client first. Reuse an already-connected server if it supplies the needed tools. Otherwise merge a server entry into that client's configuration, preserving unrelated entries; do not write Claude's config for a Codex session.

**Claude Code:** add the server under `mcpServers` in `.mcp.json`:
```json
{
  "mcpServers": {
    "{tool}": {
      "command": "npx",
      "args": ["-y", "{mcp-package-name}"],
      "env": {
        "{TOOL}_API_KEY": "${{TOOL}_API_KEY}"
      }
    }
  }
}
```
Use the exact environment-variable name from the integration reference in Step 2; `${{TOOL}_API_KEY}` above is a placeholder for a reference such as `${APOLLO_API_KEY}`, not a literal credential. HubSpot uses `HUBSPOT_ACCESS_TOKEN`; Gong uses `GONG_ACCESS_KEY`/`GONG_SECRET_KEY`.

**Codex:** add a named table to `.codex/config.toml` for a trusted project (or update an existing user-scoped server when that is the operator's intended scope):

```toml
[mcp_servers.example_tool]
command = "npx"
args = ["-y", "example-mcp-package"]
env_vars = ["EXAMPLE_API_KEY"]
```

Replace the example name, package and variable with the verified server contract. `env_vars` forwards named variables from the client environment; it does not contain secret values. For an HTTP server, use its documented URL/auth configuration instead of this STDIO example. Project config requires Codex project trust. Other clients use their own supported MCP configuration; check their documentation rather than assuming either format.

**Credentials:** a script's `.env` file does not automatically populate the MCP client's environment. Ensure the client can access the required variables or complete the server's supported OAuth flow, without printing secrets or embedding them in tracked config. State any remaining environment/authentication step explicitly. Client references: [Codex MCP](https://developers.openai.com/codex/mcp/), [Claude MCP](https://code.claude.com/docs/en/mcp).

**Pin fast-moving SDK dependencies.** Before committing a `uvx`/`npx`-launched MCP server entry, check whether it declares an unbounded dependency on a still-evolving SDK (e.g. `mcp>=1.0.0` with no ceiling). If so, pin it in the committed config (e.g. `--with "mcp<2"` for a `uvx` command, or the equivalent version pin for `npx`) and note why next to the pin — an unbounded transitive dependency breaks every fresh clone silently the day the SDK majors.

**If script needed:**
Bootstrap `scripts/` module if it doesn't exist (use AGENTS.md blueprint). Create a script at `scripts/pull-{tool}-{data}.py` using the standard script header (AGENTS.md "Module: scripts" — docstring + `ROOT` path anchor + inline deps):

```python
# /// script
# requires-python = ">=3.10"
# dependencies = ["requests", "python-dotenv"]
# ///
```

The script should:
- Read credentials from `.env` (env first, then `.env`; on Claude Code the key may already be in `.mcp.json`)
- Pull data from the API
- Write output to the appropriate location: repo state (transcripts → `demand/pull-analyses/`, metrics → the relevant campaign folder) goes to module folders; transient data (contact CSVs, enrichment results) goes to `_output/`
- **If it writes or spends**: apply the write-safety class from AGENTS.md "Module: scripts" — a paid enrichment/search gets a `--max-{unit}` ceiling (never a dry-run); a write into a CRM/sequencer gets `--plan` and a snapshot before overwriting; a write into a store the script owns is an idempotent upsert, no flag
- Be runnable with `uv run scripts/{name}.py`

### Step 5: Validate

Test the connection:
- If MCP: reload/restart the active client's server configuration as needed, confirm the tool is visible in that client, and make a basic read; a valid config file alone is not a connected integration
- If script: run it and confirm data comes back
- If auth fails: diagnose (wrong key format, missing scopes, expired token)
- **If MCP fails with transport error `-32000`:** this is opaque by design and usually does NOT mean auth — it means the server process died at launch (most often a dependency break). Run the server's launch command by hand in a terminal and read stderr to find the real cause.

### Step 6: Confirm

"**{Tool}** is connected:
- Auth: `.env` → `{TOOL}_API_KEY`
- Integration: {MCP server / script at scripts/{name}.py}
- Reference: `engine/integrations/{tool}.md`
- Data flows to: {where output goes}

Try it: {suggest a first command or script run}"

---

## For Unlisted Tools

If the operator names a tool without a reference in `engine/integrations/`:

1. Use web search to find the tool's API documentation
2. Determine: REST vs GraphQL, auth method, key endpoints for GTM use cases
3. Create `engine/integrations/{tool}.md` using this template:

```markdown
# {Tool Name} Integration

**Integration path:** [MCP / API scripts / CLI]

## Authentication
- **Type:** [API key / OAuth / Basic Auth]
- **Where:** [path in UI]
- **Env var:** `{TOOL}_API_KEY`

## Base URL
[URL]

## Auth Header
[Format]

## Key Endpoints
[Endpoints relevant to GTM operations]

## Common Patterns
[Code examples for typical operations]

## Rate Limits
[Limits and gotchas]

## Notes
[Quirks, tips, things that surprised you]
```

4. Scaffold a script if appropriate
5. Add env var to `.env`
