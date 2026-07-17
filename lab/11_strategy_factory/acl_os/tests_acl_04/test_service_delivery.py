from pathlib import Path
import hashlib
import json
from tools.strategy_factory.acl_os.acl_04.service import ACL04DualSetupFactoryService
from tools.strategy_factory.acl_os.acl_04.canonical import verify_embedded_digest


def build(fixtures,out):
    return ACL04DualSetupFactoryService().build(compiled_root=fixtures['acl03'],output_root=out,authority_permit=fixtures['permit'],search_authority=fixtures['search'],treatment_envelope=fixtures['envelope'],human_setups=[fixtures['human']],ai_requests=[fixtures['ai']])


def test_service_writes_complete_output(fixtures,tmp_path):
    result=build(fixtures,tmp_path/'out')
    assert result['passed']
    assert result['source_candidate_count']==12
    assert result['canonical_candidate_count']>=10
    for rel in ['factory_receipt.json','output_manifest.json','handoff/acl05_handoff.json','reports/deduplication_report.json','reports/search_exposure_ledger.json','lineage/provenance_graph.json','docs/ACL04_FACTORY_SUMMARY.md']:
        assert (tmp_path/'out'/rel).is_file()
    assert verify_embedded_digest(result['receipt'],'receipt_digest')
    assert verify_embedded_digest(result['handoff'],'handoff_digest')
    assert result['handoff']['live_order_submission_allowed'] is False
    assert result['handoff']['capital_activation_allowed'] is False


def test_output_manifest_matches_files(fixtures,tmp_path):
    result=build(fixtures,tmp_path/'out')
    for item in result['output_manifest']['files']:
        path=tmp_path/'out'/item['path']
        assert 'sha256:'+hashlib.sha256(path.read_bytes()).hexdigest()==item['digest']


def test_replay_is_deterministic(fixtures,tmp_path):
    a=build(fixtures,tmp_path/'a');b=build(fixtures,tmp_path/'b')
    assert a['receipt']['receipt_digest']==b['receipt']['receipt_digest']
    assert a['handoff']['handoff_digest']==b['handoff']['handoff_digest']
    assert [c['candidate_digest'] for c in a['canonical_candidates']]==[c['candidate_digest'] for c in b['canonical_candidates']]


def test_owned_output_root_required(fixtures,tmp_path):
    out=tmp_path/'out';out.mkdir();(out/'foreign.txt').write_text('x')
    import pytest
    with pytest.raises(RuntimeError): build(fixtures,out)


def test_no_baselines_mode(fixtures,tmp_path):
    result=ACL04DualSetupFactoryService().build(compiled_root=fixtures['acl03'],output_root=tmp_path/'out',authority_permit=fixtures['permit'],search_authority=fixtures['search'],treatment_envelope=fixtures['envelope'],human_setups=[fixtures['human']],ai_requests=[],include_baselines=False)
    assert result['source_candidate_count']==1
    assert result['diagnostic_candidate_count']==0
