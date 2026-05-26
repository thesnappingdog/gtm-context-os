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
Add to `.mcp.json`:
```json
{
  "{tool}": {
    "command": "npx",
    "args": ["-y", "{mcp-package-name}"],
    "env": {
      "{TOOL}_API_KEY": "${.env key name}"
    }
  }
}
```

**If script needed:**
Bootstrap `scripts/` module if it doesn't exist (use AGENTS.md blueprint). Create a script at `scripts/pull-{tool}-{data}.py` using the inline dependency pattern:

```python
# /// script
# requires-python = ">=3.10"
# dependencies = ["requests", "python-dotenv"]
# ///
```

The script should:
- Read credentials from `.env`
- Pull data from the API
- Write output to the appropriate location (transcripts → `demand/pull-analyses/`, metrics → `campaigns/results.json`, contacts → a CSV or directly to a target tool)
- Be runnable with `uv run scripts/{name}.py`

### Step 5: Validate

Test the connection:
- If MCP: confirm server starts and can make a basic read
- If script: run it and confirm data comes back
- If auth fails: diagnose (wrong key format, missing scopes, expired token)

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
