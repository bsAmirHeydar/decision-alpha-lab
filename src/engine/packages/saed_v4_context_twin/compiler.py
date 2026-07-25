from __future__ import annotations
from dataclasses import asdict
from .models import *
from .enums import *
from .canonical import content_hash,stable_id,normalize_time
from .authority import default_boundary,assert_safe_boundary
from .ontology import OntologyGraph
from .lifecycle import LifecycleMachine
from .errors import ContractError,IdentityError
COMPILER_VERSION='saed-v4-02-twin-compiler/1.0.0'

def _tuple_str(xs):return tuple(str(x) for x in xs)
def compile_twin(context_spec:dict,seed:dict,exact_version='1.0.0')->ContextTwinManifest:
    required={'context_id','context_version','artifact_id','specification_hash','ucee_phase','schema_version','ontology_terms','ontology_relations','observables','hypotheses','support_geometry','lifecycle_states','transition_rules','initial_lifecycle_state','limitations'}
    unknown=set(context_spec)-required;missing=required-set(context_spec)
    if unknown:raise ContractError('unknown context spec fields: '+','.join(sorted(unknown)))
    if missing:raise ContractError('missing context spec fields: '+','.join(sorted(missing)))
    sreq={'package_id','package_hash','lineage_root','known_as_of','constitution_hash','snapshot_ids','schema_versions','limitations','context_specification_artifact_id'}
    if set(seed)!=sreq:raise ContractError('invalid twin seed fields')
    if seed['context_specification_artifact_id']!=context_spec['artifact_id']:raise IdentityError('seed context artifact mismatch')
    cref=ContextSpecificationRef(context_spec['context_id'],context_spec['context_version'],context_spec['artifact_id'],context_spec['specification_hash'],context_spec['ucee_phase'],context_spec['schema_version'])
    sref=TwinSeedRef(seed['package_id'],seed['package_hash'],seed['lineage_root'],normalize_time(seed['known_as_of']),seed['constitution_hash'],tuple(sorted(seed['snapshot_ids'])),dict(sorted(seed['schema_versions'].items())),tuple(seed['limitations']))
    terms=tuple(sorted((OntologyTerm(**x) for x in context_spec['ontology_terms']),key=lambda x:x.term_id))
    rels=tuple(sorted((OntologyRelation(x['source_term_id'],x['target_term_id'],RelationKind(x['relation_kind']),x.get('source_ref','')) for x in context_spec['ontology_relations']),key=lambda x:x.relation_id))
    OntologyGraph(terms,rels)
    obs=tuple(sorted((ObservableDefinition(x['observable_id'],x['name'],x['value_type'],x['required'],x['canonical_source'],x.get('unit'),tuple(x.get('allowed_values',[])),x.get('minimum'),x.get('maximum'),x.get('freshness_seconds')) for x in context_spec['observables']),key=lambda x:x.observable_id))
    hyps=tuple(sorted((LatentHypothesis(**x) for x in context_spec['hypotheses']),key=lambda x:x.hypothesis_id))
    gd=context_spec['support_geometry']
    dims=tuple(sorted((SupportDimension(x['dimension_id'],x['observable_id'],x['required'],tuple(x.get('allowed_values',[])),x.get('minimum'),x.get('maximum'),x.get('maximum_age_seconds'),x.get('weight',1.0)) for x in gd['dimensions']),key=lambda x:x.dimension_id))
    observable_ids={x.observable_id for x in obs}
    if any(d.observable_id not in observable_ids for d in dims):raise ContractError('support references unknown observable')
    geometry=SupportGeometry(gd['geometry_id'],dims,gd['minimum_coverage'],gd['unknown_policy'],gd['degraded_threshold'])
    states=tuple(sorted((LifecycleStateDefinition(**x) for x in context_spec['lifecycle_states']),key=lambda x:x.state_id))
    rules=tuple(sorted((TransitionRule(x['rule_id'],x['from_state'],x['to_state'],x['trigger'],tuple(x.get('required_observables',[])),tuple(x.get('forbidden_contradiction_severities',[])),x.get('requires_support',False),x.get('review_required',False)) for x in context_spec['transition_rules']),key=lambda x:x.rule_id))
    LifecycleMachine(states,rules,context_spec['initial_lifecycle_state'])
    authority=default_boundary();assert_safe_boundary(authority)
    identity={'context_ref':cref.to_dict(),'seed_ref':sref.to_dict(),'compiler_version':COMPILER_VERSION,'exact_version':exact_version}
    twin_id=stable_id('twin',identity)
    provisional=ContextTwinManifest(twin_id,exact_version,COMPILER_VERSION,cref,sref,terms,rels,obs,hyps,geometry,states,rules,context_spec['initial_lifecycle_state'],TwinState.INITIALIZED,authority,tuple(context_spec['limitations'])+tuple(seed['limitations']),'')
    semantic_hash=content_hash(provisional.semantic_payload())
    return ContextTwinManifest(**{**provisional.__dict__,'semantic_hash':semantic_hash})
