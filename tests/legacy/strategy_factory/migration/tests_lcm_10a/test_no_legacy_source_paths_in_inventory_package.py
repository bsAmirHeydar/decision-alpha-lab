from .conftest import ROOT
def test_generated_package_contains_evidence_only():
 assert not any(p.suffix.lower() in {'.mq5','.mqh'} for p in ROOT.rglob('*') if p.is_file())
