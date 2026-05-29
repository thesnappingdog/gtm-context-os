---
name: pull-query
description: "Search PULL analyses by criteria to find evidence for segments. Use when searching for demand signals, conversion patterns, or buyer evidence."
argument-hint: "[query — e.g., 'scaling triggers', 'score > 15', 'would close']"
---

Query PULL analyses to find evidence for segments, messaging, or pattern recognition.

## Process

### Step 1: Load Index

Read `demand/pull-index.json`.

If missing or empty: "No PULL analyses indexed yet. Paste a sales call transcript and I'll run a PULL analysis to start building the evidence layer."

### Step 2: Parse Query

Accept natural language or structured filters:

**Natural language:**
- "Show me all demand calls"
- "Find calls where they mentioned scaling"
- "Who would close?"
- "Calls with score above 15"

**Structured filters:**
```
classification = demand
primary_trigger = scaling_team
pull_score >= 15
buyer_type = vp_engineering
would_close = yes
features_resonated contains integration
```

Multiple conditions use AND logic.

### Step 3: Execute and Display

**Summary view (default):**
```
## Results: {count} analyses matching "{query}"

| Company | Prospect | Score | Trigger | Would Close |
|---------|----------|-------|---------|-------------|
| {co} | {name} | {X}/20 | {trigger} | {yes/no} |

Avg Score: {avg}/20
```

**Detailed view (if few results or requested):**
Include full analysis metadata per result.

### Step 4: Aggregation Queries

Support "group by" for pattern analysis:

```
## By Trigger

| Trigger | Count | Avg Score | Demand % |
|---------|-------|-----------|----------|
| {trigger} | {n} | {avg} | {pct} |
```

### Step 5: Suggest Usage

After displaying results:
- If user is building a segment: "These analyses support a segment hypothesis. Want to create a segment definition?"
- If user is developing messaging: "These buyer quotes can ground your messaging angles."
- If finding patterns: "The dominant trigger is {X} — this could be your primary scenario."

## Common Patterns

- **Segment validation:** "Do we have evidence for targeting {persona}?" → filter by buyer_type
- **Messaging grounding:** "What language do buyers use about {topic}?" → read full analyses for quotes
- **Win pattern:** "What do fast buyers have in common?" → filter would_close = yes, look for patterns
- **Trigger discovery:** "Group by trigger" → find which triggers correlate with demand
