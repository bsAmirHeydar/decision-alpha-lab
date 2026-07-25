from tools.strategy_factory.lcm.lcm_06.verify import verify_package
def test_reference_package(framework_root):
    r=verify_package(framework_root);assert r["passed"];assert r["packet_result_count"]==5;assert r["adapter_contract_count"]==4
def test_reference_manifest_nonempty(framework_root):
    import json
    m=json.loads((framework_root/"output_manifest.json").read_text());assert m["artifact_count"]>=35
def test_reference_claim_ceiling(framework_root):
    import json
    s=json.loads((framework_root/"reports/framework_summary.json").read_text());assert s["claim_ceiling"]=="MIGRATION_FRAMEWORK_REFERENCE_ONLY"
def test_no_migration_executed(framework_root):
    import json
    s=json.loads((framework_root/"reports/framework_summary.json").read_text());assert not any(s[k] for k in ["source_move_performed","source_delete_performed","target_materialization_performed","semantic_refactor_performed","merge_performed","cutover_performed"])
