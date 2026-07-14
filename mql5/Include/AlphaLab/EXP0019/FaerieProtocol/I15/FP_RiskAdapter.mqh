#ifndef FP_RISK_ADAPTER_MQH
#define FP_RISK_ADAPTER_MQH
#include "FP_I15_Contracts.mqh"
double FP_I15_FloorStep(const double value,const double step){ return MathFloor((value+1e-12)/step)*step; }
double FP_I15_CeilStep(const double value,const double step){ return MathCeil((value-1e-12)/step)*step; }
bool FP_I15_BuildGeometry(const FP_I15_WinnerInput &winner,const FP_I15_QuoteSnapshot &quote,const FP_I15_SymbolSpec &spec,const FP_I15_RiskConfig &risk,FP_I15_Geometry &out){
 out.status=FP_I15_GEOMETRY_BLOCKED; out.entry=(winner.direction==FP_I15_BUY?quote.ask:quote.bid); out.worst_entry=out.entry+(winner.direction==FP_I15_BUY?risk.max_slippage_price:-risk.max_slippage_price); out.raw_stop=winner.raw_structural_stop; out.spread=quote.ask-quote.bid;
 if(winner.direction==FP_I15_SELL && out.spread<=0){out.reason_code="FP_PAPER_SPREAD_SNAPSHOT_UNAVAILABLE";return false;}
 out.adjusted_stop=(winner.direction==FP_I15_BUY?out.raw_stop:out.raw_stop+out.spread);
 out.adjusted_stop=(winner.direction==FP_I15_BUY?FP_I15_FloorStep(out.adjusted_stop,spec.tick_size):FP_I15_CeilStep(out.adjusted_stop,spec.tick_size));
 if(winner.direction==FP_I15_BUY && out.adjusted_stop>=out.entry){out.reason_code="FP_PAPER_BUY_STOP_NOT_BELOW_ENTRY";return false;}
 if(winner.direction==FP_I15_SELL && out.adjusted_stop<=out.entry){out.reason_code="FP_PAPER_SELL_STOP_NOT_ABOVE_ENTRY";return false;}
 out.stop_distance=MathAbs(out.worst_entry-out.adjusted_stop); double minimum=MathMax(spec.tick_size,MathMax(spec.stops_level_price,spec.freeze_level_price));
 if(out.stop_distance<minimum){out.reason_code="FP_PAPER_MINIMUM_STOP_DISTANCE_VIOLATED";return false;}
 double base=MathAbs(out.entry-out.adjusted_stop); out.target=out.entry+(winner.direction==FP_I15_BUY?base*risk.target_r_multiple:-base*risk.target_r_multiple); out.target=(winner.direction==FP_I15_BUY?FP_I15_FloorStep(out.target,spec.tick_size):FP_I15_CeilStep(out.target,spec.tick_size));
 out.status=FP_I15_GEOMETRY_READY;out.reason_code="FP_PAPER_READY";return true;
}
bool FP_I15_SizeFixedRisk(const FP_I15_Geometry &g,const FP_I15_SymbolSpec &spec,const FP_I15_RiskConfig &risk,FP_I15_Sizing &out){
 out.status=FP_I15_GEOMETRY_BLOCKED; out.loss_per_lot=(g.stop_distance/spec.tick_size)*spec.tick_value_loss+risk.round_trip_cost_per_lot; if(out.loss_per_lot<=0){out.reason_code="FP_PAPER_LOSS_PER_LOT_NONPOSITIVE";return false;}
 out.raw_volume=risk.fixed_risk_amount/out.loss_per_lot; out.volume=FP_I15_FloorStep(MathMin(out.raw_volume,spec.volume_max),spec.volume_step); out.max_loss=out.volume*out.loss_per_lot;
 if(out.volume<spec.volume_min){out.reason_code="FP_PAPER_MIN_VOLUME_EXCEEDS_RISK_CAP";return false;} if(out.max_loss>risk.fixed_risk_amount+1e-8){out.reason_code="FP_PAPER_RISK_CAP_EXCEEDED";return false;}
 out.status=FP_I15_GEOMETRY_READY;out.reason_code="FP_PAPER_READY";return true;
}
#endif
