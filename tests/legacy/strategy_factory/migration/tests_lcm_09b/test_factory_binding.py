from tools.strategy_factory.lcm.lcm_09b.factory_bridge import SetupFactoryReferencePort
from .conftest import ROOT
def test_factory_reference_port_is_read_only_and_complete():
 port=SetupFactoryReferencePort(ROOT/"factory/setup_factory_registration.json");rows=port.list_reference_candidates();assert len(rows)==60;assert all(x["registration_status"]=="REFERENCE_BLOCKED" for x in rows)
def test_factory_has_zero_authority():
 rows=SetupFactoryReferencePort(ROOT/"factory/setup_factory_registration.json").list_reference_candidates();assert all(not x[k] for x in rows for k in ("promotion_authority","runtime_authority","live_order_authority","capital_authority"))
