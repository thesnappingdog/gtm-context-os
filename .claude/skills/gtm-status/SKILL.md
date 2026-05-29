---
name: gtm-status
description: "Dashboard of current GTM state across all active modules. Use when user asks about status, progress, or what to do next."
---

Show the current GTM state as a dashboard with actionable next steps.

## Process

### Step 1: Scan Active Modules

Check which modules exist (have been bootstrapped):
- `demand/` — always present
- `segments/` — if exists, read `segments.json`
- `messaging/` — if exists, read `messaging.json`
- `campaigns/` — if exists, read `campaigns.json`
- `engine/` — if exists, note it
- `content/` — if exists, note it

Also read:
- `context.md` — is it filled or still template?
- `status.md` — last entry date

### Step 2: Display Core Status

```
## GTM Context OS — Status

**Context:** {filled | template — needs /quickstart}
**Last session:** {date from status.md}
**Active modules:** {list}
```

### Step 3: Demand Layer

```
## Demand Evidence

| Metric | Value |
|--------|-------|
| PULL analyses | {count} |
| Demand (14+) | {count} |
| Benefit (8-13) | {count} |
| Neither (<8) | {count} |
| Avg PULL score | {avg}/20 |

Top demand signals:
- {company} ({score}/20) — {trigger}
- {company} ({score}/20) — {trigger}
```

If no analyses exist: "No demand evidence yet. Paste a sales call transcript and I'll run a PULL analysis to start building the evidence layer."

### Step 4: Module Dashboards (if they exist)

**Segments:**
```
## Segments

| Segment | Status | Volume | Evidence | Campaigns |
|---------|--------|--------|----------|-----------|
| {name} | {status} | {vol} | {count} analyses | {count} |
```

Flag: segments without PULL evidence, stale segments (active but no campaign in 30+ days)

**Campaigns:**
```
## Campaigns

| Campaign | Segment | Status | Sent | Replies | Meetings |
|----------|---------|--------|------|---------|----------|
| {name} | {segment} | {status} | {n} | {n} | {n} |
```

Flag: draft campaigns ready to launch, running campaigns without recent results

**Messaging:**
```
## Messaging

| Angle | Segment | Status | Campaigns Using |
|-------|---------|--------|-----------------|
| {name} | {segment} | {status} | {count} |
```

### Step 5: Recommendations

Based on current state, suggest 1-3 specific next actions:

```
## Recommended Next Steps

1. **{action}** — {why}
2. **{action}** — {why}
```

Common recommendations:
- If no analyses: "Ingest sales calls to build demand evidence"
- If analyses but no segments: "Enough evidence to identify your first segment"
- If segments but no messaging: "Develop messaging angles for active segments"
- If messaging but no campaigns: "Draft sequences for tested angles"
- If campaigns running without results: "Pull campaign metrics to track performance"
- If segments lack evidence: "Link PULL analyses to segments or run more calls"

### Step 6: Consistency Checks (silent, only surface issues)

- Segments referencing PULL analyses that don't exist in the index
- Campaigns referencing segments that don't exist
- Results for campaigns that aren't in campaigns.json
- Stale status.md (>7 days since last entry)

If issues found, add a brief section:
```
## Attention Needed
- {issue and suggested fix}
```
