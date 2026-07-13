"""Cross-run conformance vectors for I12 identities and decisions."""
from __future__ import annotations
from dataclasses import asdict
from .canonical import canonical_sha256
from .golden import golden_family_definition, golden_policy, golden_universe
from .multiplicity import multiplicity_report
from .registry import registry_snapshot

def generate_vectors()->dict[str,object]:
    universe=golden_universe(); definition=golden_family_definition(); report=multiplicity_report(universe,definition); registry=registry_snapshot()
    payload={"universe_hash":universe.universe_hash,"policy_hash":golden_policy().policy_hash,"family_definition_hash":canonical_sha256(asdict(definition)),"multiplicity_evidence_hash":report.evidence_hash,"registry_hash":registry["registry_hash"],"disposition_counts":universe.disposition_counts()}
    return {"version":"1.0.0","vectors":payload,"vector_hash":canonical_sha256(payload)}

def verify_vectors(expected:dict[str,object])->bool:
    return generate_vectors()==expected
