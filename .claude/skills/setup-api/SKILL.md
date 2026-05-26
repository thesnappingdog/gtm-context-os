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

### Step 2: Determine Integration Path

For the named tool, figure out the best way to connect:

1. **MCP server available?** — Best option for Claude Code users. Direct tool access, no scripts needed for reads.
2. **CLI available?** — Sometimes tools have CLI packages that simplify auth and requests.
3. **REST API** — Most common fallback. Scaffold a Python script.

Check the hardcoded references below first. For unlisted tools, use web search to find their API docs and determine the integration path.

### Step 3: Configure Auth

Add the tool's credentials to `.env`:
```
# {Tool Name}
{TOOL}_API_KEY=
```

Tell the user exactly where to find the key:
- Which settings page in the tool's UI
- What scopes or permissions to enable
- Any gotchas (e.g., "use a private app token, not an OAuth token")

### Step 4: Set Up Integration

**If MCP server available:**
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

### Step 5: Create Integration Reference Doc

Bootstrap `engine/` module if it doesn't exist (use AGENTS.md blueprint).

Create `engine/integrations/{tool}.md` with:
- Auth details (type, scopes, env var name)
- Key API endpoints the operator will need
- Common code patterns
- Rate limits and gotchas
- MCP availability note

Use the hardcoded reference if available. Otherwise, build a reference from API docs.

### Step 6: Validate

Test the connection:
- If MCP: confirm server starts and can make a basic read
- If script: run it and confirm data comes back
- If auth fails: diagnose (wrong key format, missing scopes, expired token)

### Step 7: Confirm

"**{Tool}** is connected:
- Auth: `.env` → `{TOOL}_API_KEY`
- Integration: {MCP server / script at scripts/{name}.py}
- Reference: `engine/integrations/{tool}.md`
- Data flows to: {where output goes}

Try it: {suggest a first command or script run}"

---

## Hardcoded Integration References

### HubSpot

**Integration path:** MCP server (primary) + API scripts (for writes/bulk operations)

**MCP package:** `@anthropic/hubspot-mcp` (via npx)

**Auth:**
- Type: Private app access token
- Where: Settings → Integrations → Private Apps → Create
- Scopes: `crm.objects.contacts.read`, `crm.objects.companies.read`, `crm.objects.deals.read`, `sales-email-read`
- Env var: `HUBSPOT_ACCESS_TOKEN`

**Key endpoints:**

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Search contacts | POST | `/crm/v3/objects/contacts/search` |
| Search companies | POST | `/crm/v3/objects/companies/search` |
| Search deals | POST | `/crm/v3/objects/deals/search` |
| Get contact | GET | `/crm/v3/objects/contacts/{id}` |
| Get company | GET | `/crm/v3/objects/companies/{id}` |
| List properties | GET | `/crm/v3/properties/{objectType}` |
| Get associations | GET | `/crm/v4/objects/{objectType}/{id}/associations/{toObjectType}` |
| Create contact | POST | `/crm/v3/objects/contacts` |
| Update contact | PATCH | `/crm/v3/objects/contacts/{id}` |
| List pipelines | GET | `/crm/v3/pipelines/{objectType}` |
| Get owners | GET | `/crm/v3/owners` |
| Engagements (calls) | GET | `/crm/v3/objects/calls` |
| Engagements (emails) | GET | `/crm/v3/objects/emails` |

**Base URL:** `https://api.hubapi.com`

**Auth header:** `Authorization: Bearer {HUBSPOT_ACCESS_TOKEN}`

**Search filter syntax:**
```json
{
  "filterGroups": [{
    "filters": [{
      "propertyName": "email",
      "operator": "EQ",
      "value": "user@example.com"
    }]
  }],
  "properties": ["email", "firstname", "lastname", "company"],
  "limit": 100,
  "after": 0
}
```
Operators: EQ, NEQ, GT, GTE, LT, LTE, CONTAINS_TOKEN, NOT_CONTAINS_TOKEN, HAS_PROPERTY, NOT_HAS_PROPERTY, IN

**Pagination:** All list endpoints return `paging.next.after`.

**Rate limits:** 100 req/10s (private apps), Search: 4 req/s, Batch: 100 records/req

**Common patterns:**
```python
def search_contacts(token, filters, properties):
    url = "https://api.hubapi.com/crm/v3/objects/contacts/search"
    headers = {"Authorization": f"Bearer {token}"}
    body = {"filterGroups": [{"filters": filters}], "properties": properties, "limit": 100}
    results, after = [], None
    while True:
        if after:
            body["after"] = after
        data = requests.post(url, headers=headers, json=body).json()
        results.extend(data.get("results", []))
        after = data.get("paging", {}).get("next", {}).get("after")
        if not after:
            break
    return results
```

**Notes:**
- Properties are the key abstraction — custom properties hold all business-specific data
- Association labels (v4) allow typed relationships
- Workflows are read-only via API
- Call transcripts: `hs_call_body` property on call objects

---

### Gong

**Integration path:** API scripts (no MCP server available)

**Auth:**
- Type: Basic Auth (access-key as username, secret as password)
- Where: Company Settings → Ecosystem → API → Create API Key
- Scopes: `api:calls:read:basic`, `api:calls:read:extensive` (for transcripts)
- Env vars: `GONG_ACCESS_KEY`, `GONG_SECRET_KEY`

**Key endpoints:**

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List calls | POST | `/v2/calls` |
| Get call | GET | `/v2/calls/{id}` |
| Get transcript | POST | `/v2/calls/transcript` |
| List users | GET | `/v2/users` |

**Base URL:** `https://api.gong.io`

**Pulling transcripts:**
```python
import requests, base64

def get_transcript(access_key, secret_key, call_id):
    auth = base64.b64encode(f"{access_key}:{secret_key}".encode()).decode()
    headers = {"Authorization": f"Basic {auth}"}
    body = {"filter": {"callIds": [call_id]}}
    r = requests.post("https://api.gong.io/v2/calls/transcript", headers=headers, json=body)
    return r.json()["callTranscripts"][0]["transcript"]
```

**Transcript format:** Array of monologues with `speakerId` and `sentences`. Reconstruct as speaker-labeled text for PULL analysis.

**Rate limits:** 600 req/min. Transcript calls count as 3.

**Script to scaffold:** `scripts/pull-gong-transcripts.py` — pulls recent calls, writes raw transcripts to `demand/transcripts/` for analysis.

**Notes:**
- Call list supports date range filters (`fromDateTime`, `toDateTime`)
- Transcripts available ~30 min after call ends
- Speaker IDs map to users endpoint for internal participants

---

### Fireflies

**Integration path:** API scripts (GraphQL API)

**Auth:**
- Type: API key (Bearer token)
- Where: Settings → Developer → API Keys
- Env var: `FIREFLIES_API_KEY`

**Base URL:** `https://api.fireflies.ai/graphql`

**Auth header:** `Authorization: Bearer {FIREFLIES_API_KEY}`

**Key queries:**

List transcripts:
```graphql
query {
  transcripts(limit: 10) {
    id
    title
    date
    duration
    participants
    sentences {
      speaker_name
      text
      start_time
      end_time
    }
  }
}
```

Get single transcript:
```graphql
query {
  transcript(id: "{id}") {
    title
    date
    sentences {
      speaker_name
      text
    }
    summary {
      overview
      action_items
    }
  }
}
```

**Python pattern:**
```python
import requests

def get_transcripts(api_key, limit=10):
    url = "https://api.fireflies.ai/graphql"
    headers = {"Authorization": f"Bearer {api_key}"}
    query = """query { transcripts(limit: %d) { id title date sentences { speaker_name text } } }""" % limit
    return requests.post(url, headers=headers, json={"query": query}).json()["data"]["transcripts"]
```

**Script to scaffold:** `scripts/pull-fireflies-transcripts.py` — pulls recent meetings, reconstructs as speaker-labeled text, writes to `demand/transcripts/`.

**Notes:**
- GraphQL API, not REST — all requests are POST to a single endpoint
- `sentences` array gives speaker-labeled transcript (ideal for PULL analysis)
- Free tier: 300 minutes/month of transcription
- Summary and action items are AI-generated by Fireflies — use raw sentences for PULL analysis

---

### Lemlist

**Integration path:** API scripts

**Auth:**
- Type: Basic Auth (empty username, API key as password)
- Where: Settings → Integrations → API
- Env var: `LEMLIST_API_KEY`

**Key endpoints:**

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List campaigns | GET | `/api/campaigns` |
| Get sequences | GET | `/api/campaigns/{id}/sequences?version=v2` |
| Add step | POST | `/api/sequences/{seqId}/steps?version=v2` |
| Add lead | POST | `/api/campaigns/{id}/leads/{email}` |
| Get activities | GET | `/api/activities` |

**Base URL:** `https://api.lemlist.com`

**Auth:** Basic Auth with empty username, API key as password.

**Adding leads:**
```python
from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth("", LEMLIST_API_KEY)

def add_lead(campaign_id, email, first_name, last_name, company, **custom):
    url = f"https://api.lemlist.com/api/campaigns/{campaign_id}/leads/{email}"
    body = {"firstName": first_name, "lastName": last_name, "companyName": company, **custom}
    return requests.post(url, auth=auth, json=body)
```

**Rate limits:** 100 req/10s

**Notes:**
- Always use `?version=v2` for sequence endpoints
- Cannot pull reply text via API — only `messagePreview` (first line)
- Custom variables: any key passed on lead creation becomes `{{key}}` in sequences
- LinkedIn: `linkedinInvite`, `linkedinSend` (DM, 1st-degree only)

---

### Clay

**Integration path:** API scripts (for import/export) + UI (for enrichment column configuration)

**Auth:**
- Type: API key (Bearer token)
- Where: Settings → API Keys
- Env var: `CLAY_API_KEY`

**Key endpoints:**

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Import rows | POST | `/v1/tables/{tableId}/rows` |
| Get table | GET | `/v1/tables/{tableId}` |
| List tables | GET | `/v1/tables` |
| Trigger run | POST | `/v1/tables/{tableId}/trigger` |

**Base URL:** `https://api.clay.com`

**Auth header:** `Authorization: Bearer {CLAY_API_KEY}`

**Import pattern:**
```python
def import_to_clay(api_key, table_id, rows):
    url = f"https://api.clay.com/v1/tables/{table_id}/rows"
    headers = {"Authorization": f"Bearer {api_key}"}
    return requests.post(url, headers=headers, json={"rows": rows})
```

**Notes:**
- Clay's power is in UI-configured enrichment columns (AI, waterfall, HTTP)
- API is best for: bulk imports, triggered runs, data export
- Document Clay table architecture in `engine/architecture.md`
- Webhook triggers connect Clay outputs to downstream tools

---

### Apollo

**Integration path:** API scripts

**Auth:**
- Type: API key (passed in request body)
- Where: Settings → Integrations → API
- Env var: `APOLLO_API_KEY`

**Key endpoints:**

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Search people | POST | `/v1/mixed_people/search` |
| Search companies | POST | `/v1/mixed_companies/search` |
| Enrich person | POST | `/v1/people/match` |
| Enrich company | GET | `/v1/organizations/enrich?domain={domain}` |

**Base URL:** `https://api.apollo.io`

**People search:**
```python
def search_people(api_key, titles, company_sizes):
    url = "https://api.apollo.io/v1/mixed_people/search"
    body = {
        "api_key": api_key,
        "person_titles": titles,
        "organization_num_employees_ranges": company_sizes,
        "per_page": 100
    }
    return requests.post(url, json=body).json()
```

**Notes:**
- Search doesn't consume credits until you reveal contact info
- `organization_num_employees_ranges`: `["1,10", "11,50", "51,200"]`
- `email_status` field — only use "verified" for outbound
- Also usable as Clay enrichment source via HTTP column

---

## For Unlisted Tools

If the operator names a tool not listed above:

1. Use web search to find the tool's API documentation
2. Determine: REST vs GraphQL, auth method, key endpoints for GTM use cases
3. Create `engine/integrations/{tool}.md` using this template:

```markdown
# {Tool Name} Integration

## Authentication
- **Type:** [API key / OAuth / Basic Auth]
- **Where to get it:** [path in UI]
- **Env var:** `{TOOL}_API_KEY`

## Key Endpoints
[Endpoints relevant to GTM operations]

## Base URL
[URL]

## Auth Header
[Format]

## Common Patterns
[Code examples for typical operations]

## Notes
[Rate limits, gotchas, quirks]
```

4. Scaffold a script if appropriate
5. Add env var to `.env`
