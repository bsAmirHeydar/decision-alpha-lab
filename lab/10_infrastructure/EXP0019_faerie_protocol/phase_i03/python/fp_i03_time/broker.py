"""Explicit broker-time adapter; no automatic live offset inference is allowed in FP-I03."""
from .contracts import BrokerTimestamp, TimeKernelConfig
from .calendar import snapshot


def snapshot_from_broker(broker_epoch_ms: int, broker_utc_offset_minutes: int, config: TimeKernelConfig | None = None):
    stamp = BrokerTimestamp(broker_epoch_ms, broker_utc_offset_minutes)
    return snapshot(stamp.utc_epoch_ms, config)
