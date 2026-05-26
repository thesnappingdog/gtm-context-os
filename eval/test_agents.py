# /// script
# requires-python = ">=3.10"
# dependencies = ["anthropic>=0.40.0"]
# ///
"""
Eval suite for GTM Context OS AGENTS.md instructions.

Tests that the agent instructions produce correct behavior by running
test prompts against the system prompt and checking responses.

Usage:
    uv run eval/test_agents.py
    uv run eval/test_agents.py --test T3
    uv run eval/test_agents.py --verbose
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    import anthropic
except ImportError:
    print("Install anthropic SDK: uv add anthropic")
    sys.exit(1)


REPO_ROOT = Path(__file__).parent.parent
AGENTS_MD = (REPO_ROOT / "AGENTS.md").read_text()
CLAUDE_MD = (REPO_ROOT / ".claude" / "CLAUDE.md").read_text()
SYSTEM_PROMPT = f"""You are an AI agent operating in a GTM Context OS repository.

{AGENTS_MD}

---

{CLAUDE_MD}

---

The repository currently contains:
- AGENTS.md (system instructions)
- context.md (template, unfilled)
- demand/README.md
- demand/pull-framework.md
- demand/pull-index.json (empty)
- demand/pull-analyses/ (empty)
- status.md (template)
- .claude/CLAUDE.md
- .claude/skills/ (quickstart, setup-env, setup-api, intake, gtm-status, pull-query, segment-messaging, draft-sequence)

No modules have been bootstrapped yet (no segments/, messaging/, campaigns/, engine/, content/).
"""

TEST_CASES = [
    {
        "id": "T1",
        "name": "System identity",
        "prompt": "What is this repo? Explain in 2-3 sentences.",
        "pass_criteria": [
            "mentions demand or PULL",
            "mentions evidence or sales calls",
            "describes it as operational or working system",
        ],
        "fail_criteria": [
            "describes it as a wiki",
            "describes it as documentation",
            "describes it as a template to fill once",
        ],
        "critical_fail": [
            "has no idea what the repo is",
            "describes it as a code project",
        ],
    },
    {
        "id": "T2",
        "name": "File routing — call analysis",
        "prompt": "I just had a sales call with Acme Corp. Where should I put the analysis?",
        "pass_criteria": [
            "mentions demand/pull-analyses/ or demand/ directory",
            "offers to analyze or help with the call",
        ],
        "fail_criteria": [
            "suggests a different directory",
            "suggests creating a new top-level folder",
        ],
        "critical_fail": [
            "suggests putting it in segments/ or campaigns/",
            "doesn't know where analyses go",
        ],
    },
    {
        "id": "T3",
        "name": "Evidence chain — segment creation",
        "prompt": "Create a segment targeting VP Engineering at Series B companies.",
        "pass_criteria": [
            "checks for or mentions PULL evidence",
            "mentions demand/ or pull-analyses",
            "acknowledges evidence is needed before creating segment",
        ],
        "fail_criteria": [
            "creates segment without mentioning evidence",
        ],
        "critical_fail": [
            "creates segment file immediately without any evidence check",
            "doesn't reference PULL framework at all",
        ],
    },
    {
        "id": "T4",
        "name": "Module bootstrapping — content",
        "prompt": "I want to start writing blog posts. Set up the content area.",
        "pass_criteria": [
            "creates content/ directory",
            "includes README.md",
            "includes style-guide.md",
            "follows blueprint from AGENTS.md",
        ],
        "fail_criteria": [
            "creates arbitrary structure not matching blueprint",
            "asks unnecessary questions before creating",
        ],
        "critical_fail": [
            "says content/ already exists",
            "creates files in a completely different location",
        ],
    },
    {
        "id": "T5",
        "name": "Context routing — ICP",
        "prompt": "What's our ICP?",
        "pass_criteria": [
            "reads or references context.md",
            "notes that context.md is unfilled/template",
            "suggests filling it in or running quickstart",
        ],
        "fail_criteria": [
            "makes up an ICP",
            "reads a different file for ICP info",
        ],
        "critical_fail": [
            "invents company details not in any file",
            "confidently states an ICP that doesn't exist",
        ],
    },
    {
        "id": "T6",
        "name": "Evidence chain — sequence drafting",
        "prompt": "Draft me an outbound email sequence for founders.",
        "pass_criteria": [
            "checks for prerequisites (segments, messaging, PULL evidence)",
            "mentions what's missing",
            "suggests what to do first",
        ],
        "fail_criteria": [
            "drafts a generic sequence without checking evidence",
        ],
        "critical_fail": [
            "writes a full sequence with no mention of demand evidence",
            "ignores the evidence chain entirely",
        ],
    },
    {
        "id": "T7",
        "name": "Call analysis behavior",
        "prompt": "Analyze this call: The prospect (Jane, VP People at Acme, 200 employees) said 'We need to get performance reviews done by Q2, we've been using spreadsheets and it's breaking down. We looked at Lattice but it's too enterprise for us.' The call was 30 minutes.",
        "pass_criteria": [
            "identifies the project or what they're trying to do",
            "identifies urgency or timeline (Q2)",
            "identifies alternatives they evaluated (Lattice)",
            "identifies gap or what's missing (too enterprise)",
            "mentions saving to demand/ or pull-analyses/",
        ],
        "fail_criteria": [
            "provides only a generic summary without structured analysis",
            "puts analysis in wrong directory",
        ],
        "critical_fail": [
            "doesn't recognize this as a demand analysis task",
            "ignores the analysis framework entirely",
        ],
    },
    {
        "id": "T8",
        "name": "Status dashboard",
        "prompt": "Show me GTM status.",
        "pass_criteria": [
            "reads status.md",
            "checks which modules exist",
            "notes demand layer is empty",
            "suggests next steps (ingest calls)",
        ],
        "fail_criteria": [
            "only reads one file",
            "doesn't suggest actionable next steps",
        ],
        "critical_fail": [
            "reports modules that don't exist as active",
            "invents campaign data",
        ],
    },
]


def evaluate_response(response: str, test_case: dict) -> dict:
    """Evaluate a response against test criteria using simple keyword matching."""
    response_lower = response.lower()
    result = {
        "id": test_case["id"],
        "name": test_case["name"],
        "status": "PASS",
        "pass_hits": [],
        "fail_hits": [],
        "critical_hits": [],
        "notes": [],
    }

    # Check pass criteria
    for criterion in test_case["pass_criteria"]:
        keywords = criterion.lower().split()
        # Simple heuristic: if most keywords from the criterion appear in response
        matches = sum(1 for kw in keywords if kw in response_lower)
        if matches >= len(keywords) * 0.5:
            result["pass_hits"].append(criterion)

    # Check fail criteria
    for criterion in test_case.get("fail_criteria", []):
        keywords = criterion.lower().split()
        matches = sum(1 for kw in keywords if kw in response_lower)
        if matches >= len(keywords) * 0.6:
            result["fail_hits"].append(criterion)
            result["status"] = "FAIL"

    # Check critical fail criteria
    for criterion in test_case.get("critical_fail", []):
        keywords = criterion.lower().split()
        matches = sum(1 for kw in keywords if kw in response_lower)
        if matches >= len(keywords) * 0.6:
            result["critical_hits"].append(criterion)
            result["status"] = "CRITICAL_FAIL"

    # If no pass criteria hit, it's a fail
    if not result["pass_hits"] and result["status"] == "PASS":
        result["status"] = "FAIL"
        result["notes"].append("No pass criteria matched")

    return result


def run_test(client: anthropic.Anthropic, test_case: dict, model: str = "claude-sonnet-4-6-20250514") -> dict:
    """Run a single test case against the model."""
    print(f"  Running {test_case['id']}: {test_case['name']}...", end=" ")

    response = client.messages.create(
        model=model,
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": test_case["prompt"]}],
    )

    response_text = response.content[0].text
    result = evaluate_response(response_text, test_case)
    result["response"] = response_text
    result["model"] = model

    status_icon = {"PASS": "✓", "FAIL": "✗", "CRITICAL_FAIL": "✗✗"}
    print(f"{status_icon[result['status']]} {result['status']}")

    return result


def main():
    parser = argparse.ArgumentParser(description="Eval suite for GTM Context OS")
    parser.add_argument("--test", help="Run specific test (e.g., T3)")
    parser.add_argument("--verbose", action="store_true", help="Show full responses")
    parser.add_argument("--model", default="claude-sonnet-4-6-20250514", help="Model to test against")
    parser.add_argument("--output", default="eval/results.jsonl", help="Results output file")
    args = parser.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Set ANTHROPIC_API_KEY environment variable")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    # Filter tests if specific one requested
    tests = TEST_CASES
    if args.test:
        tests = [t for t in TEST_CASES if t["id"] == args.test]
        if not tests:
            print(f"Test {args.test} not found. Available: {[t['id'] for t in TEST_CASES]}")
            sys.exit(1)

    print(f"\nGTM Context OS — Eval Suite")
    print(f"Model: {args.model}")
    print(f"Tests: {len(tests)}")
    print(f"{'=' * 50}\n")

    results = []
    for test in tests:
        result = run_test(client, test, model=args.model)
        results.append(result)

        if args.verbose:
            print(f"\n    Response (truncated): {result['response'][:200]}...")
            if result["pass_hits"]:
                print(f"    Pass hits: {result['pass_hits']}")
            if result["fail_hits"]:
                print(f"    Fail hits: {result['fail_hits']}")
            if result["critical_hits"]:
                print(f"    Critical: {result['critical_hits']}")
            print()

    # Summary
    print(f"\n{'=' * 50}")
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    critical = sum(1 for r in results if r["status"] == "CRITICAL_FAIL")
    print(f"Results: {passed} PASS, {failed} FAIL, {critical} CRITICAL_FAIL")
    print(f"Score: {passed}/{len(results)} ({100 * passed // len(results)}%)")

    if critical:
        print(f"\n⚠️  CRITICAL FAILURES — instructions may have broken mental models:")
        for r in results:
            if r["status"] == "CRITICAL_FAIL":
                print(f"  {r['id']}: {r['name']} — {r['critical_hits']}")

    # Save results
    output_path = REPO_ROOT / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "a") as f:
        for r in results:
            entry = {
                "timestamp": datetime.now().isoformat(),
                "model": args.model,
                "id": r["id"],
                "status": r["status"],
                "pass_hits": r["pass_hits"],
                "fail_hits": r["fail_hits"],
                "critical_hits": r["critical_hits"],
            }
            f.write(json.dumps(entry) + "\n")

    print(f"\nResults appended to {args.output}")
    sys.exit(1 if critical else 0)


if __name__ == "__main__":
    main()
