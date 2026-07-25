from tools.strategy_factory.lcm.lcm_05.io import read_json,read_jsonl

def test_root_plan_complete(topology_root):
    rows=read_jsonl(topology_root/'root_relocation/root_relocation_plan.jsonl');summary=read_json(topology_root/'reports/topology_summary.json');assert len(rows)==summary['root_relocation_plan_count'];assert all(not x['move_performed'] and not x['delete_performed'] for x in rows)
def test_root_canonical_retained(topology_root):
    rows=read_jsonl(topology_root/'root_relocation/root_relocation_plan.jsonl');canonical=[x for x in rows if x['source_classification']=='ROOT_CANONICAL'];assert canonical;assert all(x['target_outcome']=='RETAIN_CURRENT' for x in canonical)
def test_doc_successors_non_destructive(topology_root):
    rows=read_jsonl(topology_root/'documentation/documentation_successor_map.jsonl');assert rows;assert all(not x['deletion_authorized'] and not x['redirect_materialized'] for x in rows)
def test_master_architecture_selected(topology_root):
    rows=read_jsonl(topology_root/'documentation/documentation_successor_map.jsonl');dups=[x for x in rows if x['relationship']=='EXACT_BYTE_DUPLICATE_TREE'];assert dups;assert all(x['canonical_successor'].startswith('docs/alpha_lab_master_architecture/') for x in dups)
