from datetime import datetime,timezone
from strategy_factory_rthp_mt5_activation_v1.acquire import _latest_closed,acquire_symbol,resolve_range
from strategy_factory_rthp_mt5_activation_v1.config import load_mt5_activation_config
from strategy_factory_rthp_mt5_activation_v1.symbols import resolve_symbol
from strategy_factory_rthp_mt5_activation_v1.terminal import TerminalSession

def test_fake_provider_resolves_and_acquires_m1(config_path,fake_provider):
    c=load_mt5_activation_config(config_path)
    with TerminalSession(fake_provider,None,1000,False,True) as session:
        p=resolve_symbol(fake_provider,c.primary_symbol,c.canonical_primary_id); s=resolve_symbol(fake_provider,c.secondary_symbol,c.canonical_secondary_id)
        start,end=resolve_range(fake_provider,p,s,c.history,datetime.now(timezone.utc)); result=acquire_symbol(fake_provider,p,start,end,c.history,session.receipt.terminal_id,c.source_revision)
    assert len(result.bars)>1000; assert all(x.timeframe_seconds==60 for x in result.bars); assert all(x.known_time_utc_ms==x.bar_close_time_utc_ms for x in result.bars)


class _WarmupProvider:
    package_version = "5.0.fake"

    def __init__(self, rows):
        self.rows = rows
        self.calls = []
        self._attempt = 0

    def copy_rates_from_pos(self, symbol, start_pos, count):
        self.calls.append((symbol, start_pos, count))
        self._attempt += 1
        if self._attempt == 1:
            return []
        return self.rows[-count:]

    def last_error(self):
        return (1, "Success")


def test_latest_closed_uses_closed_position_and_retries(fake_provider):
    provider = _WarmupProvider(fake_provider.data["FAKE_A"])
    now = datetime(2026, 1, 7, 0, 0, tzinfo=timezone.utc)

    latest = _latest_closed(
        provider,
        "FAKE_A",
        now,
        retry_count=2,
        retry_delay_seconds=0.0,
    )

    assert latest.tzinfo is timezone.utc
    assert provider.calls == [
        ("FAKE_A", 1, 10),
        ("FAKE_A", 1, 10),
    ]
