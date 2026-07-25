from tools.strategy_factory.lcm.lcm_15a.service import LCM15ADeletionCandidateService
def test_service(repo_root,proof_root):
 r=LCM15ADeletionCandidateService(repo_root).verify(proof_root);assert r.validation_status=="PASS"
