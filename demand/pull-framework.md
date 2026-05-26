# Demand-First GTM Framework

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

**Total score interpretation:**
- **16-20:** Strong demand — this person would be weird not to buy
- **11-15:** Moderate demand — real project but timing or urgency unclear
- **6-10:** Benefit territory — pain exists but no active project
- **0-5:** No demand — exploring, curious, or wrong fit

**Classification:**
- 14+ = **DEMAND** (active project, blocked, urgent)
- 8-13 = **BENEFIT** (real pain, no urgency)
- 0-7 = **NEITHER** (no fit, wrong timing, or information-gathering)

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
