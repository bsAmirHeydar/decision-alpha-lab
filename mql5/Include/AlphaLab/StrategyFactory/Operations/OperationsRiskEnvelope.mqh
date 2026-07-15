#ifndef ALPHALAB_OPERATIONS_RISK_ENVELOPE_MQH
#define ALPHALAB_OPERATIONS_RISK_ENVELOPE_MQH
struct ALOperationsRiskEnvelope { double max_total_risk; double max_open_risk; double max_order_risk; double max_daily_loss; double max_weekly_loss; int max_positions; int max_orders_per_minute; };
bool ALOpsRiskEnvelopeValid(const ALOperationsRiskEnvelope &value){ if(value.max_total_risk<0.0||value.max_open_risk<0.0||value.max_order_risk<0.0||value.max_daily_loss<0.0||value.max_weekly_loss<0.0) return false; if(value.max_open_risk>value.max_total_risk||value.max_order_risk>value.max_open_risk) return false; return value.max_positions>=0 && value.max_orders_per_minute>=0; }
double ALOpsRiskHeadroom(const ALOperationsRiskEnvelope &value,const double open_risk,const double reserved_risk){ if(!ALOpsRiskEnvelopeValid(value)||open_risk<0.0||reserved_risk<0.0) return 0.0; double a=value.max_open_risk-open_risk; double b=value.max_total_risk-reserved_risk; double result=MathMin(value.max_order_risk,MathMin(a,b)); return result>0.0?result:0.0; }
#endif
