from fp_i13_release import *
def test_four_profiles():assert len(PROFILES)==4
def test_profile_hashes_valid():assert all(len(x.profile_hash)==64 for x in PROFILES)
def test_audit_profile_export_enabled():assert get_profile('AUDIT_90D').audit_export_enabled
def test_performance_profile_minimal():assert get_profile('PERFORMANCE_7D').visual_mode=='MINIMAL'
def test_release_manifest_open_decision():
 m=build_release_manifest({'a':'0'*64});assert m.open_decision_id=='FP-DEC-012' and m.open_decision_state=='UNSET'
def test_release_manifest_compile_pending():assert build_release_manifest({'a':'0'*64}).metaeditor_compile_status==GateStatus.PENDING
