from src.engine.tooling.strategy_factory.contexts.rthp.detector import evaluate_divergence
def base():
 return {"context_id":"CTX_RTHP_CROSS_SYMBOL_CYCLE_DIVERGENCE_V1","family":"NN","pair_id":"P","cycle_definition_version":"1.0.0","active_cycle_id":"A","reference_cycle_id":"R","level_side":"HIGH","confirmation_close_time":"2026-01-01T10:15:00-05:00","price_basis_primary":"BID","price_basis_secondary":"BID","primary":{"symbol":"A","touched":True,"first_touch_time":"2026-01-01T10:05:00-05:00","data_status":"VALID"},"secondary":{"symbol":"B","touched":False,"first_touch_time":None,"data_status":"VALID"},"available_reference_count":12,"required_reference_count":12}
def test_high_bearish():
 r=evaluate_divergence(base());assert r["event_created"] and r["polarity"]=="BEARISH_DIVERGENCE"
def test_low_bullish():
 x=base();x["level_side"]="LOW";assert evaluate_divergence(x)["polarity"]=="BULLISH_DIVERGENCE"
def test_both_no_event():
 x=base();x["secondary"]["touched"]=True;assert evaluate_divergence(x)["evaluation_status"]=="NO_EVENT"
def test_stale_unconfirmed():
 x=base();x["secondary"]["data_status"]="STALE_OR_IMPUTED";r=evaluate_divergence(x);assert r["evaluation_status"]=="UNCONFIRMED" and not r["event_created"]
