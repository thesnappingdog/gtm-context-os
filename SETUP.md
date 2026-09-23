# Setup Guide

Get operational in 10 minutes.

## Requirements

- Git
- An AI coding assistant (Claude Code, Codex, Cursor, Copilot, Windsurf, or similar)

**Optional but recommended:**
- Sales call transcripts — the system is most powerful with real buyer conversations, but can start from a hypothesis if you don't have recordings yet

**Optional:**
- Python 3.10+ with `uv` (for API automation scripts)
- MCP server access (for external integrations)

**Not required:** No runtime, no database, no deployment. The repo IS the system.

## Step 1: Clone and Open

```bash
# Clone the repo
git clone https://github.com/thesnappingdog/gtm-context-os.git my-company-gtm
cd my-company-gtm
```

Open with your AI editor:
- Claude Code: `claude`
- Codex: `codex` (or open this repo in the Codex app/IDE extension)
- Claude Cowork: Open as a **project** from the Cowork dashboard (not a task)
- Cursor: `cursor .`
- VS Code + Copilot: `code .`

## Step 2: Bootstrap Your Context

**Fastest path (Claude Code):** Type `/bootstrap acme.com` — agents crawl your website and populate `context.md` automatically. Everything gets tagged as `[CLAIMED: website]` since marketing sites aren't ground truth.

**Guided path (Claude Code):** Type `/quickstart` for a conversational walkthrough that fills `context.md` and ingests your first sales call.

**Codex:** Use `$bootstrap acme.com` or `$quickstart`, or describe the task in natural language. These are the same skill files as Claude's, discovered through `.agents/skills`.

**Other editors:** Ask "Help me get started with this GTM system" — the AI will read AGENTS.md and guide you through filling `context.md`.

## Step 3: Feed It Calls

The system gets smarter with every sales call you analyze:

**Claude Code:** Paste a transcript and ask for a PULL analysis

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

## Claude Cowork Notes

Claude Cowork runs in an isolated Linux VM on your device. This repo is optimized for it:

- **Open as project, not task.** Tasks do not load `.claude/` configuration, skills, or rules.
- **Rules load automatically.** `.claude/rules/` provides scoped guidance — you do not need to manually reference AGENTS.md.
- **Skills work normally.** All slash commands (`/start`, `/bootstrap`, `/quickstart`, etc.) are available.
- **Hooks are not supported.** If hooks are added to the repo later, they will not execute in Cowork.
- **Start with `/start`.** Same as CLI — checks repo state and tells you what to do next.

## Configuration (Optional)

### Codex Instruction and Skill Discovery

Codex automatically loads `AGENTS.override.md`, a small guide that requires the common operating conventions and routes each task to the relevant sections of the full `AGENTS.md` handbook. Do not replace the handbook with a summary or increase the instruction budget just to load every blueprint at startup.

After cloning or upgrading, start a fresh session and ask it to name its instruction entrypoint and locate the `intake` skill. Expect `AGENTS.override.md` and `.agents/skills/intake/SKILL.md` resolving to `.claude/skills/intake/SKILL.md`. Confirm discovery in the skill picker as well; reading a file manually does not prove it was discovered. If a change has not appeared, restart the client.

The relative skill symlink is committed. On Windows or a checkout that materializes symlinks as text, restore it using supported symlink/junction facilities and re-check discovery. Preserve any existing custom skills; do not replace a real skill directory with a link blindly. A temporary fallback is asking the agent to read the canonical `SKILL.md` directly. Maintain skill edits only in `.claude/skills/`.

`release-check` and `run-probes` need isolated workers and judges, and their current harness is validated in Claude Code. Shared discovery alone does not establish equivalent execution in another client.

### MCP Servers

**Claude Code:** Run `/setup-env` to check Python/uv and scaffold a starter `.env` and `.mcp.json`, then `/setup-api <tool>` (e.g. `/setup-api hubspot`) to wire up a specific integration.

**Codex:** Use `$setup-env`, then `$setup-api <tool>`. The skill reuses existing connections or configures `.codex/config.toml` for a trusted project, preserving other settings. A Codex connection is not configured by writing `.mcp.json`. Other editors use their own MCP settings.

For manual Claude Code setup, merge the server into `.mcp.json`:

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

For manual Codex STDIO setup, merge a named table into `.codex/config.toml` (replace the example package and environment-variable name):

```toml
[mcp_servers.your_tool]
command = "npx"
args = ["-y", "your-mcp-server"]
env_vars = ["YOUR_API_KEY"]
```

Keep secret values out of tracked configuration. Both examples require the client environment to supply the named variables; a script's `.env` does not automatically populate the MCP environment. Use the server's supported OAuth flow where applicable. Reload the client's configuration and verify a real read-only tool call before calling the connection ready. See [Codex MCP](https://developers.openai.com/codex/mcp/) and [Claude MCP](https://code.claude.com/docs/en/mcp).

Common integrations people add:
- Web research (for account research and competitive intel)
- CRM access (for deal and contact context)
- Pipeline tools (for table management and enrichment)

### Push Leak Sweep

A leak sweep (`.githooks/pre-push`) blocks pushes whose outgoing commits contain secret-looking patterns (API keys, tokens, private keys) or terms you list in the gitignored `.gtm-os/sensitive-terms.txt` (customer names, codenames — one per line; the file is local by design). Activate it as a native git hook once per clone so it applies to pushes from either client or your terminal; Claude Code has an additional agent-side hook where that hook runtime is supported:

```
git config core.hooksPath .githooks
```

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
