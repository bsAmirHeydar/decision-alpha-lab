"""Cross-language conformance vector generation and verification."""

from __future__ import annotations

from typing import Any, Mapping

from .canonical import canonical_sha256
from .compiler import ExperimentDagCompiler
from .golden import golden_declaration
from .search import propose


def generate_vectors() -> dict[str, Any]:
    declaration = golden_declaration()
    manifest = ExperimentDagCompiler(declaration.compiler_version).compile(declaration)
    proposals = propose(declaration.search_plan)
    return {
        "version": "1.0.0",
        "declaration_hash": declaration.declaration_hash,
        "search_plan_hash": declaration.search_plan.plan_hash,
        "proposal_hashes": [proposal.candidate_hash for proposal in proposals],
        "trial_ids": [trial.trial_id for trial in manifest.trials],
        "manifest_hash": manifest.manifest_hash,
        "node_count": len(manifest.nodes),
        "edge_count": len(manifest.edges),
        "vector_hash": canonical_sha256(
            {
                "declaration_hash": declaration.declaration_hash,
                "proposal_hashes": [proposal.candidate_hash for proposal in proposals],
                "trial_ids": [trial.trial_id for trial in manifest.trials],
                "manifest_hash": manifest.manifest_hash,
                "node_count": len(manifest.nodes),
                "edge_count": len(manifest.edges),
            }
        ),
    }


def verify_vectors(vectors: Mapping[str, Any]) -> bool:
    expected = generate_vectors()
    return dict(vectors) == expected
