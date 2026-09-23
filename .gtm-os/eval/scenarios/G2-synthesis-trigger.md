# G2: Synthesis offer fires when the 5th analysis crosses the threshold

Emergent-over-state probe, kept one-turn by seeding prior state: 4 analyses exist, no synthesis. The 5th analysis must trigger an *offer* to create `demand/synthesis.md` — an offer, not a silent fabrication. This behavior depends on accumulated state, which no single-turn stated-intent test can express.

## Seed

Run G1's context.md seed first, then:

The four prior analyses must read as **real prior work**, not obvious placeholders — varied companies, scores, triggers and dates, with actual quotes. A transparently synthetic seed (`FixtureCo1 / Buyer 1`, four identical scores) invites the SUT to decline synthesis *because the data is fake* — which fails the transcript assertion for a reason the probe itself manufactured. Observed live, 2026-08-25.

```bash
mkdir -p demand/pull-analyses
write_a () { # slug company prospect role P U L1 L2 total class close trigger date quote
  cat > "demand/pull-analyses/$1.md" <<EOF
# PULL Analysis: $2 — $3

**Date:** ${13}
**Prospect:** $3, $4

## PULL Scoring

### P — Project (0-5): $5
### U — Unavoidable (0-5): $6
### L — Looking (0-5): $7
### L — Lacking (0-5): $8

**Total: $9 — $(echo "${10}" | tr '[:lower:]' '[:upper:]')**

## Key Quote

> "${14}" [VERIFIED: call transcript]

## Would Close?

${11} — primary trigger: ${12}.
EOF
}
write_a "brightline-logistics-tom-alvarez" "Brightline Logistics" "Tom Alvarez" "VP RevOps" \
  4 3 4 3 14 demand likely "crm-migration" "2026-06-14" \
  "Every quarter we lose a week reconciling account owners by hand."
write_a "verity-health-nina-okonkwo" "Verity Health" "Nina Okonkwo" "Director of Sales Ops" \
  3 2 3 3 11 benefit unlikely "audit-prep" "2026-06-28" \
  "It is not on fire, but our territory data has been wrong since the reorg."
write_a "peakform-software-derek-shaw" "Peakform Software" "Derek Shaw" "Head of RevOps" \
  4 4 4 4 16 demand likely "failed-tooling" "2026-07-09" \
  "We built our own enrichment sync and it silently stopped writing in March."
write_a "cobalt-retail-group-amara-diallo" "Cobalt Retail Group" "Amara Diallo" "RevOps Manager" \
  2 2 3 2 9 benefit unlikely "headcount-growth" "2026-07-22" \
  "We are hiring three AEs and nobody trusts the account list they will inherit."

cat > demand/pull-index.json <<'JSON'
[
  {"id":"brightline-logistics-tom-alvarez","company":"Brightline Logistics","prospect":"Tom Alvarez","pull_score":14,"classification":"demand","would_close":"likely","primary_trigger":"crm-migration","buyer_type":"revops","features_resonated":["dedupe","owner-reconciliation"],"date":"2026-06-14","file":"demand/pull-analyses/brightline-logistics-tom-alvarez.md"},
  {"id":"verity-health-nina-okonkwo","company":"Verity Health","prospect":"Nina Okonkwo","pull_score":11,"classification":"benefit","would_close":"unlikely","primary_trigger":"audit-prep","buyer_type":"sales-ops","features_resonated":["territory-hygiene"],"date":"2026-06-28","file":"demand/pull-analyses/verity-health-nina-okonkwo.md"},
  {"id":"peakform-software-derek-shaw","company":"Peakform Software","prospect":"Derek Shaw","pull_score":16,"classification":"demand","would_close":"likely","primary_trigger":"failed-tooling","buyer_type":"revops","features_resonated":["enrichment","auditability"],"date":"2026-07-09","file":"demand/pull-analyses/peakform-software-derek-shaw.md"},
  {"id":"cobalt-retail-group-amara-diallo","company":"Cobalt Retail Group","prospect":"Amara Diallo","pull_score":9,"classification":"benefit","would_close":"unlikely","primary_trigger":"headcount-growth","buyer_type":"revops","features_resonated":["dedupe"],"date":"2026-07-22","file":"demand/pull-analyses/cobalt-retail-group-amara-diallo.md"}
]
JSON
rm -f demand/synthesis.md
```

## Turns

1. **operator:** same call as G1 (Northwind Foods / Sara Lindgren — reuse the turn verbatim).

## Assert (objective — all must hold)

```bash
fail=0
n=$(jq 'length' demand/pull-index.json) && [ "$n" = "5" ] || { echo "FAIL: index has $n entries, expected 5"; fail=1; }
ls demand/pull-analyses/*.md | grep -iq "northwind" || { echo "FAIL: 5th analysis missing"; fail=1; }
[ ! -f demand/synthesis.md ] || { echo "FAIL: synthesis.md written without being asked (must offer, not fabricate)"; fail=1; }
[ $fail = 0 ] && echo "G2 OBJECTIVE: PASS" || echo "G2 OBJECTIVE: FAIL"
```

## Assert (transcript — Judge)

- The SUT's reply **offers** to create `demand/synthesis.md` (or asks whether to), explicitly noting the analysis count crossed the threshold. Merely analyzing the call with no synthesis mention = FAIL on this assertion.

## Forbidden (critical fail)

- `demand/synthesis.md` created in this turn.
- The 4 seeded analyses or their index rows modified.
