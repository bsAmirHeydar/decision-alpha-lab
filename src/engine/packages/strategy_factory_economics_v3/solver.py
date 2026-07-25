from __future__ import annotations
from decimal import Decimal
from strategy_factory_treatments_v3.enums import TradeSide
from .contracts import *
from .price_kernel import ExecutablePriceKernel
from .costs import CostEstimator
from .broker import BrokerConstraintSolver
from .errors import InsufficientRiskBudget,StaleEconomicInput
from .utils import dec,floor_step
class MaximumLossSolver:
    VERSION='3.0.0'
    def __init__(self): self.price=ExecutablePriceKernel(); self.costs=CostEstimator(); self.broker=BrokerConstraintSolver()
    def _conversion_rate(self,spec,account,conversion):
        if spec.profit_currency==account.currency: return Decimal('1')
        if conversion is None: raise StaleEconomicInput('missing_conversion','profit currency conversion required',{'from':spec.profit_currency,'to':account.currency})
        if conversion.from_currency!=spec.profit_currency or conversion.to_currency!=account.currency: raise StaleEconomicInput('wrong_conversion_pair','conversion quote does not match symbol/account')
        return conversion.bid
    def solve(self,geometry:RiskGeometry,quote:QuoteSnapshot,spec:SymbolEconomicsSpec,account:AccountEconomicSnapshot,cost_model:CostModelDescriptor,budget:CapitalBudget,conversion:CurrencyConversionQuote|None=None,minimum_reward_cost_ratio=Decimal('0')):
        if not budget.accepted or budget.approved_cash<=0: raise InsufficientRiskBudget('zero_budget','capital budget rejected')
        decision_time=max(account.known_time_ms,quote.known_time_ms,spec.known_time_ms)
        if quote.age_ms(decision_time)>cost_model.max_quote_age_ms: raise StaleEconomicInput('stale_quote','quote too old')
        if spec.age_ms(decision_time)>cost_model.max_spec_age_ms: raise StaleEconomicInput('stale_spec','spec too old')
        conv=self._conversion_rate(spec,account,conversion)
        slip=cost_model.slippage_rule
        entry_req=ExecutablePriceRequest(geometry.side,ExecutionRole.ENTRY,geometry.order_kind,decision_time,geometry.logical_entry_price,slip.points(geometry.side,True,geometry.volatility_points))
        stop_req=ExecutablePriceRequest(geometry.side,ExecutionRole.STOP_EXIT,OrderKind.CLOSE,decision_time,geometry.logical_stop_price,slip.points(geometry.side,False,geometry.volatility_points))
        target_req=None if geometry.logical_target_price is None else ExecutablePriceRequest(geometry.side,ExecutionRole.TARGET_EXIT,OrderKind.CLOSE,decision_time,geometry.logical_target_price,slip.points(geometry.side,False,geometry.volatility_points))
        entry=self.price.compute(entry_req,quote,spec,cost_model.max_quote_age_ms); stop=self.price.compute(stop_req,quote,spec,cost_model.max_quote_age_ms); target=None if target_req is None else self.price.compute(target_req,quote,spec,cost_model.max_quote_age_ms)
        price_loss_per_lot=abs(entry.executable_price-stop.executable_price)*spec.value_per_price_unit_per_lot(True)*conv
        unit_cost=self.costs.estimate(cost_model,spec,quote,geometry,Decimal('1'),entry.executable_price,stop.executable_price,None if target is None else target.executable_price,conv)
        per_lot=(price_loss_per_lot+unit_cost.total_cash)*cost_model.reserve_multiplier
        if per_lot<=0: raise InsufficientRiskBudget('non_positive_unit_risk','unit maximum loss is not positive')
        raw=budget.approved_cash/per_lot
        constrained=self.broker.solve(spec,quote,geometry,entry.executable_price,stop.executable_price,None if target is None else target.executable_price,raw,account.free_margin,conv,cost_model.max_spec_age_ms)
        if not constrained.accepted:
            empty=CostBreakdown(*([Decimal('0')]*8))
            return EconomicEnvelope(geometry.treatment_id,geometry.geometry_id,quote.quote_id,spec.definition_id,cost_model.definition_id,budget.budget_id,geometry.side,entry.executable_price,stop.executable_price,None if target is None else target.executable_price,Decimal('0'),raw,Decimal('0'),empty,Decimal('0'),Decimal('0'),Decimal('0'),constrained.margin_required,budget.approved_cash,Decimal('0'),False,constrained.reason_code,tuple(f.code for f in constrained.findings),decision_time,{})
        v=constrained.volume
        cb=self.costs.estimate(cost_model,spec,quote,geometry,v,constrained.entry_price,constrained.stop_price,constrained.target_price,conv)
        price_loss=abs(constrained.entry_price-constrained.stop_price)*spec.value_per_price_unit_per_lot(True)*v*conv
        max_loss=(price_loss+cb.total_cash)*cost_model.reserve_multiplier
        # Corrective floor loop for non-linear minimum commissions and tick/margin adjustments.
        while v>=spec.volume_min and max_loss>budget.approved_cash:
            v=floor_step(v-spec.volume_step,spec.volume_step)
            if v<spec.volume_min: break
            cb=self.costs.estimate(cost_model,spec,quote,geometry,v,constrained.entry_price,constrained.stop_price,constrained.target_price,conv)
            price_loss=abs(constrained.entry_price-constrained.stop_price)*spec.value_per_price_unit_per_lot(True)*v*conv
            max_loss=(price_loss+cb.total_cash)*cost_model.reserve_multiplier
        if v<spec.volume_min:
            empty=CostBreakdown(*([Decimal('0')]*8)); return EconomicEnvelope(geometry.treatment_id,geometry.geometry_id,quote.quote_id,spec.definition_id,cost_model.definition_id,budget.budget_id,geometry.side,constrained.entry_price,constrained.stop_price,constrained.target_price,Decimal('0'),raw,Decimal('0'),empty,Decimal('0'),Decimal('0'),Decimal('0'),Decimal('0'),budget.approved_cash,Decimal('0'),False,'risk_budget_below_minimum_volume',(),decision_time,{})
        target_gross=Decimal('0') if constrained.target_price is None else abs(constrained.target_price-constrained.entry_price)*spec.value_per_price_unit_per_lot(False)*v*conv
        target_net=target_gross-cb.total_cash
        ratio=Decimal('Infinity') if cb.total_cash<=0 else target_gross/cb.total_cash
        accepted=target_gross==0 or ratio>=dec(minimum_reward_cost_ratio)
        reason='ok' if accepted else 'reward_consumed_by_cost'
        margin=self.broker.margin(spec,v,constrained.entry_price,conv)
        return EconomicEnvelope(geometry.treatment_id,geometry.geometry_id,quote.quote_id,spec.definition_id,cost_model.definition_id,budget.budget_id,geometry.side,constrained.entry_price,constrained.stop_price,constrained.target_price,v,raw,price_loss,cb,max_loss,target_gross,target_net,margin,budget.approved_cash,max_loss/budget.approved_cash,accepted,reason,tuple(f.code for f in constrained.findings),decision_time,{'unit_max_loss_cash':per_lot,'conversion_rate':conv,'reward_cost_ratio':ratio})
