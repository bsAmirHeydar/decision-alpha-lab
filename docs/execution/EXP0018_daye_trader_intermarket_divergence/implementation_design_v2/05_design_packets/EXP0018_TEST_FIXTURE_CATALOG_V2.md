  ---
  id: EXP0018-FIXTURE-CATALOG-V2
  title: "EXP0018 Test Fixture Catalog v2"
  type: test-plan
  status: draft
  project: EXP0018
  version: 2.0.0
  created: 2026-07-10
  updated: 2026-07-10
  tags:
    - exp0018
- daye-trader
- implementation-design
  ---

# کاتالوگ Fixtureها

## Time
- DST spring/fall
- 18:00 rollover
- p4 tail
- 17:00 gap

## Hunt/Confirmation
- equal high/low touch
- one-sided high/low
- double hunt before close
- multiple relationships same candle

## Lifecycle
- protected survives
- protected later hunts and retires
- same reference different composite key
- retired reference attempted reuse

## Visual
- hunter-only high/low line
- major label / minor no label
- object idempotency

## Replay
- live vs historical event hashes
- missing bar / reconnect
- DST week

هر fixture دارای expected event ledger، expected visual coordinates و reason code است.
