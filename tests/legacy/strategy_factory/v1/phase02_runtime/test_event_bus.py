from strategy_factory_runtime import EventEnvelope, EventType, BoundedEventBus, BusOverflowPolicy

def event(i=0):
    return EventEnvelope(i, EventType.HEARTBEAT, "runtime", "test", 1000, 1000, "sha256_x", 10)

def test_sequence_and_fifo():
    bus = BoundedEventBus(8, BusOverflowPolicy.REJECT_NEW)
    assert bus.publish(event())
    assert bus.publish(event())
    assert bus.poll().sequence == 1
    assert bus.poll().sequence == 2

def test_reject_new_overflow():
    bus = BoundedEventBus(8, BusOverflowPolicy.REJECT_NEW)
    for _ in range(8): assert bus.publish(event())
    assert not bus.publish(event())
    assert bus.dropped == 1

def test_drop_oldest_overflow():
    bus = BoundedEventBus(8, BusOverflowPolicy.DROP_OLDEST)
    for _ in range(9): assert bus.publish(event())
    assert len(bus) == 8 and bus.dropped == 1
