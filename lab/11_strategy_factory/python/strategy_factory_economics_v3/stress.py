from dataclasses import replace
from decimal import Decimal
from .contracts import *
from .enums import StressKind,SpreadSource,TradeStatus
from .solver import MaximumLossSolver
class EconomicStressSuite:
    def __init__(self,solver=None): self.solver=solver or MaximumLossSolver()
    def apply(self,scenario,quote,spec,model,geometry,conversion):
        m=scenario.magnitude
        if scenario.kind is StressKind.SPREAD_MULTIPLIER:
            mid=(quote.bid+quote.ask)/2; half=(quote.ask-quote.bid)*m/2; quote=replace(quote,bid=mid-half,ask=mid+half,sequence=quote.sequence+1)
        elif scenario.kind is StressKind.COMMISSION_MULTIPLIER:
            rules=tuple(replace(r,amount=r.amount*m,minimum=r.minimum*m,maximum=None if r.maximum is None else r.maximum*m) for r in model.commission_rules); model=replace(model,commission_rules=rules,version=model.version+'.stress')
        elif scenario.kind is StressKind.SLIPPAGE_POINTS:
            s=model.slippage_rule; model=replace(model,slippage_rule=replace(s,entry_long_points=s.entry_long_points+m,entry_short_points=s.entry_short_points+m,exit_long_points=s.exit_long_points+m,exit_short_points=s.exit_short_points+m),version=model.version+'.stress')
        elif scenario.kind is StressKind.GAP_POINTS: geometry=replace(geometry,gap_reserve_points=geometry.gap_reserve_points+m)
        elif scenario.kind is StressKind.CONVERSION_SHOCK and conversion is not None: conversion=replace(conversion,bid=conversion.bid*(Decimal('1')-m),ask=conversion.ask*(Decimal('1')+m))
        elif scenario.kind is StressKind.TICK_VALUE_SHOCK: spec=replace(spec,tick_value_loss=spec.tick_value_loss*m,tick_value_profit=spec.tick_value_profit*m,version=spec.version+'.stress')
        elif scenario.kind is StressKind.MARGIN_SHOCK:
            spec=replace(spec,margin_per_lot=spec.margin_per_lot*m,margin_rate=spec.margin_rate*m,leverage=spec.leverage/max(m,Decimal('0.0001')),version=spec.version+'.stress')
        elif scenario.kind is StressKind.VOLUME_REJECT: spec=replace(spec,volume_min=max(spec.volume_min,m),version=spec.version+'.stress')
        elif scenario.kind is StressKind.STALE_QUOTE: quote=replace(quote,known_time_ms=max(0,quote.known_time_ms-int(m)))
        elif scenario.kind is StressKind.STALE_SPEC: spec=replace(spec,known_time_ms=max(0,spec.known_time_ms-int(m)))
        return quote,spec,model,geometry,conversion
    def run_one(self,scenario,baseline,quote,spec,model,geometry,account,budget,conversion=None):
        q,s,m,g,c=self.apply(scenario,quote,spec,model,geometry,conversion)
        try: stressed=self.solver.solve(g,q,s,account,m,budget,c)
        except Exception:
            return StressResult(scenario.definition_id,baseline.envelope_id,'',baseline.maximum_loss_cash,Decimal('0'),baseline.normalized_volume,Decimal('0'),True,False,'stress_rejected')
        # Under the same cash budget, harsher economics must not increase approved volume.
        mono=stressed.normalized_volume<=baseline.normalized_volume
        return StressResult(scenario.definition_id,baseline.envelope_id,stressed.envelope_id,baseline.maximum_loss_cash,stressed.maximum_loss_cash,baseline.normalized_volume,stressed.normalized_volume,mono,stressed.accepted,stressed.reason_code)
