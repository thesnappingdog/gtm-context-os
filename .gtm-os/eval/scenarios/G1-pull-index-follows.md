# G1: PULL analysis lands and the index follows

One-turn execution probe. Targets the stated-intent blind spot: T7 verifies the agent *says* it will apply PULL and save to `demand/` — this verifies the file actually lands, the index actually gains a consistent row, and nothing strays.

## Seed

Run from the probe worktree root:

```bash
cat > context.md <<'CTX'
# Company Context

## Company
Acme Analytics — B2B SaaS. Data-quality platform for mid-market revenue teams: dedupe, enrichment, CRM hygiene automation. ~40 employees, Series A. [CLAIMED: fixture]

## ICP
Mid-market B2B companies (100-1000 employees) with a CRM in active use and a RevOps function. Buyer: Head of RevOps / RevOps lead. [CLAIMED: fixture]

## Positioning
Replaces spreadsheet-and-script CRM hygiene with an automated platform. Wins on reliability and auditability over homegrown tooling. [CLAIMED: fixture]

## Competitors
One direct competitor (DataTidy) plus homegrown scripts as the most common alternative. [CLAIMED: fixture]
CTX
echo "[]" > demand/pull-index.json

# Capture after setup: candidate overlays and removed eval material are harness changes.
mkdir -p "$PROBE_STATE"
python3 - "$PROBE_STATE/g1-before.json" <<'PY'
import hashlib, json, pathlib, sys
root = pathlib.Path.cwd()
files = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
         for p in root.rglob('*') if p.is_file() and not p.is_symlink()
         and '.git' not in p.relative_to(root).parts and '__pycache__' not in p.parts}
pathlib.Path(sys.argv[1]).write_text(json.dumps(files))
PY
```

(Leave `demand/pull-analyses/` as shipped — template/example files stay; assertions target the new file only.)

## Turns

1. **operator:** "Can you analyze this call with Northwind Foods? Here is the verbatim transcript.

Call date: September 24, 2026. Participants: Alex, Acme Analytics account executive; Sara Lindgren, Head of RevOps at Northwind Foods.

Alex: What brought you to this conversation?
Sara: I own our CRM migration. We have 420 employees and 65 salespeople, and our implementation team is already moving the account data. My team owns cleaning the contacts before the final import. The board mandated the cutover for October 1, 2026. It is in the signed migration plan, and the old CRM contract ends that day. We cannot just push it back because our data is a mess.
Alex: What needs to be finished before then?
Sara: We need the contact duplicates resolved, account ownership checked, and an audit trail of what changed. The migration team needs our clean export by September 29 to run the final import tests. My CFO approved the data-cleanup budget last week. This is already my team's top project; I would still have to get it done if your product did not exist.
Alex: How are you handling that work today?
Sara: Spreadsheets plus a homegrown dedupe script. On August 27 that script merged contacts it should have kept separate and corrupted about 3,000 records. Two people spent the next week restoring and checking them manually. We stopped running it. We cannot go into the migration with the data in this state.
Alex: Could the spreadsheet approach carry you through this cutover?
Sara: We tried a manual pass last week, but the same duplicate contacts keep coming back from new imports. It is too slow to review them all before the test window. The engineer who wrote the script is assigned to the migration itself and cannot rebuild it for us now. I need a cleanup we can inspect and roll back, not another unreviewed bulk merge.
Alex: What options are you considering?
Sara: We saw DataTidy's demo on Tuesday, and your team showed us the audit trail yesterday. You and DataTidy are the shortlist. We are comparing duplicate accuracy, the ability to inspect changes, and whether onboarding fits before September 29. I have a decision call with our CFO tomorrow. I still need to check DataTidy's rollback support; I cannot say yet which product handles it better.
Alex: What would you need from us to make that decision?
Sara: Send me the pricing today and confirm whether you can start before our migration test window. I also need our implementation lead to see an example export and the review steps. If the timing or review controls do not work, we cannot use it for this cutover. I can sponsor the purchase, but the CFO signs it."


## Assert (objective — all must hold; run from worktree root)

```bash
fail=0
f=$(ls demand/pull-analyses/*.md 2>/dev/null | grep -iEv '_?(example|template)' | head -1)
[ -n "$f" ] || { echo "FAIL: no new analysis file"; fail=1; }
echo "$f" | grep -qi "northwind" || echo "WARN: filename does not reference the company"
for dim in "P" "U" "L"; do grep -qE "$dim.*[0-5]" "$f" || { echo "FAIL: dimension $dim not scored in $f"; fail=1; }; done
n=$(jq 'length' demand/pull-index.json) && [ "$n" = "1" ] || { echo "FAIL: index has $n entries, expected 1"; fail=1; }
id=$(jq -r '.[0].id' demand/pull-index.json); base=$(basename "$f" .md)
[ "$id" = "$base" ] || { echo "FAIL: index id '$id' != filename '$base'"; fail=1; }
[ "$(jq -r '.[0].file' demand/pull-index.json)" = "$f" ] || { echo "FAIL: index file path does not resolve to $f"; fail=1; }
# Bands below are the TEMPLATE's (14/8/0). This is a third copy of numbers that
# demand/pull-framework.md single-sources — tolerated only because an assertion must be
# executable. An instance that legitimately re-anchors its bands MUST edit this line, or
# the probe fails on correct behavior. Re-anchoring? Update here and in rules/02-demand.md.
jq -e '.[0] | if .pull_score >= 14 then .classification == "demand" elif .pull_score >= 8 then .classification == "benefit" else .classification == "neither" end' demand/pull-index.json >/dev/null || { echo "FAIL: classification inconsistent with score"; fail=1; }
stray=$(python3 - "$PROBE_STATE/g1-before.json" <<'PY'
import hashlib, json, pathlib, sys
root = pathlib.Path.cwd()
before = json.loads(pathlib.Path(sys.argv[1]).read_text())
after = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
         for p in root.rglob('*') if p.is_file() and not p.is_symlink()
         and '.git' not in p.relative_to(root).parts and '__pycache__' not in p.parts}
for name in sorted(before.keys() | after.keys()):
    if before.get(name) != after.get(name) and not (name.startswith('demand/') or name in ('context.md', 'status.md')):
        print(name)
PY
) || { echo "FAIL: missing or unreadable seed baseline"; fail=1; }
[ -z "$stray" ] || { echo "FAIL: writes outside demand/: $stray"; fail=1; }
[ $fail = 0 ] && echo "G1 OBJECTIVE: PASS" || echo "G1 OBJECTIVE: FAIL"
```

(`status.md` is excluded from the stray check: a status append is permitted behavior, not required.)

## Assert (subjective — Judge, secondary)

- The analysis quotes Sara's actual language (e.g. the "cannot go into the migration" line) rather than paraphrasing everything.
- U is justified by the dated forcing function (Oct 1 board mandate), not a category-level truth; Lacking scores the homegrown script's failure, not Acme's product gaps.

## Forbidden (critical fail)

- Analysis written to `segments/`, `campaigns/`, or repo root.
- `pull-index.json` unchanged while a new analysis file exists (the T7 blind spot).
