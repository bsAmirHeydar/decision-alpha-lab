#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'lab/11_strategy_factory/python'))
from strategy_factory_runtime_v3.golden import golden_bundle,golden_vectors
from strategy_factory_runtime_v3.parity import certify_parity
from strategy_factory_runtime_v3.canonical import canonical_json
m,p,model,e,data=golden_bundle();v=golden_vectors();c=certify_parity(m,p,model,data,v,created_at_ms=0)
out=ROOT/'lab/11_strategy_factory/test_vectors/v3/uce_i14_runtime_parity_vectors.json';out.write_text(canonical_json({'version':'1.0.0','bundle_hash':m.bundle_hash,'vectors':v,'certificate_hash':c.certificate_hash})+'\n');print(out)
