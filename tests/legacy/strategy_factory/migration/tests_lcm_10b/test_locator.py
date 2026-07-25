from .conftest import ROOT,j
from tools.strategy_factory.lcm.lcm_10b.canonical import digest_object
def test_required_artifact_locator_is_complete():
 d=j("required_artifact_locator.json");assert d["locator_digest"]==digest_object(d,"locator_digest");assert len(d["artifacts"])==7
 for x in d["artifacts"].values():assert (ROOT/x["path"]).exists()
