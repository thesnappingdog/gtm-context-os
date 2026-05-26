# HubSpot Integration

**Integration path:** MCP server (primary) + API scripts (for writes/bulk operations)

**MCP package:** `@anthropic/hubspot-mcp` (via npx)

## Authentication

- **Type:** Private app access token
- **Where:** Settings → Integrations → Private Apps → Create
- **Scopes:** `crm.objects.contacts.read`, `crm.objects.companies.read`, `crm.objects.deals.read`, `sales-email-read`
- **Env var:** `HUBSPOT_ACCESS_TOKEN`

## Base URL

`https://api.hubapi.com`

## Auth Header

`Authorization: Bearer {HUBSPOT_ACCESS_TOKEN}`

## Key Endpoints

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

## Search Filter Syntax

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

## Common Patterns

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

## Rate Limits

- 100 req/10s (private apps)
- Search: 4 req/s
- Batch: 100 records/req
- Pagination: all list endpoints return `paging.next.after`

## Notes

- Properties are the key abstraction — custom properties hold all business-specific data
- Association labels (v4) allow typed relationships
- Workflows are read-only via API
- Call transcripts: `hs_call_body` property on call objects
