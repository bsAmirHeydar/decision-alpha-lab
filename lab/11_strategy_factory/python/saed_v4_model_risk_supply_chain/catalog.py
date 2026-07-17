from __future__ import annotations
from copy import deepcopy
from .contracts import require_exact,require_list,require_unique,require_sha256,require_time_before,require_sorted_unique_strings
from .errors import CatalogError
from .canonical import seal

def _freeze(items:list[dict],kind:str,id_field:str,required:list[str],cutoff:str,minimum:int=1)->dict:
    items=require_list(items,kind,minimum); require_unique(items,id_field,kind); out=[]
    for x in items:
        require_exact(x,required); require_sha256(x["content_hash"],f"{kind}.content_hash"); require_time_before(x["known_time"],cutoff,f"{kind}.known_time")
        if x.get("immutable") is not True or x.get("status")!="approved-reference": raise CatalogError(f"{kind} must be immutable approved-reference")
        out.append(deepcopy(x))
    return seal({"phase":"SAED_V4_35","kind":kind,"records":sorted(out,key=lambda x:x[id_field]),"record_count":len(out),"cutoff_time":cutoff,"research_only":True},f"v435_{kind}","registry_id","registry_hash")

def freeze_models(items,cutoff):return _freeze(items,"models","model_id",["model_id","model_family","version","content_hash","architecture_hash","training_evidence_hash","owner_id","known_time","immutable","status","external_origin","capabilities"],cutoff,2)
def freeze_datasets(items,cutoff):return _freeze(items,"datasets","dataset_id",["dataset_id","data_role","version","content_hash","schema_hash","lineage_hash","owner_id","known_time","immutable","status","license_id","contains_personal_data"],cutoff,2)
def freeze_dependencies(items,cutoff):return _freeze(items,"dependencies","dependency_id",["dependency_id","name","version","ecosystem","content_hash","supplier_id","known_time","immutable","status","license_id","direct","build_only"],cutoff,4)
def freeze_tools(items,cutoff):return _freeze(items,"tools","tool_id",["tool_id","name","version","content_hash","supplier_id","known_time","immutable","status","license_id","network_capable"],cutoff,2)
def freeze_runtimes(items,cutoff):return _freeze(items,"runtimes","runtime_id",["runtime_id","image_ref","content_hash","base_image_hash","builder_id","known_time","immutable","status","network_egress_default_deny"],cutoff,2)
def freeze_services(items,cutoff):return _freeze(items,"external_services","service_id",["service_id","service_name","version","content_hash","supplier_id","known_time","immutable","status","data_export_allowed","contract_hash"],cutoff,1)
