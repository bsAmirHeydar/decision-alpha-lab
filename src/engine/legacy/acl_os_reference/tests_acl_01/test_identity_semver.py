import pytest
from src.engine.tooling.strategy_factory.acl_os.acl_01.identity import build_artifact_id,parse_artifact_id,validate_component
from src.engine.tooling.strategy_factory.acl_os.acl_01.errors import IdentityError,ContractError
from src.engine.tooling.strategy_factory.acl_os.acl_01.semver import Version,satisfies,highest_satisfying

@pytest.mark.parametrize("value",["alpha","alpha-1","ctx_nds","a1","a-b_c2"])
def test_valid_components(value): validate_component(value)
@pytest.mark.parametrize("value",["Alpha","1alpha","alpha space","alpha/child","a..b","","a-","_alpha"])
def test_invalid_components(value):
    with pytest.raises(IdentityError): validate_component(value)

def test_artifact_identity_roundtrip():
    aid=build_artifact_id("alpha","nds","context_contract","occurrence","1.2.3")
    assert parse_artifact_id(aid)["base_id"]=="al://alpha/nds/context_contract/occurrence"

@pytest.mark.parametrize("version",["0.0.0","1.2.3","10.20.30","1.0.0-alpha","1.0.0+build.1"])
def test_semver_valid(version): assert str(Version.parse(version))==version
@pytest.mark.parametrize("version",["1","1.2","01.2.3","v1.2.3","1.2.3.4",""])
def test_semver_invalid(version):
    with pytest.raises(ContractError): Version.parse(version)
@pytest.mark.parametrize("version,constraint,expected",[("1.2.3","^1.0.0",True),("2.0.0","^1.0.0",False),("0.2.4","^0.2.0",True),("0.3.0","^0.2.0",False),("1.2.9","~1.2.0",True),("1.3.0","~1.2.0",False),("1.2.3",">=1.0.0,<2.0.0",True),("2.0.0",">=1.0.0,<2.0.0",False),("1.5.0","1.x",True),("2.0.0","1.x",False),("1.2.9","1.2.x",True),("1.2.3","1.2.3",True)])
def test_constraints(version,constraint,expected): assert satisfies(version,constraint) is expected

def test_highest_satisfying(): assert highest_satisfying(["1.0.0","1.5.0","2.0.0"],"^1.0.0")=="1.5.0"
