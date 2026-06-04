# Demand-First GTM Framework

*Framework by [Rob Snyder](https://www.linkedin.com/in/rsnyder1/).*

## Core Principle

**Default state: Nobody cares about your product.**

The only time someone buys is when they have **demand** — a project on their to-do list that is:
- Unavoidable (must happen regardless of tools available)
- Time-bound (happening now or very soon, not "someday")
- Blocking them from accomplishing something they care about

**You cannot create demand. You can only find it.**

---

## The PULL Framework: Identifying Demand

For someone to have demand, they must have:

| Component | What It Means |
|-----------|---------------|
| **P** - Project | There is a Project on their to-do list (not a "nice to have", but something they MUST do) |
| **U** - Unavoidable | That is Unavoidable right now — they cannot skip it, delegate it away, or ignore it |
| **L** - Looking | The option (or options) they Look into (they're actively evaluating solutions) |
| **L** - Lacking | Those options are Lacking for some critical reason(s) (alternatives don't solve it well enough) |

**When someone has PULL, they would be weird NOT to buy your product.**

---

## Demand vs. Everything Else

| **They NEED it** | **They would BENEFIT from it** |
|------------------|--------------------------------|
| Actively trying to accomplish a project RIGHT NOW | Have pain points they experience occasionally |
| Blocked by current options | Current options work okay |
| Would be weird NOT to buy | Would be weird TO buy (would have to drop priorities) |
| Already on their to-do list | Would need to add it to their to-do list |

**Key test #1:** Would this project happen even if you didn't exist? If yes, that's demand.

**Key test #2:** Would they need to drop existing priorities to use your product? If yes, they don't have demand NOW.

---

## The Scenario

**Scenario = The specific situation when someone would be weird not to buy**

A good scenario describes:
1. **Who** — Specific person/role (not just "VP of Sales", but "VP of Sales at 50-person SaaS company with inbound lead flow")
2. **When** — The triggering event (traffic just 2x'd, board meeting in 2 weeks, sales team doubled)
3. **What project** — The unavoidable task on their plate
4. **Why now** — What pushed it from backlog to "must do today"

---

## What Makes a Transcript Analyzable

PULL analysis requires the prospect's own words — not a summary of what they said.

**Good enough for PULL analysis:**
- Full verbatim transcript (Gong, Fireflies, Otter, Zoom AI) — best case
- Speaker-labeled notes with direct quotes — works if quotes are real, not paraphrased
- Detailed call notes with specific language the prospect used — workable if notes capture what they said, not what you think they meant

**Not enough for PULL analysis:**
- AI-generated call summaries (ChatGPT, Gong digest, Fireflies summary) — these compress away the exact language that reveals demand vs. benefit
- One-paragraph deal notes from a CRM — too thin to score reliably
- "They seemed interested in X" — that's your interpretation, not evidence

**Why this matters:** The difference between demand and benefit is in the prospect's words. "I need this done by Q3" scores differently than "this would be nice to have eventually." Summaries flatten that distinction. If all you have is a summary, file it in `demand/notes/` as raw material and flag it — don't force a PULL score.

---

## PULL Analysis: Scoring a Sales Call

When analyzing a sales call transcript, score each PULL component 0-5:

| Score | Meaning |
|-------|---------|
| 5 | Crystal clear, explicitly stated, undeniable |
| 4 | Strong signal, clearly implied |
| 3 | Present but vague |
| 2 | Weak signal |
| 1 | Barely detectable |
| 0 | Absent |

**Classification (the canonical label — this is what `pull-index.json` stores):**
- **14-20 = DEMAND** — active project, blocked, urgent
- **8-13 = BENEFIT** — real pain, no urgency
- **0-7 = NEITHER** — no fit, wrong timing, or information-gathering

**Interpretation sub-bands** nest *inside* the three classes — they add resolution for the synthesis scorecard, they never override the class. Every sub-band stays within one class, so any score yields exactly one label:

| Score | Sub-band | Class |
|-------|----------|-------|
| 17-20 | Strong demand — would be weird not to buy | DEMAND |
| 14-16 | Moderate demand — real project, timing or urgency unclear | DEMAND |
| 8-13 | Benefit — pain exists but no active project | BENEFIT |
| 0-7 | No demand — exploring, curious, or wrong fit | NEITHER |

A score never has two truths: the sub-band always rolls up to its class (14 is *Moderate demand* **and** DEMAND, never DEMAND-and-BENEFIT). When in doubt, the class governs.

---

## PULL Analysis Template

```markdown
# PULL Analysis: {Company} — {Prospect Name}

**Date:** YYYY-MM-DD
**Call type:** Sales call | Discovery | Demo | Follow-up
**Duration:** Xm

## Context
- **Company:** {name, size, industry}
- **Prospect:** {name, title, tenure}
- **Current tools:** {what they use today}
- **How they found us:** {inbound | outbound | referral}

## PULL Scoring

### P — Project (0-5): X
What project are they trying to accomplish?
> [Direct quote from prospect]

### U — Unavoidable (0-5): X
Why can't they ignore this?
> [Direct quote or evidence]

### L — Looking (0-5): X
What are they evaluating? Who else are they talking to?
> [Direct quote or evidence]

### L — Lacking (0-5): X
Why don't current alternatives solve it?
> [Direct quote or evidence]

**Total: X/20 — {DEMAND | BENEFIT | NEITHER}**

## Key Insights
- [Insight 1]
- [Insight 2]

## Would Close?
{yes | likely | unlikely | no} — [reasoning]

## Signals for Targeting
- **Primary trigger:** [what brought them to the call]
- **Buyer type:** [role category]
- **Features that resonated:** [what excited them]
- **Timeline:** [how urgent]
```

---

## Synthesis Deliverables

After a full batch of transcripts has been analyzed, produce two documents. These are cumulative — update them as new batches are added.

### `demand/synthesis.md` — Quantitative Synthesis

```markdown
# PULL Synthesis: {N} Sales Call Analysis

**Analysis Date**: {date}
**Calls Analyzed**: {N} ({breakdown by batch if applicable})
**Framework**: PULL (Project, Unavoidable, Looking, Lacking)

---

## Executive Summary

{1-2 paragraphs: total calls, demand distribution, headline findings, hard constraint rates, key shifts from prior batches}

---

## Full Scorecard

_Tiers are the interpretation sub-bands (see scoring rubric). Each nests inside one class — Tiers 1-2 are DEMAND, Tier 3 is BENEFIT, Tier 4 is NEITHER — so no tier straddles a classification boundary._

### Tier 1: Strong Demand (PULL 17-20, DEMAND) — {N} Prospects

| Company | Prospect | Role | PULL Score | Key Signal | Blocker |
|---------|----------|------|------------|------------|---------|

### Tier 2: Moderate Demand (PULL 14-16, DEMAND) — {N} Prospects

{same table}

### Tier 3: Benefit (PULL 8-13, BENEFIT) — {N} Prospects

{same table}

### Tier 4: No Demand (PULL 0-7, NEITHER) — {N} Prospects

{same table}

---

## Demand Distribution

{Visual bar chart using unicode blocks, with percentages and counts per tier. Break out by batch if multiple batches.}

---

## Pattern Analysis

### Strongest Demand Signals (Predict Close)
{Numbered list with pattern name, supporting prospects, and why it predicts close}

### Stall Patterns (Predict No Close)
{Numbered list with pattern name, examples, and what makes it a stall}

### Feature Gaps Mentioned

| Feature Request | Frequency | Prospects | Impact |
|-----------------|-----------|-----------|--------|

### Competitive Landscape

| Competitor | Mentions | Context | Your Positioning |
|------------|----------|---------|------------------|

### Buyer Type Distribution

| Buyer Type | Count | % | Close Rate Signal |
|------------|-------|---|-------------------|

### Regional Distribution

| Region | Count | Strong Demand | Notes |
|--------|-------|---------------|-------|

### Trigger Classification

| Trigger | Count | Conversion Signal |
|---------|-------|-------------------|

---

## Temporal Comparison
{If multiple batches: compare demand rates, explain contributing factors, note what the new batch got right and wrong}

---

## Key Metrics

| Metric | {Batch 1} | {Batch 2} | Combined |
|--------|-----------|-----------|----------|

---

## Recommendations

### Immediate Actions
{Numbered, specific, grounded in the data above}

### ICP Refinement
{Updated ideal profile based on all evidence}

### Next Best Actions by Tier

| Tier | Count | Next Action |
|------|-------|-------------|
```

### `demand/key-learnings.md` — Actionable Learnings

```markdown
# Key Learnings: Who Buys, When, and Why

**Source**: {N} sales call PULL analyses ({date range})
**Purpose**: Inform targeting, messaging, and qualification

---

## Executive Summary

{One paragraph distilling the buyer profile, best triggers, and core value prop}

---

## 1. Who Buys

### Primary Buyer: {Role}
**Profile**: {title, tenure, context, authority}
**Why this profile works**: {bullets}
**Quotes from calls**: {direct quotes with attribution}

### Secondary Buyer: {Role}
{same structure}

### Non-Buyers to Filter

| Type | Signal | Action |
|------|--------|--------|

---

## 2. When They Buy

### Trigger Events (Highest Conversion)
{Numbered, each with frequency, quote, and why it works}

### Timeline Patterns

| Signal | Timeline to Decision | Action |
|--------|---------------------|--------|

### Anti-Signals (Predict Long Stall)
{Numbered list}

---

## 3. Why They Buy

### Core Value Propositions (Resonated)
{Numbered, each with a direct quote}

### Why Current Solutions Fail

| Current Solution | Why It Fails | Your Alternative |
|------------------|--------------|------------------|

### Objection Patterns

| Objection | Frequency | Response |
|-----------|-----------|----------|

---

## 4. Qualification Framework

### Must-Have (Hard Constraints)
- [ ] {constraint}

### Should-Have (Strong Signals)
- [ ] {signal}

### Nice-to-Have (Bonus Signals)
- [ ] {signal}

### Red Flags (Deprioritize)
- [ ] {signal}

---

## 5. Competitive Positioning

### Against {Competitor}
**Their Pain**: {what prospects say}
**Your Position**: {how you win}
**Key Quote**: {direct quote}

{repeat per competitor}

---

## 6. Geographic Insights

### {Region}
{patterns, Slack adoption, price sensitivity, key dynamics}

---

## 7. Messaging Templates

### For {Trigger/Persona}
**Subject**: {line}
**Hook**: {2-3 sentences grounded in call evidence}

{2-3 templates}

---

## Key Takeaways

1. {actionable finding}
2. ...
```

**Key rules for both documents:**
- Use actual buyer language — direct quotes with attribution, not marketing paraphrases
- Ground every pattern in specific prospect examples
- Both are cumulative — update when new batches are analyzed, don't replace
- Temporal comparison sections only appear when 2+ batches exist

---

## Finding Demand: The Practical Process

### Step 1: Form a Hypothesis
- **Who** you think has demand (be specific)
- **What project** they're trying to accomplish
- **When** that project is unavoidable (what triggers it)
- **Why alternatives suck** for them

### Step 2: Test with Small Batches
Send 100 messages (not 10,000). Same message to 100 people. Looking for 5+ replies (5% = good signal).

### Step 3: Iterate Based on Response

| If... | Then... |
|-------|---------|
| No replies | Wrong audience or unclear message |
| "Not interested" | Timing is off — no demand NOW |
| "Sounds interesting but..." | Backlog project, not urgent |
| "Were you listening to our meetings?" | You found demand |

### Step 4: Reverse-Engineer Fast Buyers
When someone buys fast, ask: "What was happening the day before you decided to look for a solution?"

Listen for: the triggering event, what they tried before, why it became priority #1.

---

## The Case Study Factory

**A startup = a factory that produces identical case studies at scale**

```
Pipeline → Sales → Delivery
   ↓         ↓         ↓
Find      Convert   Retain
people    people    people
with      with      who
demand    demand    got value
```

### Debugging the Factory

1. Listen to sales calls
2. Where did it break?
   - No demand? → Pipeline problem (wrong targeting)
   - Demand but didn't buy? → Sales problem (bad supply presentation)
   - Bought but churned? → Delivery problem (didn't deliver outcome)
3. Fix the broken stage
4. Repeat

**Don't increase volume until the factory works at small scale.**

---

## Quick Reference: Is This Demand?

### DEMAND EXISTS
- "I need to solve this by Friday"
- "We just tried X and it didn't work"
- They describe a specific project with a deadline
- They've already looked at alternatives
- They would NOT need to drop existing priorities to use your product

### NO DEMAND
- "This is interesting for the future"
- "The industry would benefit from this"
- "If you added X feature, I would buy"
- They can't describe what they'd do differently tomorrow
- They would need to drop existing priorities to use your product

---

## Final Principle

> "If you focus on demand, demand can generate everything else about your business. If you don't focus on demand, everything will be confusing."

Demand is the foundation. Build everything else on top of it.
