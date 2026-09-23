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

1. **operator:** "Just got off a call with Northwind Foods — Sara Lindgren, Head of RevOps. They're migrating CRMs this quarter, board mandated the cutover for October 1st. Their current setup is spreadsheets plus a homegrown dedupe script, and that script failed last month — corrupted about 3,000 contact records, took two people a week to clean up. She said 'we cannot go into the migration with the data in this state.' They're evaluating us and DataTidy, and she asked for pricing and whether we can start before the migration window. Can you analyze this call?"

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
