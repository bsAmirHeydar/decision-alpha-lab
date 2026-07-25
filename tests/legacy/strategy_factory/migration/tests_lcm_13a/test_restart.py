def test_restart_generation_is_explicit(scenarios):
    restart = [row for row in scenarios if row["scenario_kind"] == "RESTART_REPLAY"]
    other = [row for row in scenarios if row["scenario_kind"] != "RESTART_REPLAY"]
    assert restart and all(row["causal_input"]["restart_generation"] == 1 for row in restart)
    assert all(row["causal_input"]["restart_generation"] == 0 for row in other)
