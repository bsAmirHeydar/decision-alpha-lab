#ifndef FP_I07_SIGNAL_IDENTITY_MQH
#define FP_I07_SIGNAL_IDENTITY_MQH
string FP_I07_SignalMaterial(const string candidate_id,const string relation,const string direction,const string hunter,const string protected,const datetime hunt_time,const string bar_id,const datetime close_time,const ENUM_TIMEFRAMES timeframe,const string config_hash)
{ return candidate_id+"|"+relation+"|"+direction+"|"+hunter+"|"+protected+"|"+IntegerToString((int)hunt_time)+"|"+bar_id+"|"+IntegerToString((int)close_time)+"|"+EnumToString(timeframe)+"|"+config_hash; }
#endif
