from __future__ import annotations
from .contracts import *
from .constants import *
from .canonical import sha256,stable_id
from .profiles import PROFILES

def build_release_manifest(source_file_hashes:dict[str,str],compile_status=GateStatus.PENDING):
    composition=tuple(sorted(COMPOSITION_VERSIONS.items()))
    body={'version':RELEASE_MANIFEST_VERSION,'product':PRODUCT_NAME,'phase':PHASE_ID,'phase_version':PHASE_VERSION,'composition':composition,'profiles':tuple((p.profile_id.value,p.profile_hash) for p in PROFILES),'indicator':'mql5/Indicators/EXP0019/FaerieProtocol/EXP0019_FaerieProtocol_Context.mq5','self_test':'mql5/Tests/Indicators/EXP0019/FaerieProtocol/EXP0019_FP_I13_ReleaseSelfTest.mq5','guide':'docs/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phase_deliveries/fp_i13/70_INDICATOR_USER_GUIDE.md','open_decision':(OPEN_DECISION_ID,OPEN_DECISION_STATE),'compile_status':compile_status.value,'hashes':tuple(sorted(source_file_hashes.items()))}
    mid=stable_id('FPRELEASE',body)
    return ReleaseManifest(mid,RELEASE_MANIFEST_VERSION,PRODUCT_NAME,PHASE_ID,PHASE_VERSION,composition,PROFILES,body['indicator'],body['self_test'],body['guide'],OPEN_DECISION_ID,OPEN_DECISION_STATE,compile_status,tuple(sorted(source_file_hashes.items())),sha256(body))
