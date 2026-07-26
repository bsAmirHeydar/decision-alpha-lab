from src.engine.tooling.strategy_factory.lcm.lcm_04.io import read_json,read_jsonl

def test_packet_coverage(char_root):
    s=read_json(char_root/'reports/characterization_summary.json');packets=list(read_jsonl(char_root/'packets/characterization_packet_index.jsonl'))
    assert len(packets)==s['identity_packet_count'] and all(not x['source_mutation_allowed'] for x in packets)
def test_no_legacy_execution_eligibility(char_root): assert not any(x['legacy_execution_allowed'] for x in read_jsonl(char_root/'packets/characterization_packet_index.jsonl'))
def test_static_profiles_are_not_behavioral_proof(char_root): assert all(not x['static_profile_is_behavioral_proof'] for x in read_jsonl(char_root/'profiles/source_static_profiles.jsonl'))
