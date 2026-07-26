from pathlib import Path
from .io import load_json
EXPECTED='sha256:a11402e1d120630785aa127654670796f2a77278674759126d03d3104f6df26f'
def verify_upstream(repo_root:Path):
 p=repo_root/'registry/history/lcm/root_release_reorganizations/ROOTREORG_1D879F480AD3B6F4C6EDC307D43AA381/LCM15B_TO_LCM15C_HANDOFF.json'
 obj=load_json(p)
 if obj.get('handoff_digest')!=EXPECTED or obj.get('validation_status')!='PASS':raise ValueError('LCM-15B handoff mismatch')
 if obj.get('future_deletion_approved_count')!=0 or obj.get('deletion_performed'):raise ValueError('unexpected deletion authority')
 return obj
