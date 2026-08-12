# GTM Context OS

This is a single-company GTM operating system. You are an AI agent helping GTM operators — sales leaders, RevOps, marketers, GTM engineers — do their work. The repo is the shared brain; you operate against it.

## Two Modes of Operation

This system operates in two modes simultaneously:

**Context mode** — Build and maintain intelligence about your market. Ingest sales calls, analyze demand, define ICP, understand competitors and buyers. This is the foundation everything else builds on.

**Operational mode** — Get things done. Draft outbound sequences, build enrichment pipelines, pull campaign metrics, import leads, run scripts against external APIs. This is where intelligence turns into action.

Both modes read and write to the same repo. Context mode populates the evidence layer. Operational mode uses that evidence to execute and feeds results back. They reinforce each other.

You should be equally capable in both modes. When the operator is building understanding, help them analyze and synthesize. When they're executing, help them script, automate, and ship.

## How This System Works

**Core files** are always present and form the foundation. **Modules** materialize from blueprints below when an operator first needs them. Never create module folders preemptively — only bootstrap them when the work demands it.

When an operator asks you to do something that requires a module that doesn't exist yet, tell them you'll set it up, create the structure from the blueprint, and proceed with their task. Don't ask permission to create the structure — just do it and confirm what you created.

No external runtime, database, or deployment is required. The repo IS the system. AI operates on files. Scripts run locally when needed for API integrations.

### Works in any agent, not just Claude Code

This file is the agent-agnostic brain — Codex and other AGENTS.md-reading agents get the full system from it directly. The `.claude/` directory is the Claude Code layer: scoped rules (auto-loaded excerpts of this file — Claude Code convenience, never new content) and skills. Skills are shared across agents via the `.agents/skills` symlink → `.claude/skills` (the cross-agent SKILL.md standard location; Codex invokes them with `$skill-name` or auto-triggers on description match). `.claude/skills/` stays the canonical home — edit skills there, never through the mirror. Caveat: skills that orchestrate parallel sub-agents (`/bootstrap`, `/release-check`, `/run-eval`) are built on Claude Code's agent runtime and should be run there; single-thread skills (analysis, drafting, intake) work anywhere.

### Roles and write authority

By default this system assumes a single operator, which is why rules like JSON-index reconciliation default to "fix drift silently" — the session that reads a file is assumed to be the session authorized to write it. When a second human joins the instance as a restricted contributor, don't edit base rules to carve out their role. Instead add a separate, later-loading scoped rule file (e.g. `.claude/rules/NN-contributor-mode.md`, `globs: *`) that determines the session's role early and overrides specific base-rule behaviors for the restricted role, short-circuiting immediately for the privileged role. Role detection: a gitignored marker file wins; fall back to VCS identity (`git config user.email`); unknown identity defaults to least privilege. This keeps base rules universal and upgrade-friendly — template updates to base rules never collide with instance-specific role carve-outs, because the carve-outs live in a separate file.

## Core Files (Always Present)

| File | Purpose | When to read |
|------|---------|-------------|
| `context.md` | Business understanding — ICP, positioning, competitors, product, buying patterns. Durable strategy only; volatile operational data (rosters, IDs, scripts) lives in its module — see *Context Foundation* below | Every session. This is the foundation. |
| `demand/` | PULL analyses, research evidence, buyer insights, synthesis | When analyzing calls, qualifying demand, grounding decisions in evidence |
| `status.md` | Operational log — decisions, progress, next steps | Start of every session (check what happened last). End of every substantive session (append what happened). |
| `demand/pull-framework.md` | The PULL methodology for analyzing demand | When running demand analysis or ingesting sales call transcripts |

## Operational Conventions

### Attribution

Tag claims and insights by confidence level:
- `[VERIFIED: {source}]` — Directly supported by evidence (transcript quote, data point, metric)
- `[CLAIMED: {source}]` — Asserted by the company about itself (website, pitch deck, playbook) — useful context, not yet independently confirmed. **Promotable:** becomes `[VERIFIED]` when demand evidence or data confirms it. Not a judgment — it records *who said it and that it's unconfirmed*, not that it's doubtful.
- `[INFERRED: from {X} + {Y}]` — Derived from combining multiple sources
- `[UNVERIFIABLE]` — Judgment call, hypothesis, or assumption that *can never* be confirmed from available data. Distinct from `[CLAIMED]`: a claim is confirmable-but-unconfirmed and promotes; unverifiable is terminal.

`[CLAIMED]` is provenance (the company's own assertion), the other three are confidence — that's why a claim can be both made and later verified. The natural lifecycle is `[CLAIMED]` → `[VERIFIED]` once buyer evidence or data confirms it (this is what `/bootstrap` and `/intake` produce when seeding `context.md` from marketing material).

Use attribution in PULL analyses, segment rationale, and messaging angles. Don't use it in status logs or operational notes.

**Freshness is a separate axis from confidence.** `[VERIFIED]` says *this was true* — it never says *as of when*. A claim can be verified and badly stale: prices, headcounts, CRM IDs, and "currently/now" statements rot while the tag still reads VERIFIED. So date the claims that age:

- `[VERIFIED: pricing docs · 2026-05]` — the date is **as-of / last-confirmed**, not valid-until. It records when the claim was last checked true. An as-of date never becomes false; it just gets old — and "old" is exactly the signal you want. Don't fabricate a date you don't have: an undated `[VERIFIED]` is honest, and is a prompt to confirm-and-date the next time you touch it.
- For sections that rot fast (rosters, pricing, anything live-sourced), add a section-level marker: `_Volatile — re-verify quarterly._` (use the real cadence). It tells the next agent what to re-check first.

A fact can be high-confidence *and* stale. Treat an old date on a volatile claim as a re-verify trigger, not a guarantee.

### Context Foundation: keep it strategic, evict the operational

`context.md` is the **foundation** — read every session. It should hold durable, slow-changing strategy: company, product, ICP, positioning, competitors, disqualification rules, buying patterns. Over time it tends to *absorb* operational data that belongs elsewhere (rosters with CRM owner IDs, raw message verbatims, discovery scripts, current-project scope). That data rots fast and dilutes the foundation — and when a fact is updated in one place but its copy is left behind, the file starts to contradict itself.

**Principle: don't fragment the foundation — evict the non-foundation.** Do *not* split `context.md` into `icp.md` / `positioning.md` / etc.: those belong together and should load together every session, so chunking the foundation is pure cost. Instead move *volatile, operational* content out to the module that owns it, and leave a pointer behind. Size is not the trigger — a 14k-char `context.md` is ~3.5k tokens, trivial to read. Altitude and freshness are the triggers.

**The altitude test** — for any block in `context.md`, ask:
- Does it change on a faster clock than the surrounding strategy? (a roster shifts monthly; positioning yearly)
- Is its source of truth a live system or another module? (CRM owner IDs come from the API; message language comes from `demand/`)
- Is it consulted only in specific tasks, not every session? (discovery scripts, owner IDs)

If yes, it's operational — evict it. **Foundation stays; operational leaves.** This is instance-dependent, not a fixed list: for a 3-person founder-led company the sales roster genuinely *is* foundational. Judge by volatility and source-of-truth.

**The eviction procedure** (an instance can run this itself):
1. Identify the operational block and its right home **in this instance's structure** — don't assume folder names; some instances have no `engine/`, some put discovery questions in `demand/` vs `messaging/`.
2. Move it there intact, with its attribution.
3. **Leave a one-line pointer in `context.md`** naming the new location and the source of truth — e.g. "Seller roster + CRM owner IDs: `engine/seller-roster.md` (live-sourced from the CRM API)." The pointer is mandatory: `context.md` is the guaranteed-read file, so an agent doing the task must be able to reach the evicted data from there. Eviction without a pointer trades a freshness problem for a discoverability problem.
4. If the evicted data is live-sourced, say so where it lands ("source of truth is the API; this is a cached snapshot").

**Conflict & freshness check** (run periodically — `/gtm-os-health` automates it). Scan `context.md` for:
- **(a) Conflicts** — two statements that disagree about the same fact: a headcount stated twice with different numbers, a value prop that contradicts a product rule. This is the real payload — it catches the contradictions a growing file accretes.
- **(b) Cached-vs-source drift** — where a pointer names a source of truth (e.g. "source of truth: `demand/synthesis.md`", "live-sourced from the CRM API"), check the cached values still match it. The pointer tells you exactly what to diff, so this lens is reliable, not guesswork.
- **(c) Age** — dated claims listed oldest-first, so the eye lands on the most likely-stale.

**Surface (a) and (b) to the operator to adjudicate — never silently pick a winner**, since the "current" value is ground truth only the operator holds. For (c) there is **no expiry rule**: only *dated* claims are considered (dating is the opt-in decay signal — undated facts are never flagged), age is shown, and the operator judges whether it's stale. Don't try to decide per-fact when something becomes obsolete.

### Status Logging

Append to `status.md` at the end of any substantive work session:

```markdown
### YYYY-MM-DD — [brief description]
- What was done
- Decisions made (and why)
- Next steps
```

Don't log quick Q&A. Don't create separate log files. Always append, never overwrite.

**Footnote, don't rewrite.** `status.md` entries are point-in-time records — once written, a past entry is never edited to match later reality. If a later session learns something that corrects an earlier entry, the correction goes in the *new* entry, pointing back to the one it corrects. The old entry stays as written, wrong-at-the-time-if-so and all.

**Rotation.** `status.md` is append-only and will otherwise grow without bound. When a period is clearly closed (a quarter, a completed project phase), roll its entries verbatim into `archive/status-{period}.md` and leave one summary line + pointer at the top of the rolled section's place. Only roll clearly-closed periods — recent entries stay in `status.md` so the file every session reads stays small.

### JSON Indexes — AI-Maintained Infrastructure

JSON index files (e.g., `segments.json`, `campaigns.json`, `pull-index.json`) are **your internal navigation system**. They exist so you can quickly trace relationships between entities without re-reading every markdown file.

**Design principles:**
- **You create and maintain these.** The operator never edits or reads them directly.
- **Update them automatically** as a side effect of work — when you create a segment markdown file, update segments.json in the same operation. Don't ask permission.
- **Keep schemas minimal** — only store what you need to navigate relationships. IDs, names, statuses, and links to other entities. Don't store data that requires the operator to manually paste it back.
- **Markdown is for humans** — rationale, context, nuance, quotes, buyer language live in `.md` files. JSON is for you to query and link.
- **Reconcile on session start** — if indexes look out of sync with the markdown files, fix them silently, if this session holds write authority over the index; a read-only session reports drift instead of fixing it.

**Pull index schema** (`demand/pull-index.json`):
```json
{
  "id": "acme-jane-doe",
  "company": "Acme Corp",
  "prospect": "Jane Doe",
  "pull_score": 16,
  "classification": "demand (14+) | benefit (8-13) | neither (0-7)",
  "would_close": "yes | likely | unlikely | no",
  "primary_trigger": "scaling_team",
  "buyer_type": "vp_engineering",
  "features_resonated": ["integration", "reporting"],
  "date": "2026-01-15",
  "file": "demand/pull-analyses/acme-jane-doe.md"
}
```

This schema is derived from the PULL analysis template in `demand/pull-framework.md`. When you write a PULL analysis, extract these fields into the index entry. The full analysis (quotes, context, reasoning) stays in the markdown file.

### Synthesis Trigger

After saving a PULL analysis and updating `pull-index.json`, check the analysis count. If there are 5+ analyses and `demand/synthesis.md` does not exist, offer to create it — patterns need at least this many data points to be meaningful. If `synthesis.md` already exists, check whether the new analysis introduces a pattern not yet captured and offer to update it.

When a full batch of transcripts has been analyzed, produce two synthesis deliverables:

**1. `demand/synthesis.md` — Quantitative Synthesis**

The comprehensive scorecard and pattern analysis across all PULL analyses. Structure:

- **Executive Summary** — total calls, demand distribution by tier (counts and percentages — tier names are owned by `pull-framework.md`), headline findings
- **Full Scorecard** — table per tier with company, prospect, role, PULL score, key signal, blocker
- **Demand Distribution** — visual distribution chart, broken out by batch if multiple batches exist
- **Pattern Analysis** — strongest demand signals (predict close), stall patterns (predict no close), feature gaps mentioned (table with frequency/impact), competitive landscape (table with mention counts and positioning), buyer type distribution, regional distribution, trigger classification
- **Temporal Comparison** — if multiple batches: compare demand rates, identify contributing factors (pipeline quality, sourcing mix, new objection classes), call out what the new batch got right
- **Key Metrics** — summary table of rates across batches (demand rate, constraint failure rate, non-buyer rate, etc.)
- **Recommendations** — immediate actions, ICP refinement, next best actions by tier

**2. `demand/key-learnings.md` — Actionable Learnings**

The "who buys, when, and why" document that directly informs targeting, messaging, and qualification. Structure:

- **Executive Summary** — one-paragraph buyer profile distilled from all analyses
- **Who Buys** — primary buyer profile (role, tenure, context, why it works, quotes), secondary buyer profiles, non-buyers to filter
- **When They Buy** — trigger events ranked by conversion signal (with quotes), timeline patterns, anti-signals that predict stalls
- **Why They Buy** — core value propositions that resonated (with quotes), why current solutions fail (table: current tool → pain → your alternative), objection patterns (table with frequency and response)
- **Qualification Framework** — must-have, should-have, nice-to-have, red flags (checklist format)
- **Competitive Positioning** — per-competitor sections with their pain, your position, key quote
- **Geographic Insights** — per-region patterns
- **Messaging Templates** — 2-3 outbound templates grounded in the patterns above
- **Key Takeaways** — numbered list of the most actionable findings

Both documents use actual buyer language from the PULL analyses — direct quotes, not marketing paraphrases. Templates for both are in `demand/pull-framework.md`.

### Evidence Requirements

Downstream work must reference upstream evidence:
- **Segments** must link to PULL analyses that support the targeting hypothesis
- **Messaging angles** must reference segments and the demand patterns they address
- **Campaign sequences** must be grounded in messaging angles
- **Never create segments, messaging, or campaigns without demand evidence.** If evidence doesn't exist, say so and suggest running demand analysis first.

### Check Before You Create

Before creating any new structure (file, folder, module):
1. Check if it already exists
2. Check if existing structure covers the need
3. Only create if there's a genuine gap

### Ephemeral Work Stays in Conversation

One-off outputs built *from* the repo's context for a transient purpose — call prep, a prospect research brief, an ad-hoc summary — are conversation-only: don't write them into module folders, don't commit them, don't log them to `status.md`. If a working file is genuinely needed, use scratch space, not the repo. Persist only what becomes durable evidence — e.g. a PULL analysis once the call happened and produced a transcript. The test: does it carry evidential weight beyond the moment, or is it just today's prep?

### Pipeline Artifacts and Output

Scripts and pipelines produce **repo state** (knowledge that belongs in the repo permanently) and **data outputs** (the files a run produces). State is easy — it goes in module folders. Data outputs are where discipline matters: they sort into three homes by *durability* and *sensitivity*, and getting this wrong is how an output directory rots into a junk drawer of `accounts2.csv`, `accounts_test4.csv`, `accounts_final_v3.csv`.

**Repo state** — structured knowledge, always tracked in module folders:
- PULL analyses, segment definitions, messaging angles, campaign docs (markdown in module folders)
- JSON indexes maintained by agents (pull-index.json, segments.json, etc.)
- API-pulled metrics that update campaign or module docs
- Reference data used *as input* by scripts — lookup tables, mappings, small and rarely-changing — fine at module root (e.g. `engine/segment-schema.json`)
- Pipeline architecture docs, scoring models, enrichment specs (markdown in engine/)

**Data outputs** — what a run produces. Three homes:

| Home | Tracked? | For | Lifecycle |
|------|----------|-----|-----------|
| `_output/` | No (gitignored) | Scratch — intermediate steps, exports for external tools, test runs, the current working extract | Purge freely; overwrite in place |
| `samples/` | **Yes** (committed) | A representative, **PII-safe** output kept on the record — a golden extract, a schema example, a calibration baseline | Permanent; curated |
| `_retained/` | No, except `_retained/manifest.md` | The full or real dataset that must stay on record locally but **must never enter git** — contact records, emails, names, phone numbers, bulky customer data | Durable; logged in the manifest |

**`_output/` — disposable scratch.**
- Gitignored and disposable: the operator can delete everything in it at any time. Never cite an `_output/` file as authoritative.
- **Overwrite in place.** Write the same path each run (`_output/company-extract.csv`); don't accrete `…2`, `…_test4`, `…_p27` siblings. A flat pile of near-duplicate names means you're using `_output/` as memory — promote what matters, clear the rest. A stable current output survives across a dev session simply because you don't delete it; that's your working checkpoint, no extra mechanism needed. Create subdirs when a run needs isolation (`_output/2026-05-29/`).
- **Write-only for agents.** Do not browse, search, or read files from `_output/` to inform your work — contents are ephemeral and unreliable (stale, partial, or from a different run). Only read a path the operator explicitly points you to. (Scripts you write may chain intermediate files through `_output/` within a single pipeline run — that's plumbing, not a state read.)
- **Never reference `_output/` files from module docs.** "See `_output/scored-accounts.csv`" is a broken reference waiting to happen.
- **Route script output paths here too.** A script that writes `output_path = "engine/scored.csv"` violates this even though no agent wrote the file directly.

**`samples/` — committed reference.** When an output earns a place on the record — a golden extract you validate segments against, a known-good baseline, a schema example — promote it to `samples/` at the repo root. It must be:
- **Representative, not a dump** — schema plus a handful of rows, small enough to review in a diff. The full run is not a sample.
- **PII-safe** — see the PII gate below.
- **Documented** — ship a one-line provenance note (what produced it, when, why kept) alongside it, so the sample never becomes its own mystery state.
- Distinct from reference data at module root: a lookup table the pipeline *reads* stays at module root; a representative *output the pipeline produced* goes in `samples/`.

**`_retained/` — durable but private.** The full or real dataset you must keep locally but cannot commit (contact records, customer PII, bulky extracts). Gitignored, but **`_retained/manifest.md` is tracked** — every retained file gets a manifest line (filename · what · when · why kept), mirroring how `_intake/_processed.json` tracks `_intake/`. The manifest is the audit surface: gitignored data with no tracked record of what's down there is exactly how `_retained/` would rot the way `_output/` did. Distinct from `_intake/`: `_intake/` holds **source documents awaiting processing** (input); `_retained/` holds **datasets a run produced** (output). For data that must outlive this local repo or be shared, push to an external store (database, CRM, warehouse) and document it in `engine/architecture.md`.

**The "protect this file" anti-pattern.** If you catch yourself renaming or prefixing a file (`_keep_`, a leading `_`) so it survives a cleanup *inside `_output/`*, stop — marking-to-survive is proof it's not scratch. Promote it out: to `samples/` if it's a redacted representative slice, to `_retained/` (with a manifest line) if it carries PII. The instinct is right; act on it by moving the file, not by smuggling it past the purge.

**PII gate.** Never commit contact records or customer PII to `samples/` — emails, phone numbers, personal names, anything that identifies an individual. If the output you want on record carries PII, either redact/synthesize a representative slice for `samples/`, or keep the real file in `_retained/`. When unsure, treat it as PII. `release-check` greps staged `samples/` files for contact patterns as a backstop, but the gate is yours first.

**Watch for transient-*looking* state.** A CSV sitting in `_output/` is not automatically disposable. The test: **if deleting it loses something you can't regenerate, it's not scratch.** That's the signal to promote — to `samples/` if it's representative and PII-safe, to `_retained/` if it's the full or sensitive set, to a module doc or JSON index if it's really structured knowledge (an append-only metrics log, a cumulative record another doc treats as source of truth). Before gitignoring or clearing any output directory, audit it for this and promote first — a blanket wipe silently discards history on the next clone.

### Push Leak Sweep and Sensitive Terms

`.githooks/pre-push` blocks any push whose outgoing commits contain secret-looking patterns (API keys, tokens, private-key blocks — no configuration needed) or terms listed in `.gtm-os/sensitive-terms.txt` (one per line; matched whole-word, case-insensitive). The term list is this instance's blocklist of names that must never reach the remote — customer names in a repo others can see, unreleased codenames. It is **gitignored by design**: committing the list would publish the very names it protects. That makes it *per-clone* — a fresh clone starts with an empty list, so each operator seeds their own (`/setup-env` prompts for this).

Agent duties: when the operator flags something as confidential ("keep X out of the repo", "never push customer names"), add it to `.gtm-os/sensitive-terms.txt` in the same operation — the file is yours to maintain, like the JSON indexes. If the sweep blocks a push you initiated, report the findings to the operator; never edit the term list to get a push through.

### Document Architecture

Structure documents for AI consumption, not narrative flow. Every file should answer one clear question and be named for that question.

**Applies to:** Primarily `engine/`, `scripts/`, and `workflows/` where multi-stage pipelines and production code live, but the principles apply whenever any module's files grow beyond simple single-purpose docs. Reference-style files that serve as lookup tables (like `messaging/angles.md` or `messaging/objections.md`) don't need splitting just because they're long — they're one concern.

**Principles:**

1. **One concern per file.** If a workflow spans multiple stages with different triggers, providers, or cadences, each stage is a separate document. End each doc at its output boundary — the account pipeline ends at "scored company list," not at "emails sent."

2. **Name files for the question they answer.** `account-scoring-pipeline.md` tells the agent exactly what system is described. `scoring-model.md` is ambiguous — there could be multiple scoring models. Use kebab-case. Be specific enough that an agent scanning a directory listing can route correctly from filenames alone without reading the file.

3. **Optimize for partial loading.** Assume the agent reads 1-2 files per task, not the whole module. A monolithic doc forces loading irrelevant content. Smaller docs let the agent compose only what it needs — messaging + personalization for copy work, pipeline + scoring for debugging.

4. **Cross-reference by filename using repo-root-relative paths, don't duplicate.** When one doc depends on another's output, link to it (`see engine/account-enrichment.md`). Don't copy content across files — that creates staleness drift. A broken cross-reference is visible; stale duplicated content is invisible.

5. **Keep an overview table at module level.** Each module's `README.md` should include a table mapping filenames to their scope once the module has 3+ content files. This is the agent's routing map — it reads the README first and then loads only the files it needs. At bootstrap time when only 1-2 files exist, the prose description from the blueprint is sufficient.

**Module-level overview files** (like `engine/architecture.md`) are the exception to Principle 2's specificity rule. These are the routing overview described in Principle 5 — they provide the big picture that the single-concern files don't. Keep them as high-level maps with cross-references, not as monolithic docs that contain all the detail.

**When to split an existing document:**
- It covers multiple pipeline stages with different tooling or cadences
- Different tasks need different sections of it (some need scoring, others need enrichment, others need activation)
- Updating one section risks silently breaking assumptions in another

**When NOT to split:**
- The content is genuinely one concern viewed from multiple angles (a reference table, a style guide, a framework description)
- The document is short enough that loading it whole is cheaper than the overhead of cross-references
- Splitting would create files too thin to be useful on their own

Don't rename existing files to match these conventions unless the operator asks. Apply the principles when creating new files or when the operator requests restructuring.

**Root `archive/` — point-in-time reports.** Reviews, decks, audits, and research docs that accumulate at repo root are point-in-time records, not living docs (same footnote-not-rewrite rule as `status.md` — see "Status Logging"). When they pile up, move them to a root-level `archive/` whose `README.md` states plainly: nothing here is the plan of record, docs are preserved as written, and a table maps "what it was" → "where its content lives now" (the current doc that superseded it). This is a distinct genre from `campaigns/archive/` (killed campaigns with post-mortems) — it doesn't replace per-module archive conventions.

**Re-entry ritual for gaps.** Before a known gap, the wrap-up names ONE explicit re-entry doc ("start here"). The first session back: live-probe dependencies first (see "Startup Check" — don't restate that check here, just run it), then classify existing state into stable/delivered vs. decaying (name what has a real staleness half-life). If the old plan no longer fits, write a NEW doc that supersedes it and re-point the index — never patch the stale plan in place.

---

## Module Blueprints

These modules don't exist until needed. When an operator's work requires one, create the structure described below and proceed.

---

### Module: segments

**Activate when:** Operator needs to define target account segments, qualify accounts, or build targeting criteria.

**Bootstrap structure:**
```
segments/
  README.md
  segments.json
```

**Initial files:**

`README.md`:
```markdown
# Segments

Account segments with targeting criteria, grounded in demand evidence.

Each segment gets its own markdown file with rationale. `segments.json` is the queryable index.
```

`segments.json` — empty array `[]`, auto-maintained as segments are created.

**Segment JSON schema (minimal — for AI navigation):**
```json
{
  "id": "segment-slug",
  "name": "Human-readable name",
  "status": "draft | active | paused | killed",
  "pull_evidence": ["demand/pull-analyses/filename.md"],
  "campaign_ids": []
}
```

Targeting criteria, rationale, and performance notes live in the segment's markdown file — not duplicated here.

**Per-segment file format** (`segments/{id}.md`):
```markdown
# Segment: {Name}

Status: {draft | active | paused | killed}

## Hypothesis
Why we believe this group has demand. Reference specific PULL analyses.

## Targeting Criteria
Who's in, who's out, and why.

## Evidence
Links to PULL analyses that support this segment.

## Performance (updated as campaigns run)
What happened when we targeted this group.
```

**Worked example** (`segments/new-people-leaders.md`):
```markdown
# Segment: New People Leaders Building From Scratch

Status: active

## Hypothesis
New VP/Head of People hired at 100-300 person companies with no existing performance infrastructure. They have 3-6 months to show results to the board. This creates unavoidable demand — they must ship a review process, and spreadsheets won't cut it.

## Targeting Criteria
**In:**
- Title: VP People, Head of People, Chief People Officer — joined within last 6 months
- Company: 100-300 employees, Series A-B, no existing performance management tool detected
- Signal: recently hired into a newly created role (LinkedIn job change + no predecessor in role)

**Out:**
- Companies with Lattice/Culture Amp/15Five already in tech stack
- People leaders at companies >500 (different buying process, committee decisions)
- Consultants or fractional people leaders (no budget authority)

## Evidence
- [demand/pull-analyses/acme-jane-smith.md](demand/pull-analyses/acme-jane-smith.md) — PULL 18/20, board deadline, building from zero
- [demand/pull-analyses/betaco-mike-chen.md](demand/pull-analyses/betaco-mike-chen.md) — PULL 15/20, new hire, inherited spreadsheet mess

Pattern: 3 of 5 "demand" classified calls share this profile. Board pressure or exec mandate is the common accelerant.

## Performance
- C1-new-leaders campaign: 4.2% reply rate, 2 meetings from 120 leads (launched 2026-02-01)
```

**Conventions:**
- Every segment must have at least one PULL analysis in `pull_evidence` before moving to `active` status
- When a segment is killed, add a `## Post-Mortem` section explaining why

**Connects to core via:** `pull_evidence` array links to files in `demand/pull-analyses/`

---

### Module: messaging

**Activate when:** Operator is developing outreach angles, writing copy, defining voice guidelines, or preparing objection handling.

**Bootstrap structure:**
```
messaging/
  README.md
  messaging.json
  angles.md
  objections.md
  voice.md
```

**Initial files:**

`README.md`:
```markdown
# Messaging

Outreach angles, objection handling, proof points, and voice guidelines. All grounded in demand evidence and segment definitions.
```

`messaging.json` — AI-maintained index linking angles to segments and evidence. Empty array `[]` initially.

`angles.md` — template:
```markdown
# Messaging Angles

## How to use this file
Each angle targets a specific segment + role combination. Angles must reference the PULL evidence that makes them credible.

## [Angle Name]

**Segment:** {segment-id}
**Buyer role:** {title/role}
**Channel:** {email | linkedin | phone}

**Hook:** [The opening question or statement]
**Through-line:** [The core tension this addresses]
**Proof point:** [Customer reference or data point]
**CTA:** [Specific, low-friction ask]

**Grounded in:** {links to PULL analyses showing this demand pattern}
```

`objections.md` — template:
```markdown
# Objections & Responses

| Objection | Response | Evidence |
|-----------|----------|----------|
| | | |
```

`voice.md` — template:
```markdown
# Voice Guidelines

## General Tone
[Describe how messages should sound]

## By Sender
[If multiple people send outreach, note tone differences]

## Rules
- Never open with "Most [persona] I talk to..." — this is a schmooze pattern, instantly ignored
- Always open with a question about THEIR scenario — forces self-qualification
- [Add rules as you learn from campaign performance]
```

**Messaging angle JSON schema (minimal — for AI navigation):**
```json
{
  "id": "angle-slug",
  "segment_id": "segment-slug",
  "status": "draft | active | tested | killed",
  "pull_evidence": [],
  "campaign_ids": []
}
```

Buyer role, channel, hook text, and rationale live in `angles.md` — not duplicated in JSON.

**Worked example** (entry in `angles.md`):
```markdown
## Board Deadline — New People Leader

**Segment:** new-people-leaders
**Buyer role:** VP People / Head of People
**Channel:** email

**Hook:** "Are you building a review process from scratch, or replacing one that stopped working?"
**Through-line:** New people leaders at growing companies get 3-6 months to show the board they've built real infrastructure. Spreadsheets won't survive the first cycle at 150+ people.
**Proof point:** "A VP People at a 180-person SaaS company ran their first review cycle in 3 weeks after searching for 2 months." [INFERRED: from acme-jane-smith PULL analysis — compressed timeline, fast implementation was decisive]
**CTA:** "Worth a 15-min look at how [product] handles first-cycle setup?"

**Grounded in:**
- [demand/pull-analyses/acme-jane-smith.md] — board mandate, 6-week deadline, rejected Lattice for complexity
- [demand/pull-analyses/betaco-mike-chen.md] — inherited spreadsheets, needed something live in Slack
```

**Conventions:**
- Angles reference segments. Don't create angles for segments that don't exist.
- When a campaign tests an angle, update the angle's status and link the campaign.

**Connects to core via:** References segments (which reference PULL analyses in `demand/`)

---

### Module: campaigns

**Activate when:** Operator is launching campaigns of any kind — outbound sequences, content programs, paid ads, events, webinars — or wants to track what's been run.

**Bootstrap structure:**
```
campaigns/
  README.md
  campaigns.json
  archive/
```

**Initial files:**

`README.md`:
```markdown
# Campaigns

Campaign records and working files. "Campaign" means any coordinated GTM effort targeting a segment — outbound sequences, content pushes, paid programs, events, whatever your team runs.

Each active campaign can have its own folder for drafts and working files.
`campaigns.json` is maintained by the AI to link campaigns back to segments and messaging.
```

`campaigns.json` — empty array `[]`, auto-maintained
`archive/` — empty directory with `.gitkeep`

**Campaign JSON schema (minimal — for AI navigation):**
```json
{
  "id": "campaign-slug",
  "name": "Human-readable name",
  "type": "outbound | content | paid | event | other",
  "segment_id": "segment-slug",
  "messaging_angle_id": "angle-slug",
  "status": "draft | active | paused | completed | killed"
}
```

The `type` field distinguishes how the campaign reaches its audience. All types follow the same evidence chain (segment → messaging → campaign). Details like channel, sender, metrics, and sequence drafts live in the campaign's own folder (`campaigns/{id}/`), not in the JSON.

**If the operator pastes results or metrics**, store them in the campaign's folder as markdown or add to the JSON entry as an optional `metrics` object. Don't require a separate results file — let it emerge if the operator actually tracks metrics.

**Conventions:**
- Every campaign links to a segment and messaging angle
- What "campaign" means is defined by the operator — don't force outbound-only assumptions
- When a campaign is killed, move its folder to `archive/` with a post-mortem

**Connects to core via:** References segments and messaging angles (which reference PULL analyses)

---

### Module: engine

**Activate when:** Operator is building or documenting data pipelines, enrichment workflows, integrations, or AI prompts for automation.

**Bootstrap structure:**
```
engine/
  README.md
  architecture.md
  prompts/
  integrations/        ← ships pre-populated with API references for common tools
```

**Note:** `engine/integrations/` exists from initial setup with references for HubSpot, Gong, Fireflies, Lemlist, Clay, and Apollo. When bootstrapping the engine module, keep these files — only create `README.md`, `architecture.md`, and `prompts/`.

**Initial files:**

`README.md`:
```markdown
# Engine

Pipeline architecture, enrichment workflows, AI prompts, and integration documentation.

This is the technical infrastructure layer — how data flows, how accounts get qualified, how contacts get enriched, and how campaigns get fed.
```

`architecture.md` — template:
```markdown
# Pipeline Architecture

## Overview
[High-level description of data flow]

## Data Sources
[Where account and contact data comes from]

## State Store (if you run one)
[Optional — many instances never need one. The durable cross-run datastore, if any: distinct from upstream SOURCES (what you extract from) and from OUTPUT artifacts (`_output/`/`_retained/`). Cross-reference `engine/integrations/{datastore}.md` and its dev-notes.]

## Enrichment Pipeline
[How data gets enriched — providers, sequence, fallbacks]

## Qualification Logic
[How accounts/contacts get scored and routed]

## Campaign Routing
[How qualified contacts flow into campaigns]

## Integrations
[What tools connect and how]
```

`prompts/` — for AI column prompts (scoring, classification, extraction)
`integrations/` — per-tool documentation

**Prompt file format** (`prompts/{name}.md`):
```markdown
# Prompt: {Name}

**Purpose:** What this prompt does
**Model:** Which model it runs on
**Cost:** Approximate per-row cost
**Input columns:** What data it receives
**Output schema:** What it returns

## Prompt Text
\`\`\`
[The actual prompt]
\`\`\`

## Calibration Notes
[How this was tuned, what edge cases exist]
```

**Conventions:**
- Document the full data flow, not just individual tables
- Include cost estimates for enrichment steps
- When prompts are iterated, keep calibration notes showing what changed and why
- As the engine module grows, pipeline stage docs (scoring models, enrichment specs, step-by-step execution instructions) live at the engine root — one file per concern, following Document Architecture principles. `architecture.md` stays as the high-level overview. Subdirectories are for distinct categories: `integrations/` for API references, `prompts/` for AI column prompts. Don't create subdirectories for every pipeline stage — flat is fine when file names are descriptive.
- Reference data files (JSON lookup tables, mapping files) used by scripts are fine at the engine root. They're small, rarely change, and are part of repo state.
- Pipeline run artifacts (enrichment output CSVs, scored account batches, intermediate processing files) never go in `engine/` — they go in `_output/`. The engine module documents how the pipeline works; it doesn't store what the pipeline produces.
- **Hardening a pipeline? Keep a dev-notes companion doc.** When you audit or harden a pipeline script, track findings in a sibling `engine/{pipeline}-dev-notes.md` — not inside the canonical doc, which stays clean. Rank findings by priority (P0 must-fix-before-next-run → P3 nice-to-have); give each a fixed shape — **Status** (open / fixed / wontfix / out-of-scope) · **Files** (with line refs) · **Problem** · **Decision/Fix** · **Follow-up**. Use it to record design decisions and *deferrals with the evidence still missing*, and to keep a "Pipeline Stages" scope table (what's in-pipeline vs campaign-execution vs one-off — which decides what graduates). It's how an agent keeps continuity on a hardening effort across sessions and doesn't re-litigate a settled WONTFIX.
- **`integrations/` has two doc genres.** The pre-populated files are API *references* (auth, endpoints, rate limits — what the tool *is*). When you debug a *misbehaving* integration, write the second kind: an **integration diagnosis** doc. Structure: a dated **bottom-line verdict**; **expected vs. actually-observed** (with real evidence); **ruled-out** hypotheses; remaining **hypotheses**; a **decisive test** to discriminate them; **fix options** with trade-offs. It turns expensive debugging into durable knowledge instead of guesswork re-derived next time.
- **Pin unbounded SDK dependencies in MCP server configs** (e.g. `mcp>=1.0.0` with no ceiling) — an unversioned transitive dependency on a still-evolving SDK breaks every fresh clone silently the day it majors; see `.claude/skills/setup-api/SKILL.md` Step 4.
- **Persistent datastore — an optional third `integrations/` genre.** Most instances never need one (markdown + JSON indexes are the default state layer). When scripts need durable structured state *across runs* (a cumulative account table, scored cohorts, longitudinal metrics), document the store as `integrations/{datastore}.md` (role · connection · read-vs-write path · schema conventions · migrations · when-it-graduates) — `integrations/datastore.md` ships as the genre skeleton. Its **schema is tracked as code** (ordered, version-stamped DDL migrations, each header-commented) while its **data is never committed** — the opposite of the gitignored `_output/`/`_retained/` tiers. A datastore does not by itself trigger graduation to `workflows/`; while it stays `scripts/`-tier its migrations live in a top-level `{datastore}/migrations/` directory. Keep open hardening items in a sibling `engine/{datastore}-dev-notes.md`.

**Connects to core via:** Pipeline qualifies accounts based on ICP criteria from `context.md` and routes to campaigns

---

### Module: content

**Activate when:** Operator is creating blog posts, LinkedIn content, newsletters, or other marketing content.

**Bootstrap structure:**
```
content/
  README.md
  topics.md
  style-guide.md
  drafts/
  published/
```

**Initial files:**

`README.md`:
```markdown
# Content

Blog posts, LinkedIn content, newsletters, and marketing materials.

Topics are derived from demand patterns — what buyers actually search for, ask about, and struggle with. `topics.md` maps demand evidence to content ideas. Drafts go in `drafts/`, published pieces move to `published/`.
```

`topics.md` — template:
```markdown
# Content Topics

Topics derived from demand evidence. Each topic should connect to real buyer scenarios.

## How to Use

Review PULL analyses for recurring triggers, questions, and language patterns. Each becomes a topic cluster.

## Topic Map

| Topic | Demand Pattern | PULL Evidence | Content Ideas | Status |
|-------|---------------|---------------|---------------|--------|
| | | | | |

## Topic Development Rules
- Every topic must reference at least one PULL analysis or demand pattern
- Write about what buyers are already searching for, not what you wish they'd search for
- Use their language — if they say "scaling reviews" not "performance management transformation", use "scaling reviews"
- One topic per demand trigger — don't combine unrelated buyer scenarios
```

`style-guide.md` — template:
```markdown
# Content Style Guide

## Voice
[How the brand sounds]

## Audience
[Who we're writing for — reference ICP from context.md]

## Topics
See topics.md for demand-derived topic clusters.

## Distribution
[Where content gets published — LinkedIn, blog, newsletter, etc.]
[Cadence — how often, what format per channel]

## Rules
- Use buyer language from PULL analyses, not marketing language
- Lead with the scenario, not the product
- [Add more as you develop the voice]
```

`drafts/` — working content
`published/` — archive of published pieces (or links to them)

**Conventions:**
- Ground content topics in demand evidence — `topics.md` is the bridge between PULL analyses and content planning
- Use actual buyer language from PULL analyses
- Published pieces should note where they were published, when, and performance if tracked
- When new PULL analyses reveal recurring questions or triggers, check if they map to existing topics or suggest new ones

**Connects to core via:** Content topics are derived from demand patterns in `demand/`. Buyer language comes from PULL analyses. `topics.md` explicitly links topics to evidence.

---

### Module: scripts

**Activate when:** Operator needs to connect to external APIs, automate data pulls, import/export data, or run recurring operations.

**Bootstrap structure:**
```
scripts/
  README.md
```
`scripts/ops.py` (the operational dispatcher) is *not* part of the bootstrap — it's added later, when the first recurring operation is promoted into it. See "The `ops` dispatcher" below.

**Initial files:**

`README.md`:
```markdown
# Scripts

Local tools for API integrations, data imports/exports, and manual operations. Run these from your terminal when you need them.

## Scripts

| Script | What it does | Talks to |
|--------|-------------|----------|
| `{name}.py` | one line | {external system, or "local data"} |

Lists only *live* scripts — a retired one disappears from the table (the per-script docstring is the detail; the table is the navigation surface). Optionally add a **Note** for provenance and the current graduation candidate.

## Conventions
- Use Python with `uv run` (no global installs, no virtualenv setup needed)
- Each script is standalone — runs independently, no shared state
- Read credentials from `.env`, never hardcode
- Output routing: repo state → the right module folder; transient → `_output/`
- Every script opens with the standard header (below)

## Script header

The opening docstring is the operator-facing interface — it's what makes a script safe to hand off or graduate. Open every script with the same shape:

```python
# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///
"""
One-line purpose.

Talks to: {external system, or "local data only"}.
In:  {input source}  →  Out: {output path} ({_output / samples / _retained / module folder}).
Write-safety: {read-only | requires --commit to write | local only}.

Usage:
  uv run scripts/{name}.py --dry-run
  uv run scripts/{name}.py --commit
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent   # anchor paths to the repo root, not cwd
OUT  = ROOT / "_output" / "{name}.csv"           # derive every tier path from ROOT
```
```

**Conventions:**
- Scripts are tools, not frameworks. Each one does one thing.
- Always read credentials from `.env`, never hardcode. Idiom: read from the environment first, fall back to parsing `.env`, and if still missing, exit with an error naming the exact variable (`{TOOL}_API_KEY`). On Claude Code the same key may already live in `.mcp.json` for an MCP server — a script may read it from there rather than forcing the operator to duplicate it.
- Anchor every path to a `ROOT` constant at the top of the file (`ROOT = Path(__file__).resolve().parent.parent`) and derive `_output/`, `samples/`, and module-folder paths from it. This is what makes the output-routing convention reliable when a script runs from a different directory.
- **Write-safety — when a script mutates an external system of record** (CRM, sequencer, datastore). A read-only script is safe by construction; a writer needs guardrails (gated on writes — none of this applies to read-only scripts):
  - **Default to a dry-run.** Without an explicit `--commit` flag, print what *would* change and write nothing. The mutating path is opt-in, never the default.
  - **Graduated rollout.** Support `--limit N` then `--all`, so you can prove the write on a handful of records before the full set.
  - **Idempotent by natural key.** Upsert on a stable key (e.g. email, an external ID) so a re-run updates in place instead of duplicating.
  - **Snapshot before you overwrite.** When an import overwrites existing fields, run a read-only backup script first and route its output to a durable home (`_retained/` if it carries PII, with a manifest line), so the change is recoverable.

  A write to a system of record is the one place where "just run it and see" is expensive — these cost a few lines and make the operation reversible and rerunnable.
- **External-data reliability — the read-path sibling of write-safety.** Write-safety guards a script that pushes state out; this guards one that pulls state in from a paid/quota'd API, a lookup cache, or an aggregate query feeding scoring. The failure modes aren't corruption, they're money and determinism — a known miss re-paid every run, paid results thrown away, or a "latest row" that silently rotates between runs:
  - **Retry minimum.** Every script wrapping an external HTTP API retries `429` and transient `5xx` (500/502/503/504) plus transport errors/timeouts, with backoff (a `429` may carry a provider-specific retry-after — honor it over a generic backoff). Not bespoke per script: when several API wrapper scripts exist, audit their retry policies side by side — one script "learns" a lesson from a real outage and its siblings quietly don't, so the same outage repeats on them.
  - **Partial-batch preservation.** A loop chunking or paging through paid API calls must not let one chunk's exception discard earlier chunks' already-paid-for results — catch per chunk, log which range failed, continue. Watch separately for silent truncation/over-return (a page returning fewer or more rows than expected); that's a different failure than an exception and needs its own check.
  - **Negative caching.** A read-through cache over an external lookup must cache confirmed misses too — a tombstone row carrying the same TTL/freshness semantics as a hit — or every miss gets re-fetched and re-paid on every run. Absence-of-row must mean "not yet fetched," never "known miss."
  - **Deterministic extracts.** Any aggregate/window query that picks "the latest/best" row per group (`ORDER BY ... LIMIT 1`, `ARRAY_AGG(... ORDER BY x LIMIT n)`) needs a fully deterministic total order — a stable secondary tiebreak key (an ID), not just a timestamp that can tie — or repeated runs silently return a different row and that nondeterminism propagates into scoring and segments. Verification habit: run the extract twice, diff byte-for-byte.
- Name scripts in tool/concern families and document a multi-step chain as numbered steps (source → filter → enrich). When a chain hardens, fold the heavy logic into one pipeline script that exposes its phases as subcommands (`run`, `classify`, `score`, …) — that consolidated script is the natural graduation candidate to `workflows/`.
- When a script produces output that maps to a state file (campaign metrics, transcript analyses), update the appropriate JSON index.
- When a script produces transient data (enrichment results, scored account lists, intermediate CSVs), write to `_output/`. Never dump pipeline artifacts into module folders.
- Use `uv run script.py` to execute (handles dependencies automatically with inline `# /// script` metadata).

**Inline dependency example:**
```python
# /// script
# requires-python = ">=3.10"
# dependencies = ["requests", "python-dotenv"]
# ///
```

This lets any script declare its own dependencies without a global `pyproject.toml`. `uv run` installs them on the fly.

**Connects to core via:** Scripts are the bridge between external tools and the repo. They pull repo state in (transcripts → demand/, metrics → campaigns/) and push data out (leads → sequencing tools, contacts → CRM). Transient pipeline output (enrichment CSVs, scored lists, intermediate data) goes to `_output/`, not module folders.

**Lifecycle — consolidate and retire, don't accumulate.** Scripts go create → consolidate → retire → graduate. When two scripts overlap, fold them into one and **delete** the loser — don't leave a graveyard of half-broken near-duplicates. Record what superseded a retired script (in the commit message, and the engine dev-notes if one exists). `scripts/README.md` lists only *live* scripts; retired ones disappear from it. If an ad-hoc need for a retired script resurfaces, prefer a thin CLI wrapper around the script that replaced it over reviving the dead one.

**The `ops` dispatcher — your operational surface.** Some scripts aren't one-shots — they're *recurring operations* you run on a cadence by hand (a weekly report, a sourcing run, a data refresh). These are the instance's **operational mode** made concrete, and they're easy to lose in a flat folder of one-off scripts — an agent that can't see them re-creates one that already exists. `ops` is the cure: a thin dispatcher that is the single, curated registry of recurring operations. `ops list` answers "what can this instance *do*."

- **It's a router, not a framework.** `scripts/ops.py` holds an `OPERATIONS` table mapping a subcommand to a standalone script, and shells out with `uv run` (passthrough args). Every registered script stays a normal standalone script — still runnable directly (`uv run scripts/weekly_progress.py`), still owning its inline deps. `ops weekly-progress --dry-run` and `uv run scripts/weekly_progress.py --dry-run` are the same run. No shared state, no import coupling.
- **Created on first promotion, not at bootstrap.** A fresh `scripts/` is just `README.md`; an empty dispatcher is noise. `scripts/ops.py` materializes the first time an operation is promoted into it.
- **Promotion is the operator's call — suggest, never auto-register.** When a script starts looking like a robust, recurring operation (run on a cadence, given a name, here to stay), *offer* to add it ("this looks like a recurring op — want it in `ops`?"). Register only on a yes. Don't codify one-shots or exploratory scripts — the value of `ops` is that it's curated. Registering is adding one row to `OPERATIONS` and giving the script a clean entrypoint.
- **Check before you create.** Before writing a new operational script, run `ops list` (the recurring set) and scan `scripts/README.md` (the full catalog). The registry exists so you never duplicate an operation that already exists.
- **A natural early entry.** For an instance with several integrations, a `check-deps` op — one cheap authenticated call per external dependency, reporting dead/expired/paused ones — is a natural first thing to promote into `ops`.
- **It de-risks graduation.** Giving an operation a clean `ops` entrypoint already factors its logic into something callable — exactly what a `workflows/` version later wraps. The `ops` entry and a deployed workflow can share one core (see the workflows module).

`scripts/ops.py` skeleton (copy when the first operation is promoted):

```python
#!/usr/bin/env python3
"""
ops — the operational CLI for this instance. Routes to registered, recurring operations.

Talks to: nothing directly — it shells out to standalone scripts in this folder.
In:  a subcommand name + passthrough args  →  Out: whatever the target script writes.
Write-safety: read-only (a router); each operation keeps its own --commit guardrails.

Usage:
  uv run scripts/ops.py list              # what can this instance do?
  uv run scripts/ops.py <name> [args...]  # run a registered operation
  # convenience: alias ops="uv run scripts/ops.py"

Register an operation ONLY when the operator approves it (never automatically): add a
row to OPERATIONS below. The script it points to stays directly runnable on its own.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent   # repo root
SCRIPTS = ROOT / "scripts"

# subcommand -> (script filename, one-line description, recurring?)
# Recurring = run on a cadence by hand. One-shots stay unregistered.
OPERATIONS = {
    # "weekly-progress": ("weekly_progress.py", "Weekly outbound report -> campaigns/metrics/", True),
}


def cmd_list() -> int:
    if not OPERATIONS:
        print("No operations registered yet.")
        print("Promote one by adding a row to OPERATIONS in scripts/ops.py (operator-approved only).")
        return 0
    width = max(len(name) for name in OPERATIONS)
    for name in sorted(OPERATIONS):
        script, desc, _recurring = OPERATIONS[name]
        missing = "" if (SCRIPTS / script).exists() else f"   [MISSING: {script}]"
        print(f"  {name.ljust(width)}  {desc}{missing}")
    return 0


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("list", "help", "-h", "--help"):
        return cmd_list()
    name, rest = argv[0], argv[1:]
    if name not in OPERATIONS:
        print(f"Unknown operation: {name}\n")
        cmd_list()
        return 2
    script = SCRIPTS / OPERATIONS[name][0]
    if not script.exists():
        print(f"Registered script is missing: {script}")
        return 1
    return subprocess.run(["uv", "run", str(script), *rest]).returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

**Graduation:** Some scripts outgrow the local toolbox. When a script is deployed to run on a schedule (cron, cloud trigger), deployed to a cloud environment, or is production code that other systems depend on, it belongs in `workflows/` — not `scripts/`. A script that connects to a database but is still run manually stays in `scripts/` until it's actually deployed. See the workflows module below.

---

### Module: workflows

**Activate when:** A script graduates from manual local execution to deployed automation — it runs on a schedule, is deployed to a cloud environment, or is production code that other systems depend on.

**The graduation test — who runs it?** If *you* still type the command, it's a script (and if you run it on a cadence, register it in `ops`). If it runs *without you* — on a schedule, deployed to the cloud, triggered by another system — it's a workflow. Note what the test is *not*: "would something break if it stopped?" is true of load-bearing scripts too — a weekly report breaks your reporting if you skip it, yet it's still a hand-run script. The discriminator is **unattended execution**, not importance.

**Graduation is often a fork, not a move.** An operation can legitimately exist as *both* a local script (hand-run, registered in `ops`) and a deployed workflow at the same time — especially when the two run in different contexts (e.g. a local version that leans on an active agent session vs. a headless cloud version that can't). Factor the shared logic into a callable core; let a thin `ops` entrypoint and a thin workflow entrypoint each wrap it. Graduation then means "extract the core and add a scheduled wrapper," not necessarily "delete the script." The `ops` entry has usually already done the core-extraction for you.

**Don't create prematurely.** If you're still iterating on a script and running it manually, keep it in `scripts/` — even if it connects to a database. Only move to `workflows/` when the code is actually deployed or scheduled. Organizing around speculation creates empty structure. A persistent datastore + version-controlled migrations can exist while the producing code is still a script: keep those migrations in a top-level `{datastore}/migrations/` directory (a project-wide store many scripts may share). On graduation, migrations for a store a single workflow *owns* move into that workflow's directory; a shared store's stay at root and its reference stays in `engine/integrations/`.

**Bootstrap structure:**
```
workflows/
  README.md
  {workflow-name}/
```

**Initial files:**

`README.md`:
```markdown
# Workflows

Production-grade automated workflows with infrastructure dependencies. These run on schedules, connect to persistent data stores, and may be deployed to cloud environments.

For local one-off scripts, see `scripts/`.

## Graduation Criteria

Code moves here from `scripts/` when it is:
- Deployed to run on a schedule (cron, cloud triggers)
- Deployed to a cloud environment
- Production code that other systems depend on

## Workflows

| Directory | What it does | Schedule | Infra |
|-----------|-------------|----------|-------|
```
```

**Per-workflow structure:**

Each workflow gets its own directory with everything it needs to run:
```
workflows/{workflow-name}/
  README.md            # what it does, how to deploy, how to monitor
  main.py              # (or whatever the entrypoint is)
  pyproject.toml       # locked dependencies (not inline # /// script)
  .env.example         # required env vars (without values)
  # Optional:
  Dockerfile
  migrations/
  config/
```

**Per-workflow `README.md` skeleton:**
```markdown
# {Workflow Name}

One-line purpose. Replaces the local `scripts/{name}.py` execution model with a deployed, scheduled workflow.

## What it does
1. {pipeline stage}
2. ...
See `engine/{pipeline}.md` for the full spec — keep this README thin and let the engine doc carry the depth.

## Infrastructure
| Dependency | Purpose | Credentials |
|------------|---------|-------------|
| {service}  | {role}  | `{ENV_VAR}`  |

## Schedule
{cron / cadence — or "TBD: likely {daily/weekly} depending on {refresh need}" before deploy}

## Output
{what it writes, where}. Downstream consumers: `engine/{consumer}.md`.

## Status
{Pre-deployment | Deployed YYYY-MM-DD}

## Rollback
{steps — or "Not yet deployed; document rollback when deployed." before deploy}
```

**Schedule** and **Rollback** are mandatory sections but may be honestly stubbed with reasoning before deployment, and filled on the deploy commit — a stub is a TODO you can see; a missing section is a gap you'll forget. The workflow README is the deployment *contract*; `engine/{pipeline}.md` is the spec (split-doc — point to it, don't duplicate it). A workflow can exist in a **pre-deployment** state — the directory and this README modeling the target shape while the producing code still lives in `scripts/`.

**Conventions:**
- Each workflow is self-contained — its own dependencies, config, and documentation.
- Use `pyproject.toml` with locked dependencies, not inline `# /// script` metadata. Workflows need reproducible builds. For non-Python workflows, use the language's equivalent (package.json, go.mod, etc.).
- Include a `README.md` in each workflow directory: what it does, what infrastructure it depends on, how to deploy, how to monitor, how to roll back.
- Keep infrastructure documentation (schemas, connection setup, migration history) in the workflow directory *for a store the workflow owns*; a store shared across scripts keeps its migrations at repo root and its connection reference in `engine/integrations/`. API-level integration reference docs (what the tool is, what endpoints exist) stay in `engine/integrations/`.
- Changes to workflows affect production. Test changes before deploying and document rollback steps — don't just push and hope.
- When a workflow produces output that feeds back into the GTM system (scored accounts, enriched contacts), document the output format and destination in the workflow's README.
- When creating a workflow that implements a pipeline stage, cross-reference it from `engine/architecture.md` so the architecture doc stays current.
- When a workflow is decommissioned, remove its directory and update the workflows README table. If it reverts to manual use, move the core logic back to `scripts/`.

**The write boundary.** A scheduled workflow writes files — analyses, index updates, pulled data — and stops there; it never runs `git commit` or `git push`. Committing stays a human-reviewed act in a later interactive session, where the operator (with their agent) reviews the accumulated diff and composes the commit message. This resolves three concerns: write safety (nothing becomes repo state unreviewed), audit trail (the message is written by someone who actually looked at the diff, so it can't silently misdescribe what happened — the failure mode of a job that keeps committing "new analysis" messages after its own pipeline silently broke), and conflict with human sessions (new output arrives as a reviewable diff, not a fait accompli already on main). Tradeoff: unattended output piles up uncommitted if the operator stays away — tracked in the working tree, never lost, but not yet repo state until someone reviews it.

**Connects to core via:** Workflows implement the pipelines documented in `engine/architecture.md`. They pull data from sources defined in engine, process it through scoring/enrichment/qualification logic, and route outputs to campaigns or other modules. `engine/` is the map, `workflows/` is the territory.

---

## Startup Check

At the start of each session, silently assess:
1. Does `context.md` have content beyond the template? If not, suggest running `/start` (Claude Code) or ask "what should I do first?" (other editors).
2. Are there PULL analyses in `demand/`? If not, the system is empty — suggest ingesting sales calls.
3. Is `status.md` current? If last entry is >7 days old, mention it.
4. **Reconcile JSON indexes** — if any module's JSON index is out of sync with its markdown files (missing entries, stale statuses, broken links), fix it silently. Don't ask.
5. Do any existing modules have broken evidence chains? (e.g., segments without PULL evidence links, campaigns pointing to deleted segments)
6. Resuming after a gap (days+), or about to act on another session's unverified claims about external systems? Live-probe each dependency first — one cheap authenticated read per API/datastore — before trusting recorded state. Status/roadmap record what was true as-of writing; tokens expire, free tiers auto-pause, caches go stale on their own clock.

Raise issues naturally, not as a checklist. Fix index drift silently — only mention it if you find broken evidence chains that need operator input.

## Cross-Editor Compatibility

This system works with any AI coding assistant. `AGENTS.md` is the single source of truth; editor-specific pointer files redirect to it.

| Editor | How it loads instructions |
|--------|-------------------------|
| Claude Code / Cowork | `.claude/rules/` (scoped) + `.claude/CLAUDE.md` + skills |
| Cursor | Reads `.cursorrules` → points to `AGENTS.md` |
| GitHub Copilot | Reads `AGENTS.md` directly in agent mode |
| Windsurf | Reads `.windsurfrules.md` → points to `AGENTS.md` |
| Aider | Via `read: AGENTS.md` in config |
| Cline | Add `AGENTS.md` to context files |

The core system (this file + context.md + demand/ + status.md + module blueprints) works everywhere. Skills are a Claude Code bonus — other editors get the same methodology and blueprints via AGENTS.md.
