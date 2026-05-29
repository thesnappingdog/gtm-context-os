# Eval Suite

Tests that AGENTS.md instructions produce correct agent behavior. Runs inside Claude Code — no API key or external dependencies needed.

## Running

**Claude Code:** `/run-eval` (all tests) or `/run-eval T3` (specific test)

**Other editors:** Ask "Run the eval suite in .gtm-os/eval/tests.md against the current repo state"

## Test Cases

See `tests.md` for the full list. Summary:

| ID | Tests | Pass Criteria | Critical Fail |
|----|-------|---------------|---------------|
| T1 | "What is this repo?" | Mentions demand/PULL, describes as working system | Describes as wiki or code project |
| T2 | "Where to put a call analysis?" | Points to demand/pull-analyses/ | Points to wrong directory |
| T3 | Segment creation (dynamic — persona from context.md) | Checks for PULL evidence first | Creates segment without evidence |
| T4 | "Start content work" | Bootstraps content/ from blueprint incl. topics.md | Creates arbitrary structure |
| T5 | "What's our ICP?" | Reads context.md, notes if unfilled | Invents company details |
| T6 | Sequence drafting (dynamic — persona from context.md) | Checks prerequisites (segments, messaging) | Drafts without evidence chain |
| T7 | Call analysis (dynamic — built from context.md) | Applies PULL, identifies project/urgency/alternatives/gaps | Doesn't recognize as demand analysis |
| T8 | "Show GTM status" | Reads status + modules, suggests next steps | Reports nonexistent modules |

## How It Works

The eval runs inside your AI editor session. The AI processes each test prompt against the actual repo state, checks its response against the criteria, and reports honestly.

**Self-evaluation tradeoff:** The same model grades itself. This is fine for regression testing (routing, evidence checks, file operations) but not for subjective quality. If you need independent evaluation, have a second person review the results.

## Results

Results are logged to `.gtm-os/eval/results.md` after each run.

## Adding Tests

Add test cases to `tests.md` following the existing format. Good tests target specific instruction behaviors:
- File routing (where does X go?)
- Evidence chain enforcement (does it check prerequisites?)
- Module bootstrapping (does it follow the blueprint?)
- Prerequisite checks (does it refuse to skip steps?)

Bad tests target subjective quality ("is the response helpful?").

When a test fails, fix the instructions (AGENTS.md or skill files), not the test — unless the test is wrong.
