from conftest import CLOSURE
def test_exact_case_counts():
 assert len(list((CLOSURE/'dry_run/request_cases').glob('*.json')))==422
 assert len(list((CLOSURE/'dry_run/replay_results').glob('*.json')))==422
 assert len(list((CLOSURE/'parity/package_results').glob('*.json')))==422
 assert len(list((CLOSURE/'authority_negative/adapter_results').glob('*.json')))==483
