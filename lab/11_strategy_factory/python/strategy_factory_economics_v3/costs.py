from __future__ import annotations
from decimal import Decimal
from strategy_factory_treatments_v3.enums import TradeSide
from .contracts import *
from .enums import *
from .utils import dec,stable_id
from .errors import EconomicsError,StaleEconomicInput
class CostModelRegistry:
    def __init__(self): self._models={}
    def register(self,model:CostModelDescriptor):
        if model.exact_key in self._models: raise EconomicsError('duplicate_cost_model','duplicate exact cost model',{'exact_key':model.exact_key})
        self._models[model.exact_key]=model; return model
    def resolve(self,exact_key):
        if exact_key not in self._models: raise EconomicsError('missing_cost_model','cost model not found',{'exact_key':exact_key})
        return self._models[exact_key]
    def snapshot(self): return tuple(self._models[k] for k in sorted(self._models))

def default_cost_registry():
    r=CostModelRegistry()
    r.register(CostModelDescriptor('cost.fx_standard','1.0.0',SpreadSource.MAX_OBSERVED_AND_FLOOR,Decimal('8'),Decimal('0'),
      (CommissionRule('commission.lot_side',CommissionBasis.PER_LOT_PER_SIDE,Decimal('3.5')),),
      SlippageRule('slippage.conservative',SlippageModelKind.ORDER_SIDE_POINTS,Decimal('2'),Decimal('2'),Decimal('3'),Decimal('3')),FinancingRule(),Decimal('0'),Decimal('0.5'),Decimal('1')))
    r.register(CostModelDescriptor('cost.index_cfd','1.0.0',SpreadSource.OBSERVED,Decimal('0'),Decimal('0'),
      (CommissionRule('commission.fixed_min',CommissionBasis.FIXED_PER_TRANSACTION,Decimal('0.25'),Decimal('0.25')),),
      SlippageRule('slippage.index',SlippageModelKind.VOLATILITY_SCALED,Decimal('1'),Decimal('1'),Decimal('2'),Decimal('2'),Decimal('0.05')),FinancingRule(FinancingBasis.NOTIONAL_ANNUAL_RATE,Decimal('0.08'),Decimal('0.08')),Decimal('0'),Decimal('1'),Decimal('1.05')))
    return r

class CostEstimator:
    def commission(self,model:CostModelDescriptor,volume,entry_price,exit_price,contract_size,entry_transactions=1,exit_transactions=1):
        volume,entry_price,exit_price,contract_size=map(dec,(volume,entry_price,exit_price,contract_size)); total=Decimal('0')
        notional=((entry_price+exit_price)/2)*contract_size*volume
        for rule in model.commission_rules:
            if rule.basis is CommissionBasis.PER_LOT_PER_SIDE:
                raw=rule.amount*volume*((entry_transactions if rule.applies_entry else 0)+(exit_transactions if rule.applies_exit else 0))
            elif rule.basis is CommissionBasis.PER_LOT_ROUND_TURN: raw=rule.amount*volume
            elif rule.basis is CommissionBasis.PER_NOTIONAL_BPS: raw=notional*rule.amount/Decimal('10000')
            elif rule.basis is CommissionBasis.FIXED_PER_TRANSACTION: raw=rule.amount*((entry_transactions if rule.applies_entry else 0)+(exit_transactions if rule.applies_exit else 0))
            else: raw=rule.amount*volume+notional*rule.amount/Decimal('10000')
            raw=max(raw,rule.minimum)
            if rule.maximum is not None: raw=min(raw,rule.maximum)
            total+=raw
        return total
    def estimate(self,model:CostModelDescriptor,spec:SymbolEconomicsSpec,quote:QuoteSnapshot,geometry:RiskGeometry,volume,entry_px,stop_px,target_px=None,conversion_rate=Decimal('1'),extra_gap_points=Decimal('0')):
        volume,entry_px,stop_px,conversion_rate=map(dec,(volume,entry_px,stop_px,conversion_rate)); vp=spec.value_per_price_unit_per_lot(True)*volume*conversion_rate
        spread_points=max(quote.spread/spec.point,model.spread_floor_points,model.spread_percentile_points if model.spread_source is SpreadSource.PERCENTILE_POINTS else Decimal('0'))
        spread_cash=spread_points*spec.point*vp
        slip=model.slippage_rule
        entry_slip=slip.points(geometry.side,True,geometry.volatility_points)*spec.point*vp
        exit_slip=slip.points(geometry.side,False,geometry.volatility_points)*spec.point*vp
        commission=self.commission(model,volume,entry_px,stop_px,spec.contract_size,geometry.entry_transactions,geometry.exit_transactions)*conversion_rate
        notional=entry_px*spec.contract_size*volume*conversion_rate
        if model.financing_rule.basis is FinancingBasis.PER_LOT_PER_DAY:
            rate=model.financing_rule.long_amount if geometry.side is TradeSide.LONG else model.financing_rule.short_amount; financing=abs(rate)*volume*geometry.expected_holding_days*conversion_rate
        elif model.financing_rule.basis is FinancingBasis.NOTIONAL_ANNUAL_RATE:
            rate=model.financing_rule.long_amount if geometry.side is TradeSide.LONG else model.financing_rule.short_amount; financing=abs(notional*rate*geometry.expected_holding_days/Decimal('365'))
        else: financing=Decimal('0')
        tax=abs(notional)*model.tax_bps/Decimal('10000')
        conversion=abs(notional)*model.conversion_cost_bps/Decimal('10000')
        gap=(geometry.gap_reserve_points+dec(extra_gap_points))*spec.point*vp
        return CostBreakdown(spread_cash,entry_slip,exit_slip,commission,financing,tax,conversion,gap)
