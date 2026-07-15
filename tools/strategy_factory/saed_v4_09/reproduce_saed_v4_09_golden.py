from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'lab/11_strategy_factory/python'))
from saed_v4_execution_twin.models import ExecutionTwinProfile
from saed_v4_execution_twin.twin import build_execution_twin
from saed_v4_execution_twin.integrity import build_integrity_receipt
from saed_v4_execution_twin.aggregation import build_summary
from saed_v4_execution_twin.telemetry import build_telemetry
from saed_v4_execution_twin.handoff import build_v4_10_handoff
from saed_v4_execution_twin.serialization import write_json
from saed_v4_execution_twin.replay import replay
from saed_v4_execution_twin.diff import semantic_diff
from saed_v4_execution_twin.conformance import run_vectors
from saed_v4_execution_twin.canonical import content_hash,stable_id
load=lambda p:json.loads((ROOT/p).read_text())
cube=load('lab/11_strategy_factory/artifacts/saed_v4_08/GOLDEN_OUTCOME_CUBE.JSON');handoff=load('lab/11_strategy_factory/artifacts/saed_v4_08/V4_08_TO_V4_09_HANDOFF.JSON');profile=ExecutionTwinProfile.from_mapping(load('lab/11_strategy_factory/examples/saed_v4_09/execution_twin_profile.json'))
twin=build_execution_twin(cube,handoff,profile);out=ROOT/'lab/11_strategy_factory/artifacts/saed_v4_09';out.mkdir(parents=True,exist_ok=True)
write_json(out/'GOLDEN_EXECUTION_TWIN.JSON',twin)
write_json(out/'GOLDEN_INTEGRITY_RECEIPT.JSON',build_integrity_receipt(twin))
write_json(out/'GOLDEN_TWIN_SUMMARY.JSON',build_summary(twin))
write_json(out/'GOLDEN_TELEMETRY.JSON',build_telemetry(twin))
write_json(out/'GOLDEN_EXPOSURE_LEDGER.JSON',twin['exposure_ledger'])
write_json(out/'V4_09_TO_V4_10_HANDOFF.JSON',build_v4_10_handoff(twin))
_, replay_receipt = replay(cube,handoff,profile,twin)
write_json(out/'GOLDEN_REPLAY_RECEIPT.JSON',replay_receipt)
write_json(out/'GOLDEN_SEMANTIC_DIFF.JSON',semantic_diff(twin,twin))
profile_registry={'phase':'SAED_V4_09','profiles':[{'profile_id':profile.profile_id,'profile_hash':profile.profile_hash,'profile_name':profile.profile_name,'exact_version':profile.exact_version,'evidence_class':profile.evidence_class,'synthetic_watermark':profile.synthetic_watermark}]}
profile_registry['registry_id']=stable_id('exectwinprofileregistry',profile_registry);profile_registry['registry_hash']=content_hash(profile_registry)
write_json(out/'PROFILE_REGISTRY.JSON',profile_registry)
scenario_manifest={'phase':'SAED_V4_09','profile_id':profile.profile_id,'profile_hash':profile.profile_hash,'scenario_count':len(profile.scenarios),'scenario_ids':[s.scenario_id for s in sorted(profile.scenarios,key=lambda x:x.scenario_id)],'scenario_hashes':{s.scenario_id:s.scenario_hash for s in sorted(profile.scenarios,key=lambda x:x.scenario_id)}}
scenario_manifest['manifest_id']=stable_id('exectwinscenarios',scenario_manifest);scenario_manifest['manifest_hash']=content_hash(scenario_manifest)
write_json(out/'GOLDEN_SCENARIO_MANIFEST.JSON',scenario_manifest)
vectors=load('lab/11_strategy_factory/test_vectors/saed_v4_09/SAED_V4_09_CONFORMANCE_VECTORS.json')
write_json(out/'CONFORMANCE_RESULTS.JSON',run_vectors(vectors,cube,handoff,load('lab/11_strategy_factory/examples/saed_v4_09/execution_twin_profile.json')))
claim_ledger={'phase':'SAED_V4_09','proven_claims':['closed-contract reference implementation','deterministic replay','complete source-row by scenario exposure','authority boundary enforcement','synthetic watermark enforcement','MQL5 static diagnostics'],'blocked_claims':['real alpha','calibrated broker fill forecast','cross-broker transport','prospective success','shadow replacement','runtime parity','production authorization','live trading'],'external_gates':{'metaeditor_compile':'pending_local_windows','broker_calibration':'pending_external','cross_broker_transport':'pending_external','prospective_paper':'not_replaced','shadow':'not_replaced','i18_qualification':'pending_future_phase'}}
claim_ledger['ledger_id']=stable_id('exectwinclaims',claim_ledger);claim_ledger['ledger_hash']=content_hash(claim_ledger)
write_json(out/'CLAIM_LEDGER.JSON',claim_ledger)
print(twin['twin_hash'])
