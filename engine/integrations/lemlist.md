# Lemlist Integration

**Integration path:** API scripts

## Authentication

- **Type:** Basic Auth (empty username, API key as password)
- **Where:** Settings → Integrations → API
- **Env var:** `LEMLIST_API_KEY`

## Base URL

`https://api.lemlist.com`

## Key Endpoints

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List campaigns | GET | `/api/campaigns` |
| Get sequences | GET | `/api/campaigns/{id}/sequences?version=v2` |
| Add step | POST | `/api/sequences/{seqId}/steps?version=v2` |
| Add lead | POST | `/api/campaigns/{id}/leads/{email}` |
| Get activities | GET | `/api/activities` |

## Common Patterns

```python
from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth("", LEMLIST_API_KEY)

def add_lead(campaign_id, email, first_name, last_name, company, **custom):
    url = f"https://api.lemlist.com/api/campaigns/{campaign_id}/leads/{email}"
    body = {"firstName": first_name, "lastName": last_name, "companyName": company, **custom}
    return requests.post(url, auth=auth, json=body)
```

## Rate Limits

- 100 req/10s

## Notes

- Always use `?version=v2` for sequence endpoints
- Cannot pull reply text via API — only `messagePreview` (first line)
- Custom variables: any key passed on lead creation becomes `{{key}}` in sequences
- LinkedIn step types: `linkedinInvite`, `linkedinSend` (DM, 1st-degree only)
