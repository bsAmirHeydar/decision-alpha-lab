from pathlib import Path
from tools.strategy_factory.lcm.lcm_14b.service import LCM14BQuarantineObservationService
def test_service_in_place():
 root=Path(__file__).resolve().parents[4]; r=LCM14BQuarantineObservationService(root).build(Path("registry/legacy_context_migration/quarantine_observations")); assert r.package_count==136 and r.proof_eligible_count==136
