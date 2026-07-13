#ifndef __EXP0019_FP_I02_IDENTITY_MQH__
#define __EXP0019_FP_I02_IDENTITY_MQH__

#include "FP_I02_Types.mqh"
#include "FP_I02_Hash.mqh"

string FP_I02_BoolText(const bool value) { return value ? "true" : "false"; }
string FP_I02_LongText(const long value) { return StringFormat("%I64d",value); }
string FP_I02_DoubleText(const double value) { return DoubleToString(value,10); }

string FP_I02_BuildPairId(const string symbol_a,const string symbol_b,const string version="1.0.0")
  {
   string first=symbol_a,second=symbol_b;
   if(StringCompare(first,second)>0) { string temp=first; first=second; second=temp; }
   return FP_I02_CompactId("FPPAIR","symbols="+first+","+second+"|version="+version);
  }

string FP_I02_BuildWindowId(const FP_I02_WindowKey &value)
  {
   string material=StringFormat("context=%s|pair=%s|kind=%d|scope=%d|day=%s|start=%I64d|end=%I64d|tz=%s|offset=%d|week=%s|revision=%s",
      value.context_id,value.pair_id,(int)value.kind,(int)value.scope,value.trading_day_id,value.start_utc_ms,value.end_utc_ms,
      value.timezone,value.calendar_offset,value.week_id,value.data_revision);
   return FP_I02_CompactId("FPWIN",material);
  }

string FP_I02_BuildReferenceSideId(const FP_I02_ReferenceSideKey &value)
  {
   return FP_I02_CompactId("FPREF",StringFormat("window=%s|symbol=%s|side=%d|price=%s|revision=%s",
      value.window_id,value.symbol,(int)value.side,FP_I02_DoubleText(value.price),value.data_revision));
  }

string FP_I02_BuildQuotaKeyId(const FP_I02_QuotaKey &value)
  {
   return FP_I02_CompactId("FPQUOTA",StringFormat("epoch=%s|day=%s|pair=%s|session=%d",
      value.context_epoch_id,value.trading_day_id,value.pair_id,(int)value.session));
  }

string FP_I02_BuildProjectionId(const string signal_id,const string projection_config_hash,const string object_role,const string chart_instance_id)
  {
   return FP_I02_CompactId("FPPROJ","domain=FP_PROJECTION|signal="+signal_id+"|config="+projection_config_hash+"|role="+object_role+"|chart="+chart_instance_id);
  }

#endif
