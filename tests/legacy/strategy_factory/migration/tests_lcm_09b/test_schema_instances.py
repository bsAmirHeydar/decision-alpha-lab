import json
from jsonschema import Draft202012Validator
from .conftest import ROOT,SCHEMAS,j,jl

def validate(name,doc):
 schema=json.loads((SCHEMAS/f"{name}.schema.json").read_text()); errors=list(Draft202012Validator(schema).iter_errors(doc)); assert not errors,[e.message for e in errors[:5]]

def test_core_generated_instances_match_closed_schemas():
 for row in j("canonical_setup_registry.json")["packages"]: validate("canonical_setup_package",j(row["package_path"]))
 for row in jl("parity/setup_parity_registry.jsonl"): validate("parity_record",row)
 for row in jl("blockers/setup_blocker_registry.jsonl"): validate("blocker_record",row)
 for row in jl("dependencies/treatment_dependency_inventory_seed.jsonl"): validate("treatment_dependency_seed",row)
 validate("setup_factory_registration",j("factory/setup_factory_registration.json"))
 validate("parity_registry",j("parity/setup_parity_registry.json"))
 validate("handoff",j("handoff/lcm09b_to_lcm10a_handoff.json"))
 validate("required_artifact_locator",j("required_artifact_locator.json"))
 validate("migration_receipt",j("setup_migration_receipt.json"))
