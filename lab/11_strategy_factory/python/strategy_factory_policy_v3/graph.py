from __future__ import annotations
from dataclasses import dataclass
from .contracts import PolicyGraphSpec,PromotionAdmission
from .enums import NodeKind,Authority,PolicyMode
from .errors import PolicyError
AI_KINDS={NodeKind.MODEL_FILTER,NodeKind.MODEL_RANK,NodeKind.MODEL_TREATMENT,NodeKind.MODEL_RISK}
AUTHORITY_BY_KIND={
NodeKind.INPUT:Authority.SYSTEM,NodeKind.MANUAL_ELIGIBILITY:Authority.MANUAL_POLICY,NodeKind.MANUAL_TREATMENT:Authority.MANUAL_POLICY,
NodeKind.MODEL_FILTER:Authority.MODEL,NodeKind.MODEL_RANK:Authority.MODEL,NodeKind.MODEL_TREATMENT:Authority.MODEL,NodeKind.MODEL_RISK:Authority.MODEL,
NodeKind.MANUAL_VETO:Authority.MANUAL_POLICY,NodeKind.OPERATOR_APPROVAL:Authority.HUMAN_OPERATOR,NodeKind.PORTFOLIO_ALLOCATION:Authority.PORTFOLIO_ENGINE,
NodeKind.RISK_GATE:Authority.RISK_ENGINE,NodeKind.KILL_SWITCH:Authority.KILL_SWITCH,NodeKind.FALLBACK:Authority.SYSTEM,NodeKind.OUTPUT:Authority.SYSTEM}
ALLOWED_CONFIG={
NodeKind.INPUT:set(),NodeKind.MANUAL_ELIGIBILITY:set(),NodeKind.MANUAL_TREATMENT:set(),NodeKind.MODEL_FILTER:{'action','minimum_probability','minimum_utility','max_uncertainty','max_novelty','allow_degraded_calibration'},
NodeKind.MODEL_RANK:{'minimum_rank'},NodeKind.MODEL_TREATMENT:set(),NodeKind.MODEL_RISK:set(),NodeKind.MANUAL_VETO:set(),NodeKind.OPERATOR_APPROVAL:{'required'},
NodeKind.PORTFOLIO_ALLOCATION:{'capacity_available','allocation_weight'},NodeKind.RISK_GATE:{'risk_rejected'},NodeKind.KILL_SWITCH:{'engaged'},NodeKind.FALLBACK:set(),NodeKind.OUTPUT:set()}
@dataclass(frozen=True,slots=True)
class CompiledGraph:
    spec:PolicyGraphSpec; topological_order:tuple[str,...]; adjacency:dict[str,tuple[str,...]]
    @property
    def graph_hash(self): return self.spec.graph_hash

def compile_graph(spec:PolicyGraphSpec,admission:PromotionAdmission|None=None)->CompiledGraph:
    ids=[n.node_id for n in spec.nodes]
    if len(ids)!=len(set(ids)): raise PolicyError('duplicate_node_id','node ids must be unique')
    by={n.node_id:n for n in spec.nodes}
    if spec.output_node_id not in by or by[spec.output_node_id].kind is not NodeKind.OUTPUT: raise PolicyError('invalid_output_node','output_node_id must identify output node')
    if sum(n.kind is NodeKind.INPUT for n in spec.nodes)!=1: raise PolicyError('input_node_count','exactly one input node required')
    if sum(n.kind is NodeKind.OUTPUT for n in spec.nodes)!=1: raise PolicyError('output_node_count','exactly one output node required')
    ai=[n for n in spec.nodes if n.kind in AI_KINDS]
    if spec.mode is PolicyMode.MANUAL_ONLY and ai: raise PolicyError('ai_node_in_manual_graph','manual-only graph cannot contain AI nodes')
    if ai:
        if admission is None: raise PolicyError('missing_promotion_admission','AI graph requires promotion admission')
        admission.assert_ai_usable(admission.valid_from_ms)
        if spec.admission_hash!=admission.admission_hash: raise PolicyError('admission_hash_mismatch','graph admission hash mismatch')
        support_checks=((spec.supported_context_types,admission.context_types,'context'),(spec.supported_treatments,admission.treatments,'treatment'),(spec.supported_risk_tiers,admission.risk_tiers,'risk'),(spec.supported_actions,admission.actions,'action'))
        for declared,promoted,label in support_checks:
            if not set(declared).issubset(set(promoted)): raise PolicyError('graph_support_exceeds_promotion',f'graph {label} support exceeds signed promotion admission')
    for n in spec.nodes:
        if n.authority is not AUTHORITY_BY_KIND[n.kind]: raise PolicyError('node_authority_mismatch',f'{n.node_id} authority does not match node kind')
        if set(n.config)-ALLOWED_CONFIG[n.kind]: raise PolicyError('unknown_node_config',f'{n.node_id} has unsupported config keys',{'keys':sorted(set(n.config)-ALLOWED_CONFIG[n.kind])})
        for d in n.dependencies:
            if d not in by: raise PolicyError('missing_dependency',f'{n.node_id} depends on missing node {d}')
    indeg={i:0 for i in ids}; adj={i:[] for i in ids}
    for n in spec.nodes:
        for d in n.dependencies: indeg[n.node_id]+=1; adj[d].append(n.node_id)
    ready=sorted(i for i,v in indeg.items() if v==0); order=[]
    while ready:
        i=ready.pop(0); order.append(i)
        for j in sorted(adj[i]):
            indeg[j]-=1
            if indeg[j]==0: ready.append(j); ready.sort()
    if len(order)!=len(ids): raise PolicyError('policy_graph_cycle','policy graph must be acyclic')
    ancestors=set(); stack=[spec.output_node_id]
    while stack:
        i=stack.pop()
        if i in ancestors:continue
        ancestors.add(i); stack.extend(by[i].dependencies)
    unreachable=set(ids)-ancestors
    if unreachable: raise PolicyError('unreachable_policy_nodes','all nodes must contribute to output',{'nodes':sorted(unreachable)})
    return CompiledGraph(spec,tuple(order),{k:tuple(sorted(v)) for k,v in adj.items()})
