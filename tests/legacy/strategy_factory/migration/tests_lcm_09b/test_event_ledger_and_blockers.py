from .conftest import j,jl

def test_event_ledger_is_contiguous_and_unique():
 d=j("events/setup_migration_event_ledger.json"); rows=d["events"]
 assert d["event_count"]==60; assert [x["sequence"] for x in rows]==list(range(1,61)); assert len({x["subject_id"] for x in rows})==60

def test_every_package_blocker_is_present_in_global_registry():
 global_ids={x["blocker_id"] for x in jl("blockers/setup_blocker_registry.jsonl")}
 for row in j("canonical_setup_registry.json")["packages"]:
  p=j(row["package_path"]); assert set(p["blocker_ids"])<=global_ids
