#property strict
#property version "1.000"
#include <AlphaLab/EXP0019/FaerieProtocol/I15/FP_I15_All.mqh>
int OnInit(){
 int failed=0; FP_I15_WinnerInput w;w.signal_id="SIG";w.signal_hash="HASH";w.protected_symbol="TEST";w.quota_key_id="Q";w.i09_reservation_id="R";w.direction=FP_I15_SELL;w.raw_structural_stop=101.0;w.confirmation_close=1;
 FP_I15_QuoteSnapshot q;q.quote_id="QUOTE";q.symbol="TEST";q.bid=100.0;q.ask=100.25;q.captured_at=2;q.source_revision_id="REV";
 FP_I15_SymbolSpec s;s.symbol="TEST";s.tick_size=.25;s.tick_value_loss=5;s.volume_min=.01;s.volume_max=100;s.volume_step=.01;s.stops_level_price=.25;s.freeze_level_price=0;
 FP_I15_RiskConfig r;r.fixed_risk_amount=100;r.target_r_multiple=2;r.max_slippage_price=.25;r.round_trip_cost_per_lot=0;
 FP_I15_Geometry g;if(!FP_I15_BuildGeometry(w,q,s,r,g))failed++; if(MathAbs(g.adjusted_stop-101.25)>1e-9)failed++;
 FP_I15_Sizing z;if(!FP_I15_SizeFixedRisk(g,s,r,z))failed++; if(z.max_loss>r.fixed_risk_amount+1e-8)failed++;
 FP_I15_Plan p;p.plan_id="PLAN";p.signal_id=w.signal_id;p.quota_key_id=w.quota_key_id;p.trade_symbol=w.protected_symbol;p.direction=w.direction;p.geometry=g;p.sizing=z;
 FP_I15_QuotaRecord qr;qr.state=FP_I15_QUOTA_AVAILABLE;qr.generation=0;FP_I15_PaperOrder o;if(!FP_I15_SimulateImmediateFill(p,FP_I15_POLICY_TWO_STAGE_FILLED,qr,o))failed++;if(qr.state!=FP_I15_QUOTA_CONSUMED)failed++;if(o.state!=FP_I15_ORDER_FILLED)failed++;
 Print("FP-I15 self-test failed=",failed," authority=",FP_I15_Authority()," live_ready=",FP_I15_LiveReady()); return failed==0?INIT_SUCCEEDED:INIT_FAILED;
}
void OnTick(){}
