from .conftest import ROOT,j
from tools.strategy_factory.lcm.lcm_10a.canonical import digest_object
def test_named_locator_is_complete():
 d=j('required_artifact_locator.json');assert digest_object(d,'locator_digest')==d['locator_digest'];assert len(d['artifacts'])==7
 for item in d['artifacts'].values():assert (ROOT/item['path']).is_file()
