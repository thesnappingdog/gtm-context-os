# Setup Guide

Get operational in 10 minutes.

## Requirements

- Git
- An AI coding assistant (Claude Code, Cursor, Copilot, Windsurf, or similar)
- Sales call transcripts (recordings, text transcripts, or detailed notes)

**Optional:**
- Python 3.10+ with `uv` (for eval scripts)
- MCP server access (for external integrations)

## Step 1: Clone and Open

```bash
git clone <this-repo> my-company-gtm
cd my-company-gtm
```

Open with your AI editor:
- Claude Code: `claude`
- Cursor: `cursor .`
- VS Code + Copilot: `code .`

## Step 2: Run Quickstart

**Claude Code:** Type `/quickstart`

**Other editors:** Ask "Help me get started with this GTM system" — the AI will read AGENTS.md and guide you through filling `context.md`.

This walks you through:
1. Filling in your company context (ICP, positioning, competitors)
2. Ingesting your first sales call transcript
3. Understanding how the system builds intelligence over time

## Step 3: Feed It Calls

The system gets smarter with every sales call you analyze:

**Claude Code:** `/ingest` then paste a transcript

**Other editors:** "Analyze this sales call transcript using the PULL framework" then paste

Each call produces a scored analysis in `demand/pull-analyses/`. After 5+ calls, ask for patterns.

## Step 4: Work With It

As evidence accumulates, the system supports progressively more sophisticated operations:

| After... | You can... |
|----------|-----------|
| 1 call | See PULL scoring in action |
| 5 calls | Identify demand trigger patterns |
| 10 calls | Define evidence-based segments |
| 15+ calls | Develop grounded messaging and sequences |

## Configuration (Optional)

### MCP Servers

If you use external tools and want AI access to them, create `.mcp.json`:

```json
{
  "mcpServers": {
    "your-tool": {
      "command": "npx",
      "args": ["-y", "your-mcp-server"],
      "env": {
        "API_KEY": "${YOUR_API_KEY}"
      }
    }
  }
}
```

Common integrations people add:
- Web research (for account research and competitive intel)
- CRM access (for deal and contact context)
- Pipeline tools (for table management and enrichment)

### Environment Variables

If using MCP or scripts with API keys, create `.env`:
```
# Add your API keys here
# This file is gitignored
```

## Maintenance

The system is largely self-maintaining:
- `status.md` gets appended after each work session
- JSON indexes update as you create segments, campaigns, etc.
- Module folders appear when you first need them

Periodically check:
- Is `demand/pull-index.json` in sync with the analyses? (Ask the AI to verify)
- Are old campaigns archived?
- Has `context.md` drifted from reality? (ICP evolves)
