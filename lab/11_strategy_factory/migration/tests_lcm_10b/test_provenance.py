from .conftest import j
def test_provenance_counts_are_consistent():
 p=j("provenance/treatment_boundary_provenance_graph.json");assert p["node_count"]==len(p["nodes"])==905;assert p["edge_count"]==len(p["edges"])
