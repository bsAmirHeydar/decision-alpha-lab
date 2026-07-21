from tools.strategy_factory.lcm.lcm_12a.io import load_jsonl
def test_reference_edge_count(mapping_root,load):
    graph=load("documentation_inbound_reference_graph.json")
    edges=load_jsonl(mapping_root/graph["edges_path"])
    assert len(edges)==graph["edge_count"]
    assert all(e["target_document_id"] for e in edges)
