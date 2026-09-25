---
name: setup-env
description: "Check and set up base technical environment — Python, uv, credentials, shared skill discovery, and the active client's MCP configuration. Use when repo is freshly cloned or operator hits a missing-tool error."
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
| MCP configuration | Identify active client and existing project/user connections | Claude Code: `.mcp.json`; Codex: `.codex/config.toml` or existing user configuration; report configured vs connected separately |
| Shared skills | Resolve `.agents/skills` and enumerate `*/SKILL.md` | Same canonical files as `.claude/skills/`; report a broken/plain-text link rather than silently creating a second skill tree |
| Codex instructions (if used) | Check `AGENTS.override.md` exists and points to the handbook | Small loader present; full `AGENTS.md` remains available for explicit reads |
| git | `git --version` | Should always exist |

### Step 2: Install Missing Basics

| Tool | macOS | Windows | Linux |
|------|-------|---------|-------|
| Python | `brew install python@3.12` | `winget install Python.Python.3.12` | `sudo apt install python3.12` or equivalent |
| uv | `curl -LsSf https://astral.sh/uv/install.sh \| sh` | `winget install astral-sh.uv` | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Node/npx (if MCP servers wanted) | `brew install node` | `winget install OpenJS.NodeJS.LTS` | `curl -fsSL https://fnm.vercel.app/install \| bash && fnm install --lts` |

uv needs no project-level config — scripts use inline `# /// script` metadata.

**Windows notes:** an MCP server config that launches via `npx` must use `cmd /c npx ...` as the command — Windows resolves `npx` to a `.cmd` shim that process-spawn can't invoke directly, and the server fails silently otherwise. Line endings are handled by the repo's `.gitattributes` (LF-normalized on checkout) — don't set `core.autocrlf` locally, it will fight the repo setting.

### Step 3: Create .env

If `.env` doesn't exist, create from `.env.example`:
```bash
cp .env.example .env
```

Tell the user: "Add your API keys to `.env` as you connect tools. Use `/setup-api` to set up specific integrations."

### Step 4: Prepare the Active Client's MCP Configuration

If `.mcp.json` doesn't exist and user is on Claude Code, create a starter:
```json
{
  "mcpServers": {}
}
```

Tell the user: "MCP servers will be added here as you connect tools via `/setup-api`."

For Codex, reuse existing connections and configure new project servers in `.codex/config.toml` when a concrete integration is requested via `$setup-api`; an empty Codex config is unnecessary. Preserve existing settings, and explain that project config needs project trust. Other clients use their own configuration. Do not create `.mcp.json` merely because a Codex setup was requested. The MCP client needs access to the required environment variables or OAuth credentials; creating `.env` for scripts alone does not establish that access.

If the shared skill link is broken, restore the relative `.agents/skills` → `../.claude/skills` link where supported. If the path already holds real files, inspect for custom skills before proposing a repair; never overwrite them. Where symlinks are unavailable, document a supported local link mechanism and verify discovery. Opening the canonical `SKILL.md` manually is a temporary fallback, not a successful discovery check. Codex supports `$skill-name` and natural-language invocation; Claude Code uses `/skill-name`.

### Step 5: Activate the Push Leak Sweep

Per-clone setup for the leak sweep (see AGENTS.md "Push Leak Sweep and Sensitive Terms"):

1. Inspect `git config --get core.hooksPath` first. Preserve any existing maintainer-specific hooks; do not replace a private privacy guard with the basic shared hook. Otherwise activate the native git hook: `git config core.hooksPath .githooks` (guards pushes from either client or a terminal; the extra agent-side hook in `.claude/settings.json` applies only where Claude hooks are supported). The basic shared hook checks added lines in unpublished HEAD commits, not messages, tags, other refs or already-published history; follow AGENTS.md's public-template privacy review too. Maintainer utilities remain in gitignored `.dev-tools/`.
2. If `.gtm-os/sensitive-terms.txt` doesn't exist, ask the operator: "Any names or terms that must never be pushed to this repo — customer names, codenames? I'll keep them in a local-only blocklist that blocks pushes containing them." Write one term per line. Skip the question if the repo has no remote.

### Step 6: Report

```
Environment Status:
  Python 3.12  ✓
  uv 0.6.x    ✓
  npx          ✓
  .env         ✓ (empty — add keys as you connect tools)
  MCP config   {active client, path/scope, configured/connected/not configured}
  Skills       {shared link valid; discovery verified or needs reload}

Ready to go. Use /setup-api to connect your CRM, call recorder, or other tools.
```
