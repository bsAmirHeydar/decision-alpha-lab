from src.engine.tooling.strategy_factory.lcm.lcm_05.io import read_json,read_jsonl

def test_all_artifacts_mapped(topology_root):
    marker=read_json(topology_root/'topology_marker.json');rows=read_jsonl(topology_root/'mappings/artifact_target_map.jsonl');assert len(rows)==marker['artifact_mapping_count']==38595;assert len({x['artifact_path'] for x in rows})==len(rows)
def test_all_identities_mapped(topology_root):
    marker=read_json(topology_root/'topology_marker.json');rows=read_jsonl(topology_root/'mappings/identity_target_map.jsonl');assert len(rows)==marker['identity_mapping_count']==2792;assert len({x['identity_id'] for x in rows})==len(rows)
def test_ambiguities_blocked(topology_root):
    rows=read_jsonl(topology_root/'mappings/identity_ambiguity_target_queue.jsonl');assert len(rows)==2040;assert all(x['materialization_status']=='BLOCKED_IDENTITY_AMBIGUITY' for x in rows)
def test_no_artifact_authority(topology_root):
    rows=read_jsonl(topology_root/'mappings/artifact_target_map.jsonl');keys=['source_move_authorized','source_delete_authorized','semantic_refactor_authorized','cutover_authorized','runtime_authorized','live_order_authorized','capital_authorized'];assert not any(any(x[k] for k in keys) for x in rows)
def test_protected_platform_retained(topology_root):
    rows=read_jsonl(topology_root/'mappings/identity_target_map.jsonl');protected=[x for x in rows if x['protected_platform_asset']];assert protected;assert all(x['materialization_status']=='RETAINED_IN_PLACE' for x in protected)
