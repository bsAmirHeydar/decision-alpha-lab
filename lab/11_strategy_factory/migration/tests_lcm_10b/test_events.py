from .conftest import j
def test_event_ledger_is_contiguous_and_authority_negative():
 e=j("events/treatment_boundary_event_ledger.json");assert [x["sequence"] for x in e["events"]]==list(range(1,e["event_count"]+1));assert all(not x["authority_created"] for x in e["events"])
