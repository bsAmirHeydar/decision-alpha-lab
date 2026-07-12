#ifndef __UCEI03_CATALOG_MQH__
#define __UCEI03_CATALOG_MQH__
#include "UCEI03_Registry.mqh"
void UCEI03_InitDescriptor(UCEI03_AtomDescriptor &d,const string id,const ENUM_UCEI03_ATOM_KIND kind,const string family,const string description){d.atom_id=id;d.version="1.0.0";d.kind=kind;d.family=family;d.owner_id="alpha_lab";d.implementation_id="mql5:"+id+":1.0.0";d.compatibility.side_mask=3;d.compatibility.runtime_mode_mask=31;d.compatibility.required_context_fields_csv="";d.compatibility.incompatible_atom_ids_csv="";d.compatibility.tags_csv="manual,ai_search,research,runtime";ArrayResize(d.parameters,0);d.description=description;d.definition_id="";d.evidence_hash="";}
void UCEI03_AddParameter(UCEI03_AtomDescriptor &d,const string name,const ENUM_UCEI03_PARAM_TYPE type,const string def,const string minv,const string maxv,const string units,const string monotonic="none",const string allowed_values_csv="",const string description=""){int n=ArraySize(d.parameters);ArrayResize(d.parameters,n+1);d.parameters[n].name=name;d.parameters[n].type=type;d.parameters[n].default_value=def;d.parameters[n].minimum_value=minv;d.parameters[n].maximum_value=maxv;d.parameters[n].allowed_values_csv=allowed_values_csv;d.parameters[n].units=units;d.parameters[n].identity_affecting=true;d.parameters[n].monotonic_direction=monotonic;d.parameters[n].description=description;}
void UCEI03_ApplyParameterSchema(UCEI03_AtomDescriptor &d){
   if(d.atom_id=="entry.breakout_stop"){
      d.compatibility.required_context_fields_csv="reference_price";
      UCEI03_AddParameter(d,"buffer_points",UCEI03_PARAM_DECIMAL,"2","0","10000","points","none","","");
      UCEI03_AddParameter(d,"ttl_ms",UCEI03_PARAM_INTEGER,"300000","1","86400000","milliseconds","none","","");
   }
   else if(d.atom_id=="entry.confirmation_market"){
      d.compatibility.required_context_fields_csv="confirmation_price";
      UCEI03_AddParameter(d,"max_deviation_points",UCEI03_PARAM_DECIMAL,"20","0","100000","points","none","","");
   }
   else if(d.atom_id=="entry.immediate_market"){
      UCEI03_AddParameter(d,"max_age_ms",UCEI03_PARAM_INTEGER,"1000","0","60000","milliseconds","none","","");
   }
   else if(d.atom_id=="entry.ladder"){
      UCEI03_AddParameter(d,"leg_count",UCEI03_PARAM_INTEGER,"3","2","8","count","none","","");
      UCEI03_AddParameter(d,"spacing_points",UCEI03_PARAM_DECIMAL,"10","0.1","100000","points","none","","");
      UCEI03_AddParameter(d,"ttl_ms",UCEI03_PARAM_INTEGER,"900000","1","86400000","milliseconds","none","","");
   }
   else if(d.atom_id=="entry.passive_limit"){
      UCEI03_AddParameter(d,"offset_points",UCEI03_PARAM_DECIMAL,"10","0","100000","points","increasing","","");
      UCEI03_AddParameter(d,"ttl_ms",UCEI03_PARAM_INTEGER,"300000","1","86400000","milliseconds","none","","");
   }
   else if(d.atom_id=="entry.retest_limit"){
      d.compatibility.required_context_fields_csv="retest_price";
      UCEI03_AddParameter(d,"offset_points",UCEI03_PARAM_DECIMAL,"0","0","10000","points","none","","");
      UCEI03_AddParameter(d,"ttl_ms",UCEI03_PARAM_INTEGER,"600000","1","86400000","milliseconds","none","","");
   }
   else if(d.atom_id=="entry.stop_limit_hybrid"){
      d.compatibility.required_context_fields_csv="reference_price";
      UCEI03_AddParameter(d,"trigger_buffer_points",UCEI03_PARAM_DECIMAL,"2","0","10000","points","none","","");
      UCEI03_AddParameter(d,"limit_slip_points",UCEI03_PARAM_DECIMAL,"5","0","10000","points","none","","");
      UCEI03_AddParameter(d,"ttl_ms",UCEI03_PARAM_INTEGER,"300000","1","86400000","milliseconds","none","","");
   }
   else if(d.atom_id=="entry.time_window"){
      UCEI03_AddParameter(d,"delay_ms",UCEI03_PARAM_INTEGER,"0","0","86400000","milliseconds","none","","");
      UCEI03_AddParameter(d,"window_ms",UCEI03_PARAM_INTEGER,"60000","1","86400000","milliseconds","none","","");
   }
   else if(d.atom_id=="stop.catastrophic"){
      UCEI03_AddParameter(d,"distance_points",UCEI03_PARAM_DECIMAL,"500","1","10000000","points","increasing","","");
   }
   else if(d.atom_id=="stop.context_boundary"){
      d.compatibility.required_context_fields_csv="context_high,context_low";
      UCEI03_AddParameter(d,"buffer_points",UCEI03_PARAM_DECIMAL,"2","0","100000","points","none","","");
   }
   else if(d.atom_id=="stop.fixed_distance"){
      UCEI03_AddParameter(d,"distance_points",UCEI03_PARAM_DECIMAL,"100","1","1000000","points","increasing","","");
   }
   else if(d.atom_id=="stop.hybrid"){
      d.compatibility.required_context_fields_csv="structural_stop";
      UCEI03_AddParameter(d,"buffer_points",UCEI03_PARAM_DECIMAL,"2","0","100000","points","none","","");
      UCEI03_AddParameter(d,"max_distance_points",UCEI03_PARAM_DECIMAL,"250","1","1000000","points","none","","");
   }
   else if(d.atom_id=="stop.signal_bar"){
      d.compatibility.required_context_fields_csv="signal_high,signal_low";
      UCEI03_AddParameter(d,"buffer_points",UCEI03_PARAM_DECIMAL,"1","0","100000","points","none","","");
   }
   else if(d.atom_id=="stop.structural"){
      d.compatibility.required_context_fields_csv="structural_stop";
      UCEI03_AddParameter(d,"buffer_points",UCEI03_PARAM_DECIMAL,"2","0","100000","points","none","","");
   }
   else if(d.atom_id=="stop.time"){
      UCEI03_AddParameter(d,"holding_ms",UCEI03_PARAM_INTEGER,"3600000","1","604800000","milliseconds","none","","");
   }
   else if(d.atom_id=="stop.volatility"){
      d.compatibility.required_context_fields_csv="atr";
      UCEI03_AddParameter(d,"atr_multiple",UCEI03_PARAM_DECIMAL,"1.5","0.05","50","multiple","increasing","","");
      UCEI03_AddParameter(d,"minimum_points",UCEI03_PARAM_DECIMAL,"10","0","100000","points","none","","");
   }
   else if(d.atom_id=="target.capped_runner"){
      UCEI03_AddParameter(d,"cap_r",UCEI03_PARAM_DECIMAL,"8","0.1","1000","R","none","","");
      UCEI03_AddParameter(d,"risk_points",UCEI03_PARAM_DECIMAL,"100","0.1","1000000","points","none","","");
   }
   else if(d.atom_id=="target.context_endpoint"){
      d.compatibility.required_context_fields_csv="context_high,context_low";
      UCEI03_AddParameter(d,"buffer_points",UCEI03_PARAM_DECIMAL,"0","0","100000","points","none","","");
   }
   else if(d.atom_id=="target.fixed_r"){
      UCEI03_AddParameter(d,"reward_multiple",UCEI03_PARAM_DECIMAL,"2","0.05","100","R","increasing","","");
      UCEI03_AddParameter(d,"risk_points",UCEI03_PARAM_DECIMAL,"100","0.1","1000000","points","none","","");
   }
   else if(d.atom_id=="target.multi_ladder"){
      UCEI03_AddParameter(d,"first_r",UCEI03_PARAM_DECIMAL,"1","0.05","100","R","none","","");
      UCEI03_AddParameter(d,"step_r",UCEI03_PARAM_DECIMAL,"1","0.05","100","R","none","","");
      UCEI03_AddParameter(d,"leg_count",UCEI03_PARAM_INTEGER,"3","2","8","count","none","","");
      UCEI03_AddParameter(d,"risk_points",UCEI03_PARAM_DECIMAL,"100","0.1","1000000","points","none","","");
   }
   else if(d.atom_id=="target.runner"){
      UCEI03_AddParameter(d,"runner_fraction",UCEI03_PARAM_DECIMAL,"1","0.01","1","fraction","none","","");
   }
   else if(d.atom_id=="target.structural"){
      d.compatibility.required_context_fields_csv="structural_target";
      UCEI03_AddParameter(d,"buffer_points",UCEI03_PARAM_DECIMAL,"0","0","100000","points","none","","");
   }
   else if(d.atom_id=="target.volatility"){
      d.compatibility.required_context_fields_csv="atr";
      UCEI03_AddParameter(d,"atr_multiple",UCEI03_PARAM_DECIMAL,"2","0.05","100","multiple","increasing","","");
   }
   else if(d.atom_id=="trailing.activation_conditioned"){
      UCEI03_AddParameter(d,"activation_r",UCEI03_PARAM_DECIMAL,"2","0","100","R","none","","");
      UCEI03_AddParameter(d,"distance_points",UCEI03_PARAM_DECIMAL,"50","0.1","1000000","points","none","","");
      UCEI03_AddParameter(d,"cadence_ms",UCEI03_PARAM_INTEGER,"1000","0","86400000","milliseconds","none","","");
   }
   else if(d.atom_id=="trailing.atr"){
      d.compatibility.required_context_fields_csv="atr";
      UCEI03_AddParameter(d,"activation_r",UCEI03_PARAM_DECIMAL,"1","0","100","R","none","","");
      UCEI03_AddParameter(d,"atr_multiple",UCEI03_PARAM_DECIMAL,"2","0.05","100","multiple","none","","");
   }
   else if(d.atom_id=="trailing.break_even"){
      UCEI03_AddParameter(d,"activation_r",UCEI03_PARAM_DECIMAL,"1","0","100","R","none","","");
      UCEI03_AddParameter(d,"offset_points",UCEI03_PARAM_DECIMAL,"0","0","100000","points","none","","");
   }
   else if(d.atom_id=="trailing.chandelier"){
      d.compatibility.required_context_fields_csv="atr,swing_high,swing_low";
      UCEI03_AddParameter(d,"activation_r",UCEI03_PARAM_DECIMAL,"1","0","100","R","none","","");
      UCEI03_AddParameter(d,"atr_multiple",UCEI03_PARAM_DECIMAL,"3","0.05","100","multiple","none","","");
   }
   else if(d.atom_id=="trailing.context_state"){
      d.compatibility.required_context_fields_csv="context_high,context_low";
      UCEI03_AddParameter(d,"activation_r",UCEI03_PARAM_DECIMAL,"0","0","100","R","none","","");
      UCEI03_AddParameter(d,"buffer_points",UCEI03_PARAM_DECIMAL,"1","0","100000","points","none","","");
   }
   else if(d.atom_id=="trailing.none"){
   }
   else if(d.atom_id=="trailing.opposite_signal"){
      UCEI03_AddParameter(d,"activation_r",UCEI03_PARAM_DECIMAL,"0","0","100","R","none","","");
   }
   else if(d.atom_id=="trailing.profit_lock"){
      UCEI03_AddParameter(d,"activation_r",UCEI03_PARAM_DECIMAL,"1.5","0","100","R","none","","");
      UCEI03_AddParameter(d,"lock_r",UCEI03_PARAM_DECIMAL,"0.5","0","100","R","none","","");
   }
   else if(d.atom_id=="trailing.swing_node"){
      d.compatibility.required_context_fields_csv="swing_high,swing_low";
      UCEI03_AddParameter(d,"activation_r",UCEI03_PARAM_DECIMAL,"1","0","100","R","none","","");
      UCEI03_AddParameter(d,"buffer_points",UCEI03_PARAM_DECIMAL,"2","0","100000","points","none","","");
   }
   else if(d.atom_id=="trailing.time_step"){
      UCEI03_AddParameter(d,"activation_r",UCEI03_PARAM_DECIMAL,"0.5","0","100","R","none","","");
      UCEI03_AddParameter(d,"step_ms",UCEI03_PARAM_INTEGER,"300000","1","86400000","milliseconds","none","","");
      UCEI03_AddParameter(d,"lock_increment_r",UCEI03_PARAM_DECIMAL,"0.25","0","100","R","none","","");
   }
   else if(d.atom_id=="management.cancel_remaining"){
      UCEI03_AddParameter(d,"after_fill_fraction",UCEI03_PARAM_DECIMAL,"0.5","0","1","fraction","none","","");
   }
   else if(d.atom_id=="management.evidence_add_on"){
      UCEI03_AddParameter(d,"minimum_confidence",UCEI03_PARAM_DECIMAL,"0.75","0","1","probability","none","","");
      UCEI03_AddParameter(d,"quantity_fraction",UCEI03_PARAM_DECIMAL,"0.25","0.01","1","fraction","none","","");
   }
   else if(d.atom_id=="management.forced_flatten"){
      UCEI03_AddParameter(d,"trigger_tag",UCEI03_PARAM_STRING,"operator_kill","","","unitless","none","","");
   }
   else if(d.atom_id=="management.market_state_guard"){
      UCEI03_AddParameter(d,"max_spread_points",UCEI03_PARAM_DECIMAL,"50","0","100000","points","none","","");
      UCEI03_AddParameter(d,"action",UCEI03_PARAM_ENUM,"block_add","","","unitless","none","block_add,reduce,flatten","");
   }
   else if(d.atom_id=="management.max_holding_time"){
      UCEI03_AddParameter(d,"holding_ms",UCEI03_PARAM_INTEGER,"14400000","1","604800000","milliseconds","none","","");
   }
   else if(d.atom_id=="management.partial_exit_r"){
      UCEI03_AddParameter(d,"activation_r",UCEI03_PARAM_DECIMAL,"1","0","100","R","none","","");
      UCEI03_AddParameter(d,"quantity_fraction",UCEI03_PARAM_DECIMAL,"0.5","0.01","1","fraction","none","","");
   }
   else if(d.atom_id=="management.scale_out_ladder"){
      UCEI03_AddParameter(d,"first_r",UCEI03_PARAM_DECIMAL,"1","0","100","R","none","","");
      UCEI03_AddParameter(d,"step_r",UCEI03_PARAM_DECIMAL,"1","0.01","100","R","none","","");
      UCEI03_AddParameter(d,"leg_count",UCEI03_PARAM_INTEGER,"3","2","8","count","none","","");
   }
   else if(d.atom_id=="management.session_close"){
      d.compatibility.required_context_fields_csv="session_close_ms";
      UCEI03_AddParameter(d,"lead_ms",UCEI03_PARAM_INTEGER,"300000","0","86400000","milliseconds","none","","");
   }
   else if(d.atom_id=="sizing.capped_fractional_kelly"){
      d.compatibility.required_context_fields_csv="account_equity";
      UCEI03_AddParameter(d,"kelly_fraction",UCEI03_PARAM_DECIMAL,"0.25","0","1","fraction","none","","");
      UCEI03_AddParameter(d,"maximum_equity_fraction",UCEI03_PARAM_DECIMAL,"0.02","0","1","fraction","none","","");
   }
   else if(d.atom_id=="sizing.confidence_scaling"){
      UCEI03_AddParameter(d,"base_cash",UCEI03_PARAM_DECIMAL,"100","0","1000000000","account_currency","none","","");
      UCEI03_AddParameter(d,"floor_confidence",UCEI03_PARAM_DECIMAL,"0.5","0","1","probability","none","","");
      UCEI03_AddParameter(d,"ceiling_confidence",UCEI03_PARAM_DECIMAL,"0.9","0","1","probability","none","","");
   }
   else if(d.atom_id=="sizing.drawdown_scaling"){
      UCEI03_AddParameter(d,"base_cash",UCEI03_PARAM_DECIMAL,"100","0","1000000000","account_currency","none","","");
      UCEI03_AddParameter(d,"minimum_scale",UCEI03_PARAM_DECIMAL,"0.1","0","1","fraction","none","","");
      UCEI03_AddParameter(d,"maximum_drawdown",UCEI03_PARAM_DECIMAL,"0.2","0.0001","1","fraction","none","","");
   }
   else if(d.atom_id=="sizing.equity_fraction"){
      d.compatibility.required_context_fields_csv="account_equity";
      UCEI03_AddParameter(d,"fraction",UCEI03_PARAM_DECIMAL,"0.01","0","1","fraction","none","","");
   }
   else if(d.atom_id=="sizing.fixed_cash"){
      UCEI03_AddParameter(d,"cash_amount",UCEI03_PARAM_DECIMAL,"100","0","1000000000","account_currency","none","","");
   }
   else if(d.atom_id=="sizing.fixed_volume"){
      UCEI03_AddParameter(d,"volume",UCEI03_PARAM_DECIMAL,"0.1","0","1000000","lots","none","","");
   }
   else if(d.atom_id=="sizing.portfolio_budget"){
      d.compatibility.required_context_fields_csv="portfolio_budget";
      UCEI03_AddParameter(d,"share",UCEI03_PARAM_DECIMAL,"0.1","0","1","fraction","none","","");
   }
   else if(d.atom_id=="sizing.risk_tier"){
      UCEI03_AddParameter(d,"low_cash",UCEI03_PARAM_DECIMAL,"50","0","1000000000","account_currency","none","","");
      UCEI03_AddParameter(d,"medium_cash",UCEI03_PARAM_DECIMAL,"100","0","1000000000","account_currency","none","","");
      UCEI03_AddParameter(d,"high_cash",UCEI03_PARAM_DECIMAL,"200","0","1000000000","account_currency","none","","");
      UCEI03_AddParameter(d,"medium_confidence",UCEI03_PARAM_DECIMAL,"0.6","0","1","probability","none","","");
      UCEI03_AddParameter(d,"high_confidence",UCEI03_PARAM_DECIMAL,"0.8","0","1","probability","none","","");
   }
   else if(d.atom_id=="sizing.volatility_target"){
      d.compatibility.required_context_fields_csv="realized_volatility";
      UCEI03_AddParameter(d,"target_volatility",UCEI03_PARAM_DECIMAL,"0.01","0","10","fraction","none","","");
      UCEI03_AddParameter(d,"base_cash",UCEI03_PARAM_DECIMAL,"100","0","1000000000","account_currency","none","","");
   }
}
bool UCEI03_RegisterNames(CUCEI03ExactRegistry &r,const ENUM_UCEI03_ATOM_KIND kind,const string ids[],const string families[],string &error){for(int i=0;i<ArraySize(ids);i++){UCEI03_AtomDescriptor d;UCEI03_InitDescriptor(d,ids[i],kind,families[i],ids[i]+" canonical atom");UCEI03_ApplyParameterSchema(d);if(!r.Register(d,error))return false;}return true;}
class CUCEI03Catalog{
public:CUCEI03ExactRegistry entry;CUCEI03ExactRegistry stop;CUCEI03ExactRegistry target;CUCEI03ExactRegistry trailing;CUCEI03ExactRegistry management;CUCEI03ExactRegistry sizing;
CUCEI03Catalog():entry(UCEI03_ENTRY),stop(UCEI03_STOP),target(UCEI03_TARGET),trailing(UCEI03_TRAILING),management(UCEI03_MANAGEMENT),sizing(UCEI03_SIZING){}
bool Build(string &error){string e[] ={"entry.immediate_market","entry.passive_limit","entry.breakout_stop","entry.confirmation_market","entry.retest_limit","entry.ladder","entry.stop_limit_hybrid","entry.time_window"};string ef[]={"immediate","passive","breakout","confirmation","retest","ladder","hybrid","time_window"};string s[]={"stop.fixed_distance","stop.structural","stop.signal_bar","stop.context_boundary","stop.volatility","stop.catastrophic","stop.time","stop.hybrid"};string sf[]={"fixed","structural","signal_bar","context_boundary","volatility","catastrophic","time","hybrid"};string t[]={"target.fixed_r","target.structural","target.context_endpoint","target.volatility","target.multi_ladder","target.runner","target.capped_runner"};string tf[]={"fixed_r","structural","context_endpoint","volatility","ladder","runner","runner"};string tr[]={"trailing.none","trailing.break_even","trailing.profit_lock","trailing.swing_node","trailing.atr","trailing.chandelier","trailing.time_step","trailing.context_state","trailing.opposite_signal","trailing.activation_conditioned"};string trf[]={"none","break_even","profit_lock","swing_node","volatility","chandelier","time_step","context_state","opposite_signal","activation_conditioned"};string m[]={"management.partial_exit_r","management.scale_out_ladder","management.evidence_add_on","management.cancel_remaining","management.max_holding_time","management.session_close","management.market_state_guard","management.forced_flatten"};string mf[]={"partial_exit","scale_out","add_on","cancel_remaining","time_exit","session_close","guard","forced_flatten"};string z[]={"sizing.fixed_cash","sizing.equity_fraction","sizing.fixed_volume","sizing.risk_tier","sizing.capped_fractional_kelly","sizing.volatility_target","sizing.drawdown_scaling","sizing.confidence_scaling","sizing.portfolio_budget"};string zf[]={"fixed_cash","equity_fraction","fixed_volume","risk_tier","kelly","volatility_target","drawdown","confidence","portfolio_budget"};if(!UCEI03_RegisterNames(entry,UCEI03_ENTRY,e,ef,error)||!UCEI03_RegisterNames(stop,UCEI03_STOP,s,sf,error)||!UCEI03_RegisterNames(target,UCEI03_TARGET,t,tf,error)||!UCEI03_RegisterNames(trailing,UCEI03_TRAILING,tr,trf,error)||!UCEI03_RegisterNames(management,UCEI03_MANAGEMENT,m,mf,error)||!UCEI03_RegisterNames(sizing,UCEI03_SIZING,z,zf,error))return false;entry.Freeze();stop.Freeze();target.Freeze();trailing.Freeze();management.Freeze();sizing.Freeze();error="";return true;}int Count()const{return entry.Count()+stop.Count()+target.Count()+trailing.Count()+management.Count()+sizing.Count();}
};
#endif
