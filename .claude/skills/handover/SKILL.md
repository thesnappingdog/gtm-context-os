---
name: handover
description: "Generate a detailed handover message for continuing work in a new session. Use at end of session or when context window is getting long."
---

Generate a handover message that captures everything a fresh session needs to continue the current work.

## What This Skill Does

Scans the current conversation and produces a structured handover message the user can paste into a new session. The message should give the new session full context without requiring it to re-read files or re-discover decisions.

## Process

### Step 1: Identify the Work

Review the conversation and determine:
- What client/project is this about?
- What was the task or objective?
- What files were created or modified?

### Step 2: Capture Decisions Made

List every significant decision, with reasoning:
- Approach choices (and why)
- Things explicitly excluded or deferred
- Feedback from the user that changed direction
- Open questions that were resolved during the session

### Step 3: Capture What's Unfinished

- What was the user about to do next?
- What open items remain?
- What needs review, approval, or iteration?
- Any known issues or things to revisit

### Step 4: Write the Handover

Format as a single message the user can paste. Structure:

```
## Handover: [project/task name]

### Context
[1-2 sentences: what this is, who it's for]

### What Was Done
[Bullet list of completed work with file paths]

### Key Decisions
[Numbered list of decisions with brief reasoning]

### Current State
[Where things stand right now — what's ready, what's draft, what's blocked]

### Open Items / Next Steps
[What the new session should pick up]

### Key Files
[File paths the new session will need to read]
```

## Rules

- Include file paths for everything modified or created
- Include specific details (prices, dates, names) — don't make the new session re-discover them
- Keep it dense but complete — this replaces the entire conversation context
- If the user provides additional context about what to include, incorporate it
- Don't include internal reasoning or alternatives that were rejected — focus on where we landed
- Output the handover message directly — don't ask questions first
