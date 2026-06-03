# GTM Context OS

An AI-native operating system for Go-to-Market teams. Works with any AI coding assistant that reads `AGENTS.md`.

## What This Is

A git repository that serves as the shared brain AND the operational backbone for your GTM. AI agents read and write to it — building intelligence from real sales conversations, then using that evidence to build pipelines, connect tools, write scripts, draft sequences, and run campaigns.

**It is not** a wiki or a documentation template. It's a working system with two modes:

**Context mode** — Build intelligence. Ingest sales calls, analyze demand, define your ICP, understand competitors and buyers. Every call analyzed makes the system smarter.

**Operational mode** — Get things done. Connect your CRM and call recorder via MCP. Write scripts that pull transcripts, enrich contacts, and push leads to sequencing tools. Build enrichment pipelines. Draft outbound sequences. Track campaign results. This is where intelligence turns into revenue.

Both modes work against the same repo. Context mode populates the evidence layer. Operational mode uses that evidence and feeds results back.

## How It Works

### Building intelligence

- **Start with demand** — Ingest sales call transcripts. The system produces structured PULL analyses scoring each call for real buyer demand.
- **Patterns emerge** — After 5+ analyses, trigger patterns, buyer personas, and competitive dynamics become visible. The system produces a quantitative synthesis and actionable key-learnings document.
- **Segments form** — Group prospects by shared demand patterns, not just firmographics.
- **Messaging grounds** — Write outreach angles using actual buyer language from calls.

### Operating on it

- **Connect your tools** — MCP servers for CRM, call recording, enrichment, pipeline tools. Scripts for anything that has an API.
- **Build pipelines** — Document data flow from sourcing through enrichment, qualification, and campaign routing in `engine/`.
- **Execute campaigns** — Launch sequences, track results, feed learnings back into demand evidence.
- **Automate what repeats** — Python scripts with `uv run` for recurring operations: transcript pulls, lead imports, metric snapshots, enrichment waterfalls.

Every layer is grounded in the one below it. No messaging without demand evidence. No campaigns without tested messaging.

## Getting Started

```bash
git clone https://github.com/thesnappingdog/gtm-context-os.git my-company-gtm
cd my-company-gtm
```

After cloning, disconnect from the template repo so your instance is fully yours:

```bash
git remote remove origin
git remote add origin <your-own-repo-url>  # optional — push to your own remote
```

Then open in your AI editor and start:

```bash
claude  # or open in Cursor/Copilot/Windsurf
```

Run `/quickstart` (Claude Code) or ask "help me get started" (any editor).

**Claude Cowork users:** Open this repo as a **project**, not a task. Cowork projects persist across sessions and load the full `.claude/` configuration (rules, skills, settings). Tasks are one-shot and miss the system context. After opening as a project, type `/start` to begin.

See `SETUP.md` for detailed requirements and configuration.

## Staying Up to Date

The template keeps evolving — new skills, conventions, and framework improvements ship over time. Because you disconnected from the template repo, your instance is fully yours: updates are **opt-in and adapted to your structure**, never force-merged over your work.

Updates ship as *patterns*, not files. The template publishes a `CHANGELOG.md` describing each change as a pattern with its rationale. To pull improvements in:

- **Claude Code:** run `/gtm-upgrade`. Your agent fetches the latest template, checks each new pattern against your actual repo, and proposes — per item — what to adopt, adapt to your layout, or skip. Changes land on a review branch and it pauses before anything destructive, so you review the diff and merge (or discard) when ready. Decisions are recorded so the next `/gtm-upgrade` only surfaces what's new. (Don't have the skill yet? Just ask the agent to *"install the gtm-upgrade skill from the template"* — one-time.)
- **Any editor:** ask *"Check the GTM Context OS template at https://github.com/thesnappingdog/gtm-context-os for new patterns and propose what applies to this repo."* Same advisory flow.

What it will **never** do: touch your content (`context.md`, `demand/`, `segments/`, …), impose the template's folder names, or change anything without your approval. The template is a source of ideas, not a remote you sync to.

## Structure

```
AGENTS.md              # System instructions (read by all AI editors)
context.md             # Your ICP, positioning, competitors
demand/                # PULL analyses, synthesis, key learnings
status.md              # Operational log

# Modules (created when needed):
segments/              # Target account segments
messaging/             # Outreach angles and voice
campaigns/             # Sequences, results, tracking
engine/                # Pipeline architecture, integrations, enrichment prompts
content/               # Blog, LinkedIn, marketing
scripts/               # API scripts, data pulls, automation
workflows/             # Production-grade automated workflows (graduated from scripts/)

samples/               # Committed, PII-safe representative outputs (golden extracts, baselines)
_output/               # Transient pipeline scratch — disposable (gitignored)
_retained/             # Durable but private full/real datasets — never committed (gitignored; manifest tracked)
.gtm-os/               # OS machinery — eval harness, upgrade ledger (editor-agnostic)
.claude/               # Claude Code skills and scoped rules
.mcp.json              # MCP server connections (CRM, enrichment, research)
.env                   # API keys (gitignored)
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
| Claude Code | `.claude/rules/` (scoped) + `.claude/CLAUDE.md` + skills |
| Claude Cowork | Same as Claude Code — open as **project**, not task |
| Cursor | `.cursorrules` → points to `AGENTS.md` |
| GitHub Copilot | `AGENTS.md` directly (agent mode) |
| Windsurf | `.windsurfrules.md` → points to `AGENTS.md` |
| Aider | Via `read: AGENTS.md` in config |
| Cline | Add `AGENTS.md` to context files |

Claude Code users get bonus slash commands (`/pull-query`, `/gtm-status`, `/intake`, `/handover`, etc.). Everyone else gets the same methodology and blueprints via AGENTS.md.

## Development

**Branching:**
- **`main`** — Stable. This is what people clone. Only receives merged PRs from `dev`.
- **`dev`** — Working branch. Iterate here, run `/run-eval` before merging to main.

**Versioning:** Date-based tags on main (`2026-05-28`, `2026-06-12`, etc.). Tagged when dev merges to main with a coherent batch of changes. No semver — the repo evolves too fast for version number semantics.

**If you cloned this and want to contribute back:** PRs welcome against `dev`.

## Acknowledgments

The **PULL Framework** (Project, Unavoidable, Looking, Lacking) is the work of [Rob Snyder](https://www.linkedin.com/in/rsnyder1/). This repo operationalizes his framework for AI-native GTM — any credit for the underlying theory belongs to him.

The quickstart flow, eval harness pattern, attribution tags, and "check before you create" convention were inspired by [Jacob Dietle's](https://www.linkedin.com/in/jacob-dietle/) [context-os](https://github.com/jacob-dietle/context-os) — an open-source template for AI-native knowledge management. Different problem, overlapping patterns.

## License

MIT — see `LICENSE`.
