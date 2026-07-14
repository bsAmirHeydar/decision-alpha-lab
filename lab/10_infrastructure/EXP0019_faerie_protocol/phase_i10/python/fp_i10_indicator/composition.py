from pathlib import Path
import json
from .contracts import UpstreamModuleDescriptor,CompositionManifest,IndicatorConfig
from .constants import EXPECTED_UPSTREAM,COMPOSITION_VERSION,NO_RUNTIME_AUTHORITY
from .canonical import canonical_sha256,stable_id
from .enums import ModuleStatus
from .errors import FPI10InitializationError

def build_composition(config:IndicatorConfig, modules:tuple[UpstreamModuleDescriptor,...])->CompositionManifest:
    expected=dict(EXPECTED_UPSTREAM)
    if tuple(m.phase_id for m in modules)!=tuple(expected): raise FPI10InitializationError('FP_IND_UPSTREAM_SEQUENCE_MISMATCH','upstream phases must be exact I03-I09 sequence')
    reasons=[]
    for m in modules:
        if m.version!=expected[m.phase_id]: reasons.append(f'{m.phase_id}_VERSION')
        if m.authority!=NO_RUNTIME_AUTHORITY: reasons.append(f'{m.phase_id}_AUTHORITY')
        if m.status is ModuleStatus.BLOCKED: reasons.append(f'{m.phase_id}_BLOCKED')
    if reasons and config.fail_init_on_blocked_manifest: raise FPI10InitializationError('FP_IND_UPSTREAM_MANIFEST_BLOCKED',','.join(reasons))
    payload={'version':COMPOSITION_VERSION,'config_hash':config.config_hash,'modules':[m.descriptor_hash for m in modules]}
    return CompositionManifest(stable_id('FPCOMP',payload),COMPOSITION_VERSION,config.config_hash,modules,canonical_sha256(payload))

def descriptors_from_repository(root:Path)->tuple[UpstreamModuleDescriptor,...]:
    root=Path(root); out=[]
    for phase,version in EXPECTED_UPSTREAM:
        n=phase.split('-I')[1]
        candidates=list((root/f'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i{n}/artifacts').glob(f'FP_I{n}_*STATUS*.json'))
        status=ModuleStatus.READY; reasons=()
        if not candidates:
            status=ModuleStatus.BLOCKED; reasons=('FP_IND_UPSTREAM_STATUS_MISSING',)
            contract_hash=canonical_sha256({'phase':phase,'missing':True})
        else:
            data=json.loads(candidates[0].read_text(encoding='utf-8'))
            raw=str(data.get('status','')).upper()
            status=ModuleStatus.BLOCKED if 'BLOCK' in raw or 'FAIL' in raw else ModuleStatus.READY
            contract_hash=canonical_sha256(data)
        out.append(UpstreamModuleDescriptor(phase,version,contract_hash,NO_RUNTIME_AUTHORITY,status,reasons))
    return tuple(out)
