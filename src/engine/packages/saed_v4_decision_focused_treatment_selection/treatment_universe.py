from __future__ import annotations
from .contracts import TreatmentUniverseContract
from .errors import TreatmentUniverseError
from .canonical import content_hash

def compile_treatment_universe(mapping):
    c=TreatmentUniverseContract.from_mapping(mapping)
    treatments={t['treatment_id']:dict(t) for t in c.treatments}
    enabled=tuple(sorted(k for k,v in treatments.items() if v['enabled']))
    if c.canonical_baseline not in enabled or c.skip_treatment not in enabled:raise TreatmentUniverseError('baseline and skip must be enabled')
    frozen={'exact_version':c.exact_version,'treatments':[treatments[k] for k in sorted(treatments)],'enabled_treatments':list(enabled),'canonical_baseline':c.canonical_baseline,'skip_treatment':c.skip_treatment,'closed_world':True,'runtime_mutation_allowed':False,'synthetic_only':True}
    frozen['universe_hash']=content_hash(frozen)
    return frozen

def treatment_by_id(universe,treatment_id):
    rows={x['treatment_id']:x for x in universe['treatments']}
    if treatment_id not in rows:raise TreatmentUniverseError(f'unknown treatment: {treatment_id}')
    return rows[treatment_id]
