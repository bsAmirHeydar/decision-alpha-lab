from strategy_factory_experiments_v3.isolation import capture_environment, run_callable_in_spawn


def test_environment_capture_is_deterministic_for_same_allowlist():
    first = capture_environment(("pytest", "definitely_missing_package"))
    second = capture_environment(("definitely_missing_package", "pytest"))
    assert first.capture_hash == second.capture_hash
    assert first.package_versions["definitely_missing_package"] == "missing"


def test_spawned_process_returns_value_without_inheriting_parent_callable_state():
    result = run_callable_in_spawn(
        "strategy_factory_experiments_v3.isolation:echo_value",
        args=({"x": [1, 2, 3]},),
        timeout_seconds=5.0,
    )
    assert result.status == "succeeded"
    assert result.value == {"x": [1, 2, 3]}
    assert result.exit_code == 0


def test_spawned_process_timeout_is_enforced_by_parent():
    result = run_callable_in_spawn(
        "strategy_factory_experiments_v3.isolation:sleep_seconds",
        args=(1.0,),
        timeout_seconds=0.05,
    )
    assert result.status == "timed_out"
    assert result.error_type == "TimeoutError"
