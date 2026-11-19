---
name: bootstrap
description: "Fastest way to get started — give a company website URL and agents crawl it to populate context.md. Use when operator wants to set up fast without answering 20 questions."
argument-hint: "[company website URL, e.g. 'acme.com' or 'https://www.acme.com']"
---

Bootstrap the GTM Context OS from a company's website. Agents crawl key pages, extract business context, and populate `context.md` — all tagged as marketing claims, not verified truth.

## When to Use

- First thing after cloning: "here's our website, get me started"
- Faster alternative to `/quickstart` when the operator doesn't want a Q&A session
- Anytime: "fill in context.md from our site"

## Core Principle

**A marketing website is a curated performance, not ground truth.** Everything extracted gets `[CLAIMED: website]` attribution. The operator can promote claims to `[VERIFIED]` later with sales data, PULL analyses, or direct confirmation.

Don't be cynical about it — website content is useful starting context. Just be honest that it's the company's own positioning, not independent evidence.

## Process

### Step 1: Normalize the URL

Accept any format: `acme.com`, `www.acme.com`, `https://acme.com`. Normalize to `https://` base URL.

### Step 2: Crawl Key Pages

Fetch these pages in parallel (use agents or concurrent web fetches). Not all will exist — that's fine, work with what you get:

| Page | What to extract | Typical URL patterns |
|------|----------------|---------------------|
| Homepage | Value prop, tagline, key features, social proof | `/` |
| About | Company story, team size, founding date, HQ, mission | `/about`, `/about-us`, `/company` |
| Product / Features | Core product, feature list, platform details | `/product`, `/features`, `/platform`, `/solutions` |
| Pricing | Pricing model, tiers, plan names | `/pricing`, `/plans` |
| Customers / Case studies | Customer logos, industries served, company sizes | `/customers`, `/case-studies`, `/stories` |
| Careers | Team size signal, HQ/offices, culture, tech stack | `/careers`, `/jobs`, `/open-positions` |
| Integrations | Tech ecosystem, required tools, partnership signals | `/integrations`, `/apps`, `/marketplace` |
| Blog (recent) | Topics they care about, thought leadership angles | `/blog` (just the index, not individual posts) |

**Crawl strategy:**
- Start with homepage — it usually links to the other key pages
- Follow navigation links to find the right URLs for each category
- If a page doesn't exist at expected URLs, skip it — don't guess
- Don't crawl more than 10-12 pages total. Breadth over depth.
- For case studies / customers pages, skim for company names and industries — don't read full case studies

### Step 3: Extract and Attribute

For each page, extract structured facts into these buckets:

**Company basics:**
- Name, tagline, what they do (1-2 sentences)
- Stage signals (funding mentions, team size, customer count)
- Founded date, HQ location
- Any explicit numbers (ARR, customer count, team size)

**Product:**
- Core product description
- Key features (top 5-8, not exhaustive)
- Platform / tech details
- Pricing model and tiers (if public)

**ICP signals:**
- Customer logos → infer company sizes, industries
- Case study titles → infer buyer roles, triggers
- "Built for..." or "Designed for..." copy → explicit ICP claims
- Pricing tiers → infer target company size (self-serve = SMB, "contact sales" = enterprise)

**Positioning:**
- Value proposition (usually on homepage hero)
- Comparison pages or "vs." content → competitors
- "Why us" or differentiation copy
- Categories they claim (e.g., "the AI-native CRM")

**Competitor signals:**
- Named alternatives on comparison pages
- Integration partners (sometimes reveal the ecosystem)
- Category language → who else is in that category

Tag everything: `[CLAIMED: website]`

### Step 4: Populate context.md

Fill in the `context.md` template with extracted data. For each section:

- **Company** — Fill from about/homepage. Straightforward.
- **Product** — Fill from product/features/pricing pages.
- **ICP** — Fill what you can infer. Firmographic criteria from customer logos and pricing. Buyer titles from case studies. **Leave buying patterns mostly empty** — websites don't reveal how people actually buy, only what the company wishes they'd do.
- **Positioning** — Fill from homepage/about. Tag as `[CLAIMED: website]`.
- **Competitors** — Fill if comparison pages exist. Otherwise leave a note: "No competitor data found on website — fill in from sales experience."
- **Disqualification rules** — Usually can't determine from a website. Leave template with a note.

### Step 5: Gap Analysis

After populating, report what's solid and what the website couldn't tell you:

```
## What I Learned From the Website

### Filled In
- Company basics: [what you found]
- Product: [what you found]
- Positioning: [what you found]

### Gaps — Needs Your Input
- **Buying patterns** — The website says who uses the product but not 
  how they find and evaluate it. How do prospects typically discover you? 
  What's the usual sales cycle?
- **ICP hard constraints** — I can see who your customers are, but not 
  who ISN'T a fit. What disqualifies a prospect?
- **Competitors from the buyer's perspective** — [Found X on comparison pages / 
  No comparison content found]. Who do prospects actually mention on calls?
- **Demand triggers** — Marketing copy describes benefits, not the 
  situations that make someone buy NOW. What's usually happening when 
  someone reaches out?
```

Frame gaps as things the website structurally can't answer, not as failures. Suggest the operator fill these in directly or run `/quickstart` to do it conversationally.

### Step 6: Confirm and Next Steps

Show the populated `context.md` to the operator. Then:

"Your context is bootstrapped from the website. Everything is tagged `[CLAIMED: website]` — it's useful starting context but reflects your marketing, not verified buyer behavior.

**To strengthen it:**
- Paste a sales call transcript — I'll run a PULL analysis that tests these claims against real buyer language
- Use `/quickstart` to fill in the gaps I flagged (buying patterns, triggers, disqualifiers)
- Use `/intake` if you have existing documents (pitch decks, playbooks, competitor analyses)"

Update `status.md` with a bootstrap entry.

## What This Skill Does NOT Do

- Does not verify any claims — everything is `[CLAIMED: website]` until confirmed
- Does not build segments, messaging, or campaigns — those need demand evidence
- Does not replace `/quickstart` — quickstart covers the human knowledge a website can't surface
- Does not deeply analyze blog content or case studies — that's `/intake` territory
