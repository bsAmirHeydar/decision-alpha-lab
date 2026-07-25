from tools.strategy_factory.acl_os.acl_04.legacy_reference import open_legacy_reference_port
from .conftest import ROOT
def test_acl04_public_extension_opens_reference_registry():assert len(open_legacy_reference_port(ROOT/"factory/setup_factory_registration.json").list_reference_candidates())==60
