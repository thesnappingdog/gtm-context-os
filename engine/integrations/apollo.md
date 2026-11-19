# Apollo Integration

**Integration path:** API scripts

## Authentication

- **Type:** API key (passed in request body)
- **Where:** Settings → Integrations → API
- **Env var:** `APOLLO_API_KEY`

## Base URL

`https://api.apollo.io`

## Key Endpoints

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Search people | POST | `/v1/mixed_people/search` |
| Search companies | POST | `/v1/mixed_companies/search` |
| Enrich person | POST | `/v1/people/match` |
| Enrich company | GET | `/v1/organizations/enrich?domain={domain}` |

## Common Patterns

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

## Notes

- Search doesn't consume credits until you reveal contact info
- `organization_num_employees_ranges`: `["1,10", "11,50", "51,200"]`
- `email_status` field — only use "verified" for outbound
- Also usable as Clay enrichment source via HTTP column
