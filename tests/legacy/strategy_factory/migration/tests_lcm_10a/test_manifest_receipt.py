from .conftest import j
from src.engine.tooling.strategy_factory.lcm.lcm_10a.canonical import digest_object
def test_receipt_binds_manifest_and_handoff():
 m=j('output_manifest.json');r=j('treatment_inventory_receipt.json');h=j('handoff/lcm10a_to_lcm10b_handoff.json');assert digest_object(r,'receipt_digest')==r['receipt_digest'];assert r['output_manifest_digest']==m['manifest_digest'];assert r['handoff_digest']==h['handoff_digest'];assert all(x['path'] not in {'output_manifest.json','treatment_inventory_receipt.json'} for x in m['files'])
