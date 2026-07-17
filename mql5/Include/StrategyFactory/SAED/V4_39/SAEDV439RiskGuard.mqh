#ifndef SAED_V4_39_RISK_GUARD_MQH
#define SAED_V4_39_RISK_GUARD_MQH
#include "SAEDV439Types.mqh"
bool SAEDV439RiskPass(const SAEDV439Intent &i,const SAEDV439RiskState &s,const double max_trade,const double max_size,const double max_daily,const double max_dd){if(!s.kill_switch_armed)return false;if(i.risk_fraction>max_trade||i.size_fraction>max_size)return false;if(s.daily_loss_fraction>=max_daily||s.drawdown_fraction>=max_dd)return false;return true;}
#endif
