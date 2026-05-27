# GTM Context OS

An AI-native operating system for Go-to-Market teams. Works with any AI coding assistant that reads `AGENTS.md`.

## What This Is

A git repository that serves as the shared brain for your GTM operations. AI agents read and write to it, building intelligence about your market from real sales conversations and using that evidence to drive targeting, messaging, and outbound campaigns.

**It is not** a wiki, a documentation dump, or a template you fill once and forget. It's a working system that compounds — every sales call analyzed makes future decisions better.

## How It Works

1. **Start with demand** — Ingest sales call transcripts. The system produces structured PULL analyses scoring each call for real buyer demand.
2. **Patterns emerge** — After 5+ analyses, demand triggers and buyer personas become visible.
3. **Segments form** — Group prospects by shared demand patterns, not just firmographics.
4. **Messaging grounds** — Write outreach angles using actual buyer language from calls.
5. **Campaigns execute** — Launch sequences, track results, feed learnings back.

Every layer is grounded in the one below it. No messaging without demand evidence. No campaigns without tested messaging.

## Getting Started

```bash
# Clone the repo
git clone https://github.com/thesnappingdog/gtm-context-os.git my-company-gtm
cd my-company-gtm
claude  # or open in Cursor/Copilot/Windsurf
```

Then run `/quickstart` (Claude Code) or ask "help me get started" (any editor).

See `SETUP.md` for detailed requirements and configuration.

## Structure

```
AGENTS.md              # System instructions (read by all AI editors)
context.md             # Your ICP, positioning, competitors
demand/                # PULL analyses and buyer evidence
status.md              # Operational log

# Modules (created when needed):
segments/              # Target account segments
messaging/             # Outreach angles and voice
campaigns/             # Sequences, results, tracking
engine/                # Pipeline architecture and ops
content/               # Blog, LinkedIn, marketing

.claude/               # Claude Code skills (optional power layer)
```

## Core Methodology

Built on the **Demand-First GTM Framework** and **PULL Framework** (see `demand/pull-framework.md`):

- **P**roject — There's a project on their to-do list
- **U**navoidable — That is unavoidable right now
- **L**ooking — They're actively looking at options
- **L**acking — Those options are lacking

When someone scores high on PULL, they would be weird NOT to buy. Everything else is "would benefit" — real pain but no urgency.

## Compatibility

Works with any AI coding assistant. `AGENTS.md` is the single source of truth; editor-specific pointer files redirect to it.

| Editor | How it loads instructions |
|--------|-------------------------|
| Claude Code | `AGENTS.md` + `.claude/CLAUDE.md` + skills |
| Cursor | `.cursorrules` → points to `AGENTS.md` |
| GitHub Copilot | `AGENTS.md` directly (agent mode) |
| Windsurf | `.windsurfrules.md` → points to `AGENTS.md` |
| Aider | Via `read: AGENTS.md` in config |
| Cline | Add `AGENTS.md` to context files |

Claude Code users get bonus slash commands (`/pull-query`, `/gtm-status`, `/intake`, etc.). Everyone else gets the same methodology and blueprints via AGENTS.md.

## Acknowledgments

The **PULL Framework** (Project, Unavoidable, Looking, Lacking) is the work of [Rob Snyder](https://www.linkedin.com/in/rsnyder1/). This repo operationalizes his framework for AI-native GTM — any credit for the underlying theory belongs to him.

The quickstart flow, eval harness pattern, attribution tags, and "check before you create" convention were inspired by [Jacob Dietle's](https://www.linkedin.com/in/jacob-dietle/) [context-os](https://github.com/jacob-dietle/context-os) — an open-source template for AI-native knowledge management. Different problem, overlapping patterns.

## License

MIT — see `LICENSE`.
