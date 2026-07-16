from __future__ import annotations
from .contracts import OntologyContract
from .errors import OntologyError

def compile_ontology(mapping):
    o=OntologyContract.from_mapping(mapping)
    concepts={c['concept_id']:dict(c) for c in o.concepts}
    relations={r['relation_id']:dict(r) for r in o.relations}
    return {'exact_version':o.exact_version,'concepts':concepts,'relations':relations,'closed_world':o.closed_world,'synthetic_only':o.synthetic_only}
def validate_value(spec,value):
    t=spec['value_type']
    ok=(t=='boolean' and isinstance(value,bool)) or (t=='number' and isinstance(value,(int,float)) and not isinstance(value,bool)) or (t in {'string','timestamp','category'} and isinstance(value,str))
    if not ok:raise OntologyError(f"value type mismatch for {spec['concept_id']}")
    allowed=spec.get('allowed_values',[])
    if allowed and value not in allowed:raise OntologyError(f"value outside allowed set for {spec['concept_id']}")
    return True
def validate_fact(ontology,fact,decision_time):
    keys={'fact_id','subject_id','concept_id','value','polarity','event_time','known_time','source_hash','synthetic_only'}
    if set(fact)!=keys:raise OntologyError('fact fields mismatch')
    if fact['concept_id'] not in ontology['concepts']:raise OntologyError('unknown concept')
    if fact['known_time']>decision_time:raise OntologyError('future-known fact')
    if fact['polarity'] not in {1,-1}:raise OntologyError('invalid polarity')
    if not fact['synthetic_only']:raise OntologyError('non-synthetic fact forbidden')
    validate_value(ontology['concepts'][fact['concept_id']],fact['value'])
    return True
