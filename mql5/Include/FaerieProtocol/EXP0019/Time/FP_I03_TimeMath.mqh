#ifndef __EXP0019_FP_I03_TIME_MATH_MQH__
#define __EXP0019_FP_I03_TIME_MATH_MQH__

#include <DayeTrader/EXP0018/DAYE_Time.mqh>
#include <FaerieProtocol/EXP0019/Core/FP_I02_Hash.mqh>
#include "FP_I03_Config.mqh"

DAYE_LocalResolutionPolicy FP_I03_ToDAYEPolicy(const FP_I03_LocalResolutionPolicy policy)
  {
   if(policy==FP_I03_LOCAL_EARLIEST)return DAYE_LOCAL_EARLIEST;
   if(policy==FP_I03_LOCAL_LATEST)return DAYE_LOCAL_LATEST;
   return DAYE_LOCAL_REJECT;
  }

void FP_I03_BuildDAYEConfig(const FP_I03_TimeKernelConfig &source,DAYE_TimeConfig &target)
  {
   target.schema_version=DAYE_TIME_SCHEMA_VERSION;
   target.broker_offset_mode=DAYE_BROKER_OFFSET_MANUAL_FIXED;
   target.broker_utc_offset_minutes=0;
   target.ny_offset_mode=DAYE_NY_AUTO_US_DST;
   target.manual_new_york_utc_offset_minutes=-300;
   target.ambiguous_start_policy=FP_I03_ToDAYEPolicy(source.ambiguous_start_policy);
   target.ambiguous_end_policy=FP_I03_ToDAYEPolicy(source.ambiguous_end_policy);
  }

string FP_I03_LocalIso(const datetime value)
  {
   MqlDateTime p;ZeroMemory(p);
   if(!TimeToStruct(value,p))return "";
   return StringFormat("%04d-%02d-%02dT%02d:%02d:%02d",p.year,p.mon,p.day,p.hour,p.min,p.sec);
  }

bool FP_I03_UtcToNewYork(const datetime utc_time,const FP_I03_TimeKernelConfig &config,FP_I03_NyTimestamp &result,string &reason)
  {
   ZeroMemory(result);reason="";
   MqlDateTime utc_parts;ZeroMemory(utc_parts);
   if(!TimeToStruct(utc_time,utc_parts) || utc_parts.year<config.minimum_supported_year || utc_parts.year>config.maximum_supported_year)
     {reason="FP_TRC_YEAR_UNSUPPORTED";return false;}
   DAYE_TimeConfig daye;FP_I03_BuildDAYEConfig(config,daye);
   bool is_dst=false;int offset=0;int fold=0;datetime ny=0;
   if(!DAYE_UtcToNewYork(utc_time,daye,ny,is_dst,offset,fold,reason))return false;
   result.utc_time=utc_time;result.ny_time=ny;result.local_iso=FP_I03_LocalIso(ny);result.local_date=DAYE_DateKey(ny);
   result.second_of_day=DAYE_SecondOfDay(ny);result.utc_offset_minutes=offset;
   result.dst_regime=is_dst ? FP_I03_DST_DAYLIGHT : FP_I03_DST_STANDARD;result.fold=fold;
   result.timestamp_id=FP_I02_CompactId("FPNYTS",IntegerToString((long)utc_time)+"|"+result.local_iso+"|"+IntegerToString(offset)+"|"+IntegerToString(fold)+"|"+config.time_rule_version);
   return true;
  }

bool FP_I03_ResolveLocal(const datetime local_ny,const FP_I03_LocalResolutionPolicy policy,const FP_I03_TimeKernelConfig &config,FP_I03_LocalResolution &result)
  {
   ZeroMemory(result);result.local_iso=FP_I03_LocalIso(local_ny);result.policy=policy;
   DAYE_TimeConfig daye;FP_I03_BuildDAYEConfig(config,daye);
   datetime candidates[];int count=DAYE_CollectUtcCandidatesForNyLocal(local_ny,daye,candidates);
   result.candidate_count=count;
   if(count==0)
     {result.status=FP_I03_LOCAL_NONEXISTENT;result.reason_code="FP_TRC_LOCAL_NONEXISTENT";}
   else if(count==1)
     {result.status=FP_I03_LOCAL_UNIQUE;result.candidate_utc_earliest=candidates[0];result.candidate_utc_latest=candidates[0];result.selected_utc=candidates[0];result.reason_code="FP_TRC_LOCAL_UNIQUE";}
   else
     {
      result.status=FP_I03_LOCAL_AMBIGUOUS;result.candidate_utc_earliest=candidates[0];result.candidate_utc_latest=candidates[count-1];
      if(policy==FP_I03_LOCAL_EARLIEST){result.selected_utc=candidates[0];result.reason_code="FP_TRC_LOCAL_AMBIGUOUS_EARLIEST";}
      else if(policy==FP_I03_LOCAL_LATEST){result.selected_utc=candidates[count-1];result.reason_code="FP_TRC_LOCAL_AMBIGUOUS_LATEST";}
      else {result.selected_utc=0;result.reason_code="FP_TRC_LOCAL_AMBIGUOUS_REJECTED";}
     }
   result.resolution_id=FP_I02_CompactId("FPLOCAL",result.local_iso+"|"+IntegerToString((int)result.status)+"|"+IntegerToString((long)result.selected_utc)+"|"+IntegerToString((int)policy)+"|"+config.time_rule_version);
   return (result.selected_utc>0);
  }

bool FP_I03_BrokerToUtc(const datetime broker_time,const int broker_offset_minutes,datetime &utc_time,string &reason)
  {
   reason="";
   if(broker_time<=0){reason="FP_TRC_TIMESTAMP_INVALID";return false;}
   if(broker_offset_minutes<-840 || broker_offset_minutes>840){reason="FP_TRC_BROKER_OFFSET_INVALID";return false;}
   utc_time=broker_time-(datetime)(broker_offset_minutes*60);
   return true;
  }

#endif
