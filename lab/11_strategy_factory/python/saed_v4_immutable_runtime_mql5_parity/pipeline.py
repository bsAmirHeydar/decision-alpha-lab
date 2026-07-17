from __future__ import annotations
from copy import deepcopy
from .upstream import verify_upstream
from .constitution import freeze_constitution,authority_boundary
from .abi import freeze_all
from .numeric import freeze_numeric_profile
from .clock import freeze_clock_profile,validate_timestamps
from .policy import freeze_policy_graph
from .model import freeze_linear_model
from .state import initial_state,state_ledger,transition
from .compiler import compile_bundle,verify_immutable
from .integrity import build_file_manifest,verify_file_manifest,synthetic_signature,verify_synthetic_signature
from .codegen import generate_mql5_sources
from .parity import freeze_vectors,run_synthetic_parity
from .external import freeze_external_evidence
from .release import build_release_candidate
from .governance import review_bundle
from .evidence import baseline_receipt,evidence_bundle,certificate,handoff
from .canonical import content_hash
from .errors import IntegrityError

def run_reference(f:dict)->dict:
 cutoff=f["cutoff_time"]
 upstream=verify_upstream(f["upstream"]); constitution=freeze_constitution(f["constitution"]); authority=authority_boundary()
 abis=freeze_all(f["feature_abi"],f["model_abi"],f["policy_abi"],f["output_abi"],f["state_abi"])
 feature_abi=next(x for x in abis["abis"] if x["kind"]=="FEATURE"); output_abi=next(x for x in abis["abis"] if x["kind"]=="OUTPUT")
 numeric=freeze_numeric_profile(f["numeric_profile"]); clock=freeze_clock_profile(f["clock_profile"])
 validate_timestamps(sorted(f["parity_vectors"],key=lambda x:x["known_time"]),cutoff)
 feature_names={x["name"] for x in feature_abi["fields"]}; output_names={x["name"] for x in output_abi["fields"]}
 policy=freeze_policy_graph(f["policy_graph"],feature_names,output_names); model=freeze_linear_model(f["model"],feature_names); state0=initial_state(f["initial_state"])
 bundle=compile_bundle(upstream,constitution,authority,abis,numeric,clock,policy,model,state0,f["compiler_profile"])
 if not verify_immutable(bundle):raise IntegrityError("bundle immutability failed")
 codegen=generate_mql5_sources(bundle,feature_abi,policy,model,numeric)
 files=[{k:x[k] for k in ["path","role","content_hash","size_bytes","executable","research_only"]} for x in codegen["files"]]
 manifest=build_file_manifest(files,bundle["bundle_hash"])
 if not verify_file_manifest(manifest):raise IntegrityError("manifest failed")
 signature=synthetic_signature(bundle["bundle_hash"],f["synthetic_key_id"])
 if not verify_synthetic_signature(signature):raise IntegrityError("signature envelope failed")
 vectors=freeze_vectors(f["parity_vectors"],cutoff); parity=run_synthetic_parity(vectors,policy,model,feature_abi,state0,numeric)
 external=freeze_external_evidence(f["external_evidence"])
 release=build_release_candidate(bundle,manifest,codegen,parity,external,authority)
 reviews=[]
 for r in f["reviews"]:
  x=deepcopy(r); x["release_hash"]=release["release_candidate_hash"]; y=deepcopy(x); y.pop("review_hash",None); x["review_hash"]=content_hash(y); reviews.append(x)
 review=review_bundle(reviews,release["release_candidate_hash"]); baseline=baseline_receipt(release)
 states=[state0]
 for vec in vectors["vectors"][:5]:
  d=next(x["python_decision"] for x in parity["rows"] if x["vector_id"]==vec["vector_id"]); states.append(transition(states[-1],d,vec["known_time"]))
 ledger=state_ledger(states)
 ev_items=[{"kind":"RUNTIME_BUNDLE","hash":bundle["bundle_hash"]},{"kind":"FILE_MANIFEST","hash":manifest["manifest_hash"]},{"kind":"CODEGEN","hash":codegen["codegen_hash"]},{"kind":"SYNTHETIC_PARITY","hash":parity["parity_report_hash"]},{"kind":"EXTERNAL_MATRIX","hash":external["matrix_hash"]},{"kind":"STATE_LEDGER","hash":ledger["ledger_hash"]},{"kind":"SYNTHETIC_SIGNATURE","hash":signature["signature_hash"]}]
 evidence=evidence_bundle(ev_items,release,review,baseline); cert=certificate(bundle,parity,external,release,evidence); ho=handoff(cert,bundle,external)
 return {"upstream_receipt":upstream,"constitution":constitution,"authority_boundary":authority,"abi_registry":abis,"numeric_profile":numeric,"clock_profile":clock,"policy_graph":policy,"model":model,"initial_state":state0,"runtime_bundle":bundle,"file_manifest":manifest,"synthetic_signature":signature,"codegen_manifest":codegen,"parity_vectors":vectors,"synthetic_parity_report":parity,"external_evidence_matrix":external,"release_candidate":release,"review_bundle":review,"baseline_receipt":baseline,"state_ledger":ledger,"evidence_bundle":evidence,"certificate":cert,"handoff":ho}
