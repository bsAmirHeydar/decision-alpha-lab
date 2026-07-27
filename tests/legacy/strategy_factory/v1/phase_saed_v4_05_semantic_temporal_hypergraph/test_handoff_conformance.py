from .helpers import build_graph, build_package
from saed_v4_semantic_hypergraph.conformance import run_conformance
from saed_v4_semantic_hypergraph.handoff import build_v4_06_handoff
from saed_v4_semantic_hypergraph.integrity import build_integrity_receipt


def test_v4_06_handoff_is_hash_bound_and_non_authoritative():
    graph = build_graph()
    handoff = build_v4_06_handoff(graph, build_integrity_receipt(graph))
    assert handoff["phase"] == "SAED_V4_05"
    assert handoff["next_phase"] == "SAED_V4_06"
    assert handoff["graph_hash"] == graph.graph_hash
    assert handoff["authority"]["generate_treatment"] is False
    assert handoff["authority"]["select_treatment"] is False
    assert handoff["authority"]["send_order"] is False
    assert len(handoff["handoff_hash"]) == 64


def test_conformance_suite_passes():
    result = run_conformance(build_package())
    assert result["status"] == "pass"
    assert all(result["checks"].values())
