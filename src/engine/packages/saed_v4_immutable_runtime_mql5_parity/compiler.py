from __future__ import annotations
from copy import deepcopy
from .contracts import exact
from .errors import CompilerError
from .canonical import content_hash,merkle_root,seal

def compile_bundle(upstream:dict,constitution:dict,authority:dict,abis:dict,numeric:dict,clock:dict,policy:dict,model:dict,state:dict,compiler:dict)->dict:
 exact(compiler,["compiler_id","compiler_version","source_language","target_runtime","optimization_level","deterministic_build","network_access","environment_variables_allowed","build_timestamp_policy","research_only"])
 if compiler["deterministic_build"] is not True or compiler["network_access"] is not False or compiler["environment_variables_allowed"] is not False or compiler["build_timestamp_policy"]!="OMIT":raise CompilerError("compiler is not hermetic")
 components={"upstream":upstream["receipt_hash"],"constitution":constitution["constitution_hash"],"authority":authority["boundary_hash"],"abis":abis["registry_hash"],"numeric":numeric["profile_hash"],"clock":clock["clock_hash"],"policy":policy["frozen_graph_hash"],"model":model["frozen_model_hash"],"state":state["state_hash"],"compiler":content_hash(compiler)}
 root=merkle_root(list(components.values()))
 body={"phase":"SAED_V4_38","bundle_format":"SAED_IMMUTABLE_RUNTIME_BUNDLE_V1","bundle_version":"1.0.0","components":dict(sorted(components.items())),"component_count":len(components),"merkle_root":root,"compiler":deepcopy(compiler),"mutable_fields":[],"network_dependencies":[],"runtime_authority":"RESEARCH_DECISION_ONLY","research_only":True,"production_authorized":False}
 return seal(body,"v438_bundle","bundle_id","bundle_hash")

def verify_immutable(bundle:dict)->bool:
 if bundle.get("mutable_fields")!=[] or bundle.get("network_dependencies")!=[] or bundle.get("production_authorized") is not False:return False
 root=merkle_root(list(bundle["components"].values()))
 return root==bundle["merkle_root"]
