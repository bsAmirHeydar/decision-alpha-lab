from tools.repository_paths import find_repository_root
from pathlib import Path
from tools.strategy_factory.acl_os.acl_04.legacy_reference import open_legacy_reference_port
REPO=find_repository_root(__file__)
def test_lcm09b_reference_port_does_not_widen_factory_authority():
 p=REPO/"registry/legacy_context_migration/setup_package_migrations/SETUPMIGRATION_8F5CED333AA143A8F2A798BA01D550D9/factory/setup_factory_registration.json"
 rows=open_legacy_reference_port(p).list_reference_candidates();assert len(rows)==60;assert all(x["live_order_authority"] is False and x["capital_authority"] is False for x in rows)
