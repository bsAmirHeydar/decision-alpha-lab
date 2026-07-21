from tools.strategy_factory.lcm.lcm_12b.io import load_json
def test_no_document_deletion(reconciliation_root):
    move=load_json(reconciliation_root/"documentation_move_manifest.json")
    handoff=load_json(reconciliation_root/"LCM12B_TO_LCM13A_HANDOFF.json")
    assert move["source_delete_count"]==0
    assert "DELETE_LEGACY_DOCUMENT" in handoff["forbidden_actions"]
