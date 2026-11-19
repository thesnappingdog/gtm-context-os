# Gong Integration

**Integration path:** API scripts (no MCP server available)

## Authentication

- **Type:** Basic Auth (access-key as username, secret as password)
- **Where:** Company Settings → Ecosystem → API → Create API Key
- **Scopes:** `api:calls:read:basic`, `api:calls:read:extensive` (for transcripts)
- **Env vars:** `GONG_ACCESS_KEY`, `GONG_SECRET_KEY`

## Base URL

`https://api.gong.io`

## Key Endpoints

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List calls | POST | `/v2/calls` |
| Get call | GET | `/v2/calls/{id}` |
| Get transcript | POST | `/v2/calls/transcript` |
| List users | GET | `/v2/users` |

## Common Patterns

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

**Script to scaffold:** `scripts/pull-gong-transcripts.py` — pulls recent calls, writes raw transcripts to `demand/transcripts/` for analysis.

## Rate Limits

- 600 req/min
- Transcript calls count as 3

## Notes

- Call list supports date range filters (`fromDateTime`, `toDateTime`)
- Transcripts available ~30 min after call ends
- Speaker IDs map to users endpoint for internal participants
