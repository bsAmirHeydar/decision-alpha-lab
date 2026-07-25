from tools.repository_paths import find_repository_root
from pathlib import Path
from tools.strategy_factory.lcm.lcm_14b.service import LCM14BQuarantineObservationService
def test_service_in_place():
 root=find_repository_root(__file__); r=LCM14BQuarantineObservationService(root).build(Path("registry/legacy_context_migration/quarantine_observations")); assert r.package_count==136 and r.proof_eligible_count==136
