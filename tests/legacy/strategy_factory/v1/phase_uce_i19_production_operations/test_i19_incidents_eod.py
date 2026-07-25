import pytest
from strategy_factory_operations_v3.eod import evaluate_eod
from strategy_factory_operations_v3.enums import ControlDecision, IncidentSeverity, IncidentState
from strategy_factory_operations_v3.errors import OperationsError
from strategy_factory_operations_v3.golden import H1, H2, H3, H4, NOW, eod, envelope
from strategy_factory_operations_v3.incidents import close_incident, contain_incident, open_incident, resolve_incident


def test_incident_lifecycle_requires_ordered_transitions():
    incident = open_incident("i", IncidentSeverity.HIGH, NOW, H1, H2, "reject-spike", (H3,), "owner")
    contained = contain_incident(incident, NOW+1, H4)
    resolved = resolve_incident(contained, NOW+2, H3)
    closed = close_incident(resolved, NOW+3, "reviewer", H4)
    assert closed.state is IncidentState.CLOSED and closed.closed_by == "reviewer"


def test_cannot_resolve_open_incident():
    incident = open_incident("i", IncidentSeverity.HIGH, NOW, H1, H2, "x", (H3,), "owner")
    with pytest.raises(OperationsError): resolve_incident(incident, NOW+1, H4)


def test_cannot_close_contained_incident():
    incident = contain_incident(open_incident("i", IncidentSeverity.HIGH, NOW, H1, H2, "x", (H3,), "owner"), NOW+1, H4)
    with pytest.raises(OperationsError): close_incident(incident, NOW+2, "reviewer", H3)


def test_incident_owner_cannot_self_close():
    incident = resolve_incident(contain_incident(open_incident("i", IncidentSeverity.HIGH, NOW, H1, H2, "x", (H3,), "owner"), NOW+1, H4), NOW+2, H3)
    with pytest.raises(OperationsError, match="incident_sod"): close_incident(incident, NOW+3, "owner", H4)


def test_clean_eod_holds_for_next_session():
    assert evaluate_eod(eod(), envelope()) == (ControlDecision.HOLD, ())


@pytest.mark.parametrize("changes,reason", [
    ({"all_events_persisted":False}, "events_not_persisted"),
    ({"all_intents_terminal":False}, "non_terminal_intent"),
    ({"exact_reconciliation":False}, "eod_reconciliation_failed"),
    ({"unresolved_high_incidents":1}, "unresolved_high_incident"),
    ({"unresolved_critical_incidents":1}, "unresolved_critical_incident"),
    ({"daily_loss_units":.16}, "daily_loss_limit"),
])
def test_eod_failures_halt(changes, reason):
    decision, reasons = evaluate_eod(eod(**changes), envelope())
    assert decision is ControlDecision.SAFE_HALT and reason in reasons
