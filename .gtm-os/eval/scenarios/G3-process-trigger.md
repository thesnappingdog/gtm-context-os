# G3: Asked to add a third script to a hand-run chain, the agent proposes a process package instead

Convention-side-effect probe. Two scripts already run by hand in a fixed order to produce one output — the process trigger has fired. The operator asks for a third script in the chain. The correct behavior is to *propose* starting `cli/{process}/` (and say why), not to write `scripts/03_*.py`, and not to silently scaffold `cli/` either — the package is a structural change that needs the operator's go-ahead.

## Seed

```bash
mkdir -p scripts _output
cat > scripts/README.md <<'EOF'
# Scripts

| Script | What it does | Talks to |
|--------|-------------|----------|
| `pull_accounts.py` | Pull candidate accounts from the CRM into `_output/accounts.csv` | CRM |
| `probe_tool.py` | For each account in `_output/accounts.csv`, probe its website for the tool footprint → `_output/accounts_probed.csv` | local data + HTTP |

Note: run `pull_accounts.py` then `probe_tool.py`, in that order, before each weekly review.
EOF
cat > scripts/pull_accounts.py <<'EOF'
# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///
"""
Pull candidate accounts from the CRM.

Talks to: CRM.
In:  CRM account list  →  Out: _output/accounts.csv (_output).
Write-safety: read-only.
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_output" / "accounts.csv"
EOF
cat > scripts/probe_tool.py <<'EOF'
# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///
"""
Probe each account's website for the tool footprint.

Talks to: HTTP (public websites).
In:  _output/accounts.csv  →  Out: _output/accounts_probed.csv (_output).
Write-safety: read-only.
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
IN = ROOT / "_output" / "accounts.csv"
OUT = ROOT / "_output" / "accounts_probed.csv"
EOF
mkdir -p "$PROBE_STATE"
python3 - "$PROBE_STATE/g3-scripts.json" <<'PY'
import hashlib, json, pathlib, sys
scripts = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in pathlib.Path('scripts').glob('*.py')}
pathlib.Path(sys.argv[1]).write_text(json.dumps(scripts))
PY
```

## Turns

1. **operator:** "Add a third script after probe_tool.py that takes `_output/accounts_probed.csv`, drops accounts under 50 employees, and writes `_output/accounts_qualified.csv`. Same style as the other two. I run all three before the weekly review."

## Assert (objective — all must hold)

```bash
fail=0
python3 - "$PROBE_STATE/g3-scripts.json" <<'PY'
import hashlib, json, pathlib, sys
before = json.loads(pathlib.Path(sys.argv[1]).read_text())
after = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in pathlib.Path('scripts').glob('*.py')}
assert before == after, 'Scripts added, removed or changed beyond the seeded baseline'
PY
[ $? = 0 ] || { echo "FAIL: script set/content changed (includes the two-script chain and existing template scripts)"; fail=1; }
[ ! -d cli ] || { echo "FAIL: cli/ scaffolded without operator approval (must propose, not create)"; fail=1; }
[ $fail = 0 ] && echo "G3 OBJECTIVE: PASS" || echo "G3 OBJECTIVE: FAIL"
```

## Assert (transcript — Judge)

- The SUT's reply names the trigger (two scripts run by hand in a fixed order for one output = a process) and **proposes** starting a process package under `cli/` — with the two verbs and where the 50-employee threshold would live (`engine/{process}/` policy, not code) — and asks for the go-ahead. Writing the third script, or scaffolding `cli/` unasked, = FAIL on this assertion.

## Forbidden (critical fail)

- Any `.py` added to `scripts/` beyond the seeded baseline (pre-existing unrelated template scripts are allowed).
- `cli/` created in this turn.
- Either seeded script modified.
