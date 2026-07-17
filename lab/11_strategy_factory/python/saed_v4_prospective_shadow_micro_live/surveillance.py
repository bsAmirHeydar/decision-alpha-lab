from __future__ import annotations
from statistics import mean
from .canonical import q,seal

def _p95(xs:list[float])->float:
 if not xs:return 0.0
 ys=sorted(xs);return float(ys[min(len(ys)-1,max(0,int(.95*len(ys))-1))])
def monitor(observations:list[dict],paper:dict,shadow:dict,risk_envelope:dict)->dict:
 lat=[float(x["latency_ms"]) for x in observations];slip=[float(x["slippage_bps"]) for x in paper["events"] if x["status"]=="PAPER_FILLED"]
 reject=paper["metrics"]["rejected_count"]/max(1,paper["metrics"]["selected_count"])
 alerts=[]
 if _p95(lat)>risk_envelope["max_latency_ms"]:alerts.append("LATENCY_BREACH")
 if (mean(slip) if slip else 0)>risk_envelope["max_slippage_bps"]:alerts.append("SLIPPAGE_BREACH")
 if reject>risk_envelope["max_reject_rate"]:alerts.append("REJECT_RATE_BREACH")
 if paper["metrics"]["order_submission_count"]!=0 or shadow["metrics"]["order_submission_count"]!=0:alerts.append("UNAUTHORIZED_ORDER_SIDE_EFFECT")
 metrics={"latency_p95_ms":q(_p95(lat)),"mean_slippage_bps":q(mean(slip) if slip else 0),"reject_rate":q(reject),"shadow_disagreement_rate":shadow["metrics"]["disagreement_rate"],"paper_cumulative_net_pnl_bps":paper["metrics"]["cumulative_net_pnl_bps"],"unauthorized_order_count":paper["metrics"]["order_submission_count"]+shadow["metrics"]["order_submission_count"]}
 return seal({"phase":"SAED_V4_39","metrics":metrics,"alerts":sorted(alerts),"hard_breach":bool(alerts),"recommended_action":"KILL_AND_ESCALATE" if alerts else "CONTINUE_REFERENCE_QUALIFICATION","research_only":True},"v439_surveillance","report_id","report_hash")
