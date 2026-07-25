from tools.repository_paths import find_repository_root
import json,sys
from pathlib import Path
ROOT=find_repository_root(__file__);sys.path.insert(0,str(ROOT/'src/engine/packages'))
from saed_v4_immutable_runtime_mql5_parity.constitution import authority_boundary
x=authority_boundary();denied=['may_send_order','may_activate_capital','may_mutate_ucee','may_promote_model','may_claim_metaeditor_compile_without_evidence','may_claim_terminal_parity_without_evidence','may_authorize_production','live_trading_authority']
if any(x[k] for k in denied):raise SystemExit('authority expansion')
print(json.dumps({'phase':'SAED_V4_38','denied':denied,'passed':True}))
