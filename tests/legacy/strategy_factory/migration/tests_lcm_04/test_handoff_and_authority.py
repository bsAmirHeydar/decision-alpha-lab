from src.engine.tooling.strategy_factory.lcm.lcm_04.io import read_json

def test_handoff_blocks_materialization(char_root):
    h=read_json(char_root/'handoff/lcm04_to_lcm05_handoff.json');assert not h['legacy_characterization_complete'] and not h['target_path_materialization_allowed']
def test_summary_no_authority(char_root):
    s=read_json(char_root/'reports/characterization_summary.json')
    for k in ['source_move_performed','source_delete_performed','semantic_refactor_performed','merge_performed','cutover_performed','runtime_authority_created','live_order_authority_created','capital_authority_created']: assert not s[k]
