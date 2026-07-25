import pytest
from saed_v4_causal_mechanism_discovery.graph import validate_graph
from saed_v4_causal_mechanism_discovery.contracts import GraphConstraints
from saed_v4_causal_mechanism_discovery.errors import GraphError

def constraints(load):return GraphConstraints.from_mapping(load('examples/legacy/strategy_factory/saed_v4_17/reference_graph_constraints.json'))
def test_candidate_graph_valid(load):
 g=load('releases/history/strategy_factory/artifacts/saed_v4_17/GOLDEN_TEMPORAL_CANDIDATE_GRAPH.JSON')['graph'];assert validate_graph(g['nodes'],g['edges'],constraints(load))['valid']
def test_graph_acyclic(load):assert load('releases/history/strategy_factory/artifacts/saed_v4_17/GOLDEN_ACYCLICITY_AUDIT.JSON')['passed']
def test_temporal_precedence(load):assert load('releases/history/strategy_factory/artifacts/saed_v4_17/GOLDEN_TEMPORAL_PRECEDENCE_AUDIT.JSON')['all_passed']
def test_future_edge_rejected(load):
 g=load('releases/history/strategy_factory/artifacts/saed_v4_17/GOLDEN_TEMPORAL_CANDIDATE_GRAPH.JSON')['graph'];edges=list(g['edges'])+[{'source':'outcome_proxy','target':'treatment_proxy'}]
 with pytest.raises(GraphError):validate_graph(g['nodes'],edges,constraints(load))
def test_cycle_rejected(load):
 g=load('releases/history/strategy_factory/artifacts/saed_v4_17/GOLDEN_TEMPORAL_CANDIDATE_GRAPH.JSON')['graph'];c=constraints(load);pairs=[dict(e) for e in g['edges']];pairs.append({'source':'outcome_proxy','target':'context_state'})
 with pytest.raises(GraphError):validate_graph(g['nodes'],pairs,c)
def test_negative_controls_absent_from_target_edges(load):
 g=load('releases/history/strategy_factory/artifacts/saed_v4_17/GOLDEN_TEMPORAL_CANDIDATE_GRAPH.JSON')['graph'];assert not any(e['source'].startswith('negative_control') and e['target'] in {'treatment_proxy','mediator_fill_quality','outcome_proxy'} for e in g['edges'])
