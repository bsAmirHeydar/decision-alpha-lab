from dataclasses import replace
from strategy_factory_live import *
from strategy_factory_live.examples import reference_bundle

def reason(**changes):
    release,auth,policy,intent,account,quote=reference_bundle()
    values=dict(mode=LiveMode.DRY_RUN,intent=intent,release=release,authorization=auth,policy=policy,
      account=account,quote=quote,now_utc_msc=quote.time_utc_msc,session_orders=0,kill_switch=KillSwitch(),
      circuit=CircuitBreaker(2,1000))
    values["kill_switch"].state=KillSwitchState.DISARMED
    values.update(changes); return preflight_reason(**values)

def test_reference_preflight_passes(): assert reason()==LiveRejectReason.NONE

def test_default_micro_live_kill_switch_blocks():
    release,auth,policy,intent,account,quote=reference_bundle()
    auth=replace(auth,mode=LiveMode.MICRO_LIVE,authorization_hash="")
    auth=replace(auth,authorization_hash=auth.derived_hash())
    assert preflight_reason(mode=LiveMode.MICRO_LIVE,intent=intent,release=release,authorization=auth,policy=policy,
      account=account,quote=quote,now_utc_msc=quote.time_utc_msc,session_orders=0,kill_switch=KillSwitch(),
      circuit=CircuitBreaker(2,1000))==LiveRejectReason.KILL_SWITCH_ENGAGED

def test_spread_and_loss_limits():
    release,auth,policy,intent,account,quote=reference_bundle()
    ks=KillSwitch(KillSwitchState.DISARMED)
    wide=replace(quote,ask=quote.bid+1)
    assert preflight_reason(mode=LiveMode.DRY_RUN,intent=intent,release=release,authorization=auth,policy=policy,
      account=account,quote=wide,now_utc_msc=quote.time_utc_msc,session_orders=0,kill_switch=ks,
      circuit=CircuitBreaker(2,1000))==LiveRejectReason.SPREAD_LIMIT
    losing=replace(account,daily_realized_pnl_cash=-250,snapshot_hash="")
    losing=replace(losing,snapshot_hash=losing.derived_hash())
    assert preflight_reason(mode=LiveMode.DRY_RUN,intent=intent,release=release,authorization=auth,policy=policy,
      account=losing,quote=quote,now_utc_msc=quote.time_utc_msc,session_orders=0,kill_switch=ks,
      circuit=CircuitBreaker(2,1000))==LiveRejectReason.DAILY_LOSS_LIMIT
