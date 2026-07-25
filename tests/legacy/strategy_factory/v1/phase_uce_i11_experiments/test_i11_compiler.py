from dataclasses import replace

from strategy_factory_experiments_v3.compiler import ExperimentDagCompiler, manifest_semantic_snapshot
from strategy_factory_experiments_v3.enums import NodeKind
from strategy_factory_experiments_v3.golden import golden_declaration


def test_same_declaration_emits_identical_manifest_and_trials():
    declaration = golden_declaration()
    first = ExperimentDagCompiler().compile(declaration)
    second = ExperimentDagCompiler().compile(declaration)
    assert first.manifest_hash == second.manifest_hash
    assert [trial.trial_id for trial in first.trials] == [trial.trial_id for trial in second.trials]
    assert manifest_semantic_snapshot(first) == manifest_semantic_snapshot(second)


def test_rejected_uce_i10_candidate_never_enters_dag():
    manifest = ExperimentDagCompiler().compile(golden_declaration())
    assert "uce.deep.rejected_graph@1.0.0" in manifest.rejected_candidate_keys
    assert all("rejected_graph" not in trial.candidate_key for trial in manifest.trials)
    assert all("rejected_graph" not in node.semantic_key for node in manifest.nodes)


def test_declared_trial_count_reconciles_and_budget_caps_cross_product():
    manifest = ExperimentDagCompiler().compile(golden_declaration(max_trials=7))
    assert manifest.declared_trial_count == 7 == len(manifest.trials)
    assert len({trial.trial_id for trial in manifest.trials}) == 7


def test_baseline_trials_are_compiled_before_challengers():
    manifest = ExperimentDagCompiler().compile(golden_declaration())
    keys = [trial.candidate_key for trial in manifest.trials]
    baseline_end = max(index for index, key in enumerate(keys) if "classical.logistic" in key)
    challenger_start = min(index for index, key in enumerate(keys) if "deep.temporal_conv" in key)
    assert baseline_end < challenger_start
    trial_nodes = [node for node in manifest.nodes if node.kind is NodeKind.TRIAL]
    baseline_priorities = [node.priority for node in trial_nodes if "classical.logistic" in next(t.candidate_key for t in manifest.trials if t.trial_id == node.trial_id)]
    challenger_priorities = [node.priority for node in trial_nodes if "deep.temporal_conv" in next(t.candidate_key for t in manifest.trials if t.trial_id == node.trial_id)]
    assert max(baseline_priorities) < min(challenger_priorities)


def test_all_edges_reference_known_nodes_and_graph_is_acyclic():
    manifest = ExperimentDagCompiler().compile(golden_declaration())
    node_ids = {node.node_id for node in manifest.nodes}
    assert all(edge.parent_id in node_ids and edge.child_id in node_ids for edge in manifest.edges)
    # Every dependency is mirrored by an edge.
    edge_pairs = {(edge.parent_id, edge.child_id) for edge in manifest.edges}
    assert all((parent, node.node_id) in edge_pairs for node in manifest.nodes for parent in node.dependencies)


def test_scheduler_version_changes_trial_identity_and_manifest():
    original = golden_declaration()
    changed = replace(original, scheduler_version="1.0.1")
    first = ExperimentDagCompiler().compile(original)
    second = ExperimentDagCompiler().compile(changed)
    assert first.manifest_hash != second.manifest_hash
    assert [trial.trial_id for trial in first.trials] != [trial.trial_id for trial in second.trials]


def test_known_time_policy_is_identity_bearing():
    original = golden_declaration()
    changed = replace(original, known_time_policy_hash="f" * 64)
    first = ExperimentDagCompiler().compile(original)
    second = ExperimentDagCompiler().compile(changed)
    assert first.trials[0].trial_id != second.trials[0].trial_id


def test_manifest_contains_exact_resource_claim_for_every_trial():
    manifest = ExperimentDagCompiler().compile(golden_declaration())
    assert len(manifest.resource_claims) == len(manifest.trials)
    assert {claim.trial_id for claim in manifest.resource_claims} == {trial.trial_id for trial in manifest.trials}
