# Clay Integration

**Integration path:** API scripts (for import/export) + UI (for enrichment column configuration)

## Authentication

- **Type:** API key (Bearer token)
- **Where:** Settings → API Keys
- **Env var:** `CLAY_API_KEY`

## Base URL

`https://api.clay.com`

## Auth Header

`Authorization: Bearer {CLAY_API_KEY}`

## Key Endpoints

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Import rows | POST | `/v1/tables/{tableId}/rows` |
| Get table | GET | `/v1/tables/{tableId}` |
| List tables | GET | `/v1/tables` |
| Trigger run | POST | `/v1/tables/{tableId}/trigger` |

## Common Patterns

```python
def import_to_clay(api_key, table_id, rows):
    url = f"https://api.clay.com/v1/tables/{table_id}/rows"
    headers = {"Authorization": f"Bearer {api_key}"}
    return requests.post(url, headers=headers, json={"rows": rows})
```

## Notes

- Clay's power is in UI-configured enrichment columns (AI, waterfall, HTTP)
- API is best for: bulk imports, triggered runs, data export
- Document Clay table architecture in `engine/architecture.md`
- Webhook triggers connect Clay outputs to downstream tools
