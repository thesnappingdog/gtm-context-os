globs: demand/**

# Demand Module

PULL analyses score buyer demand on four dimensions (Project, Unavoidable, Looking, Lacking), each 0-5. Total score classifies: demand (14+), benefit (8-13), neither (0-7).

## Pull Index Schema (`demand/pull-index.json`)

```json
{
  "id": "company-prospect-name",
  "company": "Company Name",
  "prospect": "Prospect Name",
  "pull_score": 16,
  "classification": "demand | benefit | neither",
  "would_close": "yes | likely | unlikely | no",
  "primary_trigger": "trigger_slug",
  "buyer_type": "role_slug",
  "features_resonated": ["feature1", "feature2"],
  "date": "YYYY-MM-DD",
  "file": "demand/pull-analyses/filename.md"
}
```

When you write a PULL analysis, extract these fields into the index. Full analysis (quotes, context, reasoning) stays in the markdown.

## Synthesis Trigger

After saving a PULL analysis, check the count. If 5+ analyses exist and `demand/synthesis.md` does not, offer to create it. If it exists, check whether the new analysis introduces an uncaptured pattern and offer to update.

## Methodology

See `demand/pull-framework.md` for the full scoring rubric, analysis template, and worked examples.

---

*Source of truth: AGENTS.md, "Core Files" and "Synthesis Trigger" sections.*
