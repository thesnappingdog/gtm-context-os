---
name: setup-env
description: "Check and set up base technical environment — Python, uv, .env, .mcp.json. Use when repo is freshly cloned or operator hits a missing-tool error."
---

Check and bootstrap the base technical environment for this GTM system.

## When to Use

- Repo was just cloned and operator wants to run scripts
- User hits "uv not found", "python not found", or similar
- User says "set up my environment" or "check my setup"
- Before first use of any script or API integration

## Process

### Step 1: Audit

Run these checks silently, report results as a status table:

| Check | Command | What to look for |
|-------|---------|-----------------|
| Python | `python3 --version` | 3.10+ |
| uv | `uv --version` | Any version |
| Homebrew (macOS) | `which brew` | Present if macOS |
| Node/npx | `npx --version` | Needed for MCP servers |
| .env | Check file exists | Has content beyond comments |
| .mcp.json | Check file exists | Has server configs |
| git | `git --version` | Should always exist |

### Step 2: Install Missing Basics

**Python** (if missing):
- macOS: `brew install python@3.12`
- Linux: `sudo apt install python3.12` or equivalent

**uv** (if missing):
- `curl -LsSf https://astral.sh/uv/install.sh | sh`
- No project-level config needed — scripts use inline `# /// script` metadata

**Node/npx** (if missing and MCP servers are wanted):
- macOS: `brew install node`
- Or: `curl -fsSL https://fnm.vercel.app/install | bash && fnm install --lts`

### Step 3: Create .env

If `.env` doesn't exist, create from `.env.example`:
```bash
cp .env.example .env
```

Tell the user: "Add your API keys to `.env` as you connect tools. Use `/setup-api` to set up specific integrations."

### Step 4: Create .mcp.json (Claude Code users)

If `.mcp.json` doesn't exist and user is on Claude Code, create a starter:
```json
{
  "mcpServers": {}
}
```

Tell the user: "MCP servers will be added here as you connect tools via `/setup-api`."

### Step 5: Report

```
Environment Status:
  Python 3.12  ✓
  uv 0.6.x    ✓
  npx          ✓
  .env         ✓ (empty — add keys as you connect tools)
  .mcp.json    ✓ (no servers configured yet)

Ready to go. Use /setup-api to connect your CRM, call recorder, or other tools.
```
