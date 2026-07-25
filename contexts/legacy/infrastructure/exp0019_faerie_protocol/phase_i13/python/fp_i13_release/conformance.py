from .constants import COMPOSITION_VERSIONS,OPEN_DECISION_STATE
from .profiles import PROFILES

def run_conformance():
    checks={
      'composition_i03_i12_exact':tuple(COMPOSITION_VERSIONS)==tuple(f'FP-I{i:02d}' for i in range(3,13)),
      'profiles_unique':len({x.profile_id for x in PROFILES})==len(PROFILES),
      'profile_hashes_present':all(len(x.profile_hash)==64 for x in PROFILES),
      'open_decision_unset':OPEN_DECISION_STATE=='UNSET',
      'no_live_authority':True,
    }
    return checks
