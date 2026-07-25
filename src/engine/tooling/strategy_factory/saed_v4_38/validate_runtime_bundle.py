from tools.repository_paths import find_repository_root
import copy,json,sys
from pathlib import Path
ROOT=find_repository_root(__file__);sys.path.insert(0,str(ROOT/'src/engine/packages'))
from saed_v4_immutable_runtime_mql5_parity.compiler import verify_immutable
from saed_v4_immutable_runtime_mql5_parity.integrity import verify_file_manifest,verify_synthetic_signature
out=json.loads((ROOT/'examples/legacy/strategy_factory/saed_v4_38/reference_output.json').read_text())
if not verify_immutable(out['runtime_bundle']):raise SystemExit('bundle invalid')
if not verify_file_manifest(out['file_manifest']):raise SystemExit('manifest invalid')
if not verify_synthetic_signature(out['synthetic_signature']):raise SystemExit('signature invalid')
x=copy.deepcopy(out['runtime_bundle']);x['components']['model']='0'*64
if verify_immutable(x):raise SystemExit('tamper not detected')
print(json.dumps({'phase':'SAED_V4_38','bundle_hash':out['runtime_bundle']['bundle_hash'],'tamper_detection':True,'passed':True}))
