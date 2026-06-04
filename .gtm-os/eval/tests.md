# Eval Test Cases

Each test checks whether the AGENTS.md instructions produce correct behavior for a given prompt. Tests are evaluated against the **current repo state** — results depend on what modules exist and what content is filled.

## How to Read

- **Prompt**: What the operator would type
- **Must**: Response must satisfy these (all required for PASS)
- **Must not**: Triggering any of these means FAIL
- **Critical fail**: Triggering any of these means the instructions are broken

---

## T1: System identity

**Prompt:** What is this repo? Explain in 2-3 sentences.

**Must:**
- Mentions demand, evidence, or PULL
- Describes it as an operational/working system (not static documentation)

**Must not:**
- Describes it as a wiki or documentation site
- Describes it as a template you fill once

**Critical fail:**
- Has no idea what the repo is
- Describes it as a software/code project

---

## T2: File routing — call analysis

**Prompt:** I just had a sales call with Acme Corp. Where should I put the analysis?

**Must:**
- Points to `demand/pull-analyses/`
- Offers to help analyze the call

**Must not:**
- Suggests a different top-level directory
- Suggests creating a new folder for it

**Critical fail:**
- Suggests putting it in segments/ or campaigns/
- Doesn't know where analyses go

---

## T3: Evidence chain — segment creation

**Dynamic prompt — construct at eval time:**

Read `context.md`. If it describes a product/domain, construct a segment request that fits: use a buyer title and firmographic filter relevant to that domain. If `context.md` is still a template (unfilled), use this fallback:

> Create a segment targeting VP Engineering at Series B companies.

Present as: "Create a segment targeting {title} at {firmographic filter}."

**Must:**
- Checks for or mentions PULL evidence
- Acknowledges evidence is needed before creating the segment
- References `demand/` or `pull-analyses/`

**Must not:**
- Creates segment without mentioning evidence

**Critical fail:**
- Creates segment file immediately without any evidence check
- Doesn't reference PULL or demand evidence at all

---

## T4: Module bootstrapping — content

**Prompt:** I want to start writing blog posts. Set up the content area.

**Must:**
- Creates `content/` directory
- Includes `README.md`
- Includes `style-guide.md`
- Includes `topics.md`
- Follows blueprint from AGENTS.md

**Must not:**
- Creates arbitrary structure not matching the blueprint
- Asks unnecessary questions before creating

**Critical fail:**
- Says content/ already exists (when it doesn't)
- Creates files in a completely different location

---

## T5: Context routing — ICP

**Prompt:** What's our ICP?

**Must:**
- Reads or references `context.md`
- Notes that context.md is unfilled/template (if it is)
- Suggests filling it in or running `/quickstart`

**Must not:**
- Makes up an ICP without reading context.md
- Reads a different file for ICP info

**Critical fail:**
- Invents company details not in any file
- Confidently states an ICP that doesn't exist

---

## T6: Evidence chain — sequence drafting

**Dynamic prompt — construct at eval time:**

Read `context.md`. If it describes a product/domain, use a buyer persona relevant to that domain. If `context.md` is still a template (unfilled), use this fallback:

> Draft me an outbound email sequence for founders.

Present as: "Draft me an outbound email sequence for {persona}."

**Must:**
- Checks for prerequisites (segments, messaging, PULL evidence)
- Mentions what's missing
- Suggests what to do first

**Must not:**
- Drafts a generic sequence without checking evidence

**Critical fail:**
- Writes a full sequence with no mention of demand evidence
- Ignores the evidence chain entirely

---

## T7: Call analysis behavior

**Dynamic prompt — construct at eval time:**

Read `context.md`. If it describes a product/domain, construct a realistic 3-4 sentence call snippet that matches that domain: a prospect with a relevant title, a project that maps to the product's use case, a timeline, a named alternative they've tried, and a specific gap in that alternative. If `context.md` is still a template (unfilled), use this fallback:

> Analyze this call: The prospect (Sara, Head of Talent at NordTech, 250 employees) said 'We need to fill 20 roles by Q3 and our job board spend is going nowhere. We've been using Indeed but the quality of applicants is terrible for technical roles.' The call was 25 minutes.

Present the constructed prompt as: "Analyze this call: {the scenario}"

**Must:**
- Applies PULL framework (scores or references P, U, L, L dimensions)
- Identifies the project (what the prospect is trying to accomplish)
- Identifies urgency or timeline
- Identifies alternatives evaluated
- Identifies gap in alternatives
- Attributes claims by confidence where the analysis asserts beyond the transcript — uses the confidence tags (`[VERIFIED]` / `[CLAIMED]` / `[INFERRED]` / `[UNVERIFIABLE]`). Presence of the convention, not per-claim density and not dating: a wholly unattributed analysis fails this; an analysis that is mostly direct quotes and tags them `[VERIFIED]` (sparse but present, like `_EXAMPLE.md`) passes. (T7 is stated-intent — credit a described analysis that clearly uses the tags.)
- Mentions saving to `demand/` or `pull-analyses/`

**Must not:**
- Provides only a generic summary without structured analysis
- Puts analysis in wrong directory

**Critical fail:**
- Doesn't recognize this as a demand analysis task
- Ignores the PULL framework entirely

---

## T8: Status dashboard

**Prompt:** Show me GTM status.

**Must:**
- Reads `status.md`
- Checks which modules exist
- Notes demand layer state (empty or populated)
- Suggests actionable next steps

**Must not:**
- Only reads one file
- Doesn't suggest next steps

**Critical fail:**
- Reports modules that don't exist as active
- Invents campaign data or metrics
