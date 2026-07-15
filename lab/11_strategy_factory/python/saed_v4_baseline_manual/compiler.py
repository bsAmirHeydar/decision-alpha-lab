from __future__ import annotations
from .canonical import content_hash, stable_id
from .feature_space import feature_registry
from .models import ManualProgram
from .validation import validate_program

def compile_program(source:dict,view_package:dict,lattice:dict)->dict:
    registry=feature_registry(view_package)
    program=ManualProgram.from_mapping(source)
    validate_program(program,registry,lattice)
    ordered=sorted(program.rules,key=lambda r:(-r.priority,r.rule_id))
    semantic={
      "phase":"SAED_V4_10","program_name":program.program_name,"exact_version":program.exact_version,
      "evidence_role":program.evidence_role,"authoring_basis":program.authoring_basis,
      "rules":[{"rule_id":r.rule_id,"priority":r.priority,"predicates":[p.__dict__ for p in r.predicates],"action_node_id":r.action_node_id,"reason_code":r.reason_code} for r in ordered],
      "fallback_node_id":program.fallback_node_id,"feature_registry_hash":content_hash(registry),
      "source_lattice_hash":lattice['lattice_hash'],"source_view_package_hash":view_package['package_hash'],
      "selection_authority":False,"execution_authority":False,"learning_semantics":"none",
      "limitations":["Human-authored deterministic reference program only.","No outcome-derived predicate, parameter fitting, treatment ranking, capital allocation or execution authority."]
    }
    semantic['compiled_program_id']=stable_id('manualprogram',semantic)
    semantic['compiled_program_hash']=content_hash(semantic)
    return semantic
