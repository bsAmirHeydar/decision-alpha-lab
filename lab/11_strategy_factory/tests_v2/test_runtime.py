import time
from strategy_factory.runtime import AtomicGeneration, Generation, IdempotencyGuard, LatencyBudget, LatencyTracker, TelemetryBuffer


def test_atomic_generation_swap():
    holder = AtomicGeneration(Generation(1, "a", "ha"))
    next_gen = holder.swap("b", "hb")
    assert next_gen.generation_id == 2
    assert holder.get().artifact == "b"


def test_idempotency_guard():
    guard = IdempotencyGuard(2)
    assert guard.claim("a")
    assert not guard.claim("a")


def test_latency_tracker_reports_breach():
    tracker = LatencyTracker(); tracker.start("x"); time.sleep(.001); tracker.stop("x")
    report = tracker.report(LatencyBudget({"x":1}, total_limit_ns=1))
    assert "x" in report.breaches and "total" in report.breaches
