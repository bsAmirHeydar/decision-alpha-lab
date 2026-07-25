from __future__ import annotations
from .contracts import GraphSpec
from .validation import validate_graph_spec,validate_candidates,validate_objectives,validate_upstream
from .graph_compiler import compile_graph
from .models import encode
from .objectives import evaluate
from .budget import enforce
from .checkpoint import make_checkpoint
from .tournament import run as run_tournament
from .registry import build as build_registry
from .perturbation import future_suffix_audit,node_order_audit
from .contamination import audit_documents
from .integrity import receipt
from .replay import replay_receipt
from .provenance import build as build_provenance
from .handoff import build as build_handoff
from .claims import claim_ledger
from .security import sbom,incident_template
from .authority import boundary_record
from .canonical import content_hash

def build_reference_bundle(v405_graph,v405_receipt,v412_handoff,v412_registry,v412_distillation,v412_snapshots,graph_spec_doc,candidate_docs,objective_docs,compute_envelope):
    spec=validate_graph_spec(graph_spec_doc);candidates=validate_candidates(candidate_docs);objectives=validate_objectives(objective_docs)
    upstream=validate_upstream(v405_graph,v405_receipt,v412_handoff,v412_registry,v412_distillation)
    graph=compile_graph(v405_graph,v412_snapshots,v412_distillation,spec,v405_graph['known_as_of'])
    budget=enforce(graph,candidates,compute_envelope);encoded=[];metrics=[];checkpoints=[];future=[];order=[]
    for c in candidates:
        if not c.enabled:continue
        z=encode(graph,spec,c);m=evaluate(graph,z,objectives);encoded.append(z);metrics.append(m);checkpoints.append(make_checkpoint(c,z,m,graph));future.append(future_suffix_audit(v405_graph,graph,spec,c,compile_graph,v412_snapshots,v412_distillation));order.append(node_order_audit(graph,spec,c))
    baseline_id=next(c.candidate_id for c in candidates if c.architecture=='relation_mean_baseline')
    tournament=run_tournament(metrics,baseline_id);registry=build_registry(checkpoints,tournament)
    contamination=audit_documents(v405_graph,v412_snapshots)
    core={'compiled_graph':graph,'budget':budget,'candidate_metrics':metrics,'tournament':tournament,'checkpoint_registry':registry,'future_suffix_audits':future,'order_invariance_audits':order,'contamination_audit':contamination}
    integ=receipt(core);prov=build_provenance(upstream,graph,tournament,registry);handoff=build_handoff(v412_handoff,graph,tournament,registry,integ)
    bundle={**core,'upstream_validation':upstream,'candidate_embeddings':encoded,'candidate_checkpoints':checkpoints,'integrity_receipt':integ,'replay_receipt':replay_receipt(core,core),'provenance':prov,'handoff':handoff,'claim_ledger':claim_ledger(),'sbom':sbom(),'incident_template':incident_template(),'authority_boundary':boundary_record()}
    bundle['bundle_hash']=content_hash(bundle);return bundle
