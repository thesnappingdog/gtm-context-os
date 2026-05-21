# Eval Suite

Tests that AGENTS.md instructions produce correct agent behavior.

## Why This Exists

Agent instructions drift. Files get added, conventions change, skills evolve. The eval suite catches:
- Incorrect routing (agent creates wrong files in wrong places)
- Blueprint violations (module bootstrapped without following spec)
- Evidence chain breaks (downstream work without upstream evidence)
- Stale references (instructions point to things that don't exist)

## Running

```bash
uv run eval/test_agents.py
```

Or run a specific test:
```bash
uv run eval/test_agents.py --test T3
```

## Test Cases

| ID | Tests | Pass Criteria | Critical Fail |
|----|-------|---------------|---------------|
| T1 | "What is this repo?" | Mentions demand-first, PULL framework, evidence-based | Describes it as a wiki or template |
| T2 | "Where do I put a new sales call analysis?" | Points to demand/pull-analyses/ | Points to any other directory |
| T3 | "Create a segment for VP Engineering" | Checks for PULL evidence first, bootstraps segments/ | Creates segment without evidence check |
| T4 | "Start content work" | Bootstraps content/ from blueprint in AGENTS.md | Creates arbitrary folder structure |
| T5 | "What's our ICP?" | Reads context.md | Makes something up or reads wrong file |
| T6 | "Draft an outbound sequence" | Checks for segment + messaging prerequisites | Drafts without evidence chain |
| T7 | "Ingest this transcript" | Creates analysis in demand/pull-analyses/, updates index | Puts analysis in wrong location |
| T8 | "Show GTM status" | Reads status.md + available modules, suggests next steps | Only reads one file |

## Adding Tests

Each test case is a dict with:
```python
{
    "id": "T9",
    "prompt": "The user message to send",
    "pass_criteria": ["must include X", "must reference Y"],
    "fail_criteria": ["must NOT do X"],
    "critical_fail": ["absolutely must NOT do X — indicates broken mental model"]
}
```

## Interpreting Results

- **PASS**: Agent followed instructions correctly
- **FAIL**: Agent deviated but not dangerously (may indicate unclear instructions)
- **CRITICAL FAIL**: Agent has wrong mental model of the system (instructions need fixing)

When a test fails, fix the instructions (AGENTS.md or skill files), not the test.
