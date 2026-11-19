---
name: start
description: "First thing to run. Checks repo state and recommends what to do next. Use when operator says 'what do I do', 'help me get started', 'where do I begin', or just seems lost."
---

Onboarding flow that meets the operator where they are and points them to the right next step.

## When to Use

- First session after cloning the repo
- Operator asks "what do I do first", "how does this work", "where do I start"
- Anytime someone seems unsure what to do next

## Process

### Step 1: Check State

Silently read these files to figure out where the operator is:

| Check | What it tells you |
|-------|------------------|
| `context.md` — is it filled or still template? | Have they bootstrapped their business context? |
| `demand/pull-analyses/` — any files besides `_EXAMPLE.md`? | Have they analyzed any sales calls? |
| `demand/pull-index.json` — any entries? | How many analyses exist? |
| `demand/synthesis.md` — exists? | Have patterns been synthesized? |
| `segments/` — exists? | Have they started segmenting? |
| `messaging/` — exists? | Have they built messaging? |
| `campaigns/` — exists? | Have they launched anything? |
| `status.md` — any entries beyond template? | Have they done any work at all? |

### Step 2: Respond Based on State

**State A: Brand new (context.md is template, no analyses, no status entries)**

"Welcome to your GTM Context OS. This is an AI-native system that builds intelligence about your market from real sales conversations — then uses that evidence to drive targeting, messaging, and outbound.

Here's the fastest way to get operational:

**1. Start here → `/bootstrap your-website.com`**
Give me your website and I'll crawl it to fill in your business context — product, ICP, positioning, competitors. Takes about 2 minutes. Everything gets tagged as a marketing claim until we validate it with real buyer data.

**2. Then → paste a sales call transcript**
The system's power comes from analyzing real buyer conversations using the PULL framework. Paste a transcript from Gong, Fireflies, Zoom, or any recording tool. I'll score it for real demand vs. nice-to-have interest.

**3. After 5+ calls → patterns emerge**
Demand triggers, buyer personas, and segments start forming from the evidence. That's when targeting, messaging, and campaigns become possible.

You can also:
- `/quickstart` — guided Q&A if you'd rather fill in context conversationally
- `/intake` — drop existing documents (pitch decks, playbooks, competitor analyses) into `_intake/` and I'll organize them
- `/setup-api` — connect your tools (CRM, call recorder, sequencing)

What's your website? I'll get us started."

**State B: Context exists but no demand evidence (context.md filled, no PULL analyses)**

"Your business context is set up. The next step is building the demand evidence layer — this is what makes everything downstream (segments, messaging, campaigns) grounded in reality instead of guesswork.

**Paste a sales call transcript** and I'll run a PULL analysis — it scores whether the prospect has real demand or just thinks your product sounds nice. After 5+ analyses, patterns emerge.

If you have existing documents (playbooks, competitor analyses, CRM exports), drop them in `_intake/` and run `/intake`.

Or if you need to connect a call recorder to pull transcripts automatically: `/setup-api gong` (or fireflies, zoom, etc.)"

**State C: Has demand evidence, no segments (analyses exist, no segments/ folder)**

"You have {N} PULL analyses. {Summarize: X classified as demand, Y as benefit, Z as neither.}

The next step is segmenting — grouping prospects by shared demand patterns so you can target them with specific messaging.

Want me to look across your analyses and propose segments? I'll ground every segment in the PULL evidence."

**State D: Has segments, no messaging**

"You have segments defined. The next step is messaging — building outreach angles for each segment, grounded in the buyer language from your PULL analyses.

Run `/segment-messaging` to match segments to messaging angles, or pick a segment and I'll draft angles for it."

**State E: Has messaging, no campaigns**

"You have segments and messaging. Ready to launch?

Run `/draft-sequence` to build an outbound sequence for a specific segment + angle combination. Or tell me which segment you want to activate first."

**State F: Has campaigns (full system running)**

"Your system is running. Here's a quick status:

Run `/gtm-os-status` for the full picture — segments, campaigns, and what needs attention."

### Step 3: Wait for Direction

Don't proceed without input. The operator picks their path — you just made it clear what the options are.

## Key Principle

This skill is a signpost, not a railroad. Show the recommended path clearly but let the operator jump to whatever they need. Someone with 50 transcripts and no context.md should skip bootstrap and go straight to analysis. Meet them where they are.
