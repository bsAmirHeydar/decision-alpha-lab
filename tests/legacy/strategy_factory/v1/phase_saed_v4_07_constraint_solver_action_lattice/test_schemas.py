from tools.repository_paths import find_repository_root
from pathlib import Path
import json
from jsonschema import Draft202012Validator
ROOT=find_repository_root(__file__);S=ROOT/'schemas/legacy/strategy_factory/saed_v4_07';E=ROOT/'examples/legacy/strategy_factory/saed_v4_07'
PAIRS={'institutional_action_lattice_policy.json':'action_lattice_policy','golden_parameter_domain_registry.json':'parameter_domain_registry','golden_solver_request.json':'solver_request','golden_solver_result.json':'solver_result','golden_action_lattice.json':'action_lattice','golden_action_node.json':'action_node','golden_lattice_edge.json':'lattice_edge','golden_constraint_evaluation.json':'constraint_evaluation','golden_pruning_ledger.json':'pruning_ledger','golden_budget_ledger.json':'budget_ledger','golden_lattice_integrity_receipt.json':'lattice_integrity_receipt','golden_lattice_replay_receipt.json':'lattice_replay_receipt','golden_lattice_diff.json':'lattice_diff','golden_lattice_partition_manifest.json':'lattice_partition_manifest','golden_lattice_telemetry.json':'lattice_telemetry','golden_exposure_ledger.json':'exposure_ledger','golden_release_manifest.json':'release_manifest','golden_quarantine_record.json':'quarantine_record','golden_incident_record.json':'incident_record','v4_07_to_v4_08_handoff.json':'v4_07_to_v4_08_handoff','conformance_vectors.json':'conformance_vectors','golden_conformance_results.json':'conformance_results','schema_catalog.json':'schema_catalog'}
def test_schema_count_and_closed():
 paths=list(S.glob('*.schema.json'));assert len(paths)>=28
 for p in paths:
  x=json.loads(p.read_text());Draft202012Validator.check_schema(x);assert x['additionalProperties'] is False
def test_examples_validate():
 for e,s in PAIRS.items():
  doc=json.loads((E/e).read_text());sch=json.loads((S/f'{s}.schema.json').read_text());Draft202012Validator(sch).validate(doc)
