from dataclasses import replace

from strategy_factory_experiments_v3.compiler import ExperimentDagCompiler
from strategy_factory_experiments_v3.golden import golden_declaration
from strategy_factory_experiments_v3.reproducibility import audit_reproducibility, compare_numeric_artifact


def compiled():
    declaration = golden_declaration(max_trials=4)
    return declaration, ExperimentDagCompiler().compile(declaration)


def test_reproducibility_passes_for_identical_manifest_counts_selection_and_artifacts():
    declaration, manifest = compiled()
    comparison = compare_numeric_artifact("predictions", (0.1, 0.2), (0.1, 0.2), 0.0)
    selected = (manifest.trials[0].trial_id,)
    report = audit_reproducibility(
        manifest=manifest,
        rerun_manifest=ExperimentDagCompiler().compile(declaration),
        executed_trial_ids=[trial.trial_id for trial in manifest.trials],
        selected_trial_ids_expected=selected,
        selected_trial_ids_actual=selected,
        artifact_comparisons=(comparison,),
        event_stream_hash_expected="a" * 64,
        event_stream_hash_actual="a" * 64,
    )
    assert report.passed
    assert not report.blockers


def test_reproducibility_fails_when_manifest_semantics_change():
    declaration, manifest = compiled()
    changed = replace(declaration, scheduler_version="1.0.1")
    rerun = ExperimentDagCompiler().compile(changed)
    report = audit_reproducibility(
        manifest=manifest,
        rerun_manifest=rerun,
        executed_trial_ids=[trial.trial_id for trial in manifest.trials],
        selected_trial_ids_expected=(),
        selected_trial_ids_actual=(),
        artifact_comparisons=(),
        event_stream_hash_expected="a" * 64,
        event_stream_hash_actual="a" * 64,
    )
    assert not report.passed
    assert "manifest_semantics_changed" in report.blockers


def test_reproducibility_reconciles_declared_and_executed_counts():
    _, manifest = compiled()
    report = audit_reproducibility(
        manifest=manifest,
        rerun_manifest=manifest,
        executed_trial_ids=[manifest.trials[0].trial_id],
        selected_trial_ids_expected=(),
        selected_trial_ids_actual=(),
        artifact_comparisons=(),
        event_stream_hash_expected="a" * 64,
        event_stream_hash_actual="a" * 64,
    )
    assert "declared_executed_trial_count_mismatch" in report.blockers


def test_numeric_tolerance_is_reported_as_warning_not_silent_hash_parity():
    _, manifest = compiled()
    comparison = compare_numeric_artifact("predictions", (0.1, 0.2), (0.10001, 0.19999), 0.001)
    report = audit_reproducibility(
        manifest=manifest,
        rerun_manifest=manifest,
        executed_trial_ids=[trial.trial_id for trial in manifest.trials],
        selected_trial_ids_expected=(),
        selected_trial_ids_actual=(),
        artifact_comparisons=(comparison,),
        event_stream_hash_expected="a" * 64,
        event_stream_hash_actual="a" * 64,
    )
    assert report.passed
    assert report.warnings == ("artifact_numeric_tolerance_used:predictions",)


def test_selected_trial_change_and_event_stream_change_are_blockers():
    _, manifest = compiled()
    report = audit_reproducibility(
        manifest=manifest,
        rerun_manifest=manifest,
        executed_trial_ids=[trial.trial_id for trial in manifest.trials],
        selected_trial_ids_expected=(manifest.trials[0].trial_id,),
        selected_trial_ids_actual=(manifest.trials[1].trial_id,),
        artifact_comparisons=(),
        event_stream_hash_expected="a" * 64,
        event_stream_hash_actual="b" * 64,
    )
    assert "selected_trial_set_changed" in report.blockers
    assert "event_stream_changed" in report.blockers
